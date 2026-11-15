# -*- coding: utf-8 -*-
"""MDA Space research workbook data. One row = one claim."""

AS_OF = "2026-11-15"

# ---------------------------------------------------------------- sources
# (ID, 자료명, 자료 성격, 발표·기준일, URL 또는 경로, 사용 범위·주의)
SOURCES = [
 ("F01","MDA 3Q 2026 실적 릴리스","회사 공시","2026-11-05","https://mda-en.investorroom.com/2026-11-05-MDA-SPACE-REPORTS-THIRD-QUARTER-2026-RESULTS","분기 실적·잔고·수주·가이던스. 계약 금액은 거의 없음."),
 ("F02","MDA 4Q·FY2025 실적 릴리스","회사 공시","2026-03-04","https://mda-en.investorroom.com/2026-03-04-MDA-SPACE-REPORTS-FOURTH-QUARTER-AND-FISCAL-2025-RESULTS","연간 실적·최초 2026 가이던스·파이프라인 C$40B."),
 ("F03","MDA FY2025 MD&A (SEC F-10 Ex.4.3)","회사 공시","2026-03-03","https://www.sec.gov/Archives/edgar/data/1857047/000110465926025809/tm266080d2_ex4-3.htm","계약별 금액·SatixFy·CHORUS·소송. 뒷부분 1/3은 요약본으로만 읽음."),
 ("F04","MDA FY2025 Annual Information Form (SEC F-10 Ex.4.1)","회사 공시","2025-12-31 기준","https://www.sec.gov/Archives/edgar/data/1857047/000110465926025809/tm266080d2_ex4-1.htm","사업 설명·고객·경쟁·리스크·시설. 8회로 나눠 전체 열람."),
 ("F05","MDA 2Q 2026 실적 릴리스","회사 공시","2026-08-07","https://mda-en.investorroom.com/2026-08-07-MDA-SPACE-REPORTS-SECOND-QUARTER-2026-RESULTS","수주 808.9·잔고 4,003.0. 검색 요약으로 확인."),
 ("F06","MDA 3Q 2026 Investor Presentation","회사 IR 자료","2026-11","https://filecache.investorroom.com/mr5ircnw_mda/754/MDA_Space_Ltd-Q3_2026-Investor_Presentation.pdf","p4·6·7·9·12·14·16. 다른 브랜치 노트(N03)를 거쳐 인용했고 이번에 원본을 직접 읽지 않음. 원그래프 수치는 눈대중."),
 ("F07","MDA 2026-07 Prospectus Supplement (bought deal)","회사 공시","2026-07-08","https://www.sec.gov/Archives/edgar/data/0001857047/000110465926082327/tm2619705-6_suppl.htm","증자 조건·직전 종가. 검색 요약으로 확인."),
 ("F08","MDA Form 6-K: BCT 인수 계약","회사 공시","2026-06-19","https://www.sec.gov/Archives/edgar/data/0001857047/000110465926075950/tm2618399d1_ex99-1.htm","가격·조건·지연 시 추가 지급. 검색 요약으로 확인."),
 ("F09","MDA 릴리스: Lightspeed 확장 C$474M","회사 공시","2026-08-04","https://mda-en.investorroom.com/2026-08-04-MDA-SPACE-AWARDED-474-MILLION-TO-EXPAND-THE-TELESAT-LIGHTSPEED-LEO-CONSTELLATION","198기 + 27기."),
 ("F10","MDA 릴리스: EchoStar 계약 업데이트","회사 공시","2025-09-08","https://mda-en.investorroom.com/2025-09-08-MDA-SPACE-PROVIDES-UPDATE-ON-ECHOSTAR-CONTRACT","편의 해지 통보. 해지 대금은 비공개."),
 ("F11","MDA 릴리스: 한화시스템 K-LEO MOU","회사 공시","2026-01-26","https://mda-en.investorroom.com/2026-01-26-MDA-SPACE-AND-HANWHA-SIGN-MOU-TO-PURSUE-KOREAN-MILITARY-CONSTELLATION-PROGRAM","MOU일 뿐 계약 아님."),
 ("F12","MDA 릴리스: Mitsubishi Electric 방위통신위성","회사 공시","2026-06-25","https://mda-en.investorroom.com/2026-06-25-MDA-SPACE-SELECTED-BY-MITSUBISHI-ELECTRIC-FOR-NEXT-GENERATION-DEFENCE-COMMUNICATIONS-SATELLITE-PROGRAM","금액 미공개."),
 ("F13","MDA 릴리스: BAE Systems MEO Epoch 2","회사 공시","2026-06-02","https://mda.space/article/mda-space-selected-by-bae-systems-for-u.s.-space-systems-command-meo-epoch2-constellation","안테나·제어전자. 금액 미공개."),
 ("F14","MDA 릴리스: Airbus OneWeb 안테나 재수주","회사 공시","2026-04-20","https://mda.space/article/mda-space-contracted-by-airbus-for-repeat-order-of-antennas-for-oneweb-constellation-extension","Ka 880개+ · Ku 440개. 금액 미공개."),
 ("F15","MDA 릴리스: 몬트리올 대량생산 시설 준공","회사 공시","2026-05","https://mda.space/article/mda-space-inaugurates-high-volume-satellite-manufacturing-facility-in-montreal","설계 용량은 회사 표현(up to)."),
 ("F16","MDA·CSA 릴리스: RCM 보충위성 C$688M","회사 공시","2026-06","https://mda.space/article/canadian-space-agency-and-mda-space-conclude-contract-for-replenishment-satellite-valued-at-688m","2Q26 수주에 반영."),
 ("F17","MDA 릴리스: CLS 인수 firm offer","회사 공시","2026-07-08","https://mda.space/article/mda-space-enters-into-firm-offer-to-acquire-collecte-localisation-satellites-a-global-leader-in-ai-driven-earth-observation-data-analytics","70%·€567M."),
 ("T01","MDA 3Q 2026 컨퍼런스콜 전사본 (Motley Fool)","콜 전사본","2026-11-05","https://www.fool.com/earnings/call-transcripts/2026/11/05/mda-space-mda-q3-2026-earnings-call-transcript/","일부 문장이 깨져 있음. 인용 전 음성 대조."),
 ("G01","캐나다 국방투자청: ESCP-P 계약 발표","정부 발표","2026-08-04","https://www.canada.ca/en/defence-investment-agency/news/2026/08/the-government-of-canada-awards-a-military-communications-contract-to-support-arctic-sovereignty-and-national-security.html","Telesat 2.3B·MDA MEO 프라임(협상 중)."),
 ("G02","캐나다 Budget 2026 Chapter 5","정부 발표","2026","https://budget.canada.ca/2026/report-rapport/chap5-en.html","국방비 총량. 우주 항목 세부는 거의 없음."),
 ("G03","PBO: Canada's Defence Spending Commitments Primer","정부 기관 보고서","2026-10-06","https://www.pbo-dpb.ca/en/publications/NT-2627-013-S--canada-defence-spending-commitments-primer--engagements-canada-matiere-depenses-defense-guide-introduction","NATO 3.5% 경로."),
 ("G04","캐나다 국방산업전략","정부 발표","2026-02","https://www.canada.ca/en/global-affairs/news/2026/02/canada-advances-defence-industrial-strategy-to-strengthen-security-sovereignty-and-prosperity.html","브랜치 노트 경유. C$180B 등 수치는 원문 재확인."),
 ("W01","Via Satellite: Telesat Lightspeed 2028년 중반으로 지연","업계 매체","2026-10-29","https://www.satellitetoday.com/finance/2026/10/29/telesat-delays-lightspeed-service-entry-to-mid-2028-goldberg-addresses-launch-crunch-and-sovereign-demand/","Telesat 3Q 콜 요약. MDA 책임 언급은 없음."),
 ("W02","SpaceNews: Global Telesat Lightspeed service delayed to mid-2028","업계 매체","2026-10-29","https://spacenews.com/global-telesat-lightspeed-service-delayed-to-mid-2028/","프라임 MDA의 조립·소프트웨어 문제로 서술."),
 ("W03","Space Intel Report: MDA on Lightspeed delay","업계 매체","2026-11","https://www.spaceintelreport.com/mda-space-on-telesat-lightspeed-delay-and-how-its-positioning-itself-to-win-us-and-european-military-satellite-business/","제목·요약만 확인(유료)."),
 ("W04","Via Satellite: Amazon의 Globalstar 인수","업계 매체","2026-04-14","https://www.satellitetoday.com/connectivity/2026/04/14/amazon-enters-d2d-market-with-globalstar-acquisition-and-system-plans/","자체 D2D 2028 계획."),
 ("W05","Via Satellite: FCC, Amazon–Globalstar 승인","업계 매체","2026-10-27","https://www.satellitetoday.com/connectivity/2026/10/27/amazon-secures-fcc-approval-for-globalstar-acquisition/","종결 2027 예정."),
 ("W06","SpaceQ: EchoStar cancels contract with MDA","업계 매체","2025-09-08","https://spaceq.ca/echostar-cancels-1-8b-contract-with-mda-space/","C$1.8B = US$1.3B."),
 ("W08","Payload: The State of Satcom 2026","업계 매체","2026-04-06","https://payloadspace.com/the-state-of-satcom-2026/","운영사 인터뷰 모음. 시장 규모 수치 없음."),
 ("W09","SatNews: What the SpaceX IPO Changes for Every Satellite Operator","업계 논평","2026-04-07","https://satnews.com/2026/04/07/what-the-spacex-ipo-changes-for-every-satellite-operator/","상장 전 논평. 시각으로만 인용."),
 ("W10","Breaking Defense: Novaspace 위성 시장 전망","업계 매체","2025-10","https://breakingdefense.com/2025/10/defense-to-anchor-exploding-satellite-market-over-next-decade-novaspace/","7% 열린 시장·70% 자국 캡티브. 원보고서는 유료."),
 ("W11","CompositesWorld: Novaspace 43,000 satellites 2025-2034","업계 매체","2025-10","https://www.compositesworld.com/news/novaspace-reports-43000-satellites-to-be-launched-2025-2034","$665B는 제조+발사."),
 ("W12","Defense News: Novaspace 우주 ISR 전망","업계 매체","2026-09-15","https://www.defensenews.com/space/2026/09/15/space-based-isr-launches-to-grow-fourfold-in-next-decade-novaspace-says/?nb=1","우주 국방 예산 $74B → $121B."),
 ("W13","Space Economy Institute: IRIS² Contracts","업계 매체","2026-09-11","https://spaceeconomyinstitute.com/2026/09/11/iris2-contracts-europe-sovereign-satellite-network/","348기·€15.6B."),
 ("W14","SatNews: Germany Commits €35B","업계 매체","2026-02-28","https://satnews.com/2026/02/28/germany-commits-e35-billion-to-leo-resilience-and-non-kinetic-deterrence/","공약 규모. 계약 아님."),
 ("W15","Via Satellite: MDA, IRIS² 66기 안테나","업계 매체","2026-10-30","https://www.satellitetoday.com/technology/2026/10/30/mda-space-to-build-antenna-subsystems-for-66-iris%C2%B2-leo-satellites/","ATP·C$100M 이상·4Q26 잔고 편입."),
 ("W17","Aviation Week: Canada Pivots Canadarm3","업계 매체","2026","https://aviationweek.com/space/space-exploration/canada-pivots-canadarm3-lunar-exploration","달 표면 전용."),
 ("W18","Globe and Mail: NASA drops lunar space station","일간지","2026-03","https://www.theglobeandmail.com/canada/science/article-nasa-drops-lunar-space-station-puts-canadian-robotic-arm-on-uncertain/","Gateway 중단·주가 −11%."),
 ("W19","SpaceQ: RADARSAT replenishment $688M","업계 매체","2026-06","https://spaceq.ca/mda-space-moves-to-build-phase-with-688m-radarsat-replenishment-satellite-contract-award/",""),
 ("W20","SpaceQ: CHORUS 41 commitments","업계 매체","2026-05","https://spaceq.ca/mda-space-reports-41-commitments-for-chorus-ahead-of-launch/","약정이지 계약 아님."),
 ("W21","GovConWire: MDA to Acquire Blue Canyon","업계 매체","2026-06","https://www.govconwire.com/articles/mda-space-blue-canyon-technologies","US$620M·파이프라인 US$3.5B."),
 ("W22","Via Satellite: MDA to Acquire Blue Canyon","업계 매체","2026-06-22","https://www.satellitetoday.com/manufacturing/2026/06/22/mda-space-to-acquire-blue-canyon-from-raytheon-to-reach-us-defense-market/","400명+·기밀 사업 경로."),
 ("W23","Yahoo Finance: MDA Bets €567M on CLS","금융 매체","2026-07","https://finance.yahoo.com/technology/ai/articles/mda-space-bets-567m-cls-060157230.html","CLS 매출·유지율."),
 ("W24","SpaceQ: MDA issues $600M senior notes","업계 매체","2026-08","https://spaceq.ca/mda-space-issues-600-million-in-senior-notes-to-finance-u-s-expansion/","6.50%·2033. 1차 릴리스 미확인."),
 ("W25","Wikipedia: Initial public offering of SpaceX","백과","2026","https://en.wikipedia.org/wiki/Initial_public_offering_of_SpaceX","단일 출처 주의. 상장 후 주가 서술이 다른 출처와 충돌."),
 ("W26","Quantral: SpaceX (SPCX) IPO","금융 블로그","2026","https://quantral.com/blog/spacex-ipo","공모가·첫날 종가·락업 일정. 원공시 미확인."),
 ("W27","Yahoo Finance: Rocket Lab buys Iridium in $8B deal","금융 매체","2026-06-29","https://finance.yahoo.com/technology/articles/rocket-lab-buy-satellite-communications-111416348.html","EV 약 $8.0B·2027 중반 종결."),
 ("W28","Kyiv Independent(Reuters 인용): Musk ordered Starlink shutdown","일간지","2025-07-25","https://kyivindependent.com/musk-ordered-starlink-shutdown-over-kherson-during-ukraines-2022-counteroffensive-reuters-reports/","관계자 3인 증언. 머스크 부인."),
 ("W29","Tom's Hardware: Ontario cancels Starlink deal","IT 매체","2025-03","https://www.tomshardware.com/tech-industry/ontario-cancels-starlink-deal-over-us-tariffs-italy-may-follow-due-to-us-pullback-from-europe","C$100M 계약 취소·광물 협상 보도 언급."),
 ("W30","Yahoo News: Italy suspends Starlink negotiations","일간지","2025","https://www.yahoo.com/news/italy-suspends-starlink-purchase-negotiations-050003550.html","2025년 시점. 이후 변동 확인 필요."),
 ("W31","캐나다 총리실: Telesat Lightspeed 자금 지원","정부 발표","2024-09-13","https://www.pm.gc.ca/en/news/news-releases/2024/09/13/high-speed-internet-across-country-canadas-largest-space-program","연방 2.14B·퀘벡 400M 대출."),
 ("W32","DefenseScoop: Space Force awards SpaceX SDN backbone","업계 매체","2026-05-27","https://defensescoop.com/2026/05/27/space-force-awards-spacex-contract-backbone-satcom-network/","$2.29B OTA. 브랜치 노트 경유."),
 ("W33","Breaking Defense: SDA Transport Layer → Space Data Network","업계 매체","2026-04","https://breakingdefense.com/2026/04/space-force-shifts-from-sda-transport-layer-to-new-space-data-network-backbone-for-orbital-relay/","Tranche 3 Transport 미배정. 브랜치 노트 경유."),
 ("W34","Aerospacelab: IRIS² 264기 €2.4B","회사 발표(타사)","2026-09-10","https://www.aerospacelab.com/blog/press-releases-1/aerospacelab-awarded-2-4-billion-landmark-contract-to-build-264-leo-satellites-for-iris2-38","브랜치 노트 경유."),
 ("W35","Euronews: Europe's answer to Starlink","일간지","2026-10-16","https://www.euronews.com/2026/10/16/europes-answer-to-starlink-who-is-building-iris-and-what-is-germanys-role","SATCOMBw 4·OHB–Rheinmetall. 브랜치 노트 경유."),
 ("W36","SatNews: South Korea ratifies K-LEO plan","업계 매체","2026-07-06","https://satnews.com/2026/07/06/south-korea-formally-ratifies-2035-k-starlink-low-earth-orbit-constellation-plan/","128~512기·제조 발주 없음. 브랜치 노트 경유."),
 ("W37","Thinking in Multiples(Substack): Research Report MDA Space","독립 리서치","2026","https://thinkinginmultiples.substack.com/p/research-report-mda-space","잔고 73% 수치의 출처. 기준 시점이 오래됨."),
 ("W38","Kratos Constellations: MDA 2 sats per day plant","업계 매체","2025","https://www.kratosspace.com/constellations/articles/mda-space-2-sats-per-day-plant-opens-by-december-but-telesat-globalstar-production-to-start-slowly","생산 램프는 느리게 시작."),
 ("W39","Space Intel Report: MDA factory for up to 400 sats/year","업계 매체","2026-05","https://www.spaceintelreport.com/mda-space-factory-for-up-to-400-software-defined-sats-year-is-open-pursuing-multiple-commercial-government-constellations/","제목만 확인(유료)."),
 ("W40","Morningstar DBRS: MDA Space rating","신용평가","2025-12","https://dbrs.morningstar.com/research/468942/morningstar-dbrs-assigns-issuer-rating-of-bb-high-to-mda-space-ltd-and-provisional-credit-rating-of-p-bb-to-its-senior-unsecured-notes-stable-trends","발행자 BB(high). 2025-12 사채 기준이라 인수 발표 전."),
 ("W41","MarketBeat·StockAnalysis: MDA 주가·목표가","시세·집계","2026-11-10~13","https://www.marketbeat.com/instant-alerts/analyst-mda-space-nyse-mda-stock-price-target-cut-by-jpmorgan-chase-co-2026-11-10/","집계 사이트. 시세는 직접 재확인."),
 ("W42","nai500·Yahoo: MDA 주가 하락 기사","금융 매체","2026-08~11","https://nai500.com/blog/2026/08/mda-space-plunges-29-despite-4-billion-backlog-whats-spooking-investors/","52주 고점 C$67.90(날짜 없음)."),
 ("W43","Motley Fool·24/7 Wall St.: 우주주 배수","금융 매체","2026-11","https://www.fool.com/investing/2026/11/13/heres-what-1000-in-each-of-these-x-space-stocks-co/","기사마다 주가 시점이 달라 배수는 참고용."),
 ("W44","York Space Systems 1Q 2026 실적","회사 발표(타사)","2026-05-14","https://www.businesswire.com/news/home/20260514013419/en/York-Space-Systems-Reports-First-Quarter-2026-Results","잔고 $642M·매출 가이던스 $545~595M. 브랜치 노트 경유."),
 ("W45","SatNews: Apex $500M at $4B","업계 매체","2026-10-24","https://satnews.com/2026/10/24/satellite-bus-maker-apex-in-talks-to-raise-500m-at-4b-valuation/","협상 중 보도."),
 ("W46","Flight Plan: Airbus·Leonardo·Thales 우주사업 통합","업계 매체","2025-10-24","https://flightplan.forecastinternational.com/2025/10/24/airbus-leonardo-thales-join-forces-to-reshape-european-space-landscape/","MOU 단계."),
 ("W47","Via Satellite: MDA supply chain delays on Globalstar and CHORUS","업계 매체","2025-11-14","https://www.satellitetoday.com/finance/2025/11/14/mda-space-reports-supply-chain-delays-on-globalstar-and-chorus-posts-45-revenue-increase-in-q3","지체상금 권리·Rocket Lab 버스(Space Intel Report 제목)."),
 ("W48","Motley Fool Canada: MDA vs. SpaceX","금융 매체","2026-08-11","https://www.fool.ca/2026/08/11/mda-vs-spacex-how-a-canadian-space-stock-can-still-win/","대화 기록 출처. 논평."),
 ("W49","SpaceQ: MDA acquires Blue Canyon","업계 매체","2026-06","https://spaceq.ca/mda-space-acquires-blue-canyon-technologies-in-u-s-space-defence-push/","CEO의 '긴급 공급자' 표현. 브랜치 노트 경유."),
 ("W50","SatNews: factory rates and component waits","업계 매체","2026-09-27","https://satnews.com/2026/09/27/satellite-primes-quoted-factory-rates-of-up-to-two-a-day-in-paris-the-component-tier-below-them-described-18-month-waits/","부품 대기 18개월. 브랜치 노트 경유."),
 ("W51","Black Spade Acquisition III Form F-4/A","타사 공시","2026","https://www.sec.gov/Archives/edgar/data/0002087087/000121390026116443/ea0303223-04.htm","SpaceX의 EchoStar 잔여 주파수 $19.6B 인수 언급. 검색 요약으로만 확인."),
 ("W52","Via Satellite: Telesat's Lightspeed slips to 2028","업계 매체","2026-03-17","https://www.satellitetoday.com/finance/2026/03/17/telesats-lightspeed-service-launch-slips-to-2028/","ASIC 지연 사유."),
 ("W53","SatNews: MDA delivers record $1.6B, $40B pipeline","업계 매체","2026-03-04","https://satnews.com/2026/03/04/mda-space-delivers-record-1-6-billion-revenue-in-2025-unveils-40-billion-opportunity-pipeline/","49North·DIS C$180B 언급. MDA 릴리스에 없는 수치 포함."),
 ("N01","이 저장소: research/mda-space-deep-dive.md","리서치 노트","2026-11-13","research/mda-space-deep-dive.md","1차 정리본. 출처 링크 전체 수록."),
 ("N02","브랜치 claude/elegant-cerf-tmeeqn: study/MDA","리서치 노트","2026-11-13","study/MDA/study_v2/verification/M1_M2_sovereign_demand.md · M3_M4_company.md · data/quarterly.csv","정부 발주 표·회사 검증·분기 시계열. 계산값(등급 3)이 많으니 원 계약으로 재검증."),
 ("N03","브랜치 claude/hopeful-galileo-se2znn: study/SPACE","리서치 노트","2026-11-13","study/SPACE/MDA_투자포인트_v2.md · MDA_BKSY_칠판개요.md","투자포인트 v2·IR 자료 페이지 인용. '내 추정'은 공시값 아님."),
 ("N04","브랜치 claude/laughing-ride-qdcywi: space/companies/mda-space","리서치 노트","2026-11-13","space/companies/mda-space/overview.md · tracking.md · ir_notes.jsonl","3Q26 콜 정리·추적 레지스터."),
 ("N05","브랜치 claude/ecstatic-clarke-fbv4xc: 우주산업 밸류체인 정리","리서치 노트","2026-11-12","claude/01_우주산업_밸류체인_정리_2026-11-12.md","부품별 업체 지도. SIA 2025 수치."),
 ("N06","대화 기록: MDA Q&A 6건 + SpaceX 의존 설명","대화 기록","2026-11-13~15","이 세션에 붙여 넣은 문답","MDA vs SpaceX·국가별 프라임·인수 레버리지·프라임 계약·해자·한국 구조. 일부는 검색 없이 기억으로 답한 것."),
 ("N07","SMIC Guide · Coverage List","팀 자료","2026.09 기준","reference/SMIC_Guide.md · reference/SMIC_Coverage_List.md","보고서 구성·양식·스크리닝 기준·과거 커버리지."),
]

# ---------------------------------------------------------------- layers
# (1층, 2층 조사 영역, 질문, 보고서 배치, rows)
# row = (3층 세부 주제, 근거 구분, 재료, 의미·적용 범위, 출처)
L = []

L.append(("01 산업의 변화","두 스택과 상업의 항복","상업 위성 수요는 왜 SpaceX·Amazon으로 넘어가고 있는가?","산업분석",[
 ("두 스택","보도","SpaceX(Falcon·Starlink 1만 기 이상·Starshield)와 Amazon(New Glenn·Leo 3,236기 계획·Globalstar 주파수)이 발사·위성·서비스를 모두 가진 수직계열 스택을 만들고 있다.","나머지 운영사는 '세입자'가 된다는 업계 프레임이다. 논평 기사이므로 사실이 아닌 시각으로 인용한다.","W09"),
 ("Starlink 규모","보도","Starlink 가입자는 2026-02에 1,000만을 넘었고 궤도 위성은 1만 기 이상이다.","상업 광대역에서 규모 격차가 벌어진 근거.","W08"),
 ("SpaceX 상장","보도","SpaceX는 2026-06-12 나스닥(SPCX)에 공모가 $135, 시가총액 약 $1.77T로 상장했다.","자본 조달력 격차가 더 벌어졌다. 조달액과 상장 후 주가는 출처마다 다르다(층위 17).","W25; W26"),
 ("EchoStar 해지","확인 사실","EchoStar는 2025-09 AWS-4·H블록 주파수를 SpaceX에 약 $17B에 팔고 MDA와의 US$1.3B(100기 이상) 계약을 편의 해지했다. 계약 발표(8/1) 약 5주 만이다.","고객이 경쟁을 포기하면 MDA 주문이 사라지는 구조의 실제 사례.","F10; W06"),
 ("EchoStar 후속","추가 확인","SpaceX가 EchoStar의 남은 AWS-4·H블록 주파수도 약 $19.6B에 인수하기로 했다는 타사 공시 인용이 있다.","주파수가 SpaceX로 모이는 흐름. 원공시를 확인하고 쓴다.","W51"),
 ("Globalstar 인수","확인 사실","Amazon은 2026-04 Globalstar 인수(약 $11.6B)에 합의했고 FCC가 2026-10-27 승인했다. 종결은 2027년 예정이다. Amazon은 MDA가 제작 중인 위성을 운영하겠다고 밝혔다.","현재 계약은 유지된다. 후속 발주는 불확실하다.","W04; W05"),
 ("Amazon 자체 D2D","회사 발표","Amazon은 2028년부터 자체 차세대 D2D 위성 시스템을 배치할 계획이다.","Globalstar 후속 물량이 MDA로 올 가능성을 낮춘다.","W04"),
 ("Rocket Lab–Iridium","확인 사실","Rocket Lab은 2026-06-29 Iridium을 기업가치 약 $8.0B에 인수하기로 했다(2027년 중반 종결 예정).","제조·발사 업체가 운영사를 사는 세 번째 수직계열화 사례. MDA의 부품 고객이자 경쟁사가 운영사까지 갖게 된다.","W27"),
 ("운영사 통합","보도","SES–Intelsat, Viasat–Inmarsat(2023), Eutelsat–OneWeb(2023)이 합쳤다. SES 임원은 옛 생태계가 '사라졌거나 사라지는 중'이라고 말했다.","독립 상업 운영사가 줄면 MDA 완성 위성의 상업 고객 풀도 준다.","W08"),
 ("Telesat 본업","보도","Telesat의 3Q26 GEO 매출은 전년 대비 −20%, 조정 EBITDA는 −74%였다.","정지궤도 사업이 잠식되는 숫자.","W01"),
 ("운영사의 대응","보도","Telesat·Hispasat·Viasat·SES는 Starlink·Leo와 정면 경쟁하지 않고 정부·기업 고객 유지에 집중한다고 밝혔다.","살아남는 운영사의 수요가 정부 쪽으로 기운다. 층위 02로 이어진다.","W08"),
 ("MDA에 주는 의미","리서치 해석","이 전제가 강할수록 MDA의 현재 매출 기반(2025년 상업 72%)에는 악재다.","투자포인트는 '상업 성장'이 아니라 '돈 내는 주체의 교체'로 세워야 한다.","N01; N03"),
]))

L.append(("02 산업의 변화","소버린 수요: 통제권","정부는 왜 Starlink를 쓰지 않고 자기 위성망을 사는가?","산업분석",[
 ("의존의 두 층","기초 개념","SpaceX 의존에는 서비스 의존(Starlink 망을 빌려 씀)과 발사 의존(자기 위성을 Falcon 9에 실음)이 있다.","소버린 수요가 벗어나려는 것은 서비스 의존이다. 발사 의존은 남는다.","N06"),
 ("보안이 아닌 통제권","리서치 해석","문제는 도청이 아니라 통제권이다. 어디서, 누구에게, 어떤 용도로 서비스할지를 SpaceX가 정한다.","암호화는 사용자가 얹을 수 있어서 '보안'으로 쓰면 반박당한다. '통제권'으로 쓴다.","N06"),
 ("헤르손 사례","보도","Reuters(2025-07)는 머스크가 2022년 가을 우크라이나의 헤르손 반격 중 Starlink 차단을 지시했다는 관계자 3인의 증언을 보도했다. 머스크는 부인했다.","통제권 리스크의 대표 사례. '보도'로 인용한다.","W28"),
 ("광물 협상 보도","보도","미국이 우크라이나와의 광물 협정 압박 수단으로 Starlink 차단을 거론했다는 보도가 2025년에 있었다. 머스크는 부인했다.","미국 정부 영향권에 있다는 리스크.","W29"),
 ("온타리오 취소","확인 사실","온타리오주는 2025년 미국 관세에 대응해 Starlink와의 C$100M 계약을 취소했다.","캐나다 안의 실제 사례. 산업정책·정치 리스크.","W29"),
 ("이탈리아","보도","이탈리아가 검토하던 약 €1.5B 규모 Starlink 계약은 2025년에 중단됐다. 입찰이나 예산은 아직 없다.","수요 근거이면서 '계획일 뿐'이라는 반론 근거이기도 하다.","W30; N02"),
 ("Telesat CEO 발언","경영진 설명","Telesat CEO(2026-10-29)는 우크라이나에서의 Starlink·Starshield 차질이 '여러 정부를 움직였다'고 했고, 향후 1년 내 의미 있는 계약 체결에 낙관적이라고 했다. 캐나다 밖 고객명이나 금액은 없었다.","수요 증언. 숫자가 없다는 점을 같이 적는다.","W01"),
 ("Iridium CEO 발언","인터뷰 발언","Iridium CEO는 소버린 수요가 '일시적 유행이 아니다'라고 했다. 미국 정책과 미국 운영사 의존의 불확실성을 동인으로 들었다.","수요의 지속성 증언.","W08"),
 ("군 사양","기초 개념","군은 전용 주파수(UHF·X밴드), 항재밍, 보호 파형, 자국 지상국과 자국 인력의 운영을 요구한다.","상용 요금제로 대체할 수 없는 영역. ESCP-P 2단계가 UHF·X밴드인 이유.","N06; G01"),
 ("수요의 범위","리서치 해석","정부도 농촌 인터넷 같은 비핵심 용도는 Starlink를 계속 쓴다. 소버린 수요는 끊기면 안 되는 군·정부망에 한정된다.","시장 규모를 넘겨 잡지 않는다.","N06"),
 ("반례: 미국","보도","미국은 2026-05 Space Data Network 백본을 SpaceX에 $2.29B로 발주했다. SDA Transport Tranche 3에는 예산이 배정되지 않았다.","가장 큰 정부 구매자는 반대로 갔다. '소버린 = 비SpaceX'로 일반화하지 않는다.","W32; W33; N02"),
 ("반례: 영국·EU","보도","영국 국방부는 Starshield 사용을 확인했다(2026-09). EU 집행위원은 IRIS² 전까지 Starlink를 버릴 수 없다고 말했다(2026-01).","탈피는 2029~2032년까지 걸리는 과정이다.","N02"),
 ("발사 의존은 남는다","확인 사실","Lightspeed와 CHORUS는 모두 Falcon 9로 발사한다. 3Q26 콜에서 Falcon 9 퇴역 우려 질문에 CEO는 '지켜볼 지점'이라고 답했다.","소버린 군집도 발사는 SpaceX에 묶여 있다.","T01; F04"),
 ("핵심 문장","리서치 해석","정부가 사는 것은 통신 용량이 아니라 통제권이고, 통제권은 SpaceX가 가격을 낮춰도 팔 수 없다.","'구조적 수요'를 논증하는 근거 문장.","N06"),
]))

L.append(("03 산업 구조","시장 규모와 열린 몫","SpaceX·Amazon 밖 시장은 얼마이고, 그중 MDA가 닿는 몫은 얼마인가?","산업분석",[
 ("전체 물량","외부 추정","Novaspace 28판(2025-10)은 2025~2034년 발사 위성을 43,000기 이상, 제조와 발사를 합한 가치를 약 $665B로 본다.","TAM의 출발점. 원보고서는 유료라 언론 보도로만 확인했다.","W11; W10"),
 ("메가군집 비중","외부 추정","5개 메가군집(Starlink·Starshield·Kuiper·Qianfan·Guowang)이 위성 수의 66%를 차지하지만 가치로는 11%다.","대수로는 캡티브가 압도하고 가치로는 나머지가 크다.","W10"),
 ("국방 비중","외부 추정","국방은 위성 수의 9%지만 시장 가치의 48%다.","가치의 절반이 국방이라는 정량 근거.","W10"),
 ("열린 시장 7%","외부 추정","제조 시장 가치 중 어느 제조사에나 열린 몫은 7%뿐이다. 약 70%는 '자국 캡티브'이고 나머지는 수직계열 군집 내부다.","'접근 가능 20~30%'를 수주 가능 시장으로 읽으면 안 된다는 가장 강한 반증.","W10; N02"),
 ("MDA의 주장","회사 발표","MDA IR 자료는 2025~34년 4~5만 기 중 20~30%가 접근 가능하고 현재 파이프라인에 5% 이상이 있다고 한다.","대수 기준 산술은 맞다(메가군집 밖이 34%). 열린 몫과는 다른 개념이다.","F06; N02"),
 ("정부 우주예산","외부 추정","2025년 전 세계 정부 우주예산은 $137.4B이고 국방이 54%($73.5B), 민간이 $63.7B다.","수요 주체의 규모. AIF가 Novaspace를 인용한 수치.","F04"),
 ("우주 국방 전망","외부 추정","우주 국방 예산은 $74B에서 2028년 $121B로 늘 것으로 전망되고, 55개국 이상이 우주 국방 예산을 갖고 있다.","성장 방향. 전망치 인용은 최소로 한다(SMIC 가이드).","W12"),
 ("실제 발주 추이","직접 계산","SpaceX·Amazon·중국 밖 정부 통신위성 발주는 2020년 약 $1B, 2023~24년 연 $3~4B, 2026년 누계 $5~7B다. 지명됐지만 아직 발주되지 않은 사업이 $12~15B 더 있다.","전망치 대신 실제 발주 합계로 성장을 증명한다. 브랜치 노트의 계산이므로 원 계약을 재검증하고 쓴다.","N02"),
 ("구성 변화","리서치 해석","2020~24년은 미국 SDA Transport가 대부분이었다. 2025~26년에 그 예산은 0이 됐고 유럽(IRIS²)·캐나다·일본이 채웠다.","성장의 주체가 바뀌었다. 미국 통신 라인은 줄었다.","N02"),
 ("정부 통신위성 수","직접 계산","식별된 정부 통신위성(2025~34)은 2,000~2,600기, 미발표분을 감안하면 2,000~4,000기다. MDA가 프라임인 것은 300~400기이고 전부 캐나다다.","SOM 추정의 출발점.","N02"),
 ("대당 가격","직접 계산","소버린 LEO 통신위성은 대당 $10~25M이다. Lightspeed 약 C$13M, ESCP-P 추가분 약 C$17.6M, IRIS² L2 플랫폼 €9.1M, SDA Transport $10~29M.","P 추정의 근거. MDA는 서방 범위의 하단이다.","N02"),
 ("연간 시장","직접 계산","2,000~4,000기 × $10~25M = 10년간 $20~100B, 연 $2~10B. 실제 발주 연 $3~7B와 맞는다.","TAM 교차 검증.","N02"),
 ("제조 단계의 크기","외부 추정","2025년 위성 제조 매출은 $20.4B로 우주산업 전체의 4.8%다(SIA).","밸류체인에서 제조 단계가 차지하는 크기.","N05"),
 ("계획과 계약","리서치 해석","독일 €35B, K-LEO, 이탈리아는 공약이나 계획이지 계약이 아니다. 독일이 계획한 1,200기 중 통신은 약 200기다.","큰 숫자를 수요로 인용할 때는 단계를 표시한다.","N02; W14; W35"),
]))

L.append(("04 산업 구조","밸류체인과 국가별 프라임","위성은 누가 만들고, MDA는 그 안 어디에 있는가?","산업분석",[
 ("두 층 구조","기초 개념","위성은 프라임(본체 제작·탑재체 통합·시험·납품 책임)과 하위 시스템 공급사(안테나·디지털 탑재체·전자장비) 두 층으로 만들어진다.","MDA는 아래층 출신이고 AURORA로 위층에 올라가는 중이다.","N06"),
 ("캡티브","기초 개념","SpaceX·Amazon·중국은 위성을 직접 만든다. 가장 큰 수요처가 외부에 발주하지 않는다.","MDA 시장의 상한을 정한다. 직접 경쟁자라기보다 시장을 없애는 쪽이다.","N06"),
 ("유럽 프라임","확인 사실","IRIS²에서 L2 플랫폼 264기는 Aerospacelab(€2.4B), L1 플랫폼 66기는 Airbus, LEO 탑재체 330기는 Thales Alenia Space, MEO 18기는 OHB가 맡았다.","유럽 사업은 전부 유럽 프라임이다.","W13; W34; N02"),
 ("미국 프라임","확인 사실","SDA 전 트랜치는 Lockheed, Northrop, L3Harris, York, Rocket Lab, Sierra Space, Tyvak, SpaceX가 가져갔다.","미국 사업도 전부 자국 프라임이다.","N02"),
 ("일본","확인 사실","차세대 방위통신위성(¥123.5B)은 Mitsubishi Electric이 프라임이고, MDA가 디지털 탑재체와 안테나를, Lockheed가 항재밍 탑재체를 댄다.","자국 프라임 아래 하위 시스템으로 들어가는 전형.","F12; N02"),
 ("한국","기초 개념","우주항공청은 발주와 관리를 하고, KARI·ADD가 설계를 주도하며, KAI·쎄트렉아이·한화시스템이 제작에서 주관으로 올라가는 중이다.","국가 연구소가 설계를 쥔 나라에는 외국 프라임의 자리가 없다. 기억으로 적은 내용이라 다시 확인한다.","N06"),
 ("캐나다","리서치 해석","캐나다에는 KARI나 JPL 같은 국가 설계 조직이 사실상 없고 그 역할을 MDA가 맡는다.","국내 해자가 강한 이유이자 이 모델이 수출되지 않는 이유.","N06"),
 ("프라임이 없는 나라","확인 사실","자국 프라임이 없는 나라는 외국 프라임을 쓴다. UAE(Airbus, Al Yah 4/5 $1.1B), 폴란드(Airbus·Thales·Radmor), 대만(CesiumAstro 탑재체).","MDA 해외 프라임의 이론적 경로. 아직 사례는 없다.","N02"),
 ("외국 프라임의 실패","확인 사실","호주는 Lockheed를 선정했던 JP9102(A$7B)를 2024-11에 취소했다.","외국 프라임이 주도하는 소버린 사업은 버티기 어렵다.","N02"),
 ("유럽 3사 통합","보도","Airbus(35%)·Thales(32.5%)·Leonardo(32.5%)가 우주사업 통합 MOU를 맺었다(2025-10). 합산 매출 약 €6.5B, 2027년 출범 목표이고 EU 승인을 기다린다. OHB는 반대한다.","MDA에는 큰 고객이 하나로 뭉치는 일(협상력 하락)이자 완성 위성 경쟁자가 커지는 일이다.","W46; N02"),
 ("신흥 버스 업체","보도","York(2026-01 상장), Apex(약 $4B 밸류로 조달 협상), K2($6.8B), Rocket Lab이 표준 버스를 대량생산한다.","프라임 층의 미국 경쟁이 세졌다. 이들은 버스를 팔고 탑재체는 밖에서 산다.","W45; N02"),
 ("경쟁사가 곧 고객","확인 사실","AIF의 고객 목록에 Airbus, Thales Alenia, Lockheed, Northrop, Boeing, L3Harris, OHB, York, Rocket Lab, Lanteris가 있고, 같은 문서의 경쟁사 목록과 겹친다.","부품 매출은 프라임 경쟁에서 누가 이기든 발생한다.","F04"),
 ("부품 병목","보도","태양전지 등 부품사는 가동률 100%에 대기 18개월이라고 말한다.","모든 제조사의 명목 생산능력을 제한한다.","W50"),
 ("MDA가 없는 곳","확인 사실","MDA는 발사를 하지 않고(Maritime Launch Services에 C$10M 지분만 보유) 통신위성을 운영하지도 않는다.","밸류체인의 빈칸.","F03"),
]))

L.append(("05 회사의 사업 구조","사업부와 수익 모델","MDA는 무엇을 팔고 누구에게서 돈을 받는가?","기업분석",[
 ("3개 사업부","확인 사실","FY2025 매출은 Satellite Systems 1,109.5(68%), Robotics & Space Operations 309.3(19%), Geointelligence 214.4(13%)다.","2024년 55/26/19에서 위성 쏠림이 심해졌다.","F02; F04"),
 ("고객 구성","회사 발표","2025년 매출은 상업 72%, 정부 28%다. 지역은 캐나다 63%, 미국 30%, EU 5%다(IR 자료 p4).","지금은 상업 의존 회사다. 다만 '상업'에 정부 자금으로 짓는 Lightspeed가 들어 있다.","F06; N03"),
 ("2026년 지역 구성","확인 사실","9M26 매출은 캐나다 1,018(70%), 미국 357(24%), 유럽 59, 아시아·중동 24다.","사실상 캐나다 재원으로 움직인다. 미국 매출은 Globalstar 소진으로 줄고 있다.","N02"),
 ("고객 집중","확인 사실","상위 10개 고객이 FY2025 매출의 87.2%다. 주요 고객으로 캐나다 정부·Telesat·Globalstar가 명시돼 있고 개별 비중은 공시하지 않는다.","고객별 비중은 직접 추정해야 한다.","F04"),
 ("프라임 역할","확인 사실","Telesat Lightspeed와 Globalstar 2건에서 위성 전체를 납품하는 프라임이다.","매출의 큰 덩어리. 수주가 몇 건에 몰린다.","F04"),
 ("머천트 역할","확인 사실","OneWeb(Airbus 경유), IRIS² L1(Thales 경유), SDA T0~T2(L3Harris·Lockheed·York 경유), MEO Epoch 2(BAE 경유), 일본(Mitsubishi 경유)에 안테나와 탑재체를 납품한다.","프라임이 누구든 비Starlink 군집이 늘면 같이 는다. 금액은 대부분 공개되지 않았다.","F14; W15; F13; F12; N02"),
 ("AURORA","회사 발표","AURORA는 소프트웨어 정의 디지털 위성 제품군이다. 디지털 빔포밍, 직접방사 위상배열 안테나, 자체 ASIC을 쓰고 LEO·MEO와 광대역·D2D에 적용된다.","용역에서 제품으로 가는 전환. 현지에 조립 라인만 세우면 된다는 것이 회사 주장이다.","F03; N04"),
 ("군용 제품","회사 발표","2026-04에 우주자산 방호 플랫폼 MIDNIGHT를, 2026-09에 항재밍·GPS 기만 저항·보호 파형을 넣은 AURORA BLACK을 내놨다.","국방 고객용 라인. 수주 실적은 아직 없다.","F01; T01"),
 ("SatixFy","확인 사실","2025-07-02 SatixFy 인수를 마쳤고 총 대가는 C$448.3M이다. 우주급 빔포밍·모뎀 ASIC을 내재화했다.","수직통합. 다만 Lightspeed 지연 사유로 ASIC이 거론됐다(층위 09).","F03; F04"),
 ("공장","회사 발표","Sainte-Anne-de-Bellevue에 185,000 sq ft를 증설해 2026-05 준공식을 열었다. 설계 용량은 '하루 최대 2기, 연 최대 400기'다.","명목치다. 2026년 초 실제 속도는 주 1기 수준이고 2027년 '수백 기'를 기대한다.","F15; W38; W39; N02"),
 ("Robotics","확인 사실","Canadarm3는 잠재 총매출 약 C$1.8B(15년 운영 포함)이고 Phase B 269(2022), Phase C/D 1,000(2024)이다. 계약 상대는 CSA다. ISS 로봇 운영은 C$250M(2025~2030)이다.","정부가 주는 연금형 사업. 분기 80~100 수준.","F03; F04"),
 ("Geointelligence","확인 사실","RADARSAT-2 상업 배급, 지상국 70개 이상(25개국), CHORUS(C밴드+X밴드, 2026년 말 발사), RADARSAT+ C$1.012B(15년), RCM 보충위성 C$688M(2026-06).","유일한 반복 매출. CLS로 키운다.","F04; F16; W20"),
 ("49North","회사 발표","2026-02에 출범했다. 우주 밖 국방(C4ISR, 해군 ISTAR 무인기, RPAS)을 맡는다.","캐나다 국방 조달을 겨냥한 조직.","F03; W53"),
 ("인력·시설","확인 사실","직원 4,000명 이상(엔지니어 약 2,000명), 노조 조직률 약 55%, 시설 16곳, 공급사 750곳 이상. 본사는 온타리오주 브램턴이다.","기초 정보.","F04"),
]))

L.append(("06 회사의 사업 구조","프라임 계약과 매출 인식","프라임 계약은 무엇이고, 계약하면 매출과 현금은 언제 생기는가?","기업분석 · 매출추정",[
 ("프라임 계약","기초 개념","프라임 계약은 발주처에 위성 시스템 전체를 끝까지 책임지고 넘기는 계약이다. 설계, 제작, 하청 관리, 지상 시스템, 일정과 원가를 책임진다.","하청 매출까지 프라임 매출로 잡히고 위험도 전부 진다.","N06; G01"),
 ("CEO의 정의","경영진 설명","'As prime, we own the program, from design all the way through assembly, integration, test, and delivery.'","인용할 수 있는 문장.","T01; N04"),
 ("고정가","확인 사실","AIF는 '계약의 큰 부분이 확정 고정가'라고 적는다. 원가 초과는 MDA가 부담하고 지체상금 조항이 있다.","마진 리스크의 근원.","F04"),
 ("편의 해지","확인 사실","대부분의 계약은 고객이 언제든 중단하거나 편의 해지할 수 있다. 회수액은 '보장되지 않는다'.","EchoStar가 선례다. 잔고의 질에 붙는 단서.","F04"),
 ("선정과 계약","기초 개념","순서는 선정 → 정의(설계) 계약 → 본계약 → 잔고 편입이다. 잔고는 미행사 옵션과 IDIQ를 뺀다.","ESCP-P MEO, IRIS² ATP, K-LEO MOU는 아직 잔고가 아니다.","F01; N06"),
 ("ATP","확인 사실","IRIS² 안테나는 착수 승인(ATP) 단계이고 본계약은 '계약 확정 조건부'다. 4Q26에 잔고에 들어올 예정이다.","9/30 잔고 3,949에는 없다.","W15"),
 ("매출 인식 방식","추가 확인","장기 계약은 진행률(투입원가 기준)로 인식하는 것으로 보인다. 사업보고서 주석 원문은 확인하지 못했다.","매출추정의 기본 가정. 감사 재무제표 주석을 확인한다.","N06; F03"),
 ("간접 증거","경영진 설명","Lightspeed 시험위성이 2027-06 이후로 밀렸는데도 CEO는 재무 전망에 변화가 없다고 했다. CFO는 마일스톤이 잘게 쪼개져 있고 패스파인더 납품에 큰 대금이 걸려 있지 않다고 했다.","매출이 납품이나 발사가 아니라 작업량을 따라간다는 증거.","T01"),
 ("현금 사이클","확인 사실","수주 직후 선수금으로 OCF가 급증했고(2024년 812.7) 생산 구간에는 운전자본을 쓴다(9M26 OCF 73.7). 계약부채는 2025년 말 798.9에서 2026-09 601.7로 줄었다.","매출과 현금의 시차. FCF 가이던스가 중립~음수인 이유.","F01; F02"),
 ("인식 곡선","리서치 해석","계약 첫해 5~10%, 2~3년 차에 정점(연 30% 안팎), 마지막 해는 꼬리.","추정이고 계약마다 다르다. 프로그램별 인식 경로를 따로 그린다.","N06"),
 ("Lightspeed 사례","확인 사실","2023-08 계약 후 2023년부터 인식했고 2026~27년이 정점이다. 남은 약 1.4B는 2027~2029년에 인식한다.","인식 곡선의 기준 사례.","T01; N02"),
 ("추가분 사례","경영진 설명","Lightspeed 추가 27기(C$474M, 2026-08)는 2027·2028년 매출에 반영된다.","신규 수주의 효과는 약 1년 뒤에 나타난다.","N03; F09"),
 ("대형 계약 의존","직접 계산","2026년 9개월 수주 1,397 중 두 건(RCM 688, Lightspeed 474)이 1,162다. 이를 빼면 분기당 약 80이다.","대형 정부 계약이 없으면 잔고가 분기에 약 400씩 준다.","N02"),
 ("대당 단가","직접 계산","Lightspeed 2.4B ÷ 198기 = 약 C$12M, 추가분 474 ÷ 27기 = C$17.6M, Globalstar 차세대 1.1B ÷ 50기 이상 = 약 C$20M, EchoStar US$1.3B ÷ 100기 이상 = 약 US$13M.","매출추정의 P. 군용 사양이 단가를 올린다.","N01"),
]))

L.append(("07 시장 논리","\"2029년이면 공장이 빈다\"","시장은 MDA의 무엇을 걱정하고, 그 구멍은 얼마나 큰가?","기업분석(주가 분석)",[
 ("한 줄 주장","리서치 해석","시장은 MDA의 위성 공장이 2029년이면 빈다고 본다. 우리는 그 공장을 국가가 채운다고 본다.","보고서 한 줄 주장(브랜치 투자포인트 v2).","N03"),
 ("잔고 추이","확인 사실","잔고는 1Q25 4,838이 정점, 1Q26 3,693이 저점이고 이후 2Q26 4,003, 3Q26 3,949다.","저점은 3Q26이 아니라 1Q26이다.","N02; F01"),
 ("수주/매출","직접 계산","수주/매출은 2023년 3.13, 2024년 2.19, 2025년 0.73, 9M26 0.96이다.","2년 연속 1 미만.","N02"),
 ("잔고/매출","직접 계산","잔고/연매출은 2024년 말 4.1배, 2025년 말 2.5배, 2026-09 약 2.0배(가이던스 기준)다.","매출 가시성이 줄었다.","N01"),
 ("Lightspeed 소진","경영진 설명","Lightspeed 잔여 잔고 약 1.4B는 2027·2028·2029년에 인식된다.","2029년에 끝난다.","T01"),
 ("Globalstar 소진","경영진 설명","Globalstar 차세대 물량은 2027년부터 '점진 감소'한다. Globalstar 10-Q로 계산한 잔여는 약 US$245M, 교체위성 약 US$26M이다.","미국 매출이 준다.","T01; N02"),
 ("구멍 크기","직접 계산","위성 부문 매출은 연 약 1.35B(9M26 1,008 연환산)이고 대부분이 두 고객이다. 2029년까지 연 약 1B가 빠진다.","추정. 고객별 인식액을 확인해 확정한다.","N03"),
 ("매출 정체","확인 사실","분기 매출은 4Q25 499, 1Q26 464, 2Q26 499, 3Q26 498이다. 4Q26 내재 가이던스는 439~489로 전년 499보다 2~12% 적다.","기존 사업은 이미 멈췄다는 공격 재료.","N02; F01"),
 ("성장의 출처","외부 추정","2027년 컨센서스 매출 약 C$2.84~2.86B 중 약 0.7B가 BCT·CLS 인수분이다.","유기 성장에 대한 의심.","N02; N03"),
 ("목표가 하향","보도","3Q26에 가이던스를 올렸는데도 목표가는 내려갔다. JPMorgan $50→44, Jefferies $49→45.","시장이 2027년 이후를 본다는 증거.","W41"),
 ("구멍 메우기","직접 계산","연 1B 감소를 메우려면 2027~28년 신규 위성 수주가 누적 약 3B 필요하다(3~4년 인식 가정). 캐나다에서 이름이 붙은 건이 약 3B 이상이다.","승부처. 가설이고 검증 대상이다.","N03"),
 ("가이던스 이력","확인 사실","최초 가이던스 중간값 대비 최종치는 2024년 +8%, 2025년 +4%, 2026년 +7%였다.","경영진 가이던스는 3년 연속 보수적이었다.","N02"),
]))

L.append(("08 투자포인트 1","캐나다: 국가가 공장을 채운다","캐나다 정부 일감이 상업 롤오프를 메울 만큼 크고 확실한가?","투자포인트 1",[
 ("전략 파트너 지정","확인 사실","2025-12 캐나다 정부는 북극 군 통신 사업(ESCP-P)에 Telesat과 MDA를 경쟁 입찰 없이 전략 파트너로 지정했다.","캐나다에서 MDA는 지정되는 공급자다.","G01; N03"),
 ("국방산업전략","확인 사실","2026-02 국방산업전략은 우주를 주권 역량으로 지정했다. 향후 10년 국내 국방 조달은 C$180B로 인용된다.","정책 근거. 수치는 정부 원문으로 다시 확인한다.","G04; W53"),
 ("ESCP-P 1단계","확인 사실","2026-08-04 국방투자청은 Telesat에 군용 Ka밴드 서비스 약 C$2.3B를 발주했다. 옵션은 약 214와 218이다.","Lightspeed가 준소버린이 된 계기.","G01"),
 ("Lightspeed 확장","확인 사실","이 계약으로 MDA 수주는 198기에서 225기로 늘었다(+27기, C$474M). Telesat의 군집 계획은 156기에서 225기다.","MDA 증분은 27기다(층위 17 참조).","F09; G01"),
 ("ESCP-P 2단계","확인 사실","MEO UHF·X밴드 군집은 MDA가 엔드투엔드 프라임이고 Telesat이 하청이다. 협상 중이고 금액은 공개되지 않았다.","투자포인트 1의 핵심 촉매.","G01"),
 ("2단계 규모","직접 계산","프로그램 전체 C$5B 이상(IR 자료)에서 Telesat 몫 약 2.7B를 빼면 MDA 몫은 C$2B 이상이다.","추정. 정부 공고와 IR 문의로 확인한다.","N03; F06"),
 ("수주 시점","경영진 설명","CEO는 대형 국방 사업이 '수십억 달러대가 덩어리로' 오고 '수개월 내 움직임'을 기대한다고 했다. 정의 단계가 먼저이고 덩어리가 점점 커진다.","시점은 불확실하다. 날짜는 없었다.","T01"),
 ("RADARSAT","확인 사실","RADARSAT+ 이니셔티브는 C$1.012B(15년)다. RCM 보충위성 본계약 C$688M이 2026-06에 체결돼 2Q26 수주에 들어갔다.","이미 잔고에 들어온 캐나다 정부 일감.","F16; W19"),
 ("우주감시","확인 사실","국방부 Surveillance of Space 2용 지상 광학 관측소 3기를 수주했다. 감시위성 사업(DESSP)은 예산 C$1~5B로 보도됐고 일정은 확인되지 않았다.","추가 파이프라인.","T01; N02"),
 ("국방비 경로","확인 사실","캐나다는 2025-26 회계연도에 GDP 2%(C$65B 이상)를 달성했고 2035년 핵심 국방 3.5%를 약속했다. IR 자료는 C$63B → C$110B(2029) → C$155B(FY35-36)로 제시한다.","예산 총량은 는다.","G02; G03; F06"),
 ("약점: 우주 몫","보도","2026년 예산안에는 우주 항목 숫자가 거의 없다. 국방투자청에도 신규 자금이 없다.","국방비 증가분 중 우주 몫을 숫자로 증명하기 어렵다.","N03; G02"),
 ("Canadarm3","확인 사실","NASA가 2026-03-24 Gateway를 중단했지만 계약 상대가 CSA라 금액은 그대로다. CSA는 달 표면·LEO로 전용할 방침이고 달 기지 로봇 계획 과업을 유상 발주했다.","발표 당일 주가 −11%. 캐나다 정부가 일감을 유지시킨 사례.","W17; W18; T01"),
 ("국가 우주전략","경영진 설명","CEO는 캐나다가 '선도적 우주 중견국'이 될 수 있고 국가 우주전략이 그 방향으로 간다고 했다.","정책 방향에 대한 회사 발언.","T01"),
 ("투자포인트 1 결론","리서치 해석","캐나다에서 이름이 붙은 건(ESCP-P MEO 2B 이상, RADARSAT 계열)만 받아도 구멍의 대부분이 메워진다.","결론 문장. 2단계 규모 가정에 달려 있다.","N03"),
]))

L.append(("09 투자포인트 1","Telesat Lightspeed: 준소버린과 그 리스크","최대 계약은 누가 돈을 내고, 그 통로는 얼마나 튼튼한가?","투자포인트 1 · Issue & Risk",[
 ("계약","확인 사실","2023-08 프라임으로 선정됐다. 약 C$2.4B·198기(옵션 100기)였고, 확장 후 약 C$2.9B·225기(옵션 73기)다.","MDA 최대 계약.","F04; F06; N02"),
 ("정부 대출","확인 사실","연방 정부 C$2.14B(15년 대출, 워런트 10%)와 퀘벡 C$400M 대출이 2024-09 확정됐다. 차주는 Telesat LEO다.","상업 계약이지만 재원은 정부다.","W31"),
 ("총투자","보도","Lightspeed 총 capex는 약 US$5B로 계획됐다(US$6.5B로 쓴 보도도 있다). Telesat은 2026-09까지 C$3.1B를 투자했다.","총액은 출처마다 다르다. Telesat 공시로 확인한다.","W31; W01"),
 ("군 선급금","확인 사실","ESCP-P 계약으로 Telesat은 마일스톤 2.0B를 3Q26~4Q28에 받는다. 9M26에 선급금 510을 받았다.","MDA 수금의 재원.","N02"),
 ("조달 상태","경영진 설명","Telesat은 Lightspeed가 '전액 조달 완료'라고 밝혔다.","회사 주장.","N02"),
 ("일정 지연","보도","2026-10-29 Telesat은 패스파인더 2기 발사가 2026-12에서 2027-06 이후로 밀렸다고 밝혔다. SpaceNews는 프라임 MDA의 조립·소프트웨어 개발 문제로 썼다. 전 세계 서비스는 2Q28 말, 고위도(캐나다 군) 서비스는 1Q28 말이다.","MDA의 실행 문제로 지목됐다.","W02; W01"),
 ("ASIC","보도","2026-03 Telesat은 서비스 지연 사유로 온보드 프로세서용 ASIC 지연을 들었다. 공급자는 MDA가 인수한 SatixFy다.","수직통합의 그늘.","W52"),
 ("MDA의 답","경영진 설명","MDA는 재무 전망에 변화가 없고 일정은 Telesat 소관이라고 답했다. 원인은 밝히지 않았다.","매출 영향은 없다는 주장.","T01; W03"),
 ("GEO 부채","보도","Telesat의 GEO 부채 약 C$3.1B가 2026-12~2027-10에 만기가 온다(2026-12-06분이 약 US$1.71B). Telesat은 상환 재원이 부족하다고 인정했고 채권단과 협의 중이다.","최대 고객의 신용 사건이 임박했다.","W01; N02"),
 ("LEO와 GEO의 분리","추가 확인","LEO 법인이 GEO 부채의 보증인이 아니라는 점은 검색 요약으로만 확인했다. 채권단이 LEO 지분 담보를 요구하고 소송이 진행 중이라는 보도가 있다.","Telesat 20-F·6-K 주석 원문을 확인한다.","N02"),
 ("발사","보도","Telesat은 Falcon 9를 14회 예약했고 1회가 더 필요하다. 패스파인더는 다른 회사의 Falcon 9에 합승하고 이후 15기씩 쏜다.","발사 의존.","W01"),
 ("해석","리서치 해석","Lightspeed는 상업으로 시작했지만 정부 대출과 군 15년 계약으로 살아남은 준소버린 사업이다.","소버린 논리가 MDA 최대 계약에 이미 작동한다는 증거다. 동시에 그 통로(Telesat)가 약하다는 리스크다.","N01; N02"),
]))

L.append(("10 투자포인트 2","해외 소버린: 탑재체 머천트","캐나다 밖 정부 사업에서 MDA는 무엇을 얼마나 가져가는가?","투자포인트 2",[
 ("판정","리서치 해석","캐나다 밖에서 MDA는 정부 사업 프라임이 된 적이 없고 전부 하위 시스템 공급이다.","'각국의 탈스타링크 수요가 MDA의 세계 시장'이라는 가설은 약하다.","N02"),
 ("IRIS² 규모","확인 사실","2026-08-07 이행 합의로 IRIS²는 348기(LEO 330 + MEO 18), 약 €15.6B가 됐고 군사 Ka 계층 66기가 추가됐다. 첫 발사는 2029년, 완전 서비스는 2032년경이다.","유럽 최대 소버린 사업.","W13; N02"),
 ("IRIS²에서 MDA 몫","회사 발표","MDA는 Thales Alenia Space로부터 L1 66기용 AURORA 디지털 위상배열 안테나와 컨트롤러의 ATP를 받았다. C$100M 이상이다(2026-10-30).","유럽 진입점. LEO 330기 중 20%다. Thales 쪽 발표는 확인되지 않았다.","W15; N02"),
 ("IRIS²의 한계","경영진 설명","CEO는 프로그램 전체 수주는 기대하지 않으며 '지정학과 현지 조달 요소가 높다'고 했다.","현지화 장벽을 회사도 인정한다.","T01"),
 ("EU 조달 규칙","보도","비EU 공급사는 동등한 EU 기술이 없을 때만 집행위 승인 보증하에 허용된다는 법무법인 해설이 있다. 유럽 대안으로 SWISSto12가 거론된다. 같은 날 캐나다와 EU는 IRIS² 협력 예비 협의를 발표했다.","본계약 전환과 L2 264기 확장의 변수.","N02"),
 ("독일","보도","SATCOMBw 4단계는 €8~10B, 100~200기로 보도되고 OHB–Rheinmetall 합작이 입찰했다(Airbus가 생산 파트너). 결정은 2026/27년으로 예상된다. CEO는 캐나다–독일 잠수함 거래의 산업협력 기회로 언급했다.","미발주. MDA는 하위 시스템이 최선이다.","W35; T01"),
 ("미국 SDA","확인 사실","T0 Tracking(L3Harris), T1 Transport(Lockheed 42기의 안테나·제어전자, York의 Ka 안테나), T1 Tracking(L3Harris 14 flight set)에 납품했다. 금액은 한 번도 공개되지 않았다.","CEO 표현으로 미국 프라임의 '긴급 공급자' 역할.","N02; W49"),
 ("MEO Epoch 2","확인 사실","BAE Systems가 미 우주군 MEO 미사일 경보 위성(10기)의 안테나와 제어전자를 MDA에 맡겼다(2026-06-02). 2027년 완료 예정이다.","미사일 경보·추적은 예산이 늘고 있는 영역.","F13"),
 ("미국 통신 예산 축소","보도","SDA Transport Tranche 3는 예산이 없고 후속 백본은 SpaceX가 가져갔다.","MDA 안테나가 들어가던 통신 라인은 줄었다.","W33; W32"),
 ("일본","확인 사실","Mitsubishi Electric의 차세대 방위통신위성(GEO 1기)에 디지털 탑재체(영국)와 안테나·중계기(몬트리올)를 공급한다. 금액은 공개되지 않았다.","군집이 아니라 GEO 1기다. 브랜치 노트 추정은 C$50~150M.","F12; N02"),
 ("한국","확인 사실","2026-01-26 한화시스템과 K-LEO MOU를 맺었다. K-LEO 계획은 2026-07 비준됐고 128~512기, 4~13.2조 원, 2035년 목표다. 제조 발주는 없다.","MOU뿐이다. 한화가 수직계열화하면 MDA는 탑재체나 라이선스가 최선이다.","F11; W36"),
 ("OneWeb","확인 사실","Airbus로부터 Ka 가변 안테나 880개 이상과 Ku 안테나 440개를 재수주했다(2026-04). OneWeb 교체 위성 669기는 Airbus가 만든다.","프랑스·영국 정부가 주주인 상업 군집. 재발주의 증거.","F14; N02"),
 ("해외 정부 수주 규모","직접 계산","캐나다 밖 정부 사업 누적 수주는 약 C$0.2~0.5B로 추정된다. 공개된 금액은 100M 이상 한 건뿐이다.","잔고의 10% 미만. 투자포인트 2는 '덤'으로 쓴다.","N02"),
 ("왜 MDA 부품인가","리서치 해석","세 관할의 자국 프라임(Thales, Mitsubishi, 미국 프라임들)이 MDA의 안테나와 디지털 탑재체를 샀다. 하위 시스템은 프로그램 가치의 5~10%다.","진짜 차별점은 부품이다. 위성 1기당 MDA 납품 금액으로 추적한다.","N02"),
 ("수출 규제","경영진 설명","CEO는 캐나다 설계 제품이 대체로 ITAR 대상이 아니고 고객 요구에 따라 미국산 위주나 유럽산 위주로 구성할 수 있다고 했다.","여러 나라 프라임에 납품할 수 있는 이유. 독립 검증은 없다.","T01"),
]))

L.append(("11 투자포인트 2","인수로 현지화: BCT·CLS","두 인수는 무엇을 사는 것이고, '레버리지'라고 부를 수 있는가?","투자포인트 2",[
 ("BCT 조건","확인 사실","RTX(Raytheon)에서 Blue Canyon Technologies 100%를 US$620M(약 C$874M) 현금에 산다. 2026-06-19 발표, 2026년 말 종결 예상이다. HSR·CFIUS 승인이 조건이고 지연되면 US$10M, US$20M을 더 낸다.","미국 진입권.","F08; W21"),
 ("BCT 사업","회사 발표","덴버에 시설 2곳, 직원 400명 이상, 위성 85기 이상 발사 실적. 매출과 파이프라인의 75%가 국방 관련이다. 반작용휠·별추적기 같은 자세제어 부품과 소형위성 버스를 만든다.","버스와 소형위성이 약한 MDA를 보강한다.","N02; W22"),
 ("BCT 논리","경영진 설명","미국 프라임('MDA Space USA')으로 키우고 기밀 프로그램 입찰 자격을 유지한다. 파이프라인 US$3.5B가 추가되고 2027년 EPS가 늘어난다고 한다.","회사 주장. BCT 실적은 공개되지 않았다.","T01; W21"),
 ("외국 지배 차단","추가 확인","외국 기업이 미국 기밀 사업을 하는 회사를 사면 보통 외국 지배 차단 조치(별도 이사회 등)가 붙는다. 이번 인수에 적용되는지는 확인되지 않았다.","기밀 사업 시너지가 본사와 섞이기 어려울 수 있다. 일반론은 기억으로 적었다.","N06"),
 ("CLS 조건","확인 사실","CLS 지분 약 70%를 €567M 현금에 산다. CNES가 약 30%를 유지한다. 재융자가 안 되면 기존 부채 약 €198M을 갚아 줄 수 있다. 2026년 말~2027년 초 종결 예상.","'$920M' 표기는 C$ 환산이거나 부채 포함 기준으로 보인다.","F17; W23"),
 ("CLS 사업","회사 발표","2025년 매출 €203M, 2026년 예상 약 €286M, 상위 100개 고객 유지율 99%, 19개국 운영. EBITDA 마진은 18~20%로 제시됐다.","반복 매출을 두 배(전사의 30% 이상)로 늘린다는 주장의 근거.","W23; N02; T01"),
 ("자금 조달","확인 사실","NYSE 상장 US$30.50(2026-03), bought deal US$35.60 × 2,300만 주 = US$819M(2026-07, CLS용), 사채 C$600M·6.50%·2033(2026-08, BCT용).","2026년 조달액은 약 C$2.1B다.","F07; W24"),
 ("재무 레버리지","직접 계산","순현금 1,328에서 두 건 약 1,794를 내면 순차입 약 0.5B가 되고 2026E EBITDA의 약 1.3배다. 회사 목표는 1.5~2.5배다.","빚보다 희석(주식 수 약 +26%)이 본질이다.","N01; N02"),
 ("영업 레버리지","리서치 해석","2026년 프로포마 매출 약 C$700M 추가는 합산이지 레버리지가 아니다. 합친 마진이 단순 합을 넘는다는 증거는 아직 없다.","'레버리지'라고 쓰면 공격받는다.","N06"),
 ("멀티플 논리","리서치 해석","CLS의 반복 매출이 수주 공백을 메우면 '수주 장사'에서 '구독형 매출이 있는 회사'로 재평가될 수 있다.","가장 방어하기 쉬운 프레임.","N06"),
 ("CSG 지분","확인 사실","체코 방산그룹 CSG가 2026-10-13 지분 9.5%(1,536만 주)를 평균 C$42.69에 샀고 '장기 전략적 주주'라고 밝혔다. 유럽 내 제조·조립 공동 투자를 검토하지만 합의된 것은 없다.","유럽 현지화의 또 다른 경로. Schedule 13D 원문을 확인한다.","N02"),
 ("통합 부담","리서치 해석","1년 사이 3건(SatixFy 포함)이고 미국과 프랑스를 동시에 통합해야 한다. CNES가 30%를 갖고 있어 CLS 경영권도 완전하지 않다.","Issue & Risk로 이어진다.","N06"),
 ("한 줄","리서치 해석","두 인수는 재무 레버리지가 아니라 포트폴리오 재구성이다. BCT는 미국 진입권이고 CLS는 반복 매출이다.","보고서 문장.","N06"),
]))

L.append(("12 경쟁과 해자","설계 능력·피어·해자","MDA는 무엇을 잘하고, 그것은 해자인가?","기업분석(Why 동사)",[
 ("로봇","확인 사실","Canadarm, Canadarm2, Dextre, 우주왕복선 90회 이상 임무, Canadarm3. AIF는 경쟁사로 Airbus, GITAI, Motiv, Redwire, Lanteris를 든다.","세계 최정상이다. 다만 부문 매출은 약 C$3억이다.","F04"),
 ("SAR 위성","확인 사실","RADARSAT-1·2와 RCM을 프라임으로 설계했다. 경쟁사는 Airbus, ICEYE, e-GEOS다. CHORUS의 X밴드 위성은 ICEYE가 만든다.","최상위권.","F04"),
 ("안테나·탑재체","확인 사실","350개 이상의 위성 미션에 기술이 들어갔다. OneWeb에는 2016년 약 2,000개, 2026년 1,320개 안테나를 수주했다.","프라임들이 사 가는 부품.","F03; F14"),
 ("디지털 위성","리서치 해석","미국 버스 업체(York, Apex, K2, Rocket Lab)는 버스를 팔고 탑재체는 밖에서 산다. AURORA는 재생형 디지털 위성 전체를 제품으로 판다.","실재하는 차별점. 다만 위성 고객은 Telesat과 Globalstar 둘뿐이고 셋째(EchoStar)는 취소했다.","N02"),
 ("대량생산","리서치 해석","고속 공장은 MDA만 가진 것이 아니다. Airbus, Aerospacelab(연 500기 주장), Thales(하루 1기 목표), York(연 300기), Apex(연 200기 이상)가 있다. 2026년 최대 소버린 LEO 플랫폼 발주는 Aerospacelab이 가져갔다.","공장은 해자가 아니다.","N02"),
 ("궤도 검증","확인 사실","Globalstar 교체위성이 2026-08 처음 발사됐다(프라임으로 납품한 첫 상업 LEO 군집). AURORA는 아직 궤도에서 검증되지 않았고 Lightspeed 패스파인더는 2027-06이다.","2027년 Lightspeed의 궤도 성능이 해자 여부를 가른다.","T01; W02"),
 ("버스","추가 확인","Globalstar 17기의 버스는 Rocket Lab이 공급한 것으로 보인다(업계 매체 제목 기준). 소형위성 버스는 BCT로 보강한다.","몸통은 약하고 머리(탑재체)가 강하다. 원문 확인이 필요하다.","W47; N06"),
 ("실행 이력","확인 사실","Globalstar 17기가 지연돼 Globalstar는 지체상금 권리를 공시했다. CHORUS는 공급사 지연으로 2026년 말로 밀렸다. Lightspeed 패스파인더도 지연됐다.","프라임 실행력에 대한 공격 재료 3건.","W47; F03; W02"),
 ("해자: 캐나다 정부","리서치 해석","RADARSAT, Canadarm, ESCP-P 모두 사실상 단독이다.","강하다. 상한은 캐나다 예산이다.","N06"),
 ("해자: 재발주","확인 사실","Lightspeed +27기, Globalstar(17기 후 50기 이상), RCM 보충위성, OneWeb 안테나 재수주가 모두 같은 제작사로 왔다.","군집은 중간에 제작사를 바꾸기 어렵다.","F09; F14; F16"),
 ("해자: 칩","추가 확인","ASIC 내재화는 원가와 성능에서 이점이 될 수 있지만 숫자로 확인되지 않았고 독립 검증도 없다.","잠재적.","N02"),
 ("종합","리서치 해석","해자는 좁다. 확실한 해자(캐나다 정부, 로봇)는 시장이 작고 성장 엔진(AURORA 프라임)은 아직 해자가 아니다.","Why 동사 문단의 수위.","N06"),
 ("Rocket Lab과의 차이","리서치 해석","버스와 발사는 Rocket Lab이 앞서지만 탑재체는 MDA가 앞선다. 캐나다 정부와 로봇은 Rocket Lab이 들어올 수 없는 영역이다.","세션 예상 질문의 답.","N06"),
 ("가격 위치","직접 계산","MDA의 대당 가격(약 US$9~13M)은 서방 범위의 하단으로 York, Aerospacelab과 비슷하다.","가격 경쟁력은 있다. 고정가 마진 압박과 맞물린다.","N02"),
]))

L.append(("13 MDA vs SpaceX","왜 SpaceX가 아닌가","우주가 커진다면 SpaceX를 사면 되는데 왜 MDA인가?","Q&A 대비 · Intro",[
 ("질문의 전제","리서치 해석","투자 논지가 '우주 산업이 구조적으로 커진다'라면 SpaceX가 더 정확한 베팅이다. MDA를 사려면 다른 논지가 필요하다.","세션 첫 질문 대비.","N06"),
 ("반대편","리서치 해석","SpaceX가 커지면 MDA가 같이 좋아지는 것이 아니라 MDA의 고객이 준다. EchoStar가 그 예다.","MDA는 우주 산업 지수가 아니다.","N06"),
 ("대체 논지","리서치 해석","MDA는 Starlink 독점에 대한 대안 수요(주권·국방, 비Starlink 사업자)에 대한 베팅이다.","한 줄 답변.","N06"),
 ("SpaceX 밸류","보도","공모가 $135(시총 약 $1.77T), 첫날 종가 $160.95. 이후 '7월 $1.98T'라는 보도와 '고점 대비 약 −50%'라는 서술이 충돌한다. 마지막 내부자 락업 해제는 2026-12-08로 보도됐다.","현재가를 확인한다. 락업 해제는 우주주 수급 이벤트다.","W25; W26"),
 ("주가 연동","확인 사실","MDA 주가는 SpaceX 상장일(2026-06-12)에 −8.7%였다.","SpaceX가 우주주 자금을 빨아들인 날.","N02"),
 ("규모 효과","리서치 해석","MDA는 시총이 작아 계약 하나가 숫자를 바꾼다. 27기 추가 하나로 수주가 474 늘었다.","SpaceX에는 없는 레버리지.","N06"),
 ("SpaceX의 정부 사업","보도","SpaceX는 2Q26에 미국 계약 $6B 이상을 땄다고 밝혔고 SDN 백본 $2.29B, SB-AMTI $4.16B 수주가 보도됐다.","SpaceX도 미국 소버린을 가져간다. '정부 = 비SpaceX'가 아니다.","N02"),
 ("비교표 재료","리서치 해석","SpaceX는 1등 독식, 발사·구독 매출, 높은 밸류와 머스크 리스크. MDA는 대안 수요, 제조·국방 수주, 고객 집중과 수주 공백.","보고서 표로 만든다.","N06"),
 ("헤지 프레임","리서치 해석","'MDA는 우주 산업 지수가 아니라 Starlink 독점에 대한 헤지다.'","세션 답변 문장. 미국 정부 수요는 예외로 둔다.","N06"),
]))

L.append(("14 실적과 현금흐름","성장·마진·현금·자본","숫자는 논지를 받쳐 주는가, 어디가 약한가?","실적 연결 · 매출추정",[
 ("성장","확인 사실","매출은 2022년 641, 2023년 808, 2024년 1,080, 2025년 1,633(+51%)이고 2026년 가이던스는 1,900~1,950이다.","3년 만에 2.5배.","N02; F01"),
 ("3Q26","확인 사실","3Q26 매출 498.1(+21.5%), 매출총이익률 25.3%, 조정 EBITDA 96.0(19.3%), 조정 순이익 60.4, 조정 EPS 0.37(+0.7%).","EPS는 희석으로 제자리다.","F01"),
 ("마진 추세","확인 사실","조정 EBITDA 마진은 2022년 24.6%, 2023년 21.6%, 2024년 20.1%, 2025년 19.8%, 9M26 19.4%다.","규모가 커질수록 마진이 내려갔다.","N02"),
 ("마진 원인","경영진 설명","프로그램 믹스와 SG&A 투자(9M26 114.4, 전년 81.0)가 원인이다. CFO는 IT·AI·R&D 투자가 2027년에도 이어진다고 했다.","영업 레버리지가 보이지 않는다.","T01; F01"),
 ("4Q26 내재치","직접 계산","가이던스에서 9개월 실적을 빼면 4Q26 매출은 439~489, EBITDA는 72~92, 마진은 약 18%다.","전년 대비 역성장 가능성.","F01; T01"),
 ("현금흐름","확인 사실","OCF는 2024년 812.7, 2025년 407.5, 9M26 73.7이다. FCF는 2024년 614.8, 2025년 165.3, 9M26 −116.2다.","선수금 사이클의 하강 구간.","F01; F02"),
 ("설비투자","확인 사실","2025년 순 capex는 242.2, 2026년 가이던스는 225~275다(몬트리올 증설과 칩 개발). 5년간 C$1.25B를 재투자했다.","매출의 약 13%. 몬트리올 투자 강도는 내려가고 칩은 이어진다.","F02; T01"),
 ("재무상태","확인 사실","2026-09-30 현금 2,153.8, 장기부채 825.8, 순현금 1,328.0, 유동성 2.9B. 영업권 816.2, 무형자산 865.0.","현금은 인수 대금으로 배정돼 있다.","F01"),
 ("주식 수","확인 사실","2025년 말 126.3M주에서 3Q26 가중평균 158.8M주(희석 163.1M주)가 됐다.","약 26% 희석.","F01"),
 ("신용등급","보도","Morningstar DBRS는 발행자 BB(high), 선순위 무담보채 (P)BB를 줬다. S&P는 2차 출처에서 BB−로 나온다.","대화 기록의 'S&P B'는 확인되지 않았다(층위 17).","W40"),
 ("2027년","경영진 전망","CFO는 기존 사업이 '견조한 두 자릿수 성장'을 한다고 했다. 동인은 Lightspeed, Canadarm3, RCM 위성, Mitsubishi, OneWeb 안테나, IRIS², CHORUS이고 감소 요인은 Globalstar다. 정식 가이던스는 2027-03이다.","유기 성장이 유지되는지가 쟁점.","T01"),
 ("반복 매출","직접 계산","현재 반복 매출 비중은 약 15%로 추정된다(CLS로 두 배, 30% 이상이 된다는 발언 역산).","추정.","N04"),
]))

L.append(("15 주가와 밸류에이션","주가 Driver·배수·컨센서스","주가는 무엇을 따라 움직였고 지금 무엇을 반영하고 있는가?","기업분석(주가 분석) · Valuation",[
 ("2021~2025","확인 사실","IPO가는 C$14.00(2021-04)다. 2025-08 월 고점 C$48.31에서 2025-12 C$22.69~27.58로 내려왔다.","EchoStar 취소로 급락한 구간.","F04"),
 ("2026년 고점","보도","NYSE 고점은 US$48.68(2026-05-28), TSX 52주 고점은 C$67.90로 보도됐다. 증자 직전 7/8 종가는 C$54.90, US$38.67이다.","고점 대비 약 35~43% 내려왔다.","N02; W42; F07"),
 ("큰 하락일","확인 사실","2025-09-08 −25~30%(EchoStar 해지), 2026-03 −11%(Gateway 중단), 6/12 −8.7%(SpaceX 상장), 7/9 −8.5%와 7/13 −7.4%(증자), 10/22 −6.7%.","주가 Driver는 대형 계약의 득실, 희석, 우주 섹터 수급이다.","N02; W06; W18"),
 ("주가 Driver","리서치 해석","주가는 잔고(대형 수주와 취소)를 따라 움직였다.","SMIC 가이드의 '주가 Driver를 투자포인트에 연결'. 잔고·주가 도표로 증명한다.","N03; N07"),
 ("현재가","보도","NYSE 종가 US$29.16(11/12), TSX C$42.08(11/13).","미국 상장가 30.50, 증자가 35.60, CSG 취득가 C$42.69가 모두 현재가 이상이다.","N02; W42"),
 ("시총·EV","직접 계산","시가총액은 약 US$4.7B(C$6.7B)다. 두 인수를 반영한 EV는 약 C$7.1B다.","계산값.","N02"),
 ("배수","직접 계산","2027E EV/EBITDA는 약 13배(컨센서스 EBITDA 540~565 기준), 2026E 단독 기준은 약 14~16배, 선행 P/E는 약 29배다.","밸류의 출발점.","N02; N01"),
 ("컨센서스","외부 추정","2027년 매출 C$2.84~2.86B, EBITDA 540~565. 목표가는 JPMorgan US$44, Jefferies US$45, Beacon C$88.","시장과 다른 숫자가 아직 없다.","N02"),
 ("피어","보도","Rocket Lab 선행 EV/Sales 약 23~27배, Planet 약 9배, Redwire 약 3배. York은 2026년 매출 가이던스 $545~595M이다.","기사마다 주가 시점이 다르다. 시세로 다시 계산한다.","W43; W44"),
 ("목표 배수","리서치 해석","18배를 적용하면 약 US$40(+37%)이다.","18배의 근거는 피어 표로 증명해야 한다.","N03"),
 ("할인 요인","리서치 해석","고객 집중, 수주 공백, 고정가, 음의 FCF가 '상업 하청 할인'을 만든다.","해소 조건은 2028년 유기 매출이 줄지 않는 것.","N03"),
 ("밸류 방법","기초 개념","SMIC 가이드는 PER을 기본으로 하고 필요하면 EV/EBITDA를 쓴다. MDA는 인수 무형자산 상각이 커서 조정 EPS나 EV/EBITDA가 맞다.","툴 선택의 근거를 본문에 쓴다.","N07"),
]))

L.append(("16 리스크","Issue & Risk","무엇이 논지를 깨는가, 방어할 수 있는가?","Issue & Risk",[
 ("고객 집중","확인 사실","상위 10개 고객 87.2%. Lightspeed가 잔고의 약 35%다.","방어: 재원이 정부 대출과 군 계약이라는 점.","F04; T01"),
 ("Telesat 신용","보도","GEO 부채 C$3.1B의 만기가 2026-12부터 온다. LEO 법인과의 분리는 원문으로 확인하지 못했다.","Telesat이 법원 절차에 들어가 지급이 멈추면 논지가 깨진다.","W01; N02"),
 ("실행","보도","Lightspeed 패스파인더, Globalstar 17기, CHORUS가 모두 지연됐다.","프라임 실행력 질문이 나온다. 재무 영향이 없다는 회사 답변만으로는 약하다.","W02; W47"),
 ("Globalstar와 Amazon","확인 사실","차세대 매출은 2027년부터 줄고 Amazon은 2028년부터 자체 D2D를 계획한다. 지체상금 금액은 협의 중이다.","후속 발주를 가정하지 않는다.","T01; W04; N02"),
 ("편의 해지","확인 사실","대부분 계약이 언제든 해지될 수 있다. EchoStar가 선례다.","정부 계약도 예외가 아니다(호주 JP9102).","F04"),
 ("고정가 마진","확인 사실","계약 대부분이 고정가이고 EBITDA 마진은 4년째 내려왔다.","정부 일감의 마진은 공시되지 않는다.","F04; N02"),
 ("시점 불일치","리서치 해석","정부 사업은 정의 단계가 길고 덩어리로 들어온다. 2028년에 일시적인 공백이 생길 수 있다.","2028년 공백 시나리오를 본문에 넣는다.","N03"),
 ("인수 승인·통합","확인 사실","BCT는 HSR·CFIUS, CLS는 규제 승인이 남았다. 미국과 프랑스를 동시에 통합한다.","종결 지연 시 추가 지급 조항이 있다.","F08; T01"),
 ("희석·수급","확인 사실","2026년 주식 수가 약 26% 늘었다. 전환사채는 확인되지 않았다. CSG는 현금결제 스왑으로 추가 노출을 쌓고 있다(헤지 기간 2027-08-31까지).","SMIC 체크리스트의 오버행 항목. CB·워런트 유무를 재무제표로 확정한다.","F01; N02"),
 ("정책 의존","확인 사실","Gateway 중단처럼 다른 나라 정부의 결정에 노출된다. 캐나다 2026년 예산에는 우주 항목 숫자가 거의 없다.","예산 증가분의 우주 몫을 증명해야 한다.","W18; N03"),
 ("발사 의존","확인 사실","CHORUS와 고객 위성 모두 Falcon 9에 의존한다.","CEO는 '지켜볼 지점'이라고 했다.","T01"),
 ("소송","확인 사실","EchoStar 공시와 내부자 매도에 관한 집단소송이 2025-11-17 제기됐다. 청구액은 약 C$225M, C$25M, C$90M이다. 회사는 근거가 없다는 입장이다.","내부자 매도 내역을 확인해 둔다.","F03; F04"),
 ("단일 위성","확인 사실","RADARSAT-2는 설계수명을 넘겼다. CHORUS 가동 전에 고장 나면 Geointelligence 매출이 타격을 받는다.","CHORUS 발사(2026년 말)가 해소 이벤트.","F04"),
 ("EU 현지조달","보도","비EU 공급사 제한 규칙과 '왜 유럽산이 아니냐'는 비판이 있다.","IRIS² 본계약 전환의 변수.","N02"),
]))

L.append(("17 자료 정정","엇갈린 숫자와 고칠 것","기존 노트와 대화 기록에서 무엇을 고쳐야 하는가?","리서치 품질",[
 ("잔고의 73%","수정 필요","'잔고의 73%가 Telesat·Globalstar'는 독립 리서치 수치이고 잔고 C$4.4B 시점(2025년) 기준으로 보인다. 3Q26 기준으로 직접 계산하면 Lightspeed 1.4B(35%)와 Globalstar 잔여 약 US$271M(약 C$0.38B, 10%)를 합쳐 약 45%다.","최신 분기로 다시 계산한 값을 쓴다.","W37; N02; T01"),
 ("Lightspeed +69기","수정 필요","'추가분 69기를 전부 MDA가 제작'은 Telesat의 배치 계획(156기 → 225기) 기준이다. MDA의 수주는 198기 → 225기로 +27기(C$474M)다.","MDA 증분은 27기로 쓴다.","F09; G01"),
 ("9개월 수주","추가 확인","릴리스는 9M26 수주를 1,397.0으로, 콜은 '총 수주 약 1.6B'로 말한다. 2Q26 릴리스에 River-class Destroyer 범위 축소가 순수주에 반영됐다는 주석이 있다.","총수주와 순수주의 차이일 가능성. 약 200의 차감 내역을 확인한다.","F01; F05; T01"),
 ("3Q 수주와 474","추가 확인","Lightspeed 추가분 474가 3Q26 수주 444.2보다 크다.","일부만 편입됐거나 차감이 있었을 것이다. 확인한다.","F01; F09"),
 ("Lightspeed 금액","수정 필요","2.1B(최초), 2.4B(AIF), 2.9B(확장 후 IR 자료)가 섞여 쓰인다. 대수는 198 → 225, 옵션은 100 → 73이다.","시점을 붙여 쓴다.","F04; F06"),
 ("Globalstar 금액","수정 필요","C$1.1B(MDA), US$750M(AIF), US$775M(Globalstar 10-Q)가 섞여 있다. 17기 건은 US$327M 또는 US$329.3M이다. '$415M'은 17기 건의 C$ 환산이다.","통화와 출처를 명시한다.","F04; N02"),
 ("Globalstar 발사 수","추가 확인","대화 기록은 '8기 발사', 콜 전사본은 '8기 … 남은 9기'로 읽힌다.","17기 중 8기 발사, 9기 연내 납품으로 읽는 것이 자연스럽다. Globalstar 공시로 확인한다.","T01; N06"),
 ("CLS 가격","수정 필요","€567M(70%)과 '$920M'이 같이 돈다. 후자는 C$ 환산(약 C$920M)이거나 부채 €198M 포함 기준이다.","유로 기준으로 쓴다.","W23"),
 ("S&P 등급","수정 필요","대화 기록의 'S&P B, 2027년 부채비율 3배'는 확인되지 않았다. 확인된 것은 DBRS BB(high)와 2차 출처의 S&P BB−다.","등급 원문을 확인하기 전에는 인용하지 않는다.","W40"),
 ("SpaceX 상장 수치","추가 확인","조달액은 $75B와 $86B, 상장 후 주가는 '$1.98T'와 '고점 대비 −50%'로 갈린다.","시세와 공시로 확인한다.","W25; W26"),
 ("공장 용량","수정 필요","'연 400기'와 '하루 2기'가 섞여 있다. 회사 표현은 'up to'이고 2026년 초 실제 속도는 주 1기 수준이다.","명목 용량이라고 표시한다.","W38; W39"),
 ("ESCP-P 금액","수정 필요","Telesat 계약은 C$2.3B인데 '$1.6B'(US$ 환산)나 2.7B(옵션 포함)로도 쓰인다.","C$ 기준으로 쓰고 옵션을 구분한다.","G01"),
 ("패스파인더 발사일","수정 필요","일부 매체의 '2028년 6월'은 오기로 보인다. 다수는 2027년 6월이다.","2027-06으로 쓴다.","W02; W01"),
 ("상업·정부 비중","추가 확인","상업 72%, 정부 28%는 IR 자료 p4를 브랜치 노트를 거쳐 인용한 것이다. Lightspeed가 어느 쪽인지 정의를 확인해야 한다.","'돈 내는 주체'로 다시 나누면 비중이 달라진다.","F06"),
 ("NYSE 상장 주식 수","추가 확인","검색 결과는 9,836,065주, 브랜치 노트는 1,118만 주다.","초과배정 포함 여부의 차이로 보인다. 6-K로 확인한다.","N02; F07"),
 ("기억으로 쓴 서술","추가 확인","한국 기관 구조, 차세대중형위성 주관 이전, 외국 지배 차단 조치 일반론은 검색 없이 기억으로 적었다.","보고서에 넣기 전에 출처를 붙인다.","N06"),
]))

L.append(("18 추가 조사와 구성","다음 조사와 보고서 구조","보고서를 어떻게 짜고, 무엇부터 더 조사할 것인가?","보고서 구성",[
 ("커버리지 중복","확인 사실","SMIC 커버리지 리스트에 MDA Space는 없다. 관련 과거 보고서는 우주산업(2024.01), 쎄트렉아이(2024.08, 2016.11), 한화시스템(2024.08), 인텔리안테크(2021.12, 2019.02), 한국항공우주(2026.02 등)다.","종목 중복은 없다. 과거 우주 보고서와 논리가 겹치는지 확인한다.","N07"),
 ("보고서 유형","리서치 해석","SMIC 7유형 중 Top-Down(투자포인트 1은 전방, 2는 동사의 몫)에 가깝다. 현재 안은 시장 논리 → 투자포인트 1 캐나다 → 투자포인트 2 해외다.","구조를 확정한다.","N07; N03"),
 ("목차 안","리서치 해석","표지(상업 공장에서 국가 공장으로) / 산업 / 기업(잔고와 주가) / 시장 논리 / 투자포인트 1 / 투자포인트 2 / 리스크 / 밸류.","브랜치 v2 구조.","N03"),
 ("키 도표","리서치 해석","① 위성 부문 매출: 상업 감소분과 정부 증가분 누적 막대 ② 잔고와 주가 추이(EchoStar 표시) ③ Lightspeed·Globalstar 연도별 인식 ④ 캐나다 프로그램 표 ⑤ 서방 제조사 비교표 ⑥ 피어 배수.","도표를 먼저 정하고 글을 맞춘다(SMIC 가이드).","N03; N07"),
 ("Why Now","리서치 해석","주가는 상장가, 증자가, 전략 주주 취득가 아래에 있다. 촉매는 ESCP-P MEO 본계약(수개월 내), CHORUS 발사(2026년 말), BCT·CLS 종결, 2027-03 가이던스, Lightspeed 패스파인더(2027-06)다.","시의성.","N02; N04"),
 ("매출추정 방법","리서치 해석","P×Q로 짠다. 프로그램별(대수 × 대당 단가 × 인식 곡선), 부품(위성당 납품 금액 × 대수), 반복 매출로 나눈다. CAGR은 쓰지 않는다.","SMIC 가이드의 데칼코마니 원칙.","N07"),
 ("조사 1","추가 확인","위성 부문 매출을 고객별로 나눈다. Lightspeed와 Globalstar의 연도별 인식액으로 구멍 크기를 확정한다.","최우선.","N03"),
 ("조사 2","추가 확인","ESCP-P MEO에서 MDA 몫의 금액과 일정을 확인한다(국방투자청 공고, IR 문의).","투자포인트 1의 성패.","N03"),
 ("조사 3","추가 확인","캐나다 국방부 우주 예산을 확인한다(부서별 계획, 국방산업전략 세부).","우주 몫의 정량 근거.","N03"),
 ("조사 4","추가 확인","잔고를 '돈 내는 주체'(정부 재원, 상업 재원)로 다시 나눈다.","투자포인트 1의 키 도표.","N02"),
 ("조사 5","추가 확인","감사 재무제표 주석에서 매출 인식 방식, 10% 이상 고객, 12개월 내 인식 잔고를 확인한다.","매출추정의 전제.","N01"),
 ("조사 6","추가 확인","Telesat 20-F·6-K 주석에서 LEO 법인의 보증 여부와 MDA 지급 조건을 확인한다.","최대 리스크의 방어 근거.","N02"),
 ("조사 7","추가 확인","피어 배수 표(Rocket Lab, York, Redwire, Planet, L3Harris, Kratos, OHB)를 만들고 목표 배수의 근거를 세운다.","밸류에이션.","N03"),
 ("조사 8","추가 확인","셀사이드 리포트 원문 8편 이상과 3Q26 IR 자료 원본 페이지를 대조한다.","컨센서스와 다른 숫자를 찾는다.","N02"),
 ("반증 조건","리서치 해석","ESCP-P MEO 본계약이 2027년 상반기까지 없거나 1B 미만 / 2027년 말 유기 잔고 4B 미만 / Telesat 법원 절차로 지급 중단 / 해외 소버린 수주 없음 / BCT CFIUS 무산.","트래킹 항목.","N01; N02"),
]))

# ---------------------------------------------------------------- quarterly series
# quarter, revenue, sat systems, robotics, geo, adj ebitda, bookings, backlog end, note
Q = [
 ("2022Q1",128.4,37.1,42.4,48.9,44.5,780.9,1516.8,""),
 ("2022Q2",154.7,58.9,48.8,47.0,34.7,158.7,1520.8,""),
 ("2022Q3",172.0,71.9,54.6,45.5,38.8,56.3,1405.1,""),
 ("2022Q4",186.1,84.3,47.9,53.9,39.9,159.2,1378.2,""),
 ("2023Q1",201.9,87.7,62.9,51.3,48.9,56.1,1232.4,""),
 ("2023Q2",196.0,89.4,58.7,47.9,40.4,61.9,1098.3,""),
 ("2023Q3",204.7,94.4,61.9,48.4,42.8,2175.1,3068.7,"Telesat Lightspeed 프라임 계약"),
 ("2023Q4",205.0,None,None,None,42.1,233.3,3097.0,"매출·수주는 연간에서 9개월을 뺀 값. 사업부 미확보"),
 ("2024Q1",209.1,87.0,70.6,51.5,42.0,424.3,3312.2,""),
 ("2024Q2",242.0,109.1,78.0,54.9,48.7,1525.8,4596.0,"9개월 누계에서 역산. Canadarm3 C$1B, Globalstar ATP"),
 ("2024Q3",282.4,167.6,66.5,48.3,55.5,264.5,4578.1,""),
 ("2024Q4",346.6,234.5,64.7,47.4,70.9,154.0,4385.5,"FY2025 릴리스의 4Q24 비교치"),
 ("2025Q1",351.0,222.0,77.3,51.7,68.6,803.9,4838.4,"Globalstar 본계약(총 C$1.1B). 잔고 정점"),
 ("2025Q2",373.3,232.6,88.0,52.7,76.3,102.8,4567.9,""),
 ("2025Q3",409.8,283.5,78.3,48.0,82.8,174.2,4392.8,"SatixFy 기초 잔고 60.5 별도 가산. EchoStar 수주와 해지가 같은 분기"),
 ("2025Q4",499.1,371.4,65.7,62.0,96.2,119.2,4012.9,"EchoStar 해지 정산 포함"),
 ("2026Q1",464.1,313.1,91.6,59.4,90.6,143.9,3692.7,"잔고 저점"),
 ("2026Q2",498.6,336.1,99.5,63.0,96.3,808.9,4003.0,"RCM 보충위성 C$688M, 일본 탑재체"),
 ("2026Q3",498.1,358.3,79.9,59.9,96.0,444.2,3949.1,"Lightspeed +27기 C$474M"),
]

# ---------------------------------------------------------------- metrics ledger
# (key, 분류, 지표, 기간·기준, 값 or formula with {key}, 단위, 성격, 해석·주의, 출처, numfmt)
N1 = '#,##0.0;(#,##0.0);"—"'; N0 = '#,##0;(#,##0);"—"'; P1 = '0.0%;(0.0%);"—"'; X2 = '0.00"x";(0.00"x");"—"'; N2 = '#,##0.00;(#,##0.00);"—"'
M = []
def m(key,cat,name,period,val,unit,kind,note,src,fmt=N1): M.append((key,cat,name,period,val,unit,kind,note,src,fmt))

for y,rev,bk,bl,eb in [("FY2022",641.2,1155.1,1378.2,157.9),("FY2023",807.6,2526.4,3097.0,174.2),("FY2024",1080.1,2368.6,4385.5,217.1),("FY2025",1633.2,1200.1,4012.9,323.9),("9M2026",1460.8,1397.0,3949.1,282.9)]:
    src = "N02; F02" if y in ("FY2022","FY2023") else ("F02" if y in ("FY2024","FY2025") else "F01")
    m(f"rev{y}","연간 실적","매출",y,rev,"C$ m","실적","2022·2023은 분기 합계." if y<"FY2024" else "",src)
    m(f"bk{y}","연간 실적","수주(order bookings)",y,bk,"C$ m","실적","비IFRS 지표. 확정 계약 금액 합계.",src)
    m(f"bl{y}","연간 실적","기말 수주잔고",y,bl,"C$ m","실적","미행사 옵션·IDIQ 제외.",src)
    m(f"eb{y}","연간 실적","조정 EBITDA",y,eb,"C$ m","실적","",src)
    m(f"bb{y}","연결 계산","수주/매출(book-to-bill)",y,f"={{bk{y}}}/{{rev{y}}}","배","직접 계산","1 미만이면 잔고가 준다.","계산",X2)
    m(f"mg{y}","연결 계산","조정 EBITDA 마진",y,f"={{eb{y}}}/{{rev{y}}}","%","직접 계산","",  "계산",P1)
m("blrev24","연결 계산","잔고/연매출","2024년 말","={blFY2024}/{revFY2024}","배","직접 계산","","계산",X2)
m("blrev25","연결 계산","잔고/연매출","2025년 말","={blFY2025}/{revFY2025}","배","직접 계산","","계산",X2)
m("blrev26","연결 계산","잔고/2026 가이던스 중간값","2026-09","={bl9M2026}/(({g_rev_lo}+{g_rev_hi})/2)","배","직접 계산","","계산",X2)

for y,ss,ro,ge,src in [("FY2024",598.2,279.8,202.1,"F02"),("FY2025",1109.5,309.3,214.4,"F02"),("9M2026",1007.5,271.0,182.3,"F01")]:
    m(f"ss{y}","사업부 매출","Satellite Systems",y,ss,"C$ m","실적","",src)
    m(f"ro{y}","사업부 매출","Robotics & Space Operations",y,ro,"C$ m","실적","",src)
    m(f"ge{y}","사업부 매출","Geointelligence",y,ge,"C$ m","실적","",src)
m("ssShare25","연결 계산","Satellite Systems 매출 비중","FY2025","={ssFY2025}/{revFY2025}","%","직접 계산","AIF 기재 68%와 일치.","계산",P1)
m("ssShare26","연결 계산","Satellite Systems 매출 비중","9M2026","={ss9M2026}/{rev9M2026}","%","직접 계산","","계산",P1)
m("ssAnnual","연결 계산","Satellite Systems 연환산 매출","9M2026 × 4/3","={ss9M2026}*4/3","C$ m","직접 계산","구멍 크기 추정의 분모.","계산")

m("q3rev","분기 실적","매출","3Q2026",498.1,"C$ m","실적","전년 동기 409.8, +21.5%.","F01")
m("q3gm","분기 실적","매출총이익률","3Q2026",0.253,"%","실적","전년 동기 26.4%. 프로그램 믹스.","F01",P1)
m("q3eb","분기 실적","조정 EBITDA","3Q2026",96.0,"C$ m","실적","마진 19.3%.","F01")
m("q3ni","분기 실적","조정 순이익","3Q2026",60.4,"C$ m","실적","2026년부터 조정 실효세율 적용.","F01")
m("q3eps","분기 실적","조정 희석 EPS","3Q2026",0.37,"C$/주","실적","전년 동기 0.37. 주식 수 증가로 정체.","F01",N2)
m("sga26","분기 실적","SG&A","9M2026",114.4,"C$ m","실적","전년 동기 81.0.","F01")
m("sga25","분기 실적","SG&A","9M2025",81.0,"C$ m","실적","","F01")
m("rd26","분기 실적","R&D(순)","9M2026",33.0,"C$ m","실적","전년 동기 23.4.","F01")

m("g0_lo","가이던스","2026 매출 가이던스 하단(최초)","2026-03",1700,"C$ m","경영진 전망","","F02",N0)
m("g0_hi","가이던스","2026 매출 가이던스 상단(최초)","2026-03",1900,"C$ m","경영진 전망","","F02",N0)
m("g_rev_lo","가이던스","2026 매출 가이던스 하단","2026-11",1900,"C$ m","경영진 전망","BCT·CLS 제외.","F01",N0)
m("g_rev_hi","가이던스","2026 매출 가이던스 상단","2026-11",1950,"C$ m","경영진 전망","","F01",N0)
m("g_eb_lo","가이던스","2026 조정 EBITDA 가이던스 하단","2026-11",355,"C$ m","경영진 전망","마진 18~20%.","F01",N0)
m("g_eb_hi","가이던스","2026 조정 EBITDA 가이던스 상단","2026-11",375,"C$ m","경영진 전망","","F01",N0)
m("g_cx_lo","가이던스","2026 capex 가이던스 하단","2026-11",225,"C$ m","경영진 전망","몬트리올 증설·칩 개발.","F01",N0)
m("g_cx_hi","가이던스","2026 capex 가이던스 상단","2026-11",275,"C$ m","경영진 전망","","F01",N0)
m("q4lo","연결 계산","4Q26 내재 매출 하단","2026","={g_rev_lo}-{rev9M2026}","C$ m","직접 계산","전년 4Q 499.1.","계산")
m("q4hi","연결 계산","4Q26 내재 매출 상단","2026","={g_rev_hi}-{rev9M2026}","C$ m","직접 계산","","계산")
m("q4eblo","연결 계산","4Q26 내재 조정 EBITDA 하단","2026","={g_eb_lo}-{eb9M2026}","C$ m","직접 계산","","계산")
m("q4ebhi","연결 계산","4Q26 내재 조정 EBITDA 상단","2026","={g_eb_hi}-{eb9M2026}","C$ m","직접 계산","","계산")

for y,o,f,src in [("FY2024",812.7,614.8,"F02"),("FY2025",407.5,165.3,"F02"),("9M2026",73.7,-116.2,"F01")]:
    m(f"ocf{y}","현금흐름","영업현금흐름",y,o,"C$ m","실적","",src)
    m(f"fcf{y}","현금흐름","잉여현금흐름",y,f,"C$ m","실적" if y!="9M2026" else "직접 계산","OCF − 순 capex(정부 보조금 차감)." + (" 릴리스에 9개월 합계가 없어 직접 계산." if y=="9M2026" else ""),src)
m("capex25","현금흐름","순 capex","FY2025",242.2,"C$ m","직접 계산","유형 175.3 + 무형 100.1 − 보조금 33.2.","F02")
m("cash","재무상태","현금","2026-09-30",2153.8,"C$ m","실적","증자·사채 대금. 인수에 쓸 예정.","F01")
m("debt","재무상태","장기부채","2026-09-30",825.8,"C$ m","실적","리스부채 133.6 별도.","F01")
m("netcash","재무상태","순현금","2026-09-30","={cash}-{debt}","C$ m","직접 계산","릴리스 기재 1,328.0과 일치.","계산")
m("cl25","재무상태","계약부채","2025-12-31",798.9,"C$ m","실적","선수금 잔액.","F02")
m("cl26","재무상태","계약부채","2026-09-30",601.7,"C$ m","실적","선수금 소진 중.","F01")
m("gw","재무상태","영업권","2026-09-30",816.2,"C$ m","실적","","F01")
m("intang","재무상태","무형자산","2026-09-30",865.0,"C$ m","실적","","F01")
m("ta","재무상태","총자산","2026-09-30",5543.4,"C$ m","실적","","F01")
m("gwshare","연결 계산","(영업권+무형자산)/총자산","2026-09-30","=({gw}+{intang})/{ta}","%","직접 계산","","계산",P1)
m("eq","재무상태","자본총계","2026-09-30",3050.0,"C$ m","실적","","F01")

m("sh25","자본","발행주식 수","2025-12-31",126.3,"백만 주","확인 사실","","F04")
m("sh26","자본","가중평균 주식 수(기본)","3Q2026",158.8,"백만 주","실적","희석 163.1.","F01")
m("dil","연결 계산","주식 수 증가율","2025말 → 3Q26","={sh26}/{sh25}-1","%","직접 계산","","계산",P1)
m("ipoNY","자본","NYSE 상장 공모가","2026-03",30.50,"US$/주","확인 사실","9,836,065주(브랜치 노트는 1,118만 주).","F07",N2)
m("bdpx","자본","bought deal 발행가","2026-07",35.60,"US$/주","확인 사실","2,300만 주.","F07",N2)
m("bdsh","자본","bought deal 주식 수","2026-07",23.0,"백만 주","확인 사실","2,000만 주에서 증액.","F07")
m("bdamt","연결 계산","bought deal 조달액","2026-07","={bdpx}*{bdsh}","US$ m","직접 계산","공시 약 US$819M과 일치.","계산")
m("note1","자본","선순위 무담보채 2030","2025-12",250,"C$ m","확인 사실","7.00%.","F03",N0)
m("note2","자본","선순위 무담보채 2033","2026-08",600,"C$ m","보도","6.50%. 1차 릴리스 미확인.","W24",N0)

m("ls_val","계약","Telesat Lightspeed 계약액","2023-08(AIF 기준)",2400,"C$ m","확인 사실","최초 발표는 2.1B.","F04",N0)
m("ls_n","계약","Telesat Lightspeed 대수","2023-08",198,"기","확인 사실","옵션 100기.","F04",N0)
m("ls_px","연결 계산","Lightspeed 대당 단가","계약 기준","={ls_val}/{ls_n}","C$ m/기","직접 계산","","계산")
m("lx_val","계약","Lightspeed 확장 계약액","2026-08-04",474,"C$ m","확인 사실","ESCP-P 군용 Ka.","F09",N0)
m("lx_n","계약","Lightspeed 확장 대수","2026-08-04",27,"기","확인 사실","","F09",N0)
m("lx_px","연결 계산","확장분 대당 단가","계약 기준","={lx_val}/{lx_n}","C$ m/기","직접 계산","군용 사양이 단가를 올렸다.","계산")
m("ls_rem","계약","Lightspeed 잔여 잔고","2026-09-30",1400,"C$ m","경영진 설명","2027~2029 인식.","T01",N0)
m("ls_share","연결 계산","Lightspeed/전체 잔고","2026-09-30","={ls_rem}/{bl9M2026}","%","직접 계산","","계산",P1)
m("gs_val","계약","Globalstar 차세대 계약액","2025-02",1100,"C$ m","확인 사실","AIF는 US$750M, Globalstar 10-Q는 US$775M.","F03",N0)
m("gs_rem","계약","Globalstar 차세대 잔여","2026-09 추정",245,"US$ m","직접 계산","Globalstar 집행액 US$529.5M 기준. 브랜치 노트 계산.","N02",N0)
m("gs17","계약","Globalstar 17기 계약액","2022",327,"US$ m","확인 사실","옵션 9기. 잔여 약 US$26M.","F04",N0)
m("echo","계약","EchoStar 계약액(해지)","2025-08",1300,"US$ m","확인 사실","100기 이상. 2025-09 편의 해지.","F10",N0)
m("ca3","계약","Canadarm3 잠재 총매출","2024-06",1800,"C$ m","확인 사실","Phase C/D 1,000, 15년 운영 포함.","F03",N0)
m("rcm","계약","RCM 보충위성 본계약","2026-06",688,"C$ m","확인 사실","2Q26 수주.","F16",N0)
m("rsp","계약","RADARSAT+ 이니셔티브","2023-10 발표",1012,"C$ m","확인 사실","15년. MDA 몫 전체는 아님.","F04",N0)
m("escp1","계약","ESCP-P 1단계(Telesat 계약)","2026-08-04",2300,"C$ m","확인 사실","MDA 계약이 아니라 Telesat 계약. 옵션 214·218 별도.","G01",N0)
m("iris","계약","IRIS² L1 안테나 ATP","2026-10-30",100,"C$ m","회사 발표","'이상'. 본계약 전, 4Q26 잔고 편입 예정.","W15",N0)
m("big2","연결 계산","2026년 대형 2건 수주 합계","9M2026","={rcm}+{lx_val}","C$ m","직접 계산","","계산",N0)
m("rest","연결 계산","대형 2건 제외 분기 평균 수주","9M2026","=({bk9M2026}-{big2})/3","C$ m","직접 계산","대형 정부 계약이 없을 때의 수주 속도.","계산")
m("pipe","계약","기회 파이프라인","2026-11",40000,"C$ m","회사 발표","구성 미공시. 약 30,000이 위성시스템이라는 2차 요약.","F01",N0)
m("pipe10","계약","다운셀렉트·후속 기회","2026-03",10000,"C$ m","회사 발표","정부 다운셀렉트 또는 기존 고객 후속.","F02",N0)

m("top10","집중도","상위 10개 고객 매출 비중","FY2025",0.872,"%","확인 사실","개별 고객 비중은 미공시.","F04",P1)
m("nonca","집중도","캐나다 외 매출 비중","FY2025",0.374,"%","확인 사실","","F04",P1)
m("ca26","집중도","캐나다 매출 비중","9M2026",0.70,"%","확인 사실","1,018/1,461. 브랜치 노트 경유.","N02",P1)
m("comm","집중도","상업 고객 매출 비중","FY2025",0.72,"%","회사 발표","IR 자료 p4. Lightspeed 분류 확인 필요.","F06",P1)

m("bct","인수","BCT 인수가","2026-06-19",620,"US$ m","확인 사실","약 C$874M. 100% 현금.","F08",N0)
m("cls","인수","CLS 70% 인수가","2026-07-08",567,"€ m","확인 사실","부채 약 €198M 상환 가능.","F17",N0)
m("cls25","인수","CLS 매출","2025",203,"€ m","회사 발표","","W23",N0)
m("cls26","인수","CLS 예상 매출","2026E",286,"€ m","회사 발표","","W23",N0)
m("pf","인수","BCT·CLS 프로포마 매출","2026",700,"C$ m","경영진 설명","두 회사 합산.","T01",N0)
m("satixfy","인수","SatixFy 총 대가","2025-07-02",448.3,"C$ m","확인 사실","","F03")
m("outflow","인수","두 인수 대금 합계","추정",1794,"C$ m","직접 계산","874 + 920. 브랜치 노트 계산.","N02",N0)
m("pfnd","연결 계산","인수 후 순차입(추정)","프로포마","={outflow}-{netcash}","C$ m","직접 계산","수수료·운전자본·CLS 부채 제외.","계산")
m("pflev","연결 계산","인수 후 순차입/2026E EBITDA","프로포마","={pfnd}/(({g_eb_lo}+{g_eb_hi})/2)","배","직접 계산","인수 회사 EBITDA 미반영. 회사 목표 1.5~2.5배.","계산",X2)

m("pxNY","주가·밸류","NYSE 종가","2026-11-12",29.16,"US$/주","보도","브랜치 노트 경유. 시세 재확인.","N02",N2)
m("pxTO","주가·밸류","TSX 주가","2026-11-13",42.08,"C$/주","보도","","W42",N2)
m("csg","주가·밸류","CSG 평균 취득가","2026-10-13",42.69,"C$/주","확인 사실","9.5%, 1,536만 주.","N02",N2)
m("hiNY","주가·밸류","NYSE 고점","2026-05-28",48.68,"US$/주","보도","","N02",N2)
m("hiTO","주가·밸류","TSX 52주 고점","2026",67.90,"C$/주","보도","날짜 미확인.","W42",N2)
m("ddNY","연결 계산","NYSE 고점 대비","2026-11-12","={pxNY}/{hiNY}-1","%","직접 계산","","계산",P1)
m("vsIPO","연결 계산","현재가/NYSE 공모가","2026-11-12","={pxNY}/{ipoNY}-1","%","직접 계산","","계산",P1)
m("vsBD","연결 계산","현재가/증자가","2026-11-12","={pxNY}/{bdpx}-1","%","직접 계산","","계산",P1)
m("mcap","주가·밸류","시가총액","2026-11-12",6700,"C$ m","직접 계산","약 US$4.7B. 브랜치 노트 계산.","N02",N0)
m("ev","주가·밸류","인수 반영 EV","프로포마",7100,"C$ m","직접 계산","브랜치 노트 계산.","N02",N0)
m("c27rev","주가·밸류","2027 컨센서스 매출","2026-11",2850,"C$ m","외부 추정","2.84~2.86B.","N02",N0)
m("c27eb","주가·밸류","2027 컨센서스 EBITDA","2026-11",552.5,"C$ m","외부 추정","540~565의 중간.","N02")
m("evx","연결 계산","2027E EV/EBITDA","프로포마","={ev}/{c27eb}","배","직접 계산","","계산",X2)
m("evs","연결 계산","2027E EV/Sales","프로포마","={ev}/{c27rev}","배","직접 계산","피어 EV/Sales와 비교.","계산",X2)
m("tpJ","주가·밸류","목표가 JPMorgan","2026-11-10",44,"US$/주","외부 추정","50에서 하향.","W41",N0)
m("tpF","주가·밸류","목표가 Jefferies","2026-11",45,"US$/주","외부 추정","49에서 하향.","W41",N0)

m("nv_n","산업","2025~2034 발사 위성","Novaspace 28판",43000,"기","외부 추정","","W11",N0)
m("nv_v","산업","제조+발사 시장 가치","2025~2034",665,"US$ bn","외부 추정","$655B로 쓴 보도도 있음.","W11",N0)
m("nv_mc","산업","메가군집 위성 수 비중","2025~2034",0.66,"%","외부 추정","가치로는 11%.","W10",P1)
m("nv_def","산업","국방의 가치 비중","2025~2034",0.48,"%","외부 추정","위성 수로는 9%.","W10",P1)
m("nv_open","산업","완전히 열린 제조 시장","가치 기준",0.07,"%","외부 추정","약 70%는 자국 캡티브.","W10",P1)
m("nv_rest","연결 계산","메가군집 밖 위성 수","2025~2034","={nv_n}*(1-{nv_mc})","기","직접 계산","MDA '접근 가능 20~30%'의 모집단.","계산",N0)
m("gov","산업","정부 우주예산","2025",137.4,"US$ bn","외부 추정","국방 73.5, 민간 63.7.","F04")
m("def28","산업","우주 국방 예산 전망","2028",121,"US$ bn","외부 추정","2025년 74.","W12",N0)
m("iris_n","산업","IRIS² 위성 수","2026-08 합의",348,"기","확인 사실","LEO 330 + MEO 18.","W13",N0)
m("iris_v","산업","IRIS² 프로그램 규모","2026-08 합의",15.6,"€ bn","보도","","W13")
m("de","산업","독일 군사우주 공약","~2030",35,"€ bn","보도","공약. 계약 아님.","W14",N0)
m("spx","산업","SpaceX 공모 시가총액","2026-06-12",1.77,"US$ tn","보도","공모가 $135.","W25",N2)
m("amz","산업","Amazon–Globalstar 인수가","2026-04",11.6,"US$ bn","보도","","W04")
m("es","산업","EchoStar 주파수 매각(SpaceX)","2025-09",17,"US$ bn","보도","","W08",N0)
m("rkir","산업","Rocket Lab–Iridium 기업가치","2026-06-29",8.0,"US$ bn","확인 사실","","W27")
m("alab","피어","Aerospacelab IRIS² L2 플랫폼 단가","2026-09",9.1,"€ m/기","직접 계산","€2.4B ÷ 264기.","W34")
m("yorkg","피어","York 2026 매출 가이던스 중간","2026",570,"US$ m","외부 추정","$545~595M. 잔고 $642M(1Q26).","W44",N0)
m("apex","피어","Apex 기업가치(협상 중)","2026-10",4.0,"US$ bn","보도","","W45")
m("k2","피어","K2 Space 기업가치","2026",6.8,"US$ bn","보도","브랜치 노트 경유.","N02")
