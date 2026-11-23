import json, time, sys, os, requests, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
base = sys.argv[1]
U = [r for r in json.load(open(f"{base}/universe.json")) if r["mcap"] >= 3000 and r["endType"] == "stock"]
os.makedirs(f"{base}/band", exist_ok=True)
R = "https://navercomp.wisereport.co.kr"
local = threading.local()
def sess():
    if not hasattr(local, "s"):
        local.s = requests.Session(); local.s.headers.update({"User-Agent": "Mozilla/5.0"})
    return local.s
def work(r):
    c = r["code"]; p = f"{base}/band/{c}.json"
    if os.path.exists(p): return c, None
    for i in range(6):
        try:
            x = sess().get(f"{R}/common/BandChart3.aspx?cmp_cd={c}&gubun=0", timeout=25, headers={"Referer": f"{R}/v2/company/c1050001.aspx?cmp_cd={c}"})
            if x.status_code == 200 and x.text.strip():
                d = json.loads(x.text); json.dump(d, open(p, "w"), ensure_ascii=False); return c, None
        except Exception:
            pass
        time.sleep(1.5 * (i + 1))
    return c, "fail"
fails = []
with ThreadPoolExecutor(max_workers=6) as ex:
    for i, f in enumerate(as_completed([ex.submit(work, r) for r in U])):
        c, e = f.result()
        if e: fails.append(c)
print("done", len(U), "fails", len(fails), fails[:20])
