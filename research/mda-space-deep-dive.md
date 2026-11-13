# MDA Space (TSX/NYSE: MDA) 딥다이브 — BM 해부와 투자포인트 검증

작성 기준일: 2026-11-13 · 통화: 별도 표기 없으면 C$(캐나다 달러)

표기 규칙
- **[1차]** 회사 공시(실적 릴리스, MD&A, AIF)·정부 발표에서 직접 확인한 수치
- **[2차]** 업계 매체·검색 요약으로 확인한 수치(보고서 인용 전 원문 대조 필요)
- **[추정]** 공시 수치로 내가 계산한 값

---

## 0. 결론 먼저

1. **MDA는 "위성을 운영하는 회사"가 아니라 "위성을 만들어 파는 회사"다.** 매출의 68%가 위성 제조(Satellite Systems)이고, 그 대부분이 Telesat Lightspeed·Globalstar 두 건의 LEO 군집위성 프라임 계약에서 나온다. 2025년 매출 구성은 상업 72% / 정부 28%로 **[2차]**, 지금 이 순간의 MDA는 소버린 기업이 아니라 "SpaceX·Amazon이 아닌 상업 군집위성"에 가장 크게 노출된 회사다.
2. **"상업 수요는 SpaceX·Amazon에 항복한다"는 전제는 MDA 자신의 계약에서 이미 두 번 증명됐다.** EchoStar는 스펙트럼을 SpaceX에 팔고 US$1.3B 계약을 5주 만에 해지했고(2025-09), Globalstar는 Amazon에 인수된다(2026-04 발표, 2027 종결 예정). 이 전제는 논증하기 쉽다.
3. **"소버린 수요가 구조적으로 커진다"는 전제도 증거가 충분하다.** IRIS² 348기·€15.6B로 확대, 독일 군사우주 €35B, 캐나다 ESCP-P, 한국 K-LEO, 일본 방위통신위성 등.
4. **가장 약한 고리는 "그 시장 안에서 MDA 점유율이 커진다"이다.** 소버린 프로그램은 본질적으로 자국 산업에 돌아간다. MDA는 캐나다에서는 프라임이지만 해외에서는 안테나·디지털 페이로드를 납품하는 부품사 위치다. 그리고 수주잔고는 10분기째 약 C$4B에서 정체, 2025년과 2026년 9개월 누적 book-to-bill 모두 1 미만이다.
5. **따라서 논증은 가능하지만 문장을 바꿔야 한다.** "소버린 시장에서 점유율 상승"이 아니라 **"상업 군집위성 프라임에서 소버린·국방 공급자로의 믹스 전환이 일어나고, 소버린 유입이 상업 롤오프(Globalstar 2027년 감소, Lightspeed 2029년 소진)를 넘어선다"**가 검증 가능한 형태다. 이 문장의 성패는 ESCP-P 2단계(MEO, MDA 프라임) 수주 규모와 시점에 달려 있다.

---

## 1. 회사 스냅샷

| 항목 | 수치 | 출처 |
|---|---|---|
| FY2025 매출 | 1,633.2M (+51.2%) | [1차] |
| FY2025 조정 EBITDA | 323.9M (마진 19.8%) | [1차] |
| FY2025 매출총이익률 | 25.1% | [1차] |
| 2026 가이던스(11/5 상향) | 매출 1.90–1.95B, 조정 EBITDA 355–375M, 마진 18–20%, capex 225–275M, FCF 중립~음수 | [1차] |
| 수주잔고(2026-09-30) | 3,949.1M (전년 동기 4,392.8M) | [1차] |
| 파이프라인 | "C$40B", 그중 C$10B가 다운셀렉트·후속 기회 | [1차] |
| 현금 / 순현금(2026-09-30) | 2,153.8M / 1,328.0M (인수 대금 집행 전) | [1차] |
| 인력 | 4,000명 이상, 엔지니어 약 2,000명, 노조 조직률 약 55% | [1차] |
| 상위 10개 고객 매출 비중 | 87.2% (FY2025) | [1차] |
| 해외(비캐나다) 매출 비중 | 37.4% (FY2025) | [1차] |
| 주식 수 | 2025년 말 126.3M → 2026 3Q 가중평균 158.8M | [1차] |
| 주가 | NYSE 약 US$29–31, TSX 약 C$40–44 (11/10–13) | [2차] |

연혁: 1969년 설립 계보 → Maxar 산하 → 2020년 캐나다 PE 컨소시엄이 인수(Neptune Acquisition Holdings) → 2021-04 TSX IPO(C$14.00) → 2024-05 MDA Space로 사명 변경 → 2026-03 NYSE 상장(US$30.50, 약 US$300M) → 2026-07 bought deal(US$35.60 × 23M주, 약 US$819M) → 2026-08 선순위 무담보채 C$600M(6.50%, 2033 만기 **[2차]**).

---

## 2. BM 해부

### 2.1 세 사업부 한눈에

| | Satellite Systems | Robotics & Space Operations | Geointelligence |
|---|---|---|---|
| FY2025 매출 | 1,109.5M (68%) | 309.3M (19%) | 214.4M (13%) |
| FY2025 성장률 | +85.5% | +10.5% | +6.1% |
| 9M 2026 매출 | 1,007.5M (+36.5%) | 271.0M (+11.2%) | 182.3M (+19.6%) |
| 파는 것 | 위성 완제품(프라임), 디지털 페이로드, 안테나, ASIC | 우주 로봇팔, 센서, 관제·운영 서비스 | SAR 영상 데이터, 지상국, 분석, 국방 ISR |
| 돈 버는 방식 | 고정가 제조 계약, 진행률 인식, 마일스톤 선수금 | 정부(CSA) 장기 개발 + 15년 운영 서비스 | 자기 위성 데이터 판매 + 정부 미션 계약 |
| 핵심 고객 | Telesat, Globalstar, Airbus, Thales Alenia, 미국 프라임 | 캐나다우주청(CSA), NASA, Starlab | 캐나다 정부·국방, 각국 정보기관 |
| 성격 | 성장 엔진, 변동성 큼 | 안정적, 정책 의존 | 반복 매출, 소규모 |

세그먼트별 이익은 공시하지 않는다. 전사 매출총이익률 25%, 조정 EBITDA 마진 19–20%만 알 수 있다.

### 2.2 Satellite Systems — 회사의 본체

**두 가지 역할을 동시에 한다. 이 구분이 투자포인트의 핵심이다.**

- **프라임(완성 위성 제조)**: 고객의 군집위성 전체를 설계·제작·시험해 납품한다. Telesat Lightspeed, Globalstar가 여기에 해당한다.
- **머천트 서브시스템 공급자**: 다른 프라임이 만드는 위성에 안테나·디지털 페이로드를 납품한다. OneWeb(Airbus 경유), IRIS²(Thales Alenia 경유), 미 SDA Tranche 1(L3Harris 경유), Iridium NEXT, O3b mPower, Mitsubishi Electric 방위통신위성. AIF상 고객 목록에 Airbus, Thales Alenia, Lockheed, Northrop, Boeing, L3Harris, OHB, York, Rocket Lab이 모두 있다. 즉 **경쟁사가 곧 고객**이다.

**제품: MDA AURORA.** 소프트웨어 정의 디지털 위성 제품군이다. 궤도상에서 빔·주파수·용량을 재구성할 수 있는 디지털 빔포밍 페이로드가 핵심이고, LEO·MEO, 광대역·D2D 양쪽에 적용된다. 2026-09에 항재밍·GPS 스푸핑 저항·보호 파형을 넣은 군용판 **AURORA BLACK**을, 2026-04에 우주자산 방호용 플랫폼 **MDA MIDNIGHT**를 내놨다.

**수직통합: SatixFy 인수(2025-07, 총 대가 C$448.3M).** 빔포밍·모뎀용 우주급 ASIC을 사내화했다. 회사 표현으로는 "실리콘 칩 수준까지" 통합. 양날의 검이다. Telesat은 2026-03에 Lightspeed 서비스 개시 지연 사유로 온보드 프로세서용 ASIC 지연을 들었고 **[2차]**, 그 칩의 공급자가 이제 MDA 자신이다.

**생산능력.** 몬트리올 인근 Sainte-Anne-de-Bellevue에 185,000 sq ft 증설, 2026년 가동 시작. 회사 표현은 "월 수십 기의 위성 및 서브시스템". 구체적 대수는 공시하지 않는다.

**계약 구조와 현금 사이클 [1차].**
- 계약 대부분이 **확정 고정가(firm fixed price)**. 원가 초과는 MDA가 부담하고, 납기 지연 시 지체상금(liquidated damages)이 붙는다.
- 대부분의 계약은 고객이 **언제든 편의 해지(termination for convenience)** 가능. 해지 시 회수액은 "보장되지 않는다"고 스스로 적고 있다.
- 매출은 진행률로 인식하고, 현금은 마일스톤 선수금으로 먼저 들어온다. 그래서 수주 직후 영업현금흐름이 급증하고(2024년 OCF 812.7M), 생산 구간에서는 운전자본을 소모한다(2026년 9개월 OCF 73.7M, FCF −116.2M **[추정]**). 계약부채는 2025년 말 798.9M → 2026-09 601.7M으로 줄었다.

**주요 계약.**

| 계약 | 규모 | 대수 | 대당 단가 [추정] | 상태 |
|---|---|---|---|---|
| Telesat Lightspeed | 약 C$2.4B | 198기 (+옵션 100기) | 약 C$12M | 잔고 약 C$1.4B, 2027–2029 인식. 패스파인더 2기 지연 |
| Lightspeed 확장(ESCP-P 군용 Ka) | C$474M (2026-08) | +27기 | 약 C$17.6M | 3Q26 수주 |
| Globalstar 확장(2022) | US$327M | 17기 (+옵션 9기) | 약 US$19M | 지연, 지체상금 분쟁 소지. 2026년 발사 시작 |
| Globalstar 차세대 | 약 C$1.1B | 50기 이상 | 약 C$20M | 2027년부터 매출 감소 |
| EchoStar D2D | US$1.3B (잠재 US$2.5B) | 100기 이상 | 약 US$13M | **2025-09 해지**. 해지 대금 전액 수령(금액 비공개) |
| Airbus/OneWeb 안테나 | 비공개 (2026-04) | 안테나 1,320개 | — | 재수주 |
| IRIS² Layer 1 | 비공개 (2026-10) | 66기분 안테나·디지털 컨트롤러 | — | Thales Alenia 하도급 |
| Mitsubishi Electric | 비공개 (2026-06) | 디지털 페이로드·안테나 | — | 일본 방위통신위성 |

### 2.3 Robotics & Space Operations — 정부가 주는 연금

- **Canadarm3**: 잠재 총매출 약 C$1.8B(15년 운영 서비스 포함). Phase B C$269M(2022), Phase C/D C$1.0B(2024). 계약 상대방은 NASA가 아니라 **캐나다우주청(CSA)**이다.
- **Gateway 중단**: NASA가 2026-03-24에 Gateway를 중단하고 달 표면 기지로 방향을 틀었다. 발표 당일 주가 −11% **[2차]**. 계약 금액은 변동 없고, CSA가 Canadarm3를 달 표면·LEO 임무로 전용하는 계획을 공식화했다. 3Q26 콜에서 CSA가 달 기지 로봇 계획에 대한 유상 과업을 발주했다고 밝혔다. 다만 미세중력용 팔을 먼지 환경에 쓰는 기술적 의문은 남아 있다.
- **ISS 로봇 운영**: C$250M, 2025–2030.
- **MDA SKYMAKER**: Canadarm 파생 상업용 로봇 제품군. Starlab(지분 보유)이 대표 고객. 파이프라인 C$3B 이상이라고 주장하나 상업 우주정거장 시장 자체가 초기다.
- 2026년 분기 매출 약 80M 수준에서 횡보. 성장 엔진이 아니라 안정 기반이다.

### 2.4 Geointelligence — 작지만 유일한 반복 매출

- **데이터 사업**: RADARSAT-2(2007년 발사, 설계수명 초과)의 상업 배급권을 갖고 SAR 영상을 판다. 최대 시장은 해양 감시.
- **MDA CHORUS**: 후속 자체 군집. C-밴드 SAR(700km 관측폭) 1기 + ICEYE 제작 X-밴드 SAR(서브미터) 1기가 60분 간격으로 같은 궤도를 돈다. 2026년 말 Falcon 9 발사, 2027년 초 상업 운영 목표. 사전 약정 41건 **[2차]**. 투자는 "대부분 완료".
- **정부 미션**: RADARSAT+ 이니셔티브(C$1.012B, 15년). 2026-06에 CHORUS 기반 RCM 보충위성 본계약 C$688M **[2차]**.
- **CLS 인수(2026-07 발표)**: 프랑스 CLS 지분 70%를 €567M에 인수, CNES가 30% 유지. CLS는 2025년 매출 €203M, 19개국 운영 **[2차]**. 종결되면 전사 반복 매출 비중이 30% 이상으로 두 배가 된다는 것이 회사 주장이다. 종결은 2026년 말~2027년 1분기 예상.
- **49North(2026-02 출범)**: 우주 외 국방 사업(C4ISR, 해군 함정 탑재 무인기 ISTAR, General Atomics와의 RPAS)을 분리한 조직.

### 2.5 손익과 현금의 구조적 특징

- **마진은 올라가지 않고 있다.** 매출은 2년간 약 1.8배가 됐지만 조정 EBITDA 마진은 20.1%(2024) → 19.8%(2025) → 19.4%(9M26)로 소폭 하락. 고정가 대형 제조 프로그램 비중이 커지는 믹스 효과와 SG&A 투자(9M26 SG&A 114.4M, 전년 81.0M) 때문이다. CFO는 이 추세가 2027년에도 이어진다고 했다. **규모의 경제가 마진으로 나타나는 사업이 아직 아니다.**
- **자본집약도가 높다.** 5년간 C$1.25B를 재투자했다(CFO 발언). 2026년 capex 225–275M은 매출의 약 13%.
- **주당 가치 희석.** 2026년 두 차례 증자로 주식 수가 약 26% 늘었다. 3Q26 조정 순이익 +26%인데 조정 EPS는 +0.7%다.

---

## 3. 밸류체인에서의 위치

```
[부품·칩] → [서브시스템: 안테나·페이로드] → [위성 프라임(버스+통합)] → [발사] → [운영자] → [서비스·데이터]
  SatixFy ASIC      MDA (머천트)                MDA (프라임)            SpaceX     Telesat      MDA Geointelligence
  (MDA 내재화)      ↳ Airbus·TAS·L3Harris·       ↳ Lightspeed·                    Globalstar   (RADARSAT-2, CHORUS,
                      Mitsubishi에 납품            Globalstar                      (→Amazon)    CLS)
```

- **MDA가 없는 곳**: 발사(SpaceX 의존, Maritime Launch Services에 C$10M 소수 지분만 보유), 통신 위성 운영.
- **SpaceX·Amazon과의 관계**: 이 둘은 위성을 자체 제작하는 캡티브다. MDA의 시장은 정의상 "캡티브가 아닌 나머지"다. MDA는 SpaceX와 위성 제조에서 직접 경쟁하지 않는다. **MDA의 고객이 SpaceX·Amazon과 경쟁하고, 고객이 지면 MDA의 주문이 사라진다.** 이것이 EchoStar에서 일어난 일이다.
- **경쟁사(AIF 명시)**: Airbus, Thales Alenia Space, Lockheed Martin, Northrop Grumman, L3Harris, Lanteris(구 Maxar Space Systems), Rocket Lab, York. 여기에 유럽 3사 통합(Airbus·Thales·Leonardo, 2025-10 MOU)과 미국 신생 버스 업체(Apex, K2, York 상장)가 압력을 더한다.
- **MDA의 차별점으로 주장되는 것**: 디지털 페이로드 기술, 고객 요구에 따라 부품 구성을 미국산 위주 또는 유럽산 위주로 맞출 수 있는 설계(CEO 발언), 프라임들과 경쟁하지 않는 독립 공급자 지위, 캐나다 유일의 우주 프라임이라는 지위.

---

## 4. 사업 방향성

경영진이 2026년에 실제로 한 행동을 순서대로 놓으면 방향이 보인다.

1. **캐나다 국방·우주 국가 챔피언 지위 굳히기.** ESCP-P 전략적 파트너십(2025-12), 49North 출범(2026-02), RCM 보충위성, 우주감시 관측소, 캐나다 벤처 투자 프로그램 LaunchPad.
2. **군용 제품 라인 신설.** MIDNIGHT(4월), AURORA BLACK(9월).
3. **미국 시장은 인수로 들어간다.** Blue Canyon Technologies를 RTX로부터 US$620M에 인수(2026-06 발표, 연내 종결 목표, CFIUS·HSR 심사 대상). "MDA Space USA"로 만들어 미국 기밀 프로그램 입찰 자격을 확보하려는 것. 회사는 파이프라인 US$3.5B가 추가된다고 주장. 미 미사일방어청 SHIELD IDIQ 자격도 2026-01 확보.
4. **유럽 시장도 인수로 들어간다.** CLS(프랑스, CNES 30% 잔류)와 IRIS² 하도급 진입.
5. **아시아는 파트너십.** 한화시스템과 K-LEO MOU(2026-01), Mitsubishi Electric 수주(2026-06).
6. **이를 위해 2026년에만 약 C$2.1B를 조달했다**(증자 2회 + 사채).

요약하면 **"상업 군집위성 프라임"에서 "동맹국 다수에 현지 거점을 둔 국방·우주 공급자"로의 전환**이다. 인수 두 건은 2026년 기준 매출 약 C$700M을 더한다(CFO). 2027년 기존 사업은 "견조한 두 자릿수 성장"이라는 정성 가이던스만 나왔고, 정식 가이던스는 2027-03에 나온다.

---

## 5. 투자포인트 논증 검증

검증 대상 논증: (가) SpaceX·Amazon 밖 위성 수요가 구조적으로 존재하고 커진다 → (나) 그 동력은 소버린이다(상업은 항복 중) → (다) 그 시장에서 MDA 점유율이 커진다.

### 5.1 "상업은 항복 중" — 성립. 증거가 MDA 장부 안에 있다

| 사건 | 내용 |
|---|---|
| EchoStar → SpaceX (2025-09) | AWS-4·H블록 스펙트럼을 약 US$17B에 SpaceX에 매각, MDA와의 US$1.3B 계약 해지. 계약 발표 5주 만. MDA 주가 하루 −25~30% |
| Globalstar → Amazon (2026-04) | 약 US$11.6B 인수. FCC 승인(2026-10), 2027 종결 예정. Amazon은 MDA가 제작 중인 위성을 운영하겠다고 밝혔으나, 2028년부터 **자체 D2D 시스템**을 배치할 계획 |
| Telesat | 3Q26 GEO 매출 −20%, 조정 EBITDA −74%. GEO 부채 약 C$3.1B가 2026-12~2027-10 만기인데 상환 재원 부족을 인정 **[2차]** |
| 업계 구조 | SES-Intelsat, Viasat-Inmarsat, Eutelsat-OneWeb 통합. Starlink 가입자 1,000만 돌파(2026-02), 위성 10,000기 이상 |

주의할 점: 이 전제가 강할수록 MDA의 현재 매출 기반(상업 72%)에는 악재다. Globalstar 차세대 매출은 2027년부터 줄고, Amazon이 자체 D2D로 가면 후속 주문은 기대하기 어렵다.

### 5.2 "소버린이 구조적으로 커진다" — 성립

- 전 세계 정부 우주예산 2025년 US$137.4B, 그중 국방이 54%(US$73.5B) (Novaspace, AIF 인용 **[1차]**).
- 우주 국방 예산 US$74B → 2028년 US$121B 전망, 55개국 이상이 우주 국방 예산 보유(Novaspace 2026-09 **[2차]**).
- **유럽**: IRIS²가 290기·€10.55B에서 348기·€15.6B로 확대(2026-08), 66기 군사·안보 LEO 계층 추가. 독일은 2030년까지 군사우주에 €35B, SATCOMBw 4단계는 100~200기 규모 **[2차]**.
- **캐나다**: 2025-26 회계연도에 GDP 2% 달성, 2035년 핵심 국방 3.5% 경로. 국방투자청(DIA) 신설. ESCP-P 1단계로 Telesat에 C$2.3B 발주.
- **아시아**: 한국 K-LEO, 일본 차세대 방위통신위성.
- **수요의 성격**: Telesat CEO는 우크라이나에서의 Starlink·Starshield 서비스 차질이 "여러 정부를 움직였다"고 했고, Iridium CEO는 소버린 수요가 "일시적 유행이 아니다"라고 했다 **[2차]**.

**이 전제에서 꼭 짚어야 할 것**: Telesat Lightspeed는 회계상 상업 매출이지만 실질은 준(準)소버린이다. 캐나다 연방·퀘벡 정부 대출로 자금을 조달했고(연방 C$2.14B, 퀘벡 C$400M — 2024년 발표 기준, 재확인 필요), 이제 ESCP-P 군 수요의 플랫폼이 됐다. 즉 MDA의 최대 계약은 이미 "정부가 살려 놓은 상업 군집"이다. 이는 투자포인트에 유리한 사실이다. 소버린 논리가 MDA 매출의 가장 큰 덩어리에 이미 작동하고 있다는 뜻이기 때문이다.

### 5.3 "MDA 점유율이 커진다" — 현재 증거로는 입증 부족. 여기가 승부처

**불리한 사실**
- **수주잔고가 늘지 않는다.** 4.39B(2024 말) → 4.01B(2025 말) → 3.95B(2026-09). 경영진 스스로 "10분기 평균 4B 이상이 새 기준선"이라고 표현한다. 매출이 1.8배가 되는 동안 잔고는 제자리였으므로 잔고/매출 배수는 약 4배에서 약 2배로 떨어졌다 **[추정]**.
- **Book-to-bill 1 미만.** 2025년 0.73배(수주 1,200.1M / 매출 1,633.2M), 2026년 9개월 0.96배(1,397.0M / 1,460.8M) **[추정]**. 콜에서 언급된 "총 수주 약 1.6B"와 릴리스 수치 1,397M 사이에 차이가 있어 원인 확인이 필요하다.
- **소버린 프로그램은 자국 산업으로 간다.** IRIS²의 프라임은 Airbus·Thales Alenia·OHB이고 MDA는 Layer 1의 안테나 하도급이다. CEO도 전체를 수주할 기대는 없고 유럽 프로그램에는 "지정학적·현지 조달 요소가 높다"고 인정했다. 독일 군집위성은 OHB-Rheinmetall 합작이 입찰했다.
- **파이프라인 C$40B는 구성이 공개되지 않았다.** 국방/상업, 캐나다/해외 구분이 없다. 약 C$30B가 위성시스템이라는 2차 요약만 있다.

**유리한 사실**
- **캐나다 안에서는 사실상 독점 프라임이다.** ESCP-P 2단계(MEO, UHF·X밴드)에서 MDA가 "엔드투엔드 미션 인도 책임" 프라임으로 지정됐고 협상 중이다. CEO는 "수십억 달러대 프로그램이 덩어리로 들어온다"고 표현했다. 금액과 시점은 미공개.
- **해외 소버린 프로그램에 부품사로 연속 진입 중.** 2026년 한 해에 IRIS²(유럽), Mitsubishi(일본), OneWeb 확장(프랑스·영국 정부가 주주), K-LEO MOU(한국).
- **인수로 "자국 산업" 지위를 사고 있다.** BCT는 미국 프라임 자격, CLS는 프랑스 거점. 소버린 조달의 현지화 장벽을 M&A로 넘으려는 것.

### 5.4 논증을 이렇게 재구성하길 권한다

원안의 "점유율 상승"은 분모(비캡티브 위성 제조 시장 규모)를 구하기 어렵고 현재 데이터로는 반박당하기 쉽다. 아래 구조가 방어 가능하다.

> **① 비캡티브 위성 수요의 주인이 상업 운영자에서 정부로 바뀌고 있다** (5.1 + 5.2)
> **② 정부 수요는 SpaceX·Amazon이 구조적으로 가져가기 어렵다** — 통제권과 자국 산업 육성이 구매 목적 자체이기 때문
> **③ MDA는 이 수요에 세 경로로 접근한다**
> 　(a) 캐나다: 국가 챔피언 프라임 (ESCP-P, RADARSAT+, Canadarm3)
> 　(b) 동맹국: 어느 나라 프라임에도 납품할 수 있는 디지털 페이로드·안테나 머천트 (IRIS², 일본, OneWeb)
> 　(c) 미국·프랑스: 인수로 현지 자격 확보 (BCT, CLS)
> **④ 그 결과 2027–2029년에 소버린 유입이 상업 롤오프를 넘어 잔고가 다시 늘어난다**

④가 숫자로 반증 가능한 핵심 명제다. "점유율" 대신 **위성 1기당 MDA 콘텐츠 금액**과 **정부 매출 비중(현재 28%)의 상승**을 지표로 쓰면 추적이 가능하다.

### 5.5 이 논증이 틀렸다고 판정할 조건

- ESCP-P 2단계 본계약이 2027년 상반기까지 나오지 않거나 규모가 C$1B에 못 미침
- 2027년 말 수주잔고가 인수 효과 제외 기준 C$4B 아래에 머묾
- Lightspeed 패스파인더(2027-06 발사 예정)가 추가 지연되거나 Telesat의 GEO 부채 재조정이 Lightspeed 지급에 영향
- 독일·K-LEO 등 해외 소버린 군집에서 2027년까지 수주 없음
- BCT 인수가 CFIUS에서 지연·무산

---

## 6. 리스크

| 리스크 | 내용 |
|---|---|
| 고객 집중 | 상위 10개 고객 87.2%. Lightspeed가 잔고의 약 35% [추정] |
| Telesat 신용·일정 | 2026-10-29 Telesat이 "프라임 MDA의 조립·소프트웨어 개발 문제"로 패스파인더가 2026-12 → 2027-06으로 밀렸다고 밝힘. MDA는 재무 영향 없다고 답하고 원인은 밝히지 않음. Telesat GEO 부채 C$3.1B 만기 도래. Lightspeed 법인이 GEO 부채와 분리돼 있는지 확인 필요 |
| 편의 해지 | 대부분 계약이 언제든 해지 가능. EchoStar가 선례 |
| 고정가 실행 | Globalstar 17기 지연으로 지체상금 청구 소지. CHORUS도 공급사 지연 |
| 마진 정체 | 규모가 커져도 EBITDA 마진 19%대. 4Q26 내재 마진 약 18% |
| 현금흐름 | 2026년 FCF 중립~음수. 2027년에도 Lightspeed가 운전자본 소모 |
| 인수 통합·희석 | 1년에 SatixFy 포함 3건, 약 C$2.2B. 주식 수 +26%. 인수 후 순부채/EBITDA 목표 1.5–2.5배 [2차] |
| 정책 의존 | Gateway 중단처럼 타국 정부 결정에 노출. 캐나다 국방 조달은 속도가 느리고 덩어리로 옴 |
| 발사 의존 | CHORUS·고객 위성 모두 Falcon 9. 3Q 콜에서 Falcon 9 퇴역 우려 질문이 나왔고 CEO는 "지켜볼 지점" |
| 소송 | EchoStar 공시·내부자 매도 관련 집단소송(2025-11 제기, 청구액 합계 약 C$340M). 회사는 근거 없다는 입장 |
| 단일 위성 | RADARSAT-2는 설계수명 초과. CHORUS 가동 전 고장 시 Geointelligence 타격 |

---

## 7. 밸류에이션 스냅샷 [추정, 거친 계산]

- 시가총액: 약 159M주 × C$40–44 ≈ **C$6.4–7.0B**
- 단독 EV: 시총 − 순현금 1.33B ≈ C$5.1–5.7B → 2026E 조정 EBITDA 365M(가이던스 중간값) 대비 **약 14–16배**
- 인수 반영 프로포마: BCT 약 C$0.87B + CLS 약 C$0.9B(+ CLS 기존 부채 최대 €198M) 지급 시 순부채 약 C$0.5–0.8B, EV 약 C$7–7.8B. 프로포마 EBITDA 약 C$500M(365M + 700M × 약 19%, CLS 100% 연결 기준) 대비 **약 14–16배**. CLS 30% 비지배지분은 별도 차감 필요
- 선행 P/E 약 29배 **[2차]**
- 컨센서스 목표가: NYSE 기준 US$42–50 범위. 3Q 실적 후 JPMorgan US$50→44, Jefferies US$49→45로 하향 **[2차]**
- 주가는 7월 증자 직전 TSX C$54.90에서 현재 C$40대 초반으로 내려왔고, NYSE 주가는 3월 상장가(US$30.50)와 7월 증자가(US$35.60) 아래다

---

## 8. 확인하지 못한 것 · 추가로 봐야 할 것

1. **고객별 매출 비중**(Telesat, Globalstar, 캐나다 정부 각각) — AIF에 없음. 감사받은 재무제표 주석(주요 고객 주석)에서 확인
2. **상업 72% / 정부 28%, 캐나다 63%** — 연차보고서 검색 요약에서만 확인. 원문 페이지 대조 필요
3. **세그먼트별 수주잔고·이익** — 미공시
4. **파이프라인 C$40B의 구성** — 미공시. IR에 문의하거나 투자자 프레젠테이션 원본 확인
5. **ESCP-P 2단계 예상 규모와 전체 프로그램 예산**
6. **비캡티브 위성 제조 시장 규모**(Novaspace 유료 보고서) — 점유율 논증을 굳이 하려면 필수
7. **Lightspeed 자금 조달 구조**와 Telesat GEO 부채 재조정이 MDA 수금에 미치는 영향
8. **BCT의 실제 매출·이익**(RTX 공시에 분리 수치 없음), CLS의 EBITDA 절대액
9. **수주 수치 불일치**: 3Q26 릴리스 9개월 수주 1,397.0M vs 콜 발언 "총 수주 약 1.6B"; Lightspeed 확장 C$474M 대비 3Q 수주 444.2M
10. **Amazon의 Globalstar 인수 후 MDA 계약 처리**(옵션 9기, 후속 물량)
11. 3Q26 콜 전문은 Motley Fool 전사본 기준이며 일부 문장이 깨져 있음. 인용 전 음성 대조 권장

---

## 9. 출처

**회사 1차 자료**
- [3Q 2026 실적 릴리스 (2026-11-05)](https://mda-en.investorroom.com/2026-11-05-MDA-SPACE-REPORTS-THIRD-QUARTER-2026-RESULTS)
- [4Q·FY2025 실적 릴리스 (2026-03-04)](https://mda-en.investorroom.com/2026-03-04-MDA-SPACE-REPORTS-FOURTH-QUARTER-AND-FISCAL-2025-RESULTS)
- [FY2025 MD&A (SEC F-10 Ex. 4.3)](https://www.sec.gov/Archives/edgar/data/1857047/000110465926025809/tm266080d2_ex4-3.htm)
- [FY2025 Annual Information Form (SEC F-10 Ex. 4.1)](https://www.sec.gov/Archives/edgar/data/1857047/000110465926025809/tm266080d2_ex4-1.htm)
- [FY2025 AIF PDF](https://mda-en.investorroom.com/image/MDA_Space_Ltd_Q4_2025_AIF.pdf) · [2025 Annual Report PDF](https://mda-en.investorroom.com/image/MDA_Space_Ltd_Q4_2025_Annual_Report.pdf)
- [EchoStar 계약 관련 공시 (2025-09-08)](https://mda-en.investorroom.com/2025-09-08-MDA-SPACE-PROVIDES-UPDATE-ON-ECHOSTAR-CONTRACT)
- [Lightspeed 확장 C$474M 수주 (2026-08-04)](https://mda-en.investorroom.com/2026-08-04-MDA-SPACE-AWARDED-474-MILLION-TO-EXPAND-THE-TELESAT-LIGHTSPEED-LEO-CONSTELLATION)
- [한화 K-LEO MOU (2026-01-26)](https://mda-en.investorroom.com/2026-01-26-MDA-SPACE-AND-HANWHA-SIGN-MOU-TO-PURSUE-KOREAN-MILITARY-CONSTELLATION-PROGRAM)
- [Airbus/OneWeb 안테나 재수주](https://mda.space/article/mda-space-contracted-by-airbus-for-repeat-order-of-antennas-for-oneweb-constellation-extension) · [MDA CHORUS](https://mda.space/chorus)
- [NYSE 상장 관련 SEC 6-K](https://www.sec.gov/Archives/edgar/data/1857047/000110465926029598/tm266080d11_ex99-1.htm) · [7월 증자 Prospectus Supplement](https://www.sec.gov/Archives/edgar/data/0001857047/000110465926082327/tm2619705-6_suppl.htm)
- [BCT 인수 6-K](https://www.sec.gov/Archives/edgar/data/0001857047/000110465926075950/tm2618399d1_ex99-1.htm)

**컨퍼런스콜**
- [3Q 2026 콜 전사본 (Motley Fool)](https://www.fool.com/earnings/call-transcripts/2026/11/05/mda-space-mda-q3-2026-earnings-call-transcript/)
- [3Q 2026 콜 요약 (Yahoo Finance)](https://finance.yahoo.com/markets/stocks/articles/mda-space-ltd-mda-q3-091035485.html)

**정부**
- [캐나다 국방투자청: ESCP-P 계약 발표 (2026-08)](https://www.canada.ca/en/defence-investment-agency/news/2026/08/the-government-of-canada-awards-a-military-communications-contract-to-support-arctic-sovereignty-and-national-security.html)
- [캐나다 Budget 2026 Chapter 5](https://budget.canada.ca/2026/report-rapport/chap5-en.html) · [PBO 국방지출 프라이머](https://www.pbo-dpb.ca/en/publications/NT-2627-013-S--canada-defence-spending-commitments-primer--engagements-canada-matiere-depenses-defense-guide-introduction)

**고객·산업**
- [Amazon의 Globalstar 인수 발표](https://www.aboutamazon.com/news/company-news/amazon-globalstar-apple) · [Via Satellite: Amazon D2D 진입](https://www.satellitetoday.com/connectivity/2026/04/14/amazon-enters-d2d-market-with-globalstar-acquisition-and-system-plans/) · [FCC 승인](https://www.satellitetoday.com/connectivity/2026/10/27/amazon-secures-fcc-approval-for-globalstar-acquisition/)
- [SpaceQ: EchoStar 계약 해지](https://spaceq.ca/echostar-cancels-1-8b-contract-with-mda-space/) · [BNN Bloomberg: CEO 발언](https://www.bnnbloomberg.ca/business/company-news/2025/09/08/mda-space-caught-off-guard-by-echostars-deal-cancellation-ceo-says/)
- [Via Satellite: Telesat Lightspeed 2028년 중반으로 지연 (2026-10-29)](https://www.satellitetoday.com/finance/2026/10/29/telesat-delays-lightspeed-service-entry-to-mid-2028-goldberg-addresses-launch-crunch-and-sovereign-demand/) · [SpaceNews](https://spacenews.com/global-telesat-lightspeed-service-delayed-to-mid-2028/) · [SatNews](https://satnews.com/2026/10/31/telesat-delays-lightspeed-constellation-service-to-mid-2028-following-pathfinder-software-delays/) · [Via Satellite (2026-03, ASIC 지연)](https://www.satellitetoday.com/finance/2026/03/17/telesats-lightspeed-service-launch-slips-to-2028/)
- [Space Intel Report: MDA의 Lightspeed 지연 해명과 미·유럽 군수 전략](https://www.spaceintelreport.com/mda-space-on-telesat-lightspeed-delay-and-how-its-positioning-itself-to-win-us-and-european-military-satellite-business/)
- [SpaceQ: ESCP-P C$2.3B](https://spaceq.ca/defence-investment-agency-awards-telesat-and-mda-space-a-major-arctic-security-connectivity-contract-initially-valued-at-2-3-billion/) · [Via Satellite: ESCP-P용 Lightspeed 확장](https://www.satellitetoday.com/government-military/2026/08/04/telesat-expands-lightspeed-constellation-for-arctic-military-satcom-program/)
- [Payload: The State of Satcom 2026](https://payloadspace.com/the-state-of-satcom-2026/) · [SatNews: SpaceX IPO와 "two-stack" 시장](https://satnews.com/2026/04/07/what-the-spacex-ipo-changes-for-every-satellite-operator/)
- [Space Economy Institute: IRIS² 계약](https://spaceeconomyinstitute.com/2026/09/11/iris2-contracts-europe-sovereign-satellite-network/) · [SatNews: 독일 €35B](https://satnews.com/2026/02/28/germany-commits-e35-billion-to-leo-resilience-and-non-kinetic-deterrence/)
- [Defense News: Novaspace 우주 ISR 전망](https://www.defensenews.com/space/2026/09/15/space-based-isr-launches-to-grow-fourfold-in-next-decade-novaspace-says/?nb=1) · [Breaking Defense: Novaspace 위성 시장 전망](https://breakingdefense.com/2025/10/defense-to-anchor-exploding-satellite-market-over-next-decade-novaspace/)
- [Aviation Week: Canadarm3 달 탐사로 전환](https://aviationweek.com/space/space-exploration/canada-pivots-canadarm3-lunar-exploration) · [Globe and Mail: Gateway 중단](https://www.theglobeandmail.com/canada/science/article-nasa-drops-lunar-space-station-puts-canadian-robotic-arm-on-uncertain/) · [Payload: Canadarm3 전용](https://payloadspace.com/mda-space-will-repurpose-canadarm3-for-lunar-surface/)
- [SpaceQ: RCM 보충위성 C$688M](https://spaceq.ca/mda-space-moves-to-build-phase-with-688m-radarsat-replenishment-satellite-contract-award/) · [SpaceQ: CHORUS 약정 41건](https://spaceq.ca/mda-space-reports-41-commitments-for-chorus-ahead-of-launch/)
- [GovConWire: BCT 인수 US$620M](https://www.govconwire.com/articles/mda-space-blue-canyon-technologies) · [Yahoo Finance: CLS 인수 €567M](https://finance.yahoo.com/technology/ai/articles/mda-space-bets-567m-cls-060157230.html) · [SpaceQ: C$600M 사채](https://spaceq.ca/mda-space-issues-600-million-in-senior-notes-to-finance-u-s-expansion/)
- [Via Satellite: FY2025 실적](https://www.satellitetoday.com/finance/2026/03/04/mda-space-reports-record-revenue-again-in-2025-driven-by-satellite-manufacturing-progress) · [SatNews: C$40B 파이프라인](https://satnews.com/2026/03/04/mda-space-delivers-record-1-6-billion-revenue-in-2025-unveils-40-billion-opportunity-pipeline/)
- [Flight Plan: Airbus·Leonardo·Thales 우주사업 통합](https://flightplan.forecastinternational.com/2025/10/24/airbus-leonardo-thales-join-forces-to-reshape-european-space-landscape/) · [SatNews: Apex 자금조달](https://satnews.com/2026/10/24/satellite-bus-maker-apex-in-talks-to-raise-500m-at-4b-valuation/)

**주가·컨센서스**
- [StockAnalysis (NYSE)](https://stockanalysis.com/stocks/mda/) · [StockAnalysis (TSX)](https://stockanalysis.com/quote/tsx/MDA/) · [MarketBeat: JPMorgan 목표가 하향](https://www.marketbeat.com/instant-alerts/analyst-mda-space-nyse-mda-stock-price-target-cut-by-jpmorgan-chase-co-2026-11-10/)
