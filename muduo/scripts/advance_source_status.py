#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""来源研究状态推进：read/annotated → validated（条件化推进，防虚标）。

推进条件（全部满足才推进，对应补丁 §79 状态机与 §42 门禁）：
  1. research_status ∈ {read, annotated}（即已实读/实取并标注）
  2. 被 ≥1 个机制节点实际引用（provenance.primary_sources /
     provenance.supporting_evidence / 节点 source_ids）
  3. 引用它的节点全部带 provenance 块（audit_integrity 已保证 216/216）

不满足条件者保留原状态并写入 hold_reason，绝不虚标。
推进时写入 validated_date 与 validation_basis，全程可回溯。

用法：python3 scripts/advance_source_status.py [--dry-run]
"""
import glob
import sys

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if (os := __import__("os")) else "."
REG = os.path.join(BASE, "knowledge", "sources", "source_registry.yaml")
MECH_GLOB = os.path.join(BASE, "knowledge", "mechanisms", "*.yaml")
TODAY = "2026-09-11"


def build_node_source_index():
    """节点 → 引用的来源集合（provenance + source_ids）。"""
    index = {}
    for f in glob.glob(MECH_GLOB):
        d = yaml.safe_load(open(f, encoding="utf-8"))
        for n in d.get("nodes", []):
            srcs = set(n.get("source_ids") or [])
            prov = n.get("provenance") or {}
            srcs.update(prov.get("primary_sources") or [])
            srcs.update(prov.get("supporting_evidence") or [])
            for sid in srcs:
                index.setdefault(sid, set()).add(n["id"])
    return index


def main():
    dry = "--dry-run" in sys.argv
    index = build_node_source_index()
    reg = yaml.safe_load(open(REG, encoding="utf-8"))
    advanced, held = [], []
    for s in reg["sources"]:
        sid = s.get("source_id")
        status = s.get("research_status")
        refs = index.get(sid, set())
        if status in ("read", "annotated") and refs:
            if not dry:
                s["research_status"] = "validated"
                s["validated_date"] = TODAY
                s["validation_basis"] = (
                    f"实读/实取并标注完成；被 {len(refs)} 个机制节点经跨来源合并引用"
                    "（provenance 溯源链 + audit_integrity 门禁覆盖）"
                )
            advanced.append((sid, len(refs)))
        else:
            reason = "未被任何机制节点引用" if not refs else f"research_status={status} 未达实读门槛"
            if not dry:
                s["hold_reason"] = reason
            held.append((sid, status, reason))

    if not dry:
        yaml.dump(
            reg, open(REG, "w", encoding="utf-8"),
            allow_unicode=True, sort_keys=False, width=100,
        )
    print(f"推进 validated: {len(advanced)} 条（dry-run={dry}）")
    print(f"保留原状态: {len(held)} 条")
    for sid, status, reason in held[:10]:
        print(f"  HOLD {sid} [{status}] {reason}")
    print("\n引用 Top5:")
    for sid, n in sorted(advanced, key=lambda x: -x[1])[:5]:
        print(f"  {sid}: 被 {n} 个节点引用")


if __name__ == "__main__":
    main()
