#!/usr/bin/env python3
"""bom.json → 노드별 한눈 요약(문서 쓸 때 보는 용도). 사용: dump_compact.py [id 접두]"""
import json, re, sys
from pathlib import Path
d = json.loads((Path(__file__).resolve().parent.parent / "bom.json").read_text())
pre = sys.argv[1] if len(sys.argv) > 1 else ""
def val(x):
    if isinstance(x, dict):
        return f"{x['v']}{x['unit']}[{x['grade']}{x['source']}] {x.get('basis','')[:70]}"
    return str(x)[:40]
for n in d["nodes"]:
    if n["kind"] != "input" or not n["id"].startswith(pre) or not isinstance(n.get("makers"), list):
        continue
    print(f"\n## {n['id']} — {n['name']}\n  qty: {val(n['qty_per_unit'])}\n  price: {val(n['price'])}\n  share: {val(n['cost_share_pct'])}")
    g = {"KR": [], "해외상장": [], "비상장": []}
    for m in n["makers"]:
        t = m.get("ticker")
        sh = m.get("share_pct"); s = f" {sh['v']}%" if isinstance(sh, dict) else ""
        tag = f"{m['name']}({t or '비상장·' + str((m.get('unlisted') or {}).get('parent_ticker') or (m.get('unlisted') or {}).get('parent',''))[:18]}{s},{m.get('role','')[:4]},{m['grade']})"
        g["KR" if t and re.fullmatch(r"\d{6}", t) else "해외상장" if t else "비상장"].append(tag)
    for k, v in g.items():
        print(f"  {k}: " + "; ".join(v))
