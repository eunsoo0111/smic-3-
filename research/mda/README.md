# MDA Space 리서치 (SMIC 3팀)

기준일 2026-11-15. 이번 대화의 Q&A와 다른 브랜치 5곳의 MDA 노트를 층위별로 합친 폴더입니다.

| 파일 | 내용 |
|---|---|
| `MDA_층위별_리서치_재료.xlsx` | 셀레스티카 층위별 리서치 재료와 같은 양식. 층위 지도(18층위) / 리서치 재료(249행, 한 행에 주장 하나) / 지표 원장(161개, 수식 포함) / 분기 시계열(2022Q1~2026Q3) / 출처(82개) |
| `MDA_리서치노트_층위별.md` | 같은 재료를 층위별로 읽는 서술형 노트. 층위마다 결론 → 핵심 표 → 재료 목록. 부록에 세션 Q&A, 브랜치 출처, 출처 목록 |
| `branch_notes/` | 다른 브랜치에서 가져온 원본 노트 사본(B01~B09). 원본은 각 브랜치에 그대로 있음 |
| `_build/` | 엑셀·노트 생성 스크립트와 데이터. 재료를 고치면 아래 두 줄로 다시 만듦 |

```bash
python3 research/mda/_build/build_workbook.py
```

```bash
python3 research/mda/_build/build_note.py
```

## branch_notes 출처

| 사본 | 원 브랜치 | 원 경로 |
|---|---|---|
| B01_mda-space-deep-dive.md | claude/practical-mccarthy-g6kvct | research/mda-space-deep-dive.md |
| B02_M1_M2_sovereign_demand.md | claude/elegant-cerf-tmeeqn | study/MDA/study_v2/verification/M1_M2_sovereign_demand.md |
| B03_M3_M4_company.md | claude/elegant-cerf-tmeeqn | study/MDA/study_v2/verification/M3_M4_company.md |
| B04_narrative.json | claude/elegant-cerf-tmeeqn | study/MDA/study_v2/narrative.json |
| B05_quarterly.csv | claude/elegant-cerf-tmeeqn | study/MDA/data/quarterly.csv |
| B06_MDA_투자포인트_v2.md | claude/hopeful-galileo-se2znn | study/SPACE/MDA_투자포인트_v2.md |
| B07_MDA_BKSY_칠판개요.md | claude/hopeful-galileo-se2znn | study/SPACE/MDA_BKSY_칠판개요.md |
| B08_Q3_2026_concall_overview_tracking.md | claude/laughing-ride-qdcywi | space/companies/mda-space/{concalls/2026-Q3, overview, tracking}.md |
| B09_우주산업_밸류체인_정리.md | claude/ecstatic-clarke-fbv4xc | claude/01_우주산업_밸류체인_정리_2026-11-12.md |

## 이번에 정정한 것 (자세한 내용은 18층위)

- 잔고 저점은 3Q26이 아니라 1Q26(C$3.69B)
- SpaceX 상장: 2026-06-12, 공모가 US$135, 첫날 시총 약 US$2.1조. 이전의 '약 $1.77T, 이후 약 50% 하락'은 근거 부족
- Crimea: Starlink를 '끈' 것이 아니라 '켜 달라는 요청을 거절'한 것
- 'Starlink 약관이 무기 사용을 금지한다' → 약관 원문 미확인. Shotwell(2023-02) 발언으로 대체
- Globalstar 위성 버스는 Rocket Lab이 하청 제작(US$143M) — 공시로 확인
- Lanteris는 2026-01 Intuitive Machines에 인수됨
