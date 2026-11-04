import json,urllib.request,time,datetime,collections,sys
S=sys.argv[1]
def q(b):
    for i in range(5):
        try:
            r=urllib.request.Request("https://api.hyperliquid.xyz/info",data=json.dumps(b).encode(),headers={"Content-Type":"application/json"}); return json.load(urllib.request.urlopen(r,timeout=30))
        except Exception: time.sleep(2*(i+1))
    return []
start=int(datetime.datetime(2025,10,1,tzinfo=datetime.UTC).timestamp()*1000); end=int(time.time()*1000)
coins=[u['name'] for u in json.load(open(f"{S}/main_meta.json"))[0]['universe']]
xyz=[u['name'] for u in json.load(open(f"{S}/meta_xyz.json"))[0]['universe']]
io=[u['name'] for u in json.load(open(f"{S}/meta_io.json"))[0]['universe']]
res={'main':collections.defaultdict(float),'hip3':collections.defaultdict(float)}
for grp,lst in (('main',coins),('hip3',xyz+io)):
    for c in lst:
        cs=q({"type":"candleSnapshot","req":{"coin":c,"interval":"1d","startTime":start,"endTime":end}}) or []
        for k in cs:
            m=datetime.datetime.fromtimestamp(k['t']/1000,datetime.UTC).strftime('%Y-%m')
            tp=(float(k['h'])+float(k['l'])+float(k['c']))/3
            res[grp][m]+=float(k['v'])*tp
        time.sleep(0.12)
json.dump(res,open(f"{S}/monthly_volume.json","w"),indent=1)
for m in sorted(res['main']):
    a=res['main'][m];b=res['hip3'].get(m,0)
    print(m, f"main ${a/1e9:7.1f}B  hip3 ${b/1e9:6.1f}B  share {b/(a+b):.0%}")
