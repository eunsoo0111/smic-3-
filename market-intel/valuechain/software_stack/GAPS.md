# 소프트웨어 스택 — GAPS와 착수 큐

기준일 2026-11-11 · 기준 단위 기업 소프트웨어 지출 100 · 정본 `bom.json`, 트리와 표는 `BOM.md`

물리적 제품이 아니라서 스킬을 변형해 적용했다. 수량·단가 축은 `없음`으로 두고, 각 칸의 스펙에 **과금 단위**(좌석/사용량/거래)를 적었다.

## 1. 구조에서 읽힌 것

| # | 관찰 | 근거(최근 분기) | 함의 |
|---|---|---|---|
| 1 | 과금 단위로 나누면 숫자가 갈린다 | 좌석: HubSpot 순매출유지율 101%, monday.com 108%(1년 전 117%), Workday 구독 +13.9%, Salesforce +11%. 사용량·거래: Snowflake +37%, Datadog +35%, Cloudflare +39%, JFrog +31%, Shopify +32% | 섹터 전체가 아니라 과금 단위가 스크리닝 축이다 |
| 2 | 사용량 과금 인프라는 AI와 같은 방향이다 | Datadog 10-Q가 최대 고객 사용량 감소를 경고. Snowflake·Cloudflare의 가속도 AI 워크로드와 겹친다 | AI가 반등하면 같이 오르지만, AI가 꺾이면 같이 둔화할 수 있다. "독립"은 아니다 |
| 3 | AI와 무관하게 크는 칸은 거래·현장·규제 산업의 기록 시스템이다 | Shopify GMV 6분기 연속 약 +30%, Toast +21%, ServiceTitan +21%, Procore +18.7%(cRPO +22.6%), Tyler SaaS +21.2%, Veeva +16%, Guidewire +15% | 주제에 가장 맞는 칸. 다만 성장률이 15~32%로 넓고, 소비·건설·주택 경기에 노출 |
| 4 | 보안은 양쪽 다 이기는 칸이다 | CrowdStrike 순증 ARR +51%, Palo Alto 매출 +31% | 이미 크게 오른 것으로 보도(미검증). 남은 업사이드 확인 필요 |
| 5 | 새로 생긴 칸: 비인간 신원 | SailPoint: 신원 증가분의 40%가 비인간 신원, 에이전트 파이프라인 분기 중 2배, 가이던스에는 거의 미반영 | AI 성공 시 수혜가 크고, 실패해도 기존 사업이 +26% 성장. 2분기 실적 미확인 |
| 6 | 새로 생긴 칸: AI 배치 인력 | ServiceNow가 대형 AI 계약에서 구독 매출·cRPO 일부가 전문 서비스로 이동한다고 밝힘 | 에이전트 매출이 늘수록 마진 구조가 바뀔 수 있다 |
| 7 | 주제에서 빼야 할 칸 | IaaS, 기반 모델 API, AI 코딩 도구, EDA | AI Capex와 직결 |

## 2. 두 상태 판정표

| 칸 | 과금 단위 | AI가 실패하면 | AI가 성공하면 | 주제 적합 |
|---|---|---|---|---|
| 협업·CRM 등 수평 좌석 SaaS | 좌석 | 반등 | 좌석 감소 압박 | 낮음 |
| HCM·급여 | 직원 수 | 유지 | 고용 감소에 직접 노출 | 낮음 |
| 데이터·관측·엣지 | 사용량 | 성장 둔화 가능 | 수혜 | 중간(AI와 동행) |
| 개발 도구(저장·디자인) | 좌석+사용량 | 유지 | 산출물 증가로 수혜, 좌석은 감소 | 중간 |
| 보안·신원 | 단말·신원 수 | 유지(필수 지출) | 공격 표면·에이전트 증가로 수혜 | 높음 |
| 커머스·매장·현장 서비스 | 거래액 | 유지(경기 변수) | 영향 작음 | 높음 |
| 공공·보험·제약 기록 시스템 | 계약 규모 | 유지 | 영향 작음 | 높음 |

## 3. 모르는 것

| 항목 | 왜 필요한가 | 어디서 | 누가·언제 |
|---|---|---|---|
| 범주별 지출 비중 | 전부 미측정이라 큐 점수가 무의미 | Gartner Market Databook, IDC 트래커 | 팀(유료 자료 접근 가능 시) |
| 후보별 좌석 과금 비중 | 스크리닝 핵심 축 | 10-K·10-Q 매출 인식 주석 | 팀, 섹터 확정 직후 |
| IGV·SOX 일별 상관, 11/5 당일 등락 | "같이 빠지나"의 직접 증거 | 주가 데이터(이 환경에서는 접근 실패) | 은수 |
| Datadog 최대 고객의 정체와 비중 | AI 연동도 | 10-Q 고객 집중 주석 | 팀 |
| SailPoint 2분기 실적, 대주주 지분 | 후보 검증, 오버행 | 8-K, 10-Q | 팀 |
| 시장 점유율(CRM 외) | 메이커 점유율이 거의 전부 대체값 | IDC·Gartner 점유율 보도자료 | 팀 |
| 모든 후보의 주가·멀티플·컨센서스 | 스크리닝 2차 컷 | 주가 데이터 | 은수 |

## 4. equity-study 착수 큐

아래 표는 `check_bom.py --queue` 산식 그대로다. **지출 비중이 전부 대체값(2%)이라 이 표의 순서는 의미가 없다.** 여러 칸에 걸친 회사가 위로 올라갈 뿐이다.

<!-- queue:start -->
| # | 기업 | 티커 | 상장 | 점수 | 입력 | 실측/대체 | box_ref |
|---|---|---|---|---|---|---|---|
| 1 | Microsoft (Azure) | XNAS:MSFT | overseas | 3.39 | iaas, scm, codegen, endpoint | 0/8 | 없음 — 새 박스 후보 |
| 2 | Atlassian | XNAS:TEAM | overseas | 2.05 | scm, itsm, suite, credits | 0/4 | 없음 — 새 박스 후보 |
| 3 | ServiceNow | XNYS:NOW | overseas | 1.73 | itsm, platform, deploy | 0/3 | 없음 — 새 박스 후보 |
| 4 | Shopify | XNAS:SHOP | overseas | 1.60 | commerce | 0/1 | 없음 — 새 박스 후보 |
| 5 | Oracle | XNYS:ORCL | overseas | 1.27 | iaas, data, erp, crm | 0/4 | 없음 — 새 박스 후보 |
| 6 | Alphabet (GCP) | XNAS:GOOGL | overseas | 1.25 | iaas, suite, model | 0/3 | 없음 — 새 박스 후보 |
| 7 | Figma | XNYS:FIG | overseas | 1.07 | design, credits | 0/2 | 없음 — 새 박스 후보 |
| 8 | Okta | XNAS:OKTA | overseas | 1.07 | identity, nhi | 0/2 | 없음 — 새 박스 후보 |
| 9 | SailPoint | XNAS:SAIL | overseas | 1.07 | identity, nhi | 0/2 | 없음 — 새 박스 후보 |
| 10 | Cloudflare | XNYS:NET | overseas | 0.93 | edge, network | 0/2 | 없음 — 새 박스 후보 |
| 11 | Palo Alto Networks | XNAS:PANW | overseas | 0.93 | network, nhi | 0/2 | 없음 — 새 박스 후보 |
| 12 | Workday | XNAS:WDAY | overseas | 0.93 | erp, hcm | 0/2 | 없음 — 새 박스 후보 |
| 13 | monday.com | XNAS:MNDY | overseas | 0.85 | suite, credits | 0/2 | 없음 — 새 박스 후보 |
| 14 | Datadog | XNAS:DDOG | overseas | 0.80 | obs | 0/1 | 없음 — 새 박스 후보 |
| 15 | Dynatrace | XNYS:DT | overseas | 0.80 | obs | 0/1 | 없음 — 새 박스 후보 |
<!-- queue:end -->

**본체 판단 (큐 점수와 별개)**: 두 상태 판정표에서 "높음"인 칸의 후보를 먼저 본다. 거래·현장: Shopify, Toast, Procore, ServiceTitan. 규제 기록 시스템: Tyler, Guidewire, Veeva. 보안·신원: SailPoint, CrowdStrike. 이 중 어느 것이 싼지는 주가를 확인하기 전에는 말할 수 없다.
