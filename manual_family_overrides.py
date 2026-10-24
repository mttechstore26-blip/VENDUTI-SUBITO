"""Persistenza delle correzioni manuali delle famiglie Venduti Subito.

Le correzioni sono indicizzate dall'ID di Subito nell'URL e sono applicate
dopo la classificazione automatica. Non modificano i dati originali.
"""
import os
import re
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / ".cache" / "manual_families.sqlite"


def listing_id(url):
    match = re.search(r"-(\d{7,15})(?:\.htm)?(?:[?#]|$)", str(url or ""))
    return match.group(1) if match else None


def _connect():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DATABASE_PATH), timeout=10)
    conn.execute("PRAGMA busy_timeout=10000")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS family_overrides ("
        "listing_id TEXT PRIMARY KEY, family TEXT NOT NULL, "
        "updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
    )
    return conn


def get_overrides():
    with _connect() as conn:
        return dict(conn.execute("SELECT listing_id, family FROM family_overrides"))


def save_override(url, family):
    item_id = listing_id(url)
    family = str(family or "").strip()
    if not item_id:
        raise ValueError("L'annuncio non ha un ID Subito riconoscibile.")
    if not family or len(family) > 120 or any(ord(c) < 32 for c in family):
        raise ValueError("Il nome famiglia deve avere 1-120 caratteri.")
    with _connect() as conn:
        conn.execute(
            "INSERT INTO family_overrides(listing_id, family) VALUES (?, ?) "
            "ON CONFLICT(listing_id) DO UPDATE SET "
            "family=excluded.family, updated_at=CURRENT_TIMESTAMP",
            (item_id, family),
        )



def save_overrides(urls, family):
    """Assegna più annunci alla stessa famiglia con un'unica transazione."""
    family = str(family or "").strip()
    if not family or len(family) > 120 or any(ord(c) < 32 for c in family):
        raise ValueError("Il nome famiglia deve avere 1-120 caratteri.")
    ids = list(dict.fromkeys(listing_id(url) for url in urls))
    if not ids or any(item_id is None for item_id in ids):
        raise ValueError("La selezione contiene annunci senza ID Subito valido.")
    with _connect() as conn:
        conn.executemany(
            "INSERT INTO family_overrides(listing_id, family) VALUES (?, ?) "
            "ON CONFLICT(listing_id) DO UPDATE SET "
            "family=excluded.family, updated_at=CURRENT_TIMESTAMP",
            [(item_id, family) for item_id in ids],
        )
    return len(ids)


def delete_override(url):
    item_id = listing_id(url)
    if not item_id:
        raise ValueError("L'annuncio non ha un ID Subito riconoscibile.")
    with _connect() as conn:
        conn.execute("DELETE FROM family_overrides WHERE listing_id=?", (item_id,))


def editor_authorized(password):
    from hmac import compare_digest
    expected = os.environ.get("SUBITO_EDITOR_PASSWORD", "")
    return bool(expected) and compare_digest(str(password or ""), expected)
