# TMDX 스터디 팩 (equity-analysis, 2026-11-11)

- 먼저 읽을 것: [SUMMARY.md](SUMMARY.md)는 대화형 요약이에요(결론·드라이버·숫자·사다리·캘린더·틀릴 조건).
- 사용자 엑셀과 SEC 원문 대조: [digest/discrepancies.md](digest/discrepancies.md)
- 모델 다시 돌리기: `python3 study/TMDX/model/build_model.py`. 판단값은 스크립트 맨 위 BASE·CASES에만 있어요.
- 계약 검사:

```bash
python3 market-intel/analysts/_study_contracts/check_study.py study/TMDX/study_v2 --strict-blind --strict-thesis --model-dir study/TMDX/model
```

- 원천: `sources/primary_facts.json`(SEC accession 번호 포함). SEC 원문 파일 자체는 저장소에 넣지 않았어요(EDGAR에서 다시 받을 수 있어요).
- 미동봉: report-init Word 빌더 산출(요청 시 만듦), 하우스 도표, AUDIT_* 감사 파일(write-up 단계용)
