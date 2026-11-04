import json, sys, urllib.request, urllib.parse, os
DATA=sys.argv[1]
ds={2024:'99315a95-37ac-4eee-946a-3c523b4c481e',2025:'f38d0706-1239-442c-a3cc-40ef1b686ac0',2026:'fbb83258-11c7-47f5-8b18-5f8e79f7e704'}
# first inspect schema
u=f"https://data.medicaid.gov/api/1/datastore/query/{ds[2026]}/0?limit=1"
print(json.dumps(json.load(urllib.request.urlopen(u,timeout=120))['results'][0],indent=1))
out=[]
for yr,did in ds.items():
    params=[('limit','5000'),('offset','0'),('conditions[0][property]','ndc_description'),('conditions[0][value]','%ESTRADIOL%'),('conditions[0][operator]','LIKE')]
    off=0
    while True:
        params[1]=('offset',str(off))
        u=f"https://data.medicaid.gov/api/1/datastore/query/{did}/0?"+urllib.parse.urlencode(params)
        d=json.load(urllib.request.urlopen(u,timeout=300))
        out+=d['results']
        if len(d['results'])<5000: break
        off+=5000
    print(yr,len(out),file=sys.stderr)
json.dump(out,open(os.path.join(DATA,'nadac_estradiol.json'),'w'))
