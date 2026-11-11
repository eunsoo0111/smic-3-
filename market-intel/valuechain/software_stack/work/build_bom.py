"""software_stack bom.json 빌더 — V0(무하네스) + 검색 보강 + V1 채움. 실행: python3 software_stack/work/build_bom.py (valuechain 폴더에서)"""
import json, sys
sys.path.insert(0, "_contracts")
from v0_helpers import *

N = json.load(open("software_stack/work/v0_blind.json"))["nodes"]
A = "없음 — 범주라 단가·수량 축이 성립하지 않음"
C = "미측정 — Gartner 범주별 지출 표 미확보(총액만 확인)"

def add(id, parent, name, spec):
    n = I(id, parent, "service_ip", name, spec)
    n["qty_per_unit"] = n["price"] = A
    return n

# ── V0 보강(검색 뒤 추가된 칸) ─────────────────────────────────────────
N += [
 add("stack.sec.nhi", "stack.sec", "비인간(에이전트·기계) 신원", "사람이 아닌 신원의 발급·권한 관리. 에이전트 수에 비례. AI 실패 시 영향 작음, 성공 시 Q 급증"),
 add("stack.vert.commerce", "stack.vert", "커머스 플랫폼+결제", "온라인·오프라인 판매 운영. 거래액(GMV)과 결제 침투율로 과금. 좌석과 무관"),
 add("stack.agent.credits", "stack.agent", "좌석 위에 얹는 AI 크레딧(하이브리드 과금)", "기존 좌석 요금에 사용량 크레딧을 더하는 전환 장치. 좌석 감소를 사용량으로 메우는지가 관건"),
 add("stack.agent.deploy", "stack.agent", "AI 배치 인력(전문 서비스)", "대형 AI 계약에 붙는 현장 배치·컨설팅. 구독 매출 일부가 서비스 매출로 이동"),
]
fill(N, "stack", note="총액: 2026년 세계 소프트웨어 지출 1.44조 달러(+15.1%, Gartner 4월 전망, S201). 2026년 소프트웨어 ETF와 반도체 ETF는 대체로 반대로 움직임(6/30 이후 IGV 약 +17%, SOXX 약 −22%, S202). 선행 PER 약 35배 → 20~22.7배(S203)")

def M(id, makers, q=None, **kw):
    fill(N, id, cost_share_pct=C, makers=makers, **kw)
    if q:
        fill(N, id, open_questions=q)

T3 = ("③", "S000")
M("stack.infra.iaas", [mk("Amazon (AWS)", "XNAS:AMZN", "US", "main", *T3), mk("Microsoft (Azure)", "XNAS:MSFT", "US", "main", *T3),
                        mk("Alphabet (GCP)", "XNAS:GOOGL", "US", "main", *T3), mk("Oracle", "XNYS:ORCL", "US", "second", *T3)],
  ["주제에서 제외: AI Capex 직결"])
M("stack.infra.edge", [mk("Cloudflare", "XNYS:NET", "US", "main", "②", "S206", note="3Q26 매출 +39%(사상 최고 성장률), 순매출유지율 122%"),
                        mk("Akamai", "XNAS:AKAM", "US", "main", *T3), mk("Fastly", "XNYS:FSLY", "US", "second", *T3)],
  ["에이전트 트래픽이 매출의 몇 %인지", "하이퍼스케일러 자체 엣지와의 경쟁"])
M("stack.infra.data", [mk("Snowflake", "XNYS:SNOW", "US", "main", "①", "S213", note="2Q FY27 제품 매출 14.9억 달러(+37%, 3분기 연속 가속), 순매출유지율 126%"),
                        mk("Databricks", None, "US", "main", *T3), mk("MongoDB", "XNAS:MDB", "US", "second", *T3), mk("Oracle", "XNYS:ORCL", "US", "main", *T3)])
M("stack.infra.obs", [mk("Datadog", "XNAS:DDOG", "US", "main", "①", "S212", note="3Q26 매출 약 12.0억 달러(+35%). 10-Q가 최대 고객 사용량 감소를 경고"),
                       mk("Dynatrace", "XNYS:DT", "US", "second", *T3)],
  ["Datadog 최대 고객이 AI 모델 회사인지(AI 연동도)"])
M("stack.dev.scm", [mk("Microsoft (GitHub)", "XNAS:MSFT", "US", "main", *T3), mk("GitLab", "XNAS:GTLB", "US", "second", *T3),
                     mk("JFrog", "XNAS:FROG", "IL", "second", "①", "S207", note="3Q26 매출 1.792억 달러(+31%), 순매출유지율 124%. 코드 생산량이 늘면 바이너리 저장량 증가"),
                     mk("Atlassian", "XNAS:TEAM", "AU", "second", "①", "S210")])
M("stack.dev.design", [mk("Figma", "XNYS:FIG", "US", "main", "①", "S205", note="3Q26 순매출유지율 131%. ARR 1만 달러 이상 고객의 65%가 주간 에이전트 사용, 80% 이상이 AI 크레딧 소비"),
                        mk("Adobe", "XNAS:ADBE", "US", "main", *T3), mk("Canva", None, "AU", "second", *T3)])
M("stack.dev.codegen", [mk("Anthropic", None, "US", "main", *T3), mk("OpenAI", None, "US", "main", *T3), mk("Anysphere (Cursor)", None, "US", "second", *T3),
                         mk("Microsoft (Copilot)", "XNAS:MSFT", "US", "main", *T3)], ["주제에서 제외: 모델 회사와 직접 경쟁, 대부분 비상장"])
M("stack.sec.endpoint", [mk("CrowdStrike", "XNAS:CRWD", "US", "main", "①", "S218", note="2Q FY27 순증 ARR 3.33억 달러(+51%), 기말 ARR 약 58.4억 달러(+25%, 4분기 연속 가속). 연간 순증 ARR 가이던스 +34%"),
                          mk("Microsoft", "XNAS:MSFT", "US", "main", *T3), mk("SentinelOne", "XNYS:S", "US", "second", *T3)])
M("stack.sec.network", [mk("Palo Alto Networks", "XNAS:PANW", "US", "main", "②", "S208", note="FY26 3Q 매출 30억 달러(+31%), 사상 최고 분기 보도"),
                         mk("Zscaler", "XNAS:ZS", "US", "main", *T3), mk("Fortinet", "XNAS:FTNT", "US", "main", *T3), mk("Cloudflare", "XNYS:NET", "US", "second", "②", "S206")])
M("stack.sec.identity", [mk("Okta", "XNAS:OKTA", "US", "main", "①", "S220", note="2Q FY27 비GAAP 영업이익률 28%. 성장률은 이번 검색에서 확인 못 함"),
                          mk("Microsoft (Entra)", "XNAS:MSFT", "US", "main", *T3), mk("SailPoint", "XNAS:SAIL", "US", "second", "②", "S219")])
M("stack.sec.nhi", [mk("SailPoint", "XNAS:SAIL", "US", "main", "②", "S219", note="1Q FY27 ARR 11.63억 달러(+26%), SaaS ARR +36%. 비인간 신원이 신원 증가분의 40%, 에이전트 파이프라인 분기 중 2배. 가이던스에는 AI 기여를 크게 넣지 않음"),
                     mk("Okta", "XNAS:OKTA", "US", "main", "①", "S220", note="CEO가 에이전트를 신원이 필요한 새 인력으로 규정"),
                     mk("Palo Alto Networks (CyberArk)", "XNAS:PANW", "US", "main", *T3)])
M("stack.sec.vuln", [mk("Qualys", "XNAS:QLYS", "US", "second", *T3), mk("Tenable", "XNAS:TENB", "US", "second", *T3), mk("Rapid7", "XNAS:RPD", "US", "second", *T3)],
  ["AI가 취약점을 찾아 주면 스캐너 수요가 늘어나나 줄어드나(Mythos 이후 보안주 급락 후 급등, S208)"])
M("stack.sor.erp", [mk("SAP", "XETR:SAP", "DE", "main", *T3), mk("Oracle", "XNYS:ORCL", "US", "main", *T3),
                     mk("Workday", "XNAS:WDAY", "US", "main", "①", "S222"), mk("Intuit", "XNAS:INTU", "US", "main", *T3)])
M("stack.sor.crm", [mk("Salesforce", "XNYS:CRM", "US", "main", "①", "S211", share=val(20.0, "%", "S226", "②", "세계 CRM 매출 2025년(IDC, 2차 인용). 2021년 23.8%에서 하락", "2025"),
                        note="2Q FY27 매출 113억 달러(+11%). Agentforce ARR 15억 달러 초과(+240%, 정의 확대 포함)"),
                     mk("Oracle", "XNYS:ORCL", "US", "second", "②", "S226", share=val(4.1, "%", "S226", "②", "세계 CRM 매출 2025년(IDC, 2차 인용)", "2025")),
                     mk("HubSpot", "XNYS:HUBS", "US", "second", "②", "S204", note="3Q26 순매출유지율 101%(전분기比 −1%p), 연간 −2%p 전망. 좌석 최소 수량 폐지로 활성 좌석은 +34%"),
                     mk("Microsoft (Dynamics)", "XNAS:MSFT", "US", "second", *T3)])
M("stack.sor.hcm", [mk("Workday", "XNAS:WDAY", "US", "main", "①", "S222", note="2Q FY27 구독 매출 24.71억 달러(+13.9%), 연간 +13% 가이던스"),
                     mk("ADP", "XNAS:ADP", "US", "main", *T3), mk("Paycom", "XNYS:PAYC", "US", "second", *T3)],
  ["직원 수 과금이라 고용 감소에 직접 노출 — 고객사 인원 추이"])
M("stack.sor.itsm", [mk("ServiceNow", "XNYS:NOW", "US", "main", "①", "S209", note="3Q26 구독 매출 39.88억 달러(+21%), cRPO +20.5%. 에이전트 AI 소비량 전년比 13배 이상, AI ACV 목표 17억 달러로 상향"),
                      mk("Atlassian", "XNAS:TEAM", "AU", "second", "①", "S210", note="1Q FY27 매출 17.72억 달러(+24%), 클라우드 +31%. 구독 ARR 성장률을 18.5%로 가이던스해 주가 하락")])
M("stack.collab.suite", [mk("Microsoft (365)", "XNAS:MSFT", "US", "main", *T3), mk("Alphabet (Workspace)", "XNAS:GOOGL", "US", "main", *T3),
                          mk("monday.com", "XNAS:MNDY", "IL", "second", "①", "S221", note="3Q26 매출 3.775억 달러(+19.1%). 순매출유지율 108%(1년 전 117%), 연말 107% 전망. 실적 후 주가 약 −9%. AI ARR 3,600만 달러"),
                          mk("Atlassian", "XNAS:TEAM", "AU", "main", "①", "S210"), mk("Asana", "XNYS:ASAN", "US", "second", *T3)])
M("stack.vert.health", [mk("Veeva Systems", "XNYS:VEEV", "US", "main", "①", "S214", note="1Q FY27 매출 8.829억 달러(+16%). FY27 가이던스 약 36.8~36.9억 달러. 산업 특화 앱+에이전트 회사로 전환 선언"),
                         mk("Doximity", "XNYS:DOCS", "US", "second", *T3, note="SMIC 2025.05 커버")])
M("stack.vert.fin", [mk("Guidewire", "XNYS:GWRE", "US", "main", "①", "S215", note="4Q FY26 매출 4.111억 달러(+15%)"),
                      mk("Jack Henry", "XNAS:JKHY", "US", "main", *T3), mk("nCino", "XNAS:NCNO", "US", "second", *T3)])
M("stack.vert.gov", [mk("Tyler Technologies", "XNYS:TYL", "US", "main", "②", "S216", note="3Q26 SaaS 매출 +21.2%, 반복 매출 +11.0%, 분기 FCF 2.77억 달러(최고). AI 기능 포함 계약 약 300건. 2027년 가이던스는 유보"),
                      mk("Procore", "XNYS:PCOR", "US", "main", "①", "S223", note="3Q26 매출 약 4.02억 달러(+18.7%, 인수 제외 +17.1%), 유기적 cRPO +22.6%, 총매출유지율 95%. 실적 후 주가 +11%"),
                      mk("ServiceTitan", "XNAS:TTAN", "US", "second", "①", "S224", note="2Q FY27 매출 2.928억 달러(+21%), 거래액 268억 달러(+17%), 사용량 매출 +24%. 기존 고객 작업 건수 둔화 언급")])
M("stack.vert.smb", [mk("Toast", "XNYS:TOST", "US", "main", "②", "S217", note="3Q26 매출 19.8억 달러(+21%), ARR 25.03억 달러(+24%), 결제액 618억 달러(+20%), 매장 약 18.9만 개. GAAP EPS 미스로 주가 하락"),
                      mk("Block (Square)", "XNYS:XYZ", "US", "main", *T3)])
M("stack.vert.commerce", [mk("Shopify", "XNAS:SHOP", "CA", "main", "①", "S225", note="3Q26 매출 37.4억 달러(+32%), GMV 1,191억 달러(6분기 연속 약 +30%), B2B GMV +74%, 결제 침투율 68% 초과. 지출 계획 탓에 주가 −7.6%")],
  ["AI 쇼핑 에이전트가 GMV를 늘리나, 수수료를 가져가나"])
M("stack.vert.eng", [mk("Autodesk", "XNAS:ADSK", "US", "main", *T3), mk("Dassault Systèmes", "XPAR:DSY", "FR", "main", *T3), mk("PTC", "XNAS:PTC", "US", "second", *T3),
                      mk("Synopsys", "XNAS:SNPS", "US", "main", *T3, note="EDA는 AI 칩 설계와 연동"), mk("Cadence", "XNAS:CDNS", "US", "main", *T3, note="EDA는 AI 칩 설계와 연동")])
M("stack.agent.model", [mk("OpenAI", None, "US", "main", *T3), mk("Anthropic", None, "US", "main", *T3), mk("Alphabet", "XNAS:GOOGL", "US", "main", *T3)],
  ["주제에서 제외: AI Capex 직결"])
M("stack.agent.platform", [mk("Salesforce (Agentforce)", "XNYS:CRM", "US", "main", "①", "S211"), mk("ServiceNow", "XNYS:NOW", "US", "main", "①", "S209"),
                            mk("Microsoft", "XNAS:MSFT", "US", "main", *T3), mk("Sierra", None, "US", "second", *T3)])
M("stack.agent.credits", [mk("Figma", "XNYS:FIG", "US", "main", "①", "S205"), mk("monday.com", "XNAS:MNDY", "IL", "second", "①", "S221", note="AI ARR 3,600만 달러"),
                           mk("Atlassian", "XNAS:TEAM", "AU", "main", "①", "S210", note="엔터프라이즈 클라우드 고객의 87% 이상이 Rovo 사용")],
  ["크레딧 매출이 좌석 감소분보다 큰지 회사별로(10-Q)"])
M("stack.agent.deploy", [mk("ServiceNow", "XNYS:NOW", "US", "main", "①", "S209", note="대형 AI 계약에 배치 인력을 붙이면서 단기 구독 매출·cRPO 일부가 전문 서비스로 이동"),
                          mk("Palantir", "XNAS:PLTR", "US", "main", *T3, note="SMIC 2024.05 커버"), mk("Accenture", "XNYS:ACN", "IE", "main", *T3)])

SRC = [
 ("S000", "model_knowledge", "모델 지식", "모델 지식 — 검증 필요", "2026-06", "③", "메이커 실재·역할 등 사전 지식. V4에서 ①②로 교체"),
 ("S201", "web", "https://campustechnology.com/articles/2026/05/20/gartner-estimates-worldwide-it-spending-at-6-31t-for-2026.aspx", "Gartner 2026 IT 지출 전망(4월)", "2026-04", "②", "소프트웨어 1.44조 달러, +15.1%. 범주별 표는 못 구함"),
 ("S202", "web", "https://www.benzinga.com/markets/market-summary/26/09/61782229/beyond-nvidia-why-software-stocks-just-crushed-semiconductors-in-a-historic-25-year-shift", "Benzinga: 소프트웨어 대 반도체 로테이션", "2026-09", "②", "집계 기준일 불명"),
 ("S203", "web", "https://www.softwareseni.com/the-saas-reckoning-explained-what-happened-to-enterprise-software-in-2026", "2026 SaaS 밸류에이션 조정", "2026", "②", ""),
 ("S204", "web", "https://www.webull.com/news/15872536220507136", "HubSpot 3Q26 콜", "2026-11", "②", "회사 주장"),
 ("S205", "web", "https://www.sec.gov/Archives/edgar/data/0001579878/000162828026070133/q326pressrelease.htm", "Figma 3Q26 8-K", "2026-11", "①", ""),
 ("S206", "web", "https://finance.yahoo.com/markets/stocks/articles/cloudflare-inc-net-q3-2026-052238415.html", "Cloudflare 3Q26 콜 요약", "2026-11", "②", ""),
 ("S207", "web", "https://www.sec.gov/Archives/edgar/data/0001800667/000119312526449797/frog-ex99_1.htm", "JFrog 3Q26 8-K", "2026-11", "①", ""),
 ("S208", "web", "https://letsdatascience.com/news/palo-alto-crowdstrike-report-record-quarter-on-ai-driven-cyb-7c5755b4", "Palo Alto·CrowdStrike 사상 최고 분기", "2026", "②", "2차 요약, 주가 수치 미검증"),
 ("S209", "web", "https://www.sec.gov/Archives/edgar/data/0001373715/000137371526000092/erq3fy26.htm", "ServiceNow 3Q26 8-K", "2026-10", "①", ""),
 ("S210", "web", "https://s206.q4cdn.com/270053503/files/doc_financials/2027/q1/TEAM-Q1-2027-Earnings-Release.pdf", "Atlassian 1Q FY27 실적", "2026-11-05", "①", ""),
 ("S211", "web", "https://www.salesforce.com/news/press-releases/2026/08/26/fy27-q2-earnings/", "Salesforce 2Q FY27 실적", "2026-08-26", "①", ""),
 ("S212", "web", "https://www.sec.gov/Archives/edgar/data/0001561550/000162828026069792/ex-991x20260930x8k.htm", "Datadog 3Q26 8-K·10-Q", "2026-11-04", "①", ""),
 ("S213", "web", "https://www.nasdaq.com/press-release/snowflake-reports-financial-results-second-quarter-fiscal-2027-2026-09-02", "Snowflake 2Q FY27 실적", "2026-09-02", "①", ""),
 ("S214", "web", "https://www.sec.gov/Archives/edgar/data/0001393052/000139305226000032/veev-20260731xex991.htm", "Veeva 8-K", "2026-08", "①", "2분기 실제 수치는 검색 요약에 없었음"),
 ("S215", "web", "https://ir.guidewire.com/news-releases/news-release-details/guidewire-announces-fourth-quarter-and-fiscal-year-2026", "Guidewire 4Q FY26 실적", "2026-09", "①", ""),
 ("S216", "web", "https://www.fool.com/earnings/call-transcripts/2026/10/29/tyler-technologies-tyl-q3-2026-earnings-call-transcript/", "Tyler 3Q26 콜", "2026-10-29", "②", ""),
 ("S217", "web", "https://www.gurufocus.com/news/9166711/toast-inc-reports-strong-q3-2026-results-eps-of-029-and-revenue-of-198-billion-beat-estimates", "Toast 3Q26 요약", "2026-11", "②", ""),
 ("S218", "web", "https://www.sec.gov/Archives/edgar/data/0001535527/000153552726000029/crwd-20260826xex991.htm", "CrowdStrike 2Q FY27 8-K", "2026-08-26", "①", "기말 ARR은 2차 요약"),
 ("S219", "web", "https://finance.yahoo.com/markets/stocks/articles/sailpoint-q1-earnings-call-highlights-150636862.html", "SailPoint 1Q FY27 콜 요약", "2026-06", "②", "2분기 실적은 못 찾음"),
 ("S220", "web", "https://www.sec.gov/Archives/edgar/data/0001660134/000166013426000068/okta-7312026_ex991.htm", "Okta 2Q FY27 8-K", "2026-08", "①", ""),
 ("S221", "web", "https://www.sec.gov/Archives/edgar/data/0001845338/000117891326005085/exhibit_99-1.htm", "monday.com 3Q26 6-K", "2026-11-09", "①", ""),
 ("S222", "web", "https://newsroom.workday.com/2026-08-27-Workday-Announces-Fiscal-2027-Second-Quarter-Financial-Results", "Workday 2Q FY27 실적", "2026-08-27", "①", ""),
 ("S223", "web", "https://www.sec.gov/Archives/edgar/data/0001611052/000161105226000002/pcor-q326x8xkxexx991.htm", "Procore 3Q26 8-K", "2026-11", "①", ""),
 ("S224", "web", "https://www.stocktitan.net/sec-filings/TTAN/8-k-service-titan-inc-reports-material-event-f44e975b3277.html", "ServiceTitan 2Q FY27 8-K", "2026-09-08", "①", ""),
 ("S225", "web", "https://www.sec.gov/Archives/edgar/data/0001594805/000159480526000067/exhibit991pressreleaseq320.htm", "Shopify 3Q26 8-K", "2026-11", "①", ""),
 ("S226", "web", "https://cxfoundation.com/news/salesforce-extends-crm-market-lead", "IDC CRM 점유율(2차 인용)", "2026-06", "②", ""),
]
write_sources("software_stack/sources.jsonl", SRC)
dump("software_stack/bom.json", "software_stack", "엔터프라이즈 소프트웨어 스택", "기업 소프트웨어 지출 100(범주별 비중)", N,
     status="v3_queued",
     approved={"who": "Claude(본체)", "at": "2026-11-11", "stage": "V0", "note": "무하네스 초안 33노드에 검색으로 4노드(비인간 신원, 커머스+결제, AI 크레딧, 배치 인력) 보강 후 승인. 물리적 제품이 아니라 지출 범주 트리로 변형 적용"},
     log=[{"stage": "V0", "at": "2026-11-11", "by": "Claude(본체)", "what": "v0_blind.json 작성 후 검색 보강, v0_diff.md"},
          {"stage": "V1", "at": "2026-11-11", "by": "Claude(본체, 서브 없이 직접)", "what": "입력 27개 메이커·실적 지표 채움. 출처 S201~S226. 범주별 지출 비중은 전부 미측정"},
          {"stage": "V2", "at": "2026-11-11", "by": "Claude(본체)", "what": "레포에 core/valuechain yaml이 없어 box_ref 전부 빈칸 문면"},
          {"stage": "V3", "at": "2026-11-11", "by": "Claude(본체)", "what": "GAPS.md·BOM.md. 착수 큐는 비중이 전부 대체값이라 참고용"}])
