#!/usr/bin/env python3
"""bom.json → BOM.md(사람이 읽는 트리·표) + GAPS.md 착수 큐 블록 갱신. 판정하지 않는다 — 검사는 check_bom.py.

사용: python3 market-intel/valuechain/_contracts/render_bom.py market-intel/valuechain/hbm
  - BOM.md 는 통째로 다시 쓴다(손으로 고치지 않는다 — 고칠 것은 bom.json·process_lib.json 에).
  - GAPS.md 는 <!-- queue:start --> … <!-- queue:end --> 사이만 바꾼다(나머지 문면은 본체가 쓴다).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_bom as cb  # noqa: E402


def cell(x) -> str:
    if x is None:
        return "—"
    if isinstance(x, str):
        return x.replace("|", "/")
    v = x.get("v")
    v = f"{v[0]}~{v[1]}" if isinstance(v, list) and len(v) == 2 else v
    return f"{v} {x.get('unit', '')} ({x.get('grade', '')}{x.get('source', '')})".replace("|", "/")


def makers_cell(mk) -> str:
    if not isinstance(mk, list):
        return cell(mk)
    out = []
    for m in mk:
        t = m.get("ticker") or ("비상장·" + str((m.get("unlisted") or {}).get("parent", "?"))[:24])
        sh = m.get("share_pct")
        s = f" {sh['v']}%" if isinstance(sh, dict) else ""
        out.append(f"{m['name']}({t}{s})")
    return ", ".join(out).replace("|", "/")


def render(d: Path) -> int:
    bad, warn, doc, _ = cb.check_dir(d, cb.box_ids()[0])
    if not doc:
        print("\n".join(bad))
        return 1
    st = cb.stats(doc)
    nodes = doc["nodes"]
    kids: dict = {}
    for n in nodes:
        kids.setdefault(n.get("parent"), []).append(n)
    lib = doc.get("_lib") or {}
    bmap = {b["id"]: b for b in (lib.get("bundles") or []) + (doc.get("process_lib") or [])}
    L = [f"# {doc['product']} — 물리적 제품 구조(BOM)", "",
         f"- 기준 단위: {doc['unit_basis']} · 기준일 {doc['asof']} · 상태 {doc['status']} · 승인 {(doc.get('approved_by') or {}).get('who', '없음')}",
         f"- 생성: `render_bom.py`(손으로 고치지 않는다 — 정본 `bom.json`·`{doc.get('process_lib_ref', '')}`) · 검사 `check_bom.py` 실패 {len(bad)}·관측 {len(warn)}",
         f"- 통계: 단계 {st['stages']} · 참조 묶음 {st['bundles_referenced']} · 입력 {st['inputs']}(bom 고유 {st['inputs_bom']} + 묶음) {st['input_types']} · 메이커 고유 {st['makers_unique']}(행 {st['maker_rows']}) {st['listing']}",
         f"- 채움: 수량 {st['qty_filled']} · 가격 {st['price_filled']} · 원가 비중 {st['cost_share_filled']} · 점유율 {st['share_filled']} · 박스 연결(고유 메이커) {st['box_link_unique']}", "",
         "## 1. 트리", "```"]

    def walk(pid, depth):
        for n in kids.get(pid, []):
            tag = n["kind"] if n["kind"] != "input" else n.get("input_type", "input")
            extra = ""
            if n.get("lib_ref"):
                extra += "  ⟶ " + ", ".join(n["lib_ref"])
            if n.get("flow_ref"):
                extra += f"  ⟶ flow {n['flow_ref']}"
            L.append(f"{'  ' * depth}- [{tag}] {n['id']} {n['name']}{extra}")
            walk(n["id"], depth + 1)
    walk(None, 0)
    L += ["```", "", "## 2. 제품 고유 입력(bom 노드)", "", "| id | 종류 | 스펙 | 수량/스택 | 가격 | 원가 비중 | 메이커 | box_ref |", "|---|---|---|---|---|---|---|---|"]
    for n in nodes:
        if n["kind"] == "input" or n["kind"] == "product":
            L.append(f"| {n['id']} | {n.get('input_type', n['kind'])} | {n['spec'][:60]} | {cell(n.get('qty_per_unit'))} | {cell(n.get('price'))} | {cell(n.get('cost_share_pct'))} | {makers_cell(n.get('makers'))} | {cell(n.get('box_ref'))} |")
    L += ["", "## 3. 공정 묶음(참조된 것만) — 장비·소재·메이커의 유일한 정의", ""]
    for b in cb.referenced_bundles(doc):
        users = [n["id"] for n in nodes if b["id"] in (n.get("lib_ref") or [])]
        L += [f"### {b['id']} — {b['name']} ({b['stage_kind']}{' · HBM 경로' if b.get('hbm_path') else ''})",
              f"105단계 중 쓰는 단계: {b.get('steps') or '없음(105단계 밖 — 3D 적층 전용)'} · bom 참조 노드: {', '.join(users) or 'flow_ref 경유'}", "",
              "| 입력 | 종류 | 스펙 | 가격 | 메이커 | box_ref |", "|---|---|---|---|---|---|"]
        for i in b.get("inputs") or []:
            L.append(f"| {i['name']} | {i.get('input_type')} | {i['spec'][:50]} | {cell(i.get('price'))} | {makers_cell(i.get('makers'))} | {cell(i.get('box_ref'))} |")
        L.append("")
    if lib.get("flows"):
        L += ["## 4. 사용자 105단계 흐름 ↔ 묶음 (logic_cmos_105 — 베이스 다이 flow_ref)", "", "| # | 구간 | 8대 태그(원문) | 단계 | 묶음 |", "|---|---|---|---|---|"]
        for s in lib["flows"].get("logic_cmos_105", []):
            L.append(f"| {s['step']} | {s.get('section', '')} | {s['process_tag']} | {s['title']} | {', '.join(s['lib_ref'])} |")
    (d / "BOM.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    g = d / "GAPS.md"
    if g.exists():
        t = g.read_text(encoding="utf-8")
        a, b = t.find("<!-- queue:start -->"), t.find("<!-- queue:end -->")
        if a >= 0 and b > a:
            t = t[:a] + "<!-- queue:start -->\n" + cb.queue_md(doc, 15) + "\n" + t[b:]
            g.write_text(t, encoding="utf-8")
    print(f"BOM.md {len(L)}줄 · GAPS 큐 갱신 · 검사 실패 {len(bad)}")
    return 0


if __name__ == "__main__":
    sys.exit(render(Path(sys.argv[1])) if len(sys.argv) > 1 else 2)
