#!/usr/bin/env python3
"""audit_integrity — 研究诚信自动审计。

实现补丁要求的 11 项检查：
  audit_source_acquisition            来源获取状态审计
  detect_metadata_only_sources        仅登记元数据的来源
  detect_memory_based_claims          依赖模型记忆的主张（缺省 validation_status = MEMORY_BASED）
  detect_missing_primary_sources      无一手/综述证据的节点
  detect_missing_counterevidence      无反例证据的节点
  detect_missing_boundaries           无边界/失效条件的节点
  detect_uncited_claims               无来源引用的节点
  detect_stale_platform_claims        平台知识超期/未核验
  detect_case_without_material        无一手材料的案例
  detect_single_case_generalization   单案例过度泛化风险
  detect_platform_claim_without_level 无证据级别的平台主张

用法：
  python3 scripts/audit_integrity.py                  # 打印摘要 + 写 audits/audit_report_data.yaml
  python3 scripts/audit_integrity.py --write-tables   # 同时把自动表格回填进审计文档（标记块内）
"""
import os
import sys
import glob
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb import (load_sources, load_mechanisms, load_yaml, MECH_DIR, PLATFORM_DIR, CASES_YAML)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDITS_DIR = os.path.join(ROOT, "audits")
DATA_OUT = os.path.join(AUDITS_DIR, "audit_report_data.yaml")

NOW = datetime.date(2026, 9, 8)
# 平台知识新鲜度阈值（月）：official policy 12 · algorithm observation 6 · UI feature 3（）
FRESHNESS_MONTHS = {"official_rule": 12, "verified_observation": 6,
                    "industry_consensus": 6, "experience_speculation": 3}

# 一手类型含 official_source（任务书 §6 来源类型；平台机制节点的最强一手即官方文档，
# 2026-09-11 扩展——官方来源须为本项目实读并在 EP 中记录 content_obtained）
PRIMARY_SOURCE_TYPES = {"paper", "meta_analysis", "systematic_review", "official_source"}


def months_since(ym):
    try:
        y, m = str(ym).split("-")
        d = datetime.date(int(y), int(m), 1)
    except Exception:
        return None
    return (NOW.year - d.year) * 12 + (NOW.month - d.month)


def node_validation_status(node):
    """：缺省 = MEMORY_BASED（不得隐瞒）。"""
    return node.get("validation_status", "MEMORY_BASED")


def main():
    write_tables = "--write-tables" in sys.argv
    os.makedirs(AUDITS_DIR, exist_ok=True)

    sources = load_sources()
    nodes, mech_files = load_mechanisms()
    cases = load_yaml(CASES_YAML) or []

    # ---------- 1/2 audit_source_acquisition + detect_metadata_only_sources ----------
    sid_to_src = sources
    cited_by = {}
    for nid, (node, _) in nodes.items():
        for sid in node.get("source_ids", []) or []:
            cited_by.setdefault(sid, []).append(nid)

    src_rows = []
    metadata_only, memory_based_srcs = [], []
    for sid, s in sorted(sources.items()):
        rs = s.get("research_status", "unverified")
        row = {
            "source_id": sid,
            "title": s.get("title", ""),
            "type": s.get("type", ""),
            "access": s.get("access_level", "metadata_only"),
            "actual_read": "YES" if rs in ("read", "annotated", "validated", "distilled") else "NO",
            "evidence_use": f"cited_by_{len(cited_by.get(sid, []))}_nodes",
            "research_status": rs,
        }
        src_rows.append(row)
        if rs == "metadata_only":
            metadata_only.append(sid)
        if rs in ("memory_based", "unverified"):
            memory_based_srcs.append(sid)

    # ---------- 3 detect_memory_based_claims ----------
    memory_based_nodes, provenance_nodes = [], []
    for nid, (node, fn) in nodes.items():
        if node_validation_status(node) in ("MEMORY_BASED", "UNVERIFIED"):
            memory_based_nodes.append(nid)
        if node.get("provenance"):
            provenance_nodes.append(nid)

    # ---------- 4 detect_missing_primary_sources ----------
    no_primary = []
    for nid, (node, fn) in nodes.items():
        sids = node.get("source_ids", []) or []
        types = {sid_to_src[s].get("type") for s in sids if s in sid_to_src}
        has_primary = bool(types & PRIMARY_SOURCE_TYPES)
        has_meta = bool(node.get("evidence", {}).get("meta_analysis"))
        if not (has_primary or has_meta):
            no_primary.append(nid)

    # ---------- 5 detect_missing_counterevidence ----------
    no_counter = [nid for nid, (n, _) in nodes.items()
                  if not (n.get("evidence", {}).get("conflicting") or n.get("conflicting_nodes"))]

    # ---------- 6 detect_missing_boundaries ----------
    no_boundary = [nid for nid, (n, _) in nodes.items()
                   if not n.get("boundary_conditions") or not n.get("failure_conditions")]

    # ---------- 7 detect_uncited_claims ----------
    uncited = [nid for nid, (n, _) in nodes.items() if not (n.get("source_ids") or [])]

    # ---------- 8 detect_stale_platform_claims ----------
    adapters = []
    for path in sorted(glob.glob(os.path.join(PLATFORM_DIR, "*", "adapter.yaml"))):
        ad = load_yaml(path)
        if not ad:
            continue
        plat = ad.get("platform_name", os.path.basename(os.path.dirname(path)))
        age = months_since(ad.get("last_updated"))
        claims = ad.get("known_platform_patterns", []) or []
        n_labeled = sum(1 for c in claims if c.get("evidence_level"))
        stale_claims = sum(1 for c in claims
                           if c.get("last_verified") and (months_since(c["last_verified"]) or 0)
                           > FRESHNESS_MONTHS.get(c.get("fact_type", ""), 6))
        adapters.append({
            "platform": plat,
            "last_updated": ad.get("last_updated"),
            "last_verified": ad.get("last_verified", "未核验"),
            "months_since_update": age,
            "claims": len(claims),
            "claims_with_evidence_level": n_labeled,
            "claims_with_source_ref": sum(1 for c in claims if c.get("source_ref")),
            "stale_claims": stale_claims,
            "platform_sources_registered": len(ad.get("platform_sources") or []),
            "official_rule_claims": sum(1 for c in claims if c.get("fact_type") == "official_rule"),
        })

    # ---------- 9 detect_case_without_material ----------
    case_rows = []
    no_material = []
    for c in cases:
        has_material = bool(c.get("original_material"))
        if not has_material:
            no_material.append(c.get("case_id"))
        case_rows.append({
            "case_id": c.get("case_id"),
            "case_type": c.get("case_type"),
            "original_material": has_material,
            "outcome_status": c.get("outcome_status", "UNKNOWN"),
            "causal_status": c.get("causal_status", "unspecified"),
            "corpus_status": c.get("corpus_status", "UNVERIFIED"),
        })

    # ---------- 10 detect_single_case_generalization ----------
    case_by_mech = {}
    for c in cases:
        for m in c.get("mechanisms", []) or []:
            case_by_mech.setdefault(m, []).append(c.get("case_id"))
    single_case_risk = []
    for nid, (node, _) in nodes.items():
        n_cases = len(case_by_mech.get(nid, []))
        ev = node.get("evidence", {})
        has_research = bool(ev.get("meta_analysis") or ev.get("replication"))
        if n_cases == 1 and not has_research:
            single_case_risk.append(nid)

    # ---------- 11 detect_platform_claim_without_level ----------
    claims_total = sum(a["claims"] for a in adapters)
    claims_no_level = claims_total - sum(a["claims_with_evidence_level"] for a in adapters)
    official_no_source = claims_total - sum(a["official_rule_claims"] for a in adapters)

    # ---------- Research Gate（） ----------
    n_nodes = len(nodes)
    gate_a = round(100 * (n_nodes - len(no_primary)) / n_nodes) if n_nodes else 0
    ab_nodes = [nid for nid, (n, _) in nodes.items()
                if str(n.get("evidence_grade", "")).rstrip("+ ") in ("A", "B")
                or n.get("evidence_grade") in ("A", "A-", "B+", "B", "B-")]
    # A/B 级来源链：有 source_ids 且至少一个来源非 metadata_only = 通过
    ab_with_chain = [nid for nid in ab_nodes
                     if any((sid_to_src.get(s, {}).get("research_status")
                             in ("read", "annotated", "validated", "distilled"))
                            for s in nodes[nid][0].get("source_ids", []) or [])]
    gate_b = round(100 * len(ab_with_chain) / len(ab_nodes)) if ab_nodes else 0
    gate_c = round(100 * sum(a["claims_with_source_ref"] for a in adapters) / claims_total) if claims_total else 0
    gate_d = round(100 * (len(cases) - len(no_material)) / len(cases)) if cases else 0

    # ---------- 域覆盖表（RESEARCH_COVERAGE） ----------
    domains = {}
    for nid, (node, fn) in nodes.items():
        d = node.get("domain", fn)
        dom = domains.setdefault(d, {"nodes": 0, "primary": 0, "review": 0, "cases": 0,
                                     "counter": 0, "boundaries": 0, "grades": {}})
        dom["nodes"] += 1
        sids = node.get("source_ids", []) or []
        types = {sid_to_src[s].get("type") for s in sids if s in sid_to_src}
        if types & PRIMARY_SOURCE_TYPES or node.get("evidence", {}).get("meta_analysis"):
            dom["primary"] += 1
        if types & {"handbook", "textbook"}:
            dom["review"] += 1
        dom["cases"] += len(case_by_mech.get(nid, []))
        if node.get("evidence", {}).get("conflicting") or node.get("conflicting_nodes"):
            dom["counter"] += 1
        if node.get("boundary_conditions") and node.get("failure_conditions"):
            dom["boundaries"] += 1
        g = str(node.get("evidence_grade", "?"))
        dom["grades"][g] = dom["grades"].get(g, 0) + 1

    data = {
        "audit_date": str(NOW),
        "patch_version": "research-integrity",
        "summary": {
            "total_sources": len(sources),
            "sources_metadata_only": len(metadata_only),
            "sources_read_or_beyond": len(sources) - len(metadata_only) - len(memory_based_srcs),
            "total_mechanism_nodes": n_nodes,
            "nodes_memory_based_default": len(memory_based_nodes),
            "nodes_with_provenance_block": len(provenance_nodes),
            "nodes_without_primary_evidence": len(no_primary),
            "nodes_without_counterevidence": len(no_counter),
            "nodes_without_full_boundaries": len(no_boundary),
            "nodes_uncited": len(uncited),
            "total_cases": len(cases),
            "cases_without_material": len(no_material),
            "single_case_generalization_risk": len(single_case_risk),
            "platform_claims_total": claims_total,
            "platform_claims_without_evidence_level": claims_no_level,
            "platform_adapters": len(adapters),
            "adapters_with_platform_sources": sum(1 for a in adapters if a["platform_sources_registered"] > 0),
        },
        "research_gates": {"A": gate_a, "B": gate_b, "C": gate_c, "D": gate_d},
        "domains": domains,
        "source_rows": src_rows,
        "case_rows": case_rows,
        "adapters": adapters,
        "lists": {
            "metadata_only_sources": metadata_only,
            "memory_based_nodes": memory_based_nodes,
            "nodes_without_primary_evidence": no_primary,
            "nodes_without_counterevidence": no_counter,
            "nodes_without_full_boundaries": no_boundary,
            "cases_without_material": no_material,
            "single_case_generalization_risk": single_case_risk,
        },
    }

    with open(DATA_OUT, "w", encoding="utf-8") as f:
        f.write("# 自动生成：scripts/audit_integrity.py（勿手改；重跑即刷新）\n")
        import yaml
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=110)

    # ---------- 摘要打印 ----------
    s = data["summary"]
    print("== Research Integrity Audit ==")
    print(f"  sources: {s['total_sources']}（metadata_only {s['sources_metadata_only']}，实读+ {s['sources_read_or_beyond']}）")
    print(f"  nodes: {s['total_mechanism_nodes']}（MEMORY_BASED 缺省 {s['nodes_memory_based_default']}，有 provenance {s['nodes_with_provenance_block']}）")
    print(f"  无一手证据 {s['nodes_without_primary_evidence']} · 无反例 {s['nodes_without_counterevidence']} · 边界不全 {s['nodes_without_full_boundaries']} · 无引用 {s['nodes_uncited']}")
    print(f"  cases: {s['total_cases']}（无材料 {s['cases_without_material']}）· 单案例泛化风险 {s['single_case_generalization_risk']}")
    print(f"  platform claims: {s['platform_claims_total']}（无证据级别 {s['platform_claims_without_evidence_level']}，来源登记的 adapter {s['adapters_with_platform_sources']}/{s['platform_adapters']}）")
    print(f"  Research Gates: A={gate_a}% B={gate_b}% C={gate_c}% D={gate_d}%")
    print(f"  data → {os.path.relpath(DATA_OUT, ROOT)}")

    # ---------- 回填自动表格 ----------
    if write_tables:
        import yaml as _y
        fill_marker(os.path.join(AUDITS_DIR, "SOURCE_ACQUISITION_AUDIT.md"),
                    "AUTO_SOURCE_TABLE", build_source_table(src_rows))
        fill_marker(os.path.join(AUDITS_DIR, "KNOWLEDGE_PROVENANCE_AUDIT.md"),
                    "AUTO_PROVENANCE_TABLE", build_provenance_table(nodes, sid_to_src, case_by_mech))
        print("  tables injected into SOURCE_ACQUISITION_AUDIT.md / KNOWLEDGE_PROVENANCE_AUDIT.md")
    return 0


def build_source_table(rows):
    lines = ["| Source | Type | Access | Actual Read | Evidence Use | research_status |",
             "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['source_id']} {r['title']} | {r['type']} | {r['access']} | "
                     f"{r['actual_read']} | {r['evidence_use']} | {r['research_status']} |")
    return "\n".join(lines)


def build_provenance_table(nodes, sources, case_by_mech):
    lines = ["| Node | Grade | validation_status | 一手证据 | 反例 | 边界+失效 | 引用来源 | 案例数 |",
             "|---|---|---|---|---|---|---|---|"]
    for nid, (n, fn) in sorted(nodes.items()):
        sids = n.get("source_ids", []) or []
        types = {sources[s].get("type") for s in sids if s in sources}
        primary = "Y" if (types & PRIMARY_SOURCE_TYPES or n.get("evidence", {}).get("meta_analysis")) else "N"
        counter = "Y" if (n.get("evidence", {}).get("conflicting") or n.get("conflicting_nodes")) else "N"
        bounds = "Y" if (n.get("boundary_conditions") and n.get("failure_conditions")) else "N"
        lines.append(f"| {nid} | {n.get('evidence_grade','?')} | {node_validation_status(n)} | "
                     f"{primary} | {counter} | {bounds} | {','.join(sids) or '—'} | {len(case_by_mech.get(nid, []))} |")
    return "\n".join(lines)


def fill_marker(path, marker, content):
    if not os.path.exists(path):
        return
    begin, end = f"<!-- BEGIN:{marker} -->", f"<!-- END:{marker} -->"
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if begin not in text or end not in text:
        return
    head, rest = text.split(begin, 1)
    _, tail = rest.split(end, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + begin + "\n" + content + "\n" + end + tail)


if __name__ == "__main__":
    sys.exit(main())
