import json, os, re, sys, csv
base = sys.argv[1]
U = [r for r in json.load(open(f"{base}/universe.json")) if r["mcap"] >= 3000 and r["endType"] == "stock"]
K = {d["localDate"]: d["closePrice"] for d in json.load(open(f"{base}/kospi.json"))}
def num(s):
    if s is None: return None
    s = str(s).replace(",", "").replace("배", "").replace("원", "").replace("%", "").strip()
    try: return float(s)
    except: return None
def px_at(series, date):
    # last close on or before date
    best = None
    for d in series:
        if d["localDate"] <= date: best = d
        else: break
    return best["closePrice"] if best else None
rows = []
for r in U:
    c = r["code"]
    px = json.load(open(f"{base}/px/{c}.json"))
    px = [d for d in px if d.get("closePrice")]
    if len(px) < 60: continue
    last = px[-1]
    yr = [d for d in px if d["localDate"] >= "20251124"]
    hi = max(yr, key=lambda d: d["highPrice"] or d["closePrice"])
    hic = max(yr, key=lambda d: d["closePrice"])
    lo = min(yr, key=lambda d: d["closePrice"])
    p0622 = px_at(px, "20260622"); p1023 = px_at(px, "20261023"); p0823 = px_at(px, "20260821"); p1030 = px_at(px, "20261030")
    p0102 = px_at(px, "20260102") or px_at(px, "20251230"); p1231 = px_at(px, "20251230")
    integ = json.load(open(f"{base}/integ/{c}.json"))
    ti = {t["code"]: t["value"] for t in (integ.get("totalInfos") or [])}
    ann = json.load(open(f"{base}/annual/{c}.json"))
    fi = (ann or {}).get("financeInfo") or {}
    cols = [t["key"] for t in fi.get("trTitleList", [])]
    cons = [t["key"] for t in fi.get("trTitleList", []) if t.get("isConsensus") == "Y"]
    rowmap = {row["title"]: {k: num(v.get("value")) for k, v in row["columns"].items()} for row in fi.get("rowList", [])}
    def g(title, key):
        return rowmap.get(title, {}).get(key)
    k25 = "202512"; k26 = "202612"; k24 = "202412"
    op25, op26, op24 = g("영업이익", k25), g("영업이익", k26), g("영업이익", k24)
    ni26 = g("당기순이익", k26)
    roe26 = g("ROE", k26); roe25 = g("ROE", k25)
    debt = g("부채비율", k25)
    rows.append({
        "mkt": r["mkt"], "code": c, "name": r["name"], "mcap_tn": round(r["mcap"] / 1e4, 2),
        "close": last["closePrice"], "hi52": hic["closePrice"], "hi_date": hic["localDate"], "lo52": lo["closePrice"],
        "dd_hi": round(last["closePrice"] / hic["closePrice"] - 1, 3),
        "r_since_0622": round(last["closePrice"] / p0622 - 1, 3) if p0622 else None,
        "r_1m": round(last["closePrice"] / p1023 - 1, 3) if p1023 else None,
        "r_3m": round(last["closePrice"] / p0823 - 1, 3) if p0823 else None,
        "r_ytd": round(last["closePrice"] / p1231 - 1, 3) if p1231 else None,
        "pos52": round((last["closePrice"] - lo["closePrice"]) / (hic["closePrice"] - lo["closePrice"]), 2) if hic["closePrice"] != lo["closePrice"] else None,
        "per": num(ti.get("per")), "fper": num(ti.get("cnsPer")), "pbr": num(ti.get("pbr")), "dy": num(ti.get("dividendYieldRatio")),
        "feps": num(ti.get("cnsEps")), "eps": num(ti.get("eps")), "frn": num(ti.get("foreignRate")),
        "op24": op24, "op25": op25, "op26e": op26, "has_cons26": k26 in cons,
        "op_g26": round(op26 / op25 - 1, 2) if (op26 and op25 and op25 > 0) else None,
        "roe25": roe25, "roe26e": roe26, "debt25": debt,
    })
K0622 = 9114.55; Klast = 4708.54
json.dump(rows, open(f"{base}/screen.json", "w"), ensure_ascii=False)
with open(f"{base}/screen.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows))
