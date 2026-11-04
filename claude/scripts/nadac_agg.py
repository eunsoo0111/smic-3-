import json, sys, os
from collections import defaultdict
DATA=sys.argv[1]
rows=json.load(open(os.path.join(DATA,'nadac_estradiol.json')))
ndc=json.load(open(os.path.join(DATA,'ndc_estradiol_td.json')))['results']
prods={}
for r in ndc:
    lab,prod=r['product_ndc'].split('-'); prods[lab.zfill(5)+prod.zfill(4)]=r['labeler_name']
descs=defaultdict(set)
pts=defaultdict(dict)
for r in rows:
    d=r['ndc_description']
    if not any(k in d for k in ['PATCH','DOTTI','LYLLANA','MINIVELLE','VIVELLE','CLIMARA','MENOSTAR','TDS','TRANSDERM']): continue
    if 'NORELGEST' in d or 'XULANE' in d or 'ZAFEMY' in d or 'TWIRLA' in d or 'CLIMARA PRO' in d or 'COMBIPATCH' in d: continue
    key=r['ndc'][:9]
    lab=prods.get(key,'?'+r['ndc'][:5])
    descs[lab].add(d)
    m=r['as_of_date'][:7]
    pts[(lab,d)][m]=float(r['nadac_per_unit'])
for lab in descs: print(lab, sorted(descs[lab])[:8])
# monthly median per labeler for 0.05 mg strength (most common)
months=sorted({m for v in pts.values() for m in v})
import statistics
print()
print('month,'+','.join(sorted({k[0] for k in pts})))
labs=sorted({k[0] for k in pts})
for m in months:
    line=[m]
    for lab in labs:
        vals=[v[m] for (l,d),v in pts.items() if l==lab and m in v and ('0.05' in d or '.05MG' in d or '0.05MG' in d)]
        line.append(f"{statistics.median(vals):.2f}" if vals else '')
    print(','.join(line))
