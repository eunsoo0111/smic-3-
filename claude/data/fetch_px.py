import json, urllib.request, sys, os, datetime, ssl
S=sys.argv[1]
T="BTC-USD ^IXIC SOXX COIN MSTR HOOD CME ICE CBOE GLXY BLSH GEMI CRCL XYZ PYPL IBKR SCHW MARA RIOT CLSK CIFR IREN WULF HUT CORZ BITF BTDR HIVE CAN APLD CANG BTM EXOD XXI NAKA ASST BSTR CNCK BTGO KRAK FIGR SOFI BLK GME 3350.T 8473.T 8698.T 0863.HK 3887.HK ADE.DE CSHR DEFT BMNR SBET".split()
out=[]
for t in T:
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=2y&interval=1d"
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        d=json.load(urllib.request.urlopen(req,timeout=20))
        r=d["chart"]["result"][0]; m=r["meta"]
        ts=r["timestamp"]; c=r["indicators"]["quote"][0]["close"]
        pts=[(datetime.datetime.utcfromtimestamp(a).date(),b) for a,b in zip(ts,c) if b is not None]
        last_d,last=pts[-1]
        def ago(days):
            tgt=last_d-datetime.timedelta(days=days)
            cand=[p for p in pts if p[0]<=tgt]
            return cand[-1][1] if cand else None
        y1=[p[1] for p in pts if p[0]>last_d-datetime.timedelta(days=365)]
        ytd=[p for p in pts if p[0]<datetime.date(last_d.year,1,1)]
        ytd0=ytd[-1][1] if ytd else None
        q3s=[p for p in pts if p[0]<=datetime.date(2026,6,30)]; q3e=[p for p in pts if p[0]<=datetime.date(2026,9,30)]
        oct_s=q3e[-1][1] if q3e else None
        f=lambda a:(last/a-1)*100 if a else None
        out.append(dict(t=t,cur=m.get("currency"),date=str(last_d),px=last,hi=max(y1),lo=min(y1),
          pos=(last-min(y1))/(max(y1)-min(y1))*100 if max(y1)>min(y1) else None,
          r1m=f(ago(30)),r3m=f(ago(91)),r1y=f(ago(365)),ytd=f(ytd0),q3=((q3e[-1][1]/q3s[-1][1]-1)*100 if q3s and q3e else None),
          since_sep30=f(oct_s), name=m.get("longName") or m.get("shortName")))
    except Exception as e:
        out.append(dict(t=t,err=str(e)[:80]))
json.dump(out,open(f"{S}/px.json","w"),indent=1)
fmt=lambda v:"" if v is None else f"{v:,.1f}"
print(f"{'tkr':9}{'date':11}{'px':>10}{'52wPos%':>8}{'1M%':>7}{'3M%':>7}{'YTD%':>7}{'1Y%':>7}{'Q3%':>7}{'Oct1→%':>7}  name")
for o in out:
    if 'err' in o: print(o['t'],'ERR',o['err']); continue
    print(f"{o['t']:9}{o['date']:11}{o['px']:>10,.2f}{fmt(o['pos']):>8}{fmt(o['r1m']):>7}{fmt(o['r3m']):>7}{fmt(o['ytd']):>7}{fmt(o['r1y']):>7}{fmt(o['q3']):>7}{fmt(o['since_sep30']):>7}  {o['name']}")
