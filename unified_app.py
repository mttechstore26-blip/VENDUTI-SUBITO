"""MT TECH · Venduti — staging navigation.

Each selected page runs only once. The legacy Subito app.py is not included:
it calls st.navigation internally and would replace the unified menu.
Vinted and eBay remain placeholders pending isolated module integration.
"""
import streamlit as st

st.set_page_config(
    page_title="MT TECH · Venduti — Anteprima",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def vinted():
    from integration.vinted_preview import run_vinted_preview

    run_vinted_preview()


def ebay():
    from integration.ebay_adapter import run_ebay_preview

    run_ebay_preview()


platform_pages = [
    st.Page(vinted, title="Vinted", icon="🟢", url_path="vinted"),
    st.Page(ebay, title="eBay", icon="🔵", url_path="ebay"),
]
subito_pages = [
    st.Page("pages/categorie.py", title="Categorie", icon="🎯", url_path="subito-categorie", default=True),
    st.Page("pages/annunci.py", title="Annunci venduti", icon="📦", url_path="subito-annunci"),
    st.Page("pages/prezzi.py", title="Analisi prezzi", icon="💰", url_path="subito-prezzi"),
    st.Page("pages/trend.py", title="Trend", icon="📈", url_path="subito-trend"),
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊", url_path="subito-dashboard"),
]

# Hide native navigation; render one consistently ordered platform sidebar.
page = st.navigation(platform_pages + subito_pages, position="hidden")

with st.sidebar:
    st.title("MT TECH · Venduti")
    st.caption("Anteprima sperimentale")
    st.subheader("Piattaforme")
    for destination in platform_pages:
        st.page_link(destination)
    st.divider()
    st.subheader("Venduti Subito")
    for destination in subito_pages:
        st.page_link(destination)

page.run()
