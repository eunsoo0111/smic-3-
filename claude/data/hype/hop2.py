import json,urllib.request,time,sys,collections
S=sys.argv[1]
def q(body):
    for i in range(5):
        try:
            r=urllib.request.Request("https://api.hyperliquid.xyz/info",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
            return json.load(urllib.request.urlopen(r,timeout=30))
        except Exception: time.sleep(2*(i+1))
tr=json.load(open(f"{S}/trace2.json"))
agg=collections.Counter()
for o in tr.values():
    for d,v in o['t_out'].items(): agg[d]+=v
res={}
for d,v in agg.items():
    sp=q({"type":"spotClearinghouseState","user":d}) or {}
    spot=sum(float(b['total']) for b in sp.get('balances',[]) if b['coin']=='HYPE')
    ds=q({"type":"delegatorSummary","user":d}) or {}
    staked=float(ds.get('delegated',0) or 0)+float(ds.get('totalPendingWithdrawal',0) or 0)
    led=q({"type":"userNonFundingLedgerUpdates","user":d,"startTime":1730000000000}) or []
    inn=0;evm=0;out=0
    for e in led:
        x=e['delta']
        if x.get('token')!='HYPE' or x['type'] not in('spotTransfer','send'): continue
        if x['user'].lower()==d.lower():
            if x['destination'].startswith('0x2222222222'): evm+=float(x['amount'])
            else: out+=float(x['amount'])
        else: inn+=float(x['amount'])
    tot=max(inn,1e-9)
    held=min(spot+staked,inn)
    resid=max(inn-held-evm-out,0)
    share=v/tot
    res[d]=dict(from_us=v,inn=inn,held=held*share,evm=evm*share,out=out*share,sold=resid*share)
    time.sleep(0.3)
json.dump(res,open(f"{S}/hop2.json","w"),indent=1)
T=collections.Counter()
for r in res.values():
    for k in('held','evm','out','sold'): T[k]+=r[k]
print("hop2 allocation of",f"{sum(agg.values()):,.0f}",{k:f"{v:,.0f}" for k,v in T.items()})
