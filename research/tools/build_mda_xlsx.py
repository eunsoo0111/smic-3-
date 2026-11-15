# -*- coding: utf-8 -*-
import re, sys, math
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import PageSetupProperties
import mda_data as D

OUT = sys.argv[1]
FONT = "Malgun Gothic"
C_TITLE, C_HEAD, C_TEXT, C_SUB = "18354A", "24627C", "173044", "586B79"
C_BAND = ["EDF4F7", "F5F7F8"]
C_FACT, C_INTERP, C_FIX, C_RAW = "275F69", "5E5590", "9B5E1C", "17684F"
LINE = Side(style="thin", color="D5E0E6")
TOP = Side(style="medium", color="8DA8B5")

def fill(c): return PatternFill("solid", fgColor=c)
def font(color=C_TEXT, bold=False, size=10): return Font(name=FONT, size=size, bold=bold, color=color)
WRAP = Alignment(vertical="center", wrap_text=True)
CENTER = Alignment(vertical="center", horizontal="center", wrap_text=True)
RIGHT = Alignment(vertical="center", horizontal="right", wrap_text=True)

def width_units(s):
    return sum(2.0 if ord(ch) > 0x2E80 else 1.05 for ch in str(s))

def row_height(values, widths, base=16.5, minimum=30):
    lines = 1
    for v, w in zip(values, widths):
        if v is None: continue
        per = max(4.0, w * 0.88)
        n = sum(max(1, math.ceil(width_units(part) / per)) for part in str(v).split("\n"))
        lines = max(lines, n)
    return max(minimum, lines * base + 10)

def sheet(wb, name, title, subtitle, headers, widths, freeze):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = C_HEAD
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    n = len(headers)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=n)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=n)
    ws["A1"] = title; ws["A1"].font = font("FFFFFF", True, 17); ws["A1"].alignment = WRAP
    for c in range(1, n + 1): ws.cell(1, c).fill = fill(C_TITLE)
    ws["A2"] = subtitle; ws["A2"].font = font(C_SUB); ws["A2"].alignment = WRAP
    ws.row_dimensions[1].height = 34; ws.row_dimensions[2].height = 35; ws.row_dimensions[3].height = 9
    for c, h in enumerate(headers, 1):
        cell = ws.cell(4, c, h); cell.font = font("FFFFFF", True); cell.fill = fill(C_HEAD); cell.alignment = WRAP
    ws.row_dimensions[4].height = 28
    ws.freeze_panes = freeze
    ws.page_setup.orientation = 'landscape'; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.print_title_rows = '4:4'
    return ws

def body(ws, r, c, v, color=C_TEXT, bg="FFFFFF", align=WRAP, top=False, size=10, fmt=None, bold=False):
    cell = ws.cell(r, c, v)
    cell.font = font(color, bold, size); cell.fill = fill(bg); cell.alignment = align
    cell.border = Border(top=TOP if top else None, bottom=LINE)
    if fmt: cell.number_format = fmt
    return cell

SRC_IDS = {s[0] for s in D.SOURCES}
used = set()
def check_src(s, where):
    for tok in re.split(r"[;,]\s*", s):
        tok = tok.strip()
        if not tok or tok == "계산": continue
        if tok not in SRC_IDS: raise SystemExit(f"unknown source {tok!r} in {where}")
        used.add(tok)

def ev_color(kind):
    if kind in ("수정 필요", "추가 확인"): return C_FIX
    if kind == "리서치 해석": return C_INTERP
    return C_FACT

wb = Workbook(); wb.remove(wb.active)
n_rows = sum(len(l[4]) for l in D.L)
n_met = len(D.M)

# ------------------------------------------------------------ 1. layer map
ws = sheet(wb, "층위 지도", "MDA Space | 리서치의 층위",
    f"{n_rows + n_met}개 재료·지표 = 논리 재료 {n_rows}행 + 지표 {n_met}행 · 분기 시계열 {len(D.Q)}개 분기 · 출처 {len(D.SOURCES)}개 · 기준 {D.AS_OF} · 통화는 별도 표기가 없으면 C$",
    ["층위", "조사 영역", "이 층위에서 답하는 질문", "보고서에서의 역할", "재료 수", "재료 ID"],
    [25.6, 33.1, 58.1, 30.0, 11.5, 20.5], "A5")
last_mat = 4 + n_rows
rid = 1; r = 5
for i, (l1, l2, q, place, rows) in enumerate(D.L):
    vals = [l1, l2, q, place, f"=COUNTIFS('리서치 재료'!$B$5:$B${last_mat},A{r},'리서치 재료'!$C$5:$C${last_mat},B{r})", f"R{rid:03d}–R{rid + len(rows) - 1:03d}"]
    for c, v in enumerate(vals, 1):
        body(ws, r, c, v, bg=C_BAND[0] if c <= 2 else "FFFFFF", align=CENTER if c >= 5 else WRAP)
    ws.row_dimensions[r].height = row_height(vals[:4], [25.6, 33.1, 58.1, 30.0], minimum=36)
    rid += len(rows); r += 1
r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
for c in range(1, 7): ws.cell(r, c).fill = fill(C_HEAD)
ws.cell(r, 1, "읽는 순서와 근거 구분").font = font("FFFFFF", True); ws.cell(r, 1).alignment = WRAP
ws.row_dimensions[r].height = 28; r += 1
GUIDE = [
 ("핵심 결론", "시장은 MDA의 위성 공장이 2029년이면 빈다고 본다(상업 고객 Telesat·Globalstar 물량 소진). 우리 가설은 그 공장을 국가가 채운다는 것이다. 투자포인트 1은 캐나다(ESCP-P MEO, RADARSAT), 투자포인트 2는 해외 소버린 사업의 탑재체 납품과 인수(BCT·CLS)를 통한 현지화다. 승부처는 2027~28년 신규 위성 수주가 연 약 1B의 상업 롤오프를 메우느냐다."),
 ("가장 약한 고리", "'소버린 시장에서 MDA 점유율이 커진다'는 지금 증거로는 약하다. 소버린 사업의 프라임은 자국 기업이 가져가고(제조 가치의 약 70%가 자국 캡티브, 열린 몫 7%), MDA는 캐나다 밖에서 프라임을 딴 적이 없다. 점유율 대신 '돈 내는 주체가 상업에서 정부로 바뀐다'로 쓴다."),
 ("확인 사실 / 회사 발표", "공시·정부 발표로 확인한 것과 회사가 말한 것을 나눴다. 설계 용량, 파이프라인, ATP, MOU는 실적이 아니다."),
 ("경영진 설명 / 전망", "3Q26 컨퍼런스콜 전사본(Motley Fool) 기준. 일부 문장이 깨져 있어 인용 전에 음성과 대조한다."),
 ("보도 / 외부 추정", "업계 매체와 Novaspace 인용치. 원보고서는 유료라 읽지 못했다. 전망치 인용은 최소로 한다."),
 ("리서치 해석 / 직접 계산", "사실에서 끌어낸 연결 논리와 계산값. 브랜치 노트(N02·N03)의 계산은 원 계약으로 다시 검증한 뒤 쓴다."),
 ("추가 확인 / 수정 필요", "출처마다 엇갈리는 숫자와 기억으로 적은 서술. 층위 17에 모았다. 보고서에 넣기 전에 반드시 정리한다."),
 ("찾는 방법", "「리서치 재료」에서 층위·근거·배치로 필터 → 출처 ID 확인 → 「출처」의 원문. 수치는 「지표 원장」, 차트용 데이터는 「분기 시계열」. 초록색 숫자는 원자료, 검은색은 수식 계산."),
 ("범위", "이 세션의 조사, 붙여 넣은 문답 6건, 저장소 다른 브랜치의 MDA 노트 4개를 합쳤다. 다른 종목(BlackSky, TransMedics 등) 자료는 넣지 않았다."),
]
for k, v in GUIDE:
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
    body(ws, r, 1, k, bg=C_BAND[0])
    body(ws, r, 2, v)
    for c in range(3, 7): ws.cell(r, c).border = Border(bottom=LINE)
    ws.row_dimensions[r].height = row_height([v], [150], minimum=34)
    r += 1

# ------------------------------------------------------------ 2. materials
W2 = [7.2, 19.0, 20.5, 19.0, 13.5, 57.5, 47.0, 19.0, 18.0]
ws = sheet(wb, "리서치 재료", "MDA Space | 리서치 재료",
    f"정리 기준 {D.AS_OF} · {n_rows}개 재료 · 한 행에 주장 하나 · 층위·근거·배치·출처로 필터 · 출처 ID의 원문은 「출처」 시트 · 금액은 별도 표기가 없으면 C$ 백만",
    ["ID", "1층 · 대분류", "2층 · 조사 영역", "3층 · 세부 주제", "근거 구분", "재료 · 관찰한 내용", "의미 · 적용 범위", "보고서 배치", "출처 ID"],
    W2, "C5")
r = 5; rid = 1
for i, (l1, l2, q, place, rows) in enumerate(D.L):
    band = C_BAND[i % 2]
    for j, (topic, kind, text, mean, src) in enumerate(rows):
        check_src(src, f"R{rid:03d}")
        vals = [f"R{rid:03d}", l1, l2, topic, kind, text, mean, place, src]
        for c, v in enumerate(vals, 1):
            body(ws, r, c, v, color=ev_color(kind) if c == 5 else C_TEXT, bg=band if c in (2, 3) else "FFFFFF", top=(j == 0))
        ws.row_dimensions[r].height = row_height(vals, W2)
        r += 1; rid += 1
ws.auto_filter.ref = f"A4:I{r - 1}"

# ------------------------------------------------------------ 3. metrics
W3 = [7.2, 14.5, 32.5, 20.0, 13.5, 11.0, 13.5, 46.0, 12.0]
ws = sheet(wb, "지표 원장", "MDA Space | 지표 원장",
    f"{n_met}개 지표 · 금액은 C$ 백만(m)이 기본이고 다른 통화는 단위에 표기 · 초록색 숫자는 원자료, 검은색은 이 시트 안의 수식 계산 · 전망은 발표 시점을 유지",
    ["ID", "분류", "지표", "기간 · 기준", "값", "단위", "성격", "해석 · 주의점", "출처 ID"],
    W3, "D5")
row_of = {key: 5 + i for i, (key, *_) in enumerate(D.M)}
prev_cat = None
for i, (key, cat, name, period, val, unit, kind, note, src, fmt) in enumerate(D.M):
    r = 5 + i
    check_src(src, key)
    is_formula = isinstance(val, str) and val.startswith("=")
    if is_formula:
        val = re.sub(r"\{(\w+)\}", lambda mo: f"E{row_of[mo.group(1)]}", val)
    vals = [f"M{i + 1:03d}", cat, name, period, val, unit, kind, note, src]
    for c, v in enumerate(vals, 1):
        if c == 5:
            body(ws, r, c, v, color=C_TEXT if is_formula else C_RAW, align=RIGHT, top=(cat != prev_cat), fmt=fmt)
        else:
            body(ws, r, c, v, bg=C_BAND[1] if c == 2 else "FFFFFF", top=(cat != prev_cat))
    ws.row_dimensions[r].height = row_height([name, period, note], [32.5, 20.0, 46.0], minimum=26)
    prev_cat = cat
ws.auto_filter.ref = f"A4:I{4 + n_met}"

# ------------------------------------------------------------ 4. quarterly
HQ = ["분기", "매출", "Satellite Systems", "Robotics & Space Ops", "Geointelligence", "조정 EBITDA", "수주", "기말 잔고",
      "조정 EBITDA 마진", "수주/매출", "매출 YoY", "잔고/직전 4분기 매출", "비고"]
W4 = [10.5, 11.5, 13.5, 13.5, 14.5, 12.5, 11.5, 12.5, 12.5, 11.0, 11.0, 13.5, 52.0]
ws = sheet(wb, "분기 시계열", "MDA Space | 분기 시계열",
    f"2022Q1~2026Q3 · C$ 백만 · 분기 실적 릴리스에서 추출한 값(브랜치 노트 N02의 quarterly.csv, 4Q 사업부는 FY2025 릴리스로 보완) · 오른쪽 4개 열은 수식 · 차트는 이 표에서 바로 그린다",
    HQ, W4, "B5")
N1, P1, X2 = D.N1, D.P1, D.X2
for i, (q, rev, ss, ro, ge, eb, bk, bl, note) in enumerate(D.Q):
    r = 5 + i
    raw = [q, rev, ss, ro, ge, eb, bk, bl]
    for c, v in enumerate(raw, 1):
        if c == 1: body(ws, r, c, v, bg=C_BAND[0], top=q.endswith("Q1"))
        else: body(ws, r, c, v, color=C_RAW, align=RIGHT, fmt=N1, top=q.endswith("Q1"))
    body(ws, r, 9, f"=F{r}/B{r}", align=RIGHT, fmt=P1, top=q.endswith("Q1"))
    body(ws, r, 10, f"=G{r}/B{r}", align=RIGHT, fmt=X2, top=q.endswith("Q1"))
    body(ws, r, 11, f"=B{r}/B{r - 4}-1" if i >= 4 else None, align=RIGHT, fmt=P1, top=q.endswith("Q1"))
    body(ws, r, 12, f"=H{r}/SUM(B{r - 3}:B{r})" if i >= 3 else None, align=RIGHT, fmt=X2, top=q.endswith("Q1"))
    body(ws, r, 13, note, top=q.endswith("Q1"))
    ws.row_dimensions[r].height = row_height([note], [52.0], minimum=22)
end = 4 + len(D.Q)
r = end + 2
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=13)
for c in range(1, 14): ws.cell(r, c).fill = fill(C_HEAD)
ws.cell(r, 1, "연간 합계 (위 표에서 수식으로 집계)").font = font("FFFFFF", True); ws.cell(r, 1).alignment = WRAP
ws.row_dimensions[r].height = 24; r += 1
for c, h in enumerate(["연도", "매출", "", "", "", "조정 EBITDA", "수주", "기말 잔고", "조정 EBITDA 마진", "수주/매출", "매출 YoY", "잔고/매출", "비고"], 1):
    cell = ws.cell(r, c, h); cell.font = font(C_TEXT, True); cell.fill = fill(C_BAND[0]); cell.alignment = WRAP
r += 1
first_year_row = r
for y, a, b in [("2022", 5, 8), ("2023", 9, 12), ("2024", 13, 16), ("2025", 17, 20), ("2026 (9개월)", 21, 23)]:
    body(ws, r, 1, y, bg=C_BAND[0])
    body(ws, r, 2, f"=SUM(B{a}:B{b})", align=RIGHT, fmt=N1)
    for c in (3, 4, 5): body(ws, r, c, None)
    body(ws, r, 6, f"=SUM(F{a}:F{b})", align=RIGHT, fmt=N1)
    body(ws, r, 7, f"=SUM(G{a}:G{b})", align=RIGHT, fmt=N1)
    body(ws, r, 8, f"=H{b}", align=RIGHT, fmt=N1)
    body(ws, r, 9, f"=F{r}/B{r}", align=RIGHT, fmt=P1)
    body(ws, r, 10, f"=G{r}/B{r}", align=RIGHT, fmt=X2)
    body(ws, r, 11, f"=B{r}/B{r - 1}-1" if (r > first_year_row and not y.startswith("2026")) else None, align=RIGHT, fmt=P1)
    body(ws, r, 12, f"=H{r}/B{r}" if not y.startswith("2026") else None, align=RIGHT, fmt=X2)
    body(ws, r, 13, "9개월 누계. 연간 지표와 직접 비교하지 않는다." if y.startswith("2026") else "")
    ws.row_dimensions[r].height = 22
    r += 1

# ------------------------------------------------------------ 5. sources
W5 = [8.5, 40.0, 16.0, 16.0, 62.0, 55.6]
ws = sheet(wb, "출처", "MDA Space | 출처와 사용 범위",
    "F = 회사 공시·IR, T = 콜 전사본, G = 정부, W = 매체·타사 자료, N = 리서치 노트·팀 자료 · 웹 자료는 조사 시점에 확인한 목록이며 실시간 갱신이 아님 · '브랜치 노트 경유'는 원문을 이번에 직접 읽지 않았다는 뜻",
    ["ID", "자료명", "자료 성격", "발표 · 기준일", "원문 URL 또는 저장소 경로", "사용 범위 · 주의"],
    W5, "A5")
for i, (sid, name, kind, date, url, note) in enumerate(D.SOURCES):
    r = 5 + i
    vals = [sid, name, kind, date, url, note]
    for c, v in enumerate(vals, 1):
        cell = body(ws, r, c, v, color=C_HEAD if c == 5 else C_TEXT, size=9 if c == 5 else 10)
        if c == 5 and str(v).startswith("http"): cell.hyperlink = v
    ws.row_dimensions[r].height = row_height(vals, W5, minimum=30)
ws.auto_filter.ref = f"A4:F{4 + len(D.SOURCES)}"

unused = sorted(SRC_IDS - used)
print("rows", n_rows, "metrics", n_met, "sources", len(D.SOURCES), "unused sources", unused)
wb.save(OUT)
