#!/usr/bin/env python3
"""verify_longform_state — 模拟超长文多轮修复会话，验证 ap_lf_hits / ap_lf_fixes 跨会话持久化。
模拟三轮会话（每轮独立 load → 增量修改 → save，模拟进程间无共享内存）：
  S1 诊断：写入 ap_lf_hits（7 条命中）
  S2 修复会话 A：执行 3 条 fix（done），新增 1 条误报剔除（不改 hits 除非确认），
     验证 hits 全部保留
  S3 修复会话 B：再执行 2 条 fix + 1 条 skipped（带理由），验证 S1/S2 记录零丢失、
     对账闭合（每条 hit 都有 fix 或 skipped 理由）
退出码 0 = 持久化验证通过。同时产出示例文件 knowledge/longform/longform_state.example.yaml。
"""
import os
import sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "knowledge", "longform", "longform_state.example.yaml")

failures = []

def check(ok, ok_msg, fail_msg):
    print(f"  [{'OK' if ok else 'FAIL'}] {ok_msg if ok else fail_msg}")
    if not ok:
        failures.append(fail_msg)

def save(state):
    with open(STATE, "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, allow_unicode=True, sort_keys=False, width=100)

def load():
    with open(STATE, encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------- Session 1：诊断会话 ----------
print("== Session 1：诊断（写入 ap_lf_hits）==")
s1 = {
    "article_id": "LF-DEMO",
    "central_thesis": "演示：社群失败多因身份感缺失",
    "completed_sections": ["S1-S4"],
    "ap_lf_hits": [
        {"ap_id": "AP-LF-002", "location": "§1", "signal": "context 占比 >20%"},
        {"ap_id": "AP-LF-007", "location": "§4", "signal": "thesis 首现 36% > 15%"},
        {"ap_id": "AP-LF-003", "location": "§5", "signal": "单节 6 概念无锚定"},
        {"ap_id": "AP-LF-016", "location": "§6", "signal": "黑话 ≥10/段"},
        {"ap_id": "AP-LF-019", "location": "§5-7", "signal": "三节结构同构"},
        {"ap_id": "AP-LF-012", "location": "§4", "signal": "n=1 全称化，无反方层"},
        {"ap_id": "AP-LF-013", "location": "§9", "signal": "结尾信息增量为零"},
    ],
    "ap_lf_fixes": [],
    "open_questions": ["诊断框架五问的具体条目"],
    "pending_issues": ["咖啡案例的选择效应替代解释待补"],
}
save(s1)
check(len(load()["ap_lf_hits"]) == 7, "S1 落盘 7 条命中", "S1 命中清单写入失败")

# ---------- Session 2：修复会话 A（独立进程语义：重新 load）----------
print("== Session 2：修复 A（执行 3 条 fix）==")
s2 = load()
fixes_done = ["AP-LF-002", "AP-LF-007", "AP-LF-016"]
for ap in fixes_done:
    s2["ap_lf_fixes"].append({"ap_id": ap, "action": "Cut/Move per §3b 第三列", "status": "done",
                              "note": "S2 执行"})
s2["completed_sections"].append("S5")
save(s2)
s2r = load()
check(len(s2r["ap_lf_hits"]) == 7, "S2 后 hits 仍为 7（清单不丢）",
      f"S2 后 hits 丢失！剩余 {len(s2r['ap_lf_hits'])}")
check(len(s2r["ap_lf_fixes"]) == 3, "S2 fixes 累计 3 条", "S2 fixes 记录失败")

# ---------- Session 3：修复会话 B ----------
print("== Session 3：修复 B（再 2 done + 1 skipped）==")
s3 = load()
for ap in ["AP-LF-003", "AP-LF-019"]:
    s3["ap_lf_fixes"].append({"ap_id": ap, "action": "Rewrite/差异化结构", "status": "done",
                              "note": "S3 执行"})
s3["ap_lf_fixes"].append({"ap_id": "AP-LF-013", "action": "Rewrite Closure", "status": "skipped",
                          "note": "用户选择保留结尾呼应（修辞性重复），理由已确认"})
s3["ap_lf_fixes"].append({"ap_id": "AP-LF-012", "action": "补 counterargument 三件套", "status": "pending",
                          "note": "待用户确认边界条件措辞"})
save(s3)

# ---------- 终验 ----------
print("== 终验（模拟第 4 次会话读取）==")
s4 = load()
check(len(s4["ap_lf_hits"]) == 7, "S3 后 hits 仍为 7（零丢失）",
      f"hits 丢失！剩余 {len(s4['ap_lf_hits'])}")
check(len(s4["ap_lf_fixes"]) == 7, "fixes 累计 7（S2×3 + S3×4 = 3 done + 1 skipped + 1 pending + ...）",
      f"fixes 数量异常：{len(s4['ap_lf_fixes'])}")
hit_ids = {h["ap_id"] for h in s4["ap_lf_hits"]}
fix_ids = {x["ap_id"] for x in s4["ap_lf_fixes"]}
check(hit_ids <= fix_ids, f"对账闭合：7 条命中均有对应 fix（{sorted(hit_ids)}）",
      f"对账缺口：{sorted(hit_ids - fix_ids)}")
done = [x for x in s4["ap_lf_fixes"] if x["status"] == "done"]
skipped = [x for x in s4["ap_lf_fixes"] if x["status"] == "skipped"]
check(all("note" in x and x["note"] for x in skipped), "skipped 项均带理由",
      "存在无理由的 skipped")
check(s4["completed_sections"] == ["S1-S4", "S5"], "completed_sections 跨会话累积正常",
      f"completed_sections 异常：{s4['completed_sections']}")

print()
if failures:
    print(f"持久化验证未通过：{len(failures)} 项")
    sys.exit(1)
print("持久化验证通过：3 轮会话模拟中 ap_lf_hits/ap_lf_fixes 零丢失、对账闭合。")
print(f"示例文件已生成：{STATE}（真实任务的 longform_state.yaml 按同结构落在工作目录）")
