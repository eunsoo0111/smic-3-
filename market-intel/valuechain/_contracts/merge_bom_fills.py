#!/usr/bin/env python3
"""V1 채움 병합기(bom 노드판) — vc-input-filler 산출(work/fill_<F#>.json · work/sources_<F#>.jsonl)을 bom.json 노드에 들인다.

키트 동봉 merge_fills.py 는 공정 묶음 라이브러리(--lib)만 다룬다. 묶음 없이 bom 노드를 직접 채우는 체인(예: space)은 이 도구를 쓴다.

사용:
  python3 market-intel/valuechain/_contracts/merge_bom_fills.py market-intel/valuechain/space            # 병합
  python3 market-intel/valuechain/_contracts/merge_bom_fills.py --validate <fill.json> <sources.jsonl>   # 서브가 제출 전에 자기 산출을 잰다
규칙:
  - fill 파일 꼴: {"filler": "F1", "nodes": [완성 input 노드 행, …]}
  - 같은 id = 서브 행으로 교체(kind·parent 는 bom 것을 지킨다). 새 id 는 부모가 bom 에 실재하는 stage/input 일 때만 추가.
  - 「없음 — 이유」 행(구조상 안 쓰는 입력)은 서브가 덮어쓰지 못한다.
  - sources 는 id 로 합친다. 같은 id 에 다른 내용이면 거부(S000 은 정본 유지).
  - 병합 뒤 검사는 check_bom.py 가 한다(이 도구는 판정하지 않는다).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def node_errors(row: dict, src_ids: set) -> list:
    """꼴 검사(스키마 node 정의) + 출처 id 실재."""
    out = []
    try:
        import jsonschema  # type: ignore
        sch = json.loads((HERE / "bom.schema.json").read_text(encoding="utf-8"))
        sub = {"$schema": sch["$schema"], "$ref": "#/$defs/node", "$defs": sch["$defs"]}
        for e in jsonschema.Draft202012Validator(sub).iter_errors(row):
            out.append(f"{row.get('id')}: {'/'.join(str(p) for p in e.path)}: {e.message[:140]}")
    except ImportError:
        out.append("jsonschema 부재 — 꼴 검사 못 함")

    def srcs(x):
        if isinstance(x, dict):
            if isinstance(x.get("source"), str):
                yield x["source"]
            for v in x.values():
                yield from srcs(v)
        elif isinstance(x, list):
            for v in x:
                yield from srcs(v)
    for s in sorted(set(srcs(row))):
        if s not in src_ids:
            out.append(f"{row.get('id')}: source {s} 가 sources 파일에 없다")
    if row.get("kind") == "input":
        for k in ("qty_per_unit", "price", "cost_share_pct", "makers", "input_type"):
            if k not in row:
                out.append(f"{row.get('id')}: `{k}` 키 없음")
    return out


def read_jsonl(p: Path) -> dict:
    out = {}
    for line in p.read_text(encoding="utf-8").splitlines() if p.exists() else []:
        if line.strip():
            r = json.loads(line)
            out[r["id"]] = r
    return out


def validate(fill_p: Path, src_p: Path) -> int:
    doc = json.loads(fill_p.read_text(encoding="utf-8"))
    src = read_jsonl(src_p)
    bad = []
    for sid, r in src.items():
        for k in ("id", "kind", "ref", "title", "grade"):
            if not r.get(k):
                bad.append(f"sources {sid}: `{k}` 빈칸")
    ids = set(src) | {"S000"}
    for row in doc.get("nodes") or []:
        bad += node_errors(row, ids)
    print(f"{fill_p.name}: 노드 {len(doc.get('nodes') or [])} · 출처 {len(src)} · 오류 {len(bad)}")
    for b in bad[:60]:
        print("  " + b)
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "--validate":
        return validate(Path(argv[1]), Path(argv[2]))
    d = Path(argv[0])
    bom_p, work = d / "bom.json", d / "work"
    bom = json.loads(bom_p.read_text(encoding="utf-8"))
    by = {n["id"]: n for n in bom["nodes"]}
    src = read_jsonl(d / "sources.jsonl")
    rejected, n_rep, n_add, n_src = [], 0, 0, 0
    for f in sorted(work.glob("fill_*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        for row in doc.get("nodes") or []:
            rid = row.get("id", "")
            if rid in by:
                cur = by[rid]
                if cur.get("kind") != "input":
                    rejected.append(f"{f.name}: {rid} 는 input 이 아니다({cur.get('kind')})")
                    continue
                if isinstance(cur.get("makers"), str) and cur["makers"].startswith("없음 — "):
                    rejected.append(f"{f.name}: {rid} 는 「없음」 행 — 덮어쓰지 않는다")
                    continue
                by[rid].update({**row, "kind": "input", "parent": cur["parent"]})
                n_rep += 1
            else:
                par = row.get("parent")
                if par not in by or by[par].get("kind") not in ("stage", "input"):
                    rejected.append(f"{f.name}: 새 노드 {rid} 의 parent {par!r} 가 bom 에 없다")
                    continue
                row = {**row, "kind": "input"}
                idx = max(i for i, n in enumerate(bom["nodes"]) if n["id"] == par or n.get("parent") == par)
                bom["nodes"].insert(idx + 1, row)
                by[rid] = row
                n_add += 1
    for f in sorted(work.glob("sources_*.jsonl")):
        for sid, r in read_jsonl(f).items():
            if sid in src and src[sid] != r:
                if sid == "S000":
                    continue
                rejected.append(f"{f.name}: source {sid} 충돌(다른 내용)")
                continue
            n_src += sid not in src
            src[sid] = r
    bom_p.write_text(json.dumps(bom, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (d / "sources.jsonl").write_text("".join(json.dumps(src[k], ensure_ascii=False) + "\n" for k in sorted(src)), encoding="utf-8")
    print(f"교체 {n_rep} · 추가 {n_add} · 새 출처 {n_src} · 거부 {len(rejected)}")
    for r in rejected:
        print("  거부 " + r)
    return 1 if rejected else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
