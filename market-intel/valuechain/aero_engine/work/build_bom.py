"""aero_engine bom.json 빌더 — V0(무하네스) + 검색 보강 + V1 채움. 실행: python3 aero_engine/work/build_bom.py (valuechain 폴더에서)"""
import json, sys
sys.path.insert(0, "_contracts")
from v0_helpers import *

N = json.load(open("aero_engine/work/v0_blind.json"))["nodes"]

# ── V0 보강(검색 뒤 추가된 칸) ─────────────────────────────────────────
N += [
 I("sv.exec.slot_new", "sv.exec", "service_ip", "신형 엔진(LEAP·GTF) 정비 슬롯", "OEM 네트워크와 라이선스 받은 소수 숍만 수행. LEAP Shop Visit은 2030년까지 연 25% 성장 전망, TAT 약 100일"),
 S("sv.alt", "sv", "항공 밖 경쟁 용도", "같은 코어·주조품·정비 인력을 두고 항공사와 경쟁하는 수요. AI 독립성 판정에 필요한 칸"),
 I("sv.alt.power", "sv.alt", "service_ip", "퇴역 코어의 발전용 전환", "CFM56 코어를 약 25MW 발전 터빈으로 개조해 데이터센터에 공급. 중고 부품 공급을 줄이고 엔진 가치를 받친다"),
 I("sv.alt.igt", "sv.alt", "component", "발전용 가스터빈 주조·초합금", "항공 엔진과 같은 주조 라인·초합금 용해로를 쓴다. 데이터센터 전력 수요가 항공용 물량과 경쟁"),
]
P_ = fill(N, "sv",
    price=val(6.8, "백만 USD/회", "S101", "②", "FTAI IR 자료의 CFM56 Shop Visit 비용(LLP 포함, 약 3년 전 수치·회사 주장). 2026년 벤더 자료는 성능복원만 200~450만 달러로 제시(S102)", "2023"),
    note="시장 Q: CFM56 Shop Visit 2026·2027년 각 2,300~2,400회, GE는 상단 예상(S103). CFM56 운용 약 19,000~20,000대, 2026년 퇴역률 전망 3~4% → 1.5~2%로 하향(S105). 엔진 정비는 2026년 민항 애프터마켓 1,390억 달러의 53%(S117). 반대 신호: CFM56 엔진 가치가 2026년 상반기 횡보(S119)")

SH = "미측정 — 점유율 원천 미확보"
svc = "없음 — 서비스라 수량 축이 성립하지 않음"
unk_q = "미측정 — 엔진 매뉴얼 기준 수량 미확인"
unk_p = "미측정 — 단가 원천 미확보"
unk_c = "미측정 — 비용 분해 원천 미확보"

fill(N, "sv.exec.slot", qty_per_unit=svc, price=unk_p,
     cost_share_pct=val(7, "%", "S101", "②", "CFM56 Shop Visit 비용 중 인건비(FTAI IR, 회사 주장)", "2023"),
     makers=[
      mk("GE Aerospace", "XNYS:GE", "US", "main", "②", "S121", note="상업 서비스 매출 연초 이후 +20% 이상, 서비스 수주잔고 1,700억 달러 이상, 자체 Shop Visit 처리량 분기 최고"),
      mk("Safran", "XPAR:SAF", "FR", "main", "①", "S111", note="3Q26 추진 애프터마켓 +18.7%. 민수 부품 달러 성장률 1Q +29.3% → 2Q +26.7% → 3Q +17.0%로 둔화"),
      mk("MTU Aero Engines", "XETR:MTX", "DE", "main", "①", "S112", note="1H26 민수 정비 매출 34억 유로(+21%, 달러 +29%)"),
      mk("StandardAero", "XNYS:SARO", "US", "main", "②", "S110", note="3Q26 매출 +4.0%, Engine Services EBITDA +24%. 가이던스 4분기 연속 상향"),
      mk("FTAI Aviation", "XNAS:FTAI", "US", "second", "②", "S105", share=val(15, "%", "S105", "②", "CFM56 정비 시장 내 점유율(회사 주장, 3Q26)"), note="3Q26 모듈 311개, 2026년 1,200개·2027년 1,700개 목표"),
      mk("Lufthansa Technik", None, "DE", "main", "③", "S000", parent="Deutsche Lufthansa", pt="XETR:LHA"),
      mk("ST Engineering", "XSES:S63", "SG", "second", "③", "S000"),
      mk("AFI KLM E&M", None, "FR", "second", "③", "S000", parent="Air France-KLM", pt="XPAR:AF"),
     ], open_questions=["OEM 직영 대 독립 MRO의 CFM56 물량 비중(원천 못 찾음)", "숍별 처리량과 TAT"])
fill(N, "sv.exec.slot_new", qty_per_unit=svc, price=unk_p, cost_share_pct="없음 — 기준 단위가 CFM56이라 신형 엔진 비용은 분모 밖",
     makers=[
      mk("GE Aerospace", "XNYS:GE", "US", "main", "②", "S104", note="LEAP Shop Visit 2024년 기준 2030년까지 연 25% 성장 전망"),
      mk("Safran", "XPAR:SAF", "FR", "main", "①", "S111", note="LEAP 인도 3Q26 535대, 9개월 1,565대(+26%)"),
      mk("RTX (Pratt & Whitney)", "XNYS:RTX", "US", "main", "①", "S120", note="3Q26 Pratt 민수 애프터마켓 +21%(GTF 물량)"),
      mk("MTU Aero Engines", "XETR:MTX", "DE", "second", "③", "S000", note="GTF 프로그램 파트너"),
      mk("StandardAero", "XNYS:SARO", "US", "second", "②", "S110", note="LEAP 라인 확대 중, 초기에는 마진 희석"),
     ])
fill(N, "sv.exec.testcell", qty_per_unit=svc, price=unk_p, cost_share_pct=unk_c,
     makers=[mk("MDS Aero Support", None, "CA", "main", "③", "S000"),
             mk("Safran Test Cells", None, "FR", "main", "③", "S000", parent="Safran", pt="XPAR:SAF")],
     open_questions=["테스트 셀이 정비 병목이라는 보도(S124)의 규모", "상장 순수 노출 기업이 있는지"])
fill(N, "sv.exec.exchange", qty_per_unit=svc, price="미측정 — CFM56 리스료 원천 미확보(일부 기종 최대 +40% 보도, 기준일 불명)", cost_share_pct=unk_c,
     makers=[mk("FTAI Aviation", "XNAS:FTAI", "US", "main", "②", "S125", note="CFM56 최대 보유자로 소개. 리스 부문은 자산 경량화로 EBITDA 감소"),
             mk("Willis Lease Finance", "XNAS:WLFC", "US", "second", "③", "S000"),
             mk("AerCap", "XNYS:AER", "IE", "second", "③", "S000"),
             mk("GA Telesis", None, "US", "second", "③", "S000")])
fill(N, "sv.parts.hpt", qty_per_unit=unk_q, price=unk_p,
     cost_share_pct=val(58, "%", "S101", "②", "CFM56 Shop Visit 비용 중 에어포일 전체(HPT 외 포함, FTAI IR·회사 주장)", "2023"),
     makers=[
      mk("GE Aerospace", "XNYS:GE", "US", "main", "③", "S000", note="CFM 순정 부품 공급(Safran과 50:50)"),
      mk("Safran", "XPAR:SAF", "FR", "main", "③", "S000"),
      mk("Howmet Aerospace", "XNYS:HWM", "US", "main", "②", "S122", note="3Q26 매출 +29%. 가스터빈 매출 +45%라 AI 전력 수요와 섞임"),
      mk("Precision Castparts", None, "US", "main", "③", "S000", parent="Berkshire Hathaway", pt="XNYS:BRK.B"),
      mk("Chromalloy", None, "US", "qualifying", "②", "S108", parent="Veritas Capital(비상장 PE)", note="CFM56-5B/7B HPT 블레이드 PMA 2025년 10월 FAA 승인. 유일한 비순정 대안이라는 회사 주장. FTAI와 협력"),
     ], open_questions=["HPT 블레이드가 CFM56 오버홀의 최대 제약이라는 보도(S106)의 물량 기준", "순정 블레이드 카탈로그 가격 인상률(원천 못 찾음)"])
fill(N, "sv.parts.llp", qty_per_unit=val([14, 18], "개/세트", "S102", "②", "CFM56-7B LLP 한 세트 부품 수(벤더 자료)"),
     price=val([1.1, 1.6], "백만 USD/세트", "S102", "②", "신품 LLP 한 세트(벤더 자료, 페이지마다 수치 다름)"),
     cost_share_pct=val(23, "%", "S101", "②", "CFM56 Shop Visit 비용 중 LLP(FTAI IR·회사 주장)", "2023"),
     makers=[mk("GE Aerospace", "XNYS:GE", "US", "main", "③", "S000"), mk("Safran", "XPAR:SAF", "FR", "main", "③", "S000")])
fill(N, "sv.parts.pma", qty_per_unit=unk_q, price="미측정 — 순정 대비 할인율 원천 미확보", cost_share_pct=unk_c,
     makers=[mk("HEICO", "XNYS:HEI", "US", "main", "①", "S109", note="FY26 3Q Flight Support 매출 9.478억 달러(+18%, 유기적 +12%), 영업이익 +24%"),
             mk("Chromalloy", None, "US", "second", "②", "S108", parent="Veritas Capital(비상장 PE)", note="CFM56-5B/7B용 PMA 4종"),
             mk("Jet Parts Engineering", None, "US", "second", "②", "S108", note="2026년 3월 PMA 5종 승인")],
     open_questions=["PMA가 CFM56 부품 시장에서 차지하는 비중", "리스사가 PMA 장착 엔진을 받는지"])
fill(N, "sv.parts.usm", qty_per_unit=unk_q, price=unk_p, cost_share_pct=unk_c,
     makers=[mk("AerSale", "XNAS:ASLE", "US", "main", "③", "S000"), mk("FTAI Aviation", "XNAS:FTAI", "US", "main", "③", "S000"),
             mk("AAR", "XNYS:AIR", "US", "second", "③", "S000"), mk("VSE", "XNAS:VSEC", "US", "second", "③", "S000"),
             mk("AerFin", None, "GB", "second", "②", "S106", note="잔여 수명 긴 블레이드 중고 물량이 줄었다고 발언")],
     open_questions=["해체 기재 수 추이(퇴역률 1.5~2%)와 USM 가격"])
fill(N, "sv.parts.acc", qty_per_unit=unk_q, price=unk_p, cost_share_pct=unk_c,
     makers=[mk("TransDigm", "XNYS:TDG", "US", "main", "①", "S113", note="FY27 매출 가이던스 119.5~121.5억 달러(FY26 105.57억, 중간값 +14%)"),
             mk("RTX (Collins)", "XNYS:RTX", "US", "main", "①", "S120", note="3Q26 Collins 민수 애프터마켓 +9%"),
             mk("Honeywell Aerospace", "XNAS:HONA", "US", "main", "①", "S120", note="3Q26 민수 애프터마켓 +2%, 기계 부품 조달이 제약"),
             mk("Woodward", "XNAS:WWD", "US", "second", "③", "S000"), mk("Loar Holdings", "XNYS:LOAR", "US", "second", "③", "S000"),
             mk("Parker-Hannifin", "XNYS:PH", "US", "second", "③", "S000")])
fill(N, "sv.repair.blade", qty_per_unit=svc, price=unk_p,
     cost_share_pct=val(12, "%", "S101", "②", "CFM56 Shop Visit 비용 중 수리 전체(FTAI IR·회사 주장)", "2023"),
     makers=[mk("Chromalloy", None, "US", "main", "③", "S000", parent="Veritas Capital(비상장 PE)"),
             mk("StandardAero", "XNYS:SARO", "US", "main", "②", "S110", note="Component Repair 매출 +7%, 마진 25.8%로 4.9%p 하락"),
             mk("MTU Aero Engines", "XETR:MTX", "DE", "main", "③", "S000"),
             mk("HEICO", "XNYS:HEI", "US", "second", "③", "S000")])
fill(N, "sv.repair.heat", qty_per_unit=svc, price=unk_p, cost_share_pct=unk_c,
     makers=[mk("Bodycote", "XLON:BOY", "GB", "main", "③", "S000"), mk("Linde (Praxair Surface Technologies)", "XNAS:LIN", "US", "main", "③", "S000"),
             mk("OC Oerlikon", "XSWX:OERL", "CH", "second", "③", "S000")])
fill(N, "sv.mat.ni", qty_per_unit=unk_q, price=unk_p, cost_share_pct=unk_c,
     makers=[
      mk("Carpenter Technology", "XNYS:CRS", "US", "main", "①", "S114", note="1Q FY27 영업이익 1.964억 달러(+28%), SAO 마진 37.7%, 항공 구조재·유통 수주 +49%. FY29 영업이익 목표 12~13억 달러"),
      mk("ATI", "XNYS:ATI", "US", "main", "②", "S115", note="5번째 VIM로 2H27 가동, 약 9,000t/년(용량 +8~10%)"),
      mk("Special Metals / Cannon Muskegon", None, "US", "main", "③", "S000", parent="Berkshire Hathaway(PCC)", pt="XNYS:BRK.B"),
      mk("Acerinox (VDM·Haynes)", "XMAD:ACX", "ES", "second", "③", "S000"),
      mk("Aubert & Duval", None, "FR", "second", "②", "S115", parent="Airbus·Safran·Tikehau 컨소시엄", pt="XPAR:SAF", note="Safran과 LEAP 단조품 계약 갱신"),
      mk("Cogne Acciai Speciali (SMP)", None, "IT", "second", "②", "S115", parent="Walsin Lihwa", pt="XTAI:1605", note="18t VIM 신설, Rolls-Royce 계약 약 2.4억 달러"),
      mk("Doncasters", None, "GB", "second", "②", "S115", note="앨라배마 초합금 공장 5,000만 달러 투자"),
     ], open_questions=["업체별 엔진용 초합금 용해 점유율(원천 못 찾음)", "신규 용량은 2027년 말~2030년에 가동되고 항공·방산·가스터빈이 나눠 쓴다(S115) — 항공 몫"])
fill(N, "sv.mat.ti", qty_per_unit=unk_q, price=unk_p, cost_share_pct=unk_c,
     makers=[
      mk("ATI", "XNYS:ATI", "US", "main", "②", "S116", share=val(26.7, "%", "S116", "②", "항공 티타늄 시장 2025년(시장조사 보고서, 신뢰도 낮음)", "2025")),
      mk("VSMPO-AVISMA", None, "RU", "historical", "②", "S116", share=val([20, 25], "%", "S116", "②", "항공 티타늄(공급자 가이드, 신뢰도 낮음)", "2025"), note="제재·탈러시아로 이탈 중"),
      mk("TIMET", None, "US", "main", "③", "S000", parent="Berkshire Hathaway(PCC)", pt="XNYS:BRK.B"),
      mk("Howmet Aerospace", "XNYS:HWM", "US", "second", "③", "S000"),
      mk("Toho Titanium", "XTKS:5727", "JP", "main", "②", "S116", note="스펀지 +3,000t(2026년 1월)"),
      mk("OSAKA Titanium Technologies", "XTKS:5726", "JP", "main", "②", "S116", note="스펀지 +10,000t(2028년 3월). SMIC 2024.05 커버"),
     ], open_questions=["항공·방산 스펀지 수요 7.9만t(2024) → 9.0만t(2028) → 10.2만t(2031) 전망(Toho, S116)의 엔진 등급 몫"])
fill(N, "sv.mat.forge", qty_per_unit=unk_q, price=unk_p, cost_share_pct=unk_c,
     makers=[mk("Precision Castparts (Wyman-Gordon)", None, "US", "main", "③", "S000", parent="Berkshire Hathaway", pt="XNYS:BRK.B"),
             mk("ATI", "XNYS:ATI", "US", "main", "③", "S000"), mk("Howmet Aerospace", "XNYS:HWM", "US", "main", "③", "S000"),
             mk("Aubert & Duval", None, "FR", "main", "②", "S115", parent="Airbus·Safran·Tikehau 컨소시엄", pt="XPAR:SAF"),
             mk("Safran", "XPAR:SAF", "FR", "captive", "②", "S115", note="30,000t 프레스 가동, 회전체 라인 2029년")])
fill(N, "sv.mat.cast", qty_per_unit=unk_q, price=unk_p, cost_share_pct=unk_c,
     makers=[
      mk("Precision Castparts", None, "US", "main", "②", "S122", parent="Berkshire Hathaway", pt="XNYS:BRK.B", note="Howmet과 단결정 블레이드 사실상 복점"),
      mk("Howmet Aerospace", "XNYS:HWM", "US", "main", "②", "S122", note="가스터빈 에어포일 세계 점유율 50% 이상(회사 주장, 분모는 발전용)"),
      mk("Consolidated Precision Products", None, "US", "second", "②", "S107", parent="Warburg Pincus·Berkshire Partners → GE Aerospace 인수 예정", pt="XNYS:GE", note="GE가 117.5억 달러에 인수 합의(2026-09-08), 2H27 종결 예정. 2027년 EBITDA의 약 26배"),
      mk("Doncasters", None, "GB", "second", "③", "S000"),
     ], open_questions=["GE의 CPP 인수로 다른 엔진사·MRO의 주조품 조달이 어떻게 바뀌나"])
fill(N, "sv.mat.minor", qty_per_unit=unk_q, price=unk_p, cost_share_pct=unk_c,
     makers=[mk("Molymet", "XSGO:MOLYMET", "CL", "main", "③", "S000", note="레늄"), mk("KGHM", "XWAR:KGH", "PL", "second", "③", "S000", note="레늄")])
fill(N, "sv.mat.cmc", qty_per_unit="없음 — CFM56에는 쓰지 않음(LEAP부터)", price=unk_p, cost_share_pct="없음 — 기준 단위가 CFM56이라 분모 밖",
     makers=[mk("GE Aerospace", "XNYS:GE", "US", "captive", "③", "S000"),
             mk("NGS Advanced Fibers", None, "JP", "main", "③", "S000", parent="Nippon Carbon·GE·Safran 합작", pt="XTKS:5302")])
fill(N, "sv.ip.tc", qty_per_unit=svc, price="미측정 — 카탈로그 가격 인상률 원천 미확보(IATA는 코로나 이전보다 높다고만 언급, S123)", cost_share_pct="없음 — 부품 가격에 녹아 있어 따로 떼지 못함",
     makers=[mk("GE Aerospace", "XNYS:GE", "US", "main", "②", "S121", note="2026년 조정 EPS 가이던스 8.00~8.10달러, 2027년 상업 서비스 두 자릿수 초반 성장 예상"),
             mk("Safran", "XPAR:SAF", "FR", "main", "①", "S111", note="2026년 경상영업이익 가이던스 64~65억 유로"),
             mk("RTX (Pratt & Whitney)", "XNYS:RTX", "US", "main", "①", "S120"),
             mk("Rolls-Royce", "XLON:RR.", "GB", "main", "③", "S000", note="광동체 중심. 발전 사업이 있어 AI 전력과 섞임")])
fill(N, "sv.ip.pbh", qty_per_unit=svc, price=unk_p, cost_share_pct="없음 — 계약 형태라 Shop Visit 비용의 구성 항목이 아님",
     makers=[mk("GE Aerospace", "XNYS:GE", "US", "main", "②", "S121", note="상업 서비스 수주잔고 1,700억 달러 이상"), mk("Safran", "XPAR:SAF", "FR", "main", "③", "S000"),
             mk("RTX (Pratt & Whitney)", "XNYS:RTX", "US", "main", "③", "S000")])
fill(N, "sv.alt.power", qty_per_unit=svc, price=unk_p, cost_share_pct="없음 — 항공 밖 용도라 Shop Visit 비용 분모 밖",
     makers=[mk("FTAI Aviation", "XNAS:FTAI", "US", "main", "②", "S118", note="FTAI Power. 연 100대 이상(대당 약 25MW) 목표, 첫 인도 4Q26 목표. 램프 시점은 2026년·2027년 보도가 엇갈림")],
     open_questions=["전환이 CFM56 USM 공급과 정비 슬롯을 얼마나 잠식하나"])
fill(N, "sv.alt.igt", qty_per_unit="없음 — 항공 밖 수요라 Shop Visit 단위로 셀 수 없음", price=unk_p, cost_share_pct="없음 — 항공 밖 용도라 Shop Visit 비용 분모 밖",
     makers=[mk("Howmet Aerospace", "XNYS:HWM", "US", "main", "②", "S122", note="터빈 고객의 2031년 용량 매진, 가스터빈 매출 +45%"),
             mk("Carpenter Technology", "XNYS:CRS", "US", "second", "③", "S000", note="발전용 비중 확인 필요"), mk("ATI", "XNYS:ATI", "US", "second", "③", "S000")],
     open_questions=["후보별 발전용 가스터빈 매출 비중(10-K)"])

SRC = [
 ("S000", "model_knowledge", "모델 지식", "모델 지식 — 검증 필요", "2026-06", "③", "메이커 실재·역할 등 사전 지식. V4에서 ①②로 교체"),
 ("S101", "web", "https://ir.ftaiaviation.com/static-files/7fd5dafe-1253-4e80-957a-8c5874d5f5bb", "FTAI IR 자료: CFM56 Shop Visit 비용 분해", "2023", "②", "회사 주장. 에어포일 58·LLP 23·수리 12·인건비 7%, 총 680만 달러"),
 ("S102", "web", "https://safefly.aero/engine-shop-visit-costs-2026/", "Safe Fly: 2026 엔진 Shop Visit 비용", "2026", "②", "벤더 사이트, 페이지마다 수치 불일치"),
 ("S103", "web", "https://aviationweek.com/mro/aircraft-propulsion/cfm56-overhaul-demand-remains-strong-ge-aerospace-says", "Aviation Week: CFM56 오버홀 수요", "2026-07", "②", "2026·2027년 2,300~2,400회"),
 ("S104", "web", "https://www.geaerospace.com/news/investor-relations/ir-updates/recent-events-your-questions-answered", "GE Aerospace IR Q&A", "2026", "②", "회사 주장. 퇴역률 약 2%, LEAP Shop Visit 연 25% 성장"),
 ("S105", "web", "https://www.tikr.com/blog/ftai-aviation-soars-14-on-500-million-buyback-as-ceo-sees-clear-visibility-into-2027", "FTAI 3Q26 실적 요약", "2026-10", "②", "회사 주장. 점유율 약 15%, 모듈 311개, 퇴역률 전망 하향"),
 ("S106", "web", "https://aviationweek.com/mro/supply-chain/hpt-blade-supply-crunch-slows-cfm56-overhauls", "Aviation Week: HPT 블레이드 부족", "2026", "②", "AerFin 발언(이해관계자)"),
 ("S107", "web", "https://aviationweek.com/aerospace/manufacturing-supply-chain/ge-aerospace-buy-consolidated-precision-products-12b-deal", "Aviation Week: GE의 CPP 인수", "2026-09-08", "②", "117.5억 달러, 2H27 종결 예정"),
 ("S108", "web", "https://aviationweek.com/mro/safety-ops-regulation/chromalloy-granted-faa-approval-cfm56-turbine-blade", "Chromalloy CFM56 HPT 블레이드 PMA 승인", "2025-10", "②", "회사 주장 포함"),
 ("S109", "web", "https://www.sec.gov/Archives/edgar/data/0000046619/000004661926000018/a07312026ex991earningsrele.htm", "HEICO FY26 3Q 8-K", "2026-08", "①", ""),
 ("S110", "web", "https://finviz.com/news/418164/standardaero-matches-eps-estimates-raises-guidance-a-fourth-time-and-launches-350m-buyback-but-component-repair-margins-keep-slipping", "StandardAero 3Q26 실적 요약", "2026-11", "②", "2차 요약"),
 ("S111", "web", "https://www.safran-group.com/pressroom/safran-reports-its-third-quarter-2026-revenue-2026-10-23", "Safran 3Q26 매출 공시", "2026-10-23", "①", ""),
 ("S112", "web", "https://www.mtu.de/newsroom/press/latest-press-releases/press-release-detail/mtu-aero-engines-remains-on-track-with-growth-in-first-half-of-2026-and-raises-free-cash-flow-guidance/", "MTU 1H26 실적", "2026-07", "①", "9개월 실적은 못 찾음"),
 ("S113", "web", "https://www.sec.gov/Archives/edgar/data/0001260221/000126022126000073/exhibit991tdg2026q4earning.htm", "TransDigm FY26 4Q 8-K", "2026-11", "①", ""),
 ("S114", "web", "https://www.sec.gov/Archives/edgar/data/0000017843/000001784326000049/a1stqtrfy2027results.htm", "Carpenter FY27 1Q 8-K", "2026-10-22", "①", ""),
 ("S115", "web", "https://www.argusmedia.com/en/news-and-insights/latest-market-news/2860247-jet-engines-driving-nickel-pq-titanium-demand", "Argus: 제트엔진발 니켈·티타늄 수요", "2026-07", "②", "ATI·SMP·Doncasters·Aubert & Duval 증설"),
 ("S116", "web", "https://view.ceros.com/argus-media/2025-titanium", "Argus 티타늄 2025 외 시장조사", "2025", "②", "점유율은 시장조사 보고서·블로그 출처라 신뢰도 낮음"),
 ("S117", "web", "https://aviationweek.com/mro/supply-chain/early-2026-outlook-shows-mro-market-momentum-increasing", "Aviation Week: 2026 MRO 전망", "2026", "②", ""),
 ("S118", "web", "https://www.barchart.com/story/news/36824101/ftai-aviation-announces-the-launch-of-ftai-power-ftai-adapts-the-worlds-largest-aircraft-engine-platform-to-meet-ai-driven-power-demand", "FTAI Power 출범 보도자료", "2025-12-30", "②", "회사 주장"),
 ("S119", "web", "https://aerospace-innovations.com/engine-shortages-and-mro-backlog-keep-values-and-lease-rates-elevated-says-iba/", "IBA 1H26: CFM56 엔진 가치 횡보", "2026", "②", ""),
 ("S120", "web", "https://www.rtx.com/news/news-center/2026/10/20/rtx-reports-q3-2026-results", "RTX 3Q26 실적(Honeywell Aerospace 3Q26 포함)", "2026-10", "①", "Honeywell 수치는 investor.honeywellaerospace.com 보도자료"),
 ("S121", "web", "https://www.investing.com/news/transcripts/earnings-call-transcript-ge-aerospace-beats-q3-2026-forecasts-raises-outlook-93CH-4960036", "GE Aerospace 3Q26 콜", "2026-10", "②", "회사 주장"),
 ("S122", "web", "https://www.zacks.com/stock/news/3019783/hwm-q3-earnings-beat-estimates-on-aerospace,-gas-turbine-growth", "Howmet 3Q26 요약, 단결정 블레이드 복점 분석", "2026-10", "②", "점유율 50% 이상은 회사 주장"),
 ("S123", "web", "https://www.iata.org/contentassets/85b59d951fc04c1c83fa2aab47824300/single-aisle-aircraft-engines-mro.pdf", "IATA: 협동체 엔진 MRO", "2026", "②", "OEM 부품가 인상률이 코로나 이전보다 높다는 언급"),
 ("S124", "web", "https://aviationweek.com/mro/supply-chain/magnetic-expands-cfm-engine-mro-face-testing-parts-bottlenecks", "Aviation Week: 테스트·부품 병목", "2026", "②", ""),
 ("S125", "web", "https://inpractise.com/companies/FTAI/profile/ftai-aviation", "In Practise: FTAI 프로필", "2026", "②", ""),
]
write_sources("aero_engine/sources.jsonl", SRC)
dump("aero_engine/bom.json", "aero_engine", "협동체 터보팬 엔진 Shop Visit(애프터마켓)", "CFM56-7B 성능복원 Shop Visit 1회 비용", N,
     status="v3_queued",
     approved={"who": "Claude(본체)", "at": "2026-11-11", "stage": "V0", "note": "무하네스 초안 26노드에 검색으로 4노드(신형 엔진 슬롯, 항공 밖 경쟁 용도 2칸) 보강 후 승인. 레포에 체인 yaml 없음"},
     log=[{"stage": "V0", "at": "2026-11-11", "by": "Claude(본체)", "what": "v0_blind.json 작성 후 검색 보강, v0_diff.md"},
          {"stage": "V1", "at": "2026-11-11", "by": "Claude(본체, 서브 없이 직접)", "what": "입력 22개 메이커·비용 비중 채움. 출처 S101~S125"},
          {"stage": "V2", "at": "2026-11-11", "by": "Claude(본체)", "what": "레포에 core/valuechain yaml이 없어 box_ref 전부 빈칸 문면"},
          {"stage": "V3", "at": "2026-11-11", "by": "Claude(본체)", "what": "GAPS.md·BOM.md·착수 큐"}])
