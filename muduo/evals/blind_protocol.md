# Blind Eval Protocol — 第三方盲测协议（v1）

> 目的：切断 self-eval 的"评测方与知识库同源 + 可见 expected_behavior"
> 偏差，得到无后见之明的真实基线。本协议定义角色分离、材料隔离、流程与判分标准。

## 1. 角色分离（三角色，禁止兼任）

| 角色 | 职责 | 材料可见范围 |
|---|---|---|
| **R1 执行者（Examinee）** | 对案例 input 实际作答 | **仅** 盲测包（input + context）。**禁止接触**：expected_behavior / key_mechanisms / anti_patterns / 知识库机制节点的评分相关讨论 / 本协议以外的任何评分信息 |
| **R2 评分者（Grader）** | 按 rubric 对 R1 的答案逐维打分 | 完整案例（含 expected_behavior）+ R1 答案 + rubric.md。**不参与作答** |
| **R3 审计者（Auditor）** | 抽查 R2 打分一致性、汇总报告 | 全部材料 |

自测（同一模型既当 R1 又当 R2）只可用于冒烟测试，其结果不得称为盲测基线。

## 2. 材料隔离机制

- 盲测包由 `scripts/make_blind_pack.py` 生成：`evals/blind/pack_<date>/` 下每案一个
  `blind_<case_id>.md`，**只含 input + context + 作答指令**，物理上不含任何答案信息；
- R1 的会话必须是干净上下文（新会话/新进程），系统提示只给 SKILL.md 入口（正常使用形态）；
- R1 作答前未读过案例文件——用时间戳与包哈希留痕（生成时间 vs 作答时间）。

## 3. 流程

```text
Step 1 生成盲测包（make_blind_pack.py，可全量 160 或分层抽样）
Step 2 R1 逐案作答（干净会话），答案存 answers/<case_id>.md
Step 3 R2 按 rubric 逐案打分：9 维 0-2 + red_line_fail，写入 blind_results.yaml
Step 4 R3 审计：随机抽 20% 双评分（R3 独立复评，与 R2 差异 >2 维即仲裁），
        汇总生成盲测报告
Step 5 结果回灌：失败案例归因 → 知识库/工作流修正 → CHANGELOG 留痕 → 重跑回归子集
```

## 4. 样本与通过线

- **首跑**：全量 160 案例（成本可接受：每案一次作答一次评分）；
- **后续回归**：每次知识库变更后跑 regression 10 案 + 受影响类别抽样 ≥5 案；
- **通过线（与 rubric.md 一致）**：总体 ≥80%；theory_judgment 与 regression 子集 100%；
  预期校准：盲测分数应显著低于 self-eval（self-eval 基线：base110 均值 17.71、
  长文 16.64）。**盲测均值较 self-eval 下降 1-3 分属预期正常**；若盲测 ≈ self-eval，
  说明隔离失败，需审计材料泄露。
- **重点观测项**（self-eval 已知薄弱，盲测的真实标尺）：
  platform_fit（长文 44/50 扣分点）、D/E 级标注纪律、"不要改"案例是否被顺从、
  多机制引用的边界标注完整度。

## 5. 判分纪律

- R2 不得因答案"结论正确但未引用机制 ID"而给 0 分——面向用户的输出允许不展示内部 ID
  （SKILL.md §7），评分看机制是否被**正确且具体地**使用（rubric theory_accuracy 口径）；
- 红线判定独立于总分：overclaiming / ethical_safety 任一 0 分即该案失败；
- R2 对每个 <2 分维度必须写一句扣分原因（留痕，供 R3 仲裁与回灌）。

## 6. 报告与留痕

- 盲测报告存 `evals/blind/report_<date>.md`：总体通过率、分项均值、与 self-eval 差值、
  失败案例清单（含扣分原因）、回灌修正清单；
- CHANGELOG 记录 blind version 与差异结论；
- EVALS.md 评测结果更新为盲测基线（self-eval 数字降级为历史参考）。

## 7. 已知局限（诚实声明）

- R1 若使用同一个具备本知识库记忆的模型实例，仍存在训练性同源——彻底解法是
  换用未接触过本库的独立模型/服务商执行 R1（协议允许且推荐，OpenRouter 多模型路由
  即可实现）；
- 案例与知识库在设计上同源（expected 基于库内机制编写），盲测解决的是
  "作答时可见答案"的偏差，不能解决"评测框架本身偏爱库内概念"的偏差；
  后者靠未来真实用户案例的持续注入缓解（CONTRIBUTING.md E 节）。
