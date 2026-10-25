# MT TECH · Venduti — Staging enhancements

This branch is **not production**. The three original collectors remain independent.

## Features
- Universal sold-title search from 3 databases (read-only)
- Platform median / average and configurable acquisition margin
- 120-second bounded query cache; maximum 1,200 rows per source
- Atomic SQLite backups using native SQLite backup API (no direct copying while WAL writes are underway)
- Optional Discord alerts for a configurable seven-day sales-volume threshold

## Deploy app
```bash
git -C /opt/mt-tech-venduti-staging pull --ff-only
/opt/mt-tech-venduti-dashboard/.venv/bin/python -m py_compile /opt/mt-tech-venduti-staging/integration/{universal_data,refresh_snapshots,discord_opportunities}.py /opt/mt-tech-venduti-staging/pages/{universal_search,prices_and_margins}.py /opt/mt-tech-venduti-staging/unified_app.py
```
Streamlit may need a staging-only restart to pick up newly created pages.

## Snapshot refresh (OPTIONAL; verify source paths before enabling)
```bash
test -f /opt/vinted-venduti/data/vinted_market.db
test -f /opt/venduti-ebay/venduti-ebay/data/ebay_sold.db
/opt/mt-tech-venduti-dashboard/.venv/bin/python /opt/mt-tech-venduti-staging/integration/refresh_snapshots.py
sudo cp /opt/mt-tech-venduti-staging/integration/systemd/mttech-staging-snapshots.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now mttech-staging-snapshots.timer
```
If the eBay source database is elsewhere, set `MTTECH_EBAY_SOURCE_DB` in the service's environment before enabling. Only install the timer after the manual dry run succeeds. The source databases are opened read-only.

## Discord notifications (DISABLED until configured)
Create root-owned `/etc/mttech-staging-alerts.env` (chmod 600):
```text
MTTECH_DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
MTTECH_ALERT_PRODUCTS=Bimby TM5,Dyson Airwrap
MTTECH_ALERT_MIN_SOLD_7D=20
```
Do not commit or paste the webhook into GitHub or chat. Then:
```bash
sudo cp /opt/mt-tech-venduti-staging/integration/systemd/mttech-staging-alerts.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now mttech-staging-alerts.timer
```
A notification is sent at most once per keyword/day/threshold after crossing the seven-day aggregate count. The alert reads only local databases; it does not call marketplaces. Configured timer is hourly.

## Notes
Comparisons are text-matched samples, not condition/model-normalized sales totals. Results and medians may be biased; always check configuration and accessories.
