"""V0 초안 작성 보조 — 노드를 짧게 적고 bom@1 꼴로 편다(판정은 check_bom.py)."""
import json
from pathlib import Path

V1 = "미측정 — V1 대상"

def P(id, name, spec):
    return {"id": id, "kind": "product", "parent": None, "name": name, "spec": spec,
            "box_ref": "없음 — 레포에 체인 yaml 없음", "open_questions": []}

def S(id, parent, name, spec, q=None):
    return {"id": id, "kind": "stage", "parent": parent, "name": name, "spec": spec,
            "box_ref": "없음 — 레포에 체인 yaml 없음", "open_questions": q or []}

def I(id, parent, t, name, spec, q=None, absent=None):
    b = f"없음 — {absent}" if absent else V1
    return {"id": id, "kind": "input", "input_type": t, "parent": parent, "name": name, "spec": spec,
            "qty_per_unit": b, "price": b, "cost_share_pct": b, "makers": b,
            "box_ref": "없음 — 레포에 체인 yaml 없음", "open_questions": q or []}

def dump(path, chain, product, unit, nodes, status="v0_draft", approved=None, log=None):
    doc = {"schema": "valuechain/bom@1", "chain": chain, "product": product, "unit_basis": unit,
           "asof": "2026-11-11", "status": status, "approved_by": approved, "stage_log": log or [], "nodes": nodes}
    Path(path).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    return doc

NOBOX = "없음 — 레포에 체인 yaml 없음"

def val(v, unit, src, grade, basis=None, asof="2026-11-11"):
    d = {"v": v, "unit": unit, "asof": asof, "source": src, "grade": grade}
    if basis:
        d["basis"] = basis
    return d

def mk(name, tk, country, role, grade, src, share=None, note=None, parent=None, pt=None):
    m = {"name": name, "country": country, "role": role, "grade": grade, "source": src,
         "share_pct": share if share is not None else "미측정 — 점유율 원천 미확보", "box_ref": NOBOX}
    if tk:
        m["ticker"] = tk
    else:
        m["unlisted"] = {"parent": parent or "독립 비상장", "parent_ticker": pt}
    if note:
        m["note"] = note
    return m

def fill(nodes, id, **kw):
    n = next(x for x in nodes if x["id"] == id)
    n.update(kw)
    return n

def write_sources(path, rows):
    import json
    from pathlib import Path
    Path(path).write_text("\n".join(json.dumps(
        {"id": i, "kind": k, "ref": r, "title": t, "asof": a, "grade": g, "note": n}, ensure_ascii=False)
        for i, k, r, t, a, g, n in rows) + "\n", encoding="utf-8")
