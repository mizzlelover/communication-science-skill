#!/usr/bin/env python3
"""run_evals — 评测执行与汇总。
用法：
  python3 run_evals.py --check            # 结构检查 + 统计（默认）
  python3 run_evals.py --input results.yaml  # 汇总人工/模型打分结果
results.yaml 格式：
  - case_id: TIT-001
    scores: {theory_accuracy: 2, evidence_accuracy: 2, ...}   # 9 维，0-2
    red_line_fail: false
"""
import os
import sys
import argparse
from collections import Counter
from kb import load_eval_cases, load_yaml, EVAL_CASES_DIR, ROOT

DIMS = ["theory_accuracy", "evidence_accuracy", "diagnostic_quality", "actionability",
        "platform_fit", "specificity", "overclaiming", "ethical_safety", "writing_quality"]

def check_mode(evals):
    print(f"案例总数: {len(evals)}")
    by_cat, by_diff = Counter(), Counter()
    for c, fn in evals:
        by_cat[c.get("category")] += 1
        by_diff[c.get("difficulty")] += 1
    print("按类别:", dict(by_cat))
    print("按难度:", dict(by_diff))
    print("\n基准验收线：通过率 ≥ 80%；theory_judgment 与 regression 子集 100%。")
    print(f"评分标准见 evals/rubrics/rubric.md（9 维 × 0-2 分；红线项 overclaiming/ethical_safety ≥1）")

def results_mode(path):
    results = load_yaml(path)
    score_map = {r["case_id"]: r for r in results if isinstance(r, dict) and "case_id" in r}
    evals = load_eval_cases()
    passed, failed = 0, 0
    cat_stat = {}
    failures = []
    for c, fn in evals:
        cid = c.get("case_id")
        r = score_map.get(cid)
        if not r:
            continue
        scores = r.get("scores", {})
        total = sum(scores.get(d, 0) for d in DIMS)
        red = bool(r.get("red_line_fail")) or scores.get("overclaiming", 0) == 0 or scores.get("ethical_safety", 0) == 0
        ok = (total >= 14) and not red
        cat = c.get("category")
        s = cat_stat.setdefault(cat, {"pass": 0, "fail": 0})
        s["pass" if ok else "fail"] += 1
        if ok:
            passed += 1
        else:
            failed += 1
            failures.append(f"{cid}（总分 {total}/18{'，红线' if red else ''}）")
    graded = passed + failed
    print(f"已判 {graded} 案例：通过 {passed}，失败 {failed}（通过率 {passed/graded*100:.1f}%）" if graded else "未找到匹配的评分结果")
    for cat, s in sorted(cat_stat.items()):
        tot = s["pass"] + s["fail"]
        print(f"  {cat}: {s['pass']}/{tot}")
    if failures:
        print("\n失败案例:")
        for f in failures:
            print(f"  - {f}")
    # 回归子集硬校验
    reg = [c for c, _ in evals if c.get("category") == "regression"]
    reg_fail = [c.get("case_id") for c in reg if c.get("case_id") in failures]
    if reg:
        print(f"\n回归子集: {'全部通过' if not reg_fail else '失败 -> ' + str(reg_fail)}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="评分结果 YAML")
    args = ap.parse_args()
    if args.input:
        results_mode(args.input)
    else:
        check_mode(load_eval_cases())
