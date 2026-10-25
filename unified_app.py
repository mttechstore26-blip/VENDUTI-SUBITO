"""MT TECH · Venduti: experimental one-process navigation shell.

This is a navigation prototype, NOT a replacement for the three dashboards.
Legacy code is deliberately not imported until modules and writes are isolated.
"""
import streamlit as st

st.set_page_config(
    page_title="MT TECH · Venduti — Anteprima",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PLATFORMS = {
    "Vinted": ("🟢", "Categorie, brand, modelli e annunci venduti"),
    "eBay": ("🔵", "Vendite SoldComps, famiglie, modelli e prezzi"),
    "Subito": ("🟠", "Categorie, famiglie, annunci, prezzi e trend"),
}


def platform_page(name):
    icon, description = PLATFORMS[name]
    st.title(f"{icon} Venduti {name}")
    st.caption(description)
    st.info(
        "Anteprima della navigazione unificata. "
        "I dati e le funzioni reali verranno collegati solo dopo i test di "
        "compatibilità e di isolamento dei moduli."
    )


def vinted():
    platform_page("Vinted")


def ebay():
    platform_page("eBay")


def subito():
    platform_page("Subito")


st.markdown(
    """
    <style>
      .block-container {max-width: 1600px; padding-top: 1.25rem;}
      section[data-testid="stSidebar"] {background: #f8fafc;}
    </style>
    """,
    unsafe_allow_html=True,
)
st.sidebar.title("MT TECH · Venduti")
st.sidebar.caption("Anteprima tecnica — nessuna scrittura sui database")

selected = st.navigation(
    [
        st.Page(vinted, title="Vinted", icon="🟢", default=True),
        st.Page(ebay, title="eBay", icon="🔵"),
        st.Page(subito, title="Subito", icon="🟠"),
    ],
    position="sidebar",
)
selected.run()
