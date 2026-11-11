#!/usr/bin/env python3
"""V2 새 박스 제안기 — bom.json·process_lib.json 의 「없음 — 새 박스 후보: <id>」 문면을 모아 core/valuechain/_inbox 제안 행(valuechain/chain-proposal@1)으로 내고, 문면에 `_inbox/<파일>#<proposal_id>` 참조를 붙인다(check_bom B8 이 실재를 잰다).

사용: python3 market-intel/valuechain/_contracts/propose_boxes.py market-intel/valuechain/hbm --inbox core/valuechain/_inbox/20261020_hbm_valuechain_box_proposals.jsonl --prefix VC-HBM-P
  - 본 yaml(core/valuechain/*.yaml)은 건드리지 않는다. 제안 파일은 덧붙이기만 하고 같은 후보 id 는 한 행으로 접는다.
  - 후보 id 가 이미 G-S3 박스 집합에 있으면 제안하지 않고 문면을 그 box_ref 로 바꾼다(이미 있는 박스를 새로 제안하는 실수 방지).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_bom as cb  # noqa: E402

CAND = re.compile(r"^없음 — 새 박스 후보:\s*([a-z0-9_.]+)")
CHAIN_OF = {"semi.front": "semi_krx_subchains", "semi.back": "semi_krx_subchains", "semi.fab": "semi_krx_subchains",
            "semi.equip": "memory", "semi.pkg": "memory", "semi.material": "memory", "semi.design": "memory"}


def chain_for(cid: str) -> str:
    for k, v in CHAIN_OF.items():
        if cid.startswith(k):
            return v
    return "semi_krx_subchains"


def main(argv: list[str]) -> int:
    from datetime import datetime, timedelta, timezone
    today = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")   # 제안 행의 날짜 = 실행 시각(KST)
    d = Path(argv[0]).resolve()
    inbox = Path(argv[argv.index("--inbox") + 1]).resolve()
    prefix = argv[argv.index("--prefix") + 1]
    boxes = cb.box_ids()[0]
    bom_p = d / "bom.json"
    bom = json.loads(bom_p.read_text(encoding="utf-8"))
    lib_p = cb.REPO / bom["process_lib_ref"] if bom.get("process_lib_ref") else None
    lib = json.loads(lib_p.read_text(encoding="utf-8")) if lib_p else {"bundles": []}
    existing, rows = {}, []
    if inbox.exists():
        for line in inbox.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                rows.append(r)
                vid = (r.get("value") or {}).get("id")
                if vid:
                    existing[vid] = r
    nxt = 1 + max([int(re.sub(r"\D", "", r["proposal_id"].replace(prefix, "")) or 0) for r in rows if str(r.get("proposal_id", "")).startswith(prefix)] or [0])
    cands: dict = {}

    def visit(holder, key, where, maker=None):
        x = holder.get(key)
        if not isinstance(x, str):
            return
        m = CAND.match(x)
        if not m or "_inbox/" in x:
            return
        cid = m.group(1).rstrip(".")
        cands.setdefault(cid, {"where": [], "makers": []})
        cands[cid]["where"].append(where)
        if maker:
            t = maker.get("ticker") or "비상장·" + str((maker.get("unlisted") or {}).get("parent", "?"))
            nm = f"{maker['name']}({t})"
            if nm not in cands[cid]["makers"]:
                cands[cid]["makers"].append(nm)
        cands[cid].setdefault("holders", []).append((holder, key))

    inputs = [n for n in bom["nodes"]] + [i for b in lib.get("bundles") or [] for i in b.get("inputs") or []]
    for n in inputs:
        visit(n, "box_ref", n["id"])
        for m in n.get("makers") if isinstance(n.get("makers"), list) else []:
            visit(m, "box_ref", n["id"], m)
    made = 0
    for cid, c in sorted(cands.items()):
        ref = None
        for stem in ("memory", "semi_krx_subchains", "foundry_logic", "pcb_substrate"):
            if f"{stem}#{cid}" in boxes:
                ref = f"{stem}#{cid}"
                break
        if ref:
            for h, k in c["holders"]:
                h[k] = ref
            continue
        if cid in existing:
            pid = existing[cid]["proposal_id"]
        else:
            pid = f"{prefix}{nxt:02d}"
            nxt += 1
            made += 1
            r = {"schema": "valuechain/chain-proposal@1", "proposal_id": pid, "ts_kst": today, "status": "proposed",
                 "posted_by": f"본체(valuechain-study {bom['chain']} V2 — vc-input-filler 후보 집계)",
                 "study_ref": f"{bom_p.relative_to(cb.REPO)}", "chain_file": f"core/valuechain/{chain_for(cid)}.yaml",
                 "box_id": None, "box_id_null_reason": f"새 박스 — G-S3 박스 집합에 없음(check_bom 실측 {today})",
                 "field": "boxes", "op": "add",
                 "value": {"id": cid, "label": f"(제안) {cid}", "leaves_pending": c["makers"][:12],
                           "evidence_inputs": sorted(set(c["where"]))[:12]},
                 "grade": "③", "source": f"{d.relative_to(cb.REPO)}/sources.jsonl + _process_lib/sources.jsonl(메이커별 source id)", "asof": today}
            rows.append(r)
            existing[cid] = r
        for h, k in c["holders"]:
            h[k] = f"없음 — 새 박스 후보: {cid} (_inbox/{inbox.name}#{pid})"
    inbox.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    bom_p.write_text(json.dumps(bom, ensure_ascii=False, indent=1), encoding="utf-8")
    if lib_p:
        lib_p.write_text(json.dumps(lib, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"후보 {len(cands)} · 새 제안 {made} · 제안 파일 행 {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
