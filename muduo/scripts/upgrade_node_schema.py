#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""机制节点 schema 升级（补丁 §11/§38/§48/§62）。

为 216 个机制节点补齐可诚实推导的字段，绝不虚构：
  1. knowledge_half_life —— 按领域映射理论稳定性（§62）
  2. valid_as_of        —— AI 信息环境域节点（§38，取 provenance.last_verified）
  3. culture_moderators —— 从边界/失效/误读字段提取跨文化调节变量（§48/§87），无则不写
  4. provenance.conflicting_evidence —— 由 conflicting_nodes 的来源链推导
  5. provenance.case_sources        —— 由案例语料 mechanisms_candidate 反查
  6. provenance.platform_sources    —— 由平台适配器 known_platform_patterns 反查

无法诚实推导的字段（secondary_sources / boundary_sources）不写入，
决策记录于脚本输出与 CHANGELOG。

用法：python3 scripts/upgrade_node_schema.py [--dry-run]
"""
import glob
import os
import re
import sys

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026-09"

HALF_LIFE = {
    "attention": "very_long", "perception": "very_long", "memory": "very_long",
    "cognitive_load": "very_long", "processing_fluency": "very_long",
    "prediction_surprise": "very_long", "emotion": "very_long",
    "motivation": "very_long", "language_rhetoric": "very_long",
    "comprehension": "very_long",
    "identity": "long", "social_norms": "long", "social_proof": "long",
    "trust": "long", "authority": "long", "persuasion": "long",
    "attitude_change": "long", "framing": "long", "narrative": "long",
    "belonging": "long", "community": "long", "decision_making": "long",
    "behavioral_economics": "long", "diffusion": "long",
    "network_effects": "long", "complex_contagion": "long",
    "social_comparison": "long", "habit": "medium", "reward": "long",
    "brand_consumer": "medium",
    "ai_information_environment": "short",
    "platform_algorithmic": "very_short",
}
CULTURE_KW = re.compile(
    r"文化|中国|中文|东亚|华人|集体主|个人主|collectivis|individualis|跨文化|西方|本土")
NODE_FILE_CACHE = {}


def load_cases_index():
    """机制 id → 引用它的案例 id 列表。"""
    idx = {}
    d = yaml.safe_load(open(os.path.join(BASE, "knowledge/cases/cases.yaml"), encoding="utf-8"))
    cases = d["cases"] if isinstance(d, dict) and "cases" in d else d
    for c in cases:
        for m in c.get("mechanisms") or []:
            idx.setdefault(m, []).append(c["case_id"])
    return idx


def load_platform_index():
    """机制 id → [(platform, source_ref 提取的 S-id 列表)]。"""
    idx = {}
    for f in glob.glob(os.path.join(BASE, "platforms", "*", "adapter.yaml")):
        platform = f.split(os.sep)[-2]
        d = yaml.safe_load(open(f, encoding="utf-8"))
        for pat in d.get("known_platform_patterns") or []:
            srefs = re.findall(r"S\d+", str(pat.get("source_ref") or ""))
            for m in pat.get("mechanism_links") or []:
                if srefs:
                    idx.setdefault(m, set()).update(f"{platform}:{s}" for s in srefs)
    return idx


def load_node_sources():
    """节点 id → 全部引用的 S-id（用于 conflicting_evidence 推导）。"""
    idx = {}
    for f in glob.glob(os.path.join(BASE, "knowledge/mechanisms", "*.yaml")):
        d = yaml.safe_load(open(f, encoding="utf-8"))
        for n in d.get("nodes", []):
            srcs = set(n.get("source_ids") or [])
            prov = n.get("provenance") or {}
            srcs.update(prov.get("primary_sources") or [])
            srcs.update(prov.get("supporting_evidence") or [])
            idx[n["id"]] = srcs
    return idx


def main():
    dry = "--dry-run" in sys.argv
    case_idx = load_cases_index()
    plat_idx = load_platform_index()
    node_srcs = load_node_sources()
    stats = {"half_life": 0, "valid_as_of": 0, "culture": 0,
             "conflicting": 0, "case_sources": 0, "platform_sources": 0}
    for f in glob.glob(os.path.join(BASE, "knowledge/mechanisms", "*.yaml")):
        domain = os.path.basename(f)[:-5]
        raw_head = open(f, encoding="utf-8").readline()
        d = yaml.safe_load(open(f, encoding="utf-8"))
        changed = False
        for n in d.get("nodes", []):
            nid = n["id"]
            if n.get("knowledge_half_life") is None and domain in HALF_LIFE:
                n["knowledge_half_life"] = HALF_LIFE[domain]
                stats["half_life"] += 1
                changed = True
            if domain == "ai_information_environment" and n.get("valid_as_of") is None:
                lv = (n.get("provenance") or {}).get("last_verified", TODAY)
                n["valid_as_of"] = lv
                stats["valid_as_of"] += 1
                changed = True
            if n.get("culture_moderators") is None:
                hits = [b for b in (n.get("boundary_conditions") or [])
                        + (n.get("failure_conditions") or [])
                        + (n.get("common_misinterpretations") or [])
                        if CULTURE_KW.search(str(b))]
                if hits:
                    n["culture_moderators"] = hits
                    stats["culture"] += 1
                    changed = True
            prov = n.setdefault("provenance", {})
            conf_nodes = n.get("conflicting_nodes") or []
            if conf_nodes and not prov.get("conflicting_evidence"):
                conf_srcs = sorted(set().union(
                    *(node_srcs.get(c, set()) for c in conf_nodes))) if conf_nodes else []
                if conf_srcs:
                    prov["conflicting_evidence"] = conf_srcs
                    stats["conflicting"] += 1
                    changed = True
            if nid in case_idx and not prov.get("case_sources"):
                prov["case_sources"] = sorted(set(case_idx[nid]))
                stats["case_sources"] += 1
                changed = True
            if nid in plat_idx and not prov.get("platform_sources"):
                prov["platform_sources"] = sorted(plat_idx[nid])
                stats["platform_sources"] += 1
                changed = True
        if changed and not dry:
            out = yaml.dump(d, allow_unicode=True, sort_keys=False,
                            width=100, default_flow_style=False)
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(raw_head if raw_head.startswith("#") else "")
                fh.write(out)
    print(f"节点 schema 升级（dry-run={dry}）: {stats}")


if __name__ == "__main__":
    main()
