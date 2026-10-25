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
.platform-switch-heading {text-align:center; font-size:.73rem; font-weight:750;
letter-spacing:.12em; text-transform:uppercase; color:#64748b; margin:0 0 8px}
div[class*="st-key-platform_logo_"] button {
    width:100%; min-height:58px; border-radius:14px;
    background-color:#fff; border:1px solid #dbe2ec;
    font-weight:850; font-size:20px;
}
div[class*="st-key-platform_logo_"] button:hover {
    border-color:#2563eb; box-shadow:0 5px 18px rgba(15,23,42,.12);
}
div[class*="st-key-platform_logo_"] button p {font-size:20px; font-weight:850}
div[class*="st-key-platform_logo_vinted"] button {
    color:#007782;
    background-image:url("https://cdn.simpleicons.org/vinted/007782");
    background-repeat:no-repeat; background-position:center; background-size:auto 26px;
}
div[class*="st-key-platform_logo_ebay"] button {
    background-image:url("https://cdn.simpleicons.org/ebay");
    background-repeat:no-repeat; background-position:center; background-size:auto 29px;
}
div[class*="st-key-platform_logo_vinted"] button p,
div[class*="st-key-platform_logo_ebay"] button p {opacity:0}
div[class*="st-key-platform_logo_subito"] button {color:#ff4c22}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="platform-switch-heading">Seleziona piattaforma</div>', unsafe_allow_html=True)
left, middle, right = st.columns([1.5, 3, 1.5])
with middle:
    a, b, c = st.columns(3, gap="small")
    with a:
        if st.button("Vinted", key="platform_logo_vinted", use_container_width=True,
                     type="primary" if platform == "Vinted" else "secondary"):
            st.switch_page(vinted_page)
    with b:
        if st.button("eBay", key="platform_logo_ebay", use_container_width=True,
                     type="primary" if platform == "eBay" else "secondary"):
            st.switch_page(ebay_page)
    with c:
        if st.button("subito", key="platform_logo_subito", use_container_width=True,
                     type="primary" if platform == "Subito" else "secondary"):
            st.switch_page(subito_pages[0])

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
