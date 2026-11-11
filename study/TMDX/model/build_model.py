#!/usr/bin/env python3
"""TMDX P×Q 모델 빌더 (equity-analysis S2).

설계(modeling-method 하우스 표준):
- 판단은 INPUTS 한 곳에만 둔다. 아래 산술은 INPUTS 와 원문 원장(sources/primary_facts.json)만 읽는다.
- Q = 사망 기증자 × 기증자당 이식(활용률) × TMDX 점유율 (+ 임상 케이스), P = 미국 케이스당 매출.
- 2026E 는 9M 실적 + 4Q 추정(가이던스 중간값에 닻), 2027E~2028E 는 드라이버 추정.
- EPS 는 회사 공시와 같은 if-converted 기준(전환사채 489만 주 포함 + 세후 이자 가산).

실행: python3 build_model.py  →  tmdx_model.xlsx · model_summary.json · sensitivity_grid.json · thesis_check_input.json
"""
import json, os, copy, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = json.load(open(os.path.join(HERE, "..", "sources", "primary_facts.json"), encoding="utf-8"))
F25, Q3, M9 = FACTS["fy2025"], FACTS["q3_2026"], FACTS["nine_months_2026"]
IND = FACTS["industry_2025"]
WB = FACTS["industry_2025_from_user_workbook"]
CONS = FACTS["consensus_post_3q26"]
PRICE = FACTS["price"]["close"]

YEARS = ["FY25", "FY26E", "FY27E", "FY28E"]

# ─────────────────────────── INPUTS (판단은 여기에만) ───────────────────────────
BASE = {
    # 산업(TMDX 가 못 바꾸는 변수)
    "donor_growth":      {"FY26E": -0.04, "FY27E": 0.00, "FY28E": 0.01},   # 25A −2.5%(UNOS), 3Q26 −6%(콜) → 26E −4%
    # 기증자당 이식(활용률) — 25A 는 원장에서 계산
    "util_liver":        {"FY26E": 0.720, "FY27E": 0.735, "FY28E": 0.750},  # 25A 0.703, 24→25 +0.06 보다 보수적
    "util_heart":        {"FY26E": 0.280, "FY27E": 0.285, "FY28E": 0.290},
    "util_lung":         {"FY26E": 0.210, "FY27E": 0.212, "FY28E": 0.215},
    # TMDX 점유율(케이스 ÷ 사망 기증 이식) — 26E 는 실적 닻(아래 Q4 추정에서 역산)
    "share_liver":       {"FY27E": 0.520, "FY28E": 0.565},   # 25A 36.1%(회사 4,197건), 26E 약 46.7%(실적 닻), 3Q26 연환산 약 47.5%
    "share_heart":       {"FY27E": 0.225, "FY28E": 0.240},   # 25A 18.6%(854건), 26E 약 21.4%
    "share_lung":        {"FY27E": 0.020, "FY28E": 0.030},   # 25A 2.5%(88건), 26E 약 1.6%
    # P: 미국 케이스당 매출(장기 공통 가정 — 장기별 케이스 미공시)
    "asp_growth":        {"FY26E": 0.010, "FY27E": 0.010, "FY28E": 0.010},
    # 임상(ENHANCE Part B 600 + DENOVO 450 = 1,050명, CAP 90 은 기존 적응증이라 제외)
    "trial_total":       1050,
    "trial_enroll_share": {"FY27E": 0.40, "FY28E": 0.45},
    "trial_rev_per_case": 0.100,   # $M, OCS 군(심장 약 131K·폐 약 153K) 2/3 + CHOPS 군(가격 미공개, 저가) 1/3 섞인 가정
    # 4Q26E(가이던스 764~774 중간값에 닻)
    "q4_26": {"us_liver": 154.0, "us_heart": 33.5, "us_lung": 2.0, "ous": 7.0, "other": 5.2, "gm": 0.580, "opex": 92.5},
    # 해외·비이식 서비스(PAD 전세 등)
    "ous_growth":        {"FY27E": 0.30, "FY28E": 0.30},
    "other_rev":         {"FY27E": 28.5, "FY28E": 31.0},
    # 비용
    "gm":                {"FY27E": 0.588, "FY28E": 0.593},   # 회사: 단·중기 지금 수준 유지
    "opex_growth":       {"FY27E": 0.10, "FY28E": 0.07},     # R&D 분기 ~29M 안정(콜) + 유럽·본사
    "adj_addback":       {"FY26E": 8.3, "FY27E": 4.0, "FY28E": 3.0},  # 비GAAP 가산(거래비용·상각 등)
    # 영업외·세금·주식수
    "tax_rate":          {"FY26E": 0.25, "FY27E": 0.25, "FY28E": 0.25},  # 10-Q: FY26 25~27%
    "cash_yield":        0.023,      # FY26 이자수익 약 11M(콜) ÷ 평균 현금 약 490M
    "hq_purchase_date":  "2027-12-31",  # 회사 가정대로 매입옵션 행사(374.6M)
    "convert_settle":    "shares_if_above_94",  # 28.6 만기: 94달러 위면 주식 결제 가정
    "basic_shares":      {"FY26E": 34.65, "FY27E": 35.05, "FY28E": 35.45},
    "other_dilutive":    1.25,       # 옵션·RSU (3Q26 1.25M)
    # 현금흐름(간이)
    "da":                {"FY26E": 40.0, "FY27E": 45.0, "FY28E": 48.0},
    "sbc":               {"FY26E": 45.0, "FY27E": 48.0, "FY28E": 52.0},
    "wc_build":          {"FY26E": 50.0, "FY27E": 30.0, "FY28E": 30.0},   # 9M26 운전자본 −52.8(매출채권·재고)
    "capex":             {"FY26E": 62.0, "FY27E": 60.0, "FY28E": 55.0},   # 9M26 52.1(필지·본사 공사)
    "deferred_tax":      {"FY26E": 14.0, "FY27E": 22.0, "FY28E": 25.0},   # 이연법인세자산 72.8 사용 = 현금 세금 < 장부 세금
    # 밸류
    "pe_12m":            30.0,       # 12개월 뒤 선행(FY28E) P/E
}

# 케이스: 각각 단일 변수(간 점유율 경로)에 묶고, 함께 움직이는 값만 바꾼다
CASES = {
    "base": {},
    "downside": {   # 간 점유율이 47% 근처에서 멈추는 세상(DBD 표준 간은 냉장·저온으로 충분)
        "share_liver": {"FY27E": 0.485, "FY28E": 0.495},
        "donor_growth": {"FY26E": -0.04, "FY27E": -0.05, "FY28E": 0.00},
        "trial_enroll_share": {"FY27E": 0.25, "FY28E": 0.40},
        "share_heart": {"FY27E": 0.215, "FY28E": 0.215},
        "opex_growth": {"FY27E": 0.05, "FY28E": 0.04},   # 성장이 꺾이면 R&D(신장 등) 속도 조절 — 회사: 수익성 유지
        "pe_12m": 24.0,
    },
    "upside": {     # 간 점유율 60% 로 가고 심장·폐 임상이 빨리 차는 세상
        "share_liver": {"FY27E": 0.545, "FY28E": 0.615},
        "util_liver": {"FY26E": 0.720, "FY27E": 0.750, "FY28E": 0.775},
        "trial_enroll_share": {"FY27E": 0.55, "FY28E": 0.45},
        "share_heart": {"FY27E": 0.235, "FY28E": 0.270},
        "pe_12m": 35.0,
    },
}


def merged(case):
    a = copy.deepcopy(BASE)
    for k, v in CASES[case].items():
        if isinstance(v, dict): a[k].update(v)
        else: a[k] = v
    return a


def run(a):
    r = {y: {} for y in YEARS}
    # FY25 실적
    d25 = IND["deceased_donors"]
    asp25 = F25["us_transplant"] / F25["us_ocs_cases"]           # $M/건 (블렌디드)
    OC = FACTS["fy2025_cases_by_organ"]                            # 회사 공개 장기별 케이스(②)
    asp_org25 = {o: OC[f"asp_{o}"] for o in ("liver", "heart", "lung")}
    pools25 = {"liver": IND["liver_deceased"], "heart": WB["heart_transplants"], "lung": WB["lung_transplants"]}
    r["FY25"].update(donors=d25, asp=asp25,
                     util_liver=pools25["liver"] / d25, util_heart=pools25["heart"] / d25, util_lung=pools25["lung"] / d25,
                     pool_liver=pools25["liver"], pool_heart=pools25["heart"], pool_lung=pools25["lung"],
                     us_liver=F25["us_liver"], us_heart=F25["us_heart"], us_lung=F25["us_lung"], trial=0.0,
                     ous=F25["ous_transplant"], other=F25["non_transplant_service"], rev=F25["revenue"],
                     gp=F25["revenue"] * F25["gross_margin_pct"] / 100, opex=F25["opex"], op=F25["operating_income"],
                     net_other=-F25["interest_expense"] + 9.0, ni=F25["net_income"], eps=F25["diluted_eps"],
                     dil_shares=F25["diluted_shares_m"])
    for org in ("liver", "heart", "lung"):
        r["FY25"][f"asp_{org}"] = asp_org25[org]
        r["FY25"][f"cases_{org}"] = OC[org]
        r["FY25"][f"share_{org}"] = r["FY25"][f"cases_{org}"] / pools25[org]
    r["FY25"]["cases_us"] = F25["us_ocs_cases"]
    f = r["FY25"]
    f.update(us_total=f["us_liver"] + f["us_heart"] + f["us_lung"], opm=f["op"] / f["rev"], gpm=f["gp"] / f["rev"],
             adj_op=f["op"] + 2.4, adj_opm=(f["op"] + 2.4) / f["rev"], adj_eps=None,
             ni_ex_va=F25["net_income"] - F25["tax_benefit"] - (F25["operating_income"] - F25["interest_expense"] + 9.0) * F25["etr_ex_va_pct"] / 100)

    prev_d, prev_asp = d25, asp25
    prev_aspo = dict(asp_org25)
    cash = FACTS["balance_sheet_3q26"]["cash"]
    for y in YEARS[1:]:
        o = r[y]
        o["donors"] = prev_d * (1 + a["donor_growth"][y]); prev_d = o["donors"]
        o["asp"] = prev_asp * (1 + a["asp_growth"][y]); prev_asp = o["asp"]
        for org in ("liver", "heart", "lung"):
            o[f"asp_{org}"] = prev_aspo[org] * (1 + a["asp_growth"][y]); prev_aspo[org] = o[f"asp_{org}"]
        for org in ("liver", "heart", "lung"):
            o[f"util_{org}"] = a[f"util_{org}"][y]
            o[f"pool_{org}"] = o["donors"] * o[f"util_{org}"]
        if y == "FY26E":
            q4 = a["q4_26"]
            o["us_liver"] = M9["us_liver"] + q4["us_liver"]
            o["us_heart"] = M9["us_heart"] + q4["us_heart"]
            o["us_lung"] = M9["us_lung"] + q4["us_lung"]
            o["trial"] = 0.0
            o["ous"] = M9["ous_transplant"] + q4["ous"]
            o["other"] = M9["non_transplant_service"] + q4["other"]
            for org in ("liver", "heart", "lung"):
                o[f"cases_{org}"] = o[f"us_{org}"] / o[f"asp_{org}"]
                o[f"share_{org}"] = o[f"cases_{org}"] / o[f"pool_{org}"]
        else:
            for org in ("liver", "heart", "lung"):
                o[f"share_{org}"] = a[f"share_{org}"][y]
                o[f"cases_{org}"] = o[f"pool_{org}"] * o[f"share_{org}"]
                o[f"us_{org}"] = o[f"cases_{org}"] * o[f"asp_{org}"]
            o["trial_cases"] = a["trial_total"] * a["trial_enroll_share"][y]
            o["trial"] = o["trial_cases"] * a["trial_rev_per_case"]
            o["ous"] = r[YEARS[YEARS.index(y) - 1]]["ous"] * (1 + a["ous_growth"][y])
            o["other"] = a["other_rev"][y]
        o["cases_us"] = o["cases_liver"] + o["cases_heart"] + o["cases_lung"] + o.get("trial_cases", 0.0)
        o["us_total"] = o["us_liver"] + o["us_heart"] + o["us_lung"] + o["trial"]
        o["rev"] = o["us_total"] + o["ous"] + o["other"]
        # 비용
        if y == "FY26E":
            q4 = a["q4_26"]
            q4_rev = o["rev"] - M9["revenue"]
            o["q4_rev"] = q4_rev
            o["gp"] = M9["gross_profit"] + q4_rev * q4["gm"]
            o["opex"] = M9["opex"] + q4["opex"]
        else:
            o["gp"] = o["rev"] * a["gm"][y]
            o["opex"] = r[YEARS[YEARS.index(y) - 1]]["opex"] * (1 + a["opex_growth"][y])
        o["op"] = o["gp"] - o["opex"]
        o["adj_op"] = o["op"] + a["adj_addback"][y]
        # 영업외: 전환사채 이자(쿠폰+상각 분기 2.5M), CIBC, 본사 리스 이자, 이자수익
        if y == "FY26E":
            o["int_exp"] = 29.0; o["int_inc"] = 11.0          # 회사 FY26 안내(콜)
            convert_int = 10.0
        elif y == "FY27E":
            convert_int = 10.0
            cibc = 0.053 * 25.0                                 # 잔액 54.8 → 27.7 만기까지 월 상환, 평균 약 25
            lease = 15.5                                        # 매입 전까지 리스 이자
            o["int_exp"] = convert_int + cibc + lease
            o["int_inc"] = a["cash_yield"] * 470.0
        else:
            convert_int = 5.0                                   # 28.6.1 만기까지 반년
            o["int_exp"] = convert_int
            o["int_inc"] = a["cash_yield"] * r["FY27E"]["cash_end"]
        o["net_other"] = o["int_inc"] - o["int_exp"]
        o["pretax"] = o["op"] + o["net_other"]
        o["tax"] = o["pretax"] * a["tax_rate"][y]
        o["ni"] = o["pretax"] - o["tax"]
        # if-converted EPS(회사 공시 기준)
        addback = convert_int * (1 - a["tax_rate"][y]) * (0.735 / 0.75)   # 3Q26 실제 가산 1.838/분기 ≈ 7.35/년
        conv_sh = FACTS["convertible_notes"]["shares_underlying_m"]
        o["dil_shares"] = a["basic_shares"][y] + conv_sh + a["other_dilutive"]
        o["eps"] = (o["ni"] + addback) / o["dil_shares"]
        o["adj_ni"] = o["ni"] + a["adj_addback"][y] * (1 - a["tax_rate"][y])
        o["adj_eps"] = (o["adj_ni"] + addback) / o["dil_shares"]
        o["opm"] = o["op"] / o["rev"]; o["adj_opm"] = o["adj_op"] / o["rev"]; o["gpm"] = o["gp"] / o["rev"]
        # 현금(간이): FCF = NI + D&A + SBC − 운전자본 − CapEx
        o["fcf"] = o["ni"] + a["da"][y] + a["sbc"][y] + a["deferred_tax"][y] - a["wc_build"][y] - a["capex"][y]
        if y == "FY26E":
            q4_fcf = o["fcf"] - (M9["cfo"] - M9["capex"])
            o["cash_end"] = cash + q4_fcf - 54.818 * 0.25       # 4Q CIBC 상환 약 1/4
        elif y == "FY27E":
            o["cash_end"] = r["FY26E"]["cash_end"] + o["fcf"] - 54.818 * 0.75 - FACTS["hq_finance_lease"]["purchase_option_price"]
        else:
            o["cash_end"] = r["FY27E"]["cash_end"] + o["fcf"]
            o["cash_end_if_convert_cash_repaid"] = o["cash_end"] - FACTS["balance_sheet_3q26"]["convertible_principal"]
    return r


def value(r, a):
    eps28 = r["FY28E"]["eps"]
    return {"eps_fwd_12m": eps28, "pe": a["pe_12m"], "value": eps28 * a["pe_12m"], "vs_price": eps28 * a["pe_12m"] / PRICE - 1}


def grid_eps27():
    shares = [0.475, 0.495, 0.520, 0.545, 0.570]
    opexg = [0.06, 0.10, 0.14]
    rows = []
    for s in shares:
        row = []
        for g in opexg:
            a = merged("base"); a["share_liver"]["FY27E"] = s; a["opex_growth"]["FY27E"] = g
            row.append(round(run(a)["FY27E"]["eps"], 2))
        rows.append(row)
    return {"name": "FY27E 희석 EPS($, if-converted) — 간 점유율(FY27E) × opex 증가율(FY27E)",
            "rows_label": "share_liver_FY27E", "rows": shares, "cols_label": "opex_growth_FY27E", "cols": opexg, "values": rows,
            "house_cell": [0.520, 0.10], "consensus_adj_eps_fy27": CONS["eps_adj_fy27"]}


def grid_value():
    shares28 = [0.495, 0.530, 0.565, 0.615]
    pes = [22.0, 26.0, 30.0, 35.0]
    eps_by_share, rows = [], []
    for s in shares28:
        a = merged("base"); a["share_liver"]["FY28E"] = s
        e = run(a)["FY28E"]["eps"]; eps_by_share.append(round(e, 2))
        rows.append([round(e * p, 1) for p in pes])
    # 시장 요구 칸: 현재가 = FY28E EPS × P/E 인 조합
    implied_eps = {str(p): round(PRICE / p, 2) for p in pes}
    return {"name": "12개월 케이스 값($/주) — 간 점유율(FY28E) × 12개월 뒤 선행 P/E(FY28E EPS 기준)",
            "rows_label": "share_liver_FY28E", "rows": shares28, "fy28e_eps_by_row": eps_by_share,
            "cols_label": "pe_fwd_fy28e", "cols": pes, "values": rows, "house_cell": [0.565, 30.0],
            "price": PRICE, "market_required_fy28e_eps_by_pe": implied_eps}


def solve_implied_share(pe=30.0):
    lo, hi = 0.30, 0.80
    for _ in range(60):
        mid = (lo + hi) / 2
        a = merged("base"); a["share_liver"]["FY28E"] = mid
        v = run(a)["FY28E"]["eps"] * pe
        if v > PRICE: hi = mid
        else: lo = mid
    return round((lo + hi) / 2, 4)


def main():
    out = {}
    for c in CASES:
        a = merged(c); r = run(a); out[c] = {"years": r, "value": value(r, a)}
    base = out["base"]["years"]
    grid1, grid2 = grid_eps27(), grid_value()
    implied = {str(pe): solve_implied_share(pe) for pe in (26.0, 30.0, 35.0)}

    keys = ["donors", "util_liver", "util_heart", "util_lung", "pool_liver", "pool_heart", "pool_lung",
            "share_liver", "share_heart", "share_lung", "cases_liver", "cases_heart", "cases_lung", "trial_cases", "cases_us", "asp",
            "us_liver", "us_heart", "us_lung", "trial", "us_total", "ous", "other", "rev",
            "gp", "gpm", "opex", "op", "opm", "adj_op", "adj_opm", "int_exp", "int_inc", "net_other", "pretax", "tax", "ni",
            "dil_shares", "eps", "adj_eps", "fcf", "cash_end", "cash_end_if_convert_cash_repaid", "q4_rev"]

    def rnd(v):
        return round(v, 4) if isinstance(v, float) else v
    summary = {
        "schema": "tmdx_model_summary@1", "ticker": "TMDX", "asof": FACTS["asof"], "unit": "USD m (eps $/주, asp $m/건)",
        "price": PRICE, "price_date": FACTS["price"]["date"],
        "cases": {c: {"years": {y: {k: rnd(out[c]["years"][y].get(k)) for k in keys if k in out[c]["years"][y]} for y in YEARS},
                      "value_12m": {k: rnd(v) for k, v in out[c]["value"].items()}} for c in out},
        "consensus": {"rev": {"FY26E": CONS["rev_fy26"], "FY27E": CONS["rev_fy27"]}, "adj_eps": {"FY26E": CONS["eps_adj_fy26"], "FY27E": CONS["eps_adj_fy27"]},
                      "source": FACTS["refs"]["CONS_SA"]},
        "vs_consensus_base": {"rev_FY27E": rnd(base["FY27E"]["rev"] / CONS["rev_fy27"] - 1),
                              "adj_eps_FY27E": rnd(base["FY27E"]["adj_eps"] / CONS["eps_adj_fy27"] - 1),
                              "rev_FY26E": rnd(base["FY26E"]["rev"] / CONS["rev_fy26"] - 1)},
        "market_implied_fy28e_liver_share": implied,
        "guidance_check_fy26": {"rev_model": rnd(base["FY26E"]["rev"]), "rev_guide": [764, 774],
                                "adj_opm_model": rnd(base["FY26E"]["adj_opm"]), "adj_opm_guide": [0.125, 0.14]},
        "inputs_base": BASE,
    }
    json.dump(summary, open(os.path.join(HERE, "model_summary.json"), "w"), ensure_ascii=False, indent=1)
    json.dump({"grids": [grid1, grid2], "asof": FACTS["asof"]}, open(os.path.join(HERE, "sensitivity_grid.json"), "w"), ensure_ascii=False, indent=1)

    # 테제 게이트 입력(thesis_check_input@1)
    paths = {}
    for c in out:
        yrs = out[c]["years"]
        paths[c] = {d: {y.replace("FY25", "FY25"): rnd(yrs[y][k]) for y in YEARS if k in yrs[y]}
                    for d, k in (("rev", "rev"), ("op", "op"), ("ni", "ni"), ("eps", "eps"), ("gp", "gp"),
                                 ("liver_share", "share_liver"), ("heart_share", "share_heart"), ("liver_util", "util_liver"),
                                 ("us_cases", "cases_us"), ("donors", "donors"), ("trial_rev", "trial"), ("cash_end", "cash_end"))}
    wb_path = os.path.join(HERE, "tmdx_model.xlsx")
    tci = {"schema": "thesis_check_input@1", "ticker": "TMDX", "asof": FACTS["asof"], "unit": "USD m",
           "anchor_period": "FY25", "periods": YEARS, "case_map": {"base": "base", "bull": "upside", "bear": "downside"},
           "paths": paths, "consensus": {"rev": {"FY26E": CONS["rev_fy26"], "FY27E": CONS["rev_fy27"]}, "eps": {"FY26E": CONS["eps_adj_fy26"], "FY27E": CONS["eps_adj_fy27"]}},
           "sellside_ref": [], "source": {"workbook": "tmdx_model.xlsx", "sha256": None, "built_by": "build_model.py"}}

    write_xlsx(out, summary, grid1, grid2, implied, wb_path)
    tci["source"]["sha256"] = hashlib.sha256(open(wb_path, "rb").read()).hexdigest()[:12]
    json.dump(tci, open(os.path.join(HERE, "thesis_check_input.json"), "w"), ensure_ascii=False, indent=1)

    b = base
    print("BASE  rev", [round(b[y]["rev"], 1) for y in YEARS], "op", [round(b[y]["op"], 1) for y in YEARS],
          "opm", [round(b[y]["opm"], 3) for y in YEARS], "eps", [round(b[y]["eps"], 2) for y in YEARS],
          "adj_eps", [round(b[y].get("adj_eps") or 0, 2) for y in YEARS])
    for c in out:
        v = out[c]["value"]; y = out[c]["years"]
        print(f"{c:9s} rev27 {y['FY27E']['rev']:.1f} rev28 {y['FY28E']['rev']:.1f} eps27 {y['FY27E']['eps']:.2f} eps28 {y['FY28E']['eps']:.2f} "
              f"value {v['value']:.1f} ({v['vs_price']:+.1%})  cash27 {y['FY27E']['cash_end']:.0f}")
    print("liver share", [round(b[y]["share_liver"], 3) for y in YEARS], "heart", [round(b[y]["share_heart"], 3) for y in YEARS])
    print("4Q26E rev", round(b["FY26E"]["q4_rev"], 1), "FY26 adj OPM", round(b["FY26E"]["adj_opm"], 4))
    print("implied FY28E liver share at PE", implied)
    print("vs consensus", summary["vs_consensus_base"])


def write_xlsx(out, summary, grid1, grid2, implied, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = Workbook()
    blue, bold = Font(color="1F4FBF"), Font(bold=True)
    hdr = PatternFill("solid", fgColor="E8E8E8")
    ws = wb.active; ws.title = "README"
    lines = [
        "TMDX P×Q 모델 (equity-analysis S2) — 기준일 " + FACTS["asof"],
        "Q = 사망 기증자 × 기증자당 이식(활용률) × TMDX 점유율 (+ 임상 케이스), P = 미국 케이스당 매출(장기 공통 가정).",
        "2025A 는 SEC 10-K, 2026 9M 은 3Q26 10-Q, 4Q26E 는 가이던스(764~774M) 중간값에 닻. 2027~28E 는 INPUTS 시트의 판단값.",
        "EPS 는 회사 공시와 같은 if-converted(전환사채 489만 주 포함 + 세후 이자 가산). 비GAAP(adj) EPS 는 컨센 대조용.",
        "파란 글씨 = 판단 입력(build_model.py 의 BASE/CASES 딕셔너리가 정본). 숫자를 바꾸려면 스크립트를 고치고 다시 돌린다.",
        "원장: ../sources/primary_facts.json (등급 ①②③, 원문 accession 번호 포함).",
        "장기별 ASP: 2025 장기별 매출(①) ÷ 회사가 4Q25 콜에서 밝힌 장기별 케이스(간 4,197·심장 854·폐 88, ②) — 이후 연 +1%. 2026 이후 장기별 케이스는 미공시(매출÷ASP 역산). 2026 연간 기증자는 3Q26 −6% 만 확인(미측정 — OPTN 월간).",
    ]
    for i, t in enumerate(lines, 1): ws.cell(i, 1, t)
    ws.column_dimensions["A"].width = 140

    # Inputs
    wi = wb.create_sheet("Inputs")
    wi.append(["입력", "FY26E", "FY27E", "FY28E", "메모"]); [setattr(c, "fill", hdr) for c in wi[1]]
    memo = {"donor_growth": "25A −2.5%(UNOS), 3Q26 −6%(콜). TMDX 가 못 바꾸는 역풍", "util_liver": "25A 0.703(사망 기증 간 11,635 ÷ 기증자 16,550)",
            "share_liver": "25A 34.7%(매출÷ASP 역산), 26E 는 실적 닻", "opex_growth": "R&D 분기 ~29M 안정(콜), 유럽 NOP·본사 이전", "gm": "회사: 단·중기 지금 수준"}
    for k, v in BASE.items():
        if isinstance(v, dict) and all(isinstance(x, (int, float)) for x in v.values()):
            wi.append([k, v.get("FY26E"), v.get("FY27E"), v.get("FY28E"), memo.get(k, "")])
        elif isinstance(v, dict):
            wi.append([k, json.dumps(v, ensure_ascii=False), None, None, "4Q26E 분기 추정"])
        else:
            wi.append([k, v, None, None, ""])
    for row in wi.iter_rows(min_row=2, max_col=4, min_col=2):
        for c in row: c.font = blue
    wi.column_dimensions["A"].width = 22; wi.column_dimensions["B"].width = 18; wi.column_dimensions["E"].width = 60

    labels = [("donors", "사망 기증자(명)"), ("util_liver", "기증자당 간 이식"), ("util_heart", "기증자당 심장 이식"), ("util_lung", "기증자당 폐 이식"),
              ("pool_liver", "사망 기증 간 이식(풀)"), ("pool_heart", "심장 풀"), ("pool_lung", "폐 풀"),
              ("share_liver", "TMDX 간 점유율"), ("share_heart", "TMDX 심장 점유율"), ("share_lung", "TMDX 폐 점유율"),
              ("cases_liver", "간 케이스"), ("cases_heart", "심장 케이스"), ("cases_lung", "폐 케이스"), ("trial_cases", "임상 케이스(Part B·DENOVO)"),
              ("cases_us", "미국 케이스 합"), ("asp", "케이스당 매출($M)"),
              ("us_liver", "미국 간 매출"), ("us_heart", "미국 심장 매출"), ("us_lung", "미국 폐 매출"), ("trial", "임상 매출"), ("us_total", "미국 이식 매출"),
              ("ous", "해외 이식 매출"), ("other", "비이식 서비스(PAD 전세 등)"), ("rev", "총매출"),
              ("gp", "매출총이익"), ("gpm", "GPM"), ("opex", "영업비용"), ("op", "영업이익(GAAP)"), ("opm", "OPM"), ("adj_op", "조정 영업이익"), ("adj_opm", "조정 OPM"),
              ("int_exp", "이자비용"), ("int_inc", "이자수익 등"), ("net_other", "영업외 순"), ("pretax", "세전이익"), ("tax", "법인세"), ("ni", "순이익"),
              ("dil_shares", "희석 주식수(백만, if-converted)"), ("eps", "희석 EPS(GAAP)"), ("adj_eps", "조정 EPS(컨센 비교용)"),
              ("fcf", "FCF(간이)"), ("cash_end", "기말 현금"), ("cash_end_if_convert_cash_repaid", "기말 현금(전환사채 현금 상환 시)")]
    for c in out:
        wsx = wb.create_sheet({"base": "Base", "downside": "Downside", "upside": "Upside"}[c])
        wsx.append(["항목"] + YEARS); [setattr(x, "fill", hdr) for x in wsx[1]]
        yrs = out[c]["years"]
        for k, lab in labels:
            row = [lab] + [yrs[y].get(k) for y in YEARS]
            wsx.append(row)
        v = out[c]["value"]
        wsx.append([]); wsx.append(["12개월 케이스 값", f"FY28E EPS {v['eps_fwd_12m']:.2f} × P/E {v['pe']:.0f} = ${v['value']:.1f} (현재가 {PRICE} 대비 {v['vs_price']:+.1%})"])
        wsx.column_dimensions["A"].width = 34
        for col in "BCDE": wsx.column_dimensions[col].width = 13
        for row in wsx.iter_rows(min_row=2, min_col=2, max_col=5):
            for x in row:
                if isinstance(x.value, float):
                    x.number_format = "0.0%" if abs(x.value) < 1.5 and x.row in (3, 4, 5, 9, 10, 11, 27, 30, 32) else "#,##0.00"

    # Sensitivity
    wsn = wb.create_sheet("Sensitivity")
    for g in (grid1, grid2):
        wsn.append([g["name"]]); wsn.cell(wsn.max_row, 1).font = bold
        wsn.append([f"{g['rows_label']} \\ {g['cols_label']}"] + g["cols"])
        for rv, vals in zip(g["rows"], g["values"]):
            wsn.append([rv] + vals)
        wsn.append(["하우스 칸", str(g["house_cell"])])
        if "market_required_fy28e_eps_by_pe" in g:
            wsn.append(["시장 요구 칸(현재가 ÷ P/E = 필요한 FY28E EPS)", json.dumps(g["market_required_fy28e_eps_by_pe"])])
            wsn.append(["현재가가 내재한 FY28E 간 점유율(P/E별)", json.dumps(implied)])
        wsn.append([])
    wsn.column_dimensions["A"].width = 46

    # Quarterly history
    wq = wb.create_sheet("Quarterly_hist")
    qh = FACTS["us_transplant_revenue_by_organ_quarterly"]
    wq.append(["미국 장기별 이식 매출($M, 10-Q)"] + qh["columns"])
    for k in ("liver", "heart", "lung", "us_total"):
        wq.append([k] + qh[k])
    tot = FACTS["total_revenue_quarterly"]
    wq.append(["총매출"] + tot["total"])
    wq.append([])
    wq.append(["간 QoQ"] + [None] + [round(qh["liver"][i] / qh["liver"][i - 1] - 1, 3) for i in range(1, len(qh["liver"]))])
    wq.append(["간 YoY"] + [None] * 4 + [round(qh["liver"][i] / qh["liver"][i - 4] - 1, 3) for i in range(4, len(qh["liver"]))])
    wq.append(["심장 YoY"] + [None] * 4 + [round(qh["heart"][i] / qh["heart"][i - 4] - 1, 3) for i in range(4, len(qh["heart"]))])
    wq.column_dimensions["A"].width = 30
    wb.save(path)


if __name__ == "__main__":
    main()
