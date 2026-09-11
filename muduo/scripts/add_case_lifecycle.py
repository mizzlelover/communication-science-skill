#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""社群案例生命周期字段补齐（补丁 §32）。

为 100 个 community_case 生成 lifecycle 结构块，九阶段逐一映射：
  能从现有字段（context/goal/intervention/result）定位到内容 → 摘录出处与片段
  材料未覆盖 → "not_documented（材料未覆盖该阶段）"

不虚构任何新事实：lifecycle 是既有材料按生命周期的结构化索引。

用法：python3 scripts/add_case_lifecycle.py [--dry-run]
"""
import os
import sys

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHASES = ["formation", "early_growth", "norm_creation", "role_structure",
          "participation", "conflict", "moderation", "retention",
          "decline_or_scale"]
NOT_DOC = "not_documented（材料未覆盖该阶段）"
ROUTE = {
    "formation": (["context"], ["成立", "创建", "发起", "起源", "起步", "初期", "冷启动", "组建"]),
    "early_growth": (["context", "result"], ["增长", "扩张", "拉新", "起量", "破圈", "走红"]),
    "norm_creation": (["intervention", "context"], ["规范", "规则", "公约", "礼仪", "共识", "契约"]),
    "role_structure": (["intervention", "context"], ["角色", "版主", "管理员", "阶梯", "晋升", "身份", "头衔", "committer", "maintainer"]),
    "participation": (["result", "intervention"], ["参与", "发言", "活跃", "互动", "贡献", "投稿", "讨论"]),
    "conflict": (["result", "context"], ["冲突", "争执", "吵架", "对立", "骂战", "纠纷"]),
    "moderation": (["intervention", "result"], ["审核", "治理", "管理", "删帖", "封禁", "仲裁", "moderation"]),
    "retention": (["result"], ["留存", "流失", "回头", "复访", "保留", "沉淀", "持续"]),
    "decline_or_scale": (["result", "context"], ["衰落", "沉寂", "转型", "规模化", "扩张", "稀释", "冷清"]),
}


def excerpt(text, kws, width=90):
    """返回首个命中关键词的片段（含前后文），找不到返回 None。"""
    t = str(text)
    low = t.lower()
    for kw in kws:
        i = low.find(kw.lower())
        if i >= 0:
            start = max(0, i - 20)
            frag = t[start:i + width].replace("\n", " ")
            return ("…" if start > 0 else "") + frag
    return None


def main():
    dry = "--dry-run" in sys.argv
    f = os.path.join(BASE, "knowledge", "cases", "cases.yaml")
    d = yaml.safe_load(open(f, encoding="utf-8"))
    cases = d["cases"] if isinstance(d, dict) and "cases" in d else d
    done = 0
    for c in cases:
        if c.get("case_type") != "community_case" or c.get("lifecycle"):
            continue
        lc = {}
        for phase in PHASES:
            fields, kws = ROUTE[phase]
            found = None
            for fld in fields:
                hit = excerpt(c.get(fld, ""), kws)
                if hit:
                    found = f"[{fld}] {hit}"
                    break
            lc[phase] = found or NOT_DOC
        c["lifecycle"] = lc
        done += 1
    if not dry:
        yaml.dump(d, open(f, "w", encoding="utf-8"),
                  allow_unicode=True, sort_keys=False, width=100)
    covered = sum(1 for c in cases if c.get("case_type") == "community_case"
                  and c.get("lifecycle")
                  and any(v != NOT_DOC for v in c["lifecycle"].values()))
    print(f"community_case lifecycle 补齐: {done} 条（dry-run={dry}）；"
          f"至少一个阶段有材料覆盖: {covered} 条，其余为诚实 not_documented")


if __name__ == "__main__":
    main()
