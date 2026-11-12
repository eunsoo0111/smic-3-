#!/usr/bin/env python3
"""V1 채움 병합기 — vc-input-filler 서브 산출(work/fill_<F#>.json · work/sources_<F#>.jsonl)을 묶음 라이브러리(또는 bom)에 들인다.

사용:
  python3 market-intel/valuechain/_contracts/merge_fills.py --lib market-intel/valuechain/_process_lib/process_lib.json --work market-intel/valuechain/_process_lib/work
규칙:
  - 묶음 입력은 id 로 맞춘다: 같은 id = 서브 행으로 교체, 새 id(「<묶음>.」 접두) = 추가, 서브가 안 건드린 골격 행은 그대로 둔다.
  - 접두가 묶음 id 와 다른 행·없는 묶음은 들이지 않고 거부 목록으로 찍는다(조용히 버리지 않는다).
  - sources 는 id 로 합친다. 같은 id 에 다른 내용이면 거부(서브 간 id 범위 충돌 — 재배정 필요).
  - 병합 뒤 check_bom 으로 검사하는 것은 호출자 몫(이 도구는 판정하지 않는다).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if "--lib" not in argv or "--work" not in argv:
        print(__doc__)
        return 2
    lib_p = Path(argv[argv.index("--lib") + 1])
    work = Path(argv[argv.index("--work") + 1])
    lib = json.loads(lib_p.read_text(encoding="utf-8"))
    bundles = {b["id"]: b for b in lib["bundles"]}
    src_p = lib_p.parent / "sources.jsonl"
    src = {}
    for line in src_p.read_text(encoding="utf-8").splitlines() if src_p.exists() else []:
        if line.strip():
            r = json.loads(line)
            src[r["id"]] = r
    rejected, n_rep, n_add, n_src = [], 0, 0, 0
    for f in sorted(work.glob("fill_*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        for bid, body in (doc.get("bundles") or {}).items():
            if bid not in bundles:
                rejected.append(f"{f.name}: 묶음 {bid} 없음")
                continue
            cur = {i["id"]: i for i in bundles[bid]["inputs"]}
            order = [i["id"] for i in bundles[bid]["inputs"]]
            for row in body.get("inputs") or []:
                rid = row.get("id", "")
                if not rid.startswith(bid + "."):
                    rejected.append(f"{f.name}: {rid} 접두 ≠ {bid}.")
                    continue
                row = {**row, "kind": "input", "parent": bid}
                if rid in cur:
                    n_rep += 1
                else:
                    n_add += 1
                    order.append(rid)
                cur[rid] = row
            bundles[bid]["inputs"] = [cur[i] for i in order]
    for f in sorted(work.glob("sources_*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r["id"] in src and src[r["id"]] != r:
                if r["id"] == "S000":
                    continue  # 공용 모델 지식 행 — 정본 유지
                rejected.append(f"{f.name}: source {r['id']} 충돌(다른 내용)")
                continue
            n_src += r["id"] not in src
            src[r["id"]] = r
    lib_p.write_text(json.dumps(lib, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    src_p.write_text("".join(json.dumps(src[k], ensure_ascii=False) + "\n" for k in sorted(src)), encoding="utf-8")
    print(f"교체 {n_rep} · 추가 {n_add} · 새 출처 {n_src} · 거부 {len(rejected)}")
    for r in rejected:
        print("  거부 " + r)
    return 1 if rejected else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
