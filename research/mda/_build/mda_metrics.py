# -*- coding: utf-8 -*-
"""MDA Space 지표 원장·출처·분기 시계열.

METRICS: (ID, 분류, 지표, 기간·기준, 값, 단위, 성격, 해석·주의점, 출처)
  값이 '=' 로 시작하면 수식이다. {M001} 은 해당 지표의 값 셀로 바뀐다. 수식 값은 검은색, 원자료는 초록색.
"""

FMT_NUM = '#,##0.0;(#,##0.0);"—"'
FMT_PCT = '0.0%;(0.0%);"—"'
FMT_X = '0.00"x";(0.00"x");"—"'

M = []
def add(cat, name, period, val, unit, kind, note, src):
    M.append((cat, name, period, val, unit, kind, note, src))

# ---------------- 연간 실적 (C$M)
annual = [
    ("FY2022", 641.2, 157.9, 1155.1, 1378.2),
    ("FY2023", 807.6, 174.2, 2526.4, 3097.0),
    ("FY2024", 1080.1, 217.1, 2368.6, 4385.5),
    ("FY2025", 1633.2, 323.9, 1200.1, 4012.9),
    ("9M26", 1460.8, 282.9, 1397.0, 3949.1),
]
for p, rev, ebitda, book, backlog in annual:
    add("연간 실적", "매출", p, rev, "C$M", "회사 실적", "분기 합계. FY2025는 연간 공시치와 일치.", "C01; C02; B05")
    add("연간 실적", "조정 EBITDA", p, ebitda, "C$M", "회사 실적", "회사 non-IFRS 정의. 분기 합계.", "C01; C02; B05")
    add("연간 실적", "조정 EBITDA 마진", p, "={%s_ebitda}/{%s_rev}" % (p, p), "%", "직접 계산", "", "계산")
    add("연간 실적", "신규 수주", p, book, "C$M", "회사 실적", "분기 보도자료 수주 합계. 2023·2024는 분기 합으로 역산.", "C05; B03; B05")
    add("연간 실적", "기말 수주잔고", p, backlog, "C$M", "회사 실적", "9M26은 2026-09-30 기준.", "C05; B03; B05")
    add("연간 실적", "수주/매출(B/B)", p, "={%s_book}/{%s_rev}" % (p, p), "x", "직접 계산", "1 미만이면 잔고가 줄어든다.", "계산")
add("연간 실적", "매출 증가율", "FY2025", "={FY2025_rev}/{FY2024_rev}-1", "%", "직접 계산", "공시 +51.2%.", "계산")
add("연간 실적", "잔고/매출 배수", "FY2023", "={FY2023_backlog}/{FY2023_rev}", "x", "직접 계산", "가시성 지표.", "계산")
add("연간 실적", "잔고/매출 배수", "FY2025", "={FY2025_backlog}/{FY2025_rev}", "x", "직접 계산", "2023년 3.8배 → 2025년 2.5배. 3Q26 잔고 ÷ 2026 가이던스 중간값은 약 2.0배.", "계산")
add("연간 실적", "매출총이익률", "FY2025", 0.251, "%", "회사 실적", "", "C02; B01")

# ---------------- 사업부
seg = [
    ("Satellite Systems 매출", "FY2025", 1109.5, "+85.5%"), ("Robotics & Space Ops 매출", "FY2025", 309.3, "+10.5%"),
    ("Geointelligence 매출", "FY2025", 214.4, "+6.1%"),
    ("Satellite Systems 매출", "9M26", 1007.5, "+36.5%"), ("Robotics & Space Ops 매출", "9M26", 271.0, "+11.2%"),
    ("Geointelligence 매출", "9M26", 182.3, "+19.6%"),
]
for n, p, v, g in seg:
    add("사업부", n, p, v, "C$M", "회사 실적", "전년 대비 %s. 사업부별 이익은 미공시." % g, "C01; C02; B01")
add("사업부", "위성 부문 비중", "FY2025", "={seg_sat25}/{FY2025_rev}", "%", "직접 계산", "", "계산")
add("사업부", "위성 부문 연환산 매출", "9M26 기준", "={seg_sat9m}/3*4", "C$M", "직접 계산", "구멍 크기 추정의 기준(약 C$1.35B).", "계산")

# ---------------- 가이던스
for n, lo, hi in [("2026 매출 가이던스", 1900, 1950), ("2026 조정 EBITDA 가이던스", 355, 375), ("2026 capex 가이던스", 225, 275)]:
    add("가이던스", n + " 하단", "2026-11-05", lo, "C$M", "회사 가이던스", "11월 상향 후. BCT·CLS 미포함.", "C01; T01")
    add("가이던스", n + " 상단", "2026-11-05", hi, "C$M", "회사 가이던스", "", "C01; T01")
add("가이던스", "4Q26 내재 매출 하단", "4Q26", "={g_rev_lo}-{9M26_rev}", "C$M", "직접 계산", "전년 동기 499.1 대비 감소.", "계산")
add("가이던스", "4Q26 내재 매출 상단", "4Q26", "={g_rev_hi}-{9M26_rev}", "C$M", "직접 계산", "", "계산")
add("가이던스", "2026 최초 매출 가이던스 중간값", "2026-03", 1800, "C$M", "회사 가이던스", "최초 1,700~1,900.", "B03")
add("가이던스", "인수 2건 프로포마 매출", "2026", 700, "C$M", "경영진 설명", "BCT 약 C$225M + CLS 약 C$465M.", "T01; B07")
add("가이던스", "2027 매출 컨센서스", "2027E", 2860, "C$M", "외사 추정", "12곳, 인수 포함. 범위 2,840~2,860.", "W36; B03; B07")
add("가이던스", "2027 조정 EBITDA 컨센서스", "2027E", 552.5, "C$M", "외사 추정", "범위 540~565 중간값.", "B03")

# ---------------- 매출 구성·고객
add("매출 구성", "상위 10개 고객 비중", "FY2025", 0.872, "%", "회사 공시", "AIF.", "C04; B01")
add("매출 구성", "해외(비캐나다) 매출 비중", "FY2025", 0.374, "%", "회사 공시", "", "C04; B01")
add("매출 구성", "상업 고객 매출 비중", "FY2025", 0.72, "%", "회사 IR 자료", "IR 자료 p4. 원본 대조 필요.", "C06; B07")
add("매출 구성", "캐나다 매출", "9M26", 1018, "C$M", "회사 실적", "재무제표 주석.", "C01; B03")
add("매출 구성", "미국 매출", "9M26", 357, "C$M", "회사 실적", "", "C01; B03")
add("매출 구성", "유럽 매출", "9M26", 59, "C$M", "회사 실적", "", "C01; B03")
add("매출 구성", "아시아·중동 매출", "9M26", 24, "C$M", "회사 실적", "", "C01; B03")
add("매출 구성", "캐나다 비중", "9M26", "={geo_ca}/{9M26_rev}", "%", "직접 계산", "약 70%.", "계산")
add("매출 구성", "Telesat·Globalstar 잔고 비중", "2026 중반", 0.73, "%", "독립 리서치", "잔고 C$4.4B 기준. 공시치 아님.", "W35; B06")

# ---------------- 현금·재무
fin = [
    ("현금", "2026-09-30", 2153.8, "C$M", "회사 실적", ""),
    ("순현금", "2026-09-30", 1328.0, "C$M", "회사 실적", "인수 대금 집행 전."),
    ("장기부채", "2026-09-30", 825.8, "C$M", "회사 실적", "C$600M 사채 포함."),
    ("영업현금흐름", "9M26", 73.7, "C$M", "회사 실적", ""),
    ("잉여현금흐름", "9M26", -116.2, "C$M", "직접 계산", "OCF − capex. 2차 자료 기준 약 −116."),
    ("영업현금흐름", "3Q26", 106.2, "C$M", "회사 실적", ""),
    ("잉여현금흐름", "3Q26", 61.6, "C$M", "회사 실적", "전년 동기 −36.7."),
    ("영업현금흐름", "FY2024", 812.7, "C$M", "회사 실적", "수주 직후 선수금 유입."),
    ("계약부채", "2025-12-31", 798.9, "C$M", "회사 실적", ""),
    ("계약부채", "2026-09-30", 601.7, "C$M", "회사 실적", "선수금 소진 중."),
    ("SG&A", "9M26", 114.4, "C$M", "회사 실적", "전년 81.0."),
]
for n, p, v, u, k, note in fin:
    add("현금·재무", n, p, v, u, k, note, "C01; B01; B08")
add("현금·재무", "인수 대금 합계(BCT+CLS)", "예정", "={acq_bct_c}+{acq_cls_c}", "C$M", "직접 계산", "수수료·운전자본 조정 제외.", "계산")
add("현금·재무", "인수 후 순현금(순차입)", "프로포마", "={net_cash}-{acq_sum}", "C$M", "직접 계산", "음수면 순차입.", "계산")
add("현금·재무", "인수 후 순차입/2026 EBITDA 중간값", "프로포마", "=-{acq_net}/(({g_ebitda_lo}+{g_ebitda_hi})/2)", "x", "직접 계산", "인수 회사 EBITDA 제외. 목표 1.5~2.5배.", "계산")

# ---------------- 자본·인수
cap = [
    ("주식 수(기말)", "2025-12-31", 126.3, "백만 주", "회사 실적", "", "B01"),
    ("주식 수(가중평균)", "3Q26", 158.8, "백만 주", "회사 실적", "", "B01"),
    ("발행주식", "2026-09-30", 162.2, "백만 주", "회사 실적", "", "B03"),
    ("NYSE 상장가", "2026-03", 30.50, "US$/주", "회사 발표", "1,118만 주.", "B03"),
    ("7월 증자가", "2026-07", 35.60, "US$/주", "회사 발표", "2,300만 주, US$819M.", "C21; B03"),
    ("CSG 취득 평균가", "2026-10-13", 42.69, "C$/주", "SEC 공시", "9.5%(1,536만 주).", "C20; B03"),
    ("BCT 인수가", "2026-06-19", 620, "US$M", "회사 발표", "현금 100%.", "C10"),
    ("BCT 인수가(C$)", "2026-06-19", 874, "C$M", "회사 발표", "", "B03"),
    ("CLS 인수가(70%)", "2026", 567, "€M", "회사 발표", "", "W24"),
    ("CLS 인수가(C$)", "2026", 920, "C$M", "회사 발표", "", "B03"),
    ("CLS 매출", "2026E", 286, "€M", "회사 발표", "2025년 €203M(2차)과 연도 구분.", "B03"),
    ("SatixFy 인수 총 대가", "2025-07", 448.3, "C$M", "회사 실적", "", "B01"),
    ("사채(7.00%, 2030)", "2025-12", 250, "C$M", "회사 발표", "", "W25"),
    ("사채(6.50%, 2033)", "2026-08", 600, "C$M", "회사 발표", "BCT 미종결 시 액면 상환.", "C19; W25"),
]
for n, p, v, u, k, note, s in cap:
    add("자본·인수", n, p, v, u, k, note, s)

# ---------------- 프로그램
prog = [
    ("Lightspeed 잔여 잔고", "3Q26", 1400, "C$M", "경영진 설명", "2027~29년 인식 후 종료.", "T01"),
    ("Lightspeed 총액(MDA 자료)", "2026", 2900, "C$M", "회사 IR 자료", "225기 + 옵션 73기. 원계약 약 2.4B·198기와 구분.", "C06; B02"),
    ("Lightspeed 대수", "2026", 225, "기", "회사 IR 자료", "", "C06; B02"),
    ("Lightspeed +27기 수주", "2026-08", 474, "C$M", "회사 발표", "ESCP-P 군용 Ka 확장.", "C08"),
    ("RADARSAT 보충위성 본계약", "2026-06", 688, "C$M", "보도(회사 발표)", "+C$45M 별도.", "C15"),
    ("IRIS² Layer 1 안테나 ATP", "2026-10-30", 100, "C$M", "회사 발표", "'C$100M+'. 본계약 전, 4Q26 잔고 반영.", "W13"),
    ("Globalstar 3세대 계약", "2025", 775, "US$M", "고객 공시", "50기+.", "W08; B03"),
    ("Globalstar 3세대 집행액", "3Q26", 529.5, "US$M", "고객 공시", "", "W08; B03"),
    ("Globalstar 교체 위성 계약", "2022", 329.3, "US$M", "고객 공시", "17기. 버스는 Rocket Lab(US$143M).", "W08; W18"),
    ("Globalstar 교체 잔여", "3Q26", 26, "US$M", "직접 계산", "", "B03"),
    ("EchoStar 계약(해지)", "2025-08", 1300, "US$M", "회사 발표", "잠재 US$2.5B. 2025-09 해지.", "C07"),
    ("Canadarm3 Phase C/D", "2024", 1000, "C$M", "회사 발표", "잠재 총 약 C$1.8B.", "B01"),
    ("ESCP-P LEO(Telesat)", "2026-08-04", 2300, "C$M", "정부 발표", "옵션 약 C$0.43B.", "G01"),
    ("ESCP-P MEO(MDA 몫) 추정", "추정", 2000, "C$M", "직접 추정", "전체 C$5B+ − Telesat 몫 약 2.7B. 'C$2B+'.", "C06; B06"),
    ("파이프라인", "2026", 40000, "C$M", "회사 발표", "그중 C$10B가 최종 후보·후속.", "T01"),
]
for n, p, v, u, k, note, s in prog:
    add("프로그램", n, p, v, u, k, note, s)
add("프로그램", "Globalstar 3세대 잔여", "3Q26", "={gs3_total}-{gs3_spent}", "US$M", "직접 계산", "", "계산")
add("프로그램", "Lightspeed 대당 단가", "2026", "={ls_total}/{ls_units}", "C$M/기", "직접 계산", "", "계산")
add("프로그램", "ESCP-P 추가분 대당 단가", "2026-08", "={ls_add}/27", "C$M/기", "직접 계산", "", "계산")
add("프로그램", "2026 대형 2건 수주 합", "9M26", "={radarsat}+{ls_add}", "C$M", "직접 계산", "9M 수주 1,397M 중 비중.", "계산")
add("프로그램", "대형 2건 제외 분기 평균 수주", "9M26", "=({9M26_book}-{big2})/3", "C$M", "직접 계산", "약 78M.", "계산")

# ---------------- 소버린 수요
sov = [
    ("정부 통신위성 발주(제외: SpaceX·Amazon·중국)", "2020", 0.9), ("정부 통신위성 발주", "2022", 2.0),
    ("정부 통신위성 발주", "2023", 3.3), ("정부 통신위성 발주", "2024", 4.3), ("정부 통신위성 발주", "2025", 3.0),
    ("정부 통신위성 발주(확정)", "2026 1~10월", 5.3), ("정부 통신위성 발주(OneWeb ATP 포함)", "2026 1~10월", 6.5),
]
for n, p, v in sov:
    add("소버린 수요", n, p, v, "US$B", "직접 집계", "서비스 계약·융자 제외. 2019·2021 집계 불완전.", "B02")
for n, p, v, u, k, note, s in [
    ("대기 중 발주 하단", "2026-11", 12, "US$B", "직접 집계", "SATCOMBw 4, Skynet WSS, IRIS² 잔여, K-LEO 등.", "B02"),
    ("대기 중 발주 상단", "2026-11", 15, "US$B", "직접 집계", "", "B02"),
    ("IRIS² 총 사업비", "2026-08", 15.6, "€B", "보도", "348기.", "W12"),
    ("IRIS² Layer 2 플랫폼(Aerospacelab)", "2026-09", 2.4, "€B", "회사 발표", "264기, 대당 €9.1M.", "W12"),
    ("독일 군사우주 예산", "~2030", 35, "€B", "보도", "통신 약 200기.", "W14"),
    ("SATCOMBw 4단계", "미발주", 9, "€B", "보도", "€8~10B 중간값.", "W14; B02"),
    ("SDN 백본(SpaceX)", "2026-05", 2.29, "US$B", "보도", "미국은 SpaceX를 택함.", "W15"),
    ("일본 차세대 방위통신위성", "2026", 123.5, "JPY B", "고객 발표", "GEO 1기, Mitsubishi Electric 프라임.", "W17"),
    ("정부 우주예산", "2025", 137.4, "US$B", "외사 추정", "국방 54%(73.5B).", "C04; B01"),
    ("정부 재원 통신위성 식별 대수 하단", "2025~2034", 2000, "기", "직접 계산", "", "B02"),
    ("정부 재원 통신위성 식별 대수 상단", "2025~2034", 4000, "기", "직접 계산", "", "B02"),
    ("캐나다 밖 소버린 누적 수주 추정 하단", "~2026", 0.2, "C$B", "직접 추정", "공개분은 IRIS² C$100M+뿐.", "B02"),
    ("캐나다 밖 소버린 누적 수주 추정 상단", "~2026", 0.5, "C$B", "직접 추정", "", "B02"),
]:
    add("소버린 수요", n, p, v, u, k, note, s)

# ---------------- 시장
for n, p, v, u, k, note, s in [
    ("위성 발사 대수", "2025", 4434, "기", "외사 집계", "SIA.", "W03"),
    ("위성 제조 매출", "2025", 20.4, "US$B", "외사 집계", "SIA. 평균 1기 약 460만 달러.", "W03"),
    ("10년 위성 수요", "2025~2034", 43000, "기", "외사 추정", "Novaspace 28판.", "W01; W02"),
    ("메가 군집 수량 비중", "2025~2034", 0.66, "%", "외사 추정", "가치로는 11%.", "W01"),
    ("메가 군집 가치 비중", "2025~2034", 0.11, "%", "외사 추정", "", "W01"),
    ("국방 위성 가치 비중", "2025~2034", 0.48, "%", "외사 추정", "수량 9%.", "W01"),
    ("완전 개방 제조 시장 비중", "2025~2034", 0.07, "%", "외사 추정", "자국 캡티브 약 70%.", "W01"),
    ("Starlink 소비자 가입자", "3Q26", 13.6, "백만", "보도", "", "W06"),
    ("Starlink 소비자 월 ARPU", "3Q26", 69, "US$", "보도", "전년 83.", "W06"),
    ("SpaceX 공모가", "2026-06-12", 135, "US$/주", "보도", "첫날 종가 160.95, 시총 약 2.1조 달러.", "W04; W05"),
    ("Rocket Lab 수주잔고", "2026-09-30", 3.57, "US$B", "보도", "8-K 대조 전.", "W20; B02"),
    ("York 수주잔고", "1Q26", 0.642, "US$B", "회사 실적", "", "W20; B02"),
]:
    add("시장·피어", n, p, v, u, k, note, s)

# ---------------- Telesat
for n, p, v, u, k, note, s in [
    ("Telesat GEO 부채", "~2027-10", 3000, "C$M", "보도", "가장 가까운 만기 12-06 약 US$1.7B.", "W10"),
    ("Telesat GEO 현금", "3Q26", 286.7, "C$M", "보도", "", "W10"),
    ("Telesat LEO 수주잔고", "3Q26", 5600, "C$M", "보도", "캐나다 정부 북극 C$2.7B 포함.", "W09; B09"),
    ("ESCP 마일스톤 지급", "3Q26~4Q28", 2000, "C$M", "고객 발표", "", "W09; B03"),
    ("ESCP 선급금 누계 수령", "9M26", 510, "C$M", "고객 발표", "", "W09; B03"),
    ("Telesat 3Q26 매출", "3Q26", 80.6, "C$M", "고객 실적", "−20% YoY.", "W09"),
]:
    add("Telesat", n, p, v, u, k, note, s)

# ---------------- 밸류에이션
for n, p, v, u, k, note, s in [
    ("NYSE 종가", "2026-11-12", 29.16, "US$/주", "시장 데이터", "", "B03"),
    ("52주 고점", "2026-05-28", 48.68, "US$/주", "시장 데이터", "종가 기준. 장중 49.37.", "B03; B07"),
    ("시가총액", "2026-11-12", 4.74, "US$B", "시장 데이터", "", "B07"),
    ("인수 반영 EV", "프로포마", 5.4, "US$B", "직접 계산", "순부채 0.36 + CLS 소수지분 0.29 포함.", "B07"),
    ("2027 EBITDA(컨센 매출×19%)", "2027E", 400, "US$M", "직접 계산", "C$540M × 0.733.", "B07"),
    ("셀사이드 평균 목표가", "2026-11", 41.8, "US$/주", "외사 추정", "14명.", "B07"),
    ("JPMorgan 목표가", "2026-11-10", 44, "US$/주", "외사 추정", "50에서 하향.", "W36"),
    ("Jefferies 목표가", "2026-11", 45, "US$/주", "외사 추정", "49에서 하향.", "B01"),
    ("BMO 목표가", "2026-11", 39, "US$/주", "외사 추정", "48에서 하향.", "B07"),
]:
    add("밸류에이션", n, p, v, u, k, note, s)
add("밸류에이션", "2027 EV/EBITDA(프로포마)", "2027E", "={ev}*1000/{e27}", "x", "직접 계산", "약 13.5배.", "계산")
add("밸류에이션", "52주 고점 대비", "2026-11-12", "={px}/{px_hi}-1", "%", "직접 계산", "", "계산")
add("밸류에이션", "18배 적용 시 상승여력", "2027E", 0.37, "%", "직접 계산", "18배 ≈ US$40. 피어 근거 필요.", "B06")

# 별칭: 수식에서 쓰는 키 → (지표, 기간)
ALIAS = {
    "seg_sat25": ("Satellite Systems 매출", "FY2025"), "seg_sat9m": ("Satellite Systems 매출", "9M26"),
    "g_rev_lo": ("2026 매출 가이던스 하단", "2026-11-05"), "g_rev_hi": ("2026 매출 가이던스 상단", "2026-11-05"),
    "g_ebitda_lo": ("2026 조정 EBITDA 가이던스 하단", "2026-11-05"), "g_ebitda_hi": ("2026 조정 EBITDA 가이던스 상단", "2026-11-05"),
    "geo_ca": ("캐나다 매출", "9M26"), "net_cash": ("순현금", "2026-09-30"),
    "acq_bct_c": ("BCT 인수가(C$)", "2026-06-19"), "acq_cls_c": ("CLS 인수가(C$)", "2026"),
    "acq_sum": ("인수 대금 합계(BCT+CLS)", "예정"), "acq_net": ("인수 후 순현금(순차입)", "프로포마"),
    "gs3_total": ("Globalstar 3세대 계약", "2025"), "gs3_spent": ("Globalstar 3세대 집행액", "3Q26"),
    "ls_total": ("Lightspeed 총액(MDA 자료)", "2026"), "ls_units": ("Lightspeed 대수", "2026"),
    "ls_add": ("Lightspeed +27기 수주", "2026-08"), "radarsat": ("RADARSAT 보충위성 본계약", "2026-06"),
    "big2": ("2026 대형 2건 수주 합", "9M26"),
    "ev": ("인수 반영 EV", "프로포마"), "e27": ("2027 EBITDA(컨센 매출×19%)", "2027E"),
    "px": ("NYSE 종가", "2026-11-12"), "px_hi": ("52주 고점", "2026-05-28"),
}
for p, *_ in annual:
    ALIAS[p + "_rev"] = ("매출", p)
    ALIAS[p + "_ebitda"] = ("조정 EBITDA", p)
    ALIAS[p + "_book"] = ("신규 수주", p)
    ALIAS[p + "_backlog"] = ("기말 수주잔고", p)

# ---------------- 분기 시계열 (B05 quarterly.csv + 4Q 사업부 역산)
QUARTERLY_NOTE = {
    "2023Q4": "매출·수주는 연간−9개월 역산. 사업부 미공시.",
    "2024Q4": "매출·수주 역산. 사업부는 FY2025 성장률로 FY2024를 역산한 근사치.",
    "2025Q4": "매출·수주 역산. 사업부는 FY2025 − 9M25.",
}
Q4_SEG = {  # 직접 계산
    "2024Q4": (234.4, 64.8, 47.4),
    "2025Q4": (371.4, 65.7, 62.0),
}

# ---------------- 출처
# (ID, 자료명, 자료 성격, 발표·기준일, URL 또는 경로, 사용 범위·주의)
SOURCES = [
    ("C01", "MDA 3Q26 실적 보도자료", "회사 공식 실적", "2026-11-05", "https://mda-en.investorroom.com/2026-11-05-MDA-SPACE-REPORTS-THIRD-QUARTER-2026-RESULTS", "분기 실적·잔고·현금·가이던스. 9M 수주 1,397.0M을 정본으로 사용."),
    ("C02", "MDA 4Q·FY2025 실적 보도자료", "회사 공식 실적", "2026-03-04", "https://mda-en.investorroom.com/2026-03-04-MDA-SPACE-REPORTS-FOURTH-QUARTER-AND-FISCAL-2025-RESULTS", "FY2025 연간 수치."),
    ("C03", "FY2025 MD&A (SEC F-10 Ex.4.3)", "SEC 공시", "2026-03", "https://www.sec.gov/Archives/edgar/data/1857047/000110465926025809/tm266080d2_ex4-3.htm", "사업 설명·리스크."),
    ("C04", "FY2025 Annual Information Form (SEC F-10 Ex.4.1)", "SEC 공시", "2026-03", "https://www.sec.gov/Archives/edgar/data/1857047/000110465926025809/tm266080d2_ex4-1.htm", "계약 구조(고정가·편의 해지), 고객 목록, 고객 집중, 경쟁사, Novaspace 인용."),
    ("C05", "MDA 분기 실적 보도자료 24건(2022Q1~2026Q3)", "회사 공식 실적", "2022~2026", "https://mda-en.investorroom.com/ ; 정리본 research/mda/branch_notes/B05_quarterly.csv", "분기 시계열 원천. 4분기 값 일부는 연간−9개월 역산."),
    ("C06", "MDA 투자자 프레젠테이션(2026)", "회사 IR 자료", "2026", "원본 PDF 경로 미기재 — B03·B06·B07에서 p4·p6·p7·p9·p12·p14·p16 인용", "상업 72%/정부 28%, 파이프라인 구성(원그래프 눈대중), 국방비 경로, ESCP-P C$5B+. 원본 확보 필요."),
    ("C07", "MDA EchoStar 계약 업데이트", "회사 공식 발표", "2025-09-08", "https://mda-en.investorroom.com/2025-09-08-MDA-SPACE-PROVIDES-UPDATE-ON-ECHOSTAR-CONTRACT", "해지 사실·보상."),
    ("C08", "Lightspeed 확장 C$474M 수주", "회사 공식 발표", "2026-08-04", "https://mda-en.investorroom.com/2026-08-04-MDA-SPACE-AWARDED-474-MILLION-TO-EXPAND-THE-TELESAT-LIGHTSPEED-LEO-CONSTELLATION", "+27기."),
    ("C09", "한화시스템 K-LEO MOU", "회사 공식 발표", "2026-01-26", "https://mda-en.investorroom.com/2026-01-26-MDA-SPACE-AND-HANWHA-SIGN-MOU-TO-PURSUE-KOREAN-MILITARY-CONSTELLATION-PROGRAM", "MOU(공동 검토)일 뿐 수주 아님."),
    ("C10", "BCT 인수 확정 계약", "회사 공식 발표", "2026-06-19", "https://mda.space/article/mda-space-announces-definitive-agreement-to-acquire-us-based-blue-canyon-technologies-llc", "US$620M 현금, 2026년 말 종결 예정, 국방 75%."),
    ("C11", "CLS 인수 확정 제안", "회사 공식 발표", "2026-07", "mda.space 보도자료 'MDA Space enters firm offer to acquire CLS'(정확한 URL 미기재) — W24 참조", "지분 70%, €567M, CNES 30% 잔류."),
    ("C12", "Airbus OneWeb 안테나 재수주", "회사 공식 발표", "2026-04", "https://mda.space/article/mda-space-contracted-by-airbus-for-repeat-order-of-antennas-for-oneweb-constellation-extension", "안테나 1,320개. 금액 비공개."),
    ("C13", "Mitsubishi Electric 차세대 방위통신위성 선정", "회사 공식 발표", "2026-06-25", "https://mda-en.investorroom.com/2026-06-25-MDA-SPACE-SELECTED-BY-MITSUBISHI-ELECTRIC-FOR-NEXT-GENERATION-DEFENCE-COMMUNICATIONS-SATELLITE-PROGRAM", "금액 비공개."),
    ("C14", "BAE MEO Epoch 2 안테나 선정", "보도(회사 발표 인용)", "2026-06-02", "https://www.satellitetoday.com/government-military/2026/06/02/mda-space-to-supply-antennas-to-bae-systems-for-epoch-2-missile-warning-constellation/", "미사일 경보(통신 아님). 금액 비공개."),
    ("C15", "RADARSAT 보충위성 C$688M", "보도(회사 발표 인용)", "2026-06", "https://spaceq.ca/mda-space-moves-to-build-phase-with-688m-radarsat-replenishment-satellite-contract-award/", "+C$45M 별도."),
    ("C16", "몬트리올 대량생산 공장 개소", "회사 공식 발표", "2026-05", "https://mda.space/article/mda-space-inaugurates-high-volume-satellite-manufacturing-facility-in-montreal", "연 최대 400기는 회사 전망치."),
    ("C17", "L3Harris SDA Tranche 1 추적위성 안테나", "회사 공식 발표", "2023-06-07", "https://mda-en.investorroom.com/2023-06-07-MDA-SELECTED-BY-L3HARRIS-FOR-SPACE-DEVELOPMENT-AGENCYS-TRANCHE-1-TRACKING-LAYER-CONSTELLATION", "14 flight sets. 금액 비공개."),
    ("C18", "MDA FY2025 연결재무제표(감사보고서)", "회사 공식 실적", "2026-03", "https://filecache.investorroom.com/mr5ircnw_mda/685/MDA_Space_Ltd_Q4_2025_FS.pdf", "핵심감사사항(총예정원가 추정). 수익인식 주석 원문은 미확인."),
    ("C19", "C$600M 2033 사채 발행 종결", "회사 공식 발표(재게시)", "2026-08-05", "https://smb.grandforksgazette.ca/article/MDA-SPACE-ANNOUNCES-CLOSING-OF-Cdollar600-MILLION-OFFERING-OF-SENIOR-UNSECURED-NOTES-DUE-2033/6a733f359ca6f9e041dc83c0", "BCT 대금 조달."),
    ("C20", "CSG Schedule 13D", "SEC 공시", "2026-10~11", "SEC EDGAR(정확한 URL 미기재) — B03 인용", "9.5% 취득, 현금결제 스왑."),
    ("C21", "7월 증자 Prospectus Supplement", "SEC 공시", "2026-07", "https://www.sec.gov/Archives/edgar/data/0001857047/000110465926082327/tm2619705-6_suppl.htm", "US$35.60 × 23M주."),
    ("T01", "3Q26 컨퍼런스콜 전사본(Motley Fool)", "경영진 발언", "2026-11-05", "https://www.fool.com/earnings/call-transcripts/2026/11/05/mda-space-mda-q3-2026-earnings-call-transcript/", "일부 문장 깨짐. 인용 전 음성 대조 권장. 보조: https://www.benzinga.com/news/26/11/62923439/mda-space-q3-2026-earnings-call-transcript"),
    ("G01", "캐나다 국방투자청 ESCP-P 계약 발표", "정부 공식 발표", "2026-08", "https://www.canada.ca/en/defence-investment-agency/news/2026/08/the-government-of-canada-awards-a-military-communications-contract-to-support-arctic-sovereignty-and-national-security.html", "LEO C$2.3B(Telesat), MEO 프라임 MDA·하청 Telesat(다음 단계)."),
    ("G02", "캐나다 국방산업전략", "정부 공식 발표", "2026-02", "https://www.canada.ca/en/global-affairs/news/2026/02/canada-advances-defence-industrial-strategy-to-strengthen-security-sovereignty-and-prosperity.html", "우주 = 10대 주권 역량, 10년 국내 조달 C$180B."),
    ("G03", "캐나다 Budget 2026 5장 / PBO 국방지출 프라이머", "정부 자료", "2026", "https://budget.canada.ca/2026/report-rapport/chap5-en.html", "국방비 경로. 우주 항목 숫자는 거의 없음."),
    ("G04", "캐나다–EU 협력 발표(IRIS² 탐색 협의)", "정부 공식 발표", "2026-10-30", "https://www.pm.gc.ca/en/news/news-releases/2026/10/30/canada-and-european-union-announce-new-alliance-future-create-greater", "IRIS² ATP 발표일과 같은 날."),
    ("W01", "Breaking Defense: Novaspace 위성 시장 전망", "보도(외사 보고서 요약)", "2025-10", "https://breakingdefense.com/2025/10/defense-to-anchor-exploding-satellite-market-over-next-decade-novaspace/", "7% 개방·70% 캡티브, 메가 군집 66%/11%, 국방 9%/48%. 원보고서 유료 미열람."),
    ("W02", "Payload: Novaspace 43,000기 전망", "보도", "2025-10", "https://payloadspace.com/novaspace-predicts-43000-new-sats-to-launch-by-2034/", ""),
    ("W03", "SIA State of the Satellite Industry Report(29판)", "업계 통계(요약)", "2026-05-13", "https://sia.org/news-resources/state-of-the-satellite-industry-report/", "전문 유료. 요약·보도 기준."),
    ("W04", "SpaceX 상장 신고서 요약(HL)", "보도", "2026-06-12", "https://www.hl.co.uk/news/inside-spacexs-ipo-filing-revenue-starlink-ai-and-key-financials", "2025 매출 187억 달러, Starlink 61%. S-1 원문 대조 전."),
    ("W05", "SpaceX 상장 첫날(Benzinga)", "보도", "2026-06-12", "https://cdn2.benzinga.com/markets/ipos/26/06/53180108/spacex-stock-closes-up-19-in-record-shattering-ipo-debut", "공모가 135, 종가 160.95."),
    ("W06", "Starlink 3Q26 가입자·ARPU", "보도", "2026-10-20", "https://broadbandbreakfast.com/starlink-reaches-13-6-million-subscribers-globally-as-spacex-revenue-jumps-161/", "ARPU: https://www.fierce-network.com/broadband/starlink-broadband-marches-onward-16m-new-global-subs-q3"),
    ("W07", "Amazon의 Globalstar 인수·FCC 승인", "고객 공식 발표·보도", "2026-04 / 2026-10", "https://www.aboutamazon.com/news/company-news/amazon-globalstar-apple", "FCC 승인: https://www.satellitetoday.com/connectivity/2026/10/27/amazon-secures-fcc-approval-for-globalstar-acquisition/"),
    ("W08", "Globalstar 3Q26 8-K / 10-Q", "고객 SEC 공시", "2026-11-05", "https://www.sec.gov/Archives/edgar/data/0001366868/000136686826000045/gsat20260930-ex991.htm", "MDA 계약 집행액·지체상금 권리(10-Q 기준, B03 인용)."),
    ("W09", "Via Satellite: Telesat 3Q26·Lightspeed 지연·소버린 수요", "보도", "2026-10-29", "https://www.satellitetoday.com/finance/2026/10/29/telesat-delays-lightspeed-service-entry-to-mid-2028-goldberg-addresses-launch-crunch-and-sovereign-demand/", "Telesat 콜 원문은 미열람."),
    ("W10", "Telesat GEO 부채·채권단 재자본화안", "보도", "2026-10", "https://spaceq.ca/telesat-lenders-3-2-billion-rescue-december-default/", "보조: https://www.spaceintelreport.com/telesat-lightspeed-constellation-on-track-user-terminals-1-7b-debt-maturity-in-december-unresolved/ · 11월 타결 여부 미확인."),
    ("W11", "SpaceQ: EchoStar 계약 해지", "보도", "2025-09", "https://spaceq.ca/echostar-cancels-1-8b-contract-with-mda-space/", "C$1.8B는 환산 표기."),
    ("W12", "IRIS² 이행 합의·제조 배분", "보도·회사 발표", "2026-08~09", "https://runwaygirlnetwork.com/2026/08/iiris%C2%B2-deployment-with-enhanced-security-expanded-satellites-network/", "Aerospacelab €2.4B, Thales €500M 첫 트랜치, OHB MEO."),
    ("W13", "SatNews: MDA IRIS² Thales ATP C$100M+", "보도(회사 발표 인용)", "2026-11-02", "https://satnews.com/2026/11/02/mda-space-secures-c100m-thales-alenia-space-award-for-first-66-iris%C2%B2-satellites/", "Thales 독립 확인 없음."),
    ("W14", "독일 군사우주 €35B / SATCOMBw 4", "보도", "2026-02 / 2026-10", "https://satnews.com/2026/02/28/germany-commits-e35-billion-to-leo-resilience-and-non-kinetic-deterrence/", "계획·예산이며 계약 아님."),
    ("W15", "미 우주군 SDN 백본 SpaceX 계약 / SDA Transport T3 미예산", "보도", "2026-04~05", "https://defensescoop.com/2026/05/27/space-force-awards-spacex-contract-backbone-satcom-network/", "보조: https://breakingdefense.com/2026/04/space-force-shifts-from-sda-transport-layer-to-new-space-data-network-backbone-for-orbital-relay/"),
    ("W16", "한국 K-LEO 계획 확정 / 한화–MDA 협력", "보도", "2026-07-06 / 2026-01-26", "https://satnews.com/2026/07/06/south-korea-formally-ratifies-2035-k-starlink-low-earth-orbit-constellation-plan/", "제조 발주 없음."),
    ("W17", "Mitsubishi Electric 방위통신위성 수주", "고객 공식 발표", "2026-02-06", "https://www.mitsubishielectric.com/en/pr/2026/0206-b/", "JPY 1,235억."),
    ("W18", "Rocket Lab: MDA 하청 Globalstar 버스 17기", "파트너 공식 발표·SEC 공시", "2022-02-24", "https://rocketlabcorp.com/updates/rocket-lab-selected-by-mda-to-design-and-build-spacecraft-for-globalstar/", "SEC 424B3: https://www.sec.gov/Archives/edgar/data/1819994/000119312522052423/d900616d424b3.htm · US$143M."),
    ("W19", "유럽 Project Bromo", "보도", "2026-10-16", "https://www.grosswald.org/europe-space-merger-project-bromo-airbus-leonardo-thales-ohb-opposition/", "일정은 규제 승인 조건부."),
    ("W20", "피어 실적: York 1Q26 / Rocket Lab 잔고", "회사 실적·보도", "2026", "https://www.businesswire.com/news/home/20260514013419/en/York-Space-Systems-Reports-First-Quarter-2026-Results", "Rocket Lab 잔고는 2차 자료(8-K 대조 전)."),
    ("W21", "Intuitive Machines 8-K: Lanteris 인수 완료", "SEC 공시(요약)", "2026-01-13", "https://www.boardroomalpha.com/sec/lunr-8-k-2026-01-13-0001193125-26-011200", "8억 달러."),
    ("W22", "Rocket Lab의 Iridium 인수", "회사 공식 발표", "2026-06-29", "https://www.nasdaq.com/press-release/rocket-lab-acquire-iridium-historic-deal-creating-fully-vertically-integrated-space-0", "EV 약 80억 달러."),
    ("W23", "BCT 인수 보도(Via Satellite / SpaceQ)", "보도", "2026-06-22", "https://www.satellitetoday.com/manufacturing/2026/06/22/mda-space-to-acquire-blue-canyon-from-raytheon-to-reach-us-defense-market/", "SpaceQ(CEO 'emergency supplier'): https://spaceq.ca/mda-space-acquires-blue-canyon-technologies-in-u-s-space-defence-push/ · FOCI는 해설 수준."),
    ("W24", "CLS 인수 보도(Yahoo Finance 등)", "보도", "2026-07", "https://finance.yahoo.com/technology/ai/articles/mda-space-bets-567m-cls-060157230.html", ""),
    ("W25", "SpaceQ: C$600M 사채·S&P 'B' 보도", "보도", "2026-08", "https://spaceq.ca/mda-space-issues-600-million-in-senior-notes-to-finance-u-s-expansion/", "S&P 원문 미확인. 기사 이미지에 AI 생성 표기."),
    ("W26", "Canadarm3 달 표면 전용", "보도", "2026", "https://aviationweek.com/space/space-exploration/canada-pivots-canadarm3-lunar-exploration", ""),
    ("W27", "SpaceQ: CHORUS 약정 41건", "보도", "2026", "https://spaceq.ca/mda-space-reports-41-commitments-for-chorus-ahead-of-launch/", ""),
    ("W28", "공장 램프업(Kratos / Space Intel Report)", "보도", "2026", "https://www.kratosspace.com/constellations/articles/mda-space-2-sats-per-day-plant-opens-by-december-but-telesat-globalstar-production-to-start-slowly", "'하루 2기'는 회사 전망."),
    ("W29", "Starlink와 러-우 전쟁(Crimea 거절·지오펜싱)", "보도 종합", "2022~2026", "https://en.wikipedia.org/wiki/Starlink_in_the_Russo-Ukrainian_War", "Musk 발언: https://imi.org.ua/en/news/musk-says-he-refused-to-activate-starlink-near-crimea-due-to-us-sanctions-against-russia-i55341 · 위키는 보조 출처로만."),
    ("W30", "Reuters: 광물 협상과 Starlink 차단 거론", "보도(익명 소식통)", "2025-02-22", "https://www.kyivpost.com/post/47634", "Reuters 원문 재게시 기준. Musk 부인. 미국 정부 공식 확인 없음."),
    ("W31", "온타리오주 Starlink C$1억 계약 취소", "보도", "2025-02~03", "https://techcrunch.com/2025/02/03/ontario-cancels-100-million-starlink-contract-in-protest-at-u-s-tariffs", "보조: https://betakit.com/its-done-its-gone-ontario-premier-doug-ford-cancels-100-million-starlink-contract-in-tariff-response/"),
    ("W32", "Breaking Defense: Shotwell 'Starlink 무기화 의도 없음'", "보도(경영진 발언)", "2023-02", "https://breakingdefense.com/2023/02/spacex-didnt-intend-that-starlink-be-weaponized-by-ukraine-shotwell", "약관 원문 아님."),
    ("W33", "영국 국방부 Starshield 사용 확인(Reuters 2차)", "보도", "2026-09-11", "https://247wallst.com/investing/2026/09/11/britain-just-admitted-it-uses-spacexs-secret-military-network-the-contracts-already-top-6-billion/", "2차 보도."),
    ("W34", "차세대중형위성 2호(KAI) / 425 사업", "보도", "2026-05 / 2025-11", "https://www.sidae.com/article/2026050408254174268", "425: https://www.dailian.co.kr/news/view/1570357/ · 금액은 언론 보도 기준."),
    ("W35", "Thinking in Multiples: MDA Space 리서치", "독립 리서치", "2026", "https://thinkinginmultiples.substack.com/p/research-report-mda-space", "잔고 73% Telesat·Globalstar. 공시치 아님."),
    ("W36", "MarketBeat: JPMorgan 목표가 하향 / StockAnalysis", "보도·시장 데이터", "2026-11-10", "https://www.marketbeat.com/instant-alerts/analyst-mda-space-nyse-mda-stock-price-target-cut-by-jpmorgan-chase-co-2026-11-10/", "컨센서스는 집계 사이트 기준."),
    ("W37", "호주 JP9102 취소", "보도", "2024-11-05", "https://www.satellitetoday.com/government-military/2024/11/05/australia-cancels-satellite-effort-with-lockheed-martin-to-prioritize-multi-orbit-solution", ""),
    ("W38", "이탈리아 보안 통신(Starlink 논의 정체)", "보도", "2026-05-26", "https://whbl.com/2026/05/26/canadas-telesat-eyes-secure-italian-satellite-connectivity-contract-sources-say/", ""),
    ("W39", "Defense News: Novaspace 우주 국방 예산", "보도", "2026-09-15", "https://www.defensenews.com/space/2026/09/15/space-based-isr-launches-to-grow-fourfold-in-next-decade-novaspace-says/", ""),
    ("W40", "SpaceNexus: SPCX 상장 두 달 회고", "보도", "2026-08", "https://spacenexus.us/blog/spcx-stock-since-ipo-h2-2026-outlook", "시점 불명확. 11월 시세는 별도 확인."),
    ("B01", "브랜치 노트: MDA 딥다이브(BM 해부·투자포인트 검증)", "기존 리서치 노트", "2026-11-13", "branch claude/practical-mccarthy-g6kvct : research/mda-space-deep-dive.md → 사본 research/mda/branch_notes/B01_mda-space-deep-dive.md", "[1차]/[2차]/[추정] 표기 유지. 2차 수치는 원문 대조 필요."),
    ("B02", "브랜치 노트: M1/M2 소버린 수요와 캐나다 밖 점유 검증", "기존 리서치 노트", "2026-11-13", "branch claude/elegant-cerf-tmeeqn : study/MDA/study_v2/verification/M1_M2_sovereign_demand.md → 사본 B02_M1_M2_sovereign_demand.md", "발주 집계는 직접 집계(등급 3). hopeful-galileo 판(이전 버전)보다 이 판을 우선."),
    ("B03", "브랜치 노트: M3/M4 회사 검증(잔고·고객·인수·밸류)", "기존 리서치 노트", "2026-11-13", "branch claude/elegant-cerf-tmeeqn : study/MDA/study_v2/verification/M3_M4_company.md → 사본 B03_M3_M4_company.md", "분기 보도자료 24건 추출."),
    ("B04", "브랜치 노트: MDA narrative.json(가설 H1~H5)", "기존 리서치 노트", "2026-11-13", "branch claude/elegant-cerf-tmeeqn : study/MDA/study_v2/narrative.json → 사본 B04_narrative.json", "승인 전 초안."),
    ("B05", "브랜치 데이터: 분기 시계열 quarterly.csv", "기존 데이터", "2026-11-13", "branch claude/elegant-cerf-tmeeqn : study/MDA/data/quarterly.csv → 사본 B05_quarterly.csv", "C$M. 일부 4분기는 역산."),
    ("B06", "브랜치 노트: MDA 투자포인트 v2", "기존 리서치 노트", "2026-11-13", "branch claude/hopeful-galileo-se2znn : study/SPACE/MDA_투자포인트_v2.md → 사본 B06_MDA_투자포인트_v2.md", "'내 추정'·'눈대중' 표기 유지."),
    ("B07", "브랜치 노트: MDA·BlackSky 칠판개요", "기존 리서치 노트", "2026-11-13", "branch claude/hopeful-galileo-se2znn : study/SPACE/MDA_BKSY_칠판개요.md → 사본 B07_MDA_BKSY_칠판개요.md", "MDA 투자포인트 v1은 B06으로 대체됨."),
    ("B08", "브랜치 노트: 3Q26 콜 정리·회사 개요·추적 레지스터", "기존 리서치 노트", "2026-11-13", "branch claude/laughing-ride-qdcywi : space/companies/mda-space/ → 사본 B08_Q3_2026_concall_overview_tracking.md", "녹취록 직접 읽음(source_rank 1)."),
    ("B09", "브랜치 노트: 우주산업 밸류체인 정리", "기존 리서치 노트", "2026-11-12", "branch claude/ecstatic-clarke-fbv4xc : claude/01_우주산업_밸류체인_정리_2026-11-12.md → 사본 B09_우주산업_밸류체인_정리.md", "S### 출처는 원 브랜치 market-intel/valuechain/space/sources.jsonl."),
    ("Q01", "대화 Q&A: SpaceX 의존과 탈피의 의미", "대화 정리(리서치 해석)", "2026-11-13~15", "research/mda/MDA_리서치노트_층위별.md §03", "사례 출처는 W29~W33로 교체·보강."),
    ("Q02", "대화 Q&A: MDA vs SpaceX", "대화 정리(리서치 해석)", "2026-11-13~15", "research/mda/MDA_리서치노트_층위별.md §14", "SpaceX 상장 수치는 W04·W05·W40으로 정정."),
    ("Q03", "대화 Q&A: 다른 나라 위성은 누가 만드나", "대화 정리(리서치 해석)", "2026-11-13~15", "research/mda/MDA_리서치노트_층위별.md §05", "납품 수량·금액은 원문 보도자료로 맞출 것."),
    ("Q04", "대화 Q&A: BCT·CLS 인수와 레버리지", "대화 정리(리서치 해석)", "2026-11-13~15", "research/mda/MDA_리서치노트_층위별.md §12", "순차입 계산은 개략(수수료·운전자본 제외)."),
    ("Q05", "대화 Q&A: 프라임 계약과 매출 인식 시점", "대화 정리(리서치 해석)", "2026-11-13~15", "research/mda/MDA_리서치노트_층위별.md §10·§11", "S자 곡선 비율은 추정."),
    ("Q06", "대화 Q&A: 설계 능력·피어·해자", "대화 정리(리서치 해석)", "2026-11-13~15", "research/mda/MDA_리서치노트_층위별.md §13", "피어 시총은 시세로 재확인."),
    ("Q07", "대화 Q&A: 한국의 위성 설계 구조", "대화 정리(리서치 해석)", "2026-11-13~15", "research/mda/MDA_리서치노트_층위별.md §05", "차중·425는 W34로 보강. 기관 역할은 우주항공청·KAI 자료로 재확인."),
]
