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
.platform-switch-heading {text-align:center;font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#64748b;margin:0 0 10px}
div[class*="st-key-platform_logo_"] button {
 width:100%;min-height:62px;border-radius:15px;background:#fff !important;
 border:1px solid #dbe2ec !important;box-shadow:0 3px 12px rgba(15,23,42,.045);
 transition:all .16s ease;position:relative;
}
div[class*="st-key-platform_logo_"] button:hover {
 border-color:#818cf8 !important;box-shadow:0 7px 22px rgba(79,70,229,.13);
}
div[class*="st-key-platform_logo_"] button[kind="primary"] {
 border:2px solid #6366f1 !important;background:#f4f3ff !important;
 box-shadow:0 5px 18px rgba(99,102,241,.13);
}
div[class*="st-key-platform_logo_"] button p {font-size:0 !important}
div[class*="st-key-platform_logo_"] button::after {
 position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 font-weight:900;letter-spacing:-1px;pointer-events:none;
}
div[class*="st-key-platform_logo_vinted"] button::after {
 content:"Vinted";color:#007782;font-size:27px;font-style:italic;letter-spacing:-1.5px;
}
div[class*="st-key-platform_logo_ebay"] button::after {
 content:"eBay";font-size:29px;letter-spacing:-2px;
 background:linear-gradient(90deg,#e53238 0% 30%,#0064d2 32% 55%,#f5af02 57% 75%,#86b817 78%);
 -webkit-background-clip:text;background-clip:text;color:transparent;
}
div[class*="st-key-platform_logo_subito"] button::after {
 content:"subito";color:#f9423a;font-size:29px;letter-spacing:-1.5px;
}
/* Shared visual language for all three platform sidebars */
section[data-testid="stSidebar"] {
 background:linear-gradient(180deg,#f8faff 0%,#f1f5fb 100%) !important;
 border-right:1px solid #e2e8f0;
}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {padding-top:1.25rem}
section[data-testid="stSidebar"] h1 {font-size:1.48rem !important;letter-spacing:-.045em;font-weight:850;color:#18243b}
section[data-testid="stSidebar"] h3 {font-size:.89rem !important;font-weight:800;color:#475569}
section[data-testid="stSidebar"] button,
section[data-testid="stSidebar"] [data-testid="stPageLink"] a,
section[data-testid="stSidebar"] [role="radiogroup"] label {
 border-radius:10px !important;transition:background .14s ease,border-color .14s ease;
}
section[data-testid="stSidebar"] button:hover,
section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
section[data-testid="stSidebar"] [role="radiogroup"] label:hover {background:#e9edff !important}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {
 background:#e8eaff !important;color:#3730a3 !important;font-weight:800;
}
section[data-testid="stSidebar"] hr {border-color:#e2e8f0}
/* Identical menu-item geometry across Subito links, Vinted buttons and eBay radio */
section[data-testid="stSidebar"] [data-testid="stPageLink"] a,
section[data-testid="stSidebar"] div[class*="st-key-vinted_side_"] button,
section[data-testid="stSidebar"] [role="radiogroup"] label {
 display:flex !important;align-items:center !important;justify-content:flex-start !important;
 width:100% !important;min-height:38px !important;padding:8px 12px !important;
 border:1px solid transparent !important;border-radius:11px !important;
 background:transparent !important;box-shadow:none !important;
 color:#334155 !important;font-size:.88rem !important;font-weight:650 !important;
 text-align:left !important;margin:2px 0 !important;
}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a p,
section[data-testid="stSidebar"] div[class*="st-key-vinted_side_"] button p,
section[data-testid="stSidebar"] [role="radiogroup"] label p {
 font-size:.88rem !important;font-weight:650 !important;text-align:left !important;
}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
section[data-testid="stSidebar"] div[class*="st-key-vinted_side_"] button:hover,
section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
 background:#e9edff !important;color:#3730a3 !important;
}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"],
section[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="true"],
section[data-testid="stSidebar"] div[class*="st-key-vinted_side_"] button[kind="primary"],
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
 background:#e6eaff !important;color:#3730a3 !important;
 border-color:#dce2ff !important;font-weight:800 !important;
}
section[data-testid="stSidebar"] div[class*="st-key-vinted_side_"] button[kind="primary"] p {
 color:#3730a3 !important;font-weight:800 !important;
}
section[data-testid="stSidebar"] [role="radiogroup"] label [data-testid="stMarkdownContainer"] {flex:1}
section[data-testid="stSidebar"] [role="radiogroup"] label [data-baseweb="radio"] {margin-right:7px}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {font-size:.78rem;color:#64748b;font-weight:750}

</style>
""" , unsafe_allow_html=True)

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
    st.markdown(f"**{platform.upper()}**")
    st.caption("Navigazione")
    if platform == "Subito":
        for destination in subito_pages:
            st.page_link(destination)
    elif platform == "Vinted":
        # The original Vinted app uses a radio with key main_section.
        # Set its state BEFORE running the original page.
        for label in ["📂 Categorie", "🧾 Annunci venduti", "❤️ Top Like"]:
            if st.button(label, use_container_width=True, key="vinted_side_" + label,
                         type="primary" if st.session_state.get("main_section", "📂 Categorie") == label else "secondary"):
                st.session_state["main_section"] = label
                st.rerun()
    else:
        st.caption("Seleziona la sezione e usa i filtri qui sotto.")

page.run()
