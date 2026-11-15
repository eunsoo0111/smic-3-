# -*- coding: utf-8 -*-
"""MDA Space 층위별 리서치 재료 엑셀 빌더 (셀레스티카 층위별 리서치 재료와 같은 양식).

python3 research/mda/_build/build_workbook.py  →  research/mda/MDA_층위별_리서치_재료.xlsx
"""
import math
import os
import re
import sys
import csv

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mda_layers import LAYERS, ROWS  # noqa: E402
from mda_metrics import (M as METRICS, ALIAS, SOURCES, FMT_NUM, FMT_PCT, FMT_X,  # noqa: E402
                         QUARTERLY_NOTE, Q4_SEG)

ASOF = "2026-11-15"
OUT = os.path.join(os.path.dirname(HERE), "MDA_층위별_리서치_재료.xlsx")
QCSV = os.path.join(os.path.dirname(HERE), "branch_notes", "B05_quarterly.csv")

FONT = "Malgun Gothic"
C_TITLE_BG = "FF18354A"
C_HEAD_BG = "FF24627C"
C_LAYER_BG = "FFEDF4F7"
C_TEXT = "FF173044"
C_SUB = "FF586B79"
C_RAW = "FF17684F"
C_LINK = "FF24627C"
KIND_COLOR = {
    "리서치 해석": "FF5E5590", "반론": "FF8A3B3B",
    "수정 필요": "FF9B5E1C", "추가 확인": "FF9B5E1C",
}
DEFAULT_KIND_COLOR = "FF275F69"
WHITE = PatternFill("solid", fgColor="FFFFFFFF")
LAYER_FILL = PatternFill("solid", fgColor=C_LAYER_BG)
HEAD_FILL = PatternFill("solid", fgColor=C_HEAD_BG)
TITLE_FILL = PatternFill("solid", fgColor=C_TITLE_BG)
THIN = Side(style="thin", color="FFD9E2E8")
ROW_BORDER = Border(bottom=THIN)


def f(sz=10, b=False, color=C_TEXT):
    return Font(name=FONT, size=sz, bold=b, color=color)


def text_units(s):
    n = 0.0
    for ch in str(s):
        n += 1.85 if ord(ch) >= 0x1100 else 1.05
    return n


def fit_height(values_widths, base=30, line=14.0):
    lines = 1
    for v, w in values_widths:
        if v is None:
            continue
        for part in str(v).split("\n"):
            lines = max(lines, math.ceil(text_units(part) / max(w - 1.5, 4)))
    return max(base, lines * line + 8)


def sheet_header(ws, title, subtitle, headers, widths, freeze):
    ncol = len(headers)
    last = get_column_letter(ncol)
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = C_HEAD_BG[2:]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.merge_cells(f"A1:{last}1")
    ws.merge_cells(f"A2:{last}2")
    c = ws["A1"]
    c.value = title
    c.font = f(17, True, "FFFFFFFF")
    c.fill = TITLE_FILL
    c.alignment = Alignment(vertical="center", wrap_text=True, indent=1)
    for col in range(2, ncol + 1):
        ws.cell(1, col).fill = TITLE_FILL
    c = ws["A2"]
    c.value = subtitle
    c.font = f(10, False, C_SUB)
    c.fill = WHITE
    c.alignment = Alignment(vertical="center", wrap_text=True, indent=1)
    ws.row_dimensions[1].height = 34
    ws.row_dimensions[2].height = 35
    ws.row_dimensions[3].height = 9
    for i, h in enumerate(headers, start=1):
        c = ws.cell(4, i, h)
        c.font = f(10, True, "FFFFFFFF")
        c.fill = HEAD_FILL
        c.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
    ws.row_dimensions[4].height = 28
    ws.freeze_panes = freeze
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "4:4"


def body(c, color=C_TEXT, fill=WHITE, h=None, sz=10, b=False):
    c.font = f(sz, b, color)
    c.fill = fill
    c.alignment = Alignment(vertical="center", horizontal=h, wrap_text=True)
    c.border = ROW_BORDER


# ------------------------------------------------------------------ 데이터 점검
source_ids = {s[0] for s in SOURCES}
layer_names = {n: name for n, name, *_ in LAYERS}
for r in ROWS:
    for sid in [x.strip() for x in r[6].split(";")]:
        if sid not in source_ids:
            raise SystemExit(f"알 수 없는 출처 ID {sid!r} in row: {r[3][:40]}")

# ------------------------------------------------------------------ 행 ID 부여
rows_sorted = sorted(enumerate(ROWS), key=lambda t: (t[1][0], t[0]))
mat = []
for i, (_, r) in enumerate(rows_sorted, start=1):
    mat.append((f"R{i:03d}",) + r)
by_layer = {}
for rid, ln, *_ in mat:
    by_layer.setdefault(ln, []).append(rid)

wb = Workbook()

# ================================================================== 층위 지도
ws = wb.active
ws.title = "층위 지도"
n_mat = len(mat)
n_met = len(METRICS)
sheet_header(
    ws, "MDA Space | 리서치의 층위",
    f"{n_mat + n_met}개 재료·지표 = 논리 재료 {n_mat}행 + 지표 {n_met}행 · 출처 {len(SOURCES)}개 · 분기 시계열 19분기 · 기준 {ASOF} · "
    "이번 대화 Q&A와 다른 브랜치 노트 5곳(practical-mccarthy, elegant-cerf, hopeful-galileo, laughing-ride, ecstatic-clarke)을 층위별로 재배치",
    ["층위", "조사 영역", "이 층위에서 답하는 질문", "보고서에서의 역할", "재료 수", "재료 ID"],
    [25.6, 30.0, 62.0, 30.0, 11.5, 20.5], "A5")
last_mat_row = 4 + n_mat
r = 5
for n, name, area, q, role in LAYERS:
    ids = by_layer.get(n, [])
    vals = [name, area, q, role, f"=COUNTIF('리서치 재료'!B5:B{last_mat_row},A{r})", f"{ids[0]}–{ids[-1]}" if ids else ""]
    for col, v in enumerate(vals, start=1):
        c = ws.cell(r, col, v)
        body(c, fill=LAYER_FILL if col <= 2 else WHITE, h="center" if col >= 5 else None)
    ws.row_dimensions[r].height = fit_height([(q, 62), (role, 30)], base=40)
    r += 1
r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
c = ws.cell(r, 1, "읽는 순서와 근거 구분")
c.font = f(10, True, "FFFFFFFF")
c.fill = HEAD_FILL
c.alignment = Alignment(vertical="center", indent=1)
ws.row_dimensions[r].height = 24
r += 1
guide = [
    ("핵심 결론",
     "MDA는 위성을 만들어 파는 회사이고 지금은 상업 군집(Telesat·Globalstar)에 가장 크게 노출돼 있다. 투자포인트 1: 캐나다가 국가 재원으로 MDA 공장의 새 주인이 된다(ESCP-P·RADARSAT·Lightspeed 군 계약). "
     "투자포인트 2: 동맹국 소버린 수요는 부품·인수 거점(BCT·CLS) 경로의 상방 옵션. 원안의 '소버린 시장 점유율 상승'은 증거 부족 → '2027~29년 소버린 유입이 상업 롤오프를 넘어 잔고가 다시 는다'로 재구성."),
    ("확인 사실 / 회사 발표", "공시·정부 발표·고객 공시에서 확인한 사실. 발표되었다는 사실과 전망의 실현을 구분하고, 회사 계획·회사 주장은 따로 표시."),
    ("경영진 설명 / 전망", "3Q26 컨퍼런스콜(전사본) 발언 포함. 수주 계약 원문이나 독립 검증과 다름. 전사본은 음성 대조 전."),
    ("외사 추정 / 독립 리서치 / 보도", "Novaspace·SIA·셀사이드·독립 리서치·언론 보도. 기관·시점·통화를 유지하고 공시치와 섞지 않음."),
    ("직접 계산 / 직접 집계 / 직접 추정", "공시·보도 수치로 계산한 값. 수식은 「지표 원장」·「분기 시계열」에 남김. 추정은 가정을 같은 행에 적음."),
    ("리서치 해석 / 반론", "사실로부터 도출한 연결 논리와 그에 대한 반대 증거. 대화 Q&A(Q01~Q07)에서 나온 해석은 출처 ID로 추적."),
    ("추가 확인 / 수정 필요", "원문 미확인 수치, 자료 간 불일치, 이전 답변의 기억 기반 서술을 정정한 내역. 원본 브랜치 파일은 수정하지 않음(사본은 branch_notes/)."),
    ("찾는 방법", "「리서치 재료」에서 층위·근거·배치별 필터 → 출처 ID 확인 → 「출처」의 원문. 수치와 계산은 「지표 원장」, 분기 흐름은 「분기 시계열」. 서술형 정리는 MDA_리서치노트_층위별.md."),
    ("범위", "MDA Space 관련 논리와 자료만 취합. BlackSky·TMDX 등 다른 종목 자료, 반복 문구, 검증되지 않은 TAM 계산은 재료로 확대하지 않음. 통화는 별도 표기 없으면 C$."),
]
for k, v in guide:
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
    c = ws.cell(r, 1, k)
    body(c, fill=LAYER_FILL)
    c = ws.cell(r, 2, v)
    body(c)
    for col in range(3, 7):
        ws.cell(r, col).border = ROW_BORDER
    ws.row_dimensions[r].height = fit_height([(v, 150)], base=30)
    r += 1

# ================================================================== 리서치 재료
ws = wb.create_sheet("리서치 재료")
sheet_header(
    ws, "MDA Space | 리서치 재료",
    f"정리 기준 {ASOF} · {n_mat}개 재료 · 한 행에 주장 하나 · 4행 필터로 층위·근거·배치·출처별 검색 · 출처 ID의 원문 경로는 「출처」 시트 · 통화 표기 없으면 C$",
    ["ID", "1층 · 대분류", "2층 · 조사 영역", "3층 · 세부 주제", "근거 구분", "재료 · 관찰한 내용", "의미 · 적용 범위", "보고서 배치", "출처 · 위치"],
    [7.2, 19.0, 18.5, 19.0, 13.0, 62.0, 48.0, 17.8, 20.0], "C5")
area_of = {n: area for n, name, area, *_ in LAYERS}
for i, (rid, ln, topic, kind, material, meaning, place, src) in enumerate(mat, start=5):
    vals = [rid, layer_names[ln], area_of[ln], topic, kind, material, meaning, place, src]
    for col, v in enumerate(vals, start=1):
        c = ws.cell(i, col, v)
        color = KIND_COLOR.get(kind, DEFAULT_KIND_COLOR) if col == 5 else C_TEXT
        body(c, color=color, fill=LAYER_FILL if col in (2, 3) else WHITE, h="center" if col in (1, 5) else None)
    ws.row_dimensions[i].height = fit_height([(material, 62), (meaning, 48), (topic, 19), (src, 20)], base=36)
ws.auto_filter.ref = f"A4:I{last_mat_row}"

# ================================================================== 지표 원장
ws = wb.create_sheet("지표 원장")
sheet_header(
    ws, "MDA Space | 지표 원장",
    f"{n_met}개 지표 · 금액은 별도 표기 없으면 C$ 백만(C$M) · 통화(C$/US$/€/JPY)를 단위 칸에 유지 · 초록색 숫자는 원자료, 검은색은 계산·집계·추정 · "
    "가이던스·컨센서스는 발표 시점 기준",
    ["ID", "분류", "지표", "기간 · 기준", "값", "단위", "성격", "해석 · 주의점", "출처 · 셀"],
    [7.2, 14.0, 34.0, 15.0, 13.5, 10.5, 13.0, 46.0, 18.0], "D5")
key_row = {}
for i, (cat, name, period, val, unit, kind, note, src) in enumerate(METRICS, start=5):
    key_row[(name, period)] = i
alias_row = {}
for k, (name, period) in ALIAS.items():
    if (name, period) not in key_row:
        raise SystemExit(f"ALIAS {k} → {(name, period)} 없음")
    alias_row[k] = key_row[(name, period)]


def resolve(expr):
    def rep(mo):
        k = mo.group(1)
        if k not in alias_row:
            raise SystemExit(f"수식 키 없음: {k}")
        return f"E{alias_row[k]}"
    return re.sub(r"\{([^}]+)\}", rep, expr)


for i, (cat, name, period, val, unit, kind, note, src) in enumerate(METRICS, start=5):
    mid = f"M{i - 4:03d}"
    is_formula = isinstance(val, str) and val.startswith("=")
    v = resolve(val) if is_formula else val
    calc_kind = kind.startswith("직접")
    vals = [mid, cat, name, period, v, unit, kind, note, src]
    for col, x in enumerate(vals, start=1):
        c = ws.cell(i, col, x)
        if col == 5:
            body(c, color=C_TEXT if (is_formula or calc_kind) else C_RAW, h="right")
            c.number_format = FMT_PCT if unit == "%" else (FMT_X if unit == "x" else FMT_NUM)
            if unit not in ("%", "x") and isinstance(val, (int, float)) and abs(val) < 10 and val != int(val):
                c.number_format = '#,##0.00;(#,##0.00);"—"'
        else:
            body(c, h="center" if col in (1, 4, 6) else None)
    ws.row_dimensions[i].height = fit_height([(note, 46), (name, 34)], base=30)
ws.auto_filter.ref = f"A4:I{4 + n_met}"

# ================================================================== 분기 시계열
ws = wb.create_sheet("분기 시계열")
heads = ["분기", "매출", "Satellite Systems", "Robotics & Space Ops", "Geointelligence", "조정 EBITDA", "EBITDA 마진",
         "매출 YoY", "신규 수주", "기말 수주잔고", "분기 B/B", "비고"]
sheet_header(
    ws, "MDA Space | 분기 시계열",
    "C$ 백만 · 원천: 분기 실적 보도자료 24건(B05 quarterly.csv, C05) · 초록색은 원자료, 검은색은 수식·역산 · "
    "4분기 사업부 값은 연간−9개월(2025Q4) 또는 FY2025 성장률 역산 근사(2024Q4) · 잔고 정점 1Q25, 저점 1Q26",
    heads, [10.0, 10.5, 12.5, 13.0, 13.0, 11.5, 11.0, 10.0, 11.0, 12.5, 10.0, 46.0], "B5")
with open(QCSV, encoding="utf-8") as fh:
    qrows = list(csv.DictReader(fh))
for i, q in enumerate(qrows, start=5):
    qq = q["quarter"]
    seg = [q["satellite_systems"], q["robotics_space_ops"], q["geointelligence"]]
    seg_calc = False
    if not seg[0] and qq in Q4_SEG:
        seg = list(Q4_SEG[qq])
        seg_calc = True
    note = q["note"] or ""
    if qq in QUARTERLY_NOTE:
        note = (QUARTERLY_NOTE[qq] + (" " + note if note else "")).strip()
    vals = [qq, float(q["revenue"])]
    vals += [float(x) if x not in ("", None) else None for x in seg]
    vals += [float(q["adj_ebitda"]), f"=F{i}/B{i}", (f"=B{i}/B{i-4}-1" if i - 4 >= 5 else None),
             float(q["order_bookings"]), float(q["backlog_end"]), f"=I{i}/B{i}", note]
    for col, x in enumerate(vals, start=1):
        c = ws.cell(i, col, x)
        if col == 1:
            body(c, h="center", fill=LAYER_FILL)
        elif col == 12:
            body(c)
        else:
            derived = isinstance(x, str) or (col in (3, 4, 5) and seg_calc) or (qq.endswith("Q4") and col in (2, 9) and qq in QUARTERLY_NOTE)
            body(c, color=C_TEXT if derived else C_RAW, h="right")
            c.number_format = FMT_PCT if col in (7, 8) else (FMT_X if col == 11 else FMT_NUM)
    ws.row_dimensions[i].height = fit_height([(note, 46)], base=22)
last_q = 4 + len(qrows)
ws.auto_filter.ref = f"A4:L{last_q}"

# ================================================================== 출처
ws = wb.create_sheet("출처")
sheet_header(
    ws, "MDA Space | 출처와 사용 범위",
    "C=회사 공시·발표, T=컨퍼런스콜, G=정부, W=웹·보도·외사, B=다른 브랜치 리서치 노트(사본 research/mda/branch_notes/), Q=이번 대화 Q&A · "
    "웹 자료는 조사 시점 목록이며 실시간 갱신 목록 아님 · 같은 회사 발표의 반복 보도는 독립 확인으로 세지 않음",
    ["ID", "자료명", "자료 성격", "발표 · 기준일", "원문 URL 또는 로컬 경로", "사용 범위 · 주의"],
    [8.5, 36.0, 18.1, 14.0, 70.0, 52.0], "A5")
for i, (sid, name, kind, date, url, scope) in enumerate(SOURCES, start=5):
    vals = [sid, name, kind, date, url, scope]
    for col, x in enumerate(vals, start=1):
        c = ws.cell(i, col, x)
        if col == 5:
            body(c, color=C_LINK, sz=9)
            first = str(url).split(" ")[0]
            if first.startswith("http"):
                c.hyperlink = first
        else:
            body(c, h="center" if col in (1, 4) else None)
    ws.row_dimensions[i].height = fit_height([(url, 70), (scope, 52), (name, 36)], base=30)
ws.auto_filter.ref = f"A4:F{4 + len(SOURCES)}"

wb.save(OUT)
print("saved", OUT, "materials", n_mat, "metrics", n_met, "sources", len(SOURCES), "quarters", len(qrows))
