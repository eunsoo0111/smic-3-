"""TARS(XDEMVY) 메디케어 Part D 자체 분석 — CMS 공개 API에서 직접 받아 집계한다.
실행: python3 -I tars_cms.py <출력폴더>
- 개별 처방의(이름·NPI)는 저장하지 않고 집계값만 CSV로 남긴다.
- 원천: data.cms.gov (Part D Spending by Drug 연간·분기, Prescribers by Geography and Drug,
  Prescribers by Provider and Drug, Medicare Monthly Enrollment). 데이터셋 ID는 2026-11-13 카탈로그 기준.
"""
import csv, json, sys, os, statistics as st, urllib.parse, urllib.request
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.makedirs(OUT, exist_ok=True)
B = 'https://data.cms.gov/data-api/v1/dataset/'
IDS = dict(spend_annual='7e0b4365-fd63-4a29-8f5e-e0ac9f66a81b',   # Part D Spending by Drug (DY2024)
           spend_q='4ff7c618-4e40-483a-b390-c8a58c94fa15',        # Quarterly Part D Spending (thru 2026Q1)
           geo24='c8ea3f8e-3a09-4fea-86f2-8902fb4b0920',          # Prescribers by Geography & Drug DY2024
           geo23='3463648b-1971-478d-84ca-80cadc758153',          # DY2023
           prov24='9552739e-3d05-4c1b-8eff-ecabf391e2e5',         # Prescribers by Provider & Drug DY2024
           enr='d7fabe1e-d19b-4333-9eff-e80e0643f2fd')            # Medicare Monthly Enrollment
def get(i, **f):
    rows, off = [], 0
    while True:
        q = {**{f'filter[{k}]': v for k, v in f.items()}, 'size': 5000, 'offset': off}
        with urllib.request.urlopen(B + IDS[i] + '/data?' + urllib.parse.urlencode(q), timeout=120) as r:
            page = json.load(r)
        rows += page; off += 5000
        if len(page) < 5000: return rows
def w(name, header, rows):
    with open(os.path.join(OUT, name), 'w', newline='') as fh:
        cw = csv.writer(fh); cw.writerow(header); cw.writerows(rows)

# 1) 연도·분기별 메디케어 청구(=병 수에 근사: 10mL 1병 = 1청구)
a = [r for r in get('spend_annual', Brnd_Name='Xdemvy') if r['Mftr_Name'] == 'Overall'][0]
q = [r for r in get('spend_q', Brnd_Name='Xdemvy') if r['Mftr_Name'] == 'Overall']
series = [(y, a[f'Tot_Clms_{y}'], a[f'Tot_Benes_{y}'], a[f'Tot_Spndng_{y}'], a[f'Avg_Spnd_Per_Clm_{y}']) for y in ('2023', '2024')]
series += [(r['Year'], r['Tot_Clms'], r['Tot_Benes'], r['Tot_Spndng'], r['Avg_Spnd_Per_Clm']) for r in q]
w('medicare_xdemvy_series.csv', ['period', 'claims', 'beneficiaries', 'gross_spend_usd', 'gross_spend_per_claim_usd'], series)

# 2) 주별 침투율(2024): 메디케어 Part D 가입자 10만 명당 청구
enr = get('enr', YEAR='2024', MONTH='Year', BENE_GEO_LVL='State')
pd = {r['BENE_STATE_DESC']: int(r['PRSCRPTN_DRUG_TOT_BENES']) for r in enr if r['PRSCRPTN_DRUG_TOT_BENES'].isdigit()}
geo = get('geo24', Brnd_Name='Xdemvy')
nat = [r for r in geo if r['Prscrbr_Geo_Lvl'] == 'National'][0]
states = []
for r in geo:
    if r['Prscrbr_Geo_Lvl'] == 'State' and pd.get(r['Prscrbr_Geo_Desc'], 0) >= 100000:
        c = float(r['Tot_Clms']); e = pd[r['Prscrbr_Geo_Desc']]
        states.append((r['Prscrbr_Geo_Desc'], int(c), int(r['Tot_Prscrbrs']), e, round(c / e * 1e5, 1)))
states.sort(key=lambda x: -x[4])
w('medicare_xdemvy_state_2024.csv', ['state', 'claims', 'prescribers', 'partd_enrollees', 'claims_per_100k'], states)

# 3) 처방의 구조(2024): 연 11건 이상 처방의만 공개됨(CMS 소규모 셀 비공개 규칙)
prov = get('prov24', Brnd_Name='Xdemvy')
by = {}
for r in prov:
    t = r['Prscrbr_Type']; by.setdefault(t, [0, 0.0]); by[t][0] += 1; by[t][1] += float(r['Tot_Clms'])
tc = sum(v[1] for v in by.values())
w('medicare_xdemvy_prescriber_type_2024.csv', ['prescriber_type', 'n_prescribers_ge11', 'claims', 'share_of_ge11_claims'],
  [(k, v[0], int(v[1]), round(v[1] / tc, 3)) for k, v in sorted(by.items(), key=lambda x: -x[1][1])])
cl = sorted((float(r['Tot_Clms']) for r in prov), reverse=True)
g23 = [r for r in get('geo23', Brnd_Name='Xdemvy') if r['Prscrbr_Geo_Lvl'] == 'National'][0]
top = states[:len(states) // 5]; topavg = sum(s[1] for s in top) / sum(s[3] for s in top) * 1e5
allc = sum(s[1] for s in states); alle = sum(s[3] for s in states)
summary = {
    'prescribers_2023': int(g23['Tot_Prscrbrs']), 'prescribers_2024': int(nat['Tot_Prscrbrs']),
    'claims_2024_national': int(float(nat['Tot_Clms'])), 'ge65_claims_2024': int(float(nat['GE65_Tot_Clms'])),
    'n_prescribers_ge11_2024': len(prov), 'claims_ge11_share_of_national': round(tc / float(nat['Tot_Clms']), 3),
    'median_claims_ge11_prescriber': st.median(cl), 'top10pct_of_ge11_share': round(sum(cl[:len(cl) // 10]) / tc, 3),
    'state_median_per_100k': st.median(s[4] for s in states), 'national_per_100k': round(allc / alle * 1e5, 1),
    'top_quintile_per_100k': round(topavg, 1), 'uplift_if_all_states_top_quintile': round(topavg * alle / 1e5 / allc, 2)}
json.dump(summary, open(os.path.join(OUT, 'medicare_xdemvy_summary_2024.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps(summary, indent=1)); print(series)
