#!/usr/bin/env python3
"""make_blind_pack — 生成第三方盲测包（盲测协议 Step 1）。
从 eval 案例生成只含 input/context/作答指令 的盲测文件（物理隔离 expected_behavior/
key_mechanisms/anti_patterns）。用法：
  python3 scripts/make_blind_pack.py                     # 全量
  python3 scripts/make_blind_pack.py --sample 30         # 分层抽样 30 案
  python3 scripts/make_blind_pack.py --only regression,theory_judgment
"""
import argparse
import hashlib
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime

from kb import load_eval_cases, ROOT

OUT_BASE = os.path.join(ROOT, "evals", "blind")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0, help="分层抽样数量（按类别等比）")
    ap.add_argument("--only", default="", help="逗号分隔的类别过滤")
    args = ap.parse_args()

    cases = load_eval_cases()
    if args.only:
        cats = set(args.only.split(","))
        cases = [(c, f) for c, f in cases if c.get("category") in cats]

    if args.sample and args.sample < len(cases):
        by_cat = defaultdict(list)
        for c, f in cases:
            by_cat[c.get("category")].append((c, f))
        picked, ratio = [], args.sample / len(cases)
        for cat, items in sorted(by_cat.items()):
            k = max(1, round(len(items) * ratio))
            picked.extend(items[:k])  # 按 ID 序取前 k 个（可复现，无随机）
        cases = picked

    date = datetime.now().strftime("%Y%m%d")
    tag = ""
    if args.only:
        tag += "_" + args.only.replace(",", "-")
    if args.sample:
        tag += f"_sample{args.sample}"
    out_dir = os.path.join(OUT_BASE, f"pack_{date}{tag}")
    os.makedirs(out_dir, exist_ok=True)

    manifest = {"generated_at": datetime.now().isoformat(timespec="seconds"),
                "pack_sha": "", "count": len(cases), "categories": Counter(), "cases": []}
    for c, src in cases:
        cid = c.get("case_id", "UNKNOWN")
        content = (
            f"<!-- blind pack {date} | source: {src} -->\n\n"
            f"# 盲测案例 {cid}\n\n"
            f"## 你的任务\n\n"
            f"以「人类传播与社群增长引擎」Skill 的正常工作方式回答以下用户请求。\n"
            f"只依据 SKILL.md 与知识库的正常加载流程，输出你实际会给用户的完整回答。\n\n"
            f"## 用户请求与材料\n\n{c.get('input', '').strip()}\n\n"
            f"## 场景\n\n- 平台：{c.get('context', {}).get('platform', '未指定')}\n"
            f"- 目标：{c.get('context', {}).get('goal', '未指定')}\n"
            f"- 受众：{c.get('context', {}).get('audience', '未指定')}\n"
        )
        fn = f"blind_{cid}.md"
        with open(os.path.join(out_dir, fn), "w", encoding="utf-8") as f:
            f.write(content)
        h = hashlib.sha256(content.encode()).hexdigest()[:12]
        manifest["cases"].append({"case_id": cid, "file": fn, "sha": h})
        manifest["categories"][c.get("category")] += 1

    manifest["categories"] = dict(manifest["categories"])
    import yaml
    mpath = os.path.join(out_dir, "_manifest.yaml")
    mtext = yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False)
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(mtext)
    manifest["pack_sha"] = hashlib.sha256(mtext.encode()).hexdigest()[:12]
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False))

    print(f"盲测包已生成：{out_dir}")
    print(f"案例数：{len(cases)}；类别分布：{manifest['categories']}")
    print(f"manifest：{mpath}（pack_sha {manifest['pack_sha']}）")
    print(f"泄露自检：盲测文件中不得出现 expected/behavior 关键字 ——",
          "OK" if not any("expected" in open(os.path.join(out_dir, m['file']), encoding='utf-8').read().lower() for m in manifest['cases']) else "FAIL！")

if __name__ == "__main__":
    main()
