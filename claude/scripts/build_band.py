import json, os, sys, re, statistics as st, datetime as dt, csv
base = sys.argv[1]
S = json.load(open(f"{base}/screen2.json"))
def parse_mult(s):
    m = re.search(r"([\d\.]+)", s or ""); return float(m.group(1)) if m else None
def series(b):
    # returns list of (yyyymm, price, implied_metric_per_share)
    name = b["name"]; m4 = parse_mult(name.get("VAL4")); m1 = parse_mult(name.get("VAL1"))
    out = []
    for p, v4, v1 in zip(b["price"], b["val4"], b["val1"]):
        d = dt.datetime.utcfromtimestamp(p["x"] / 1000).strftime("%Y%m")
        eps = None
        if v1.get("y") is not None and m1: eps = v1["y"] / m1
        elif v4.get("y") is not None and m4: eps = v4["y"] / m4
        out.append((d, p.get("y"), eps))
    return out
res = []
for r in S:
    c = r["code"]; p = f"{base}/band/{c}.json"
    rr = dict(r)
    try:
        b = json.load(open(p))
        per_s = series(b["bandChart1"]); pbr_s = series(b["bandChart2"])
    except Exception:
        res.append(rr); continue
    def hist(sr, lo="202301", hi="202512"):
        vals = [pr / e for d, pr, e in sr if lo <= d <= hi and pr and e and e > 0]
        return vals
    pe_h = hist(per_s); pb_h = hist(pbr_s)
    # current metric per share at 202611
    cur_eps = next((e for d, pr, e in per_s if d == "202611"), None)
    cur_bps = next((e for d, pr, e in pbr_s if d == "202611"), None)
    px = r["close"]
    rr["pe_band_now"] = round(px / cur_eps, 1) if cur_eps and cur_eps > 0 else None
    rr["pb_band_now"] = round(px / cur_bps, 2) if cur_bps and cur_bps > 0 else None
    rr["pe_med_23_25"] = round(st.median(pe_h), 1) if len(pe_h) >= 12 else None
    rr["pe_min_23_25"] = round(min(pe_h), 1) if len(pe_h) >= 12 else None
    rr["pb_med_23_25"] = round(st.median(pb_h), 2) if len(pb_h) >= 12 else None
    rr["pb_min_23_25"] = round(min(pb_h), 2) if len(pb_h) >= 12 else None
    rr["pe_vs_med"] = round(rr["pe_band_now"] / rr["pe_med_23_25"] - 1, 2) if rr["pe_band_now"] and rr["pe_med_23_25"] else None
    rr["pb_vs_med"] = round(rr["pb_band_now"] / rr["pb_med_23_25"] - 1, 2) if rr["pb_band_now"] and rr["pb_med_23_25"] else None
    rr["pe_mult_names"] = b["bandChart1"]["name"]
    res.append(rr)
json.dump(res, open(f"{base}/screen3.json", "w"), ensure_ascii=False)
with open(f"{base}/screen3.csv", "w", newline="") as f:
    keys = sorted({k for x in res for k in x.keys()})
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(res)
print(len(res), sum(1 for x in res if x.get("pe_vs_med") is not None))
