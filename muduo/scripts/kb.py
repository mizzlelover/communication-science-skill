#!/usr/bin/env python3
"""kb.py — 共享加载与检查工具库（供 scripts/ 各脚本复用）。"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MECH_DIR = os.path.join(ROOT, "knowledge", "mechanisms")
SOURCES_YAML = os.path.join(ROOT, "knowledge", "sources", "source_registry.yaml")
EVIDENCE_DIR = os.path.join(ROOT, "knowledge", "sources", "evidence_packages")
DOMAINS_INDEX = os.path.join(ROOT, "knowledge", "domains", "_index.yaml")
PLATFORM_DIR = os.path.join(ROOT, "platforms")
EVAL_CASES_DIR = os.path.join(ROOT, "evals", "cases")
CASES_YAML = os.path.join(ROOT, "knowledge", "cases", "cases.yaml")
ANTI_DIR = os.path.join(ROOT, "knowledge", "anti_patterns")
CONFLICTS_YAML = os.path.join(ROOT, "knowledge", "evidence", "conflicts", "conflicts_index.yaml")

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("需要 PyYAML：pip install pyyaml\n")
    raise

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_sources():
    data = load_yaml(SOURCES_YAML)
    return {s["source_id"]: s for s in data["sources"]}

def load_mechanisms():
    """返回 {node_id: (node, file)} 与 {file: file_data}"""
    nodes, files = {}, {}
    for fn in sorted(os.listdir(MECH_DIR)):
        if not fn.endswith(".yaml"):
            continue
        path = os.path.join(MECH_DIR, fn)
        data = load_yaml(path)
        files[fn] = data
        for node in data.get("nodes", []):
            nid = node.get("id")
            if nid:
                nodes[nid] = (node, fn)
    return nodes, files

def load_eval_cases():
    """扫描 evals/cases/ 与 evals/longform/ 下的全部 *.yaml 案例。"""
    cases = []
    dirs = [EVAL_CASES_DIR, os.path.join(ROOT, "evals", "longform")]
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".yaml"):
                continue
            data = load_yaml(os.path.join(d, fn))
            items = data if isinstance(data, list) else data.get("cases", [])
            for c in items:
                if isinstance(c, dict):
                    cases.append((c, f"evals/{os.path.relpath(os.path.join(d, fn), os.path.join(ROOT, 'evals'))}"))
    return cases

def load_anti_patterns():
    """扫描 anti_patterns/ 目录下全部 *.yaml。"""
    out = []
    for fn in sorted(os.listdir(ANTI_DIR)):
        if not fn.endswith(".yaml"):
            continue
        data = load_yaml(os.path.join(ANTI_DIR, fn))
        items = data if isinstance(data, list) else data.get("anti_patterns", [])
        out.extend([a for a in items if isinstance(a, dict)])
    return out

GRADE_ENUM = {"A", "A-", "B+", "B", "B-", "C", "D", "E"}
GRADE_ORDER = {"E": 0, "D": 1, "C": 2, "B-": 3, "B": 4, "B+": 5, "A-": 6, "A": 7}

def err(msg):
    print(f"  [FAIL] {msg}")
    return 1

def warn(msg):
    print(f"  [WARN] {msg}")
    return 0
