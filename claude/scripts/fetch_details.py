import json, time, sys, os, requests, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
base = sys.argv[1]
U = json.load(open(f"{base}/universe.json"))
U = [r for r in U if r["mcap"] >= 3000 and r["endType"] == "stock"]
os.makedirs(f"{base}/px", exist_ok=True); os.makedirs(f"{base}/integ", exist_ok=True); os.makedirs(f"{base}/annual", exist_ok=True)
local = threading.local()
def sess():
    if not hasattr(local, "s"):
        local.s = requests.Session(); local.s.headers.update({"User-Agent": "Mozilla/5.0"})
    return local.s
def get(url, tries=6):
    for i in range(tries):
        try:
            r = sess().get(url, timeout=25)
            if r.status_code == 200 and r.text.strip():
                return r.json()
            if r.status_code == 429:
                time.sleep(5 * (i + 1)); continue
        except Exception:
            pass
        time.sleep(1.5 * (i + 1))
    return None
def work(r):
    c = r["code"]; out = {}
    p = f"{base}/px/{c}.json"
    if not os.path.exists(p):
        d = get(f"https://api.stock.naver.com/chart/domestic/item/{c}/day?startDateTime=202501010000&endDateTime=202611232359")
        if d is not None: json.dump(d, open(p, "w"))
        else: out["px"] = "fail"
    p = f"{base}/integ/{c}.json"
    if not os.path.exists(p):
        d = get(f"https://m.stock.naver.com/api/stock/{c}/integration")
        if d is not None: json.dump(d, open(p, "w"), ensure_ascii=False)
        else: out["integ"] = "fail"
    p = f"{base}/annual/{c}.json"
    if not os.path.exists(p):
        d = get(f"https://m.stock.naver.com/api/stock/{c}/finance/annual")
        if d is not None: json.dump(d, open(p, "w"), ensure_ascii=False)
        else: out["annual"] = "fail"
    return c, out
fails = {}
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(work, r) for r in U]
    for i, f in enumerate(as_completed(futs)):
        c, o = f.result()
        if o: fails[c] = o
        if i % 50 == 0: print(i, len(fails), file=sys.stderr, flush=True)
print("done", len(U), "fails", len(fails), json.dumps(fails)[:500])
