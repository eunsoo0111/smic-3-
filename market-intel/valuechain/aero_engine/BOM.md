# 협동체 터보팬 엔진 Shop Visit(애프터마켓) — 물리적 제품 구조(BOM)

- 기준 단위: CFM56-7B 성능복원 Shop Visit 1회 비용 · 기준일 2026-11-11 · 상태 v3_queued · 승인 Claude(본체)
- 생성: `render_bom.py`(손으로 고치지 않는다 — 정본 `bom.json`·``) · 검사 `check_bom.py` 실패 0·관측 1
- 통계: 단계 6 · 참조 묶음 0 · 입력 23(bom 고유 23 + 묶음) {'service_ip': 8, 'equipment': 1, 'component': 10, 'material': 4} · 메이커 고유 48(행 84) {'overseas': 30, 'unlisted_listed_parent': 11, 'unlisted': 7}
- 채움: 수량 1/23 · 가격 1/23 · 원가 비중 4/23 · 점유율 3/84 · 박스 연결(고유 메이커) 0/48

## 1. 트리
```
- [product] sv 협동체 터보팬 엔진 Shop Visit
  - [stage] sv.exec 정비 실행
    - [service_ip] sv.exec.slot 정비 슬롯·인력
    - [equipment] sv.exec.testcell 테스트 셀
    - [service_ip] sv.exec.exchange 엔진·모듈 교환과 리스
    - [service_ip] sv.exec.slot_new 신형 엔진(LEAP·GTF) 정비 슬롯
  - [stage] sv.parts 교체 부품
    - [component] sv.parts.hpt 고압터빈 블레이드·베인
    - [component] sv.parts.llp 수명제한부품(LLP)
    - [component] sv.parts.pma PMA 대체부품
    - [component] sv.parts.usm 중고 부품(USM)
    - [component] sv.parts.acc 보기류·제어계·나셀
    - [component] sv.parts.pma_llp PMA 수명제한부품
    - [component] sv.parts.usm_new 신형 엔진(LEAP·GTF) 중고 부품
  - [stage] sv.repair 부품 수리
    - [service_ip] sv.repair.blade 블레이드·베인 수리(DER 포함)
    - [service_ip] sv.repair.heat 열처리·HIP·표면처리
  - [stage] sv.mat 소재·성형(부품의 상류)
    - [material] sv.mat.ni 니켈 초합금(용해·분말)
    - [material] sv.mat.ti 티타늄(스펀지·잉곳·빌릿)
    - [component] sv.mat.forge 디스크·샤프트·링 단조
    - [component] sv.mat.cast 에어포일·구조물 정밀주조
    - [material] sv.mat.minor 희소 합금원소(Re·Hf·Co·Ta)
    - [material] sv.mat.cmc 세라믹 기지 복합재(CMC)·SiC 섬유
  - [stage] sv.ip 설계권·계약
    - [service_ip] sv.ip.tc 형식증명·부품 카탈로그 가격
    - [service_ip] sv.ip.pbh 시간당 정비계약(PBH)
  - [stage] sv.alt 항공 밖 경쟁 용도
    - [service_ip] sv.alt.power 퇴역 코어의 발전용 전환
    - [component] sv.alt.igt 발전용 가스터빈 주조·초합금
```

## 2. 제품 고유 입력(bom 노드)

| id | 종류 | 스펙 | 수량/스택 | 가격 | 원가 비중 | 메이커 | box_ref |
|---|---|---|---|---|---|---|---|
| sv | product | CFM56-7B/-5B·V2500(구형), LEAP·GTF(신형)의 성능복원 정비 1회. 엔진을 내려 분해· | — | 6.8 백만 USD/회 (②S101) | — | — | 없음 — 레포에 체인 yaml 없음 |
| sv.exec.slot | service_ip | OEM 직영 숍, 항공사 계열 MRO, 독립 MRO의 엔진 라인. 인증(FAA Part 145/EASA)과  | 없음 — 서비스라 수량 축이 성립하지 않음 | 미측정 — 단가 원천 미확보 | 7 % (②S101) | GE Aerospace(XNYS:GE), Safran(XPAR:SAF), MTU Aero Engines(XETR:MTX), StandardAero(XNYS:SARO), FTAI Aviation(XNAS:FTAI 15%), Lufthansa Technik(비상장·Deutsche Lufthansa), ST Engineering(XSES:S63), AFI KLM E&M(비상장·Air France-KLM) | 없음 — 레포에 체인 yaml 없음 |
| sv.exec.testcell | equipment | 조립 후 추력·EGT 마진 시운전 설비. 신형 고바이패스 엔진은 대형 셀 필요 | 없음 — 서비스라 수량 축이 성립하지 않음 | 미측정 — 단가 원천 미확보 | 미측정 — 비용 분해 원천 미확보 | MDS Aero Support(비상장·독립 비상장), Safran Test Cells(비상장·Safran) | 없음 — 레포에 체인 yaml 없음 |
| sv.exec.exchange | service_ip | 정비 기간(TAT) 동안 대체 엔진을 빌려주거나 정비된 모듈과 맞교환. TAT가 길수록 수요 증가 | 없음 — 서비스라 수량 축이 성립하지 않음 | 미측정 — CFM56 리스료 원천 미확보(일부 기종 최대 +40% 보도, 기준일 불명) | 미측정 — 비용 분해 원천 미확보 | FTAI Aviation(XNAS:FTAI), Willis Lease Finance(XNAS:WLFC), AerCap(XNYS:AER), GA Telesis(비상장·독립 비상장) | 없음 — 레포에 체인 yaml 없음 |
| sv.parts.hpt | component | 단결정 니켈 초합금 정밀주조 + 열차폐 코팅. 가장 자주, 가장 비싸게 교체되는 부품 | 미측정 — 엔진 매뉴얼 기준 수량 미확인 | 미측정 — 단가 원천 미확보 | 58 % (②S101) | GE Aerospace(XNYS:GE), Safran(XPAR:SAF), Howmet Aerospace(XNYS:HWM), Precision Castparts(비상장·Berkshire Hathaway), Chromalloy(비상장·Veritas Capital(비상장 PE)) | 없음 — 레포에 체인 yaml 없음 |
| sv.parts.llp | component | 디스크·샤프트 등 회전체. 사이클 한도 도달 시 강제 교체. 단조품 | 14~18 개/세트 (②S102) | 1.1~1.6 백만 USD/세트 (②S102) | 23 % (②S101) | GE Aerospace(XNYS:GE), Safran(XPAR:SAF) | 없음 — 레포에 체인 yaml 없음 |
| sv.parts.pma | component | FAA 승인 비순정 부품. 순정 대비 할인. 고온부 PMA는 드묾 | 미측정 — 엔진 매뉴얼 기준 수량 미확인 | 미측정 — 순정 대비 할인율 원천 미확보 | 미측정 — 비용 분해 원천 미확보 | HEICO(XNYS:HEI), Chromalloy(비상장·Veritas Capital(비상장 PE)), Jet Parts Engineering(비상장·독립 비상장) | 없음 — 레포에 체인 yaml 없음 |
| sv.parts.usm | component | 해체 엔진에서 떼어 재인증한 부품. 퇴역이 줄면 공급이 마름 | 미측정 — 엔진 매뉴얼 기준 수량 미확인 | 미측정 — 단가 원천 미확보 | 미측정 — 비용 분해 원천 미확보 | AerSale(XNAS:ASLE), FTAI Aviation(XNAS:FTAI), AAR(XNYS:AIR), VSE(XNAS:VSEC), AerFin(비상장·독립 비상장) | 없음 — 레포에 체인 yaml 없음 |
| sv.parts.acc | component | 연료 계통, 액추에이터, 센서, 역추진장치. 부품번호 단위 독점이 많음 | 미측정 — 엔진 매뉴얼 기준 수량 미확인 | 미측정 — 단가 원천 미확보 | 미측정 — 비용 분해 원천 미확보 | TransDigm(XNYS:TDG), RTX (Collins)(XNYS:RTX), Honeywell Aerospace(XNAS:HONA), Woodward(XNAS:WWD), Loar Holdings(XNYS:LOAR), Parker-Hannifin(XNYS:PH) | 없음 — 레포에 체인 yaml 없음 |
| sv.parts.pma_llp | component | 회전체 LLP의 비순정품 | 없음 — 회전 수명부품은 OEM 외 승인 사례가 사실상 없음(검증 필요) | 없음 — 회전 수명부품은 OEM 외 승인 사례가 사실상 없음(검증 필요) | 없음 — 회전 수명부품은 OEM 외 승인 사례가 사실상 없음(검증 필요) | 없음 — 회전 수명부품은 OEM 외 승인 사례가 사실상 없음(검증 필요) | 없음 — 레포에 체인 yaml 없음 |
| sv.parts.usm_new | component | 신형 엔진용 USM | 없음 — 해체 기재가 거의 없어 중고 부품 풀이 아직 형성되지 않음(검증 필요) | 없음 — 해체 기재가 거의 없어 중고 부품 풀이 아직 형성되지 않음(검증 필요) | 없음 — 해체 기재가 거의 없어 중고 부품 풀이 아직 형성되지 않음(검증 필요) | 없음 — 해체 기재가 거의 없어 중고 부품 풀이 아직 형성되지 않음(검증 필요) | 없음 — 레포에 체인 yaml 없음 |
| sv.repair.blade | service_ip | 팁 복원, 코팅 박리·재코팅, 냉각홀 가공. OEM 수리와 독립 DER 수리 | 없음 — 서비스라 수량 축이 성립하지 않음 | 미측정 — 단가 원천 미확보 | 12 % (②S101) | Chromalloy(비상장·Veritas Capital(비상장 PE)), StandardAero(XNYS:SARO), MTU Aero Engines(XETR:MTX), HEICO(XNYS:HEI) | 없음 — 레포에 체인 yaml 없음 |
| sv.repair.heat | service_ip | 주조품 기공 제거(HIP), 열차폐 코팅(TBC), 숏피닝 | 없음 — 서비스라 수량 축이 성립하지 않음 | 미측정 — 단가 원천 미확보 | 미측정 — 비용 분해 원천 미확보 | Bodycote(XLON:BOY), Linde (Praxair Surface Technologies)(XNAS:LIN), OC Oerlikon(XSWX:OERL) | 없음 — 레포에 체인 yaml 없음 |
| sv.mat.ni | material | VIM/VAR/ESR 다중 용해 빌릿, 디스크용 분말야금. 엔진 인증 소재 | 미측정 — 엔진 매뉴얼 기준 수량 미확인 | 미측정 — 단가 원천 미확보 | 미측정 — 비용 분해 원천 미확보 | Carpenter Technology(XNYS:CRS), ATI(XNYS:ATI), Special Metals / Cannon Muskegon(비상장·Berkshire Hathaway(PCC)), Acerinox (VDM·Haynes)(XMAD:ACX), Aubert & Duval(비상장·Airbus·Safran·Tikehau 컨소), Cogne Acciai Speciali (SMP)(비상장·Walsin Lihwa), Doncasters(비상장·독립 비상장) | 없음 — 레포에 체인 yaml 없음 |
| sv.mat.ti | material | 팬·압축기 블레이드와 디스크용. 러시아 VSMPO 이탈 후 서방 공급 타이트 | 미측정 — 엔진 매뉴얼 기준 수량 미확인 | 미측정 — 단가 원천 미확보 | 미측정 — 비용 분해 원천 미확보 | ATI(XNYS:ATI 26.7%), VSMPO-AVISMA(비상장·독립 비상장 [20, 25]%), TIMET(비상장·Berkshire Hathaway(PCC)), Howmet Aerospace(XNYS:HWM), Toho Titanium(XTKS:5727), OSAKA Titanium Technologies(XTKS:5726) | 없음 — 레포에 체인 yaml 없음 |
| sv.mat.forge | component | 대형 프레스·등온 단조. 부품번호·공정·공급자 단위 인증 | 미측정 — 엔진 매뉴얼 기준 수량 미확인 | 미측정 — 단가 원천 미확보 | 미측정 — 비용 분해 원천 미확보 | Precision Castparts (Wyman-Gordon)(비상장·Berkshire Hathaway), ATI(XNYS:ATI), Howmet Aerospace(XNYS:HWM), Aubert & Duval(비상장·Airbus·Safran·Tikehau 컨소), Safran(XPAR:SAF) | 없음 — 레포에 체인 yaml 없음 |
| sv.mat.cast | component | 단결정·방향성 응고 주조. 과점 | 미측정 — 엔진 매뉴얼 기준 수량 미확인 | 미측정 — 단가 원천 미확보 | 미측정 — 비용 분해 원천 미확보 | Precision Castparts(비상장·Berkshire Hathaway), Howmet Aerospace(XNYS:HWM), Consolidated Precision Products(비상장·Warburg Pincus·Berkshire), Doncasters(비상장·독립 비상장) | 없음 — 레포에 체인 yaml 없음 |
| sv.mat.minor | material | 단결정 초합금의 고온 강도 원소. 부산물 금속이라 공급 탄력 낮음 | 미측정 — 엔진 매뉴얼 기준 수량 미확인 | 미측정 — 단가 원천 미확보 | 미측정 — 비용 분해 원천 미확보 | Molymet(XSGO:MOLYMET), KGHM(XWAR:KGH) | 없음 — 레포에 체인 yaml 없음 |
| sv.mat.cmc | material | LEAP 슈라우드 등 신형 엔진 고온부. 구형 엔진에는 없음 | 없음 — CFM56에는 쓰지 않음(LEAP부터) | 미측정 — 단가 원천 미확보 | 없음 — 기준 단위가 CFM56이라 분모 밖 | GE Aerospace(XNYS:GE), NGS Advanced Fibers(비상장·Nippon Carbon·GE·Safran ) | 없음 — 레포에 체인 yaml 없음 |
| sv.ip.tc | service_ip | OEM이 매년 카탈로그 가격을 인상. 순정 부품 P의 원천 | 없음 — 서비스라 수량 축이 성립하지 않음 | 미측정 — 카탈로그 가격 인상률 원천 미확보(IATA는 코로나 이전보다 높다고만 언급, S123) | 없음 — 부품 가격에 녹아 있어 따로 떼지 못함 | GE Aerospace(XNYS:GE), Safran(XPAR:SAF), RTX (Pratt & Whitney)(XNYS:RTX), Rolls-Royce(XLON:RR.) | 없음 — 레포에 체인 yaml 없음 |
| sv.ip.pbh | service_ip | 비행시간당 요금을 받고 정비를 보장. 신형 엔진은 대부분 OEM 계약에 묶임 | 없음 — 서비스라 수량 축이 성립하지 않음 | 미측정 — 단가 원천 미확보 | 없음 — 계약 형태라 Shop Visit 비용의 구성 항목이 아님 | GE Aerospace(XNYS:GE), Safran(XPAR:SAF), RTX (Pratt & Whitney)(XNYS:RTX) | 없음 — 레포에 체인 yaml 없음 |
| sv.exec.slot_new | service_ip | OEM 네트워크와 라이선스 받은 소수 숍만 수행. LEAP Shop Visit은 2030년까지 연 25% 성 | 없음 — 서비스라 수량 축이 성립하지 않음 | 미측정 — 단가 원천 미확보 | 없음 — 기준 단위가 CFM56이라 신형 엔진 비용은 분모 밖 | GE Aerospace(XNYS:GE), Safran(XPAR:SAF), RTX (Pratt & Whitney)(XNYS:RTX), MTU Aero Engines(XETR:MTX), StandardAero(XNYS:SARO) | 없음 — 레포에 체인 yaml 없음 |
| sv.alt.power | service_ip | CFM56 코어를 약 25MW 발전 터빈으로 개조해 데이터센터에 공급. 중고 부품 공급을 줄이고 엔진 가치를 | 없음 — 서비스라 수량 축이 성립하지 않음 | 미측정 — 단가 원천 미확보 | 없음 — 항공 밖 용도라 Shop Visit 비용 분모 밖 | FTAI Aviation(XNAS:FTAI) | 없음 — 레포에 체인 yaml 없음 |
| sv.alt.igt | component | 항공 엔진과 같은 주조 라인·초합금 용해로를 쓴다. 데이터센터 전력 수요가 항공용 물량과 경쟁 | 없음 — 항공 밖 수요라 Shop Visit 단위로 셀 수 없음 | 미측정 — 단가 원천 미확보 | 없음 — 항공 밖 용도라 Shop Visit 비용 분모 밖 | Howmet Aerospace(XNYS:HWM), Carpenter Technology(XNYS:CRS), ATI(XNYS:ATI) | 없음 — 레포에 체인 yaml 없음 |

## 3. 공정 묶음(참조된 것만) — 장비·소재·메이커의 유일한 정의

