import json, sys, os
from collections import defaultdict
DATA=sys.argv[1]
rows=json.load(open(os.path.join(DATA,'sdud_estradiol_td.json')))
def grp(name):
    n=name.lower()
    if 'amneal' in n: return 'Amneal'
    if 'mylan' in n: return 'Viatris(Mylan)'
    if 'zydus' in n: return 'Zydus'
    if 'sandoz' in n: return 'Sandoz'
    if 'noven' in n: return 'Noven'
    if 'bayer' in n: return 'Bayer'
    return 'Other:'+name
# exclude contraceptive patches (norelgestromin/levonorgestrel+EE) -> keep HRT estradiol only
def is_hrt(r):
    g=(r['_generic'] or '').lower()
    return not ('norelgestromin' in g or 'ethinyl' in g or 'ethinly' in g)
agg=defaultdict(lambda: defaultdict(float)); rx=defaultdict(lambda: defaultdict(float)); amt=defaultdict(lambda: defaultdict(float))
seen=set()
for r in rows:
    if not is_hrt(r): continue
    # use only one utilization type total? SDUD has FFSU and MCOU; sum both
    if r['suppression_used']=='true': continue
    q=f"{r['year']}Q{r['quarter']}"
    g=grp(r['_labeler_name'])
    agg[q][g]+=float(r['units_reimbursed'] or 0)
    rx[q][g]+=float(r['number_of_prescriptions'] or 0)
    amt[q][g]+=float(r['total_amount_reimbursed'] or 0)
qs=sorted(agg)
groups=sorted({g for q in agg for g in agg[q]})
print('Quarter,'+','.join(groups)+',TOTAL_units,TOTAL_rx,TOTAL_$,$/unit')
for q in qs:
    tot=sum(agg[q].values()); trx=sum(rx[q].values()); tam=sum(amt[q].values())
    print(q+','+','.join(f"{agg[q].get(g,0)/1e3:.0f}" for g in groups)+f",{tot/1e3:.0f}k,{trx/1e3:.1f}k,{tam/1e6:.2f}M,{tam/tot if tot else 0:.2f}")
print()
print('Share of units by quarter (%)')
for q in qs:
    tot=sum(agg[q].values())
    print(q+','+','.join(f"{100*agg[q].get(g,0)/tot:.1f}" for g in groups))
print()
print('$/unit by group')
for q in qs:
    print(q+','+','.join(f"{(amt[q].get(g,0)/agg[q][g]) if agg[q].get(g) else 0:.2f}" for g in groups))
