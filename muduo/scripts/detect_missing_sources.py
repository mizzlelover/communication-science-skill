#!/usr/bin/env python3
"""detect_missing_sources — 来源覆盖报告（Coverage）。
列出未被任何机制节点引用的 Seed Sources；按 core_30 标记优先补强对象。"""
import sys
from kb import load_sources, load_mechanisms

def main():
    sources = load_sources()
    nodes, _ = load_mechanisms()
    cited = {}
    for nid, (node, fn) in nodes.items():
        for sid in node.get("source_ids", []) or []:
            cited.setdefault(sid, []).append(nid)

    uncited = [sid for sid in sorted(sources) if sid not in cited]
    core30 = {sid for sid, s in sources.items() if "core_30" in (s.get("notes") or "")}
    uncited_core = [s for s in uncited if s in core30]

    print(f"来源总数: {len(sources)}；已被引用: {len(cited)}；未引用: {len(uncited)}")
    print(f"core_30 共 {len(core30)} 个，其中未引用 {len(uncited_core)} 个\n")

    if uncited_core:
        print("== core_30 未引用（优先补强）==")
        for s in uncited_core:
            print(f"  {s}  {sources[s]['title']}")
    print("\n== 其余未引用 ==")
    for s in uncited:
        if s not in core30:
            print(f"  {s}  {sources[s]['title']}")

    print("\n说明：未引用 ≠ 必须引用——有的来源（如纯历史/批判著作）可在案例与文档层引用；")
    print("但 core_30 未深挖代表蒸馏缺口，应列入下一迭代。完整映射见 build_index 输出。")
    sys.exit(0)

if __name__ == "__main__":
    main()
