# MT TECH · Venduti — integrazione sperimentale

Stato: progetto tecnico, **non distribuire in produzione**.

## Obiettivo

Un'unica applicazione Streamlit che carica a richiesta Venduti Vinted, Venduti eBay o Venduti Subito; un solo processo web, mantenendo separati i tre database, i collector e le repository sorgenti.

## Sorgenti

- Vinted: `mttechstore26-blip/VENDUTI-VINTED`, `app.py`, servizio `venduti-vinted.service`, porta 8504, DB in `/opt/vinted-venduti/data/vinted_market.db`.
- eBay: `mttechstore26-blip/VENDUTI-EBAY`, `dashboard.py`, servizio `venduti-ebay.service`, porta 8505, DB configurato tramite `DB_PATH`.
- Subito: `mttechstore26-blip/VENDUTI-SUBITO`, `app.py` e `pages/*.py`, servizio `venduti-subito.service`, porta 8501, DB in `/opt/mt-tech-telegram/data/market.db`.

## Blocchi tecnici da risolvere prima di avviare il processo unico

1. **Import Python omonimi:** Vinted e Subito utilizzano entrambi moduli con nomi come `database`. Isolare le tre codebase in package con import espliciti (es. `venduti_vinted.database`) anziché variare `sys.path` durante le sessioni.
2. **Bootstrap Streamlit:** ogni dashboard ha un proprio `st.set_page_config`; riorganizzare i punti d'ingresso in funzioni renderizzabili per pagina, lasciando un unico punto di navigazione condiviso.
3. **Navigazione:** mappare le cinque pagine Subito, le viste eBay e i filtri Vinted; isolare le chiavi `st.session_state` per piattaforma, preservare query params ed export.
4. **Percorsi DB:** i riferimenti devono restare assoluti e configurabili sulla VPS. Niente copie di database o migrazioni nello stesso file.
5. **Scritture:** collaudare esplicitamente override famiglie Subito, watchlist e modifiche eBay. Non consentire test distruttivi sul DB produzione.
6. **Dipendenze:** verificare le versioni Streamlit e requirements delle tre .venv, scegliere un unico ambiente compatibile.
7. **Cache e polling:** mantenere paginazione e cache esistenti; sospendere refresh non pertinenti alla pagina selezionata.
8. **Segreti e autenticazione:** tenere .env fuori da GitHub, applicare autorizzazione comune e protezione Nginx.

## Strategia di migrazione

1. Refactor per sorgente su branch dedicati, senza alterare i collector.
2. Test unitari delle classificazioni e confronti di output sulle medesime istantanee SQLite.
3. Avvio della nuova app su porta di staging, con lettura dai DB esistenti; funzioni di scrittura disabilitate fino a test completati.
4. Prova manuale di tutte le categorie, filtri, titoli cliccabili, CSV, famiglie e correzioni; misurazione RAM, CPU e tempi di caricamento.
5. Abilitazione scritture, test funzionali e rollback documentato.
6. Switch Nginx alla nuova app. Solo dopo verifica prolungata fermare le **tre dashboard** Streamlit; NON fermare i collector.

## Criteri di accettazione

- Un unico processo Streamlit serve tutte le sezioni.
- Le tre sezioni riproducono le funzioni esistenti senza regressioni note.
- Database e collector restano indipendenti.
- Le singole repository possono ricevere aggiornamenti isolati, con processo di build e rilascio della webapp centrale.
- I dati di produzione non vengono alterati dalla migrazione.
- I servizi preesistenti continuano a servire il traffico finché non avviene il passaggio autorizzato e verificato.

## Baseline VPS 25 ottobre 2026

- RAM totale 11 GiB, disponibile 9.0 GiB.
- RSS: Vinted 337892 KiB, Subito 316084 KiB, eBay 279312 KiB.
- Servizi confermati: `venduti-vinted.service`, `venduti-ebay.service`, `venduti-subito.service`.

Nota: la somma RSS non misura il risparmio ottenibile perché include pagine condivise. Non esiste ancora un processo unificato testato.
