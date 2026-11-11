#!/usr/bin/env python3
"""밸류체인 스터디 bom.json 검사기 — valuechain-study 스킬의 계약 관문.

사용:
  python3 market-intel/valuechain/_contracts/check_bom.py market-intel/valuechain/hbm      # 디렉터리(bom.json·sources.jsonl·GAPS.md)
  python3 market-intel/valuechain/_contracts/check_bom.py --stats <dir>                    # 통계 표(단계·입력·메이커·채움률·연결률)
  python3 market-intel/valuechain/_contracts/check_bom.py --queue <dir> [--top 10]         # equity-study 착수 큐(우선순위)
  python3 market-intel/valuechain/_contracts/check_bom.py --selftest                       # 정상 1 + 변이 미끼 — 막는지 본다
종료코드 0 = 통과, 1 = 막음, 2 = 사용법. 파이프로 삼키지 말 것(rc 는 파이프 밖에서 잰다).

검사 코드:
  B1 트리 정합 — id 유일·꼴, product 정확히 1(parent null), parent 실재, 순환 0, kind 위계(stage→product|stage, input→stage|input)
  B2 깊이 — product→stage→input 이 최소 한 갈래(깊이 ≥3)
  B3 빈칸 규약 — qty_per_unit·price·cost_share_pct·makers 는 input 에 필수, 값 객체 또는 「없음 — 이유」/「미측정 — 이유」(이유 4자+)
  B4 축 선언 — 값 객체는 v·unit·asof·source·grade 필수, unit 비지 않음, 비율 칸(cost_share_pct·share_pct)은 unit %·0~100
  B5 출처 실재 — 모든 source id 가 sources.jsonl 에 있다; sources 행은 id·kind·ref·title·grade
  B6 메이커 — name·grade·source·share_pct·box_ref, ticker 와 unlisted 정확히 하나, 등급 ①②③
  B7 box_ref 실재 — "<yaml stem>#<box id>" 는 core/series/refresh.py G-S3 와 같은 집합(core/valuechain/*.yaml 박스 id)에 있어야 한다
  B8 _inbox 참조 — 빈칸 문면이 `_inbox/<파일>#<pid>` 를 가리키면 그 파일·행(pid)이 실재
  B9 GAPS.md — 존재, 착수 큐 블록(<!-- queue:start --> … <!-- queue:end -->) 존재
  B10 묶음 참조 — 노드 lib_ref 는 process_lib 묶음 id(파일 또는 인라인)로 풀린다, flow_ref 는 flows 키, stage_kind 는 8대 정규화 어휘, 같은 묶음 id 이중 정의 금지
  B11 흐름 정합 — flows 단계 번호 1..N 연속·id sNNN 일치·단계 lib_ref 실재, 묶음 steps 가 flows 에서 다시 잰 값과 같다(손 복사 금지)
  W1(관측) 형제 cost_share_pct 합 > 100 · W2 input_type 누락 · W3 값 grade ③ 비중 · W4 메이커 grade ③ 비중
"""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
GRADES = {"①", "②", "③"}
BLANK_RE = re.compile(r"^(없음|미측정) — (.+)$", re.S)
ID_RE = re.compile(r"^[a-z0-9_]+(\.[a-z0-9_]+)*$")
BOXREF_RE = re.compile(r"^([a-z0-9_]+)#([A-Za-z0-9_.-]+)$")
INBOX_RE = re.compile(r"_inbox/([A-Za-z0-9_.\-]+\.jsonl)#([A-Za-z0-9_.\-]+)")
SRC_RE = re.compile(r"^S\d{3,}$")
INPUT_TYPES = {"material", "equipment", "service_ip", "component"}
KINDS = {"product", "stage", "input"}
STATUSES = {"v0_draft", "v0_approved", "v1_filled", "v2_linked", "v3_queued", "active"}
VAL_FIELDS = ("qty_per_unit", "price", "cost_share_pct")
STAGE_KINDS = {"wafer", "oxidation", "photo", "etch", "deposition", "implant", "metallization", "test", "packaging", "clean", "anneal"}
PCT_FIELDS = ("cost_share_pct",)


# ── G-S3 와 같은 박스 집합 ───────────────────────────────────────────────
def _node_ids_regex(vc_dir: Path) -> set:
    """core/series/refresh.py valuechain_node_ids() 와 같은 규칙 — 그쪽을 못 불러올 때만 쓴다(selftest 가 두 집합 동일을 잰다)."""
    ids = set()
    for f in vc_dir.glob("*.yaml"):
        try:
            txt = f.read_text(encoding="utf-8")
        except OSError:
            continue
        # refresh.py 10-20 수정과 같은 꼴(뒤따르는 주석·따옴표 허용) — 두 정규식은 selftest 가 집합 동일로 묶는다
        for bid in re.findall(r"^\s*-?\s*id:\s*['\"]?([A-Za-z0-9_.-]+)['\"]?\s*(?:#.*)?$", txt, re.M):
            ids.add(bid)
            ids.add(f"{f.stem}#{bid}")
    return ids


def box_ids() -> tuple[set, str]:
    try:
        sys.path.insert(0, str(REPO / "core/series"))
        import refresh  # type: ignore  # noqa: E402
        return set(refresh.valuechain_node_ids()), "core/series/refresh.py:valuechain_node_ids"
    except Exception:  # noqa: BLE001 — yaml 없는 인터프리터 등
        return _node_ids_regex(REPO / "core/valuechain"), "regex 사본(refresh.py 불가 — 같은 정규식)"


# ── 읽기 ────────────────────────────────────────────────────────────────
def load_sources(path: Path) -> tuple[dict, list]:
    bad, src = [], {}
    if not path.exists():
        return src, [f"[B5] sources.jsonl 없음: {path}"]
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError as e:
            bad.append(f"[B5] sources.jsonl:{i} JSON 오류 {e}")
            continue
        for k in ("id", "kind", "ref", "title", "grade"):
            if not r.get(k):
                bad.append(f"[B5] sources.jsonl:{i} `{k}` 빈칸")
        if r.get("grade") and r["grade"] not in GRADES:
            bad.append(f"[B5] sources.jsonl:{i} grade {r['grade']!r} ∉ ①②③")
        if r.get("id"):
            if not SRC_RE.match(str(r["id"])):
                bad.append(f"[B5] sources.jsonl:{i} id 꼴 위반 {r['id']!r}(S + 숫자 3자리+)")
            if r["id"] in src:
                bad.append(f"[B5] sources.jsonl:{i} id 중복 {r['id']}")
            src[r["id"]] = r
    return src, bad


def is_blank(x) -> bool:
    return isinstance(x, str) and bool(BLANK_RE.match(x)) and len(BLANK_RE.match(x).group(2).strip()) >= 4


# ── 판정 ────────────────────────────────────────────────────────────────
def lib_bundles(doc: dict, lib: dict | None) -> tuple[dict, list]:
    """파일 묶음 + 인라인 묶음 → {id: bundle}. 이중 정의는 실패 문면으로 돌려준다."""
    out, bad = {}, []
    for where, arr in (("process_lib_ref", (lib or {}).get("bundles") or []), ("process_lib(인라인)", doc.get("process_lib") or [])):
        for b in arr:
            bid = b.get("id")
            if bid in out:
                bad.append(f"[B10] 묶음 {bid} 이중 정의({where}) — 한 번만 정의한다")
            out[bid] = b
    return out, bad


def judge_lib(lib: dict, bundles: dict) -> list:
    bad = []
    if lib.get("schema") != "valuechain/process_lib@1":
        bad.append(f"[B11] process_lib schema {lib.get('schema')!r} ≠ valuechain/process_lib@1")
    for fid, steps in (lib.get("flows") or {}).items():
        nums = [s.get("step") for s in steps]
        if nums != list(range(1, len(nums) + 1)):
            bad.append(f"[B11] flows.{fid}: 단계 번호가 1..{len(nums)} 연속이 아니다")
        for st in steps:
            if st.get("id") != f"s{int(st.get('step') or 0):03d}":
                bad.append(f"[B11] flows.{fid} 단계 {st.get('step')}: id {st.get('id')!r} ≠ s{int(st.get('step') or 0):03d}")
            if st.get("stage_kind") not in STAGE_KINDS:
                bad.append(f"[B11] flows.{fid} 단계 {st.get('step')}: stage_kind {st.get('stage_kind')!r}")
            for r in st.get("lib_ref") or []:
                if r not in bundles and not is_blank(r):
                    bad.append(f"[B11] flows.{fid} 단계 {st.get('step')}: lib_ref {r} 묶음 없음")
        if fid == "logic_cmos_105":
            for bid, b in bundles.items():
                want = [st["step"] for st in steps if bid in (st.get("lib_ref") or [])]
                if b in ((lib.get("bundles") or [])) and sorted(b.get("steps") or []) != want:
                    bad.append(f"[B11] 묶음 {bid}.steps 가 flows.{fid} 에서 다시 잰 값과 다르다(손 복사·낡은 판) — build_process_lib.py 로 다시 쓴다")
    for bid, b in bundles.items():
        if b.get("stage_kind") not in STAGE_KINDS:
            bad.append(f"[B10] 묶음 {bid}: stage_kind {b.get('stage_kind')!r}")
    return bad


def judge(doc: dict, sources: dict, boxes: set, inbox_dir: Path, gaps_text: str | None, lib: dict | None = None) -> tuple[list, list]:
    bad, warn = [], []
    bundles, bb = lib_bundles(doc, lib)
    bad += bb
    if lib is not None:
        bad += judge_lib(lib, bundles)
    if doc.get("process_lib_ref") and lib is None:
        bad.append(f"[B10] process_lib_ref {doc['process_lib_ref']} 를 읽지 못했다")
    if doc.get("schema") != "valuechain/bom@1":
        bad.append(f"[B1] schema {doc.get('schema')!r} ≠ valuechain/bom@1")
    for k in ("chain", "product", "unit_basis", "asof", "status", "nodes"):
        if not doc.get(k):
            bad.append(f"[B1] 최상위 `{k}` 빈칸")
    if "approved_by" not in doc:
        bad.append("[B1] 최상위 `approved_by` 없음(null 이라도 적는다 — 본체 승인 자리)")
    if doc.get("status") and doc["status"] not in STATUSES:
        bad.append(f"[B1] status {doc['status']!r} ∉ {sorted(STATUSES)}")
    if doc.get("status") not in (None, "v0_draft") and not doc.get("approved_by"):
        bad.append(f"[B1] status {doc.get('status')} 인데 approved_by 비어 있다 — V0 승인 없이 V1 이상 금지")
    nodes = doc.get("nodes") or []
    by_id: dict = {}
    for n in nodes:
        nid = n.get("id")
        if not isinstance(nid, str) or not ID_RE.match(nid):
            bad.append(f"[B1] id 꼴 위반 {nid!r}")
            continue
        if nid in by_id:
            bad.append(f"[B1] id 중복 {nid}")
        by_id[nid] = n
    roots = [n for n in nodes if n.get("kind") == "product"]
    if len(roots) != 1:
        bad.append(f"[B1] product 노드 {len(roots)}개 — 정확히 1")
    for n in nodes:
        nid, kind, par = n.get("id"), n.get("kind"), n.get("parent")
        if kind not in KINDS:
            bad.append(f"[B1] {nid}: kind {kind!r} ∉ product|stage|input")
            continue
        for k in ("name", "spec"):
            if not (isinstance(n.get(k), str) and len(n[k].strip()) >= (1 if k == "name" else 4)):
                bad.append(f"[B1] {nid}: `{k}` 빈칸·너무 짧음")
        if "open_questions" not in n or not isinstance(n.get("open_questions"), list):
            bad.append(f"[B1] {nid}: open_questions 배열 없음(비어도 키는 둔다)")
        if kind == "product":
            if par is not None:
                bad.append(f"[B1] {nid}: product 의 parent 는 null")
            continue
        if par not in by_id:
            bad.append(f"[B1] {nid}: parent {par!r} 실재하지 않음")
            continue
        pk = by_id[par].get("kind")
        if kind == "stage" and pk not in ("product", "stage"):
            bad.append(f"[B1] {nid}: stage 의 parent 는 product|stage (지금 {pk})")
        if kind == "input" and pk not in ("stage", "input"):
            bad.append(f"[B1] {nid}: input 의 parent 는 stage|input (지금 {pk})")
    # 순환
    for nid in by_id:
        seen, cur = set(), nid
        while cur is not None and cur in by_id:
            if cur in seen:
                bad.append(f"[B1] 순환: {nid} 에서 {cur} 로 되돌아온다")
                break
            seen.add(cur)
            cur = by_id[cur].get("parent")
    # 깊이
    def depth(nid, lim=50):
        d, cur = 1, by_id.get(nid, {}).get("parent")
        while cur is not None and cur in by_id and lim:
            d, cur, lim = d + 1, by_id[cur].get("parent"), lim - 1
        return d
    inputs = [n for n in nodes if n.get("kind") == "input"]
    if not any(depth(n["id"]) >= 3 for n in inputs if n.get("id") in by_id):
        bad.append("[B2] 깊이 ≥3(product→stage→input) 갈래가 없다")

    def check_val(where: str, field: str, x, required: bool):
        if x is None:
            if required:
                bad.append(f"[B3] {where}.{field}: 키 없음 — 값/「없음 — 이유」/「미측정 — 이유」 중 하나")
            return
        if isinstance(x, str):
            if not is_blank(x):
                bad.append(f"[B3] {where}.{field}: 빈칸 문면 {x[:40]!r} — 「없음 — <이유 4자+>」 또는 「미측정 — <이유 4자+>」만")
            else:
                check_inbox(where, field, x)
            return
        if not isinstance(x, dict):
            bad.append(f"[B3] {where}.{field}: 값 객체도 빈칸 문면도 아님({type(x).__name__})")
            return
        for k in ("v", "unit", "asof", "source", "grade"):
            if k not in x or x[k] in (None, ""):
                bad.append(f"[B4] {where}.{field}: `{k}` 없음 — 값에는 축(unit)·시점·출처·등급")
        if x.get("grade") and x["grade"] not in GRADES:
            bad.append(f"[B4] {where}.{field}: grade {x['grade']!r} ∉ ①②③")
        s = x.get("source")
        if s and s not in sources:
            bad.append(f"[B5] {where}.{field}: source {s} 가 sources.jsonl 에 없다")
        if field in PCT_FIELDS or field == "share_pct":
            if x.get("unit") and x["unit"] != "%":
                bad.append(f"[B4] {where}.{field}: 비율 칸 unit 은 % (지금 {x['unit']!r})")
            vals = x.get("v") if isinstance(x.get("v"), list) else [x.get("v")]
            for v in vals:
                if isinstance(v, (int, float)) and not (0 <= v <= 100):
                    bad.append(f"[B4] {where}.{field}: {v} 는 0~100 밖")

    def check_inbox(where, field, text):
        for fn, pid in INBOX_RE.findall(text):
            p = inbox_dir / fn
            if not p.exists():
                bad.append(f"[B8] {where}.{field}: _inbox/{fn} 실재하지 않음")
                continue
            if f'"proposal_id": "{pid}"' not in p.read_text(encoding="utf-8"):
                bad.append(f"[B8] {where}.{field}: _inbox/{fn} 에 proposal_id {pid} 행 없음")

    def check_box(where, x):
        if x is None:
            bad.append(f"[B7] {where}.box_ref: 키 없음 — 박스 id 또는 「없음/미측정 — 이유」")
            return
        if isinstance(x, str) and BOXREF_RE.match(x):
            if x not in boxes:
                bad.append(f"[B7] {where}.box_ref `{x}` 가 core/valuechain/*.yaml 박스에 없다(G-S3 집합)")
            return
        if is_blank(x):
            check_inbox(where, "box_ref", x)
            return
        bad.append(f"[B7] {where}.box_ref {str(x)[:40]!r} — 「<yaml stem>#<box id>」 또는 빈칸 규약")

    # 묶음 참조
    flows = (lib or {}).get("flows") or {}
    for n in nodes:
        for r in n.get("lib_ref") or []:
            if r not in bundles:
                bad.append(f"[B10] {n.get('id')}: lib_ref {r} 가 process_lib 묶음에 없다")
        if n.get("flow_ref") and n["flow_ref"] not in flows:
            bad.append(f"[B10] {n.get('id')}: flow_ref {n['flow_ref']} 가 process_lib flows 에 없다")
        if n.get("stage_kind") is not None and n["stage_kind"] not in STAGE_KINDS:
            bad.append(f"[B10] {n.get('id')}: stage_kind {n['stage_kind']!r} ∉ 8대 정규화 어휘")
    lib_inputs = []
    for bid, b in bundles.items():
        for i in b.get("inputs") or []:
            if i.get("parent") not in (None, bid):
                bad.append(f"[B10] 묶음 {bid} 입력 {i.get('id')}: parent {i.get('parent')!r} ≠ 묶음 id")
            if not str(i.get("id", "")).startswith(bid + "."):
                bad.append(f"[B10] 묶음 {bid} 입력 id {i.get('id')!r} 는 「{bid}.」 로 시작해야 한다")
            lib_inputs.append({**i, "parent": bid, "kind": "input"})
    n_g3 = n_val = 0
    for n in nodes + lib_inputs:
        nid = n.get("id")
        if n.get("kind") not in KINDS:
            continue
        check_box(nid, n.get("box_ref"))
        req = n.get("kind") == "input"
        for f in VAL_FIELDS:
            check_val(nid, f, n.get(f), req)
            if isinstance(n.get(f), dict):
                n_val += 1
                n_g3 += n[f].get("grade") == "③"
        if req and n.get("input_type") not in INPUT_TYPES:
            (bad if n.get("input_type") is not None else warn).append(
                f"[{'B1' if n.get('input_type') is not None else 'W2'}] {nid}: input_type {n.get('input_type')!r} ∉ {sorted(INPUT_TYPES)}")
        mk = n.get("makers")
        if req and mk is None:
            bad.append(f"[B3] {nid}.makers: 키 없음")
        if isinstance(mk, str):
            check_val(nid, "makers", mk, req) if not is_blank(mk) else check_inbox(nid, "makers", mk)
        elif isinstance(mk, list):
            if req and not mk:
                bad.append(f"[B3] {nid}.makers: 빈 배열 — 메이커를 못 찾았으면 「미측정 — 이유」")
            for j, m in enumerate(mk):
                w = f"{nid}.makers[{j}]({m.get('name', '?')})"
                if not m.get("name"):
                    bad.append(f"[B6] {w}: name 빈칸")
                has_t, has_u = bool(m.get("ticker")), isinstance(m.get("unlisted"), dict)
                if has_t == has_u:
                    bad.append(f"[B6] {w}: ticker 와 unlisted 중 정확히 하나")
                if has_u and not m["unlisted"].get("parent"):
                    bad.append(f"[B6] {w}: unlisted.parent 빈칸(비상장은 모회사·소유 구조를 적는다 — 없으면 「독립 비상장」)")
                if m.get("grade") not in GRADES:
                    bad.append(f"[B6] {w}: grade {m.get('grade')!r} ∉ ①②③")
                if not m.get("source"):
                    bad.append(f"[B6] {w}: source 빈칸")
                elif m["source"] not in sources:
                    bad.append(f"[B5] {w}: source {m['source']} 가 sources.jsonl 에 없다")
                check_val(w, "share_pct", m.get("share_pct"), True)
                check_box(w, m.get("box_ref"))
        elif mk is not None:
            bad.append(f"[B3] {nid}.makers: 배열도 빈칸 문면도 아님")
    # 형제 비중 합
    sib: dict = {}
    for n in nodes:
        c = n.get("cost_share_pct")
        if isinstance(c, dict) and isinstance(c.get("v"), (int, float)):
            sib.setdefault(n.get("parent"), []).append(c["v"])
    for p, vs in sib.items():
        if sum(vs) > 100.5:
            warn.append(f"[W1] {p}: 자식 cost_share_pct 합 {sum(vs):.1f}% > 100")
    mk_all = [m for n in nodes + lib_inputs if isinstance(n.get("makers"), list) for m in n["makers"]]
    mk3 = sum(m.get("grade") == "③" for m in mk_all)
    if mk_all and mk3 / len(mk_all) > 0.5:
        warn.append(f"[W4] 메이커 행 {len(mk_all)} 중 grade ③ {mk3}({100 * mk3 // len(mk_all)}%) — 메이커 실재·역할을 ①②(공시·IR·셀사이드)로 대조할 것(V4)")
    if n_val and n_g3 / n_val > 0.5:
        warn.append(f"[W3] 값 객체 {n_val} 중 grade ③(모델 지식) {n_g3} — 절반 초과, V4 에서 ①② 로 갈아끼울 것")
    # GAPS
    if gaps_text is None:
        bad.append("[B9] GAPS.md 없음 — 모르는 것·사용자 손·equity-study 착수 큐")
    elif "<!-- queue:start -->" not in gaps_text or "<!-- queue:end -->" not in gaps_text:
        bad.append("[B9] GAPS.md 에 착수 큐 블록(<!-- queue:start --> … <!-- queue:end -->) 없음")
    return bad, warn


def check_dir(d: Path, boxes: set) -> tuple[list, list, dict, dict]:
    bom = d / "bom.json"
    if not bom.exists():
        return [f"[B1] bom.json 없음: {bom}"], [], {}, {}
    try:
        doc = json.loads(bom.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"[B1] bom.json JSON 오류 {e}"], [], {}, {}
    sources, sbad = load_sources(d / "sources.jsonl")
    g = d / "GAPS.md"
    lib = None
    if doc.get("process_lib_ref"):
        lp = REPO / doc["process_lib_ref"]
        if lp.exists():
            lib = json.loads(lp.read_text(encoding="utf-8"))
            ls, lbad = load_sources(lp.parent / "sources.jsonl")
            for k in ls:
                if k in sources:
                    sbad.append(f"[B5] source id {k} 가 체인 sources.jsonl 과 묶음 sources.jsonl 에 둘 다 있다")
            sources = {**ls, **sources}
            sbad += lbad
    bad, warn = judge(doc, sources, boxes, REPO / "core/valuechain/_inbox", g.read_text(encoding="utf-8") if g.exists() else None, lib)
    doc["_lib"] = lib
    # 스키마(있으면 추가로) — 의미 검사는 위가 정본, jsonschema 는 꼴 이중 확인
    try:
        import jsonschema  # type: ignore
        sch = json.loads((HERE / "bom.schema.json").read_text(encoding="utf-8"))
        for e in sorted(jsonschema.Draft202012Validator(sch).iter_errors(doc), key=lambda e: list(e.path))[:30]:
            bad.append(f"[SCHEMA] {'/'.join(str(p) for p in e.path)}: {e.message[:160]}")
    except ImportError:
        warn.append("[W0] jsonschema 부재 — 꼴 이중 확인 건너뜀(의미 검사 B1~B9 는 돌았다)")
    return sbad + bad, warn, doc, sources


# ── 통계·큐 ─────────────────────────────────────────────────────────────
LISTED_W = {"krx": 1.0, "overseas": 0.8, "unlisted_listed_parent": 0.4, "unlisted": 0.1}


def listing(m: dict) -> str:
    t = m.get("ticker")
    if t:
        return "krx" if re.fullmatch(r"\d{6}", t) else "overseas"
    u = m.get("unlisted") or {}
    return "unlisted_listed_parent" if u.get("parent_ticker") else "unlisted"


def _num(x):
    if isinstance(x, dict):
        v = x.get("v")
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, list) and v and all(isinstance(a, (int, float)) for a in v):
            return sum(v) / len(v)
    return None


def referenced_bundles(doc: dict) -> list:
    """bom 노드가 lib_ref 로 가리키거나 flow_ref 흐름의 단계가 가리키는 묶음(중복 없이, 등장 순)."""
    lib = doc.get("_lib") or {}
    allb = {b["id"]: b for b in (lib.get("bundles") or []) + (doc.get("process_lib") or [])}
    ids = []
    for n in doc.get("nodes") or []:
        refs = list(n.get("lib_ref") or [])
        for st in (lib.get("flows") or {}).get(n.get("flow_ref") or "", []):
            refs += [r for r in st.get("lib_ref") or [] if r in allb]
        for r in refs:
            if r in allb and r not in ids:
                ids.append(r)
    return [allb[i] for i in ids]


def all_inputs(doc: dict) -> list:
    out = [n for n in doc.get("nodes") or [] if n.get("kind") == "input"]
    for b in referenced_bundles(doc):
        out += [{**i, "parent": b["id"], "kind": "input"} for i in b.get("inputs") or []]
    return out


def stats(doc: dict) -> dict:
    nodes = doc.get("nodes") or []
    by = {n["id"]: n for n in nodes}
    inputs = all_inputs(doc)
    for b in referenced_bundles(doc):
        by[b["id"]] = {"id": b["id"], "parent": None}
    for i in inputs:
        by.setdefault(i["id"], i)
    stages = [n for n in nodes if n.get("kind") == "stage"]
    makers = [m for n in inputs if isinstance(n.get("makers"), list) for m in n["makers"]]
    uniq = {}
    for m in makers:
        uniq.setdefault(m.get("ticker") or m["name"], m)  # 티커로 접는다(이름 변형 중복 방지), 비상장은 이름
    def depth(nid):
        d, cur = 1, by[nid].get("parent")
        while cur in by:
            d, cur = d + 1, by[cur].get("parent")
        return d
    price_v = sum(isinstance(n.get("price"), dict) for n in inputs)
    cs_v = sum(isinstance(n.get("cost_share_pct"), dict) for n in inputs)
    qty_v = sum(isinstance(n.get("qty_per_unit"), dict) for n in inputs)
    share_v = sum(isinstance(m.get("share_pct"), dict) for m in makers)
    linked_m = sum(bool(BOXREF_RE.match(str(m.get("box_ref") or ""))) for m in makers)
    linked_u = sum(bool(BOXREF_RE.match(str(m.get("box_ref") or ""))) for m in uniq.values())
    lst = {}
    for m in uniq.values():
        lst[listing(m)] = lst.get(listing(m), 0) + 1
    it = {}
    for n in inputs:
        it[n.get("input_type")] = it.get(n.get("input_type"), 0) + 1
    return {"stages": len(stages), "bundles_referenced": len(referenced_bundles(doc)), "inputs_bom": sum(n.get("kind") == "input" for n in nodes), "inputs": len(inputs), "input_types": it, "max_depth": max((depth(n["id"]) for n in nodes), default=0), "max_depth_with_lib": max((depth(n["id"]) for n in nodes), default=0) + (2 if referenced_bundles(doc) else 0),
            "maker_rows": len(makers), "makers_unique": len(uniq), "listing": lst,
            "qty_filled": f"{qty_v}/{len(inputs)}", "price_filled": f"{price_v}/{len(inputs)}", "cost_share_filled": f"{cs_v}/{len(inputs)}",
            "price_or_cost_fill_pct": round(100 * sum(isinstance(n.get('price'), dict) or isinstance(n.get('cost_share_pct'), dict) for n in inputs) / max(1, len(inputs)), 1),
            "share_filled": f"{share_v}/{len(makers)}",
            "box_link_rows": f"{linked_m}/{len(makers)}", "box_link_unique": f"{linked_u}/{len(uniq)}",
            "box_link_pct_unique": round(100 * linked_u / max(1, len(uniq)), 1)}


def queue(doc: dict, top: int = 10) -> list[dict]:
    """기업별 우선순위 = Σ_입력 (원가 비중 × 점유율) × 상장 가중. 미측정은 대체 가중(비중 2%·점유율 = 1/메이커 수)으로 두고 표시한다."""
    rows: dict = {}
    for n in all_inputs(doc):
        if not isinstance(n.get("makers"), list):
            continue
        cs = _num(n.get("cost_share_pct"))
        cs_m = cs is not None
        cs = cs if cs_m else 2.0
        k = max(1, len(n["makers"]))
        for m in n["makers"]:
            sh = _num(m.get("share_pct"))
            sh_m = sh is not None
            sh = sh if sh_m else 100.0 / k
            w = LISTED_W[listing(m)]
            key = m.get("ticker") or m["name"]  # 같은 회사가 이름 변형(Tokyo Electron / Tokyo Electron(TEL))으로 와도 티커로 접는다
            r = rows.setdefault(key, {"name": m["name"], "ticker": m.get("ticker") or f"비상장({(m.get('unlisted') or {}).get('parent', '?')})",
                                            "listing": listing(m), "score": 0.0, "inputs": [], "measured": 0, "proxied": 0,
                                            "box_ref": m.get("box_ref") if BOXREF_RE.match(str(m.get("box_ref") or "")) else None})
            r["score"] += cs * sh / 100.0 * w
            if n["id"].split(".")[-1] not in r["inputs"]:
                r["inputs"].append(n["id"].split(".")[-1])
            if cs_m and sh_m:
                r["measured"] += 1
            else:
                r["proxied"] += 1
    out = sorted(rows.values(), key=lambda r: -r["score"])
    return out[:top] if top else out


def queue_md(doc: dict, top: int = 10) -> str:
    lines = ["| # | 기업 | 티커 | 상장 | 점수 | 입력 | 실측/대체 | box_ref |", "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(queue(doc, top), 1):
        lines.append(f"| {i} | {r['name']} | {r['ticker']} | {r['listing']} | {r['score']:.2f} | {', '.join(r['inputs'][:4])} | {r['measured']}/{r['proxied']} | {r['box_ref'] or '없음 — 새 박스 후보'} |")
    return "\n".join(lines)


# ── selftest ────────────────────────────────────────────────────────────
def _fixture(boxes: set) -> tuple[dict, dict, str]:
    ref = next((b for b in sorted(boxes) if "#" in b and b.startswith("semi_krx_subchains#semi.back")), None) or next(b for b in sorted(boxes) if "#" in b)
    v = lambda x, u: {"v": x, "unit": u, "asof": "2026-10-20", "source": "S001", "grade": "③"}  # noqa: E731
    doc = {"schema": "valuechain/bom@1", "chain": "t", "product": "테스트", "unit_basis": "1 개", "asof": "2026-10-20", "status": "v1_filled",
           "approved_by": {"who": "selftest", "at": "2026-10-20", "stage": "V0", "note": "미끼"},
           "nodes": [
               {"id": "t", "kind": "product", "parent": None, "name": "제품", "spec": "제품 규격", "box_ref": "없음 — 제품 노드는 박스 축 아님", "open_questions": []},
               {"id": "t.s", "kind": "stage", "parent": "t", "name": "단계", "spec": "단계 규격", "box_ref": ref, "open_questions": []},
               {"id": "t.s.i", "kind": "input", "input_type": "equipment", "parent": "t.s", "name": "입력", "spec": "입력 규격",
                "qty_per_unit": v(1, "대/라인"), "price": "미측정 — 공개 가격 없음", "cost_share_pct": v(10, "%"),
                "makers": [{"name": "갑", "ticker": "000000", "share_pct": v(50, "%"), "grade": "③", "source": "S001", "box_ref": ref},
                           {"name": "을", "unlisted": {"parent": "병", "parent_ticker": None}, "share_pct": "미측정 — 공개 점유율 없음", "grade": "③", "source": "S001", "box_ref": "없음 — 새 박스 후보"}],
                "box_ref": ref, "open_questions": []}]}
    src = {"S001": {"id": "S001", "kind": "model_knowledge", "ref": "모델 지식—검증 필요", "title": "t", "grade": "③"}}
    return doc, src, "<!-- queue:start -->\n<!-- queue:end -->"


def selftest() -> int:
    boxes, how = box_ids()
    fails = []
    # 0) 두 집합 동일(refresh.py 를 부를 수 있을 때)
    rx = _node_ids_regex(REPO / "core/valuechain")
    if how.startswith("core/series") and rx != boxes:
        fails.append(f"G-S3 집합과 regex 사본이 다르다(차 {len(rx ^ boxes)})")
    doc, src, gaps = _fixture(boxes)
    b, _ = judge(doc, src, boxes, REPO / "core/valuechain/_inbox", gaps)
    if b:
        fails.append(f"정상 미끼가 막혔다(자명참 baseline 실패): {b[:3]}")

    def mut(name, code, f):
        d, s, g = copy.deepcopy(doc), copy.deepcopy(src), gaps
        r = f(d, s)
        if r is not None:
            g = r
        bb, _ = judge(d, s, boxes, REPO / "core/valuechain/_inbox", g)
        hit = any(x.startswith(f"[{code}]") for x in bb)
        print(f"  {'OK ' if hit else 'MISS'} {code} {name}" + ("" if hit else f"  → {bb[:2]}"))
        if not hit:
            fails.append(f"변이 {name} 을 {code} 가 못 막음")
    I = lambda d: d["nodes"][2]  # noqa: E731
    mut("parent 부재", "B1", lambda d, s: I(d).__setitem__("parent", "t.zz"))
    mut("순환", "B1", lambda d, s: d["nodes"][1].__setitem__("parent", "t.s.i"))
    mut("product 2개", "B1", lambda d, s: d["nodes"][1].__setitem__("kind", "product"))
    mut("id 중복", "B1", lambda d, s: d["nodes"].append(copy.deepcopy(d["nodes"][2])))
    mut("input 이 product 직속", "B1", lambda d, s: I(d).__setitem__("parent", "t"))
    mut("승인 없이 v1", "B1", lambda d, s: d.__setitem__("approved_by", None))
    mut("깊이 2", "B2", lambda d, s: (I(d).__setitem__("parent", "t"), I(d).__setitem__("kind", "stage")))
    mut("빈칸 이유 없음", "B3", lambda d, s: I(d).__setitem__("price", "미측정"))
    mut("빈칸 무언(빈 문자열)", "B3", lambda d, s: I(d).__setitem__("price", ""))
    mut("price 키 삭제", "B3", lambda d, s: I(d).pop("price"))
    mut("makers 빈 배열", "B3", lambda d, s: I(d).__setitem__("makers", []))
    mut("값에 unit 없음", "B4", lambda d, s: I(d)["qty_per_unit"].pop("unit"))
    mut("비중 unit ≠ %", "B4", lambda d, s: I(d)["cost_share_pct"].__setitem__("unit", "USD"))
    mut("비중 130", "B4", lambda d, s: I(d)["cost_share_pct"].__setitem__("v", 130))
    mut("source 미등록", "B5", lambda d, s: I(d)["qty_per_unit"].__setitem__("source", "S999"))
    mut("메이커 source 미등록", "B5", lambda d, s: I(d)["makers"][0].__setitem__("source", "S998"))
    mut("ticker+unlisted 둘 다", "B6", lambda d, s: I(d)["makers"][0].__setitem__("unlisted", {"parent": "x"}))
    mut("ticker·unlisted 둘 다 없음", "B6", lambda d, s: I(d)["makers"][1].pop("unlisted"))
    mut("메이커 등급 ④", "B6", lambda d, s: I(d)["makers"][0].__setitem__("grade", "④"))
    mut("box_ref 가짜 id", "B7", lambda d, s: I(d).__setitem__("box_ref", "memory#semi.pkg.nonexistent_box"))
    mut("메이커 box_ref 가짜", "B7", lambda d, s: I(d)["makers"][0].__setitem__("box_ref", "semi_krx_subchains#semi.back.zz"))
    mut("_inbox 파일 부재", "B8", lambda d, s: I(d).__setitem__("box_ref", "없음 — 새 박스 _inbox/nope_20990101.jsonl#P1"))
    mut("GAPS 큐 블록 없음", "B9", lambda d, s: "# GAPS\n큐 없음")
    # GAPS.md 자체가 없음(gaps_text=None) — mut() 는 None 반환을 「바꾸지 않음」으로 읽으므로 직접 부른다
    bb, _ = judge(copy.deepcopy(doc), copy.deepcopy(src), boxes, REPO / "core/valuechain/_inbox", None)
    hit = any(x.startswith("[B9]") for x in bb)
    print(f"  {'OK ' if hit else 'MISS'} B9 GAPS.md 없음" + ("" if hit else f"  → {bb[:2]}"))
    if not hit:
        fails.append("변이 GAPS.md 없음 을 B9 가 못 막음")
    # 묶음 라이브러리 미끼 — 정상 lib 1 + 변이
    lib = {"schema": "valuechain/process_lib@1", "asof": "2026-10-20", "source": {"path": "t"},
           "flows": {"logic_cmos_105": [{"step": 1, "id": "s001", "title": "a", "process_tag": "3 포토", "stage_kind": "photo", "lib_ref": ["lib.p"]},
                                         {"step": 2, "id": "s002", "title": "b", "process_tag": "4 식각", "stage_kind": "etch", "lib_ref": ["lib.p"]}]},
           "bundles": [{"id": "lib.p", "name": "포토", "stage_kind": "photo", "steps": [1, 2], "inputs": [
               {**copy.deepcopy(doc["nodes"][2]), "id": "lib.p.scanner", "parent": "lib.p"}]}]}
    ldoc = copy.deepcopy(doc)
    ldoc["process_lib_ref"] = "t"
    ldoc["nodes"][1]["lib_ref"] = ["lib.p"]
    ldoc["nodes"][1]["flow_ref"] = "logic_cmos_105"
    ldoc["nodes"][1]["stage_kind"] = "photo"
    b0, _ = judge(ldoc, src, boxes, REPO / "core/valuechain/_inbox", gaps, lib)
    if b0:
        fails.append(f"정상 lib 미끼가 막혔다: {b0[:3]}")

    def lmut(name, code, f):
        d, L = copy.deepcopy(ldoc), copy.deepcopy(lib)
        f(d, L)
        bb, _ = judge(d, src, boxes, REPO / "core/valuechain/_inbox", gaps, L)
        hit = any(x.startswith(f"[{code}]") for x in bb)
        print(f"  {'OK ' if hit else 'MISS'} {code} {name}" + ("" if hit else f"  → {bb[:2]}"))
        if not hit:
            fails.append(f"lib 변이 {name} 을 {code} 가 못 막음")
    lmut("lib_ref 없는 묶음", "B10", lambda d, L: d["nodes"][1].__setitem__("lib_ref", ["lib.zz"]))
    lmut("flow_ref 없는 흐름", "B10", lambda d, L: d["nodes"][1].__setitem__("flow_ref", "nand_999"))
    lmut("stage_kind 어휘 밖", "B10", lambda d, L: d["nodes"][1].__setitem__("stage_kind", "포토"))
    lmut("묶음 이중 정의(인라인)", "B10", lambda d, L: d.__setitem__("process_lib", copy.deepcopy(L["bundles"])))
    lmut("묶음 입력 id 접두 위반", "B10", lambda d, L: L["bundles"][0]["inputs"][0].__setitem__("id", "x.scanner"))
    lmut("흐름 번호 건너뜀", "B11", lambda d, L: L["flows"]["logic_cmos_105"][1].__setitem__("step", 3))
    lmut("묶음 steps 손 복사 어긋남", "B11", lambda d, L: L["bundles"][0].__setitem__("steps", [1]))
    lmut("흐름 단계 lib_ref 없는 묶음", "B11", lambda d, L: L["flows"]["logic_cmos_105"][0].__setitem__("lib_ref", ["lib.nope"]))
    lmut("묶음 입력 메이커 ticker·unlisted 둘 다", "B6", lambda d, L: L["bundles"][0]["inputs"][0]["makers"][0].__setitem__("unlisted", {"parent": "x"}))
    lmut("묶음 입력 box_ref 가짜", "B7", lambda d, L: L["bundles"][0]["inputs"][0].__setitem__("box_ref", "memory#semi.zz"))
    # 끝단(check_dir) — 디렉터리 읽기 경로(파일 이름 bom.json·sources.jsonl·GAPS.md)까지 실제 파일로 본다.
    #   judge() 만 부르는 위 변이는 파일 이름 문자열이 바뀌어도(예 GAPS.md → GAPZ.md) 못 잡는다.
    import tempfile
    edoc = copy.deepcopy(doc)
    edoc["unit_basis"] = "제품 1 개 기준"
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        def lay(with_gaps=True, with_sources=True):
            for nm in ("bom.json", "sources.jsonl", "GAPS.md"):
                (tdp / nm).unlink(missing_ok=True)
            (tdp / "bom.json").write_text(json.dumps(edoc, ensure_ascii=False), encoding="utf-8")
            if with_sources:
                (tdp / "sources.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in src.values()),
                                                   encoding="utf-8")
            if with_gaps:
                (tdp / "GAPS.md").write_text(gaps, encoding="utf-8")
            return check_dir(tdp, boxes)[0]
        e0 = lay()
        if e0:
            fails.append(f"끝단 정상 디렉터리가 막혔다: {e0[:3]}")
        for name, code, kw in (("디렉터리에 GAPS.md 없음", "B9", {"with_gaps": False}),
                               ("디렉터리에 sources.jsonl 없음", "B5", {"with_sources": False})):
            eb = lay(**kw)
            hit = any(x.startswith(f"[{code}]") for x in eb)
            print(f"  {'OK ' if hit else 'MISS'} {code} 끝단 {name}" + ("" if hit else f"  → {eb[:2]}"))
            if not hit:
                fails.append(f"끝단 변이 {name} 을 {code} 가 못 막음")
    print(f"selftest: 집합 출처 = {how} · 박스 id {len(boxes)}")
    if fails:
        print("selftest FAIL:\n  " + "\n  ".join(fails))
        return 1
    print("selftest PASS — 정상 3(bom·lib·끝단 디렉터리) 통과 · 변이 36 전부 막음")
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "--selftest":
        return selftest()
    mode = None
    if argv[0] in ("--stats", "--queue"):
        mode, argv = argv[0], argv[1:]
    top = 10
    if "--top" in argv:
        i = argv.index("--top")
        top = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    boxes, how = box_ids()
    rc = 0
    for a in argv:
        d = Path(a)
        d = d.parent if d.name == "bom.json" else d
        bad, warn, doc, _ = check_dir(d, boxes)
        if mode == "--stats" and doc:
            print(json.dumps(stats(doc), ensure_ascii=False, indent=1))
        elif mode == "--queue" and doc:
            print(queue_md(doc, top))
        else:
            for w in warn:
                print("  warn " + w)
            for x in bad:
                print("  FAIL " + x)
            print(f"{d}: {'PASS' if not bad else 'FAIL'} — 실패 {len(bad)} · 관측 {len(warn)} · 박스 집합 {how}")
        rc |= 1 if bad else 0
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
