"""Staging-only adapter for the existing Venduti eBay Streamlit script.

Runs in the unified Streamlit process against a *copy* of eBay's SQLite
database. Neither collector nor production DB is changed.
"""
from __future__ import annotations

import os
from pathlib import Path
import runpy
import sys

import streamlit as st


def run_ebay_preview() -> None:
    repo_dir = Path(os.environ.get(
        "MT_TECH_EBAY_DIR", "/opt/venduti-ebay/venduti-ebay"
    )).resolve()
    script = repo_dir / "dashboard.py"
    staging_root = Path("/opt/mt-tech-venduti-staging").resolve()
    preview_db = Path(os.environ.get(
        "MT_TECH_EBAY_PREVIEW_DB",
        str(staging_root / "data" / "ebay_sold_preview.db"),
    )).resolve()

    if not script.is_file():
        st.error(f"Dashboard eBay non trovata: {script}")
        st.stop()
    if not preview_db.is_relative_to(staging_root):
        st.error("Il database eBay di prova deve trovarsi nella cartella staging.")
        st.stop()
    if not preview_db.is_file():
        st.warning(
            "Database eBay di prova non ancora preparato. "
            "Crea uno snapshot SQLite nella cartella staging prima di aprire questa pagina."
        )
        st.code(str(preview_db))
        st.stop()

    st.caption("Modalità sperimentale: eBay utilizza una copia del database.")
    original_sys_path = sys.path[:]
    vendor_dir = staging_root / "vendor"
    saved_env = {key: os.environ.get(key) for key in ("DB_PATH", "SOLDCOMPS_API_KEY")}
    try:
        if vendor_dir.is_dir():
            sys.path.insert(0, str(vendor_dir))
        sys.path.insert(0, str(repo_dir))
        os.environ["DB_PATH"] = str(preview_db)
        # Do not call SoldComps merely to render the preview.
        os.environ["SOLDCOMPS_API_KEY"] = ""
        runpy.run_path(str(script), run_name="__page__")
    finally:
        sys.path[:] = original_sys_path
        for key, value in saved_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
