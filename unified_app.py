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
.platform-logo-nav {display:flex; justify-content:center; align-items:center; gap:12px; margin:0 auto 16px}
.platform-logo-nav a {display:flex; align-items:center; justify-content:center; width:138px;
height:54px; padding:10px 18px; border-radius:14px; border:1px solid #dbe2ec;
background:#fff; text-decoration:none; transition:box-shadow .15s,border-color .15s}
.platform-logo-nav a:hover {border-color:#94a3b8; box-shadow:0 5px 18px rgba(15,23,42,.12)}
.platform-logo-nav a.active {border:2px solid #2563eb; background:#f1f6ff;
box-shadow:0 4px 14px rgba(37,99,235,.10)}
.platform-logo-nav img {display:block; max-width:104px; width:auto; height:27px; object-fit:contain}
.platform-logo-nav .subito-wordmark {font-weight:900; font-size:25px; letter-spacing:-1.2px; color:#ff4c22}
@media(max-width:600px) {
.platform-logo-nav {gap:6px}
.platform-logo-nav a {width:100px; height:48px; padding:7px}
.platform-logo-nav img {max-width:80px; height:23px}
.platform-logo-nav .subito-wordmark {font-size:20px}
}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="platform-switch-heading">Seleziona piattaforma</div>', unsafe_allow_html=True)
st.markdown(
    '<nav class="platform-logo-nav" aria-label="Piattaforme">'
    + '<a target="_parent" href="/vinted" title="Vinted" aria-label="Apri Vinted" class="' + ('active' if platform == 'Vinted' else '') + '">'
      '<img src="https://cdn.simpleicons.org/vinted/007782" alt="Vinted"></a>'
    + '<a target="_parent" href="/ebay" title="eBay" aria-label="Apri eBay" class="' + ('active' if platform == 'eBay' else '') + '">'
      '<img src="https://cdn.simpleicons.org/ebay" alt="eBay"></a>'
    + '<a target="_parent" href="/subito-categorie" title="Subito" aria-label="Apri Subito" class="' + ('active' if platform == 'Subito' else '') + '">'
      '<span class="subito-wordmark">subito</span></a>'
    + '</nav>',
    unsafe_allow_html=True,
)

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
