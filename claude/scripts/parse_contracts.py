import json, re, sys
p = sys.argv[1]; d = json.load(open(p))
rows = []
for c in d["contracts"]:
    t = c.get("text") or ""
    def g(pat):
        m = re.search(pat, t); return m.group(1).strip() if m else None
    amt = g(r"계약금액\(원\) \| ([\d,]+)")
    rev = g(r"최근매출액\(원\) \| ([\d,]+)")
    cp = g(r"3\. 계약상대 \| ([^|]+)")
    cp_en = g(r"3\. 계약상대 \| [^|]+ \| \(([^)]+)\)")
    reg = g(r"4\. 판매ㆍ공급지역 \| ([^|]+)")
    st = g(r"시작일 \| ([\d-]+)"); en = g(r"종료일 \| ([\d-]+)")
    fx = g(r"\(([\d,\.]+)원/USD\)")
    nm = g(r"체결계약명 \| ([^|]+)")
    rows.append({"date": c["date"], "corr": "정정" in c["title"], "rcpNo": c["rcpNo"], "name": nm, "amt_bn": round(int(amt.replace(",", "")) / 1e8, 1) if amt else None,
                 "cp": cp, "cp_en": cp_en, "region": reg, "start": st, "end": en, "fx": fx})
json.dump(rows, open(p.replace(".json", "_parsed.json"), "w"), ensure_ascii=False)
for r in rows: print(r["date"], "C" if r["corr"] else " ", r["amt_bn"], "|", r["cp"], "|", r["region"], "|", r["end"], "|", r["fx"], "|", r["name"])
