# copper_mine GAPS — 모르는 것·다음에 잴 것

- 기준일 2026-11-12. 검사 `check_bom.py` 통과(실패 0, 관측 1: 메이커 행 83개 중 64개가 ③ 모델 지식).
- 채움: 입력 30개 중 가격 1 · 원가 비중 5 · 수량 0 · 점유율 0/83. 박스 연결 0(이 레포에 체인 yaml 없음).
- 설명서: `claude/05_광산과_FPSO_산업_쉽게_이해하기_2026-11-12.md`

## 1. 미측정 — 누가·언제

| 칸 | 무엇이 없나 | 다음 손 |
|---|---|---|
| 전체 | 광산 1곳의 연간 이동 물량·트럭 대수·소모품 사용량(수량 축 0/30) | Escondida(BHP)·Cerro Verde(Freeport) 연차보고서로 대표 광산 1곳을 잰다 — 다음 갱신 |
| 운영비 구성 | 구리 전용 C1 현금원가 분해(인건비·에너지·소모품·정비). 지금은 북미 혼합 표본(S005)과 사례 1건(S023)뿐 | Freeport·Antofagasta·Southern Copper 10-K/연차보고서의 원가 항목 |
| 시추 | 미터당 단가·가동률과 단가의 관계(2011년 사이클) | Major Drilling 과거 연차보고서 |
| 분쇄 매체 | 점유율, 상장 접근로(Sigdo Koppers의 Magotteaux 지분) | Sigdo Koppers 연차보고서 |
| 품위 | 2026년 세계 평균 품위(S&P 최신판). AME는 향후 5년 0.56% 유지 전망 — 품위 하락 논리의 속도를 정한다 | S&P Global 원문 |
| 제련 | LS MnM·고려아연의 2026 TC 계약 조건 | DART 사업보고서 |
| 2027 TC/RC 벤치마크 | 연말 타결 예정 | 뉴스 |

## 2. 박스 후보 (체인 yaml이 생기면 반입)

- `copper_mine.explore_services` (시추·분석·소프트웨어), `copper_mine.equipment_oe` (트럭·쇼벨·천공기·밀·파쇄기), `copper_mine.consumables` (분쇄 매체·라이너·펌프 부품·시약·폭약·타이어), `copper_mine.maintenance_labour`, `copper_mine.smelting` (고객·TC)

## 3. V4 갈아끼울 것

- ③ 메이커 64행: 특히 점유율이 큰 칸(초대형 트럭 Cat·Komatsu, 분쇄 매체 Moly-Cop, 폭약 Orica·Enaex)부터 ①② 로 확인한다.

## 4. equity-study 착수 큐

주의: 아래 점수는 점유율이 전부 미측정이라 1/메이커 수로 대체한 값이다(실측/대체 칸 0/n). 순서 제안으로만 쓴다. 점수를 믿기 전에 원가 비중과 점유율을 먼저 잰다.

<!-- queue:start -->
| # | 기업 | 티커 | 상장 | 점수 | 입력 | 실측/대체 | box_ref |
|---|---|---|---|---|---|---|---|
| 1 | Mader Group | XASX:MAD | overseas | 11.47 | maintenance | 0/1 | 없음 — 새 박스 후보 |
| 2 | Finning(Cat 딜러) | XTSE:FTT | overseas | 11.47 | maintenance | 0/1 | 없음 — 새 박스 후보 |
| 3 | 장비 OEM 자체 서비스 | 비상장(Caterpillar·Komatsu 등) | unlisted_listed_parent | 5.73 | maintenance | 0/1 | 없음 — 새 박스 후보 |
| 4 | Metso | XHEL:METSO | overseas | 5.60 | crusher, mill, liners, slurry_pump | 0/6 | 없음 — 새 박스 후보 |
| 5 | FLSmidth | XCSE:FLS | overseas | 5.60 | crusher, mill, liners, slurry_pump | 0/6 | 없음 — 새 박스 후보 |
| 6 | Sandvik | XSTO:SAND | overseas | 3.33 | drill_rig, crusher | 0/2 | 없음 — 새 박스 후보 |
| 7 | Magotteaux | 비상장(Sigdo Koppers) | unlisted_listed_parent | 2.87 | grinding_media | 0/1 | 없음 — 새 박스 후보 |
| 8 | Weir(Vulco) | XLON:WEIR | overseas | 1.60 | liners, slurry_pump, tailings | 0/3 | 없음 — 새 박스 후보 |
| 9 | Caterpillar | XNYS:CAT | overseas | 1.57 | drill_rig, shovel, haul_truck, autonomy | 0/4 | 없음 — 새 박스 후보 |
| 10 | Komatsu(P&H) | XTKS:6301 | overseas | 1.57 | drill_rig, shovel, haul_truck, autonomy | 0/4 | 없음 — 새 박스 후보 |
| 11 | Epiroc | XSTO:EPI-A | overseas | 1.47 | drill_tools, drill_rig, autonomy | 0/3 | 없음 — 새 박스 후보 |
| 12 | Orica | XASX:ORI | overseas | 0.80 | explosives, reagents | 0/2 | 없음 — 새 박스 후보 |
| 13 | Austin Engineering | XASX:ANG | overseas | 0.80 | truck_body | 0/1 | 없음 — 새 박스 후보 |
| 14 | Bridgestone | XTKS:5108 | overseas | 0.80 | tyres | 0/1 | 없음 — 새 박스 후보 |
| 15 | Michelin | XPAR:ML | overseas | 0.80 | tyres | 0/1 | 없음 — 새 박스 후보 |
<!-- queue:end -->
