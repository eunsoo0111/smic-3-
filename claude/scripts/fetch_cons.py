import json, time, sys, os, requests, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
base = sys.argv[1]
U = [r for r in json.load(open(f"{base}/universe.json")) if r["mcap"] >= 3000 and r["endType"] == "stock"]
os.makedirs(f"{base}/cons", exist_ok=True)
R = "https://navercomp.wisereport.co.kr"
local = threading.local()
def sess():
    if not hasattr(local, "s"):
        local.s = requests.Session(); local.s.headers.update({"User-Agent": "Mozilla/5.0"})
    return local.s
def get(url, ref, tries=6):
    for i in range(tries):
        try:
            r = sess().get(url, timeout=25, headers={"Referer": ref})
            if r.status_code == 200 and r.text.strip():
                return r.json()
            if r.status_code == 429:
                time.sleep(5 * (i + 1)); continue
        except Exception:
            pass
        time.sleep(1.5 * (i + 1))
    return "FAIL"
def work(r):
    c = r["code"]; out = {}
    ref = f"{R}/v2/company/c1050001.aspx?cmp_cd={c}"
    for yy in ["202612", "202712"]:
        p = f"{base}/cons/{c}_{yy}.json"
        if os.path.exists(p): continue
        d = get(f"{R}/company/ajax/cF5002.aspx?cmp_cd={c}&dt=20261120&yymm={yy}&frq=Y&acc_cd=121500&fingubun=MAIN&chartType=svg", ref)
        if d == "FAIL": out[yy] = "fail"; continue
        json.dump(d, open(p, "w"), ensure_ascii=False)
    p = f"{base}/cons/{c}_tbl2027.json"
    if not os.path.exists(p):
        d = get(f"{R}/company/ajax/c1050001_data.aspx?flag=4&cmp_cd={c}&finGubun=MAIN&frq=0&sDT=20261120&yymm=202712&acc_cd=121500&chartType=svg", ref)
        if d != "FAIL": json.dump(d, open(p, "w"), ensure_ascii=False)
        else: out["tbl"] = "fail"
    return c, out
fails = {}
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(work, r) for r in U]
    for i, f in enumerate(as_completed(futs)):
        c, o = f.result()
        if o: fails[c] = o
        if i % 100 == 0: print(i, len(fails), file=sys.stderr, flush=True)
print("done", len(U), "fails", len(fails), json.dumps(fails)[:500])
