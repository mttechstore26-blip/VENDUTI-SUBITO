"""MT TECH · Venduti: experimental multipage shell.

Subito pages run directly from their original files. Vinted and eBay are
placeholders until their imports and data writes have been isolated.
Do not replace production services before staging smoke tests.
"""
import streamlit as st

st.set_page_config(
    page_title="MT TECH · Venduti — Anteprima",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def vinted():
    st.title("🟢 Venduti Vinted")
    st.info("Integrazione Vinted in preparazione. Il servizio attuale resta invariato.")


def ebay():
    st.title("🔵 Venduti eBay")
    st.info("Integrazione eBay in preparazione. Il servizio attuale resta invariato.")


st.sidebar.title("MT TECH · Venduti")
st.sidebar.caption("Anteprima sperimentale — database separati")

# Streamlit executes only the selected page per rerun. The five existing
# Subito pages continue to use data_cache, family_cache and the same SQLite.
pages = {
    "Piattaforme": [
        st.Page(vinted, title="Vinted", icon="🟢", url_path="vinted"),
        st.Page(ebay, title="eBay", icon="🔵", url_path="ebay"),
    ],
    "Subito": [
        st.Page("app.py", title="Panoramica Subito", icon="🟠", url_path="subito", default=True),
        st.Page("pages/dashboard.py", title="Dashboard", icon="📊", url_path="subito-dashboard"),
        st.Page("pages/categorie.py", title="Categorie", icon="🎯", url_path="subito-categorie"),
        st.Page("pages/annunci.py", title="Annunci venduti", icon="📦", url_path="subito-annunci"),
        st.Page("pages/prezzi.py", title="Analisi prezzi", icon="💰", url_path="subito-prezzi"),
        st.Page("pages/trend.py", title="Trend", icon="📈", url_path="subito-trend"),
    ],
}
selected = st.navigation(pages, position="sidebar")
selected.run()
