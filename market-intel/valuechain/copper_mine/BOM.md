# 구리 정광 — 연 10만 톤급 노천 구리 광산 1곳 — 물리적 제품 구조(BOM)

- 기준 단위: 광산 1곳(연 구리 10만 톤, 황화광 노천). 원가 비중의 분모는 노드마다 basis에 적는다(채굴비·선광비·현장 운영비가 다르다) · 기준일 2026-11-12 · 상태 v1_filled · 승인 본체(메인 세션)
- 생성: `render_bom.py`(손으로 고치지 않는다 — 정본 `bom.json`·``) · 검사 `check_bom.py` 실패 0·관측 1
- 통계: 단계 5 · 참조 묶음 0 · 입력 30(bom 고유 30 + 묶음) {'service_ip': 11, 'component': 4, 'equipment': 10, 'material': 5} · 메이커 고유 57(행 83) {'overseas': 35, 'unlisted': 10, 'unlisted_listed_parent': 9, 'krx': 3}
- 채움: 수량 0/30 · 가격 1/30 · 원가 비중 5/30 · 점유율 0/83 · 박스 연결(고유 메이커) 0/57

## 1. 트리
```
- [product] cu_mine 구리 정광 — 연 10만 톤급 노천 구리 광산 1곳
  - [stage] cu_mine.explore 1. 탐사 — 땅속에 구리가 얼마나 있나 찾기
    - [service_ip] cu_mine.explore.geophysics 지질·물리 탐사
    - [service_ip] cu_mine.explore.drilling 탐사 시추 용역
    - [component] cu_mine.explore.drill_tools 시추 소모품·시추공 센서
    - [service_ip] cu_mine.explore.assay 시료 분석(지화학 시험)
    - [service_ip] cu_mine.explore.software 자원량 모델링·광산 설계 소프트웨어
  - [stage] cu_mine.develop 2. 개발·건설 — 광산과 공장을 짓기
    - [service_ip] cu_mine.develop.epcm 설계·조달·건설관리(EPCM)
    - [equipment] cu_mine.develop.infra 물·전력·도로 기반시설
  - [stage] cu_mine.mine 3. 채굴 — 뚫고, 터뜨리고, 싣고, 나르기
    - [equipment] cu_mine.mine.drill_rig 생산 천공기(발파공)
    - [material] cu_mine.mine.explosives 폭약·기폭 시스템
    - [equipment] cu_mine.mine.shovel 적재 장비(전기 로프 쇼벨·초대형 굴착기)
    - [equipment] cu_mine.mine.haul_truck 초대형 운반 트럭(220~400톤급)
    - [component] cu_mine.mine.truck_body 트럭 적재함·버킷
    - [component] cu_mine.mine.tyres 초대형 광산용 타이어(OTR 57~63인치)
    - [material] cu_mine.mine.fuel 디젤 연료
    - [service_ip] cu_mine.mine.maintenance 중장비 정비 인력·부품
    - [service_ip] cu_mine.mine.autonomy 자율 운전·관제 소프트웨어
    - [service_ip] cu_mine.mine.underground 지하 채굴 장비·용역
  - [stage] cu_mine.process 4. 선광 — 돌을 밀가루처럼 갈아 구리만 골라내기
    - [equipment] cu_mine.process.crusher 1차 파쇄기(자이러토리 크러셔)
    - [equipment] cu_mine.process.mill 분쇄기(SAG 밀·볼 밀)
    - [material] cu_mine.process.grinding_media 분쇄 매체(강철 볼)
    - [component] cu_mine.process.liners 밀 라이너(내벽 보호판)
    - [equipment] cu_mine.process.slurry_pump 슬러리 펌프·사이클론
    - [equipment] cu_mine.process.flotation 부선기
    - [material] cu_mine.process.reagents 부선 시약(포수제·기포제)
    - [equipment] cu_mine.process.dewater 농축·여과기
    - [service_ip] cu_mine.process.tailings 광미 저장·관리
    - [material] cu_mine.process.power 전력
    - [equipment] cu_mine.process.sxew 용매추출·전해채취(SX-EW)
  - [stage] cu_mine.sell 5. 판매 — 정광을 제련소로 보내기
    - [service_ip] cu_mine.sell.logistics 운송·항만·해운
    - [service_ip] cu_mine.sell.smelter 제련소(정광의 고객)
```

## 2. 제품 고유 입력(bom 노드)

| id | 종류 | 스펙 | 수량/스택 | 가격 | 원가 비중 | 메이커 | box_ref |
|---|---|---|---|---|---|---|---|
| cu_mine | product | 황화 구리 광석(평균 품위 약 0.5~0.6%)을 캐서 갈고 골라 구리 25~30% 정광으로 만들어 제련소에 | — | 13768 USD/t(구리, LME 3개월물) (②S010) | — | — | 없음 — 제품 노드는 박스 축 아님 |
| cu_mine.explore.geophysics | service_ip | 항공 자력·전자기·유도분극(IP) 탐사, 위성 분광. 시추할 자리를 고르는 단계 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 프로젝트별 용역가, 공개 없음 | 미측정 — 공개 원가 구성 자료 없음 | 미측정 — 소규모 전문 업체가 대부분이고 대표 상장사가 없다(이번 범위 밖) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.explore.drilling | service_ip | 다이아몬드 코어 시추(돌 기둥 채취)·RC 시추(돌가루 채취). 리그 1대 + 시추공 2~3명이 하루 24시 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 미터당 단가는 회사들이 공시하지 않음 | 미측정 — 탐사 예산 중 시추비 비중 공개 자료 없음(업계 통념은 절반 이상, 검증 필요) | Major Drilling(XTSE:MDI), Foraco(XTSE:FAR), Capital Ltd(XLON:CAPD), Perenti(DDH1 시추 부문)(XASX:PRN), Boart Longyear(비상장·American Industrial Part) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.explore.drill_tools | component | 다이아몬드 비트·로드, 시추 유체, 시추공 방향 측정 센서, 현장 코어 분석기. 미터를 뚫을 때마다 닳는 소 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Imdex(XASX:IMD), Boart Longyear(비상장·American Industrial Part), Epiroc(XSTO:EPI-A) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.explore.assay | service_ip | 코어를 잘라 갈고 녹여 구리·금 등 함량을 잰다. 시료 1개당 요금. 탐사사가 시험소를 고르지만 대형 시험소 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 시료당 요금표 비공개 | 미측정 — 공개 원가 구성 자료 없음 | ALS(XASX:ALQ), SGS(XSWX:SGSN), Bureau Veritas(XPAR:BVI), Intertek(XLON:ITRK) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.explore.software | service_ip | 시추 결과로 3D 광체 모델을 만들고 채굴 계획을 짠다. 구독형(연 반복 매출) | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Micromine(비상장·Weir Group), Seequent(비상장·Bentley Systems), Datamine(비상장·Constellation Software), Maptek(비상장·독립 비상장) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.develop.epcm | service_ip | 엔지니어링 회사가 광산·선광장을 설계하고 장비를 사 주고 건설을 관리한다. 건설비의 일부를 수수료로 받는다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Worley(XASX:WOR), Fluor(XNYS:FLR), Hatch(비상장·직원 소유 비상장), Bechtel(비상장·가족 소유 비상장), Ausenco(비상장·독립 비상장) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.develop.infra | equipment | 칠레·페루 사막 광산은 해수담수화 설비와 수백 km 송수관이 필요하다. 송전선·변전소·접근 도로·항만 포함 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | 미측정 — 이번 범위 밖(담수화·송전 업체는 별도 체인) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.mine.drill_rig | equipment | 지름 20~30cm, 깊이 15m 안팎 구멍을 격자로 뚫는다. 자율 운전 확대 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Epiroc(XSTO:EPI-A), Caterpillar(XNYS:CAT), Komatsu(P&H)(XTKS:6301), Sandvik(XSTO:SAND) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.mine.explosives | material | 질산암모늄 기반 벌크 폭약(에멀전·ANFO)을 트럭이 구멍에 바로 채우고, 전자 뇌관으로 순서대로 터뜨린다. | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 채굴비 중 '석유계 품목(연료·폭약·타이어)'이 절반 미만이라는 자료만 있음(S005) | Orica(XASX:ORI), Dyno Nobel(XASX:DNL), Enaex(비상장·Sigdo Koppers), 한화(글로벌 부문 산업용 화약)(000880) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.mine.shovel | equipment | 버킷 한 번에 50~100톤을 떠서 트럭에 싣는다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Komatsu(XTKS:6301), Caterpillar(XNYS:CAT), Hitachi Construction Machinery(XTKS:6305), Liebherr(비상장·가족 소유 비상장), HD현대건설기계(267270) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.mine.haul_truck | equipment | 광산 운영비의 큰 몫. 점점 무인 자율 운전으로 바뀐다. 트럭은 10~20년 쓰고 부품·정비가 반복 매출 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Caterpillar(XNYS:CAT), Komatsu(XTKS:6301), Hitachi Construction Machinery(XTKS:6305), Liebherr(비상장·가족 소유 비상장), BelAZ(비상장·벨라루스 국영) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.mine.truck_body | component | 광석에 따라 맞춤 설계한 경량 적재함. 닳으면 교체 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Austin Engineering(XASX:ANG), ESCO(버킷·마모 부품)(비상장·Weir Group) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.mine.tyres | component | 개당 수천만 원, 수명 1년 안팎. 석유계 원가 항목 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Bridgestone(XTKS:5108), Michelin(XPAR:ML) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.mine.fuel | material | 트럭·쇼벨·천공기 연료. 전기 트롤리·배터리 트럭으로 일부 대체 중 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 15 % (②S006) | 미측정 — 지역 연료 유통사, 투자 대상 아님 | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.mine.maintenance | service_ip | 트럭·쇼벨을 24시간 돌리려면 정비가 필수. 숙련 정비공이 모자라 외주가 는다. 딜러가 부품·서비스를 함께  | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 43 % (②S005) | Mader Group(XASX:MAD), Finning(Cat 딜러)(XTSE:FTT), 장비 OEM 자체 서비스(비상장·Caterpillar·Komatsu 등) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.mine.autonomy | service_ip | 무인 트럭·천공기 운행 시스템과 운영 최적화 소프트웨어. 장비에 묶여 팔린다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Caterpillar(MineStar)(XNYS:CAT), Komatsu(FrontRunner)(XTKS:6301), Epiroc(XSTO:EPI-A) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.mine.underground | service_ip | 노천이 아닌 지하 광산이면 지하 로더·트럭·천공 점보와 채굴 용역 업체를 쓴다 | 없음 — 이 체인은 노천 광산 기준. 지하 광산이면 Epiroc·Sandvik 지하 장비와 Perenti 같은 용역이 들어간다 | 없음 — 노천 광산 기준이라 쓰지 않음 | 없음 — 노천 광산 기준이라 쓰지 않음 | 없음 — 노천 기준. 지하라면 Perenti(XASX:PRN)·Epiroc·Sandvik | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.crusher | equipment | 트럭이 쏟은 1m짜리 돌을 15~20cm로 깬다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 11 % (②S023) | Metso(XHEL:METSO), FLSmidth(XCSE:FLS), Sandvik(XSTO:SAND) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.mill | equipment | 지름 10~13m 회전 드럼에 돌과 쇠공을 넣고 돌려 0.1mm 이하로 간다. 광산 전력의 가장 큰 소비처. | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Metso(XHEL:METSO), FLSmidth(XCSE:FLS), CITIC Heavy Industries(XSHG:601608) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.grinding_media | material | 밀 안에서 돌과 함께 굴러 돌을 깨는 쇠공. 돌을 갈수록 쇠공도 닳아 계속 넣는다 — 처리하는 돌의 양에 비 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 21.5 % (②S005) | Moly-Cop(비상장·American Industrial Part), ME Elecmetal(비상장·Elecmetal(칠레 비상장)), Magotteaux(비상장·Sigdo Koppers) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.liners | component | 밀 안쪽을 덮는 고무·강철 판. 몇 달마다 교체. 교체하는 동안 밀이 멈추므로 수명과 교체 속도가 돈이다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Metso(XHEL:METSO), Weir(Vulco)(XLON:WEIR), ME Elecmetal(비상장·Elecmetal(칠레 비상장)), FLSmidth(XCSE:FLS) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.slurry_pump | equipment | 간 돌가루+물(슬러리)을 다음 공정으로 밀어 보낸다. 돌가루가 펌프 속을 갈아 먹어 임펠러·라이너를 계속 갈 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Weir(Warman)(XLON:WEIR), Metso(XHEL:METSO), FLSmidth(Krebs)(XCSE:FLS), KSB(XETR:KSB) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.flotation | equipment | 약품을 넣은 슬러리에 공기를 불어 구리 광물만 거품에 붙여 걷어 낸다. 구리 0.5% 돌가루가 25~30%  | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Metso(XHEL:METSO), FLSmidth(XCSE:FLS), Glencore Technology(Jameson Cell)(비상장·Glencore) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.reagents | material | 구리 광물 표면에 달라붙어 거품에 뜨게 하는 화학품. 처리 물량에 비례 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | Syensqo(옛 Solvay 광업 화학)(XBRU:SYENS), Clariant(XSWX:CLN), Orica(광업 화학)(XASX:ORI), Nouryon(비상장·Carlyle(사모펀드)) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.dewater | equipment | 정광의 물을 빼 운송 가능한 상태로, 광미의 물을 회수해 재사용 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | FLSmidth(XCSE:FLS), Metso(XHEL:METSO) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.tailings | service_ip | 남은 돌가루(전체의 99% 이상)를 댐에 쌓고 감시한다. 붕괴 사고 뒤 규제가 강해져 비용이 는다 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | WSP(옛 Golder)(XTSE:WSP), Weir(광미 펌프)(XLON:WEIR) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.power | material | 분쇄가 광산 전력의 대부분을 쓴다. 칠레는 재생에너지 구매계약(PPA)으로 전환 중 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 15 % (②S006) | 미측정 — 지역 전력회사, 이번 범위 밖 | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.process.sxew | equipment | 산화 구리 광석을 산으로 녹여 바로 구리판(음극동)을 만드는 다른 공정 | 없음 — 이 체인은 황화광 → 정광 경로. 산화광 광산만 SX-EW를 쓰고, 그 경우 정광·제련 단계가 없다 | 없음 — 황화광 경로라 쓰지 않음 | 없음 — 황화광 경로라 쓰지 않음 | 없음 — 황화광 경로라 쓰지 않음 | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.sell.logistics | service_ip | 정광 트럭·철도, 항만 하역, 벌크선 | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | 미측정 — 공개 단가 없음 | 미측정 — 공개 원가 구성 자료 없음 | 미측정 — 이번 범위 밖 | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |
| cu_mine.sell.smelter | service_ip | 정광을 녹여 99.99% 구리로 만든다. 광산 입장에선 제련수수료(TC/RC)가 '비용', 제련소 입장에선  | 미측정 — 광산·선박마다 달라 1단위 수량을 정하지 않았다 | -310 USD/t(정광, TC) (②S008) | 미측정 — 공개 원가 구성 자료 없음 | Jiangxi Copper(XSHG:600362), Tongling Nonferrous(XSHE:000630), JX Advanced Metals(XTKS:5016), Aurubis(XETR:NDA), LS MnM(비상장·LS), 고려아연(010130) | 없음 — 이 레포에 체인 yaml(core/valuechain) 없음. 박스 후보는 GAPS.md §박스 후보 |

## 3. 공정 묶음(참조된 것만) — 장비·소재·메이커의 유일한 정의

