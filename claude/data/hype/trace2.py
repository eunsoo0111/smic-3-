import json,urllib.request,time,sys,collections
S=sys.argv[1]
def q(body):
    for i in range(5):
        try:
            r=urllib.request.Request("https://api.hyperliquid.xyz/info",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
            return json.load(urllib.request.urlopen(r,timeout=30))
        except Exception: time.sleep(2*(i+1))
    return None
tr=json.load(open(f"{S}/trace.json"))
for i,(a,o) in enumerate(tr.items()):
    led=q({"type":"userNonFundingLedgerUpdates","user":a,"startTime":1730000000000}) or []
    o['usdc_withdraw']=sum(float(e['delta'].get('usdc',0)) for e in led if e['delta']['type']=='withdraw')
    tw=q({"type":"userTwapSliceFills","user":a}) or []
    o['twap_sold']=sum(float(x['fill']['sz']) for x in tw if x['fill']['coin'] in ('@107','@207','@232','@255') and x['fill']['side']=='A')
    o['twap_capped']=len(tw)>=2000
    hold=o['spot']+o['staked']+o['pending']; tout=sum(o['t_out'].values())
    o['residual']=o['recv']+o['in_other']-hold-tout-o['evm']
    time.sleep(0.3)
json.dump(tr,open(f"{S}/trace2.json","w"),indent=1)
print("done")
