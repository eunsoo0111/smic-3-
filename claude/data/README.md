# 원자료 (기준일 2026-11-04)

| 파일 | 내용 | 출처 |
|---|---|---|
| `openfda_ndc_estradiol_transdermal.json` | 미국 에스트라디올 경피 제품 NDC 목록 (제조사·브랜드) | openFDA NDC API |
| `sdud_estradiol_patch_by_maker.txt` | 메디케이드 에스트라디올 HRT 패치 물량(천 장)·점유율·단가, 2022Q1~2026Q1, 전국(XX) 합계 | Medicaid State Drug Utilization Data |
| `nadac_estradiol_patch_monthly.txt` | 에스트라디올 패치 0.05mg NADAC(약국 매입가) 월별 중앙값, 2024-01~2026-11 | Medicaid NADAC |

재현 방법 (`scripts/`):
1. `ndc_estradiol_td.json` 이름으로 openFDA 결과를 받은 폴더를 `DATA`로 둔다.
2. `python3 -I scripts/sdud.py DATA` → `python3 -I scripts/sdud_agg.py DATA`
3. `python3 -I scripts/nadac.py DATA` → `python3 -I scripts/nadac_agg.py DATA`

주의: 피임 패치(노렐게스트로민·에티닐에스트라디올) 제외, 비공개 처리(suppression) 행 제외, FFSU+MCOU 합산. NADAC는 제네릭 그룹 단위 가격이라 같은 그룹의 제조사는 같은 값이다.
