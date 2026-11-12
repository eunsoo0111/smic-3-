#!/usr/bin/env python3
"""우주 체인 V0 트리 생성기 — 구조만(기업 이름 없음). 산출: work/v0_blind.json · work/v0_tree.json · ../bom.json(v0).

V0 는 「위성 1기를 내가 직접 만들어 쏘고 운용해 돈을 번다면」 순서로 분해한다.
makers 는 전부 「미측정 — V1 대상」. 「안 쓰는 것」은 「없음 — 이유」 행.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASOF = "2026-11-12"
TBD = "미측정 — V1 대상(vc-input-filler 가 채운다)"
NOBOX = "미측정 — V2 대상(core/valuechain/space.yaml 아직 없음)"

N = []


def product(i, name, spec):
    N.append({"id": i, "kind": "product", "parent": None, "name": name, "spec": spec,
              "box_ref": "없음 — 제품 노드는 박스 축 아님", "open_questions": []})


def stage(i, parent, name, spec, q=()):
    N.append({"id": i, "kind": "stage", "parent": parent, "name": name, "spec": spec, "box_ref": NOBOX, "open_questions": list(q)})


def inp(i, parent, typ, name, spec, q=()):
    N.append({"id": i, "kind": "input", "input_type": typ, "parent": parent, "name": name, "spec": spec,
              "qty_per_unit": TBD, "price": TBD, "cost_share_pct": TBD, "makers": TBD, "box_ref": NOBOX, "open_questions": list(q)})


def none(i, parent, typ, name, spec, why):
    b = f"없음 — {why}"
    N.append({"id": i, "kind": "input", "input_type": typ, "parent": parent, "name": name, "spec": spec,
              "qty_per_unit": b, "price": b, "cost_share_pct": b, "makers": b, "box_ref": b, "open_questions": []})


product("space", "우주 산업 전체(위성을 만들어 → 쏘고 → 지상에서 받고 → 서비스로 판다 → 궤도에서 새 사업을 한다)",
        "위성 제조·발사·지상·서비스·궤도상 경제 5단. 기준 단위는 글로벌 우주경제 연 매출(SIA 2025년 4,290억 달러 = 100%)")

# ── 1. 위성 제조 ─────────────────────────────────────────────────────
stage("space.sat", "space", "① 위성 제조(Upstream — 위성 만들기)", "위성 = 버스(몸통: 전력·추진·자세·컴퓨터) + 탑재체(일하는 장비: 안테나·카메라·레이더). 2025년 4,434기 발사")
stage("space.sat.bus", "space.sat", "위성 버스(몸통·플랫폼)", "탑재체를 궤도에서 먹여 살리는 공통 플랫폼 — 구조·전력·추진·자세제어·컴퓨터·열제어·통신")
inp("space.sat.bus.structure", "space.sat.bus", "component", "구조체·기구부", "알루미늄 허니컴·CFRP 패널, 전개 장치(힌지·홀드다운), 태양전지판 구동기(SADA)")
inp("space.sat.bus.solar", "space.sat.bus", "component", "우주용 태양전지·어레이", "III-V 3중접합(GaInP/GaAs/Ge, 효율 30%+) 또는 실리콘(스타링크식 저가), 셀→CIC→패널→전개형 어레이")
inp("space.sat.bus.battery", "space.sat.bus", "component", "우주용 배터리·전력조절기", "리튬이온 셀(18650/대형 각형)·팩, 전력조절분배기(PCDU) — 식(蝕) 구간 전력 공급")
inp("space.sat.bus.ep", "space.sat.bus", "component", "전기추진(홀 추력기)·추진제", "홀 효과/이온 추력기 + 전력처리장치(PPU) + 추진제(제논→크립톤→아르곤) — 궤도 상승·유지·폐기 기동")
inp("space.sat.bus.chemprop", "space.sat.bus", "component", "화학추진(추력기·탱크·밸브)", "하이드라진 단일추진·이원추진·그린 추진제(ASCENT 등) 추력기, 추진제 탱크, 밸브·레귤레이터")
inp("space.sat.bus.adcs", "space.sat.bus", "component", "자세결정·제어(ADCS)", "반작용 휠·CMG·자기토커(구동기) + 별추적기·태양센서·자이로(IMU)·GNSS 수신기(센서)")
inp("space.sat.bus.obc", "space.sat.bus", "component", "탑재컴퓨터·내방사선 반도체", "내방사선(rad-hard)/방사선 내성(rad-tolerant) CPU·FPGA·메모리·전력반도체, 탑재 컴퓨터·데이터 처리기")
inp("space.sat.bus.thermal", "space.sat.bus", "component", "열제어", "다층박막단열재(MLI)·히트파이프·라디에이터·히터·열 루버 — 진공에서 −150~+150℃ 견디기")
inp("space.sat.bus.ttc", "space.sat.bus", "component", "TT&C·데이터 송신기", "S밴드 원격측정·명령 트랜스폰더, X/Ka밴드 고속 데이터 다운링크 송신기·안테나")
none("space.sat.bus.rtg", "space.sat.bus", "component", "원자력 전원(RTG)", "플루토늄-238 방사성동위원소 열전 발전기", "지구궤도 위성은 태양전지로 충분 — 심우주·달 밤 생존용에만 쓴다")

stage("space.sat.payload", "space.sat", "탑재체(위성이 실제로 일하는 장비)", "통신(안테나·중계기)·관측(광학·레이더·적외선)·항법(원자시계) — 위성 값의 절반 안팎")
inp("space.sat.payload.phased_array", "space.sat.payload", "component", "통신 탑재체: 위상배열 안테나·디지털 프로세서", "능동 위상배열(AESA) 안테나·빔포밍 IC·디지털 투명 프로세서/재생 중계 ASIC — Ku/Ka/E밴드, D2D 용 대형 전개 안테나 포함")
inp("space.sat.payload.rf", "space.sat.payload", "component", "RF 부품(증폭기·필터·도파관)", "진행파관 증폭기(TWTA)·GaN 고체 증폭기(SSPA)·저잡음 증폭기·필터·멀티플렉서·도파관·RF 커넥터")
inp("space.sat.payload.oisl", "space.sat.payload", "component", "광학 위성간 링크(레이저 통신 단말)", "위성끼리 레이저로 100Mbps~100Gbps 통신 — SDA 표준 단말, 망원경·정밀 지향기구·광증폭기")
inp("space.sat.payload.eo_optical", "space.sat.payload", "component", "전자광학(EO) 탑재체", "반사 망원경(SiC·제로듀어 거울)·초점면 배열(CMOS/TDI CCD)·초분광 센서 — 해상도 0.3~3m")
inp("space.sat.payload.sar", "space.sat.payload", "component", "합성개구레이더(SAR) 탑재체", "X/C/L밴드 능동 레이더 안테나·고출력 송수신 모듈 — 밤·구름 관통 관측")
inp("space.sat.payload.ir", "space.sat.payload", "component", "적외선 센서(미사일 경보·추적)", "단·중파 적외선 초점면 배열(HgCdTe 등)·극저온 냉각기 — OPIR·극초음속 추적(HBTSS)·골든돔")
inp("space.sat.payload.gnss_clock", "space.sat.payload", "component", "항법 탑재체·원자시계", "루비듐·수소메이저 원자시계, L밴드 항법 신호 발생기 — GPS·갈릴레오·KPS")
none("space.sat.payload.eclss", "space.sat.payload", "component", "생명유지장치(ECLSS)", "산소·물 재생, 기압·온도 유지 장치", "무인 위성에는 사람이 안 탄다 — 유인 정거장(space.inspace.station)에서만 쓴다")

stage("space.sat.ait", "space.sat", "체계종합·조립·시험(AIT)", "부품을 모아 위성으로 조립하고(프라임) 발사·우주 환경을 지상에서 미리 겪게 한다(환경시험)")
inp("space.sat.ait.prime", "space.sat.ait", "service_ip", "위성 체계종합(프라임·양산형 버스 메이커)", "대형 GEO·국방 프라임, LEO 양산(일 수 기~수십 기) 수직계열, 소형위성 버스 전문 메이커")
inp("space.sat.ait.test", "space.sat.ait", "equipment", "환경시험 설비·서비스", "열진공 챔버(TVAC)·진동·음향·충격·전자파(EMC) 시험, 방사선 조사 시험")

# ── 2. 발사 ─────────────────────────────────────────────────────────
stage("space.launch", "space", "② 발사(Upstream — 궤도까지 올리기)", "발사체 제조 + 발사 서비스. 2025년 325회 발사, 상업 발사 매출 124억 달러")
stage("space.launch.vehicle", "space.launch", "발사체 제조", "엔진·탱크·특수합금·페어링·항전·추진제 — 재사용(1단 회수→완전 재사용)이 원가 구조를 바꾼다")
inp("space.launch.vehicle.liquid_engine", "space.launch.vehicle", "component", "액체 로켓 엔진", "터보펌프·연소기·노즐·밸브. 케로신(RP-1)/메탄/수소 + 액체산소. 3D 프린팅 연소기, 다단연소·가스발생기 사이클")
inp("space.launch.vehicle.srm", "space.launch.vehicle", "component", "고체 로켓 모터·부스터", "복합 추진제(AP/HTPB/알루미늄)·모터 케이스(탄소섬유)·노즐 — 부스터·상단·미사일과 공용 라인")
inp("space.launch.vehicle.tank_structure", "space.launch.vehicle", "component", "추진제 탱크·동체 구조", "알루미늄-리튬 합금 마찰교반용접(FSW)·스테인리스(스타십)·탄소복합재 탱크, 단간부·엔진부")
inp("space.launch.vehicle.superalloy", "space.launch.vehicle", "material", "특수합금·단조·주조", "니켈 초합금(인코넬)·니오븀(C-103)·티타늄·구리합금(GRCop) — 엔진·노즐·배관, 정밀 단조·주조·금속 3D 프린팅 분말")
inp("space.launch.vehicle.fairing", "space.launch.vehicle", "component", "페어링·분리장치", "탄소복합재 페어링, 단분리·위성분리 장치(파이로·비화약식), 위성 어댑터")
inp("space.launch.vehicle.avionics", "space.launch.vehicle", "component", "발사체 항전·유도항법제어(GNC)", "비행 컴퓨터·관성항법장치(INS)·텔레메트리·비행종단시스템(FTS)·추력벡터제어 구동기")
inp("space.launch.vehicle.propellant", "space.launch.vehicle", "material", "추진제·산업가스", "액체산소·액화메탄·RP-1·액체수소·헬륨(가압)·질소 — 발사 1회당 수백~수천 톤")
stage("space.launch.service", "space.launch", "발사 서비스", "위성 주인에게 「궤도까지 kg당 얼마」로 파는 운송업 — 대형·소형·라이드셰어·발사장")
inp("space.launch.service.heavy", "space.launch.service", "service_ip", "중대형 발사 서비스", "LEO 8톤 이상급(팰컨9·팰컨헤비·스타십·뉴글렌·벌컨·아리안6·H3·장정·뉴트론 등) — 컨스텔레이션 대량 배치")
inp("space.launch.service.small", "space.launch.service", "service_ip", "소형 발사 서비스", "LEO 1.5톤 이하 전용 발사(일렉트론·한빛 등) — 원하는 궤도·원하는 날짜, 극초음속 시험 발사 겸용")
inp("space.launch.service.otv", "space.launch.service", "service_ip", "라이드셰어·궤도수송선(OTV)·디스펜서", "합승 발사 중개, 「마지막 구간」 궤도 이동선, 위성 분리 디스펜서")
inp("space.launch.service.spaceport", "space.launch.service", "service_ip", "발사장·발사 지원 인프라", "발사대·조립동·추진제 저장·공급 설비, 레인지 안전·추적, 해상 회수선·발사 플랫폼")
none("space.launch.service.crew", "space.launch.service", "service_ip", "유인 캡슐 수송", "사람을 태우는 캡슐·탈출 시스템·유인 등급 인증", "위성 발사에는 유인 캡슐이 필요 없다 — 유인 수송은 space.inspace.station 에서 다룬다")

# ── 3. 지상 ─────────────────────────────────────────────────────────
stage("space.ground", "space", "③ 지상 세그먼트(Midstream — 지상에서 받기)", "위성과 교신하는 지상국 + 고객 손의 단말·칩. SIA 기준 최대 매출 구간(GNSS 칩·단말 포함 1,652억 달러)")
stage("space.ground.infra", "space.ground", "지상국 인프라", "게이트웨이·관제 안테나, 지상국을 빌려 주는 서비스(GSaaS), 관제·영상처리 소프트웨어")
inp("space.ground.infra.gateway_antenna", "space.ground.infra", "equipment", "지상국 안테나·게이트웨이 장비", "3~13m 파라볼라·위상배열 지상 안테나, 모뎀·베이스밴드·업/다운 컨버터, 광학 지상국")
inp("space.ground.infra.gsaas", "space.ground.infra", "service_ip", "지상국 서비스(GSaaS)", "전 세계 지상국 네트워크를 분·패스 단위로 임대 — 위성 운영자가 지상국을 안 짓고 빌려 쓴다")
inp("space.ground.infra.mission_sw", "space.ground.infra", "service_ip", "관제·임무·영상처리 소프트웨어", "위성 관제(C2)·임무계획·궤도 결정, 영상 전처리·보정, 가상화 지상 시스템(클라우드)")
stage("space.ground.user", "space.ground", "사용자 장비", "고객이 손에 쥐는 단말·안테나·칩 — 위성 서비스가 팔리는 만큼 따라 팔린다")
inp("space.ground.user.terminal", "space.ground.user", "component", "사용자 단말(평판 안테나·해상/항공 안테나)", "전자식 조향 평판 안테나(ESA), 해상 VSAT·항공기 기내 인터넷 안테나, 군용 다궤도 단말")
inp("space.ground.user.terminal_chip", "space.ground.user", "component", "단말·D2D 칩(모뎀·빔포머·RFIC)", "단말용 빔포머 IC·RF 프런트엔드·모뎀 SoC, 스마트폰 위성통신(NTN) 모뎀")
inp("space.ground.user.gnss_chip", "space.ground.user", "component", "GNSS 수신칩·모듈·장비", "스마트폰·차량·측량·농기계용 위성항법 수신 칩·고정밀(RTK) 수신기 — 지상장비 매출의 대부분")

# ── 4. 서비스 ───────────────────────────────────────────────────────
stage("space.service", "space", "④ 위성 서비스(Downstream — 서비스로 팔기)", "위성을 운영해 통신·데이터를 파는 구간. SIA 2025년 1,050억 달러")
stage("space.service.comm", "space.service", "위성통신 서비스", "광대역 인터넷·휴대폰 직접 연결·IoT·방송·국방 통신")
inp("space.service.comm.broadband", "space.service.comm", "service_ip", "위성 광대역 인터넷(LEO·GEO)", "가정·기업·해상·항공·정부용 인터넷. LEO 메가컨스텔레이션(스타링크·카이퍼/레오·원웹·궈왕) vs GEO 대용량 위성")
inp("space.service.comm.d2d", "space.service.comm", "service_ip", "휴대폰 직접 연결(D2D·D2C)", "개조 없는 스마트폰이 위성과 직접 통신 — 문자→음성→데이터. 이통사 주파수 임차형 vs 위성 전용 주파수(MSS)형")
inp("space.service.comm.iot", "space.service.comm", "service_ip", "위성 IoT·협대역 통신", "L밴드 협대역 음성·데이터, 자산 추적·원격 검침·해상 안전(GMDSS)·항공 안전 통신")
inp("space.service.comm.video", "space.service.comm", "service_ip", "위성방송·영상 분배(구산업)", "DTH 위성TV·방송 중계 — 가입자 감소 중인 캐시카우, GEO 운영자 매출의 뿌리")
inp("space.service.comm.milsat", "space.service.comm", "service_ip", "정부·국방 위성통신·우주 국방 체계", "군 전용·상용 임차 통신, 미 우주개발청(SDA) 확산형 전투우주구조(PWSA), 골든돔 우주 기반 요격·추적")
stage("space.service.data", "space.service", "위성 데이터 서비스", "지구관측 영상·분석·항법(PNT)")
inp("space.service.data.eo_data", "space.service.data", "service_ip", "지구관측 영상·데이터 판매", "광학·SAR·초분광·RF 신호탐지 위성을 운영해 영상·구독을 정부(국방·정보)와 민간에 판매")
inp("space.service.data.analytics", "space.service.data", "service_ip", "위성 데이터 분석·AI 인사이트", "영상 위에 AI 를 얹어 변화탐지·해양감시·농업·보험·금융 인사이트로 파는 소프트웨어 층")
inp("space.service.data.pnt", "space.service.data", "service_ip", "항법·시각(PNT) 서비스·대체 항법", "GNSS 보강·정밀측위 구독, GPS 교란 대비 LEO 대체 PNT")
stage("space.service.enabler", "space.service", "사업 허가·금융 인프라", "주파수·궤도 자원 면허와 보험 — 물건은 아니지만 없으면 사업이 안 된다")
inp("space.service.enabler.spectrum", "space.service.enabler", "service_ip", "주파수·궤도 자원(면허)", "ITU 등록·각국 면허(FCC 등), MSS·AWS 대역 거래, 궤도 슬롯·EPFD 규칙")
inp("space.service.enabler.insurance", "space.service.enabler", "service_ip", "우주 보험", "발사·궤도상 보험, 제3자 배상 — 연 보험료 수억 달러대의 작은 시장, 대형 사고 한 번에 적자")

# ── 5. 궤도상 경제 ──────────────────────────────────────────────────
stage("space.inspace", "space", "⑤ 궤도상 경제·신산업(아직 작지만 커지는 곳)", "우주에서 직접 하는 사업 — 감시·정비·정거장·달·제조·컴퓨팅")
inp("space.inspace.ssa", "space.inspace", "service_ip", "우주상황인식(SSA)·우주교통관리", "레이더·망원경으로 위성·잔해 추적, 충돌 경보·회피 기동 조율 — 위성 1.5만 기 시대의 교통관제")
inp("space.inspace.servicing", "space.inspace", "service_ip", "궤도상 서비스(수명연장·급유·잔해 제거)", "도킹해 연료 보급·자세 유지·견인, 고장 위성·잔해 제거(ADR), 궤도상 조립")
inp("space.inspace.station", "space.inspace", "service_ip", "상업 우주정거장·유인 수송", "ISS(2030년 퇴역) 후계 민간 정거장, 유인·화물 수송선, 우주복")
inp("space.inspace.lunar", "space.inspace", "service_ip", "달 착륙선·심우주 수송", "NASA CLPS 상업 달 화물, 아르테미스 유인 착륙선(HLS), 달 통신·항법 중계")
inp("space.inspace.manufacturing", "space.inspace", "service_ip", "우주 제조·재진입 캡슐", "미세중력 의약품 결정·광섬유·반도체 소재 생산, 지구 귀환 캡슐, 극초음속 재진입 시험")
inp("space.inspace.compute", "space.inspace", "service_ip", "궤도 데이터센터·우주 컴퓨팅", "태양광이 24시간 드는 궤도에 AI 연산 위성을 띄운다 — 전력·방열·발사 단가가 관건")

doc = {"schema": "valuechain/bom@1", "chain": "space", "product": N[0]["name"],
       "unit_basis": "글로벌 우주경제 연 매출 1년치(SIA SSIR 2026 기준 2025년 4,290억 달러 = 100%) — cost_share_pct 는 그 세그먼트 연 시장 규모 ÷ 4,290억 달러, qty_per_unit 은 연간 물량, price 는 대표 단가",
       "asof": ASOF, "status": "v0_draft", "approved_by": None,
       "stage_log": [{"stage": "V0", "at": ASOF, "by": "본체", "what": "무하네스 초안(v0_blind) 작성 — 레포가 비어 있어(README 1개) 레포 보강판(v0_tree)과 동일. 5단·하위 12단·입력 51 + 「없음」 3행"}],
       "nodes": N}

if __name__ == "__main__":
    for name in ("v0_blind.json", "v0_tree.json"):
        (HERE / name).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if "--bom" in sys.argv:
        (HERE.parent / "bom.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ins = [n for n in N if n["kind"] == "input"]
    print(f"노드 {len(N)} · 단계 {sum(n['kind'] == 'stage' for n in N)} · 입력 {len(ins)} (없음 행 {sum(str(n['makers']).startswith('없음') for n in ins)})")
