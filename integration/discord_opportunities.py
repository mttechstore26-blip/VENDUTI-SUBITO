#!/usr/bin/env python3
"""Optional Discord alerts from local snapshots only. No Vinted/eBay/Subito API calls."""
import json
import os
import sqlite3
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA=Path("/opt/mt-tech-venduti-staging/data")
STATE=DATA/"universal_alert_state.json"
SOURCES={
 "Vinted":(DATA/"vinted_market_preview.db","listings","price","sold_at","status='sold'"),
 "eBay":(DATA/"ebay_sold_preview.db","sales","sold_price","ended_at","1=1"),
 "Subito":(Path("/opt/mt-tech-telegram/data/market.db"),"listings","price","detected_sold_at","detected_sold_at IS NOT NULL"),
}
def query_count(path,table,price,date,filter_sql,term,cutoff):
    if not path.is_file():
        return 0
    with sqlite3.connect(f"file:{path}?mode=ro",uri=True,timeout=5) as db:
        db.execute("PRAGMA query_only=ON")
        return int(db.execute(
          f"SELECT COUNT(*) FROM {table} WHERE {filter_sql} AND LOWER(title) LIKE ? "
          f"AND julianday({date}) >= julianday(?) AND {price} > 0",
          (f"%{term.lower()}%",cutoff)).fetchone()[0])

def main():
    hook=os.getenv("MTTECH_DISCORD_WEBHOOK","").strip()
    terms=[x.strip() for x in os.getenv("MTTECH_ALERT_PRODUCTS","").split(",") if len(x.strip())>=3][:20]
    threshold=max(1,int(os.getenv("MTTECH_ALERT_MIN_SOLD_7D","20")))
    if not hook or not hook.startswith("https://discord.com/api/webhooks/") or not terms:
        print("Discord non configurato: nessuna notifica inviata.")
        return
    now=datetime.now(timezone.utc)
    cutoff=(now-timedelta(days=7)).isoformat()
    try: state=json.loads(STATE.read_text())
    except (OSError, ValueError): state={}
    notifications=[]
    for term in terms:
        totals={}
        for platform,(path,table,price,date,filter_sql) in SOURCES.items():
            try: totals[platform]=query_count(path,table,price,date,filter_sql,term,cutoff)
            except sqlite3.Error: totals[platform]=0
        count=sum(totals.values())
        signature=f"{now.strftime('%Y-%m-%d')}:{term.lower()}:{threshold}"
        if count>=threshold and signature not in state:
            notifications.append((signature,f"📊 **{term}**: {count} venduti negli ultimi 7 giorni "
                         + " | ".join(f"{p} {n}" for p,n in totals.items())))
    for signature,message in notifications:
        request=urllib.request.Request(hook,data=json.dumps({"content":message}).encode(),
                      headers={"Content-Type":"application/json"},method="POST")
        try:
            with urllib.request.urlopen(request,timeout=10) as response:
                if response.status not in (200,204): raise RuntimeError("Invio Discord non riuscito")
        except Exception as exc:
            print(f"Invio Discord fallito: {type(exc).__name__}")
            continue
        state[signature]=now.isoformat()
    # Keep the state bounded
    state=dict(list(state.items())[-500:])
    DATA.mkdir(parents=True,exist_ok=True)
    tmp=STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state))
    tmp.replace(STATE)
    print(f"Avvisi Discord inviati: {len(notifications)} tentativi")

if __name__=="__main__":
    main()
