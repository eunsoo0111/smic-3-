# 기업 state.json · changelog.jsonl 계약

## state.json — 「지금 이 회사를 어떻게 보나」 한 파일(팩 루트 `packs/<tk>/state.json`). 생성기 `tools/study/state_build.py <팩>`; 손으로 안 쓴다.
| 칸 | 뜻 | 원천 |
|---|---|---|
| ticker·name·asof | 식별·생성 시각(KST 실측) | narrative.json |
| thesis_one_liner | 테제 한 줄(표지 첫 문장) | writeup/text/cover_*.json P1 첫 문장, 없으면 narrative.user_thesis |
| attention | 주목의 이유: why_now·must_be_true[3]·where_to_check[3] | narrative.attention(SKILL S0 0번째 줄), 없으면 null = 결손(🟠) |
| call·price·price_asof | 콜·현재가 | model_summary.json |
| cases | Bear/Base/Bull 값·확률, prob_weighted | cases.json(팩마다 꼴이 달라 생성기가 흡수) |
| floor_option | 바닥·옵션·내재 옵션(§2-F) | cases.json floor/option/implied_option, 없으면 null |
| lenses | 렌즈 지표 id 목록 + 마지막 lens_watch 판정 | lens_registry.yaml + status/lens_watch_latest |
| tracking | 추적 지표 수·다음 달력 항목 | tracking_register.json |
| last_reviewed | 팩 판단 파일들의 마지막 수정일(실측) | study_v2/*.json·verification/*·writeup pdf mtime 최대 |
| next_check | 다음 확인 날짜·사유 | tracking_register.calendar 중 오늘 이후 첫 항목 |
| stale | last_reviewed 가 7일(기업) 넘었나 | 생성기 계산 |

## changelog.jsonl — 변경 노트 한 행(팩 루트). 세 트리거(이벤트·데이터·달력) 회차마다 **정확히 한 행**, 변경 0 이어도 한 행.
`{"ts","trigger":"event|data|calendar|user","source":"<무엇이 들어왔나>","what_changed":"<한 줄>","must_be_true_hit":[idx…],"verdict":"kept|changed|unknown","call_before","call_after","value_before","value_after","next_check","by":"<서브·세션>"}`
추가: `.venv/bin/python tools/study/changelog_add.py <팩> --trigger data --source "lens_watch 🔴 <지표 id>" --what "…" --verdict kept --by analyst`. study-tracker 서브는 회차 끝에 반드시 이 한 줄을 남긴다(`.claude/agents/study-tracker.md`). 판정이 changed 인 행만 write-up 재발행·노션·텔레로 간다.
