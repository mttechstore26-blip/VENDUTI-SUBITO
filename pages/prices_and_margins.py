"""Platform pricing comparison + editable acquisition-cost calculator."""
import streamlit as st
from integration.universal_data import search_sold, aggregate_by_platform

st.title("📊 Prezzi e margini")
st.caption("Confronto indicativo dei venduti: verifica sempre modello, condizioni e accessori prima di acquistare.")
term = st.text_input("Prodotto / modello da confrontare", placeholder="Es. KitchenAid KSM150")
days = st.selectbox("Periodo comparabile", [30,90,365,0], format_func=lambda n:"Tutto lo storico" if not n else f"Ultimi {n} giorni")
if len(term.strip()) >= 3:
    rows, status = search_sold(term, days, 1000)
    st.caption(" · ".join(f"{name}: {state}" for name,state in status.items()))
    table = aggregate_by_platform(rows)
    if table.empty:
        st.info("Dati insufficienti per questo prodotto.")
    else:
        st.dataframe(table, width="stretch", hide_index=True,
            column_config={"platform":"Piattaforma","venduti":"Annunci nel campione",
                           "mediana":st.column_config.NumberColumn("Mediana €",format="%.2f"),
                           "media":st.column_config.NumberColumn("Media €",format="%.2f"),
                           "minimo":st.column_config.NumberColumn("Min €",format="%.2f"),
                           "massimo":st.column_config.NumberColumn("Max €",format="%.2f")})
        st.bar_chart(table.set_index("platform")[["mediana"]])
        st.warning("Le quantità sono i risultati caricati dalla ricerca, non necessariamente tutti i venduti. "
                   "Il confronto usa corrispondenze testuali, non identifica automaticamente tutte le varianti.")
else:
    st.info("Inserisci un modello per vedere il confronto tra le tre piattaforme.")

st.divider()
st.subheader("💶 Calcolatore acquisto massimo e margine")
a, b, c = st.columns(3)
with a:
    resale = st.number_input("Prezzo di rivendita previsto (€)", min_value=0.0,value=200.0,step=10.0)
    shipping = st.number_input("Spedizione e imballaggio (€)",min_value=0.0,value=10.0,step=1.0)
with b:
    purchase = st.number_input("Costo acquisto (€)",min_value=0.0,value=120.0,step=10.0)
    fixed = st.number_input("Altri costi (€)",min_value=0.0,value=0.0,step=1.0)
with c:
    fees = st.number_input("Commissioni vendita (%)",min_value=0.0,max_value=100.0,value=0.0,step=0.5)
    desired = st.number_input("Utile netto desiderato (€)",min_value=0.0,value=40.0,step=5.0)
commission = resale * fees / 100
profit = resale - purchase - shipping - fixed - commission
max_buy = max(0.0,resale - shipping - fixed - commission - desired)
m1,m2,m3 = st.columns(3)
m1.metric("Utile stimato", f"€ {profit:.2f}")
m2.metric("Acquisto massimo",f"€ {max_buy:.2f}")
m3.metric("Margine sul venduto", f"{(profit / resale * 100 if resale else 0):.1f}%")
st.caption("Stime configurabili, prima di imposte personali e resi. Non includono costi o commissioni non inseriti.")
