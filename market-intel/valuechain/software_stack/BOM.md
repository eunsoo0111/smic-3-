# 엔터프라이즈 소프트웨어 스택 — 물리적 제품 구조(BOM)

- 기준 단위: 기업 소프트웨어 지출 100(범주별 비중) · 기준일 2026-11-11 · 상태 v3_queued · 승인 Claude(본체)
- 생성: `render_bom.py`(손으로 고치지 않는다 — 정본 `bom.json`·``) · 검사 `check_bom.py` 실패 0·관측 1
- 통계: 단계 7 · 참조 묶음 0 · 입력 29(bom 고유 29 + 묶음) {'service_ip': 29} · 메이커 고유 60(행 87) {'overseas': 54, 'unlisted': 6}
- 채움: 수량 0/29 · 가격 0/29 · 원가 비중 0/29 · 점유율 2/87 · 박스 연결(고유 메이커) 0/60

## 1. 트리
```
- [product] stack 엔터프라이즈 소프트웨어 스택
  - [stage] stack.infra 인프라·런타임
    - [service_ip] stack.infra.iaas 클라우드 IaaS
    - [service_ip] stack.infra.edge 엣지·CDN·네트워크
    - [service_ip] stack.infra.data 데이터베이스·데이터 플랫폼
    - [service_ip] stack.infra.obs 관측(옵저버빌리티)
  - [stage] stack.dev 개발·배포
    - [service_ip] stack.dev.scm 소스·CI/CD·아티팩트 관리
    - [service_ip] stack.dev.design 디자인·제품 협업
    - [service_ip] stack.dev.codegen AI 코딩 도구
  - [stage] stack.sec 보안
    - [service_ip] stack.sec.endpoint 엔드포인트·XDR
    - [service_ip] stack.sec.network 네트워크 보안·SASE
    - [service_ip] stack.sec.identity 신원·접근 관리
    - [service_ip] stack.sec.vuln 취약점·앱 보안
    - [service_ip] stack.sec.nhi 비인간(에이전트·기계) 신원
  - [stage] stack.sor 수평 기록 시스템
    - [service_ip] stack.sor.erp ERP·재무
    - [service_ip] stack.sor.crm CRM·마케팅
    - [service_ip] stack.sor.hcm HCM·급여
    - [service_ip] stack.sor.itsm ITSM·워크플로
    - [service_ip] stack.onprem 신규 온프레미스 영구 라이선스
  - [stage] stack.collab 협업·생산성
    - [service_ip] stack.collab.suite 오피스·협업 도구
  - [stage] stack.vert 산업 특화 기록 시스템
    - [service_ip] stack.vert.health 헬스케어·생명과학
    - [service_ip] stack.vert.fin 금융·보험 코어
    - [service_ip] stack.vert.gov 공공·건설·현장
    - [service_ip] stack.vert.smb 매장·소상공인 운영+결제
    - [service_ip] stack.vert.eng 설계·엔지니어링(CAD·PLM·EDA)
    - [service_ip] stack.vert.commerce 커머스 플랫폼+결제
  - [stage] stack.agent 에이전트 계층
    - [service_ip] stack.agent.model 기반 모델 API
    - [service_ip] stack.agent.platform 에이전트 플랫폼
    - [service_ip] stack.agent.seat 좌석 과금 에이전트
    - [service_ip] stack.agent.credits 좌석 위에 얹는 AI 크레딧(하이브리드 과금)
    - [service_ip] stack.agent.deploy AI 배치 인력(전문 서비스)
```

## 2. 제품 고유 입력(bom 노드)

| id | 종류 | 스펙 | 수량/스택 | 가격 | 원가 비중 | 메이커 | box_ref |
|---|---|---|---|---|---|---|---|
| stack | product | 기업 1곳이 업무를 소프트웨어(와 AI 에이전트)로 처리하는 데 사는 것 전체. 층마다 과금 단위(좌석/사용 | — | — | — | — | 없음 — 레포에 체인 yaml 없음 |
| stack.infra.iaas | service_ip | 컴퓨트·스토리지. 사용량 과금. GPU 임대 포함 → AI Capex 직결(주제에서 제외 대상) | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Amazon (AWS)(XNAS:AMZN), Microsoft (Azure)(XNAS:MSFT), Alphabet (GCP)(XNAS:GOOGL), Oracle(XNYS:ORCL) | 없음 — 레포에 체인 yaml 없음 |
| stack.infra.edge | service_ip | 트래픽 전달·봇 관리·엣지 컴퓨트. 요청량 과금. 에이전트 트래픽이 늘면 Q 증가 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Cloudflare(XNYS:NET), Akamai(XNAS:AKAM), Fastly(XNYS:FSLY) | 없음 — 레포에 체인 yaml 없음 |
| stack.infra.data | service_ip | 운영 DB, 웨어하우스, 스트리밍. 사용량 과금 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Snowflake(XNYS:SNOW), Databricks(비상장·독립 비상장), MongoDB(XNAS:MDB), Oracle(XNYS:ORCL) | 없음 — 레포에 체인 yaml 없음 |
| stack.infra.obs | service_ip | 로그·메트릭·트레이스. 수집량 과금 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Datadog(XNAS:DDOG), Dynatrace(XNYS:DT) | 없음 — 레포에 체인 yaml 없음 |
| stack.dev.scm | service_ip | 저장소, 빌드, 바이너리 저장. 좌석+사용량 혼합 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Microsoft (GitHub)(XNAS:MSFT), GitLab(XNAS:GTLB), JFrog(XNAS:FROG), Atlassian(XNAS:TEAM) | 없음 — 레포에 체인 yaml 없음 |
| stack.dev.design | service_ip | UI 디자인, 프로토타입. 좌석+AI 크레딧 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Figma(XNYS:FIG), Adobe(XNAS:ADBE), Canva(비상장·독립 비상장) | 없음 — 레포에 체인 yaml 없음 |
| stack.dev.codegen | service_ip | 코드 생성 에이전트. 토큰·좌석 과금. 모델 회사와 직접 경쟁 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Anthropic(비상장·독립 비상장), OpenAI(비상장·독립 비상장), Anysphere (Cursor)(비상장·독립 비상장), Microsoft (Copilot)(XNAS:MSFT) | 없음 — 레포에 체인 yaml 없음 |
| stack.sec.endpoint | service_ip | 단말·워크로드 보호. 단말 수 과금 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | CrowdStrike(XNAS:CRWD), Microsoft(XNAS:MSFT), SentinelOne(XNYS:S) | 없음 — 레포에 체인 yaml 없음 |
| stack.sec.network | service_ip | 방화벽, 제로트러스트 접속. 사용자·대역폭 과금 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Palo Alto Networks(XNAS:PANW), Zscaler(XNAS:ZS), Fortinet(XNAS:FTNT), Cloudflare(XNYS:NET) | 없음 — 레포에 체인 yaml 없음 |
| stack.sec.identity | service_ip | 사람과 기계(에이전트) 신원. 신원 수 과금 → 에이전트가 늘면 Q 증가 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Okta(XNAS:OKTA), Microsoft (Entra)(XNAS:MSFT), SailPoint(XNAS:SAIL) | 없음 — 레포에 체인 yaml 없음 |
| stack.sec.vuln | service_ip | 스캔, 코드 보안. 자산 수 과금 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Qualys(XNAS:QLYS), Tenable(XNAS:TENB), Rapid7(XNAS:RPD) | 없음 — 레포에 체인 yaml 없음 |
| stack.sor.erp | service_ip | 회계 원장, 구매, 재고. 좌석·모듈 과금 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | SAP(XETR:SAP), Oracle(XNYS:ORCL), Workday(XNAS:WDAY), Intuit(XNAS:INTU) | 없음 — 레포에 체인 yaml 없음 |
| stack.sor.crm | service_ip | 고객 기록, 영업·마케팅 자동화. 좌석 과금 → 에이전트 대체 우려의 중심 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Salesforce(XNYS:CRM 20.0%), Oracle(XNYS:ORCL 4.1%), HubSpot(XNYS:HUBS), Microsoft (Dynamics)(XNAS:MSFT) | 없음 — 레포에 체인 yaml 없음 |
| stack.sor.hcm | service_ip | 인사·급여. 직원 수 과금 → 고용이 줄면 Q 감소 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Workday(XNAS:WDAY), ADP(XNAS:ADP), Paycom(XNYS:PAYC) | 없음 — 레포에 체인 yaml 없음 |
| stack.sor.itsm | service_ip | IT 요청·업무 흐름 자동화. 좌석+에이전트 과금 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | ServiceNow(XNYS:NOW), Atlassian(XNAS:TEAM) | 없음 — 레포에 체인 yaml 없음 |
| stack.collab.suite | service_ip | 문서·메일·화상·프로젝트 관리. 좌석 과금 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Microsoft (365)(XNAS:MSFT), Alphabet (Workspace)(XNAS:GOOGL), monday.com(XNAS:MNDY), Atlassian(XNAS:TEAM), Asana(XNYS:ASAN) | 없음 — 레포에 체인 yaml 없음 |
| stack.vert.health | service_ip | 임상·규제 문서, 영업, EHR. 좌석+모듈 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Veeva Systems(XNYS:VEEV), Doximity(XNYS:DOCS) | 없음 — 레포에 체인 yaml 없음 |
| stack.vert.fin | service_ip | 은행 코어, 보험 계약·청구. 계약 규모(보험료·자산) 연동 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Guidewire(XNYS:GWRE), Jack Henry(XNAS:JKHY), nCino(XNAS:NCNO) | 없음 — 레포에 체인 yaml 없음 |
| stack.vert.gov | service_ip | 지자체 행정, 건설 관리, 현장 서비스. 계약·공사 규모 연동 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Tyler Technologies(XNYS:TYL), Procore(XNYS:PCOR), ServiceTitan(XNAS:TTAN) | 없음 — 레포에 체인 yaml 없음 |
| stack.vert.smb | service_ip | POS, 예약, 급여 + 결제 수수료. 거래액 과금 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Toast(XNYS:TOST), Block (Square)(XNYS:XYZ) | 없음 — 레포에 체인 yaml 없음 |
| stack.vert.eng | service_ip | 제품 설계 도구. 좌석·토큰. EDA는 AI 칩 설계와 연동(주제에서 주의) | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Autodesk(XNAS:ADSK), Dassault Systèmes(XPAR:DSY), PTC(XNAS:PTC), Synopsys(XNAS:SNPS), Cadence(XNAS:CDNS) | 없음 — 레포에 체인 yaml 없음 |
| stack.agent.model | service_ip | 토큰 과금. 비상장 모델 회사와 하이퍼스케일러 → AI Capex 직결(주제에서 제외 대상) | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | OpenAI(비상장·독립 비상장), Anthropic(비상장·독립 비상장), Alphabet(XNAS:GOOGL) | 없음 — 레포에 체인 yaml 없음 |
| stack.agent.platform | service_ip | 기록 시스템 위에서 일을 수행. 대화·작업 건당 과금 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Salesforce (Agentforce)(XNYS:CRM), ServiceNow(XNYS:NOW), Microsoft(XNAS:MSFT), Sierra(비상장·독립 비상장) | 없음 — 레포에 체인 yaml 없음 |
| stack.agent.seat | service_ip | 에이전트를 좌석으로 파는 모델 | 없음 — 에이전트는 사람 수가 아니라 작업량으로 과금되는 방향(검증 필요) | 없음 — 에이전트는 사람 수가 아니라 작업량으로 과금되는 방향(검증 필요) | 없음 — 에이전트는 사람 수가 아니라 작업량으로 과금되는 방향(검증 필요) | 없음 — 에이전트는 사람 수가 아니라 작업량으로 과금되는 방향(검증 필요) | 없음 — 레포에 체인 yaml 없음 |
| stack.onprem | service_ip | 설치형 일시불 판매 | 없음 — 신규 판매는 대부분 구독으로 전환(검증 필요) | 없음 — 신규 판매는 대부분 구독으로 전환(검증 필요) | 없음 — 신규 판매는 대부분 구독으로 전환(검증 필요) | 없음 — 신규 판매는 대부분 구독으로 전환(검증 필요) | 없음 — 레포에 체인 yaml 없음 |
| stack.sec.nhi | service_ip | 사람이 아닌 신원의 발급·권한 관리. 에이전트 수에 비례. AI 실패 시 영향 작음, 성공 시 Q 급증 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | SailPoint(XNAS:SAIL), Okta(XNAS:OKTA), Palo Alto Networks (CyberArk)(XNAS:PANW) | 없음 — 레포에 체인 yaml 없음 |
| stack.vert.commerce | service_ip | 온라인·오프라인 판매 운영. 거래액(GMV)과 결제 침투율로 과금. 좌석과 무관 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Shopify(XNAS:SHOP) | 없음 — 레포에 체인 yaml 없음 |
| stack.agent.credits | service_ip | 기존 좌석 요금에 사용량 크레딧을 더하는 전환 장치. 좌석 감소를 사용량으로 메우는지가 관건 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | Figma(XNYS:FIG), monday.com(XNAS:MNDY), Atlassian(XNAS:TEAM) | 없음 — 레포에 체인 yaml 없음 |
| stack.agent.deploy | service_ip | 대형 AI 계약에 붙는 현장 배치·컨설팅. 구독 매출 일부가 서비스 매출로 이동 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 없음 — 범주라 단가·수량 축이 성립하지 않음 | 미측정 — Gartner 범주별 지출 표 미확보(총액만 확인) | ServiceNow(XNYS:NOW), Palantir(XNAS:PLTR), Accenture(XNYS:ACN) | 없음 — 레포에 체인 yaml 없음 |

## 3. 공정 묶음(참조된 것만) — 장비·소재·메이커의 유일한 정의

