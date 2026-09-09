#!/usr/bin/env python3
"""build_graph — 从节点重建 Mechanism Graph 并输出统计（关系边）。"""
import os
from collections import Counter
from kb import load_mechanisms, ROOT

EDGES = ["SUPPORTS", "CONTRADICTS", "MODERATES", "MEDIATES", "PRECEDES", "AMPLIFIES",
         "REDUCES", "REQUIRES", "OVERLAPS_WITH", "IS_SUBTYPE_OF", "APPLIES_TO"]

def main():
    nodes, _ = load_mechanisms()
    edges = []
    dangling = 0
    for nid, (node, fn) in nodes.items():
        for rid in node.get("related_nodes", []) or []:
            edges.append((nid, "RELATED", rid))
        for rid in node.get("conflicting_nodes", []) or []:
            edges.append((nid, "CONFLICTS_WITH", rid))

    # 邻接表（无向视图计数）
    adj = Counter()
    for a, rel, b in edges:
        adj[tuple(sorted([a, b]))] += 1

    deg = Counter()
    for a, rel, b in edges:
        deg[a] += 1
        deg[b] += 1

    # 连通分量
    seen, comps = set(), []
    for n in nodes:
        if n in seen:
            continue
        stack, comp = [n], set()
        while stack:
            cur = stack.pop()
            if cur in comp:
                continue
            comp.add(cur)
            for (x, y) in adj:
                if x == cur and y not in comp:
                    stack.append(y)
                if y == cur and x not in comp:
                    stack.append(x)
        seen |= comp
        comps.append(comp)
    comps.sort(key=len, reverse=True)

    # 域间边
    dom = {n: nodes[n][0].get("domain") for n in nodes}
    cross = Counter()
    for a, rel, b in edges:
        if dom.get(a) != dom.get(b):
            cross[tuple(sorted([dom[a], dom[b]]))] += 1

    print(f"节点: {len(nodes)}")
    print(f"边（含无向重复计数）: {len(edges)}；独立节点对: {len(adj)}")
    print(f"平均度: {sum(deg.values())/len(nodes):.1f}；最大度: {deg.most_common(5)}")
    print(f"连通分量: {len(comps)}（最大 {len(comps[0])} 节点）")
    if len(comps) > 1:
        print("  孤立分量:", [sorted(c) for c in comps[1:]])
    print("跨域连接 Top 10:")
    for (da, db), c in cross.most_common(10):
        print(f"  {da} <-> {db}: {c}")

    out = os.path.join(ROOT, "knowledge", "evidence", "graph_summary.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("# Mechanism Graph Summary（自动生成）\n\n")
        f.write(f"- 节点：{len(nodes)}\n- 边（引用对）：{len(edges)}（独立对 {len(adj)}）\n")
        f.write(f"- 平均度：{sum(deg.values())/len(nodes):.1f}\n- 连通分量：{len(comps)}\n\n")
        f.write("## 度数 Top 15（枢纽节点）\n\n")
        for n, d in deg.most_common(15):
            f.write(f"- `{n}` {nodes[n][0].get('canonical_name_zh','')} — 度 {d}\n")
        f.write("\n## 跨域连接 Top 15\n\n")
        for (da, db), c in cross.most_common(15):
            f.write(f"- {da} <-> {db}：{c} 条\n")
    print(f"\n已生成 {out}")

if __name__ == "__main__":
    main()
