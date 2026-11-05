# 05. TransMedics (TMDX) 비즈니스 모델 정리 (2026-11-05)

- 기준일: 2026-11-05 / 주가: $72.76 (2026-11-04 종가)
- 원자료: FY2025 10-K, 2Q26 10-Q, 2Q26 8-K. (파생)은 공시 숫자로 내가 계산한 값
- 3Q26 실적은 11/5 장 마감 후 발표 예정이라 아직 반영하지 않았다

## 1. 한 줄 요약

**장기를 얼음 상자 대신 "살아 있는 상태"로 옮기는 기계(OCS)를 팔고, 그 기계를 들고 외과의사와 전용기까지 붙여서 장기를 배달해 주는 서비스(NOP)로 돈을 번다.** 이식 1건마다 일회용 키트와 배달비가 함께 찍히는 건당 과금 구조다.

## 2. 풀려는 문제

- 기존 방식은 냉장 보관이다. 기증자에게서 꺼낸 장기를 얼음 상자에 넣고 시간과 싸운다. 일반적으로 심장은 4~6시간, 폐는 6~8시간, 간은 8~12시간 안에 이식해야 한다.
- 그래서 **멀리 있거나 상태가 애매한 장기는 버려진다.** 특히 심장이 멈춘 뒤 기증된 장기(DCD)가 그렇다. 10-K는 냉장 보관으로는 "DCD 폐와 심장은 거의 쓰이지 않는다"고 적고 있다.
- OCS는 장기에 체온의 혈액과 산소·영양분을 계속 흘려보낸다. 심장은 뛰고, 폐는 숨 쉬고, 간은 담즙을 만든다. 이동 중에 장기 상태를 측정할 수 있고, 시간 제약이 늘어나며, 버려지던 장기를 쓸 수 있게 된다.

## 3. 돈 버는 방법: 두 개의 매출

| 구분 | 무엇을 파나 | FY2025 매출 | 비중 | 매출총이익률 (파생) |
|---|---|---|---|---|
| 제품 (Product) | 장기별 일회용 관류 세트·용액, OCS 콘솔 | $372.4M | 61.5% | 79.1% (2Q26 77.0%) |
| 서비스 (Service) | NOP: 장기 적출 외과의사, 임상 전문가, 전용기·지상 운송, 조율 | $233.1M | 38.5% | 29.3% (2Q26 35.0%) |
| 합계 | | $605.5M (+37%) | | 59.9% |

- **면도기와 면도날 구조:** 콘솔이 깔리면 이식할 때마다 새 일회용 세트가 필요하다. 10-K는 매출이 "매우 반복적"이라고 설명한다.
- **서비스가 성장 엔진:** 2Q26 서비스 매출은 +29%(제품은 +16%)다. 자체 항공기를 더 많이 띄울수록 서비스 마진이 오른다(2025 29% → 2Q26 35%).
- **건당 매출 (파생):** FY2025 매출 $605.5M을 미국 케이스 5,139건으로 나누면 **건당 약 $11.8만**이다(해외 매출 3% 포함). 제품 약 $7.2만, 서비스 약 $4.5만.
- **장기별 매출 (2Q26 미국 OCS 이식 매출 $183.6M):** 간 $148.0M (81%), 심장 $33.4M (18%), 폐 $2.3M (1%). **사실상 간 회사다.**

## 4. NOP: 이 회사의 진짜 해자

```
[기증자 병원]                                      [이식 병원]
   │  ① 이식센터가 TMDX에 "이 장기를 가져와 달라" 요청        ▲
   ▼                                                  │
 TMDX 외과의사·임상팀 출동 (자체 전용기 22대, 지상 운송)        │
   │  ② 현장에서 장기 적출 → OCS에 연결 (따뜻한 관류)          │
   └──────── ③ 전용기로 운송, 이동 중 장기 상태 모니터링 ───────┘
                          │
                ④ 이식센터에 청구 (일회용 세트 + 서비스·항공)
                          │
                ⑤ 이식센터는 "장기 확보 비용"으로 분류해 Medicare에서 별도 상환
```

- **예전에는** 병원이 기계를 사고, 자체 팀을 훈련시키고, 전세기를 따로 구해야 했다. 큰 병원만 쓸 수 있었다.
- **지금은** 병원이 "이 장기 주세요"라고만 하면 TMDX가 사람·기계·비행기를 다 보낸다. 10-K: "미국 출시 이후 OCS 판매는 주로 NOP를 통해 이뤄졌다." 직접 구매 모델은 해외 고객 전부와 미국 소수 고객만 쓴다.
- **항공 수직계열화:** 2023-08 Summit Aviation 인수 이후 고정익 항공기 22대를 직접 보유한다(2025년 말). 경쟁사는 기계는 만들 수 있어도 외과의사 팀과 전용기 네트워크를 단기간에 복제하기 어렵다.
- **고객:** 이식센터와 장기구득기관(OPO). 비행 비용도 고객이 낸다.

## 5. 누가 돈을 내나: 가격 저항이 약한 이유

- 미국 Medicare는 이식 수술비와 별도로 **"장기 확보 비용(organ acquisition cost)"을 원가 기준으로 따로 상환**한다. 이식센터가 매년 비용 보고서(Worksheet D-4)에 올리면 Medicare 몫을 돌려받는다.
- 10-K: OCS 콘솔·관류 세트·용액 비용은 **장기 확보 비용으로 분류돼 Medicare가 추가로 상환한다.** 미국 폐·심장·간 이식의 절반 가까이가 Medicare·Medicaid 대상이다.
- 의미: 병원 입장에서 TMDX 비용은 대부분 그대로 넘기는 비용이라 단가 저항이 약하다. **반대로 정부가 이 원가 상환 제도를 손보면 가장 큰 리스크가 된다.** HHS OIG는 2026년에 Medicare가 6년간 이식되지 않은 장기에 $380M을 더 냈다는 보고서를 냈다.

## 6. 경쟁 구도 (10-K 원문 기준)

| 경쟁사 | 무엇 | TMDX 대비 |
|---|---|---|
| OrganOx (2025-10 Terumo 인수) | 간 전용 따뜻한 관류 | 단일 장기. 물류 서비스 없음 |
| XVIVO Perfusion | 폐 전용 관류 | 단일 장기 |
| Paragonix (2024-09 Getinge 인수) | 냉장 보관 장치 | 싸지만 DCD·장거리에 약함 |
| NRP (체내 국소 관류) | 기증자 몸 안에서 장기를 재관류하는 수술 기법 | **가장 큰 잠재 대체재.** 기계 없이 DCD 장기를 살릴 수 있다 (10-K 리스크 항목에 언급) |

- TMDX가 내세우는 차별점: "FDA 승인을 받은 유일한 휴대형·다장기 따뜻한 관류 플랫폼"과 "장기 운송 전용 자체 항공기 100% 보유·운영".

## 7. 성장 경로

| 경로 | 현재 | 목표·이벤트 |
|---|---|---|
| 미국 케이스 | 2025년 5,139건 (+38%) | **2028년 미국 NOP 이식 10,000건** (회사 목표, 신장 제외) |
| 2026 매출 | 가이던스 $737~757M (+22~25%) | 2Q26 +21% |
| 폐 부활 | 2Q26 매출 $2.3M | DENOVO 임상 |
| 차세대 심장 | — | ENHANCE Part B 임상, CHOPS(저비용 옵션) FDA 검토 중 |
| 신장 | 미진출 | 회사는 미국 연간 2만 건 이상을 노린다고 밝힘. 미국 신장 이식은 연 약 2.7만 건 (확인 필요) |
| 유럽 | 해외 매출 비중 3% | PAD Aviation 투자 (2026-07-01 종결) |

## 8. 주가가 반토막 난 이유 (시장이 걱정하는 것)

1. **성장 둔화:** 2025년 +37% → 2026년 가이던스 +22~25%. 미국 심장·간·폐 이식 건수 증가율이 약 5%로 둔화했다(2Q26, TD Cowen).
2. **이익 압축:** 2Q26 순이익 $14.7M (전년 $34.9M), 조정 EPS $0.44 (전년 $0.92). 임상·유럽·인력 투자 때문이다. 매출총이익률도 61.4% → 59.6%로 내려왔다.
3. **DCD 신뢰 문제:** 2025년 HRSA가 켄터키 장기구득기관 사례를 조사했고(검토한 351건 중 100건 이상에 우려 소견, 73건은 기증과 맞지 않는 신경학적 징후), 이후 OPO 개혁이 시작됐다. OPO 인정 기준(CfC) 최종 규칙이 2026년 말에 나올 수 있다(2차 출처, 확인 필요). DCD가 위축되면 TMDX의 핵심 시장이 줄어든다.
4. **상환 제도 리스크:** OIG가 장기 확보 비용 상환을 계속 문제 삼고 있다.
5. **기타:** 2028년 만기 1.50% 전환사채 $460M, 재고 관련 내부통제 중대 취약점, 숏셀러가 FDA에 OCS 간 승인 정지를 청원한 이력, 집단소송.

## 9. 보고서로 쓸 때의 각도

- **투자포인트 후보 1 (Q):** 사용 가능한 장기 풀 자체를 늘리는 회사라서, 미국 이식 건수 증가율(약 5%)이 아니라 **이식센터 침투율과 DCD 활용률**이 Q를 결정한다. 증명은 OPTN 장기별·기증자 유형별 이식 데이터 × ADS-B 전용기 22대의 비행 횟수로 한다.
- **투자포인트 후보 2 (P와 마진):** 서비스 마진 개선(29% → 35%)과 폐·심장 차세대 제품 믹스로 건당 매출과 이익이 늘어난다.
- **반드시 소명할 것:** NRP 대체 위험, DCD 규제, Medicare 상환 개혁.

## Sources
- FY2025 10-K: https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm
- 2Q26 10-Q: https://www.sec.gov/Archives/edgar/data/0001756262/000119312526332843/tmdx-20260630.htm
- 2Q26 8-K: https://www.sec.gov/Archives/edgar/data/0001756262/000119312526332767/tmdx-ex99_1.htm
- FY2025 실적 보도: https://www.barchart.com/story/news/397577/transmedics-reports-fourth-quarter-and-full-year-2025-financial-results
- 2028 목표·신장: https://www.alphaspread.com/security/nasdaq/tmdx/investor-relations/earnings-call/q3-2025 , https://quartr.com/events/transmedics-group-inc-tmdx-43rd-annual-j-p-morgan-healthcare-conference-2025_3gI0RRaC
- 2Q26 콜: https://vectorshift.ai/research/companies/transmedics-group/earnings/2026-q2 , https://newsable.asianetnews.com/markets/tmdx-stock-rallies-as-analyst-sees-77-upside-here-s-why-articleshow-fea6ncu
- Medicare 장기 확보 비용: https://oig.hhs.gov/reports/all/2026/conflicting-cms-guidance-and-federal-statutory-requirements-cost-medicare-380-million-over-a-6-year-period-for-organs-not-transplanted-into-medicare-enrollees/ , https://oig.hhs.gov/documents/audit/11866/OAS-25-07-124.pdf
- DCD 조사: https://hallrender.com/2025/07/25/reforms-to-organ-procurement-oversight-for-donations-after-circulatory-death-what-health-care-providers-need-to-know/ , https://energycommerce.house.gov/posts/chairmen-guthrie-and-joyce-pen-letter-to-cms-following-hhs-announcement-decertifying-south-florida-opo-and-implementing-further-safety-guidelines-for-the-organ-procurement-and-transplant-system
- 주가: https://stockanalysis.com/stocks/tmdx/statistics/
