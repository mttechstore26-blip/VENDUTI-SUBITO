"""Run the original Vinted UI in staging, with its database redirected to a snapshot.

The original repository is not modified. Collector, proxy and init_db are never run.
"""
from pathlib import Path
import sys
import streamlit as st

VENDOR = Path("/opt/mt-tech-venduti-staging/vendor")
SOURCE = Path("/opt/vinted-venduti")
SNAPSHOT = Path("/opt/mt-tech-venduti-staging/data/vinted_market_preview.db")

def run_vinted_original():
    if not SNAPSHOT.is_file():
        st.error("Snapshot Vinted mancante: non verrà usato il database di produzione.")
        return
    app = SOURCE / "app.py"
    if not app.is_file():
        st.error("Dashboard Vinted originale non trovata.")
        return
    # Imports must resolve to Vinted's own config/classifier/database modules.
    if VENDOR.is_dir() and str(VENDOR) not in sys.path:
        sys.path.insert(0, str(VENDOR))
    if str(SOURCE) not in sys.path:
        sys.path.insert(0, str(SOURCE))
    import config as vinted_config
    code = app.read_text(encoding="utf-8")
    required = (
        "st.set_page_config(page_title=APP_TITLE, page_icon=\"🟢\", layout=\"wide\")",
        "init_db()",
    )
    if not all(marker in code for marker in required):
        st.error("Versione Vinted non riconosciuta: avvio annullato per sicurezza.")
        return
    code = code.replace(required[0], "# page config is owned by unified_app", 1)
    code = code.replace("\ninit_db()\n", "\n# schema migrations disabled in preview\n", 1)
    old_db = vinted_config.DB_PATH
    try:
        vinted_config.DB_PATH = SNAPSHOT
        exec(compile(code, str(app), "exec"), {"__name__": "__vinted_preview__", "__file__": str(app)})
    finally:
        vinted_config.DB_PATH = old_db
