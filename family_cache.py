"""Cache SQLite persistente per famiglie, indipendente dal database di mercato."""
import hashlib
import inspect
import sqlite3
from pathlib import Path

CACHE_PATH = Path(__file__).resolve().parent / ".cache" / "families.sqlite"


def classify_with_disk_cache(titles, categories, classifier, normalizer):
    """Riutilizza risultati anche dopo restart; fallback sicuro se cache non disponibile."""
    pairs = [(str(t) if t is not None else "", str(c) if c is not None else "")
             for t, c in zip(titles, categories)]
    if not pairs:
        return []
    version = hashlib.sha256(
        (inspect.getsource(classifier.__wrapped__ if hasattr(classifier, "__wrapped__") else classifier)
         + inspect.getsource(normalizer.__wrapped__ if hasattr(normalizer, "__wrapped__") else normalizer)).encode()
    ).hexdigest()[:20]
    keys = [hashlib.sha256((version + "\0" + t + "\0" + c).encode()).hexdigest()
            for t, c in pairs]
    unique = dict(zip(keys, pairs))
    cached = {}
    conn = None
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(CACHE_PATH), timeout=5)
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("CREATE TABLE IF NOT EXISTS families (key TEXT PRIMARY KEY, family TEXT NOT NULL)")
        for start in range(0, len(unique), 400):
            chunk = list(unique)[start:start + 400]
            placeholders = ",".join("?" for _ in chunk)
            cached.update(conn.execute(
                f"SELECT key, family FROM families WHERE key IN ({placeholders})", chunk
            ).fetchall())
        missing = [(k, *pair) for k, pair in unique.items() if k not in cached]
        if missing:
            rows = [(k, classifier(title, category)) for k, title, category in missing]
            conn.executemany("INSERT OR REPLACE INTO families(key, family) VALUES (?, ?)", rows)
            conn.commit()
            cached.update(rows)
        return [cached[key] for key in keys]
    except (OSError, sqlite3.Error):
        # Risultati sempre corretti anche se il disco non è scrivibile.
        return [classifier(t, c) for t, c in pairs]
    finally:
        if conn is not None:
            conn.close()
