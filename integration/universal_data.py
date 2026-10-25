"""Read-only, bounded cross-platform sold listings for staging analytics."""
import re
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path("/opt/mt-tech-venduti-staging")
SOURCES = {
    "Vinted": ROOT / "data/vinted_market_preview.db",
    "eBay": ROOT / "data/ebay_sold_preview.db",
    "Subito": Path("/opt/mt-tech-telegram/data/market.db"),
}
# Bound reads and cache small results, not all database rows.
MAX_ROWS = 1200


def _read(path, query, params):
    with sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=5) as connection:
        connection.execute("PRAGMA query_only=ON")
        return pd.read_sql_query(query, connection, params=params)


@st.cache_data(ttl=120, max_entries=32, show_spinner=False)
def search_sold(term, days, limit=MAX_ROWS):
    terms = [token for token in re.split(r"\s+", term.strip()) if token][:6]
    if not terms:
        return pd.DataFrame(), {}
    limit = max(1, min(int(limit), MAX_ROWS))
    frames, statuses = [], {}
    for platform, path in SOURCES.items():
        if not path.is_file():
            statuses[platform] = "Database non disponibile"
            continue
        try:
            # Parameterized AND search; no table scans while user is not searching.
            clause = " AND ".join("LOWER(COALESCE(title,'')) LIKE ?" for _ in terms)
            params = [f"%{t.lower()}%" for t in terms]
            if platform == "Vinted":
                sql = f"""SELECT title,price,category,sold_at AS sold_date,url,
                       condition AS condition_label,model AS model_label
                       FROM listings WHERE status='sold' AND {clause}
                       ORDER BY sold_at DESC LIMIT ?"""
            elif platform == "eBay":
                sql = f"""SELECT title,sold_price AS price,category_id AS category,
                       ended_at AS sold_date,url,NULL AS condition_label,
                       NULL AS model_label
                       FROM sales WHERE {clause}
                       ORDER BY ended_at DESC LIMIT ?"""
            else:
                sql = f"""SELECT l.title,l.price,
                       COALESCE(m.name,'') AS category,
                       l.detected_sold_at AS sold_date,l.url,
                       NULL AS condition_label,NULL AS model_label
                       FROM listings l LEFT JOIN monitorings m ON m.id=l.monitoring_id
                       WHERE l.detected_sold_at IS NOT NULL AND
                       {" AND ".join("LOWER(COALESCE(l.title,'')) LIKE ?" for _ in terms)}
                       ORDER BY l.detected_sold_at DESC LIMIT ?"""
            data = _read(path, sql, params + [limit])
            if not data.empty:
                data["platform"] = platform
                frames.append(data)
            statuses[platform] = f"{len(data)} risultati caricati (massimo {limit})"
        except (sqlite3.Error, ValueError) as exc:
            statuses[platform] = f"Errore lettura: {type(exc).__name__}"
    if not frames:
        return pd.DataFrame(), statuses
    result = pd.concat(frames, ignore_index=True)
    result["price"] = pd.to_numeric(result["price"], errors="coerce")
    result["sold_date"] = pd.to_datetime(result["sold_date"], utc=True, errors="coerce")
    if days:
        cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=int(days))
        result = result[result["sold_date"] >= cutoff]
    result = result[result["price"].notna() & result["price"].gt(0)].copy()
    return result.sort_values("sold_date", ascending=False), statuses


def aggregate_by_platform(rows):
    if rows.empty:
        return pd.DataFrame()
    return (rows.groupby("platform", as_index=False)
            .agg(venduti=("price","size"),mediana=("price","median"),
                 media=("price","mean"),minimo=("price","min"),
                 massimo=("price","max"))
            .sort_values("platform"))
