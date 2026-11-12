# CLAUDE.md
이 저장소는 SMIC 스크리닝 프로젝트다. 작업 전에 `00_프로젝트_개요와_작업규칙.md` 를 읽고 그 규칙(출처 id·등급, 기준일, 사실·추론·가정 구분, 커밋 전 `check_bom.py` rc 0)을 따른다.

- 새 문서는 `claude/NN_제목_YYYY-MM-DD.md` 로 번호를 이어 붙인다(현재 03 까지).
- 종목을 보면 `screening/ledger.csv` 에 행을 더하거나 판정을 갱신한다.
- 밸류체인 값은 `market-intel/valuechain/<체인>/bom.json` 만 고치고 `render_bom.py` 로 `BOM.md` 를 다시 쓴다. 체인 yaml(`core/valuechain/*.yaml`)은 사용자 승인 없이 만들지 않는다 — 제안은 `core/valuechain/_inbox/` 에.
