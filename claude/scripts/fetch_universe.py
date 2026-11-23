import json, time, sys, os, requests
from concurrent.futures import ThreadPoolExecutor
OUT = sys.argv[1]
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})
def get(url, tries=5):
    for i in range(tries):
        try:
            r = S.get(url, timeout=20)
            if r.status_code == 200 and r.text.strip():
                return r.json()
        except Exception as e:
            pass
        time.sleep(1.5 * (i + 1))
    return None
rows = []
for mkt in ["KOSPI", "KOSDAQ"]:
    page = 1
    while True:
        d = get(f"https://m.stock.naver.com/api/stocks/marketValue/{mkt}?page={page}&pageSize=100")
        if not d or not d.get("stocks"):
            break
        for s in d["stocks"]:
            rows.append({"mkt": mkt, "code": s["itemCode"], "name": s["stockName"], "endType": s.get("stockEndType"),
                         "close": int(s["closePriceRaw"]), "mcap": int(s["marketValueRaw"]) / 1e8,
                         "chg": float(s["fluctuationsRatio"])})
        last_mcap = int(d["stocks"][-1]["marketValueRaw"]) / 1e8
        print(mkt, page, len(d["stocks"]), round(last_mcap), file=sys.stderr)
        if last_mcap < 1500:
            break
        page += 1
        time.sleep(0.3)
json.dump(rows, open(OUT, "w"), ensure_ascii=False)
print(len(rows))
