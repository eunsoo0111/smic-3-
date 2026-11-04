import json, urllib.request, datetime, sys
def get(t,rng="5y"):
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range={rng}&interval=1d"
    d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=20))
    r=d["chart"]["result"][0]
    return {datetime.datetime.fromtimestamp(a,datetime.UTC).date():b for a,b in zip(r["timestamp"],r["indicators"]["quote"][0]["close"]) if b}
btc=get("BTC-USD")
ks=sorted(btc)
last=ks[-1]
y1=[(d,btc[d]) for d in ks if d>last-datetime.timedelta(days=365)]
hi=max(y1,key=lambda x:x[1]); lo=min(y1,key=lambda x:x[1])
print("BTC last",last,round(btc[last]),"1y hi",hi[0],round(hi[1]),"1y lo",lo[0],round(lo[1]))
allhi=max(btc.items(),key=lambda x:x[1]); print("ATH",allhi[0],round(allhi[1]))
# quarterly BTC prices
for q in ["2025-09-30","2025-12-31","2026-03-31","2026-06-30","2026-09-30"]:
    d=datetime.date.fromisoformat(q); c=[k for k in ks if k<=d][-1]; print(q,round(btc[c]))
for t in ["COIN","HOOD","MSTR","CME","BLSH","GLXY","MARA","XYZ","CBOE"]:
    s=get(t)
    common=[d for d in sorted(s) if d in btc]
    r=[(d,s[d]/btc[d]*1e4) for d in common]
    cur=r[-1][1]
    import statistics
    def pct(days):
        w=[x[1] for x in r if x[0]>r[-1][0]-datetime.timedelta(days=days)]
        return sum(1 for v in w if v<cur)/len(w)*100, min(w), max(w)
    p1,mn1,mx1=pct(365); p3,mn3,mx3=pct(365*3)
    print(f"{t:5} ratio(px/BTC*1e4) now {cur:.3f}  1y pctile {p1:.0f}%  3y pctile {p3:.0f}%  3y min {mn3:.3f} max {mx3:.3f}  first date {common[0]}")
