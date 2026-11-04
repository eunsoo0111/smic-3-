import json, sys, urllib.request, urllib.parse, time, os
DATA = sys.argv[1]
ds = {
 2022:'200c2cba-e58d-4a95-aa60-14b99736808d',
 2023:'d890d3a9-6b00-43fd-8b31-fcba4c8e2909',
 2024:'61729e5a-7aa8-448c-8903-ba3e0cd0ea3c',
 2025:'158a1baa-5506-400a-8ec3-97756f0b0536',
 2026:'2957a7f9-9a15-453e-9afd-3bbdcbac8fd3'}
ndc = json.load(open(os.path.join(DATA,'ndc_estradiol_td.json')))['results']
prods = {}
for r in ndc:
    pn = r['product_ndc']; lab, prod = pn.split('-')
    key = lab.zfill(5)+prod.zfill(4)
    prods[key] = (r['labeler_name'], r.get('brand_name'), r.get('generic_name'))
labelers = sorted({k[:5] for k in prods})
out = []
for yr, did in ds.items():
    params = [('limit','5000'),('offset','0'),
      ('conditions[0][property]','state'),('conditions[0][value]','XX'),('conditions[0][operator]','='),
      ('conditions[1][property]','labeler_code'),('conditions[1][operator]','in')]
    for i,l in enumerate(labelers):
        params.append((f'conditions[1][value][{i}]', l))
    url = f'https://data.medicaid.gov/api/1/datastore/query/{did}/0?' + urllib.parse.urlencode(params)
    offset=0; rows=[]
    while True:
        u = url.replace('offset=0', f'offset={offset}')
        with urllib.request.urlopen(u, timeout=300) as f:
            d = json.load(f)
        res = d['results']; rows += res
        if len(res) < 5000: break
        offset += 5000
    keep = [r for r in rows if (r['labeler_code']+r['product_code']) in prods]
    for r in keep:
        r['_labeler_name'], r['_brand'], r['_generic'] = prods[r['labeler_code']+r['product_code']]
    out += keep
    print(yr, 'rows', len(rows), 'kept', len(keep), file=sys.stderr)
json.dump(out, open(os.path.join(DATA,'sdud_estradiol_td.json'),'w'))
