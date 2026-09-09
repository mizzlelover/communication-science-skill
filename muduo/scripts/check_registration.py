#!/usr/bin/env python3
"""check_registration — 平台注册一致性检查。
1) .trae/skills/ 与 .claude/skills/ 的软链是否指向正确的 skill 目录；
2) SKILL.md 是否存在且 frontmatter 合法（name + description）；
3) AGENTS.md 与 CLAUDE.md 的「铁律速记」段是否同步（防漂移）。
用法：python3 scripts/check_registration.py ；任一项失败退出码 1。"""
import os
import re
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # muduo/
WORKSPACE = os.path.dirname(SKILL_ROOT)                                    # 项目根
LINKS = [os.path.join(WORKSPACE, ".trae", "skills", "muduo"),
         os.path.join(WORKSPACE, ".claude", "skills", "muduo")]
ROUTER_FILES = ["AGENTS.md", "CLAUDE.md"]

failures = []

def check(ok, ok_msg, fail_msg):
    print(f"  [{'OK' if ok else 'FAIL'}] {ok_msg if ok else fail_msg}")
    if not ok:
        failures.append(fail_msg)

# ---- 1. 软链 ----
print("== 软链注册 ==")
real_skill = os.path.realpath(SKILL_ROOT)
for link in LINKS:
    rel = os.path.relpath(link, WORKSPACE)
    if not os.path.lexists(link):
        check(False, "", f"{rel} 不存在（可执行: ln -sfn {SKILL_ROOT} {link}）")
        continue
    if not os.path.islink(link):
        check(False, "", f"{rel} 存在但不是软链（是目录或普通文件）")
        continue
    target = os.path.realpath(link)
    check(target == real_skill, f"{rel} -> {target}",
          f"{rel} 指向错误：{target}（应为 {real_skill}）")

# ---- 2. SKILL.md frontmatter ----
print("== SKILL.md ==")
skill_md = os.path.join(SKILL_ROOT, "SKILL.md")
if os.path.isfile(skill_md):
    head = open(skill_md, encoding="utf-8").read(600)
    fm = re.match(r"^---\s*\nname:\s*[\"']?([\w-]+)[\"']?\s*\ndescription:\s*.+", head)
    check(bool(fm), f"frontmatter 合法（name={fm.group(1) if fm else '?'}）",
          "SKILL.md frontmatter 缺失或不含 name/description")
else:
    check(False, "", "SKILL.md 不存在")

# ---- 3. 铁律速记同步 ----
print("== 路由文件铁律同步 ==")
def extract_iron_rules(path):
    if not os.path.isfile(path):
        return None
    text = open(path, encoding="utf-8").read()
    m = re.search(r"铁律速记：(.*?)(?:\n\n|\Z)", text, re.S)
    if not m:
        return None
    return re.sub(r"\s+", "", m.group(1))  # 去空白后比较，忽略换行差异

blocks = {f: extract_iron_rules(os.path.join(WORKSPACE, f)) for f in ROUTER_FILES}
for f, b in blocks.items():
    check(b is not None, f"{f} 含铁律速记段", f"{f} 未找到「铁律速记：」段落")
vals = [b for b in blocks.values() if b]
if len(vals) == len(ROUTER_FILES) and len(set(vals)) > 1:
    check(False, "", f"铁律速记漂移！各文件内容不一致: { {f: v[:40] + '...' for f, v in blocks.items()} }")
elif len(vals) == len(ROUTER_FILES):
    print(f"  [OK] {', '.join(ROUTER_FILES)} 铁律速记一致（{len(vals[0])} 字符规范化后）")

print()
if failures:
    print(f"检查未通过：{len(failures)} 项")
    sys.exit(1)
print("检查通过：软链、frontmatter、铁律同步全部正常")
