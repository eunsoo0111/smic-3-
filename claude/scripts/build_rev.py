import json, os, sys, csv
base = sys.argv[1]
S = json.load(open(f"{base}/screen.json"))
def load(c, yy):
    p = f"{base}/cons/{c}_{yy}.json"
    if not os.path.exists(p): return None
    d = json.load(open(p))
    if not d or not isinstance(d, dict) or "chart1" not in d: return None
    try:
        c1 = json.loads(d["chart1"]); c2 = json.loads(d["chart2"])
    except Exception: return None
    cats = [x.replace("/", "") for x in c1.get("categories", [])]
    return {"cats": cats, "eps": c1.get("avg", []), "op": c2.get("avg", [])}
def at(h, key, date):
    # value at last month-end <= date
    if not h: return None
    best = None
    for c, v in zip(h["cats"], h[key]):
        if c <= date and v is not None: best = v
    return best
def nb(tbl):
    return None
out = []
for r in S:
    c = r["code"]
    h27 = load(c, "202712"); h26 = load(c, "202612")
    e27_now = at(h27, "eps", "20261130"); e27_jun = at(h27, "eps", "20260630"); e27_hi = at(h27, "eps", r["hi_date"]) or (h27["eps"][0] if h27 and h27["eps"] else None)
    e27_sep = at(h27, "eps", "20260930"); e27_aug = at(h27, "eps", "20260831")
    o27_now = at(h27, "op", "20261130"); o27_jun = at(h27, "op", "20260630"); o27_hi = at(h27, "op", r["hi_date"])
    e26_now = at(h26, "eps", "20261130"); e26_jun = at(h26, "eps", "20260630")
    def pct(a, b):
        return round(a / b - 1, 3) if (a is not None and b not in (None, 0) and b > 0) else None
    rr = dict(r)
    rr.update({
        "eps27": e27_now, "per27": round(r["close"] / e27_now, 1) if e27_now and e27_now > 0 else None,
        "d_eps27_jun": pct(e27_now, e27_jun), "d_eps27_hi": pct(e27_now, e27_hi), "d_eps27_1m": pct(e27_now, at(h27, "eps", "20261030")),
        "d_eps27_3m": pct(e27_now, e27_aug),
        "d_op27_jun": pct(o27_now, o27_jun), "d_op27_hi": pct(o27_now, o27_hi),
        "d_eps26_jun": pct(e26_now, e26_jun),
        "op27": o27_now, "eps27_g": pct(e27_now, e26_now),
        "per27_at_hi": round(r["hi52"] / e27_hi, 1) if e27_hi and e27_hi > 0 else None,
    })
    # de-rating share: how much of price fall is multiple compression
    if rr["per27"] and rr["per27_at_hi"]:
        rr["per_compress"] = round(rr["per27"] / rr["per27_at_hi"] - 1, 3)
    else:
        rr["per_compress"] = None
    out.append(rr)
json.dump(out, open(f"{base}/screen2.json", "w"), ensure_ascii=False)
with open(f"{base}/screen2.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print(len(out), sum(1 for x in out if x["eps27"]))
