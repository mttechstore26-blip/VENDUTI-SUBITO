"""Cross-platform sold search. No writes to collectors or source DBs."""
import streamlit as st
from integration.universal_data import search_sold

st.title("🔎 Ricerca universale")
st.caption("Cerca annunci venduti su Vinted, eBay e Subito. I risultati provengono dai database di anteprima.")
term = st.text_input("Prodotto o modello", placeholder="Es. Bimby TM5, PS5 Slim, Dyson Airwrap", key="universal_term")
col1, col2 = st.columns(2)
with col1:
    days = st.selectbox("Periodo", [0, 7, 30, 90, 365], format_func=lambda v: "Tutto lo storico" if v == 0 else f"Ultimi {v} giorni")
with col2:
    limit = st.select_slider("Massimo annunci per piattaforma", options=[100, 250, 500, 1000], value=250)
if len(term.strip()) < 3:
    st.info("Digita almeno tre caratteri. Nessuna ricerca viene eseguita finché il campo è vuoto.")
else:
    data, states = search_sold(term, days, limit)
    st.caption(" · ".join(f"{k}: {v}" for k,v in states.items()))
    st.metric("Annunci trovati", f"{len(data):,}".replace(",", "."))
    if data.empty:
        st.warning("Nessun annuncio venduto corrisponde ai criteri.")
    else:
        src = st.multiselect("Piattaforme", ["Vinted", "eBay", "Subito"],
                             default=["Vinted", "eBay", "Subito"], key="universal_sources")
        view = data[data["platform"].isin(src)].copy()
        view["url"] = view["url"].fillna("").astype(str)
        view.loc[view["url"].str.startswith("/items/"), "url"] = (
            "https://www.vinted.it" + view.loc[view["url"].str.startswith("/items/"), "url"])
        st.dataframe(
            view[["platform", "title", "price", "sold_date", "category", "url"]],
            hide_index=True, width="stretch",
            column_config={"platform":"Piattaforma", "title":"Annuncio",
                           "price":st.column_config.NumberColumn("Prezzo (€)",format="%.2f"),
                           "sold_date":st.column_config.DatetimeColumn("Venduto il"),
                           "category":"Categoria",
                           "url":st.column_config.LinkColumn("Annuncio online",display_text="Apri")}
        )
        st.download_button("⬇️ Esporta CSV", view.to_csv(index=False).encode("utf-8-sig"),
                           file_name="mttech_ricerca_universale.csv", mime="text/csv")
