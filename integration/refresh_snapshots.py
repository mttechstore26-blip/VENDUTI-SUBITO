#!/usr/bin/env python3
"""Coherent SQLite snapshots for MT TECH staging. Never write into production databases.

Run from systemd timer every 5 minutes; use the same host Python interpreter.
"""
import fcntl
import os
import sqlite3
import tempfile
from pathlib import Path

STAGING = Path("/opt/mt-tech-venduti-staging/data")
LOCK = Path("/tmp/mttech-snapshot-refresh.lock")
SOURCES = {
    "vinted_market_preview.db": Path("/opt/vinted-venduti/data/vinted_market.db"),
    "ebay_sold_preview.db": Path(os.getenv("MTTECH_EBAY_SOURCE_DB", "/opt/venduti-ebay/venduti-ebay/data/ebay_sold.db")),
}

def copy_sqlite(source, target):
    if not source.is_file():
        raise FileNotFoundError(f"Database sorgente mancante: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".snapshot-",suffix=".db",dir=target.parent)
    os.close(fd)
    temp = Path(temp_name)
    try:
        with sqlite3.connect(f"file:{source}?mode=ro",uri=True,timeout=10) as src:
            src.execute("PRAGMA query_only=ON")
            with sqlite3.connect(temp,timeout=10) as dst:
                src.backup(dst, pages=500, sleep=0.1)
                if dst.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                    raise RuntimeError(f"Integrità copia non valida: {source}")
        temp.chmod(0o640)
        os.replace(temp,target)
        print(f"Snapshot OK: {target} ({target.stat().st_size:,} byte)")
    finally:
        temp.unlink(missing_ok=True)

def main():
    with LOCK.open("w") as lock:
        try:
            fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Aggiornamento già in corso; salto esecuzione")
            return
        failures=[]
        for filename, source in SOURCES.items():
            try:
                copy_sqlite(source, STAGING/filename)
            except (OSError, sqlite3.Error, RuntimeError) as exc:
                print(f"ERRORE {filename}: {exc}")
                failures.append(filename)
        if failures:
            raise SystemExit(1)

if __name__=="__main__":
    main()
