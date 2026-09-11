#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""平台知识时效检测（补丁 §60：detect_stale_platform_claims）。

扫描 platforms/*/adapter.yaml 中一切带 last_verified / last_updated 的事实断言，
按证据类别应用不同时效阈值，输出过期清单：

  official_rule / official        → 12 个月
  verified_observation            → 6 个月
  industry_consensus              → 6 个月
  experience_speculation          → 3 个月

用法：
  python3 scripts/detect_stale_platform_claims.py            # 报告
  python3 scripts/detect_stale_platform_claims.py --strict   # 有过期条目时退出码 1
"""
import glob
import os
import sys
from datetime import datetime

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THRESHOLD_MONTHS = {
    "official_rule": 12, "official": 12, "L1": 12, "l1_official_rule": 12,
    "verified_observation": 6, "L2": 6, "l2_verified_observation": 6,
    "industry_consensus": 6, "L3": 6, "l3_industry_consensus": 6,
    "experience_speculation": 3, "L4": 3, "l4_experience_speculation": 3,
}
LEVEL_KEYS = ("fact_type", "evidence_level", "evidence_type", "level")
DATE_KEYS = ("last_verified", "last_updated", "verified_date", "accessed_date")


def parse_date(v):
    s = str(v)[:7]  # 取 YYYY-MM
    try:
        return datetime.strptime(s, "%Y-%m")
    except ValueError:
        return None


def months_since(d):
    now = datetime.now()
    return (now.year - d.year) * 12 + (now.month - d.month)


def walk(node, path, hits):
    """递归收集一切同时带日期键与级别键的映射（断言条目）。"""
    if isinstance(node, dict):
        date_v = next((node[k] for k in DATE_KEYS if node.get(k)), None)
        lvl_v = next((node[k] for k in LEVEL_KEYS if node.get(k)), None)
        if date_v and lvl_v:
            hits.append((path, str(lvl_v), parse_date(date_v), date_v))
        for k, v in node.items():
            walk(v, f"{path}.{k}", hits)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", hits)


def main():
    strict = "--strict" in sys.argv
    stale, undated, total = [], [], 0
    for f in sorted(glob.glob(os.path.join(BASE, "platforms", "*", "adapter.yaml"))):
        platform = f.split(os.sep)[-2]
        d = yaml.safe_load(open(f, encoding="utf-8"))
        hits = []
        walk(d, platform, hits)
        for path, lvl, dt, raw in hits:
            total += 1
            if dt is None:
                undated.append((path, lvl, raw))
                continue
            months = months_since(dt)
            threshold = THRESHOLD_MONTHS.get(lvl.lower(), 12)
            if months > threshold:
                stale.append((path, lvl, raw, months, threshold))
    print(f"扫描平台断言（带日期+级别）: {total} 条")
    print(f"过期（超阈值）: {len(stale)} 条 | 缺日期: {len(undated)} 条")
    for path, lvl, raw, months, th in stale:
        print(f"  STALE {path} [{lvl} @ {raw}] 已 {months} 个月 > 阈值 {th} 个月")
    for path, lvl, raw in undated[:10]:
        print(f"  UNDATED {path} [{lvl}] {raw}")
    if not stale and not undated:
        print("✓ 全部平台断言在时效内且带日期。")
    if strict and (stale or undated):
        sys.exit(1)


if __name__ == "__main__":
    main()
