# fpso GAPS — 모르는 것·다음에 잴 것

- 기준일 2026-11-12. 검사 `check_bom.py` 통과(실패 0, 관측 1: 메이커 행 91개 중 59개가 ③ 모델 지식).
- 채움: 입력 27개 중 가격 4 · 원가 비중 0(선체·상부 비중은 단계 노드에 있음) · 수량 0 · 점유율 0/91. 박스 연결 0(이 레포에 체인 yaml 없음).
- 설명서: `claude/05_광산과_FPSO_산업_쉽게_이해하기_2026-11-12.md`

## 1. 미측정 — 누가·언제

| 칸 | 무엇이 없나 | 다음 손 |
|---|---|---|
| 원가 구성 | 최근 대형 FPSO의 선체·상부·계류 비중. 지금은 2000년대 사례(S005)뿐 | SBM·MODEC 투자자 자료, Petrobras 계약 공시 |
| 용선료 | 대형 FPSO 일일 용선료와 리스 IRR | SBM 연차보고서의 리스 매출·자산으로 역산 |
| 수주자 명단 | 2026 상반기 FPS 8기(S007) 각각의 계약자 — MODEC·Seatrium 공백이 점유율 문제인지 | 업계지(Offshore Magazine, Upstream) — **다음 단계 1순위** |
| 해저 장비 | FPSO 1척당 해저 트리 수와 해저 계약가 | TechnipFMC 수주 공시 |
| 한국 야드 | 삼성중공업·한화오션·HD현대중공업의 2025~2026 FPSO 수주와 철수 이유 | DART 단일판매·공급계약 공시 |
| SPC 파트너 | MODEC 용선 SPC별 파트너와 지분 | MODEC 유가증권보고서 |

## 2. 박스 후보 (체인 yaml이 생기면 반입)

- `fpso.contractor` (SBM·MODEC·Yinson·BW·Bumi), `fpso.yard_hull_modules` (중국·싱가포르·한국 야드), `fpso.topsides_rotating` (압축기·터빈·펌프 OEM), `fpso.mooring`, `fpso.subsea_sps`, `fpso.offshore_services` (지원선·ROV·설치선)

## 3. V4 갈아끼울 것

- ③ 메이커 59행: 상부 설비 OEM(Baker Hughes·Siemens Energy)과 중국 야드 점유율부터 ①② 로 확인한다.

## 4. equity-study 착수 큐

주의: 점유율·원가 비중이 전부 대체값이다(실측/대체 0/n). 순서 제안으로만 쓴다. 선체·상부 비중이 입력이 아닌 단계 노드에 있어 야드·OEM 점수가 낮게 나온다.

<!-- queue:start -->
| # | 기업 | 티커 | 상장 | 점수 | 입력 | 실측/대체 | box_ref |
|---|---|---|---|---|---|---|---|
| 1 | Baker Hughes | XNAS:BKR | overseas | 3.79 | well_services, compression, power, piping | 0/8 | 없음 — 새 박스 후보 |
| 2 | SBM Offshore | XAMS:SBMO | overseas | 2.72 | feed, standard, turret, epci_mgmt | 0/5 | 없음 — 새 박스 후보 |
| 3 | DOF Group | XOSL:DOFG | overseas | 2.27 | install, ahts, vessels, rov | 0/4 | 없음 — 새 박스 후보 |
| 4 | MODEC | XTKS:6269 | overseas | 2.19 | feed, standard, epci_mgmt, om | 0/4 | 없음 — 새 박스 후보 |
| 5 | Siemens Energy | XETR:ENR | overseas | 1.52 | compression, power, spares | 0/3 | 없음 — 새 박스 후보 |
| 6 | TechnipFMC | XNYS:FTI | overseas | 1.33 | trees, surf, install | 0/3 | 없음 — 새 박스 후보 |
| 7 | Tidewater | XNYS:TDW | overseas | 1.33 | ahts, vessels | 0/2 | 없음 — 새 박스 후보 |
| 8 | SLB | XNYS:SLB | overseas | 0.93 | well_services, chemicals | 0/2 | 없음 — 새 박스 후보 |
| 9 | NOV(APL) | XNYS:NOV | overseas | 0.93 | turret, surf | 0/2 | 없음 — 새 박스 후보 |
| 10 | Oceaneering(엄빌리컬) | XNYS:OII | overseas | 0.93 | surf, rov | 0/2 | 없음 — 새 박스 후보 |
| 11 | Subsea 7 | XOSL:SUBC | overseas | 0.93 | install, rov | 0/2 | 없음 — 새 박스 후보 |
| 12 | BW Offshore | XOSL:BWO | overseas | 0.85 | feed, epci_mgmt | 0/2 | 없음 — 새 박스 후보 |
| 13 | Sulzer | XSWX:SUN | overseas | 0.80 | water | 0/1 | 없음 — 새 박스 후보 |
| 14 | Flowserve | XNYS:FLS | overseas | 0.80 | water | 0/1 | 없음 — 새 박스 후보 |
| 15 | 세아제강 | 306200 | krx | 0.67 | octg | 0/1 | 없음 — 새 박스 후보 |
<!-- queue:end -->
