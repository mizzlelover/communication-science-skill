#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建 R1 净室工作区（盲测执行者专用环境，补丁 §2 材料隔离）。

产出目录包含：AGENTS.md（= SKILL.md，Codex 自动加载）+ knowledge/platforms/
workflows/schemas（正常使用形态的按需加载集）+ blind_cases/（盲测包）+ answers/。
**物理上不含** evals（expected_behavior）、audits、FINAL_REPORT、CHANGELOG、rubrics
——R1 接触即数据作废。

用法：python3 scripts/make_r1_workspace.py [--pack <pack_dir>] [--out <dir>]
"""
import argparse
import os
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COPY_DIRS = ["knowledge", "platforms", "workflows", "schemas"]
FORBIDDEN = ["evals", "audits", "FINAL_REPORT.md", "CHANGELOG.md", "README.md",
             "INDEX.md", "research_log"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default=None, help="盲测包目录（默认取 evals/blind 下最新）")
    ap.add_argument("--out", default=os.path.join(BASE, "evals", "blind", "r1_workspace"))
    args = ap.parse_args()

    pack = args.pack
    if not pack:
        root = os.path.join(BASE, "evals", "blind")
        packs = sorted((d for d in os.listdir(root)
                        if d.startswith("pack_") and
                        os.path.isdir(os.path.join(root, d))), reverse=True)
        pack = os.path.join(root, packs[0])
    out = args.out if os.path.isabs(args.out) else os.path.join(BASE, args.out)

    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, "answers"), exist_ok=True)

    # 1) AGENTS.md = SKILL.md（Codex 自动加载；Trae 手动粘贴同文）
    shutil.copyfile(os.path.join(BASE, "SKILL.md"), os.path.join(out, "AGENTS.md"))

    # 2) 知识库与工作流（正常使用形态的加载集）
    for d in COPY_DIRS:
        shutil.copytree(os.path.join(BASE, d), os.path.join(out, d))

    # 3) 盲测包 → blind_cases/
    shutil.copytree(pack, os.path.join(out, "blind_cases"))

    # 4) 隔离自检：净室内禁止出现逐案答案字段（SKILL 自身质检用语不算泄漏）
    leak = []
    for root, _, files in os.walk(out):
        for fn in files:
            if fn.endswith((".md", ".yaml", ".yml")):
                p = os.path.join(root, fn)
                text = open(p, encoding="utf-8").read()
                for kw in ("expected_behavior", "scoring_focus", "blind_protocol",
                           "rubrics/"):
                    if kw in text:
                        leak.append((os.path.relpath(p, out), kw))
    # 5) 防漏清单确认
    for bad in FORBIDDEN:
        assert not os.path.exists(os.path.join(out, bad)), f"净室泄漏: {bad}"

    n_cases = len([f for f in os.listdir(os.path.join(out, "blind_cases"))
                   if f.startswith("blind_")])
    print(f"R1 净室工作区: {out}")
    print(f"  盲测案例: {n_cases} · 泄露自检: {'FAIL ' + str(leak[:3]) if leak else 'OK'}")
    print("  下一步：见 evals/BLIND_TEST_GUIDE.md「环境实操」——Codex 或 Trae 打开本目录执行")


if __name__ == "__main__":
    main()
