"""Isolated Vinted staging dashboard: read-only SQLite snapshot, no imports from Vinted app.py."""
from pathlib import Path
import os
import sqlite3
import pandas as pd
import streamlit as st

ROOT = Path("/opt/mt-tech-venduti-staging").resolve()
DB = (ROOT / "data" / "vinted_market_preview.db").resolve()

def run_vinted_preview():
    st.title("🟢 Venduti Vinted")
    st.caption("Anteprima su copia SQLite · nessun reader, proxy o scrittura attivati")
    if not DB.is_file():
        st.warning("Copia Vinted non ancora presente: prepara lo snapshot SQLite in staging.")
        st.code(str(DB))
        return
    try:
        with sqlite3.connect(f"file:{DB}?mode=ro", uri=True) as conn:
            df = pd.read_sql_query(
                """SELECT vinted_id, title, brand, model, category, price,
                          status, sold_at, first_seen_at, url
                   FROM listings WHERE status = 'sold'
                   ORDER BY sold_at DESC LIMIT 1000""", conn)
            total = conn.execute("SELECT COUNT(*) FROM listings WHERE status='sold'").fetchone()[0]
    except (sqlite3.Error, pd.errors.DatabaseError) as exc:
        st.error(f"Errore lettura snapshot Vinted: {exc}")
        return
    a,b = st.columns(2)
    a.metric("Venduti registrati", f"{total:,}".replace(",", "."))
    b.metric("Annunci mostrati", len(df))
    if df.empty:
        st.info("Nessun venduto nello snapshot.")
        return
    category = st.selectbox("Categoria", ["Tutte"] + sorted(df["category"].dropna().unique().tolist()))
    if category != "Tutte":
        df = df[df["category"] == category]
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption("Vista di verifica: la dashboard Vinted completa sarà integrata dopo l'isolamento dei suoi moduli.")
