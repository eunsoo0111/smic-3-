#!/usr/bin/env python3
"""QA 배달 관문(Gate 2) — quality_rubric.md 의 모든 항목(A1..F3)이
<study_dir>/QA_<YYYYMMDD>.md(최신 날짜) 안에서 체크(`- [x] A1 …`)돼 있어야 배달 통과.
「QA_<date>.md 없으면 배달 금지」를 실제로 막는 게이트.

사용: python3 check_qa_before_delivery.py <study_dir>
      (rc 0 = 전항목 체크·배달 가능 / rc 1 = QA 파일 없음 또는 미체크·누락 항목 있음 → 배달 금지)
"""
import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUBRIC_PATH = os.path.join(HERE, 'quality_rubric.md')
QA_RE = re.compile(r'^QA_(\d{8})\.md$')
ITEM_ID_RE = re.compile(r'\[[ xX]\]\s*([A-G]\d+)\b')
CHECK_LINE_RE = re.compile(r'-\s*\[([ xX])\]\s*([A-G]\d+)\b')   # G = 밸류체인 위치·이음매


def rubric_ids(rubric_path=RUBRIC_PATH):
    """quality_rubric.md 의 체크리스트에서 항목 id(A1..F3 등)를 등장 순서대로 뽑는다."""
    text = open(rubric_path, encoding='utf-8').read()
    ids, seen = [], set()
    for m in ITEM_ID_RE.finditer(text):
        item_id = m.group(1)
        if item_id not in seen:
            seen.add(item_id)
            ids.append(item_id)
    return ids


def latest_qa_file(study_dir):
    """<study_dir> 바로 아래 QA_<YYYYMMDD>.md 중 날짜가 가장 최신인 파일. 없으면 None."""
    cands = []
    for p in glob.glob(os.path.join(study_dir, 'QA_*.md')):
        m = QA_RE.match(os.path.basename(p))
        if m:
            cands.append((m.group(1), p))
    if not cands:
        return None
    cands.sort(key=lambda t: t[0])
    return cands[-1][1]


def parse_qa_checks(qa_path):
    """QA 파일에서 `- [x] <id>` / `- [ ] <id>` 줄을 읽어 {id: checked(bool)}. 같은 id 재등장 시 마지막이 이긴다."""
    text = open(qa_path, encoding='utf-8').read()
    checks = {}
    for m in CHECK_LINE_RE.finditer(text):
        checks[m.group(2)] = m.group(1).lower() == 'x'
    return checks


def gate_g_items(study_dir, ids):
    """(ids, note) — narrative.json S0 착수일이 JOINT_EFFECTIVE 전이거나 판정 불가면 G* 항목을 뺀다."""
    if not any(i.startswith('G') for i in ids):
        return ids, None
    try:
        import json
        sys.path.insert(0, HERE)
        import check_study as CS
        nar_path = os.path.join(study_dir, 'narrative.json')
        nar = json.load(open(nar_path, encoding='utf-8'))
        gdate, basis = CS.joint_gate_date(nar, nar_path)
        if gdate >= CS.JOINT_EFFECTIVE:
            return ids, None
        why = f'S0 {gdate}({basis}) < {CS.JOINT_EFFECTIVE}'
    except Exception as e:
        why = f'S0 날짜 판정 불가({e})'
    return [i for i in ids if not i.startswith('G')], f'~ G 항목(밸류체인 위치·이음매) 건너뜀 — {why}'


def run(study_dir, rubric_path=RUBRIC_PATH):
    """(rc:int, lines:list[str]) — 호출자가 원하는 형태로 출력하게 분리."""
    lines = []
    if not os.path.isdir(study_dir):
        lines.append(f'✗ study_dir 없음: {study_dir}')
        lines.append(f'BUILD/BOARD: QA 게이트 — study_dir 없음({study_dir}) → 배달 금지')
        return 1, lines

    ids = rubric_ids(rubric_path)
    if not ids:
        lines.append(f'✗ 루브릭에서 항목 id 를 못 찾음: {rubric_path}')
        lines.append('BUILD/BOARD: QA 게이트 — 루브릭 파싱 실패 → 배달 금지')
        return 1, lines

    # G 절은 S0 착수일 ≥ 2026-10-05 팩만 필수 —
    # 진행 중 팩의 QA 파일이 G1·G2 를 몰라도 배달이 막히지 않게(check_study.joint_gate_date 와 같은 날짜 키)
    ids, g_note = gate_g_items(study_dir, ids)
    if g_note:
        lines.append(g_note)

    qa_path = latest_qa_file(study_dir)
    if not qa_path:
        lines.append(f'✗ QA_<YYYYMMDD>.md 없음: {study_dir} — 배달 금지')
        lines.append(f'BUILD/BOARD: QA 게이트 — {os.path.basename(study_dir.rstrip("/"))} QA 파일 없음 → 배달 금지')
        return 1, lines

    checks = parse_qa_checks(qa_path)
    missing = [i for i in ids if i not in checks]
    unchecked = [i for i in ids if i in checks and not checks[i]]
    total = len(ids)
    passed = total - len(missing) - len(unchecked)

    lines.append(f'QA 파일: {qa_path}')
    lines.append(f'루브릭 항목 {total}개 · 체크됨 {passed} · 미체크 {len(unchecked)} · 누락 {len(missing)}')
    for i in missing:
        lines.append(f'  ✗ {i}: QA 파일에 항목이 없다')
    for i in unchecked:
        lines.append(f'  ✗ {i}: 미체크(- [ ])')

    blocked = bool(missing or unchecked)
    summary = (f'BUILD/BOARD: QA {os.path.basename(qa_path)} — {passed}/{total} 체크'
               + (f', 미체크/누락 {len(unchecked) + len(missing)}건 → 배달 금지' if blocked
                  else ' (전항목) → 배달 가능'))
    lines.append(summary)
    return (1 if blocked else 0), lines


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('study_dir')
    ap.add_argument('--rubric', default=RUBRIC_PATH, help='기본: 이 스크립트 옆 quality_rubric.md')
    a = ap.parse_args()
    rc, lines = run(a.study_dir, a.rubric)
    for line in lines:
        print(line)
    sys.exit(rc)


if __name__ == '__main__':
    main()
