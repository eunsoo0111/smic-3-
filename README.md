# smic-3-
SMIC 3주차 스크리닝을 하기 위한 저장소. 산업을 밸류체인 구조로 먼저 이해하고, 그 위에서 종목을 거른 과정과 결과를 쌓는다.

**처음 오면** `00_프로젝트_개요와_작업규칙.md` 를 먼저 읽는다.

## 지금 들어 있는 것
| 산업 | 읽는 순서 |
|---|---|
| 우주(2026-11-12) | ① `claude/01_우주산업_밸류체인_정리_2026-11-12.md` — 구조를 쉽게 정리 → ② `claude/02_우주산업_변화지도_2026-11-12.md` — 변화 12개·문제 10개 → ③ `claude/03_우주산업_롱리스트_2026-11-12.md` — 종목 32개 1차 판정 |

- 스크리닝 원장: `screening/ledger.csv`(본 종목 전부 한 줄씩) · 양식: `screening/TEMPLATE_30초테스트.md`
- 밸류체인 정본 데이터: `market-intel/valuechain/space/`(`bom.json`·`BOM.md`·`GAPS.md`·`sources.jsonl`)

## 새 산업을 추가할 때
1. `valuechain-study` 스킬로 `market-intel/valuechain/<체인>/` 을 만든다(검사: `python3 market-intel/valuechain/_contracts/check_bom.py market-intel/valuechain/<체인>`).
2. `smic-stock-screening` 스킬로 변화 지도 → 롱리스트 → 30초 테스트 → 2차 컷 순서로 `claude/NN_제목_YYYY-MM-DD.md` 를 이어 쓴다.
3. 본 종목은 `screening/ledger.csv` 에 한 줄씩 더하고, 판정이 바뀌면 그 줄을 고친 뒤 문서의 「정정 기록」에 이유를 남긴다.
