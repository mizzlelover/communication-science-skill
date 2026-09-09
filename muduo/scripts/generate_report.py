#!/usr/bin/env python3
"""generate_report — 汇总库内统计，输出报告数据段草稿。"""
import os
from collections import Counter
from kb import (load_sources, load_mechanisms, load_eval_cases, load_yaml,
                PLATFORM_DIR, ROOT)

def main():
    sources = load_sources()
    nodes, files = load_mechanisms()
    evals = load_eval_cases()
    idx = load_yaml(os.path.join(ROOT, "knowledge", "domains", "_index.yaml"))
    conf = load_yaml(os.path.join(ROOT, "knowledge", "evidence", "conflicts", "conflicts_index.yaml"))
    anti = load_yaml(os.path.join(ROOT, "knowledge", "anti_patterns", "anti_patterns.yaml"))
    cases = load_yaml(os.path.join(ROOT, "knowledge", "cases", "cases.yaml"))

    grades = Counter(n.get("evidence_grade") for n, _ in nodes.values())
    doms = Counter(n.get("domain") for n, _ in nodes.values())
    n_platforms = len([d for d in os.listdir(PLATFORM_DIR) if os.path.isfile(os.path.join(PLATFORM_DIR, d, "adapter.yaml"))])
    src_use = set()
    for n, _ in nodes.values():
        src_use |= set(n.get("source_ids", []) or [])

    print("== 报告数据段 ==")
    print(f"domains: {len(idx['domains'])}（含 ai_information_environment 模块）")
    print(f"mechanism_nodes: {len(nodes)} in {len(files)} files")
    print("evidence_distribution:", {g: grades.get(g, 0) for g in ["A", "A-", "B+", "B", "B-", "C", "D", "E"]})
    print(f"AB 级占比: {(grades.get('A',0)+grades.get('A-',0)+grades.get('B+',0)+grades.get('B',0)+grades.get('B-',0))/len(nodes)*100:.0f}%")
    print(f"sources: {len(sources)} registered, {len(src_use)} cited by mechanisms")
    print(f"platform_adapters: {n_platforms}")
    print(f"cases: {len(cases) if isinstance(cases, list) else '?'}; anti_patterns: {len(anti) if isinstance(anti, list) else '?'}; conflicts: {len(conf) if isinstance(conf, list) else '?'}")
    print(f"eval_cases: {len(evals)}")
    print("\nnode count by domain:")
    for d, c in doms.most_common():
        print(f"  {d}: {c}")

if __name__ == "__main__":
    main()
