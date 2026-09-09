#!/usr/bin/env python3
"""detect_duplicate_nodes — 节点查重（持续去重）。
检查：1) ID 重复；2) canonical_name_en 完全相同；3) aliases 与其他节点 ID/名称重叠（潜在同义）。"""
import sys
from kb import load_mechanisms, err, warn

def norm(s):
    return (s or "").strip().lower().replace("-", " ").replace("_", " ")

def main():
    nodes, _ = load_mechanisms()
    failures = 0
    ids = list(nodes.keys())
    print(f"节点总数: {len(ids)}")

    # 1) exact ID duplicates（loader 已去重，检查不同文件同名节点）
    seen = {}
    for nid, (node, fn) in nodes.items():
        seen.setdefault(nid, []).append(fn)
    for nid, fs in seen.items():
        if len(fs) > 1:
            failures += err(f"ID 在多个文件出现: {nid} -> {fs}")

    # 2) 同名
    names = {}
    for nid, (node, fn) in nodes.items():
        names.setdefault(norm(node.get("canonical_name_en")), []).append(nid)
    for name, nids in names.items():
        if len(nids) > 1:
            failures += err(f"canonical_name_en 重复: {name} -> {nids}")

    # 3) aliases 撞车
    alias_map = {}
    for nid, (node, fn) in nodes.items():
        for a in node.get("aliases", []) or []:
            alias_map.setdefault(norm(a), []).append(nid)
    hits = 0
    for a, nids in alias_map.items():
        uniq = set(nids)
        if len(uniq) > 1:
            hits += 1
            failures += warn(f"alias 重叠（检查是否应合并）: '{a}' -> {sorted(uniq)}")
        if a in [norm(i) for i in ids] and len(uniq) >= 1:
            target = norm(a)
            owner = [i for i in ids if norm(i) == target]
            if owner and owner[0] not in uniq:
                failures += warn(f"alias '{a}'（{sorted(uniq)}）与节点 ID {owner[0]} 可能同义")

    print(f"\n{'发现 ' + str(hits) + ' 处 alias 重叠（需人工判断是否合并）' if hits else '无 alias 重叠'}")
    if failures:
        print("存在问题，见上")
        sys.exit(1)
    print("查重通过：无 ID/名称重复")

if __name__ == "__main__":
    main()
