# FPSO 1척 — 심해 유전용 부유식 원유 생산·저장·하역 설비 — 물리적 제품 구조(BOM)

- 기준 단위: FPSO 1척(대형 신조, 브라질·가이아나 심해 기준) — 건조(EPCI)부터 20~30년 운영까지. 건조 단계 원가 비중의 분모는 EPCI 계약가 · 기준일 2026-11-12 · 상태 v1_filled · 승인 본체(메인 세션)
- 생성: `render_bom.py`(손으로 고치지 않는다 — 정본 `bom.json`·``) · 검사 `check_bom.py` 실패 0·관측 1
- 통계: 단계 9 · 참조 묶음 0 · 입력 27(bom 고유 27 + 묶음) {'service_ip': 13, 'material': 3, 'component': 5, 'equipment': 6} · 메이커 고유 60(행 91) {'overseas': 41, 'unlisted': 4, 'krx': 8, 'unlisted_listed_parent': 7}
- 채움: 수량 0/27 · 가격 4/27 · 원가 비중 0/27 · 점유율 0/91 · 박스 연결(고유 메이커) 0/60

## 1. 트리
```
- [product] fpso FPSO 1척 — 심해 유전용 부유식 원유 생산·저장·하역 설비
  - [stage] fpso.find 1. 유전 찾기·평가 — FPSO 이전 단계
    - [service_ip] fpso.find.seismic 해저 탄성파 탐사
    - [service_ip] fpso.find.drilling 심해 시추선(드릴십·반잠수식)
    - [service_ip] fpso.find.well_services 유정 시험·완결 서비스
    - [material] fpso.find.octg 유정용 강관(OCTG)
  - [stage] fpso.decide 2. 개발 결정 — 설계(FEED)·투자 결정(FID)·계약 방식
    - [service_ip] fpso.decide.feed 기본 설계(FEED)
    - [service_ip] fpso.decide.financing 프로젝트 금융·특수목적법인(SPC) 지분
  - [stage] fpso.build 3. 건조(EPCI) — 설계·조달·건조·설치
    - [stage] fpso.build.hull 3-1. 선체 — 떠 있는 기름 탱크
      - [service_ip] fpso.build.hull.yard 선체 건조 조선소
      - [service_ip] fpso.build.hull.standard 표준 선체 설계(IP)
    - [stage] fpso.build.topsides 3-2. 상부 설비 — 배 위의 정유 공장
      - [component] fpso.build.topsides.modules 공정 모듈 제작·통합
      - [equipment] fpso.build.topsides.compression 가스 압축기
      - [equipment] fpso.build.topsides.power 발전용 가스터빈
      - [equipment] fpso.build.topsides.water 해수 처리·주입 펌프
      - [component] fpso.build.topsides.piping 배관·피팅·밸브
      - [equipment] fpso.build.topsides.control 계장·제어·안전 시스템
    - [stage] fpso.build.mooring 3-3. 계류 — 한자리에 붙잡아 두기
      - [equipment] fpso.build.mooring.turret 터렛 계류 시스템
      - [material] fpso.build.mooring.lines 계류 체인·로프·앵커
    - [service_ip] fpso.build.epci_mgmt 설계·조달·사업 관리(FPSO 업체 본업)
  - [stage] fpso.subsea 4. 해저 생산 시스템 — 우물과 FPSO를 잇는 배관망
    - [equipment] fpso.subsea.trees 해저 트리·매니폴드·제어
    - [component] fpso.subsea.surf 엄빌리컬·라이저·플로라인(SURF)
    - [service_ip] fpso.subsea.install 해저 설치 용역
  - [stage] fpso.install 5. 현장 설치 — 끌고 가서 묶고 잇기
    - [service_ip] fpso.install.ahts 예인·앵커 설치 지원선(AHTS)
    - [component] fpso.install.pipeline 육상 송유관
  - [stage] fpso.operate 6. 운영 20~30년 — 리스료와 운영비를 받는 시간
    - [service_ip] fpso.operate.om 운영·정비 인력(O&M)
    - [service_ip] fpso.operate.vessels 보급선·지원선
    - [service_ip] fpso.operate.rov 수중 로봇(ROV) 점검·작업
    - [component] fpso.operate.spares 예비 부품·장비 애프터마켓
    - [material] fpso.operate.chemicals 생산 화학제
```

## 2. 제품 고유 입력(bom 노드)

| id | 종류 | 스펙 | 수량/스택 | 가격 | 원가 비중 | 메이커 | box_ref |
|---|---|---|---|---|---|---|---|
| fpso | product | 원유 10만~25만 배럴/일 처리, 원유 약 200만 배럴 저장. 해저 유정에서 올라온 원유·가스·물을 배  | — | 2800~3050 USD백만/척(EPCI 계약가) (②S004) | — | — | 없음 — 제품 노드는 박스 축 아님 |
| fpso.find.seismic | service_ip | 배가 음파를 쏘고 해저에 센서(OBN)를 깔아 지층 영상을 만든다. 데이터를 여러 석유회사에 파는 멀티클라이 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | TGS(XOSL:TGS), Viridien(옛 CGG)(XPAR:VIRI), Shearwater(비상장·Rasmussengruppen 등(비상장)) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.find.drilling | service_ip | 유정 하나에 수십 일. 일일 용선료(day rate)로 빌린다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 450000~500000 USD/일(최상급 드릴십 신규 계약) (②S013) | 미측정 — 공개 원가 구성 자료 없음 | Transocean(XNYS:RIG), Valaris(XNYS:VAL), Noble(XNYS:NE), Seadrill(XNYS:SDRL) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.find.well_services | service_ip | 뚫은 우물에서 실제로 기름이 얼마나 나오는지 시험하고, 생산용으로 마감(완결)한다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Expro(XNYS:XPRO), SLB(XNYS:SLB), Halliburton(XNYS:HAL), Baker Hughes(XNAS:BKR) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.find.octg | material | 우물 벽을 받치는 이음매 없는 고압 강관. 심해는 고급 사양 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Vallourec(XPAR:VK), Tenaris(XMIL:TEN), 세아제강(306200) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.decide.feed | service_ip | 처리 용량·가스 처리 방식·선체 크기를 정하는 설계. 본계약의 입장권 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | SBM Offshore(XAMS:SBMO), MODEC(XTKS:6269), BW Offshore(XOSL:BWO) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.decide.financing | service_ip | 리스형이면 FPSO 업체가 배를 소유하는 SPC를 세우고 은행 대출(비소구)과 파트너 지분으로 건조비를 댄다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — SPC별 부채·지분 구성 공시 안 됨 | Mitsui & Co.(SPC 파트너)(XTKS:8031), Mitsui O.S.K. Lines(SPC 파트너·MODEC 최대주주)(XTKS:9104), Mitsubishi Corp.(SPC 파트너)(XTKS:8058) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.hull.yard | service_ip | 신조 선체 또는 VLCC 개조. 지금 대형 FPSO 선체는 대부분 중국 야드 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Shanghai Waigaoqiao Shipbuilding(SWS)(비상장·CSSC(중국선박)), Seatrium(XSES:5E2), COOEC(해양석유공정)(XSHG:600583), BOMESC(비상장·독립 비상장), DSIC(대련조선)(비상장·CSSC), 삼성중공업(010140), 한화오션(042660), HD현대중공업(329180) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.hull.standard | service_ip | 같은 설계 선체를 반복 건조해 공기를 줄이는 방식. 수주 전에 선체를 미리 발주해 두기도 한다(투기적 발주) | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | SBM Offshore(Fast4Ward MPF)(XAMS:SBMO), MODEC(M350 등)(XTKS:6269) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.topsides.modules | component | 분리기·열교환기·배관을 철골 틀에 조립한 모듈을 만들어 선체에 올리고 연결(통합)·시운전한다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Seatrium(XSES:5E2), COOEC(XSHG:600583), BOMESC(비상장·독립 비상장), Dyna-Mac(XSES:NO4), 삼성중공업(010140) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.topsides.compression | equipment | 같이 나온 가스를 고압으로 눌러 땅속에 되넣거나(재주입) 육지로 보낸다. 브라질 프리솔트는 CO2가 많아 압 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Baker Hughes(XNAS:BKR), Siemens Energy(XETR:ENR), MAN Energy Solutions(Everllence)(비상장·Volkswagen), Atlas Copco(XSTO:ATCO-A) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.topsides.power | equipment | 배 전체 전기(수십~100MW)를 만든다. 생산 가스를 연료로 쓴다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Siemens Energy(XETR:ENR), Solar Turbines(비상장·Caterpillar), GE Vernova(항공 파생형)(XNYS:GEV), Baker Hughes(XNAS:BKR), 두산에너빌리티(034020) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.topsides.water | equipment | 바닷물의 황산염을 걸러 고압으로 유층에 넣어 압력을 유지한다(그래야 기름이 계속 올라온다) | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Sulzer(XSWX:SUN), Flowserve(XNYS:FLS) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.topsides.piping | component | 고압·부식 환경용 배관과 이음쇠·밸브. 수천 톤 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | 성광벤드(014620), 태광(023160), 하이록코리아(013030), Baker Hughes(밸브)(XNAS:BKR) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.topsides.control | equipment | 공정 제어(DCS), 비상 정지, 화재·가스 감지 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Emerson(XNYS:EMR), ABB(XSWX:ABBN), Yokogawa(XTKS:6841) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.mooring.turret | equipment | 배 앞쪽에 박는 거대한 회전 베어링 구조. 라이저(해저 배관)가 이 안으로 들어온다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | SBM Offshore(자체)(XAMS:SBMO), SOFEC(비상장·MODEC), NOV(APL)(XNYS:NOV) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.mooring.lines | material | 수백 m~수 km 길이의 대형 체인과 합성섬유 로프, 해저 말뚝 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Vicinay Cadenas(비상장·독립 비상장), Asian Star Anchor Chain(XSHG:601890), Bekaert(Bridon-Bekaert 로프)(XBRU:BEKB) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.build.epci_mgmt | service_ip | FPSO 업체의 진짜 역할: 공정 설계, 수백 개 장비 조달, 여러 야드 조율, 정액 계약의 원가 위험 관리 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | SBM Offshore(XAMS:SBMO), MODEC(XTKS:6269), Yinson Production(XKLS:7293), BW Offshore(XOSL:BWO), Bumi Armada(XKLS:5210) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.subsea.trees | equipment | 수심 2,000m에서 원격으로 우물을 여닫는 장치 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | TechnipFMC(XNYS:FTI), OneSubsea(비상장·SLB 70%·Aker Solutions 2), Baker Hughes(XNAS:BKR) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.subsea.surf | component | 제어 신호·화학제를 보내는 탯줄(엄빌리컬)과 원유를 올리는 유연·강관 배관 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | TechnipFMC(XNYS:FTI), Baker Hughes(유연관)(XNAS:BKR), NOV(유연관)(XNYS:NOV), Oceaneering(엄빌리컬)(XNYS:OII) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.subsea.install | service_ip | 전용선이 배관을 깔고 장비를 내린다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Subsea 7(XOSL:SUBC), Saipem(XMIL:SPM), TechnipFMC(XNYS:FTI), DOF Group(XOSL:DOFG) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.install.ahts | service_ip | 앵커·체인을 다루는 힘센 배. 일일 용선료 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 27373 USD/일(Tidewater 신규 계약 가중평균) (②S011) | 미측정 — 공개 원가 구성 자료 없음 | Tidewater(XNYS:TDW), DOF Group(XOSL:DOFG), Boskalis(대형 예인)(비상장·HAL Investments(2023 상장폐) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.install.pipeline | component | 고정식 플랫폼은 원유를 송유관으로 육지에 보낸다 | 없음 — FPSO는 배 안에 저장했다가 셔틀 유조선에 넘기므로 육상 송유관이 필요 없다. 이것이 육지에서 먼 심해에 FPSO를 쓰는 이유 | 없음 — FPSO 구조상 쓰지 않음 | 없음 — FPSO 구조상 쓰지 않음 | 없음 — FPSO 구조상 쓰지 않음 | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.operate.om | service_ip | 배 위 100~150명이 2주 교대로 산다. 가동률 98%+ 가 목표 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | SBM Offshore(XAMS:SBMO), MODEC(XTKS:6269), 석유회사 자체 운영(비상장·ExxonMobil·Petrobras 등) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.operate.vessels | service_ip | 식량·부품·화학제를 실어 나르는 배 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 27373 USD/일(Tidewater 신규 계약 가중평균) (②S011) | 미측정 — 공개 원가 구성 자료 없음 | Tidewater(XNYS:TDW), DOF Group(XOSL:DOFG) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.operate.rov | service_ip | 사람이 못 가는 수심에서 로봇이 계류·배관·트리를 점검 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 11781 USD/일(ROV 가동일당 매출) (①S012) | 미측정 — 공개 원가 구성 자료 없음 | Oceaneering(XNYS:OII), Subsea 7(XOSL:SUBC), DOF Group(XOSL:DOFG) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.operate.spares | component | 압축기·터빈·펌프 정비 부품. 장비 OEM의 반복 매출 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Baker Hughes(XNAS:BKR), Siemens Energy(XETR:ENR) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| fpso.operate.chemicals | material | 부식·수화물·스케일 방지제. 생산량에 비례 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | SLB(옛 ChampionX)(XNYS:SLB), Baker Hughes(XNAS:BKR), Clariant(XSWX:CLN) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |

## 3. 공정 묶음(참조된 것만) — 장비·소재·메이커의 유일한 정의

