"""MT TECH · Venduti: unified staging portal with platform-specific navigation."""
from urllib.parse import urlsplit
import streamlit as st

st.set_page_config(
    page_title="MT TECH · Venduti — Anteprima",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

def vinted():
    from integration.vinted_original_adapter import run_vinted_original
    run_vinted_original()

def ebay():
    from integration.ebay_adapter import run_ebay_preview
    run_ebay_preview()

vinted_page = st.Page(vinted, title="Vinted", icon="🟢", url_path="vinted")
ebay_page = st.Page(ebay, title="eBay", icon="🔵", url_path="ebay")
subito_pages = [
    st.Page("pages/categorie.py", title="Categorie", icon="🎯", url_path="subito-categorie", default=True),
    st.Page("pages/annunci.py", title="Annunci venduti", icon="📦", url_path="subito-annunci"),
    st.Page("pages/prezzi.py", title="Analisi prezzi", icon="💰", url_path="subito-prezzi"),
    st.Page("pages/trend.py", title="Trend", icon="📈", url_path="subito-trend"),
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊", url_path="subito-dashboard"),
]
page = st.navigation([vinted_page, ebay_page] + subito_pages, position="hidden")
path = urlsplit(st.context.url).path.rstrip("/")
if path.endswith("/vinted"):
    platform = "Vinted"
elif path.endswith("/ebay"):
    platform = "eBay"
else:
    platform = "Subito"

st.markdown("""
<style>
.platform-switch-heading {text-align:center; font-size:.78rem; font-weight:700; letter-spacing:.12em;
text-transform:uppercase; color:#64748b; margin:0 0 2px}
div[data-testid="stSegmentedControl"] {display:flex; justify-content:center}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="platform-switch-heading">Piattaforma</div>', unsafe_allow_html=True)
selected = st.segmented_control(
    "Seleziona piattaforma", ["Vinted", "eBay", "Subito"],
    default=platform, label_visibility="collapsed", key="platform_top_switch"
)
if selected and selected != platform:
    st.switch_page({"Vinted": vinted_page, "eBay": ebay_page, "Subito": subito_pages[0]}[selected])

with st.sidebar:
    st.title("MT TECH · Venduti")
    st.caption("Anteprima sperimentale")
    st.divider()
    st.subheader(f"{platform} · Menu")
    if platform == "Subito":
        for destination in subito_pages:
            st.page_link(destination)
    elif platform == "Vinted":
        # The original Vinted app uses a radio with key main_section.
        # Set its state BEFORE running the original page.
        for label in ["📂 Categorie", "🧾 Annunci venduti", "❤️ Top Like"]:
            if st.button(label, use_container_width=True, key="vinted_side_" + label):
                st.session_state["main_section"] = label
                st.rerun()
    else:
        st.caption("Filtri e sezioni eBay disponibili nella dashboard originale.")

page.run()
