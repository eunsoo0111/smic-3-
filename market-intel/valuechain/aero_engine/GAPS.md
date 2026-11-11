# 항공엔진 애프터마켓 — GAPS와 착수 큐

기준일 2026-11-11 · 기준 단위 CFM56-7B Shop Visit 1회 · 정본 `bom.json`, 트리와 표는 `BOM.md`

## 1. 구조에서 읽힌 것

| # | 관찰 | 근거 | Top pick에 주는 함의 |
|---|---|---|---|
| 1 | Shop Visit 비용의 58%가 에어포일, 23%가 LLP, 12%가 수리, 인건비는 7% | FTAI IR 자료(회사 주장, 약 3년 전, 총 680만 달러) | 정비 슬롯을 파는 쪽은 7%만 가져간다. 돈은 부품을 쥔 쪽에 있다. StandardAero 3Q 매출이 +4%에 그친 것과 맞는다 |
| 2 | 병목은 고압터빈 블레이드(단결정 주조) | Aviation Week: HPT 블레이드 부족이 CFM56 오버홀의 최대 제약(AerFin 발언) | 주조는 PCC(비상장)·Howmet 복점. 상장 순수 노출이 사실상 없다 |
| 3 | OEM이 병목을 직접 사들이는 단계 | GE가 주조사 CPP를 117.5억 달러에 인수 합의, 2027년 EBITDA의 약 26배, 2H27 종결 예정 | 독립 주조·단조 자산의 희소 가치가 가격으로 찍혔다. 반대로 독립 MRO·PMA 진영에는 조달 리스크 |
| 4 | 58% 칸에 비순정 대안이 처음 생겼다 | Chromalloy CFM56 HPT 블레이드 PMA, 2025년 10월 FAA 승인. FTAI와 협력 | FTAI의 마진 논리(순정 부품을 안 사고 정비)의 핵심. FTAI CFM56 점유율 약 15%(회사 주장) |
| 5 | Q는 가속이 아니라 고원 | CFM56 Shop Visit 2026·2027년 각 2,300~2,400회(과거 전망 2,500회보다 낮음). Safran 부품 성장률 +29% → +27% → +17%. IBA: CFM56 엔진 가치 횡보 | "더 빨라진다"가 아니라 "오래 간다"로 써야 한다. 퇴역률 전망이 3~4%에서 1.5~2%로 내려가 꼬리가 길어짐 |
| 6 | 이어달리기는 LEAP인데 독립 진영 몫이 작다 | LEAP Shop Visit 연 25% 성장 전망. OEM 계약에 묶이고 중고 부품 풀이 없음 | 2028년 이후에는 GE·Safran과 라이선스 숍(MTU, StandardAero)으로 무게가 옮겨 간다 |
| 7 | AI와 섞인 칸이 있다 | Howmet 가스터빈 매출 +45%. FTAI Power(데이터센터 발전). 초합금 신규 용량은 항공·방산·가스터빈이 나눠 씀 | 주제(AI 독립)에 깨끗한 칸: PMA(HEICO), 보기류(TransDigm), OEM 서비스(GE·Safran), 독립 MRO |

## 2. AI 독립성 판정

| 후보 | 사슬 위치 | AI와 섞이는 정도 | 3분기 숫자 |
|---|---|---|---|
| HEICO | PMA·수리 | 낮음 | Flight Support 매출 +18%(유기적 +12%), 영업이익 +24% |
| TransDigm | 보기류 독점 부품 | 낮음 | FY27 매출 가이던스 중간값 +14% |
| GE Aerospace | 설계권·OEM 정비 | 낮음(CPP 인수 후에도 항공 중심) | 서비스 +20% 이상, 2027년 서비스 두 자릿수 초반 성장 예상 |
| Safran | 설계권·OEM 정비 | 낮음 | 애프터마켓 +18.7%, 부품 성장 둔화 중 |
| MTU | 독립·파트너 정비 | 낮음 | 1H 민수 정비 +21%(9개월 실적 미확인) |
| StandardAero | 독립 정비 | 낮음 | 매출 +4.0%, 가이던스 4회 연속 상향 |
| FTAI Aviation | 모듈 교환·PMA·리스 | **중간**(FTAI Power) | Aerospace Products 매출 +76% |
| Carpenter | 초합금 용해 | **미확인**(발전용 비중) | 영업이익 +28%, SAO 마진 37.7% |
| Howmet | 주조 | **높음**(가스터빈 +45%) | 매출 +29% |

## 3. 모르는 것

| 항목 | 왜 필요한가 | 어디서 | 누가·언제 |
|---|---|---|---|
| 최신 Shop Visit 비용 분해(2026년 가격) | 58/23/12/7이 3년 전 회사 자료 | Aircraft Commerce, MBA, IBA 유료 자료 또는 MRO 견적 | 팀, 섹터 확정 직후 |
| OEM 카탈로그 가격 인상률(연도별) | 순정 부품 P의 원천이고 PMA 수요의 근거 | CFM 가격 공지, 항공사 10-K, IATA 자료 | 팀 |
| OEM 직영 대 독립 MRO 물량 비중 | 슬롯 칸의 점유율이 전부 대체값 | IATA 협동체 엔진 MRO 보고서, Cirium | 팀 |
| 주조·단조 점유율 | 병목 칸인데 숫자가 없다 | Howmet·PCC(Berkshire) 10-K, GE의 CPP 인수 자료 | 팀 |
| Carpenter·ATI의 발전용 가스터빈 매출 비중 | AI 독립성 판정 | 10-K 최종시장별 매출 | 팀 |
| FTAI Power가 CFM56 코어를 얼마나 가져가나 | USM 공급과 정비 슬롯 잠식 | FTAI 콜 원문 | 팀 |
| 제트유 급등이 Shop Visit을 얼마나 미루나 | 반대 논리 1번 | 2008·2020년 사례, 항공사 공급 계획 | 팀 |
| 모든 후보의 주가·멀티플·컨센서스 | 스크리닝 2차 컷 | 주가 데이터(이 환경에서는 접근 실패) | 은수 |

## 4. equity-study 착수 큐

아래 표는 `check_bom.py --queue` 산식 그대로다. **"실측/대체" 칸이 거의 0이라 점수는 순서 참고용**이다. 점유율이 실측된 칸은 FTAI(15%) 하나뿐이다.

<!-- queue:start -->
| # | 기업 | 티커 | 상장 | 점수 | 입력 | 실측/대체 | box_ref |
|---|---|---|---|---|---|---|---|
| 1 | GE Aerospace | XNYS:GE | overseas | 21.23 | slot, hpt, llp, cmc | 0/7 | 없음 — 새 박스 후보 |
| 2 | Safran | XPAR:SAF | overseas | 20.75 | slot, hpt, llp, forge | 0/7 | 없음 — 새 박스 후보 |
| 3 | Howmet Aerospace | XNYS:HWM | overseas | 10.80 | hpt, ti, forge, cast | 0/5 | 없음 — 새 박스 후보 |
| 4 | Precision Castparts | 비상장(Berkshire Hathaway) | unlisted_listed_parent | 4.84 | hpt, cast | 0/2 | 없음 — 새 박스 후보 |
| 5 | MTU Aero Engines | XETR:MTX | overseas | 3.42 | slot, blade, slot_new | 0/3 | 없음 — 새 박스 후보 |
| 6 | StandardAero | XNYS:SARO | overseas | 3.42 | slot, blade, slot_new | 0/3 | 없음 — 새 박스 후보 |
| 7 | FTAI Aviation | XNAS:FTAI | overseas | 3.16 | slot, exchange, usm, power | 1/3 | 없음 — 새 박스 후보 |
| 8 | HEICO | XNYS:HEI | overseas | 2.93 | pma, blade | 0/2 | 없음 — 새 박스 후보 |
| 9 | Chromalloy | 비상장(Veritas Capital(비상장 PE)) | unlisted | 1.53 | hpt, pma, blade | 0/3 | 없음 — 새 박스 후보 |
| 10 | RTX (Collins) | XNYS:RTX | overseas | 1.52 | acc, tc, pbh, slot_new | 0/4 | 없음 — 새 박스 후보 |
| 11 | ATI | XNYS:ATI | overseas | 1.51 | ni, ti, forge, igt | 0/4 | 없음 — 새 박스 후보 |
| 12 | Molymet | XSGO:MOLYMET | overseas | 0.80 | minor | 0/1 | 없음 — 새 박스 후보 |
| 13 | KGHM | XWAR:KGH | overseas | 0.80 | minor | 0/1 | 없음 — 새 박스 후보 |
| 14 | Carpenter Technology | XNYS:CRS | overseas | 0.76 | ni, igt | 0/2 | 없음 — 새 박스 후보 |
| 15 | ST Engineering | XSES:S63 | overseas | 0.70 | slot | 0/1 | 없음 — 새 박스 후보 |
<!-- queue:end -->

**본체 판단 (큐 점수와 별개)**: 구조와 AI 독립성을 같이 보면 먼저 볼 순서는 ① HEICO(깨끗한 칸, 순정가가 오를수록 수요 증가) ② FTAI(가장 큰 변화가 있는 칸이지만 AI와 섞이고 논쟁 종목) ③ Carpenter(가스터빈 비중 확인이 선행 조건). GE·Safran은 기준점으로 쓴다. Howmet은 주제에서 제외.
