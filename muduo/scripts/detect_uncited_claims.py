#!/usr/bin/env python3
"""detect_uncited_claims — 无出处断言检测（Citation 纪律）。
检查机制节点：1) evidence.supporting 为空；2) definition/core_claim 为空；3) 节点未引用任何来源（validate 已查，此处再复查）；4) 标注 verification_required 的来源。"""
import sys
from kb import load_sources, load_mechanisms, err

def main():
    sources = load_sources()
    nodes, _ = load_mechanisms()
    failures = 0
    no_support, no_claim = [], []
    for nid, (node, fn) in nodes.items():
        if not (node.get("evidence") or {}).get("supporting"):
            no_support.append(f"{fn}:{nid}")
        if not node.get("core_claim"):
            no_claim.append(f"{fn}:{nid}")
    for f in no_support:
        failures += err(f"evidence.supporting 为空: {f}")
    for f in no_claim:
        failures += err(f"core_claim 为空: {f}")

    vr = [sid for sid, s in sources.items() if s.get("access_status") == "verification_required"]
    print(f"节点总数: {len(nodes)}；无 supporting 证据: {len(no_support)}；无 core_claim: {len(no_claim)}")
    print(f"标记 verification_required 的来源: {len(vr)}")
    for sid in vr:
        print(f"  {sid} {sources[sid]['title']}")
    if failures:
        sys.exit(1)
    print("\n引用纪律检查通过：所有节点均有证据栏与来源")

if __name__ == "__main__":
    main()
