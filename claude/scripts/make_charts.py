"""HD현대마린엔진 바이더딥 피치용 핵심 도표 6종 (SMIC 팔레트 미리보기 PNG + 원자료 엑셀).
입력: 스크래치 데이터 폴더(네이버 일봉, WiseReport 컨센, Comtrade, DART 파싱, 환율). 사용: python3 make_charts.py <data_dir> <raw_dir> <out_dir>"""
import json, sys, os, datetime as dt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import koreanize_matplotlib  # noqa: F401  (NanumGothic)
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
data, raw, out = sys.argv[1], sys.argv[2], sys.argv[3]
RED, PINK, LPINK, DGRAY, GRAY, LGRAY = "#C00000", "#FF7F7F", "#FFBFBF", "#595959", "#7F7F7F", "#D0CECE"
plt.rcParams.update({"font.size": 8, "font.weight": "bold", "axes.edgecolor": GRAY, "axes.labelcolor": DGRAY,
                     "xtick.color": DGRAY, "ytick.color": DGRAY, "xtick.direction": "out", "ytick.direction": "out",
                     "axes.spines.top": False, "legend.frameon": False})
SIZE = (9.25 / 2.54, 5.1 / 2.54)
from matplotlib.ticker import FuncFormatter
COMMA = FuncFormatter(lambda v, _: f"{v:,.0f}")
def fig_ax():
    f, a = plt.subplots(figsize=SIZE, dpi=300); a.yaxis.set_major_formatter(COMMA); a.spines["right"].set_visible(False); return f, a
def finish(f, name):
    f.tight_layout(pad=0.3); f.savefig(f"{out}/{name}.png", dpi=300); plt.close(f)
wb = Workbook(); idx = wb.active; idx.title = "도표목록"
idx.append(["도표", "제목(Key message)", "출처", "시트"])
def sheet(name, title, src, header, rows):
    ws = wb.create_sheet(name); ws.append([title]); ws.append([f"출처: {src}"]); ws.append([])
    ws.append(header)
    for r in rows: ws.append(r)
    ws["A1"].font = Font(bold=True, color="C00000", size=12)
    for c in ws[4]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="595959"); c.alignment = Alignment(horizontal="center")
    idx.append([name, title, src, name])
# ---------- 도표1: 주가 vs 27E OP 컨센 ----------
px = [d for d in json.load(open(f"{data}/px/071970.json")) if d.get("closePrice")]
me = {}
for d in px: me[d["localDate"][:6]] = d["closePrice"]
cons = json.load(open(f"{data}/cons/071970_202712.json")); c2 = json.loads(cons["chart2"])
op27 = {k.replace("/", "")[:6]: v for k, v in zip(c2["categories"], c2["avg"])}
months = sorted(me)
f, a = fig_ax(); a2 = a.twinx(); a2.spines["top"].set_visible(False); a2.yaxis.set_major_formatter(COMMA)
xs = list(range(len(months)))
a.plot(xs, [me[m] / 1000 for m in months], color=GRAY, lw=1.5, marker="o", ms=3, mfc=GRAY, label="주가(LHS, 천 원)")
ox = [i for i, m in enumerate(months) if m in op27]
a2.plot(ox, [op27[months[i]] for i in ox], color=RED, lw=1.5, marker="o", ms=3, mfc=RED, label="27E 영업이익 컨센(RHS, 억 원)")
a.set_xticks(xs[::3]); a.set_xticklabels([f"{m[2:4]}.{m[4:]}" for m in months[::3]])
a.set_ylim(0, 130); a2.set_ylim(0, 2600)
a.annotate(f"{me[months[-1]]/1000:.1f}", (xs[-1], me[months[-1]] / 1000), textcoords="offset points", xytext=(-8, -11), color=GRAY, fontsize=7)
a2.annotate(f"{op27[months[-1]]:,.0f}", (xs[-1], op27[months[-1]]), textcoords="offset points", xytext=(-14, 5), color=RED, fontsize=7)
h1, l1 = a.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels()
a.legend(h1 + h2, l1 + l2, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=6.5, handlelength=1.5)
finish(f, "도표1_주가vs27E영업이익컨센")
sheet("도표1", "주가는 25년 초로 돌아갔는데, 27E 영업이익 컨센은 1년간 +26% 올랐다", "네이버 일봉(월말 종가), WiseReport 컨센 이력(cF5002, 월말)",
      ["월", "월말 종가(원)", "27E 영업이익 컨센(억 원)"], [[f"{m[:4]}.{m[4:]}", me[m], round(op27[m], 1) if m in op27 else None] for m in months])
# ---------- 도표2: Comtrade ----------
ca = json.load(open(f"{data}/comtrade_840810_annual.json"))
yrs = sorted(ca); w = [ca[y]["0"] / 1e6 for y in yrs]; c = [ca[y]["156"] / 1e6 for y in yrs]; sh = [c[i] / w[i] * 100 for i in range(len(yrs))]
f, a = fig_ax(); a2 = a.twinx(); a2.spines["top"].set_visible(False); a2.yaxis.set_major_formatter(COMMA)
xs = list(range(len(yrs)))
a.bar([x - 0.2 for x in xs], [w[i] - c[i] for i in range(len(yrs))], width=0.4, color=LGRAY, label="기타 국가(LHS, 백만 달러)")
a.bar([x + 0.2 for x in xs], c, width=0.4, color=RED, label="중국향(LHS, 백만 달러)")
a2.plot(xs, sh, color=GRAY, lw=1.5, marker="o", ms=3, label="중국 비중(RHS, %)")
a.set_xticks(xs); a.set_xticklabels([y[2:] for y in yrs]); a.set_ylim(0, 1400); a2.set_ylim(0, 100)
a.annotate(f"{c[-1]:,.0f}", (xs[-1] + 0.2, c[-1]), textcoords="offset points", xytext=(-10, 3), color=RED, fontsize=7)
a2.annotate(f"{sh[-1]:.0f}%", (xs[-1], sh[-1]), textcoords="offset points", xytext=(-14, 4), color=GRAY, fontsize=7)
h1, l1 = a.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels()
a.legend(h1 + h2, l1 + l2, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=6, handlelength=1.2)
finish(f, "도표2_한국선박엔진수출_중국비중")
sheet("도표2", "한국 선박엔진(HS 840810) 수출의 91%가 중국으로 간다: 배는 중국이, 심장은 한국이", "UN Comtrade (reporter 410, flow X, HS 840810)",
      ["연도", "세계(USD)", "중국(USD)", "중국 비중(%)"], [[y, ca[y]["0"], ca[y]["156"], round(ca[y]["156"] / ca[y]["0"] * 100, 1)] for y in yrs])
# ---------- 도표3: DART 수주 지역 ----------
rows = json.load(open(f"{raw}/dart_hdme_contracts_parsed.json"))
agg = {}
for r in rows:
    if r["corr"] or not r["amt_bn"]: continue
    y = r["date"][:4]; k = "중국" if (r["region"] and "중국" in r["region"]) else "국내·기타"
    agg.setdefault(y, {"중국": 0, "국내·기타": 0})[k] += r["amt_bn"]
ys = sorted(agg); cn = [agg[y]["중국"] for y in ys]; kr = [agg[y]["국내·기타"] for y in ys]
f, a = fig_ax(); xs = list(range(len(ys)))
a.bar(xs, kr, width=0.5, color=LGRAY, label="국내·기타(억 원)"); a.bar(xs, cn, width=0.5, bottom=kr, color=RED, label="중국 조선소(억 원)")
for i in xs:
    a.annotate(f"{kr[i]+cn[i]:,.0f}", (i, kr[i] + cn[i]), textcoords="offset points", xytext=(0, 2), ha="center", color=DGRAY, fontsize=7)
    shr = cn[i] / (kr[i] + cn[i])
    if shr >= 0.15: a.annotate(f"중국 {shr*100:.0f}%", (i, kr[i] + cn[i] / 2), ha="center", va="center", color="white", fontsize=6.5)
    else: a.annotate(f"중국 {shr*100:.0f}%", (i, kr[i] / 2), ha="center", va="center", color=DGRAY, fontsize=6.5)
a.set_xticks(xs); a.set_xticklabels([("26(~11/9)" if y == "2026" else y[2:]) for y in ys]); a.set_ylim(0, 11000)
a.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=6.5)
finish(f, "도표3_공시수주_지역별")
sheet("도표3", "26년 수주는 +56%, 그중 62%가 중국 조선소: 한국 조선소 둔화를 중국으로 메웠다", "DART 단일판매·공급계약체결 50건 전수(정정 제외)",
      ["연도", "국내·기타(억 원)", "중국(억 원)", "합계(억 원)", "중국 비중(%)"], [[y, round(agg[y]["국내·기타"], 1), round(agg[y]["중국"], 1), round(sum(agg[y].values()), 1), round(agg[y]["중국"] / sum(agg[y].values()) * 100, 1)] for y in ys])
# ---------- 도표4: 잔고 & ASP ----------
lab = ["24", "25", "26.3Q"]; bl = [7390, 10889, 17311]; asp = [44.19, 51.35, 63.94]; units = [54.3, 61.9, 61.1]
f, a = fig_ax(); a2 = a.twinx(); a2.spines["top"].set_visible(False); a2.yaxis.set_major_formatter(COMMA); xs = [0, 1, 2]
a.bar(xs, bl, width=0.5, color=[LGRAY, LGRAY, RED], label="수주잔고(LHS, 억 원)")
a2.plot(xs, asp, color=GRAY, lw=1.5, marker="o", ms=3, label="엔진 대당 평균 매출액(RHS, 억 원)")
for i, v in enumerate(bl): a.annotate(f"{v:,}", (i, v), textcoords="offset points", xytext=(0, 2), ha="center", color=(RED if i == 2 else DGRAY), fontsize=7)
for i, v in enumerate(asp): a2.annotate(f"{v:.1f}", (i, v), textcoords="offset points", xytext=(0, 5), ha="center", color=GRAY, fontsize=7)
a.set_xticks(xs); a.set_xticklabels(["24말", "25말", "26.9말"]); a.set_ylim(0, 26000); a2.set_ylim(-60, 75); a2.set_yticks([40, 50, 60, 70])
h1, l1 = a.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels()
a.legend(h1 + h2, l1 + l2, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=6.3)
finish(f, "도표4_수주잔고_대당매출")
sheet("도표4", "잔고는 연초 대비 +53%, 엔진 대당 매출은 +24.5%: 27~28년 이익은 이미 잠겨 있다", "HD현대마린엔진 분기보고서(2026.09) 사업의 내용(수주상황·가격변동), 사업보고서",
      ["구분", "기말 수주잔고(억 원)", "엔진 대당 평균 매출액(억 원)", "인도 대수 환산(대)"], [[l, b, p, u] for l, b, p, u in zip(["2024", "2025", "2026.9M"], bl, asp, units)] + [["주", "25말 잔고는 사업보고서 기준 10,889억. 26년 분기보고서는 기초를 11,277억으로 재평가(외화계약 환율 반영)", None, None], ["주", "25년 신규수주 7,347억(연간) vs 26년 9M 신규수주 10,538억", None, None]])
# ---------- 도표5: 역산 ----------
labs = ["24A", "25A", "26E", "27E", "28E"]; ops = [332, 759, 1655, 2199, 2664]
f, a = fig_ax(); xs = list(range(len(labs)))
a.bar(xs, ops, width=0.5, color=[LGRAY, LGRAY, PINK, RED, PINK], label="영업이익(억 원, 26~28E 컨센)")
a.axhline(740, color=GRAY, lw=1.5, ls="--", label="현재가 내재 영구 영업이익 740억")
for i, v in enumerate(ops): a.annotate(f"{v:,}", (i, v), textcoords="offset points", xytext=(0, 2), ha="center", color=(RED if i == 3 else DGRAY), fontsize=7)
a.set_xticks(xs); a.set_xticklabels(labs); a.set_ylim(0, 3200)
a.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=6.3)
finish(f, "도표5_역산_내재이익")
sheet("도표5", "현재 EV(5,923억)는 2025년 영업이익(759억)이 영구히 이어진다는 가정과 같다", "WiseReport 컨센(11/20), 분기보고서 재무상태표. 가정: WACC 10%, 세율 20%, 무성장",
      ["연도", "영업이익(억 원)", "비고"], [["2024A", 332, "실적"], ["2025A", 759, "실적"], ["2026E", 1655, "컨센"], ["2027E", 2199, "컨센"], ["2028E", 2664, "컨센"], ["내재 영구 OP", 740, "EV 5,923억 × 10% ÷ (1-20%)"]])
# ---------- 도표6: 환율 vs 헤지 ----------
fx = json.load(open(f"{data}/fx.json"))["FX_USDKRW"]
fx = [(d, v) for d, v in fx if d >= "2025-01-01"]
f, a = fig_ax()
a.plot(range(len(fx)), [v for _, v in fx], color=GRAY, lw=1.2, label="USD/KRW 고시환율(원)")
a.axhline(1447.96, color=RED, lw=1.5, ls="--", label="선물환 가중평균 약정환율 1,448원")
ticks = [i for i, (d, _) in enumerate(fx) if d[5:] in ("01-02", "04-01", "07-01", "10-01") or (d[8:10] <= "03" and d[5:7] in ("01", "04", "07", "10"))]
seen = set(); tk = []
for i in ticks:
    k = fx[i][0][:7]
    if k not in seen: seen.add(k); tk.append(i)
a.set_xticks(tk); a.set_xticklabels([f"{fx[i][0][2:4]}.{fx[i][0][5:7]}" for i in tk]); a.set_ylim(1250, 1600)
a.annotate(f"{fx[-1][1]:,.0f}", (len(fx) - 1, fx[-1][1]), textcoords="offset points", xytext=(4, -3), color=GRAY, fontsize=7)
a.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=6.3)
finish(f, "도표6_환율vs헤지")
sheet("도표6", "원화 강세(1,347원)는 선물환 4.33억$(평균 1,448원, 평균만기 27.11)로 27년까지 막혀 있다", "네이버 하나은행 고시환율, HD현대마린엔진 분기보고서 파생상품 주석",
      ["일자", "USD/KRW"], [[d, v] for d, v in fx])
wb.save(f"{out}/HD현대마린엔진_도표원자료_2026-11-23.xlsx")
print("ok")
