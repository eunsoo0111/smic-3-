#!/usr/bin/env python3
"""테제-모델 정합 게이트 — narrative.json 의 our_hypotheses[].model_links 가 모델 산출 경로와 같은 방향인가.

왜: 「투자 포인트가 모델에 담기게 — 수익성 좋아진다고 하면서 OPM 이 떨어지면 말이 안 된다.
셀사이드 모델을 참고하되 우리 내러티브가 반영됐는지 보고 빌드」. 가설 문장과 모델 숫자가 따로 놀면
S2 는 기계적 모델링이다. 이 검사는 가설마다 「어느 드라이버가 어느 케이스에서 어느 방향으로 가야 하나」를
모델 산출에서 직접 읽어 판정한다.

사용:
  check_thesis_model.py <narrative.json> <모델 산출 dir 또는 thesis_check_input.json> [--json OUT]
  check_thesis_model.py --emit <모델 산출 dir> -o thesis_check_input.json   # 폴백 형식을 계약으로 굳혀 쓴다
  check_thesis_model.py --selftest
rc: 0 = 위반 0 · 1 = 위반 ≥1(못 잼 포함, model_links 0 포함) · 2 = 사용 오류 · 3 = 못 읽음. 파이프로 삼키지 말 것.

model_link 칸(narrative.schema.json our_hypotheses[].model_links[]):
  driver   모델 드라이버/계정 id — paths[케이스] 의 키(rev·op·ni·opm·eps·orders·<세그먼트> …).
           opm·npm·gpm 은 paths 에 없으면 op/rev·ni/rev·gp/rev 로 유도한다.
  direction up|down|flat
  case     base|bull|bear|all 또는 세상 슬러그(케이스 = 서사 가지, equity-study §6-j)
  horizon  FY27(→ FY27E/FY27)·2y(기준 실적 연도 + 2) 등
  note     자유 문면
  선택: vs("anchor"(기본) | "consensus"), from(비교 시작 기간, 기본 = anchor_period), tol(허용 폭 — 비율 드라이버는
        절대 %p 소수, 금액은 상대 비율; 기본 0.002 / 0.01)
  판정: 변화 = 값(horizon) − 기준값(from 또는 컨센 같은 기간). |변화| ≤ tol → flat, 그보다 크면 부호로 up/down.

모델 산출 읽는 순서(dir 를 주면):
  ① thesis_check_input.json(계약 thesis_check_input@1 — fullmodel SKILL 「테제 시트」 절이 빌드마다 내게 한다)
  ② model_summary*.json 의 summary_v2 형식(worlds{세상:{FY26E:{rev,op,opm,eps…}}} + hist.annual + consensus) — 과거 S2 산출 형식
  ③ valuation*.json 의 cases{세상:{fy26e:{…}}} + consensus_reference(기준 실적 없음 → vs anchor 는 못 잼)
  ①이 있으면 ①만 본다. ②③ 폴백에서 base = sensitivity*.json base_case.world 또는 확률 최대 세상,
  bull/bear = 최종 추정 연도 EPS 최대/최소 세상(계약 ①의 case_map 이 있으면 그것).

thesis_check_input@1:
  {"schema":"thesis_check_input@1","ticker","asof","unit","anchor_period":"FY25",
   "periods":["FY25","FY26E","FY27E"],"case_map":{"base":"<세상>","bull":"<세상>","bear":"<세상>"},
   "paths":{"<세상>":{"<driver>":{"FY25":v,"FY26E":v,…}}},           # 실적 열은 모든 세상에 같은 값
   "consensus":{"<driver>":{"FY26E":v,…}}, "sellside_ref":[{"broker","date","driver","period","v"}],
   "source":{"workbook","sha256","built_by"}}
"""
import sys, os, json, glob, re, copy, tempfile

RATIO_HINT = re.compile(r"(^|_)(opm|npm|gpm|margin|ratio|rate|share|roe|roic)($|_)", re.I)
DERIVED = {"opm": ("op", "rev"), "npm": ("ni", "rev"), "gpm": ("gp", "rev")}
ALIASES = {"op_margin": "opm", "operating_margin": "opm", "revenue": "rev", "sales": "rev",
           "op_profit": "op", "operating_profit": "op", "net_income": "ni", "np": "ni"}


def _load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"못 읽음 {p}: {e}")
        sys.exit(3)


def _fy_num(p):
    m = re.match(r"^FY(\d{2,4})", str(p), re.I)
    if not m: return None
    y = int(m.group(1))
    return y + 2000 if y < 100 else y


def _norm_period(p):
    y = _fy_num(p)
    return None if y is None else f"FY{y % 100:02d}"


# ---------------- 모델 산출 → 계약 형식 ----------------
def from_summary_v2(ms, sens=None):
    hist = {(_norm_period(k)): v for k, v in (ms.get("hist", {}).get("annual") or {}).items() if _norm_period(k)}
    anchor = max(hist, key=lambda k: _fy_num(k)) if hist else None
    paths, eps_last, probs = {}, {}, {}
    for w, wv in (ms.get("worlds") or {}).items():
        ser = {}
        for per, row in hist.items():
            for k, v in row.items():
                if isinstance(v, (int, float)): ser.setdefault(k, {})[per] = v
        for per, row in wv.items():
            np_ = _norm_period(per)
            if not np_ or not isinstance(row, dict): continue
            for k, v in row.items():
                if isinstance(v, (int, float)): ser.setdefault(k, {})[np_ + "E"] = v
        paths[w] = ser
        probs[w] = wv.get("prob")
        last = sorted([p for p in ser.get("eps", {}) if p.endswith("E")], key=_fy_num)
        eps_last[w] = ser["eps"][last[-1]] if last else None
    cons = {}
    for per, row in (ms.get("consensus") or {}).items():
        np_ = _norm_period(per)
        if not np_ or not isinstance(row, dict): continue
        for k, v in row.items():
            if isinstance(v, (int, float)): cons.setdefault(ALIASES.get(k, k), {})[np_ + "E"] = v
    return _finish(ms.get("ticker"), ms.get("asof"), ms.get("unit"), anchor, paths, cons, eps_last, probs, sens,
                   "model_summary(summary_v2) 폴백")


def from_valuation_cases(val, sens=None):
    paths, eps_last, probs = {}, {}, {}
    for w, wv in (val.get("cases") or {}).items():
        ser = {}
        for per, row in wv.items():
            np_ = _norm_period(per)
            if not np_ or not isinstance(row, dict): continue
            for k, v in row.items():
                if isinstance(v, (int, float)): ser.setdefault(k, {})[np_ + "E"] = v
        paths[w] = ser
        probs[w] = wv.get("probability")
        last = sorted(ser.get("eps", {}), key=_fy_num)
        eps_last[w] = ser["eps"][last[-1]] if last else None
    cons = {}
    for per, row in (val.get("consensus_reference") or {}).items():
        np_ = _norm_period(per)
        if not np_ or not isinstance(row, dict): continue
        for k, v in row.items():
            if isinstance(v, (int, float)): cons.setdefault(ALIASES.get(k, k), {})[np_ + "E"] = v
    return _finish(val.get("ticker"), val.get("asof"), None, None, paths, cons, eps_last, probs, sens,
                   "valuation.cases 폴백(기준 실적 없음)")


def _finish(ticker, asof, unit, anchor, paths, cons, eps_last, probs, sens, src):
    cm = {}
    bw = (sens or {}).get("base_case", {}).get("world") if sens else None
    if bw in paths: cm["base"] = bw
    elif probs and any(v is not None for v in probs.values()):
        cm["base"] = max((w for w in probs if probs[w] is not None), key=lambda w: probs[w])
    ranked = [w for w in eps_last if eps_last[w] is not None]
    if ranked:
        cm["bull"] = max(ranked, key=lambda w: eps_last[w])
        cm["bear"] = min(ranked, key=lambda w: eps_last[w])
    periods = sorted({p for s in paths.values() for d in s.values() for p in d}, key=lambda p: (_fy_num(p), p))
    return {"schema": "thesis_check_input@1", "ticker": ticker, "asof": asof, "unit": unit, "anchor_period": anchor,
            "periods": periods, "case_map": cm, "paths": paths, "consensus": cons,
            "source": {"built_by": f"check_thesis_model.py {src}", "case_map_rule": "base=sensitivity base_case.world 또는 확률 최대 · bull/bear=최종 추정 연도 EPS 최대/최소"}}


def load_model(target):
    """target = thesis_check_input.json 파일 또는 모델 dir. (계약 dict, 읽은 경로) — 못 찾으면 (None, 사유)."""
    if os.path.isfile(target):
        d = _load(target)
        if d and d.get("schema") == "thesis_check_input@1": return d, target
        if d and "worlds" in d: return from_summary_v2(d), target
        if d and "cases" in d: return from_valuation_cases(d), target
        return None, f"{target}: 알 수 없는 형식"
    if not os.path.isdir(target): return None, f"{target}: 없음"
    p = os.path.join(target, "thesis_check_input.json")
    if os.path.exists(p): return _load(p), p
    sens = None
    for s in sorted(glob.glob(os.path.join(target, "sensitivity*.json")), reverse=True):
        sens = _load(s)
        if sens and sens.get("base_case", {}).get("world"): break
    for f in sorted(glob.glob(os.path.join(target, "model_summary*.json")), reverse=True):
        d = _load(f)
        if d and isinstance(d.get("worlds"), dict) and d["worlds"]: return from_summary_v2(d, sens), f
    for f in sorted(glob.glob(os.path.join(target, "valuation*.json")), reverse=True):
        d = _load(f)
        if d and isinstance(d.get("cases"), dict) and d["cases"]: return from_valuation_cases(d, sens), f
    return None, f"{target}: thesis_check_input.json·model_summary(worlds)·valuation(cases) 어느 것도 없다"


# ---------------- 판정 ----------------
def _series(model, case, driver):
    drv = ALIASES.get(driver, driver)
    s = (model.get("paths", {}).get(case) or {})
    derived = {}
    if drv in DERIVED:
        a, b = DERIVED[drv]
        if a in s and b in s:
            derived = {p: s[a][p] / s[b][p] for p in s[a] if p in s[b] and s[b][p]}
    if drv in s:  # 명시 값 우선, 빈 기간(예: 실적 열에 opm 없음)만 유도 값으로 메운다
        filled = dict(derived); filled.update(s[drv])
        return filled, (drv if len(filled) == len(s[drv]) else f"{drv}(빈 기간 {DERIVED[drv][0]}/{DERIVED[drv][1]})")
    if derived: return derived, f"{DERIVED[drv][0]}/{DERIVED[drv][1]}"
    return None, drv


def _pick(ser, period):
    """FY27 → FY27E 또는 FY27(실적) 중 있는 것."""
    if ser is None or period is None: return None, None
    n = _norm_period(period)
    for k in (period, n + "E" if n else None, n):
        if k and k in ser: return k, ser[k]
    return None, None


def _horizon_period(model, horizon):
    h = str(horizon)
    if _fy_num(h): return _norm_period(h)
    m = re.match(r"^(\d+)y$", h)
    if m and model.get("anchor_period"):
        y = _fy_num(model["anchor_period"]) + int(m.group(1))
        return f"FY{y % 100:02d}"
    return None


def _cases_for(model, case):
    if case == "all": return list(model.get("paths", {}))
    if case in model.get("paths", {}): return [case]
    w = (model.get("case_map") or {}).get(case)
    return [w] if w else []


def judge_link(hyp_id, link, model):
    rows = []
    driver, want = link.get("driver"), link.get("direction")
    case, horizon = link.get("case", "base"), link.get("horizon")
    vs = link.get("vs", "anchor")
    hp = _horizon_period(model, horizon)
    cases = _cases_for(model, case)
    base_row = {"hyp": hyp_id, "driver": driver, "want": want, "case": case, "horizon": horizon, "vs": vs}
    if want not in ("up", "down", "flat"):
        return [dict(base_row, world="-", path="-", got="-", verdict="못 잼", why=f"direction `{want}` 어휘 밖")]
    if not cases:
        return [dict(base_row, world="-", path="-", got="-", verdict="못 잼", why=f"케이스 `{case}` 가 모델에 없다(case_map·paths)")]
    if hp is None:
        return [dict(base_row, world="-", path="-", got="-", verdict="못 잼", why=f"horizon `{horizon}` 를 기간으로 못 바꿈")]
    for w in cases:
        ser, src = _series(model, w, driver)
        r = dict(base_row, world=w)
        if ser is None:
            rows.append(dict(r, path="-", got="-", verdict="못 잼", why=f"드라이버 `{driver}` 가 모델 paths[{w}] 에 없다")); continue
        kh, vh = _pick(ser, hp)
        if vs == "consensus":
            cser = (model.get("consensus") or {}).get(ALIASES.get(driver, driver))
            if cser is None and driver in DERIVED:
                a, b = DERIVED[driver]; ca, cb = (model.get("consensus") or {}).get(a), (model.get("consensus") or {}).get(b)
                if ca and cb: cser = {p: ca[p] / cb[p] for p in ca if p in cb and cb[p]}
            kf, vf = _pick(cser, hp)
            ref_label = f"컨센 {kf}"
        else:
            frm = link.get("from") or model.get("anchor_period")
            kf, vf = _pick(ser, frm)
            ref_label = f"{kf}"
        if vh is None or vf is None:
            rows.append(dict(r, path=f"{src}: {kf or '?'}→{kh or hp}", got="-", verdict="못 잼",
                             why=f"{'기준' if vf is None else 'horizon'} 값 없음(anchor_period={model.get('anchor_period')}, vs={vs})")); continue
        ratio = bool(RATIO_HINT.search(driver)) or driver in DERIVED
        tol = link.get("tol", 0.002 if ratio else 0.01)
        delta = (vh - vf) if ratio else ((vh - vf) / abs(vf) if vf else vh - vf)
        got = "flat" if abs(delta) <= tol else ("up" if delta > 0 else "down")
        fmt = (lambda x: f"{x * 100:.2f}%") if ratio else (lambda x: f"{x:,.1f}")
        dtxt = f"{delta * 100:+.2f}%p" if ratio else f"{delta * 100:+.1f}%"
        rows.append(dict(r, path=f"{src}: {ref_label} {fmt(vf)} → {kh} {fmt(vh)} ({dtxt}, tol {tol})", got=got,
                         verdict="통과" if got == want else "위반",
                         why="" if got == want else f"가설은 {want}, 모델은 {got}"))
    return rows


def check(nar, model):
    rows, n_links = [], 0
    for h in nar.get("our_hypotheses", []):
        for link in h.get("model_links") or []:
            n_links += 1
            rows += judge_link(h.get("id"), link, model)
    bad = [r for r in rows if r["verdict"] != "통과"]
    return rows, bad, n_links


def render(rows, n_links, model_src):
    out = [f"테제-모델 정합: model_links {n_links}건 · 판정 행 {len(rows)} · 위반 {sum(r['verdict'] == '위반' for r in rows)} · 못 잼 {sum(r['verdict'] == '못 잼' for r in rows)} (모델 = {model_src})",
           "| 가설 | 드라이버 | 기대 방향 | 케이스→세상 | horizon | 모델 경로 | 모델 방향 | 판정 |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['hyp']} | {r['driver']} | {r['want']}{' vs 컨센' if r['vs'] == 'consensus' else ''} | {r['case']}→{r['world']} | {r['horizon']} | {r['path']} | {r['got']} | {r['verdict']}{(' — ' + r['why']) if r['why'] else ''} |")
    return "\n".join(out)


def run(nar_path, target, json_out=None, quiet=False):
    nar = _load(nar_path)
    if nar is None:
        print(f"못 읽음 {nar_path}"); return 3
    model, src = load_model(target)
    if model is None:
        print(f"✗ 모델 산출 못 찾음 — {src} (못 잼 = 위반)"); return 1
    rows, bad, n = check(nar, model)
    if n == 0:
        print("✗ model_links 0건 — 테제가 모델 드라이버에 안 묶였다(분모 0, S2 미완)"); return 1
    if not quiet: print(render(rows, n, src))
    if json_out:
        json.dump({"model_source": src, "n_links": n, "rows": rows, "rc": 1 if bad else 0}, open(json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return 1 if bad else 0


# ---------------- 자가시험 ----------------
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _cases():
    """미끼 → 실패 문자열 목록(빈 = 통과). 변이 검사가 이 함수를 다시 돈다."""
    fails = []
    pass_dir = os.path.join(FIX, "thesis_model_pass")
    nar = _load(os.path.join(pass_dir, "narrative.json"))
    model, _ = load_model(os.path.join(pass_dir, "model"))
    if nar is None or model is None: return ["픽스처 thesis_model_pass 못 읽음"]
    _, bad, n = check(nar, model)
    if bad or n == 0: fails.append(f"(a) 정합 픽스처가 통과해야 하는데 위반 {len(bad)}·링크 {n}")
    # (b) 레포 픽스처: 모델 OPM 경로를 거꾸로 뒤집은 판 → 위반
    rev_model, _ = load_model(os.path.join(FIX, "thesis_model_opm_reversed", "model"))
    _, bad, _ = check(nar, rev_model) if rev_model else ([], [], 0)
    if not any(r["driver"] == "opm" and r["verdict"] == "위반" for r in bad): fails.append("(b) OPM 경로 역전 픽스처가 위반으로 안 잡힘")
    # (c) 메모리 변이: 가설 방향 뒤집기(up↔down) → 위반
    n2 = copy.deepcopy(nar)
    for h in n2["our_hypotheses"]:
        for l in h.get("model_links", []):
            l["direction"] = {"up": "down", "down": "up", "flat": "up"}[l["direction"]]
    _, bad, _ = check(n2, model)
    if len(bad) == 0: fails.append("(c) 방향을 다 뒤집었는데 위반 0")
    # (d) 드라이버 없음 → 못 잼(=위반)
    n3 = copy.deepcopy(nar); n3["our_hypotheses"][0]["model_links"][0]["driver"] = "no_such_driver"
    _, bad, _ = check(n3, model)
    if not any(r["verdict"] == "못 잼" for r in bad): fails.append("(d) 없는 드라이버가 못 잼으로 안 잡힘")
    # (e) flat 허용 폭: OPM +0.1%p 는 flat
    m4 = copy.deepcopy(model)
    for w in m4["paths"].values():
        w["opm"] = {k: 0.30 for k in w["opm"]}; w["opm"]["FY27E"] = 0.301
    rows = judge_link("HX", {"driver": "opm", "direction": "flat", "case": "base", "horizon": "FY27"}, m4)
    if rows[0]["verdict"] != "통과": fails.append(f"(e) +0.1%p 가 flat 으로 안 읽힘: {rows[0]}")
    # (f) 유도 OPM(op/rev) 경로: opm 칸을 지워도 판정이 같아야
    m5 = copy.deepcopy(model)
    for w in m5["paths"].values(): w.pop("opm", None)
    _, bad5, _ = check(nar, m5)
    if bad5: fails.append(f"(f) op/rev 유도 OPM 판정이 다름: {bad5[:1]}")
    # (g) vs 컨센: 컨센보다 낮은 매출은 down
    rows = judge_link("HY", {"driver": "rev", "direction": "down", "case": "base", "horizon": "FY27", "vs": "consensus"}, model)
    if rows[0]["verdict"] != "통과": fails.append(f"(g) vs 컨센 판정 실패: {rows[0]}")
    # (h) summary_v2 폴백 읽기(과거 S2 형식 축약판: 세상엔 opm 칸, 실적엔 rev·op 만) → 계약과 같은 판정
    ms = {"ticker": "T", "asof": "2026-10-20", "unit": "억원", "hist": {"annual": {"FY25": {"rev": 100, "op": 30}}},
          "worlds": {"w_base": {"prob": 0.6, "FY26E": {"rev": 120, "op": 40, "eps": 10, "opm": 0.3333}, "FY27E": {"rev": 140, "op": 49, "eps": 12, "opm": 0.35}},
                     "w_bear": {"prob": 0.4, "FY26E": {"rev": 105, "op": 30, "eps": 8}, "FY27E": {"rev": 100, "op": 27, "eps": 7}}},
          "consensus": {"FY27E": {"rev": 150, "op": 50}}}
    fm = from_summary_v2(ms)
    r_up = judge_link("HZ", {"driver": "opm", "direction": "up", "case": "base", "horizon": "FY27"}, fm)
    r_bear = judge_link("HZ", {"driver": "opm", "direction": "down", "case": "bear", "horizon": "2y"}, fm)
    if fm["case_map"].get("base") != "w_base" or r_up[0]["verdict"] != "통과" or r_bear[0]["verdict"] != "통과":
        fails.append(f"(h) summary_v2 폴백 판정 실패: {fm['case_map']} {r_up[0]['verdict']} {r_bear[0]['verdict']}")
    # (i) 링크 0 → run rc 1
    with tempfile.TemporaryDirectory() as t:
        n0 = copy.deepcopy(nar)
        for h in n0["our_hypotheses"]: h.pop("model_links", None)
        p = os.path.join(t, "n.json"); json.dump(n0, open(p, "w"))
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            rc0 = run(p, os.path.join(pass_dir, "model"))
            rc_ok = run(os.path.join(pass_dir, "narrative.json"), os.path.join(pass_dir, "model"), quiet=True)
            rc_rev = run(os.path.join(pass_dir, "narrative.json"), os.path.join(FIX, "thesis_model_opm_reversed", "model"), quiet=True)
        if (rc0, rc_ok, rc_rev) != (1, 0, 1): fails.append(f"(i) rc 기대 (링크0=1, 정합=0, 역전=1), 실제 ({rc0}, {rc_ok}, {rc_rev})")
    return fails


def _mutants():
    g = globals()
    orig_judge = g["judge_link"]
    orig_series = g["_series"]
    return [
        ("방향 비교 제거(모델 방향=기대 방향)", {"judge_link": lambda h, l, m: [dict(r, verdict="통과", why="") for r in orig_judge(h, l, m)]}),
        ("유도 OPM 제거", {"DERIVED": {}}),
        ("빈 기간 유도 메우기 제거", {"_series": lambda m, c, d: ((m.get("paths", {}).get(c) or {}).get(d), d) if d in (m.get("paths", {}).get(c) or {}) else orig_series(m, c, d)}),
        ("케이스 all 확장 제거", {"_cases_for": lambda m, c: list(m.get("paths", {}))[:1]}),
        ("horizon 2y 해석 제거", {"_horizon_period": lambda m, h: _norm_period(h) if _fy_num(h) else None}),
    ]


def selftest():
    fails = _cases()
    g = globals()
    for name, patch in _mutants():
        saved = {k: g[k] for k in patch}
        try:
            g.update(patch)
            broken = len(_cases())
        finally:
            g.update(saved)
        if broken == 0: fails.append(f"[변이] {name}: 검사를 지웠는데 미끼가 하나도 안 깨졌다")
    for f in fails: print("  ✗", f)
    print(f"selftest {'통과' if not fails else '실패 ' + str(len(fails)) + '건'}: 미끼 (a)~(i) · 변이 {len(_mutants())}")
    return 1 if fails else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: sys.exit(selftest())
    if "--emit" in a:
        i = a.index("--emit")
        if "-o" not in a or len(a) <= i + 1: sys.exit("사용: --emit <모델 dir> -o thesis_check_input.json") or 2
        m, src = load_model(a[i + 1])
        if m is None: print(f"✗ {src}"); sys.exit(1)
        json.dump(m, open(a[a.index("-o") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"썼다 {a[a.index('-o') + 1]} ← {src} · 세상 {len(m['paths'])} · case_map {m['case_map']}"); sys.exit(0)
    jo = None
    if "--json" in a:
        jo = a[a.index("--json") + 1]; a = [x for j, x in enumerate(a) if x != "--json" and (j == 0 or a[j - 1] != "--json")]
    if len(a) != 2: print(__doc__.split("\n\n")[0]); print("사용: check_thesis_model.py <narrative.json> <모델 dir|thesis_check_input.json> [--json OUT] | --emit DIR -o OUT | --selftest"); sys.exit(2)
    sys.exit(run(a[0], a[1], jo))
