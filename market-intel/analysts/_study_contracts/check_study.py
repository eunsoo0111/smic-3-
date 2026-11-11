#!/usr/bin/env python3
"""equity-study 계약 검사기 — narrative.json / findings.json / tracking_register.json.
사용: python3 check_study.py <study_dir> [--strict-review-check] [--strict-blind]
--strict-blind: blind_contrast.stages 의 S0b(price_drivers 있을 때)·S2_consensus(consensus_check.json 있을 때)
무하네스 짝 부재·불량(해시·출력·disposition·web_used)을 rc 1 로. 기본은 관측, S0 착수일 ≥ 2026-11-01 이면 자동 rc 1.
      (rc 0 통과 / 1 막음 / 3 못 읽음). 파이프로 삼키지 말 것.
--strict-review-check: s2_review_by_main 의 review_check(5+1검사, equity-study SKILL §1-B)
누락·불통·sha256 불일치를 지금은 관측(~)으로만 찍지만, 이 플래그를 주면 오류(✗, rc 1)로 막는다.
2026-10-15 이후 착수하는 스터디부터 이 플래그를 상시 켠다(그 전엔 과거 스터디 소급 검사가
막히지 않도록 관측만).

이음매 계약 3블록: narrative.json 의
cycle_context · blind_contrast · chain_position. S0 착수일(joint_gate: created 와 git 최초 추가일 중
늦은 쪽, git 이력이 없으면 created, 둘 다 없으면 「못 잼」 = 막지 않고 큰 경고; asof 는 안 씀)이
JOINT_EFFECTIVE(2026-10-05) 이상이면 누락·불량 = 오류(rc 1), 그 전 팩은 관측(~)만 — 진행 중인
스터디를 소급으로 막지 않는다(--strict-review-check 와 같은 「날짜 뒤에만 막는다」 관용구를
플래그 대신 날짜로 자동화). --selftest 가 픽스처·변이 검사를 돈다."""
import sys, os, json, re, hashlib, subprocess, copy, datetime, glob
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
JOINT_EFFECTIVE = "2026-10-05"
JOINT_KEYS = ("cycle_context", "blind_contrast", "chain_position")
def load(p):
    try: return json.load(open(p, encoding="utf-8"))
    except FileNotFoundError: return None
    except Exception as e: sys.exit(f"못 읽음 {p}: {e}") or 3
def validate(obj, schema, loc, errs):
    try:
        import jsonschema
        for e in jsonschema.Draft202012Validator(schema).iter_errors(obj):
            errs.append(f"{loc}: {'/'.join(map(str,e.path))}: {e.message[:140]}")
    except ImportError:
        for k in schema.get("required", []):
            if k not in obj: errs.append(f"{loc}: 필수 키 누락 `{k}`")
BLANK = re.compile(r"^(모름 — (공시_미제공|미측정|not_collected|not_applicable)|없음 — .+|미측정 — .+)")
def dualization_residue(study_dir):
    """과제 21: study_dir(=packs/<ticker>/study)의 형제 sources/ 에 *.jsonl 이 남아있으면
    「이원화 잔재」— market-intel/nodes/<ticker>/sources/ 가 정본이어야 하는데 팩에 옛 사본이
    그대로 있다는 뜻. 관측만(rc 0, errs 아닌 warns) — POINTER.json 만 있으면(jsonl 없음) 통과."""
    pack_dir = os.path.dirname(os.path.normpath(study_dir))
    sdir = os.path.join(pack_dir, "sources")
    if not os.path.isdir(sdir):
        return []
    try:
        names = sorted(fn for fn in os.listdir(sdir) if fn.endswith(".jsonl"))
    except OSError:
        return []
    return names
def review_check_issue(nar):
    """s2_review_by_main 이 있는데 review_check 가 없거나 verdict!=pass 거나 review_sha256 이
    지금 판정문 텍스트와 다르면(=판정문이 검사 뒤 바뀜) 사유 문자열을 돌려준다. 문제 없으면 None."""
    review = nar.get("s2_review_by_main")
    if not isinstance(review, str) or not review.strip():
        return None
    cur_sha = hashlib.sha256(review.encode("utf-8")).hexdigest()[:12]
    rc = nar.get("review_check")
    if not isinstance(rc, dict) or not rc:
        return "s2_review_by_main 있는데 review_check 없음 — 5+1검사(SKILL §1-B) 안 됨"
    reasons = []
    if rc.get("verdict") != "pass": reasons.append(f"verdict={rc.get('verdict')!r}(pass 아님)")
    if rc.get("review_sha256") != cur_sha: reasons.append(f"review_sha256 불일치(검사 뒤 판정문 변경 의심): 저장={rc.get('review_sha256')!r} 현재={cur_sha!r}")
    if reasons: return "review_check 불통 — " + " · ".join(reasons)
    return None
def c5_exception_missing_reason(nar):
    """24-e: review_check.checks.c5_base_fires_and_first_date == 'na' 인데
    checks.c5_exception_reason 이 없거나 빈 문자열이면 사유 문자열을 돌려준다(equity-study SKILL
    §1-B c5 설계 예외 — na 는 사유 필수). 관측만(rc 0, warns) — 스키마 필수 필드 아님."""
    rc = nar.get("review_check")
    if not isinstance(rc, dict): return None
    checks = rc.get("checks")
    if not isinstance(checks, dict): return None
    if checks.get("c5_base_fires_and_first_date") != "na": return None
    reason = checks.get("c5_exception_reason")
    if not isinstance(reason, str) or not reason.strip():
        return "review_check.checks.c5_base_fires_and_first_date=na 인데 c5_exception_reason 없음 — c5 설계 예외(SKILL §1-B)는 사유 필수"
    return None
# ── 이음매 계약 — 날짜 관문 ────────────────────────────────────────────
_FORCE_NO_JSONSCHEMA = False   # 자가시험용: jsonschema 부재 모의
def _have_jsonschema():
    if _FORCE_NO_JSONSCHEMA: return False
    try:
        import jsonschema  # noqa: F401
        return True
    except ImportError:
        return False
def parse_date(s):
    """YYYY-MM-DD 이고 달력에 있는 날짜만(2026-99-99·0000-00-00 거부) → ISO 문자열, 아니면 None."""
    if not isinstance(s, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s.strip()): return None
    try: return datetime.date.fromisoformat(s.strip()).isoformat()
    except ValueError: return None
def _git(args, path):
    try:
        r = subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(path)) if os.path.isfile(path) else path] + args,
                           capture_output=True, text=True, timeout=15)
        return r.returncode, r.stdout
    except Exception:
        return 1, ""
def _is_shallow(path):
    rc, out = _git(["rev-parse", "--is-shallow-repository"], path)
    return rc == 0 and out.strip() == "true"
def _git_first_add(path, fmt):
    rc, out = _git(["log", "--diff-filter=A", "--follow", f"--format={fmt}", "--date=short", "--", os.path.basename(path)], path)
    lines = [x.strip() for x in out.splitlines() if x.strip()]
    return lines[-1] if rc == 0 and lines else None
def _git_first_add_date(path):
    """narrative.json 이 git 에 처음 들어온 날(달력 검증). 미추적·git 없음 → None."""
    return parse_date(_git_first_add(path, "%ad") or "")
def joint_gate(nar, nar_path=None):
    """S0 착수일 판정 → {date, gated(True|False|None), basis, notes[], errors[]}.
    ① created(달력 검증, 틀리면 오류) ② git 최초 추가일(얕은 클론이면 안 믿음)
    둘 다 있으면 늦은 쪽(created 가 하루 넘게 앞서면 어긋남 경고 — 과거 날짜로 관문 우회 방지),
    created 만 있으면 그대로(경고), git 만 있으면 git(그 날짜 ≥ 발효일이면 created 없음 = 오류),
    둘 다 없으면 「착수일 못 잼」(gated=None: 막지 않되 큰 경고). asof 는 쓰지 않는다(갱신되는 값)."""
    notes, errors = [], []
    raw_c = nar.get("created") if isinstance(nar, dict) else None
    created = None
    if raw_c is not None:
        created = parse_date(raw_c)
        if created is None: errors.append(f"created {raw_c!r} 는 YYYY-MM-DD 달력 날짜가 아니다")
    git_d = None
    if nar_path:
        if _is_shallow(nar_path): notes.append("얕은 클론 — git 최초 추가일을 착수일 증거로 쓰지 않는다")
        else: git_d = _git_first_add_date(nar_path)
    if created and git_d:
        d = max(created, git_d)
        if (datetime.date.fromisoformat(git_d) - datetime.date.fromisoformat(created)).days > 1:
            notes.append(f"created {created} 가 git 최초 추가일 {git_d} 보다 앞선다 — 늦은 쪽({d})으로 판정")
        basis = "max(created, git 최초 추가일)"
    elif created:
        d, basis = created, "created(git 이력 없음 — 그대로 믿음)"
        notes.append(f"git 이력으로 created {created} 를 대조하지 못했다(미추적·얕은 클론·git 없음)")
    elif git_d:
        d, basis = git_d, "git 최초 추가일"
        if git_d >= JOINT_EFFECTIVE:
            errors.append(f"created 없음 — git 최초 추가일 {git_d} ≥ {JOINT_EFFECTIVE} 인 narrative.json 은 created(S0 착수일) 필수")
    else:
        notes.append("⚠⚠⚠ 착수일 못 잼(created 없음 · git 이력 없음/얕은 클론) — 이음매 관문을 적용하지 못했다, 관측만. created 를 적어라")
        return {"date": None, "gated": None, "basis": "착수일 못 잼", "notes": notes, "errors": errors}
    return {"date": d, "gated": d >= JOINT_EFFECTIVE, "basis": basis, "notes": notes, "errors": errors}
def joint_gate_date(nar, nar_path=None):
    """(날짜 문자열, 근거) — 옛 호출자 호환. 못 재면 ("", 근거) → 발효일보다 작게 비교된다(막지 않음)."""
    g = joint_gate(nar, nar_path)
    return (g["date"] or ""), g["basis"]
# ── 이음매 계약 — 내용 검사 도우미 ────────────────────────────────────────────────
def _resolve(ref, study_dir):
    if not isinstance(ref, str) or not ref.strip(): return None
    ref = ref.strip()
    cands = [ref] if os.path.isabs(ref) else [os.path.join(REPO, ref), os.path.join(study_dir, ref),
                                                os.path.join(os.path.dirname(os.path.normpath(study_dir)), ref)]
    if not os.path.isabs(ref):
        rc, top = _git(["rev-parse", "--show-toplevel"], study_dir)
        if rc == 0 and top.strip(): cands.append(os.path.join(top.strip(), ref))
    return next((c for c in cands if os.path.exists(c)), None)
def _ns(v, n=1):
    """공백 제거 뒤 n 자 이상, 그리고 서로 다른 글자 2개 이상(「xxxxx」·「-----」 같은 채움 거부)."""
    if not isinstance(v, str): return False
    s = v.strip()
    return len(s) >= n and len(set(s.replace(" ", ""))) >= min(2, n)
SOURCE_HINT = re.compile(r"(/|\.ya?ml|\.jsonl?|\.md\b|rcept|(?<!\d)\d{8,}(?!\d)|DART|공시|보고서|filings?|report|KRX|관세청|\bIR\b|\bi\d{2,}\b|MEM-\d+|TECH-\d+|§|컨센|Consensus)", re.I)
def _source_ok(v): return _ns(v, 4) and bool(SOURCE_HINT.search(v))
PATH_TOKEN = re.compile(r"[\w.*\-]+(?:/[\w.*\-]+)+")
def _path_tokens(s, study_dir, under=None):
    """문자열 안의 경로 토큰 중 실재하는 것(glob 허용). under 를 주면 그 접두 경로 아래 것만."""
    hits = []
    for tok in PATH_TOKEN.findall(str(s or "")):
        tok = tok.split("#")[0].rstrip(".")
        if under and not tok.startswith(under): continue
        if (glob.glob(os.path.join(REPO, tok)) if "*" in tok else _resolve(tok, study_dir)): hits.append(tok)
    return hits
def _text_list_ok(v, n):
    if isinstance(v, str): return _ns(v, n)
    return isinstance(v, list) and bool(v) and all(_ns(x, n) for x in v)
_PERIOD_PATS = [
    (re.compile(r"(?<![\dA-Za-z])(\d{4})[-./](\d{1,2})[-./](\d{1,2})(?!\d)"), lambda m: datetime.date(int(m[1]), int(m[2]), int(m[3]))),
    (re.compile(r"(?<![\dA-Za-z])(\d{4})[-./](\d{1,2})(?!\d)"), lambda m: _month_end(int(m[1]), int(m[2]))),
    (re.compile(r"\bFY\s?'?(\d{4}|\d{2})(?!\d)", re.I), lambda m: datetime.date(_y(m[1]), 12, 31)),
    (re.compile(r"\b([12])H\s?'?(\d{4}|\d{2})(?!\d)", re.I), lambda m: _month_end(_y(m[2]), 6 * int(m[1]))),
    (re.compile(r"\b([1-4])Q\s?'?(\d{4}|\d{2})(?!\d)", re.I), lambda m: _month_end(_y(m[2]), 3 * int(m[1]))),
    (re.compile(r"(?<![\dA-Za-z])((?:19|20)\d{2})(?!\d)"), lambda m: datetime.date(int(m[1]), 12, 31)),
]
def _y(s): return int(s) if len(s) == 4 else 2000 + int(s)
def _month_end(y, mo):
    if not 1 <= mo <= 12: raise ValueError(mo)
    nxt = datetime.date(y + (mo == 12), mo % 12 + 1, 1)
    return nxt - datetime.timedelta(days=1)
def period_end(s):
    """기간 문자열의 가장 늦은 끝 날짜(datetime.date) — 2018 · 2018-10 · 2026-06-08 · FY18 · FY2018 ·
    1H26 · 2H2026 · 3Q25 · 2024-2026 · 「2018 / 2026-06」. 못 읽으면 None."""
    s = str(s or "")
    ends = []
    for pat, fn in _PERIOD_PATS:
        def sub(m):
            try: ends.append(fn(m))
            except ValueError: pass
            return " " * len(m.group(0))
        s = pat.sub(sub, s)
    return max(ends) if ends else None
STALE_DAYS = 3 * 365.25   # 「3년 초과」(문서와 같은 경계: 정확히 3년은 낡음 아님)
def is_stale(period, ref_date):
    e = period_end(period)
    return bool(e and ref_date and (ref_date - e).days > STALE_DAYS)
def ref_date_of(nar):
    a = str((nar or {}).get("asof") or "")[:10]
    p = parse_date(a)
    return datetime.date.fromisoformat(p) if p else datetime.date.today()
_BOX_IDS = None
def known_box_ids():
    """core/valuechain/*.yaml 의 `id: <box>` 전수(문자열 스캔 — yaml 파서 없이도 돈다)."""
    global _BOX_IDS
    if _BOX_IDS is None:
        _BOX_IDS = set()
        vdir = os.path.join(REPO, "core", "valuechain")
        for fn in (os.listdir(vdir) if os.path.isdir(vdir) else []):
            if fn.endswith((".yaml", ".yml")):
                try: _BOX_IDS |= set(re.findall(r"\bid:\s*['\"]?([a-z0-9_]+(?:\.[a-z0-9_]+)+)", open(os.path.join(vdir, fn), encoding="utf-8").read()))
                except OSError: pass
    return _BOX_IDS
INBOX_DIR = os.path.join(REPO, "core", "valuechain", "_inbox")
def proposed_box_ids():
    """core/valuechain/_inbox/*.jsonl 의 valuechain/chain-proposal@1 행이 제안한 box_id."""
    out = set()
    for p in glob.glob(os.path.join(INBOX_DIR, "*.jsonl")):
        try:
            for line in open(p, encoding="utf-8"):
                try: r = json.loads(line)
                except ValueError: continue
                if isinstance(r, dict) and str(r.get("schema", "")).endswith("chain-proposal@1") and isinstance(r.get("box_id"), str):
                    out.add(r["box_id"])
        except OSError:
            pass
    return out
def narrative_ids(nar):
    ids = set()
    for k in ("market_narratives", "our_hypotheses"):
        for x in (nar.get(k) or []) if isinstance(nar.get(k), list) else []:
            if isinstance(x, dict) and isinstance(x.get("id"), str): ids.add(x["id"])
    return ids
PROMPT_FORBIDDEN = [
    (re.compile(r"(?<![A-Za-z])(MN|H)\d+\b"), "서사·가설 id"),
    (re.compile(r"market-intel|core/|tools/|modeling/|orchestration/|\.claude|/home/|~/", re.I), "레포 경로"),
    (re.compile(r"\.(json|jsonl|md|ya?ml|py)\b", re.I), "파일 이름"),
    (re.compile(r"가설|hypothes|narrative_id|우리\s*(판|뷰|가설)|셀사이드|sell-?side|컨센서스|consensus|목표주가|target price", re.I), "배경(가설·셀사이드·컨센)"),
]
PROMPT_MAX_CHARS = 600
def prompt_background(text, ticker=None):
    """무하네스 프롬프트에 배경이 섞였는지(값싼 금칙 패턴) → 문제 목록."""
    out = [f"{why}: {m.group(0)!r}" for pat, why in PROMPT_FORBIDDEN for m in [pat.search(text)] if m]
    if len(text) > PROMPT_MAX_CHARS: out.append(f"길이 {len(text)} > {PROMPT_MAX_CHARS}자 — 회사명·티커·기준일만")
    if ticker and str(ticker) not in text: out.append(f"티커 {ticker} 가 없다")
    return out
def _inside(path, root):
    try: return os.path.commonpath([os.path.realpath(path), os.path.realpath(root)]) == os.path.realpath(root)
    except ValueError: return False
def _file_time(p):
    """(epoch, 근거) — git 에 있으면 최초 추가 커밋 시각, 없으면 mtime."""
    ct = _git_first_add(p, "%ct")
    if ct and ct.isdigit(): return int(ct), "git"
    try: return os.path.getmtime(p), "mtime"
    except OSError: return None, "없음"
def _blind_item_issues(bc):
    out = []
    for j, it in enumerate(bc.get("only_blind") if isinstance(bc.get("only_blind"), list) else []):
        if not isinstance(it, dict): out.append(f"blind_contrast.only_blind[{j}]: 객체 아님"); continue
        if it.get("disposition") not in ("adopted", "rejected", "needs_check"):
            out.append(f"blind_contrast.only_blind[{j}]: disposition 없음/어휘 밖 {it.get('disposition')!r} — 채택·기각·확인필요 중 하나")
        if not _ns(it.get("why"), 5): out.append(f"blind_contrast.only_blind[{j}]: why 비었음(공백 제거 뒤 5자 미만)")
    return out
def _cycle_issues(cc, nar, study_dir):
    out = []
    if not isinstance(cc, dict): return ["cycle_context: 객체가 아니다"]
    s = cc.get("searched")
    items = cc.get("items")
    if not isinstance(s, dict):
        out.append("cycle_context.searched 없음/객체 아님 — 검색 키(티커·박스·훑은 경로·n_found)가 없으면 「안 찾아봤다」")
    else:
        tk = s.get("tickers")
        if not (isinstance(tk, list) and tk and all(_ns(t, 1) for t in tk)): out.append("cycle_context.searched.tickers 비었음")
        elif nar.get("ticker") and str(nar["ticker"]) not in [str(t).strip() for t in tk]: out.append(f"cycle_context.searched.tickers 에 이 종목 {nar['ticker']} 이 없다")
        if not isinstance(s.get("boxes"), list) or not all(isinstance(b, str) for b in s.get("boxes")): out.append("cycle_context.searched.boxes 가 문자열 배열이 아니다")
        srcs = s.get("sources")
        if not (isinstance(srcs, list) and srcs):
            out.append("cycle_context.searched.sources 비었음")
        else:
            for j, x in enumerate(srcs):
                if not _ns(x, 3) or not _path_tokens(x, study_dir): out.append(f"cycle_context.searched.sources[{j}] {x!r}: 실재하는 경로가 없다")
            if not any("narratives" in str(x) for x in srcs): out.append("cycle_context.searched.sources 에 market-intel/narratives(편·node_narratives.json) 가 없다")
        n = s.get("n_found")
        if not isinstance(n, int) or isinstance(n, bool) or n < 0: out.append(f"cycle_context.searched.n_found 정수 아님 {n!r}")
        elif isinstance(items, list) and n != len(items): out.append(f"cycle_context: searched.n_found={n} 인데 items {len(items)}개 — 찾은 편마다 stance 가 있어야 한다")
    if not isinstance(items, list):
        out.append("cycle_context.items 배열 아님"); return out
    ids, seen = narrative_ids(nar), set()
    for j, it in enumerate(items):
        loc = f"cycle_context.items[{j}]"
        if not isinstance(it, dict): out.append(f"{loc}: 객체 아님"); continue
        nid = it.get("narrative_id")
        if not _ns(nid, 2): out.append(f"{loc}: narrative_id 비었음"); nid = None
        elif nid in seen: out.append(f"{loc}: narrative_id {nid} 중복")
        seen.add(nid)
        p = _resolve(it.get("ref"), study_dir)
        if not p or "narratives" not in p.replace(os.sep, "/") or not os.path.isfile(p):
            out.append(f"{loc}: ref {it.get('ref')!r} 가 market-intel/narratives 의 실재 편 파일이 아니다")
        elif nid:
            try:
                if nid not in open(p, encoding="utf-8").read(): out.append(f"{loc}: ref 파일에 narrative_id {nid!r} 가 안 나온다")
            except OSError: out.append(f"{loc}: ref 못 읽음")
        if not period_end(it.get("asof")): out.append(f"{loc}: asof {it.get('asof')!r} 못 읽음")
        st = it.get("stance")
        if st not in ("adopt", "reject", "irrelevant"): out.append(f"{loc}: stance 어휘 밖 {st!r}")
        if not _ns(it.get("why"), 10): out.append(f"{loc}: why 비었음(공백 제거 뒤 10자 미만)")
        if st == "adopt":
            mt = it.get("maps_to")
            if not (isinstance(mt, list) and mt): out.append(f"{loc}: adopt 인데 maps_to 없음 — 이 narrative 의 MN/H id 로 연결")
            else:
                bad = [m for m in mt if m not in ids]
                if bad: out.append(f"{loc}: maps_to {bad} 가 이 narrative.json 의 서사·가설 id({sorted(ids)})에 없다")
    return out
def _blind_issues(bc, nar, study_dir):
    out, notes = [], []
    if not isinstance(bc, dict): return ["blind_contrast: 객체가 아니다"], notes
    st = bc.get("status")
    if isinstance(st, str) and st.strip().startswith("not_run"):
        return [f"blind_contrast: 실호출 안 됨(status={st!r})"], notes
    for k in ("backend", "model"):
        if not _ns(bc.get(k), 2): out.append(f"blind_contrast.{k} 비었음")
    if bc.get("made_before_s0_synthesis") is not True: out.append("blind_contrast.made_before_s0_synthesis 가 true 가 아니다")
    pack = os.path.dirname(os.path.normpath(study_dir))
    outp = _resolve(bc.get("output_ref"), study_dir)
    if not outp or not os.path.isfile(outp) or not _inside(outp, study_dir) or not re.match(r"^S0_blind_[\w.-]+\.(md|txt|json)$", os.path.basename(outp)):
        out.append(f"blind_contrast.output_ref {bc.get('output_ref')!r}: 팩 study/ 안의 S0_blind_*.md|txt|json 파일이어야 한다"); outp = None
    elif os.path.getsize(outp) == 0:
        out.append("blind_contrast.output_ref: 빈 파일"); outp = None
    pp = _resolve(bc.get("prompt_ref"), study_dir)
    sha = str(bc.get("prompt_sha") or "").strip().lower()
    if not pp or not os.path.isfile(pp) or not _inside(pp, pack):
        out.append(f"blind_contrast.prompt_ref {bc.get('prompt_ref')!r}: 팩 안의 프롬프트 파일이어야 한다(prompt_sha 대조용)"); pp = None
    else:
        raw = open(pp, "rb").read()
        real = hashlib.sha256(raw).hexdigest()
        if not re.fullmatch(r"[0-9a-f]{12,64}", sha) or not real.startswith(sha):
            out.append(f"blind_contrast.prompt_sha {sha!r} ≠ 프롬프트 파일 sha256 {real[:12]}")
        for why in prompt_background(raw.decode("utf-8", "replace"), nar.get("ticker")):
            out.append(f"blind_contrast 프롬프트에 배경이 섞였다 — {why}")
    arrs = [bc.get(k) for k in ("only_blind", "only_ours", "both")]
    if not all(isinstance(a, list) for a in arrs):
        out.append("blind_contrast: only_blind·only_ours·both 는 배열")
    else:
        if not any(arrs): out.append("blind_contrast: 차이표 세 배열이 전부 비었다 — 출력을 주장 단위로 나눠 대조하지 않았다")
        for k, a in zip(("only_blind", "only_ours", "both"), arrs):
            for j, it in enumerate(a):
                if not (isinstance(it, dict) and _ns(it.get("claim"), 5)): out.append(f"blind_contrast.{k}[{j}]: claim 비었음")
        out += _blind_item_issues(bc)
    if bc.get("audit_ref") is not None and not _resolve(bc.get("audit_ref"), study_dir):
        notes.append(f"blind_contrast.audit_ref {bc.get('audit_ref')!r} 못 찾음(외부 호출 감사 기록은 무시 경로라 없을 수 있다)")
    # 순서: 프롬프트 ≤ 출력 ≤ S0 합성(narrative.json 최초 커밋)
    if pp and outp:
        tp, kp = _file_time(pp); to, ko = _file_time(outp)
        if tp is not None and to is not None and tp > to + 1: out.append(f"blind 출력({ko})이 프롬프트({kp})보다 먼저다")
    if outp:
        nar_p = os.path.join(study_dir, "narrative.json")
        tn = _git_first_add(nar_p, "%ct")
        to_git = _git_first_add(outp, "%ct")
        if not (tn and tn.isdigit()):
            notes.append("blind 순서 못 잼 — narrative.json 이 git 에 없어 S0 합성 시점을 모른다")
        elif not (to_git and to_git.isdigit()):
            out.append("blind 출력이 git 에 없는데 narrative.json 은 이미 커밋됐다 — S0 합성 뒤에 만든 출력")
        elif int(to_git) > int(tn):
            out.append("blind 출력의 최초 커밋이 narrative.json 최초 커밋보다 늦다 — S0 합성 전에 만들어야 한다")
    return out, notes
_CP_TEXT = ("what_company_does", "who_pays_whom", "value_capture", "q_asp_to_pnl")
def _norm_name(s): return re.sub(r"\s+", " ", str(s or "")).strip().casefold()
def _chain_issues(cp, nar, study_dir):
    out = []
    if not isinstance(cp, dict): return ["chain_position: 객체가 아니다"]
    boxes = cp.get("boxes")
    if not (isinstance(boxes, list) and boxes): out.append("chain_position.boxes 비었음")
    else:
        known, proposed = known_box_ids(), proposed_box_ids()
        for b in boxes:
            if not (isinstance(b, str) and re.fullmatch(r"[a-z0-9_]+(\.[a-z0-9_]+)+", b)): out.append(f"chain_position.boxes {b!r}: 박스 id 형식 아님"); continue
            if b not in known and b not in proposed:
                out.append(f"chain_position: 박스 {b!r} 가 core/valuechain/*.yaml 에도 _inbox chain-proposal@1 에도 없다")
    ref = ref_date_of(nar)
    stale_fields = " ".join(str(s.get("field")) for s in cp.get("stale_facts") or [] if isinstance(s, dict)) if isinstance(cp.get("stale_facts"), list) else ""
    for side in ("upstream", "downstream"):
        lst = cp.get(side)
        if not (isinstance(lst, list) and lst): out.append(f"chain_position.{side} 비었음"); continue
        names = []
        for j, p in enumerate(lst):
            loc = f"chain_position.{side}[{j}]"
            if not isinstance(p, dict): out.append(f"{loc}: 객체 아님"); continue
            for k, n in (("name", 2), ("what", 2), ("share_or_dependence", 2)):
                if not _ns(p.get(k), n): out.append(f"{loc}.{k} 비었음(공백 제거 뒤)")
            if not _source_ok(p.get("source")): out.append(f"{loc}.source {p.get('source')!r}: 원천으로 읽히지 않는다(경로·rcept·공시·보고서 등)")
            if not period_end(p.get("asof")): out.append(f"{loc}.asof {p.get('asof')!r}: 기간을 못 읽는다(필수 — 낡음 판정용)")
            elif is_stale(p.get("asof"), ref) and str(p.get("name")) not in stale_fields:
                out.append(f"{loc} {p.get('name')!r}: asof {p.get('asof')} 는 3년 초과 — stale_facts 에 표시")
            nm = _norm_name(p.get("name"))
            if nm and nm in names: out.append(f"{loc}: 이름 {p.get('name')!r} 중복")
            names.append(nm)
    for k in _CP_TEXT:
        if not _ns(cp.get(k), 20): out.append(f"chain_position.{k} 비었음(공백 제거 뒤 20자 미만)")
    con = cp.get("concentration")
    if not isinstance(con, dict): out.append("chain_position.concentration 객체 아님")
    else:
        for k in ("customers", "suppliers"):
            if not _ns(con.get(k), 5): out.append(f"chain_position.concentration.{k} 비었음")
    for k in ("bottlenecks", "substitutes"):
        if not _text_list_ok(cp.get(k), 10): out.append(f"chain_position.{k}: 10자 이상 문자열 또는 그런 문자열들의 배열이어야 한다")
    sf = cp.get("stale_facts")
    if not isinstance(sf, list): out.append("chain_position.stale_facts 배열 아님")
    else:
        for j, s in enumerate(sf):
            if not (isinstance(s, dict) and _ns(s.get("field"), 3) and period_end(s.get("asof"))): out.append(f"chain_position.stale_facts[{j}]: field·asof 필요")
    srcs = cp.get("sources")
    if not (isinstance(srcs, list) and srcs and all(_ns(x, 3) for x in srcs)): out.append("chain_position.sources 비었음")
    elif not any(_path_tokens(x, study_dir, under="core/valuechain/") for x in srcs):
        out.append("chain_position.sources 에 실재하는 core/valuechain/*.yaml 경로가 없다 — 박스·간선의 정본을 적는다")
    return out
def joint_issues(nar, study_dir, schema):
    """(issues, notes) — issues 는 날짜 관문에 따라 오류/관측, notes 는 늘 관측.
    어떤 입력에도 예외를 밖으로 내지 않는다(옛 팩의 자료형 불량이 rc 1 로 새지 않게)."""
    out, notes = [], []
    try:
        if not _have_jsonschema():
            out.append("검사 불능: jsonschema 가 없다 — 중첩 스키마 제약을 못 본다(pip install jsonschema)")
        defs = (schema or {}).get("$defs", {})
        for k in JOINT_KEYS:
            blk = nar.get(k)
            if blk is None:
                out.append(f"{k} 없음 — " + {"cycle_context": "사이클 내러티브를 찾아봤다는 기록이 없다(n_found 0 + 검색 키도 유효, 블록 없음은 무효)",
                                              "blind_contrast": "무하네스 대조가 없다 — S0 합성 전에 회사명·티커·기준일만으로 부른다",
                                              "chain_position": "밸류체인 위치가 없다 — node.json chain_refs → core/valuechain/*.yaml 박스·간선에서 채운다"}[k])
                continue
            if k in defs and _have_jsonschema():
                errs = []
                vblk = {kk: vv for kk, vv in blk.items() if kk != "stages"} if (k == "blind_contrast" and isinstance(blk, dict)) else blk  # stages 는 무하네스 짝 축(관측 기본)에서 따로
                validate(vblk, {"$schema": schema.get("$schema"), "$defs": defs, **defs[k]}, k, errs)
                out.extend(errs)
            if k == "cycle_context": out += _cycle_issues(blk, nar, study_dir)
            elif k == "blind_contrast":
                o, n = _blind_issues(blk, nar, study_dir); out += o; notes += n
            else: out += _chain_issues(blk, nar, study_dir)
    except Exception as e:  # 검사기 자체 결함도 관문 규칙대로(신규 = 오류, 옛 팩 = 관측)
        out.append(f"이음매 검사 중 예외 {type(e).__name__}: {e}")
    return out, notes
# ── 무하네스 짝 stages(드라이런이 드러낸 구멍) ──────────────────────────
# blind_contrast.stages[] = 판단 스테이지별 짝(S0b 드라이버·S2_consensus 컨센·S1·S3, S0 은 상위 블록이 정본).
# ① price_drivers 가 있으면 S0b 짝 필수 ② 팩에 consensus_check.json 이 있으면 S2_consensus 짝 필수
# ③ 짝마다 prompt_sha = 프롬프트 파일 실제 해시 · output_ref 실재(<stage>_blind_*) · only_blind 전부 disposition
# · web_used 면 「재료만」 깨짐. 관측 기본(경고), --strict-blind 또는 S0 착수일 ≥ BLIND_STAGE_EFFECTIVE 면 rc 1.
BLIND_STAGE_EFFECTIVE = "2026-11-01"
BLIND_STAGES = ("S0", "S0b", "S2_consensus", "S1", "S3")
STAGE_SYNTH = {"S0b": "narrative.json", "S2_consensus": "consensus_check.json"}  # 「합성 전」 대조 대상(최초 커밋)
STAGE_PROMPT_FORBIDDEN = PROMPT_FORBIDDEN[:2]  # 재료 표는 컨센·숫자를 담으므로 서사 id·레포 경로만 금칙
def _stage_issues(st, i, nar, study_dir):
    tag = f"blind_contrast.stages[{i}]"
    if not isinstance(st, dict): return [f"{tag}: 객체 아님"]
    sg = st.get("stage"); tag = f"{tag}({sg})"
    if sg not in BLIND_STAGES: return [f"{tag}: stage 는 {'|'.join(BLIND_STAGES)} 중 하나"]
    s = st.get("status")
    if isinstance(s, str) and s.strip().startswith("not_run"): return [f"{tag}: 실호출 안 됨(status={s!r})"]
    out = []
    for k in ("backend", "model"):
        if not _ns(st.get(k), 2): out.append(f"{tag}.{k} 비었음")
    if st.get("made_before_synthesis") is not True: out.append(f"{tag}.made_before_synthesis 가 true 가 아니다")
    if st.get("web_used") is True:
        out.append(f"{tag}: web_used=true — 「재료만」 조건 깨짐(표 밖 원천 사용), web_off 로 재호출 필요")
    pack = os.path.dirname(os.path.normpath(study_dir))
    outp = _resolve(st.get("output_ref"), study_dir)
    if not outp or not os.path.isfile(outp) or not _inside(outp, study_dir) or not re.match(rf"^{re.escape(sg)}_blind_[\w.-]+\.(md|txt|json)$", os.path.basename(outp)):
        out.append(f"{tag}.output_ref {st.get('output_ref')!r}: 팩 study 안의 {sg}_blind_*.md|txt|json 파일이어야 한다"); outp = None
    elif os.path.getsize(outp) == 0:
        out.append(f"{tag}.output_ref: 빈 파일"); outp = None
    pp = _resolve(st.get("prompt_ref"), study_dir)
    sha = str(st.get("prompt_sha") or "").strip().lower()
    if not pp or not os.path.isfile(pp) or not _inside(pp, pack):
        out.append(f"{tag}.prompt_ref {st.get('prompt_ref')!r}: 팩 안의 프롬프트 파일이어야 한다(prompt_sha 대조용)"); pp = None
    else:
        raw = open(pp, "rb").read(); real = hashlib.sha256(raw).hexdigest()
        if not re.fullmatch(r"[0-9a-f]{12,64}", sha) or not real.startswith(sha):
            out.append(f"{tag}.prompt_sha {sha!r} ≠ 프롬프트 파일 sha256 {real[:12]}")
        txt = raw.decode("utf-8", "replace")
        for pat, why in STAGE_PROMPT_FORBIDDEN:
            m = pat.search(txt)
            if m: out.append(f"{tag} 프롬프트에 배경이 섞였다 — {why}: {m.group(0)!r}")
    arrs = [st.get(k) for k in ("only_blind", "only_ours", "both")]
    if not all(isinstance(a, list) for a in arrs):
        out.append(f"{tag}: only_blind·only_ours·both 는 배열")
    else:
        if not any(arrs): out.append(f"{tag}: 차이표 세 배열이 전부 비었다")
        for k, a in zip(("only_blind", "only_ours", "both"), arrs):
            for j, it in enumerate(a):
                if not (isinstance(it, dict) and _ns(it.get("claim"), 5)): out.append(f"{tag}.{k}[{j}]: claim 비었음")
        out += [x.replace("blind_contrast.", f"{tag}.", 1) for x in _blind_item_issues(st)]
    if pp and outp:
        tp, kp = _file_time(pp); to, ko = _file_time(outp)
        if tp is not None and to is not None and tp > to + 1: out.append(f"{tag}: 출력({ko})이 프롬프트({kp})보다 먼저다")
    syn = STAGE_SYNTH.get(sg)
    if outp and syn:
        tn = _git_first_add(os.path.join(study_dir, syn), "%ct"); tg = _git_first_add(outp, "%ct")
        if tn and tn.isdigit():
            if not (tg and tg.isdigit()): out.append(f"{tag}: 출력이 git 에 없는데 {syn} 은 이미 커밋됐다 — 합성 뒤에 만든 짝")
            elif int(tg) > int(tn): out.append(f"{tag}: 출력 최초 커밋이 {syn} 최초 커밋보다 늦다 — 합성 전에 만들어야 한다")
    return out
def blind_stage_issues(nar, study_dir, schema=None):
    """→ issues(관측/관문은 호출부가 정한다). 짝이 필요한 스테이지가 없거나 짝이 불량이면 문자열."""
    out = []
    try:
        bc = nar.get("blind_contrast") if isinstance(nar, dict) else None
        stages = bc.get("stages") if isinstance(bc, dict) else None
        if stages is not None and not isinstance(stages, list): return ["blind_contrast.stages: 배열이 아니다"]
        stages = stages or []
        defs = (schema or {}).get("$defs", {})
        if stages and "blind_stage" in defs and _have_jsonschema():
            errs = []
            validate(stages, {"$schema": schema.get("$schema"), "$defs": defs, "type": "array", "items": {"$ref": "#/$defs/blind_stage"}}, "blind_contrast.stages", errs)
            out += errs
        have = {s.get("stage") for s in stages if isinstance(s, dict)}
        if nar.get("price_drivers") is not None and "S0b" not in have:
            out.append("S0b 짝 없음 — price_drivers 가 있는데 blind_contrast.stages 에 S0b(가격·공시 표만 준 무하네스 판) 가 없다")
        if os.path.isfile(os.path.join(study_dir, "consensus_check.json")) and "S2_consensus" not in have:
            out.append("S2_consensus 짝 없음 — consensus_check.json 이 있는데 blind_contrast.stages 에 S2_consensus(컨센 표만 준 무하네스 판) 가 없다")
        for i, st in enumerate(stages): out += _stage_issues(st, i, nar, study_dir)
    except Exception as e:
        out.append(f"무하네스 짝 검사 중 예외 {type(e).__name__}: {e}")
    return out
def _blind_stage_cases():
    """미끼 3(짝 없음·해시 불일치·disposition 빈칸) + 정상 1 + S2 짝 없음 + 관문(rc) → 실패 문자열 목록."""
    import tempfile, io, contextlib
    fails = []
    PROMPT = "테스트기업(KRX:TEST01). 아래 표만 보고 답하라: 무엇이 주가를 움직였나.\n| 주 | 종가 |\n|---|---|\n| 2026-10-02 | 1000 |\n"
    def mk(tmp, mutate=None, consensus=False, created="2026-10-20"):
        sd = os.path.join(tmp, "pack", "study"); os.makedirs(sd)
        open(os.path.join(sd, "S0b_blind_prompt.txt"), "w", encoding="utf-8").write(PROMPT)
        open(os.path.join(sd, "S0b_blind_external.md"), "w", encoding="utf-8").write("blind S0b output\n")
        if consensus: open(os.path.join(sd, "consensus_check.json"), "w", encoding="utf-8").write("{}")
        st = {"stage": "S0b", "backend": "external", "model": "<model>", "prompt_ref": "S0b_blind_prompt.txt",
              "prompt_sha": hashlib.sha256(PROMPT.encode("utf-8")).hexdigest()[:12], "output_ref": "S0b_blind_external.md",
              "made_before_synthesis": True,
              "only_blind": [{"claim": "시장 요인을 별도 행으로 분리", "disposition": "needs_check", "why": "도구 표가 바스켓에 접는다"}],
              "only_ours": [{"claim": "셀사이드 발간일 동행 6.5%"}], "both": [{"claim": "1위는 바스켓 동행"}]}
        nar = {"created": created, "price_drivers": [{"driver": "바스켓"}], "blind_contrast": {"stages": [st]}}
        if mutate: mutate(nar)
        return nar, sd
    def exp(name, want, must=None, **kw):
        with tempfile.TemporaryDirectory() as tmp:
            nar, sd = mk(tmp, **kw); iss = blind_stage_issues(nar, sd, load(os.path.join(HERE, "narrative.schema.json")))
        if bool(iss) != want: fails.append(f"[무하네스 짝] {name}: 문제 기대 {want}, 실제 {iss}")
        if must and not any(must in x for x in iss): fails.append(f"[무하네스 짝] {name}: '{must}' 없음 {iss}")
    st0 = lambda n: n["blind_contrast"]["stages"][0]
    exp("정상 S0b 짝", False)
    exp("미끼 짝 없음", True, "S0b 짝 없음", mutate=lambda n: n["blind_contrast"].__setitem__("stages", []))
    exp("미끼 해시 불일치", True, "prompt_sha", mutate=lambda n: st0(n).__setitem__("prompt_sha", "0123456789ab"))
    exp("미끼 disposition 빈칸", True, "disposition", mutate=lambda n: st0(n)["only_blind"][0].__setitem__("disposition", ""))
    exp("S2 컨센 짝 없음", True, "S2_consensus 짝 없음", consensus=True)
    exp("web_used = 재료만 깨짐", True, "web_used", mutate=lambda n: st0(n).__setitem__("web_used", True))
    exp("output_ref 이름이 S0_blind(스테이지 불일치)", True, "S0b_blind_", mutate=lambda n: st0(n).__setitem__("output_ref", "S0_blind_external.md"))
    exp("짝 필요 없음(price_drivers·컨센 없음) = 침묵", False, mutate=lambda n: (n.pop("price_drivers"), n.pop("blind_contrast")))
    # 관문: 관측 기본 rc 0, --strict-blind rc 1, 착수일 ≥ 발효일 rc 1(main 경유, 출력은 삼킨다)
    for name, created, strict, want in [("관측 기본", "2026-10-20", False, 0), ("--strict-blind", "2026-10-20", True, 1), ("11-01 이후 착수 기본 rc 1", "2026-11-02", False, 1)]:
        with tempfile.TemporaryDirectory() as tmp:
            nar, sd = mk(tmp, mutate=lambda n: n["blind_contrast"].__setitem__("stages", []), created=created)
            got = blind_gate_rc(nar, sd, strict)
        if got != want: fails.append(f"[무하네스 짝 관문] {name}: rc 기대 {want}, 실제 {got}")
    return fails
def blind_gate_rc(nar, study_dir, strict_blind=False):
    """짝 문제가 오류(rc 1)로 가는지만 판정 — main 과 같은 규칙(자가시험·호출부 공용)."""
    iss = blind_stage_issues(nar, study_dir, load(os.path.join(HERE, "narrative.schema.json")))
    return 1 if iss and blind_strict(nar, study_dir, strict_blind)[0] else 0
def blind_strict(nar, study_dir, strict_blind=False):
    g = joint_gate(nar, os.path.join(study_dir, "narrative.json"))
    late = bool(g["date"]) and g["date"] >= BLIND_STAGE_EFFECTIVE
    return (strict_blind or late), (f"--strict-blind" if strict_blind else f"S0 {g['date'] or '못 잼'} {'≥' if late else '<'} {BLIND_STAGE_EFFECTIVE}")
def selftest_blind_stages():
    g = globals(); fails = _blind_stage_cases()
    for name, patch in [("짝 필수 판정 제거", {"STAGE_SYNTH": {}, "blind_stage_issues": lambda nar, sd, schema=None: [x for st in ((nar.get("blind_contrast") or {}).get("stages") or []) for x in _stage_issues(st, 0, nar, sd)]}),
                        ("disposition 검사 제거(스키마 층 포함)", {"_blind_item_issues": lambda bc: [], "_have_jsonschema": lambda: False}),
                        ("관문 날짜 2099", {"BLIND_STAGE_EFFECTIVE": "2099-01-01"})]:
        saved = {k: g[k] for k in patch}
        try:
            g.update(patch); n = len(_blind_stage_cases())
        finally:
            g.update(saved)
        if n == 0: fails.append(f"[무하네스 짝 변이] {name}: 검사를 지웠는데 미끼가 안 깨졌다")
    return fails
# ── 테제-모델 정합 — 별도 블록 ──
def thesis_model_issues(nar, model_dir):
    """model_links 가 있으면 check_thesis_model 로 판정 → (위반 문자열 목록, 관측 문자열 목록).
    model_dir 없음 = 관측 한 줄(정합 미검사), 링크 0 = 아무것도 안 함."""
    n = sum(len(h.get("model_links") or []) for h in nar.get("our_hypotheses", []))
    if n == 0: return [], []
    if not model_dir: return [], [f"model_links {n}건 있으나 --model-dir 없음 — 테제-모델 정합 미검사"]
    sys.path.insert(0, HERE)
    import check_thesis_model as ctm
    model, src = ctm.load_model(model_dir)
    if model is None: return [f"[테제-모델] 모델 산출 못 찾음(못 잼 = 위반): {src}"], []
    rows, bad, _ = ctm.check(nar, model)
    return ([f"[테제-모델] {r['hyp']} {r['driver']} 기대 {r['want']} · {r['case']}→{r['world']} {r['horizon']} · {r['path']} · {r['verdict']} {r['why']}" for r in bad],
            [f"[테제-모델] 판정 {len(rows)}행 · 위반 {len(bad)} (모델 = {src})"])
def selftest_thesis():
    """정합 픽스처 → 위반 0, OPM 역전 픽스처 → 위반 ≥1, 모델 dir 없음 → 관측만."""
    fx = os.path.join(HERE, "fixtures")
    nar = load(os.path.join(fx, "thesis_model_pass", "narrative.json"))
    if nar is None: return ["테제-모델 픽스처 없음"]
    out = []
    if thesis_model_issues(nar, os.path.join(fx, "thesis_model_pass", "model"))[0]: out.append("테제-모델 정합 픽스처가 위반으로 나옴")
    if not thesis_model_issues(nar, os.path.join(fx, "thesis_model_opm_reversed", "model"))[0]: out.append("테제-모델 OPM 역전 픽스처가 통과함")
    e, w = thesis_model_issues(nar, None)
    if e or not w: out.append("테제-모델 dir 없음이 관측 한 줄이 아님")
    return out
def main(d, strict_review_check=False, model_dir=None, strict_thesis=False, strict_blind=False):
    errs, warns = [], []
    residue = dualization_residue(d)
    if residue:
        warns.append(f"이원화 잔재: {os.path.basename(os.path.dirname(os.path.normpath(d)))}/sources/*.jsonl {len(residue)}개 남음({', '.join(residue)}) — market-intel/nodes/<ticker>/sources/ 가 정본(과제 21), sources/POINTER.json 으로 교체해야 함")
    nar = load(os.path.join(d, "narrative.json"))
    if nar is None: errs.append("narrative.json 없음 — S0 없이 S1 을 시작하지 않는다")
    else:
        schema = load(os.path.join(HERE, "narrative.schema.json"))
        # 이음매 3블록은 날짜 관문으로 따로 판정한다 — 본 검증에서 빼야 옛 팩의 불량 블록이 rc 1 로 새지 않는다
        validate({k: v for k, v in nar.items() if k not in JOINT_KEYS}, schema, "narrative.json", errs)
        gate = joint_gate(nar, os.path.join(d, "narrative.json"))
        errs.extend(f"narrative.json [이음매 착수일] {e}" for e in gate["errors"])
        issues, notes = joint_issues(nar, d, schema)
        for n in gate["notes"] + notes: warns.append(f"narrative.json [이음매 관측] {n}")
        tag = f"S0 {gate['date'] or '못 잼'}({gate['basis']})"
        for msg in issues:
            if gate["gated"] is True: errs.append(f"narrative.json [이음매 관문 · {tag} ≥ {JOINT_EFFECTIVE}] {msg}")
            else: warns.append(f"narrative.json [이음매 관측 · {tag}{(' < ' + JOINT_EFFECTIVE) if gate['gated'] is False else ''}] {msg}")
        ids = {h["id"] for h in nar.get("our_hypotheses", [])}
        mets = {h.get("metric") for h in nar.get("our_hypotheses", [])}
        if not nar.get("approved_by"): warns.append("narrative.json: approved_by 비어 있음 — 본체 승인 전(S1 착수 금지)")
        for h in nar.get("our_hypotheses", []):
            for dep in h.get("depends_on", []):
                if not re.match(r"^(MN|H)\d+$", dep): errs.append(f"H {h['id']}: depends_on `{dep}` 형식 아님")
        issue = review_check_issue(nar)
        if issue:
            msg = f"narrative.json: {issue}"
            (errs if strict_review_check else warns).append(msg)
        c5_issue = c5_exception_missing_reason(nar)
        if c5_issue: warns.append(f"narrative.json: {c5_issue}")
        pd_errs, pd_warns = price_driver_issues(nar)  # 선택 칸 price_drivers·business_nature — 있을 때만(2026-10-20)
        errs.extend(f"narrative.json: {e}" for e in pd_errs); warns.extend(f"narrative.json: {w}" for w in pd_warns)
        b_iss = blind_stage_issues(nar, d, schema)  # 무하네스 짝 S0b·S2_consensus — 관측 기본, --strict-blind·11-01 이후 착수는 rc 1
        if b_iss:
            b_strict, b_why = blind_strict(nar, d, strict_blind)
            (errs if b_strict else warns).extend(f"narrative.json [무하네스 짝 {'관문' if b_strict else '관측'} · {b_why}] {x}" for x in b_iss)
        t_bad, t_notes = thesis_model_issues(nar, model_dir)  # 관측 기본, --strict-thesis 로 rc 1
        warns.extend(t_notes); (errs if strict_thesis else warns).extend(t_bad)
    fin = load(os.path.join(d, "findings.json"))
    if fin is not None:
        seen = set()
        for r in fin if isinstance(fin, list) else fin.get("findings", []):
            if r.get("verdict") not in ("supported", "refuted", "unknown"): errs.append(f"findings {r.get('hyp_id')}: verdict 어휘 밖 {r.get('verdict')!r}")
            if r.get("verdict") == "unknown" and not r.get("what_is_missing"): errs.append(f"findings {r.get('hyp_id')}: unknown 인데 what_is_missing 없음")
            if not r.get("what_flips_it"): errs.append(f"findings {r.get('hyp_id')}: what_flips_it 없음")
            seen.add(r.get("hyp_id"))
        if nar is not None:
            for h in ids - seen: warns.append(f"가설 {h} 미검증(findings 없음)")
    tr = load(os.path.join(d, "tracking_register.json"))
    if tr is not None:
        validate(tr, load(os.path.join(HERE, "tracking_register.schema.json")), "tracking_register.json", errs)
        for m in tr.get("metrics", []):
            if not m.get("feeds") or BLANK.match(m.get("feeds", "")): errs.append(f"metric {m.get('id')}: feeds(dial) 없음 — 다이얼 없는 지표는 등재 금지")
            if not m.get("action"): errs.append(f"metric {m.get('id')}: action 없음")
        if nar is not None:
            reg_ids = {m["id"] for m in tr.get("metrics", [])} | {m.get("metric") for m in tr.get("metrics", [])}
            for mt in mets:
                if mt and mt not in reg_ids: warns.append(f"가설 metric `{mt}` 가 tracking_register 에 없다")
    for w in warns: print("  ~", w)
    for e in errs: print("  ✗", e)
    print(f"검사 {d}: 오류 {len(errs)} · 관측 {len(warns)}")
    return 1 if errs else 0
def selftest():
    """과제 21 픽스처: 잔재 있음(sources/*.jsonl 남음) → dualization_residue 관측 1,
    없음(POINTER.json 만) → 0. rc 는 파이프 밖에서 실측(이 함수 자체의 반환값으로)."""
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as tmp:
        # (a) 잔재 있음
        pack_a = os.path.join(tmp, "999999")
        os.makedirs(os.path.join(pack_a, "study"))
        os.makedirs(os.path.join(pack_a, "sources"))
        with open(os.path.join(pack_a, "sources", "reports.jsonl"), "w", encoding="utf-8") as f:
            f.write('{"broker":"x"}\n')
        res_a = dualization_residue(os.path.join(pack_a, "study"))
        if len(res_a) != 1:
            fails.append(f"(a) 잔재 픽스처: 관측 개수 기대 1, 실제 {len(res_a)}: {res_a}")
        # (b) 잔재 없음(POINTER.json 만)
        pack_b = os.path.join(tmp, "999998")
        os.makedirs(os.path.join(pack_b, "study"))
        os.makedirs(os.path.join(pack_b, "sources"))
        with open(os.path.join(pack_b, "sources", "POINTER.json"), "w", encoding="utf-8") as f:
            f.write('{"canon":"x"}\n')
        res_b = dualization_residue(os.path.join(pack_b, "study"))
        if len(res_b) != 0:
            fails.append(f"(b) 정리됨 픽스처: 관측 개수 기대 0, 실제 {len(res_b)}: {res_b}")
    fails += selftest_joint()
    fails += selftest_price_drivers()
    fails += selftest_thesis()
    fails += selftest_blind_stages()
    if fails:
        for x in fails: print("  ✗", x)
        print(f"selftest 실패 {len(fails)}건")
        return 1
    print("selftest 통과: 잔재 픽스처 관측 1 · 정리 픽스처 관측 0 · 이음매 계약 픽스처·변이 전부 기대대로 · 무하네스 짝(S0b·S2_consensus) 미끼·관문·변이 기대대로")
    return 0
BLIND_PROMPT = "테스트기업(TEST01), 기준일 2026-10-05. 이 회사에 대해 시장이 믿는 이야기, 이익을 움직이는 변수, 밸류체인에서의 위치, 틀릴 조건을 원천과 함께 써라."
def _joint_valid_blocks(prompt=BLIND_PROMPT):
    """픽스처용 유효 3블록 — ref 는 레포에 실재하는 편, 박스는 실재 박스, prompt_sha 는 프롬프트 파일의 실제 해시."""
    return {
        "cycle_context": {"searched": {"tickers": ["TEST01"], "boxes": ["semi.back.tcbonder"], "n_found": 1,
                                        "sources": ["market-intel/narratives/node_narratives.json", "market-intel/narratives/*.md frontmatter tickers"]},
                          "items": [{"narrative_id": "memory", "ref": "market-intel/narratives/memory.md", "asof": "2026-08-31",
                                     "stance": "adopt", "why": "적층 관문 서술을 MN1 의 배경으로 쓴다", "maps_to": ["MN1"]}]},
        "blind_contrast": {"backend": "external", "model": "<model>", "prompt_ref": "S0_blind_prompt.txt",
                           "prompt_sha": hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12], "output_ref": "S0_blind_external.md",
                           "made_before_s0_synthesis": True,
                           "only_blind": [{"claim": "무하네스 판만 본 주장 예시", "disposition": "needs_check", "why": "공시로 확인 전"}],
                           "only_ours": [{"claim": "우리 판만 본 주장 예시"}], "both": [{"claim": "양쪽이 본 주장 예시"}]},
        "chain_position": {"boxes": ["semi.back.tcbonder"],
                           "upstream": [{"name": "부품 공급사(모듈)", "what": "Bonder module", "share_or_dependence": "원재료 매입의 78.1%(1H26)", "source": "반기보고서 2026", "asof": "2026-06"}],
                           "downstream": [{"name": "SK하이닉스", "what": "HBM TC 본더", "share_or_dependence": "모름 — 공시_미제공(실명 비중 비공개)", "source": "core/valuechain/memory_hbm.yaml edges", "asof": "2026-06"}],
                           "what_company_does": "HBM 다이를 열압착으로 적층하는 TC 본더를 만든다",
                           "who_pays_whom": "메모리 IDM 이 장비 PO 를 내고 납품 시 대금을 치른다(PO→납기 약 1분기)",
                           "concentration": {"customers": "상위 2 거래처 58.8%(FY25)", "suppliers": "모듈 매입 집중 — 실명 미공개"},
                           "bottlenecks": "고객 인증(퀄)과 PO 타이밍이 물량을 정한다", "substitutes": ["한화세미텍·ASMPT TC 본더", "장기로 하이브리드 본더"],
                           "value_capture": "장비 단가 × 대수가 고객 capex 에서 직접 떨어지고 OPM 은 물량 레버리지로 40%대",
                           "q_asp_to_pnl": "대수 × 대당가 → 납기 분기 매출, 고정비 레버리지로 OPM 이 매출에 비례해 움직인다",
                           "stale_facts": [], "sources": ["core/valuechain/semi_krx_subchains.yaml#semi.back.tcbonder"]}}
def _git_env(date):
    e = dict(os.environ); e.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date); return e
def _git_commit(repo, paths, date):
    subprocess.run(["git", "-C", repo, "add", "--"] + paths, check=True, capture_output=True)
    subprocess.run(["git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "t"],
                   check=True, capture_output=True, env=_git_env(date))
def _joint_cases():
    """이음매 계약 회귀 미끼 전부 → 실패 문자열 목록(빈 목록 = 통과). 변이 검사가 이 함수를 다시 돈다."""
    import tempfile, io, contextlib
    g = globals()
    base = load(os.path.join(HERE, "fixtures", "s2_review_check_pass_sha_match", "narrative.json"))
    fails = []
    def run(nar, prompt=BLIND_PROMPT, git_plan=None, raw_created=None):
        with tempfile.TemporaryDirectory() as tmp:
            sd = os.path.join(tmp, "pack", "study"); os.makedirs(sd)
            json.dump(nar, open(os.path.join(sd, "narrative.json"), "w", encoding="utf-8"), ensure_ascii=False)
            open(os.path.join(sd, "S0_blind_prompt.txt"), "w", encoding="utf-8").write(prompt)
            open(os.path.join(sd, "S0_blind_external.md"), "w", encoding="utf-8").write("blind output\n")
            if git_plan:
                subprocess.run(["git", "init", "-q", tmp], check=True, capture_output=True)
                for paths, date in git_plan: _git_commit(tmp, [os.path.join(sd, p) for p in paths], date)
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf): rc = main(sd)
            except Exception as e:
                rc = f"예외 {type(e).__name__}: {e}"
            return rc, buf.getvalue()
    def mk(created, drop=None, mutate=None):
        nar = copy.deepcopy(base)
        if created is not None: nar["created"] = created
        nar.update(copy.deepcopy(_joint_valid_blocks()))
        if drop: nar.pop(drop)
        if mutate: mutate(nar)
        return nar
    def expect(name, nar, want_rc, must=None, must_not=None, **kw):
        rc, out = run(nar, **kw)
        if rc != want_rc: fails.append(f"[이음매] {name}: rc 기대 {want_rc}, 실제 {rc}\n{out[-1500:]}")
        for m in ([must] if isinstance(must, str) else must or []):
            if m not in out: fails.append(f"[이음매] {name}: 출력에 {m!r} 없음\n{out[-1500:]}")
        if must_not and must_not in out: fails.append(f"[이음매] {name}: 출력에 {must_not!r} 있으면 안 됨\n{out[-1500:]}")
    NEW, OLD = "2026-10-05", "2026-10-01"
    cp_ = lambda n: n["chain_position"]; bc_ = lambda n: n["blind_contrast"]; cc_ = lambda n: n["cycle_context"]
    # ── 유효·누락 ──
    expect("유효 3블록(신규)", mk(NEW), 0, must_not="이음매 관문")
    for k in JOINT_KEYS:
        expect(f"{k} 없음(신규) → 오류", mk(NEW, drop=k), 1, must=f"{k} 없음")
        expect(f"{k} 없음(옛 팩) → 관측만", mk(OLD, drop=k), 0, must="[이음매 관측")
    # ── 외부 감사 1: 공백·임의 문자열 채움 ──
    def blank_all(n):
        cc_(n)["items"][0]["why"] = " " * 12; cc_(n)["searched"]["sources"] = ["xxx"]
        for k in _CP_TEXT: cp_(n)[k] = " " * 20
        cp_(n)["concentration"] = {"customers": " " * 5, "suppliers": " " * 5}
        for side in ("upstream", "downstream"):
            cp_(n)[side] = [{"name": "  ", "what": "  ", "share_or_dependence": "  ", "source": "    ", "asof": "2026-06"}]
        cp_(n)["bottlenecks"] = [""]; cp_(n)["sources"] = ["xxx"]
    expect("공백 채움 종합(신규)", mk(NEW, mutate=blank_all), 1, must=["why 비었음", "what_company_does 비었음", "sources[0]", "upstream[0].name 비었음", "bottlenecks"])
    expect("bottlenecks=[None](신규)", mk(NEW, mutate=lambda n: cp_(n).__setitem__("bottlenecks", [None])), 1, must="bottlenecks")
    expect("substitutes=[{}](신규)", mk(NEW, mutate=lambda n: cp_(n).__setitem__("substitutes", [{}])), 1, must="substitutes")
    expect("chain sources 임의 문자열(신규)", mk(NEW, mutate=lambda n: cp_(n).__setitem__("sources", ["xxx"])), 1, must="chain_position.sources")
    expect("chain sources 실재 안 하는 경로(신규)", mk(NEW, mutate=lambda n: cp_(n).__setitem__("sources", ["core/valuechain/no_such.yaml"])), 1, must="core/valuechain")
    expect("party source 임의(신규)", mk(NEW, mutate=lambda n: cp_(n)["upstream"][0].__setitem__("source", "xxxx")), 1, must="원천으로 읽히지")
    expect("party asof 생략(신규)", mk(NEW, mutate=lambda n: cp_(n)["upstream"][0].pop("asof")), 1, must="asof")
    expect("claim 공백(신규)", mk(NEW, mutate=lambda n: bc_(n)["both"][0].__setitem__("claim", " " * 6)), 1, must="claim 비었음")
    # ── adopt ↔ MN/H 연결 ──
    expect("adopt maps_to 없음(신규)", mk(NEW, mutate=lambda n: cc_(n)["items"][0].pop("maps_to")), 1, must="maps_to 없음")
    expect("adopt maps_to H999(신규)", mk(NEW, mutate=lambda n: cc_(n)["items"][0].__setitem__("maps_to", ["H999"])), 1, must="H999")
    expect("cycle ref = 편 아님(CLAUDE.md)", mk(NEW, mutate=lambda n: cc_(n)["items"][0].__setitem__("ref", "CLAUDE.md")), 1, must="실재 편 파일이 아니다")
    expect("관련 편 0 + 검색 키(신규) = 유효", mk(NEW, mutate=lambda n: n.__setitem__("cycle_context", {"searched": {"tickers": ["TEST01"], "boxes": [], "n_found": 0, "sources": ["market-intel/narratives/node_narratives.json"]}, "items": []})), 0, must_not="이음매 관문")
    expect("검색 키 없음(신규) = 안 찾아봄", mk(NEW, mutate=lambda n: cc_(n).pop("searched")), 1, must="searched")
    expect("n_found 와 items 불일치(신규)", mk(NEW, mutate=lambda n: cc_(n)["searched"].__setitem__("n_found", 3)), 1, must="n_found=3")
    # ── 외부 감사 2: 가짜 blind ──
    expect("blind output_ref = CLAUDE.md(신규)", mk(NEW, mutate=lambda n: bc_(n).__setitem__("output_ref", "CLAUDE.md")), 1, must="S0_blind_")
    expect("blind prompt_sha 가짜(신규)", mk(NEW, mutate=lambda n: bc_(n).__setitem__("prompt_sha", "0123456789ab")), 1, must="prompt_sha")
    bad_prompt = "테스트기업(TEST01), 기준일 2026-10-05. 우리 가설 H1 과 market-intel/narratives/memory.md 를 참고해라."
    nb = mk(NEW); bc_(nb)["prompt_sha"] = hashlib.sha256(bad_prompt.encode()).hexdigest()[:12]
    expect("blind 프롬프트에 배경(신규)", nb, 1, must="배경이 섞였다", prompt=bad_prompt)
    expect("blind 차이표 셋 다 빔(신규)", mk(NEW, mutate=lambda n: bc_(n).update(only_blind=[], only_ours=[], both=[])), 1, must="전부 비었다")
    expect("only_blind disposition 없음(신규)", mk(NEW, mutate=lambda n: bc_(n)["only_blind"][0].pop("disposition")), 1, must="disposition 없음/어휘 밖")
    expect("blind not_run(신규)", mk(NEW, mutate=lambda n: bc_(n).__setitem__("status", "not_run — 실호출은 본체가")), 1, must="실호출 안 됨")
    expect("made_before false(신규)", mk(NEW, mutate=lambda n: bc_(n).__setitem__("made_before_s0_synthesis", False)), 1, must="made_before")
    expect("blind 순서 못 잼(git 밖) = 관측", mk(NEW), 0, must="blind 순서 못 잼")
    # ── 박스·낡음 ──
    expect("yaml 에 없는 박스(신규)", mk(NEW, mutate=lambda n: cp_(n).__setitem__("boxes", ["semi.back.no_such_box"])), 1, must="no_such_box")
    expect("3년 초과 미표시 2023-08(신규)", mk(NEW, mutate=lambda n: cp_(n)["downstream"][0].__setitem__("asof", "2023-08")), 1, must="3년 초과")
    expect("3년 이내 2023-10 = 낡음 아님(신규)", mk(NEW, mutate=lambda n: cp_(n)["downstream"][0].__setitem__("asof", "2023-10")), 0, must_not="이음매 관문")
    expect("FY18 미표시(신규)", mk(NEW, mutate=lambda n: cp_(n)["downstream"][0].__setitem__("asof", "FY18")), 1, must="3년 초과")
    expect("FY18 + stale_facts 표시 = 통과", mk(NEW, mutate=lambda n: (cp_(n)["downstream"][0].__setitem__("asof", "FY18"), cp_(n).__setitem__("stale_facts", [{"field": "downstream.SK하이닉스", "asof": "FY18"}]))), 0, must_not="이음매 관문")
    with tempfile.TemporaryDirectory() as ib:
        saved = g["INBOX_DIR"]
        try:
            g["INBOX_DIR"] = ib
            prop = lambda n: cp_(n).__setitem__("boxes", ["semi.test.proposed_box"])
            expect("제안 없는 새 박스(신규)", mk(NEW, mutate=prop), 1, must="proposed_box")
            open(os.path.join(ib, "x.jsonl"), "w").write(json.dumps({"schema": "valuechain/chain-proposal@1", "box_id": "semi.test.proposed_box"}) + "\n")
            expect("_inbox 제안이 있는 새 박스(신규) = 허용", mk(NEW, mutate=prop), 0, must_not="이음매 관문")
        finally:
            g["INBOX_DIR"] = saved
    # ── 외부 감사 4: 옛 팩 자료형 불량 → 예외 없이 관측, 신규는 오류 ──
    bad_types = [("cycle_context", {"searched": "bad", "items": []}), ("cycle_context", {"searched": 1, "items": 5}),
                 ("blind_contrast", {"only_blind": 1}), ("blind_contrast", "문자열"), ("chain_position", {"boxes": 1}),
                 ("chain_position", {"upstream": "x", "stale_facts": 3, "concentration": []}), ("cycle_context", [1, 2])]
    for k, v in bad_types:
        expect(f"옛 팩 자료형 불량 {k}={v!r}", mk(OLD, mutate=lambda n, k=k, v=v: n.__setitem__(k, v)), 0, must="[이음매 관측")
        expect(f"신규 자료형 불량 {k}={v!r}", mk(NEW, mutate=lambda n, k=k, v=v: n.__setitem__(k, v)), 1, must="[이음매 관문")
    # ── 외부 감사 5·6, 감사 C: 착수일 ──
    expect("created 없음 · git 없음 · asof 10-06 = 못 잼(막지 않음)", mk(None, drop="chain_position", mutate=lambda n: n.__setitem__("asof", "2026-10-06")), 0, must="착수일 못 잼")
    expect("created 2026-99-99 = 오류", mk("2026-99-99"), 1, must="달력 날짜가 아니다")
    expect("created 0000-00-00 = 오류", mk("0000-00-00"), 1, must="달력 날짜가 아니다")
    D6, D9 = "2026-10-06T10:00:00+09:00", "2026-09-01T10:00:00+09:00"
    expect("git 최초 추가 10-06 · created 없음 = 오류", mk(None), 1, must="created 없음", git_plan=[(["narrative.json", "S0_blind_prompt.txt", "S0_blind_external.md"], D6)])
    expect("git 최초 추가 09-01 · created 없음 = 옛 팩", mk(None, drop="chain_position"), 0, must="[이음매 관측", git_plan=[(["narrative.json"], D9)])
    expect("created 09-01 < git 10-06 = 늦은 쪽(신규) + 어긋남 경고", mk("2026-09-01", drop="chain_position"), 1, must=["앞선다", "chain_position 없음"], git_plan=[(["narrative.json", "S0_blind_prompt.txt", "S0_blind_external.md"], D6)])
    expect("blind 출력이 narrative 보다 늦게 커밋(신규)", mk(NEW), 1, must="늦다",
           git_plan=[(["narrative.json"], D6), (["S0_blind_prompt.txt", "S0_blind_external.md"], "2026-10-07T10:00:00+09:00")])
    expect("blind 먼저 · narrative 뒤 커밋(신규) = 통과", mk(NEW), 0, must_not="이음매 관문",
           git_plan=[(["S0_blind_prompt.txt", "S0_blind_external.md"], D6), (["narrative.json"], "2026-10-07T10:00:00+09:00")])
    saved = g["_is_shallow"]
    try:
        g["_is_shallow"] = lambda p: True
        expect("얕은 클론 · created 없음 = 못 잼", mk(None), 0, must="착수일 못 잼", git_plan=[(["narrative.json"], D6)])
    finally:
        g["_is_shallow"] = saved
    # ── Sol 6: jsonschema 부재 ──
    saved = g["_FORCE_NO_JSONSCHEMA"]
    try:
        g["_FORCE_NO_JSONSCHEMA"] = True
        expect("jsonschema 부재(신규) = 검사 불능 오류", mk(NEW), 1, must="검사 불능")
        expect("jsonschema 부재(옛 팩) = 관측", mk(OLD), 0, must="검사 불능")
    finally:
        g["_FORCE_NO_JSONSCHEMA"] = saved
    return fails
def _joint_mutants():
    """(이름, {전역: 대체값}) — 핵심 검사를 지운 변이. 각각에서 _joint_cases() 가 실패해야 한다."""
    import re as _re
    return [
        ("관문 날짜 2099", {"JOINT_EFFECTIVE": "2099-01-01"}),
        ("_resolve 가 늘 존재", {"_resolve": lambda ref, sd: os.path.join(REPO, "CLAUDE.md")}),
        ("_git_first_add_date 늘 None", {"_git_first_add_date": lambda p: None}),
        ("disposition 검사 제거", {"_blind_item_issues": lambda bc: []}),
        ("공백 제거 없음", {"_ns": lambda v, n=1: isinstance(v, str) and len(v) >= n}),
        ("프롬프트 금칙 제거", {"prompt_background": lambda t, tk=None: []}),
        ("jsonschema 부재 무시", {"_have_jsonschema": lambda: True}),
        ("달력 검증 제거", {"parse_date": lambda s: s if isinstance(s, str) and _re.fullmatch(r"\d{4}-\d{2}-\d{2}", s) else None}),
        ("낡음 판정 제거", {"is_stale": lambda p, r: False}),
        ("_inbox 제안 무시", {"proposed_box_ids": lambda: set()}),
        ("maps_to id 대조 제거", {"narrative_ids": lambda nar: {"H999", "MN1", "MN2", "H1", "H2", "H3"}}),
        ("원천 판독 제거", {"_source_ok": lambda v: isinstance(v, str)}),
        ("경로 토큰 검사 제거", {"_path_tokens": lambda s, sd, under=None: ["x"]}),
    ]
def selftest_joint():
    """회귀 미끼 → 변이 검사. 변이마다 미끼 하나 이상이 깨져야 통과(검사를 지우면 자가시험이 rc 1)."""
    g = globals()
    fails = _joint_cases()
    for name, patch in _joint_mutants():
        saved = {k: g[k] for k in patch}
        try:
            g.update(patch)
            n_broken = len(_joint_cases())
        finally:
            g.update(saved)
        if n_broken == 0: fails.append(f"[변이] {name}: 검사를 지웠는데 미끼가 하나도 안 깨졌다 — 그 검사를 지키는 미끼 없음")
    return fails
# ── price_drivers · business_nature 선택 칸 ──
# 있을 때만 검사한다(없으면 아무 말 없음 — 기존 팩 회귀 0). 원천 = tools/study/price_drivers.py, 작성 = price-driver-scout.
PD_KINDS = {"event", "sector_basket", "orders", "earnings", "flow", "narrative", "macro", "trend_index", "fandom/core_customer"}
PD_SUM_TOL = 5.0
def price_driver_issues(nar):
    errs, warns = [], []
    pdv = nar.get("price_drivers")
    if pdv is not None:
        if not isinstance(pdv, list) or not pdv:
            errs.append("price_drivers: 비었거나 배열이 아니다")
        else:
            tot = 0.0
            for i, x in enumerate(pdv):
                tag = f"price_drivers[{i}]"
                if not isinstance(x, dict): errs.append(f"{tag}: 객체 아님"); continue
                if not _ns(x.get("driver"), 3): errs.append(f"{tag}: driver 없음")
                w = x.get("weight_pct")
                if isinstance(w, bool) or not isinstance(w, (int, float)) or not 0 <= w <= 100: errs.append(f"{tag}: weight_pct 0~100 숫자 아님 ({w!r})")
                else: tot += w
                k = x.get("kind")
                if not _ns(k, 2): errs.append(f"{tag}: kind 없음")
                elif k not in PD_KINDS and not _ns(x.get("kind_note"), 3): errs.append(f"{tag}: kind `{k}` 는 알려진 목록 밖 — kind_note 필수")
                ev = x.get("evidence")
                good = [e for e in ev if isinstance(e, dict) and parse_date(e.get("date")) and _ns(e.get("ref"), 3)] if isinstance(ev, list) else []
                if not good: errs.append(f"{tag}: evidence 1건 이상(달력 날짜 + ref) 필요")
                if not _ns(x.get("falsify"), 5): errs.append(f"{tag}: falsify(틀릴 조건) 없음")
            if abs(tot - 100.0) > PD_SUM_TOL: errs.append(f"price_drivers: weight_pct 합 {tot:g} ≠ 100±{PD_SUM_TOL:g}")
    bn = nar.get("business_nature")
    if bn is not None:
        if not isinstance(bn, dict) or not _ns(bn.get("one_liner"), 10) or not all(isinstance(bn.get(k), list) and bn.get(k) for k in ("what_matters_most", "what_matters_less", "evidence")):
            errs.append("business_nature: one_liner·what_matters_most·what_matters_less·evidence 중 빈 칸")
        elif not bn.get("approved_by"):
            warns.append("business_nature: approved_by 비어 있음 — 서브 초안, 본체 승인 대기")
    elif pdv is not None:
        warns.append("price_drivers 가 있는데 business_nature 가 없다 — 경중의 전제(업의 본질) 미기재")
    return errs, warns
def _pd_cases():
    """미끼 — 실패 문자열 목록(빈 목록 = 전부 기대대로)."""
    ok = [{"driver": "섹터 바스켓 동행", "kind": "sector_basket", "weight_pct": 57, "evidence": [{"date": "2026-07-31", "ref": "drivers_attribution.json#top_days"}], "grade": "①", "falsify": "롤링120 R² < 0.3 두 분기"},
          {"driver": "실적 잠정 공시", "kind": "earnings", "weight_pct": 43.5, "evidence": [{"date": "2026-04-30", "ref": "DART rcept 20260430000000"}], "grade": "①", "falsify": "잠정실적일 |초과수익| < 3%"}]
    bn = {"one_liner": "미국 배전 변압기 수출 제조업", "what_matters_most": ["미국 수주"], "what_matters_less": ["국내 매출"], "evidence": ["반기보고서"], "approved_by": "main"}
    fails = []
    def exp(name, nar, want_err, must=None):
        e, _ = price_driver_issues(nar)
        if bool(e) != want_err: fails.append(f"[price_drivers] {name}: 오류 기대 {want_err}, 실제 {e}")
        if must and not any(must in x for x in e): fails.append(f"[price_drivers] {name}: '{must}' 오류 없음 {e}")
    exp("칸 없음 = 침묵", {}, False)
    exp("유효(합 100.5)", {"price_drivers": ok, "business_nature": bn}, False)
    exp("합 80", {"price_drivers": [ok[0]]}, True, "합")
    exp("kind 목록 밖 + note 없음", {"price_drivers": [ok[0], {**ok[1], "kind": "concert_tour"}]}, True, "kind_note")
    exp("kind 목록 밖 + note 있음 = 통과", {"price_drivers": [ok[0], {**ok[1], "kind": "concert_tour", "kind_note": "콘서트 매출 비중 큼"}]}, False)
    exp("evidence 0", {"price_drivers": [ok[0], {**ok[1], "evidence": []}]}, True, "evidence")
    exp("evidence 날짜 2026-13-40", {"price_drivers": [ok[0], {**ok[1], "evidence": [{"date": "2026-13-40", "ref": "DART x"}]}]}, True, "evidence")
    exp("falsify 채움 「-----」", {"price_drivers": [ok[0], {**ok[1], "falsify": "-----"}]}, True, "falsify")
    exp("business_nature 빈 칸", {"business_nature": {**bn, "what_matters_less": []}}, True, "business_nature")
    w = price_driver_issues({"business_nature": {**bn, "approved_by": None}})[1]
    if not any("승인 대기" in x for x in w): fails.append("[price_drivers] business_nature 미승인 관측 없음")
    return fails
def selftest_price_drivers():
    g = globals()
    fails = _pd_cases()
    for name, patch in [("합 허용폭 무한", {"PD_SUM_TOL": 1e9}), ("kind 목록 전부 허용", {"PD_KINDS": type("All", (), {"__contains__": lambda s, k: True})()}),
                        ("달력 검증 제거", {"parse_date": lambda s: s or None}), ("공백·채움 검사 제거", {"_ns": lambda v, n=1: isinstance(v, str) and len(v) >= 1})]:
        saved = {k: g[k] for k in patch}
        try:
            g.update(patch); n = len(_pd_cases())
        finally:
            g.update(saved)
        if n == 0: fails.append(f"[price_drivers 변이] {name}: 검사를 지웠는데 미끼가 안 깨졌다")
    return fails
if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    strict = "--strict-review-check" in argv
    argv = [a for a in argv if a != "--strict-review-check"]
    strict_blind = "--strict-blind" in argv  # 무하네스 짝(S0b·S2_consensus) 부재·불량을 rc 1 로(기본 관측, 2026-11-01 이후 착수는 자동)
    argv = [a for a in argv if a != "--strict-blind"]
    strict_thesis = "--strict-thesis" in argv  # 테제-모델 정합 위반을 rc 1 로(기본 관측)
    argv = [a for a in argv if a != "--strict-thesis"]
    model_dir = None
    if "--model-dir" in argv:
        i = argv.index("--model-dir"); model_dir = argv[i + 1] if i + 1 < len(argv) else None; argv = argv[:i] + argv[i + 2:]
    if not argv: sys.exit("사용: check_study.py <study_dir> [--strict-review-check] [--model-dir <모델 산출 dir> [--strict-thesis]] [--strict-blind] | check_study.py --selftest")
    sys.exit(main(argv[0], strict_review_check=strict, model_dir=model_dir, strict_thesis=strict_thesis, strict_blind=strict_blind))
