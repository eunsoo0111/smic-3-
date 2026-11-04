import json,urllib.request,time,datetime,sys,collections
S=sys.argv[1]; A="0x43e9abea1910387c4292bca4b94de81462f8a251"
def q(body):
    for i in range(5):
        try:
            r=urllib.request.Request("https://api.hyperliquid.xyz/info",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
            return json.load(urllib.request.urlopen(r,timeout=30))
        except Exception as e:
            time.sleep(2*(i+1))
    return None
dests=json.load(open(f"{S}/team_dests.json"))
out={}
for i,(a,recv) in enumerate(dests):
    spot=q({"type":"spotClearinghouseState","user":a}) or {}
    hype_spot=sum(float(b['total']) for b in spot.get('balances',[]) if b['coin']=='HYPE')
    ds=q({"type":"delegatorSummary","user":a}) or {}
    led=q({"type":"userNonFundingLedgerUpdates","user":a,"startTime":1730000000000}) or []
    fills=q({"type":"userFillsByTime","user":a,"startTime":1730000000000}) or []
    # HYPE spot market is @107 on Hyperliquid (HYPE/USDC); also count perps 'HYPE' separately
    sold=sum(float(f['sz']) for f in fills if f['coin']=='@107' and f['side']=='A')
    bought=sum(float(f['sz']) for f in fills if f['coin']=='@107' and f['side']=='B')
    perp_short=sum(float(f['sz']) for f in fills if f['coin']=='HYPE' and f['side']=='A')
    t_out=collections.Counter(); t_in_other=0.0; evm=0.0
    for e in led:
        d=e['delta']
        if d.get('token')!='HYPE': continue
        if d['type'] in ('spotTransfer','send'):
            if d['user'].lower()==a.lower():
                dest=d['destination'].lower()
                if dest.startswith('0x2222222222222222222222222222222222222222'): evm+=float(d['amount'])
                else: t_out[dest]+=float(d['amount'])
            elif d['user'].lower()!=A: t_in_other+=float(d['amount'])
    out[a]=dict(recv=recv,spot=hype_spot,staked=float(ds.get('delegated',0) or 0),pending=float(ds.get('totalPendingWithdrawal',0) or 0),
                sold=sold,bought=bought,perp_short=perp_short,t_out=dict(t_out),evm=evm,in_other=t_in_other)
    if i%20==0: print(i,a,out[a] if len(str(out[a]))<300 else '...',flush=True)
    time.sleep(0.4)
json.dump(out,open(f"{S}/trace.json","w"),indent=1)
print("done",len(out))
