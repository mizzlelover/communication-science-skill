#!/usr/bin/env python3
"""validate_schema — 校验全部 YAML 数据文件的结构合法性。
检查：来源 registry（含同书重复登记）、机制节点（必填字段/等级枚举/source_ids 存在/related_nodes 无悬空/时间格式）、
evidence_packages（全量 YAML 解析/source_id 注册表合法性/relevant_nodes 幽灵引用/MERGED_INTO 墓碑）、
案例库、反模式库、冲突索引、平台 adapter、eval 案例。"""
import os
import re
import sys
from kb import (load_sources, load_mechanisms, load_eval_cases, load_yaml, load_anti_patterns,
                GRADE_ENUM, MECH_DIR, PLATFORM_DIR, CASES_YAML, EVIDENCE_DIR,
                CONFLICTS_YAML, err, warn)

NODE_REQUIRED = ["id", "canonical_name_en", "canonical_name_zh", "domain", "definition",
                 "core_claim", "mechanism", "evidence_grade", "boundary_conditions",
                 "related_nodes", "source_ids", "last_reviewed"]
ADAPTER_REQUIRED = ["platform_name", "last_updated", "fact_confidence_summary", "content_units",
                    "dominant_user_intent", "distribution_model", "recommendation_model",
                    "social_graph_characteristics", "content_lifecycle", "primary_entry_points",
                    "attention_environment", "user_behavior", "interaction_signals",
                    "sharing_mechanism", "search_mechanism", "community_mechanism",
                    "algorithmic_features", "content_constraints", "title_role", "cover_role",
                    "opening_role", "tag_role", "comment_role", "follow_role", "risk_factors",
                    "known_platform_patterns", "confidence"]
EVAL_REQUIRED = ["case_id", "category", "difficulty", "input", "expected_behavior",
                 "key_mechanisms", "scoring_focus"]

def main():
    failures = 0
    sources = load_sources()

    # ---- sources ----
    print("== sources ==")
    if len(sources) < 100:
        failures += err(f"来源数量 {len(sources)} < 100")
    else:
        print(f"  [OK] {len(sources)} sources")
    sid_re = re.compile(r"^S[0-9]{2,3}$")
    for sid, s in sources.items():
        if not sid_re.match(sid):
            failures += err(f"来源 ID 格式非法: {sid}")
    # 同书重复登记检查（T1 验收固化）：title 归一化后不得重复
    by_title = {}
    for sid, s in sources.items():
        norm_title = re.sub(r"[^a-z0-9]", "", str(s.get("title", "")).lower())
        if norm_title:
            by_title.setdefault(norm_title, []).append(sid)
    for norm_title, sids in by_title.items():
        if len(sids) > 1:
            failures += err(f"来源注册表同书重复登记: {sids}")

    # ---- mechanisms ----
    print("== mechanisms ==")
    nodes, files = load_mechanisms()
    print(f"  [INFO] {len(nodes)} nodes in {len(files)} files")
    for nid, (node, fn) in nodes.items():
        for field in NODE_REQUIRED:
            if field not in node or node[field] in (None, "", []):
                failures += err(f"{fn}:{nid} 缺必填字段 {field}")
        g = node.get("evidence_grade")
        if g not in GRADE_ENUM:
            failures += err(f"{fn}:{nid} evidence_grade 非法: {g!r}")
        if not re.match(r"^[0-9]{4}-[0-9]{2}$", str(node.get("last_reviewed", ""))):
            failures += err(f"{fn}:{nid} last_reviewed 格式非法")
        for sid in node.get("source_ids", []) or []:
            if sid not in sources:
                failures += err(f"{fn}:{nid} 引用未知来源 {sid}")
        for rid in node.get("related_nodes", []) or []:
            if rid not in nodes:
                failures += err(f"{fn}:{nid} related_nodes 悬空引用 {rid}")
        for rid in node.get("conflicting_nodes", []) or []:
            if rid not in nodes:
                failures += err(f"{fn}:{nid} conflicting_nodes 悬空引用 {rid}")
        if len(node.get("boundary_conditions") or []) < 2:
            failures += err(f"{fn}:{nid} boundary_conditions < 2")
        if len(node.get("source_ids") or []) < 1:
            failures += err(f"{fn}:{nid} source_ids 为空")

    # ---- evidence packages（T2：整体 YAML 解析 + 引用合法性，防 S119/S30 类损坏与幽灵引用回归）----
    print("== evidence packages ==")
    eps_live, eps_tomb = {}, {}
    for fn in sorted(os.listdir(EVIDENCE_DIR)):
        if not fn.endswith(".yaml"):
            continue
        ep_path = os.path.join(EVIDENCE_DIR, fn)
        try:
            ep = load_yaml(ep_path)
        except Exception as e:
            failures += err(f"evidence_packages/{fn} YAML 解析失败: {e}")
            continue
        if not isinstance(ep, dict):
            failures += err(f"evidence_packages/{fn} 顶层结构非法（应为 dict）")
            continue
        sid = str(ep.get("source_id", ""))
        if not sid:
            failures += err(f"evidence_packages/{fn} 缺 source_id")
            continue
        if ep.get("merge_status") == "MERGED_INTO":
            eps_tomb[sid] = (fn, ep)
        else:
            eps_live[sid] = (fn, ep)
    for sid, (fn, ep) in eps_live.items():
        if not sid_re.match(sid):
            failures += err(f"evidence_packages/{fn} source_id 格式非法: {sid!r}")
            continue
        if not fn.startswith(f"{sid}_"):
            failures += err(f"evidence_packages/{fn} 文件名与 source_id {sid} 不匹配")
        if sid not in sources:
            failures += err(f"evidence_packages/{fn} source_id {sid} 不在来源注册表")
        for field in ("title", "content_obtained", "core_claims", "last_verified"):
            if not ep.get(field):
                failures += err(f"evidence_packages/{fn} 缺关键字段 {field}")
        rn = ep.get("relevant_nodes") or []
        ghosts = [r for r in rn if r not in nodes]
        if ghosts:
            failures += err(f"evidence_packages/{fn} relevant_nodes 幽灵引用: {ghosts}")
        if not rn and not ep.get("no_consumer_node"):
            failures += warn(f"evidence_packages/{fn} relevant_nodes 为空（无节点引用）")
    for sid, (fn, ep) in eps_tomb.items():
        target = str(ep.get("merged_into", ""))
        if target not in eps_live:
            failures += err(f"evidence_packages/{fn} 墓碑 merged_into 指向不存在的保留包: {target!r}")
        if ep.get("relevant_nodes"):
            failures += err(f"evidence_packages/{fn} 墓碑不应保留 relevant_nodes")
    print(f"  [INFO] {len(eps_live) + len(eps_tomb)} EPs（{len(eps_tomb)} MERGED_INTO 墓碑）")

    # ---- cases ----
    print("== cases ==")
    cases = load_yaml(CASES_YAML)
    cases = cases if isinstance(cases, list) else cases.get("cases", [])
    case_re = re.compile(r"^CASE-[A-Z]+-[0-9]{3}$")
    for c in cases:
        for field in ["case_id", "case_type", "context", "goal", "intervention", "mechanisms",
                      "result", "alternative_explanations", "evidence_quality", "lesson"]:
            if field not in c:
                failures += err(f"cases.yaml:{c.get('case_id')} 缺字段 {field}")
        if not case_re.match(str(c.get("case_id", ""))):
            failures += err(f"case_id 格式非法: {c.get('case_id')}")
        if len(c.get("alternative_explanations") or []) < 2:
            failures += err(f"cases.yaml:{c.get('case_id')} alternative_explanations < 2")
        for rid in c.get("mechanisms", []) or []:
            if rid not in nodes:
                failures += err(f"cases.yaml:{c.get('case_id')} 机制悬空 {rid}")
    print(f"  [INFO] {len(cases)} cases")

    # ---- anti patterns ----
    print("== anti_patterns ==")
    aps = load_anti_patterns()
    aps = aps if isinstance(aps, list) else aps.get("anti_patterns", [])
    for ap in aps:
        for field in ["anti_pattern_id", "name_en", "name_zh", "definition",
                      "why_short_term_works", "long_term_harms", "mechanisms"]:
            if field not in ap:
                failures += err(f"anti_patterns:{ap.get('anti_pattern_id')} 缺字段 {field}")
    print(f"  [INFO] {len(aps)} anti-patterns")

    # ---- conflicts ----
    print("== conflicts ==")
    if os.path.exists(CONFLICTS_YAML):
        cfs = load_yaml(CONFLICTS_YAML)
        cfs = cfs if isinstance(cfs, list) else cfs.get("conflicts", [])
        for cf in cfs:
            if cf.get("node_a") not in nodes or cf.get("node_b") not in nodes:
                failures += err(f"conflicts:{cf.get('conflict_id')} 节点引用悬空")
        print(f"  [INFO] {len(cfs)} conflicts")
    else:
        failures += warn("conflicts_index.yaml 不存在")

    # ---- platform adapters ----
    print("== platform adapters ==")
    n_ad = 0
    for d in sorted(os.listdir(PLATFORM_DIR)):
        p = os.path.join(PLATFORM_DIR, d, "adapter.yaml")
        if not os.path.isfile(p):
            continue
        n_ad += 1
        ad = load_yaml(p)
        for field in ADAPTER_REQUIRED:
            if field not in ad:
                failures += err(f"platforms/{d}/adapter.yaml 缺字段 {field}")
        if ad.get("confidence") not in ("high", "medium", "low"):
            failures += err(f"platforms/{d}/adapter.yaml confidence 非法")
        for pat in ad.get("known_platform_patterns", []) or []:
            for mid in pat.get("mechanism_links", []) or []:
                if mid not in nodes:
                    failures += err(f"platforms/{d}: mechanism_link 悬空 {mid}")
    print(f"  [INFO] {n_ad} adapters")

    # ---- eval cases ----
    print("== eval cases ==")
    evals = load_eval_cases()
    cat_counts = {}
    for c, fn in evals:
        for field in EVAL_REQUIRED:
            if field not in c:
                failures += err(f"evals/{fn}:{c.get('case_id')} 缺字段 {field}")
        for mid in c.get("key_mechanisms", []) or []:
            if mid not in nodes:
                failures += err(f"evals/{fn}:{c.get('case_id')} 机制悬空 {mid}")
        cat_counts[c.get("category", "?")] = cat_counts.get(c.get("category", "?"), 0) + 1
    print(f"  [INFO] {len(evals)} eval cases: {cat_counts}")

    print()
    if failures:
        print(f"校验失败：{failures} 个问题")
        sys.exit(1)
    print("校验通过：全部数据文件结构合法")

if __name__ == "__main__":
    main()
