#!/usr/bin/env python3
"""build_index — 生成知识库索引 INDEX.md（节点按域分组 + 证据等级分布 + 来源覆盖）。"""
import os
from collections import Counter
from kb import load_sources, load_mechanisms, DOMAINS_INDEX, ROOT

def main():
    sources = load_sources()
    nodes, files = load_mechanisms()
    idx = load_yaml_file()
    domains = {d["id"]: d for d in idx["domains"]}

    lines = ["# INDEX — 机制节点索引（自动生成，勿手改）", ""]
    grades = Counter(n.get("evidence_grade") for n, _ in nodes.values())
    lines.append(f"节点总数：{len(nodes)}；文件数：{len(files)}")
    lines.append("证据等级分布：" + "，".join(f"{g}={grades.get(g,0)}" for g in ["A","A-","B+","B","B-","C","D","E"]) + "\n")

    for did, d in domains.items():
        dnodes = sorted(n for n in nodes if nodes[n][0].get("domain") == did)
        declared = d.get("nodes", [])
        extra = set(dnodes) - set(declared)
        lines.append(f"## {did} — {d.get('name_zh','')} / {d.get('name_en','')}")
        lines.append(f"{d.get('scope','')}（{len(dnodes)} 节点）\n")
        for nid in dnodes:
            node, _ = nodes[nid]
            lines.append(f"- `{nid}` {node.get('canonical_name_zh','')} / {node.get('canonical_name_en','')} "
                         f"（{node.get('evidence_grade')}）")
        if extra:
            lines.append(f"- [未在 _index.yaml 声明的节点] {sorted(extra)}")
        lines.append("")

    src_use = Counter()
    for n, _ in nodes.values():
        for s in n.get("source_ids", []) or []:
            src_use[s] += 1
    lines.append("## 来源引用 Top 20\n")
    for sid, cnt in src_use.most_common(20):
        t = sources.get(sid, {}).get("title", "?")
        lines.append(f"- {sid} {t} ×{cnt}")
    uncited = [s for s in sorted(sources) if s not in src_use]
    lines.append(f"\n未被机制节点引用的来源（{len(uncited)}）：{', '.join(uncited)}\n")

    out = os.path.join(ROOT, "INDEX.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"已生成 {out}（{len(nodes)} 节点）")

def load_yaml_file():
    from kb import load_yaml
    return load_yaml(DOMAINS_INDEX)

if __name__ == "__main__":
    main()
