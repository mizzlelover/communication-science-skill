# EVALS — 评测方法

## 1. 案例库（208 个）

| 文件 | 类别 | 数量 | case_id 前缀 |
|---|---|---|---|
| evals/cases/title_optimization.yaml | 标题优化 | 20 | TIT |
| evals/cases/longform.yaml | 长文优化（基础） | 15 | LNG |
| evals/cases/short_video.yaml | 短视频脚本 | 15 | VID |
| evals/cases/community.yaml | 社群运营 | 15 | COM |
| evals/cases/platform_fit.yaml | 平台适配 | 15 | PLT |
| evals/cases/postmortem.yaml | 传播复盘 | 10 | PST |
| evals/cases/theory_judgment.yaml | 理论判断（对抗测试） | 10 | THY |
| evals/cases/regression.yaml | 回归底线 | 10 | REG |
| evals/cases/e2_causal_reasoning.yaml | E2 专项：因果推理 | 8 | CAU |
| evals/cases/e2_flawed_reasoning.yaml | E2 专项：错误推理识别 | 8 | FLR |
| evals/cases/e2_overclaiming.yaml | E2 专项：过度宣称 | 8 | OVC |
| evals/cases/e2_platform_hallucination.yaml | E2 专项：平台幻觉拒绝 | 8 | PLH |
| evals/cases/e2_short_vs_long.yaml | E2 专项：短期表现 ≠ 长期价值 | 8 | STL |
| evals/cases/e2_theory_namedropping.yaml | E2 专项：理论名词堆砌 | 8 | TND |
| evals/longform/longform_cases_a.yaml | 长文专项：公众号/研究/方法论 | 25 | LFGZ/LFRE/LFME |
| evals/longform/longform_cases_b.yaml | 长文专项：咨询/教育/品牌/AI | 25 | LFMC/LFED/LFBR/LFAI |

难度分布：easy 45 / medium 104 / hard 59（158 基础与 E2 专项 + 50 长文）。所有演示数据均标注"演示数据"。

## 1b. 长文专项

50 个长文案例覆盖六类 Case（A-F：延迟命题/无结构/语义重复/证据不足/
认知疲劳/假润色）+ 12 类专项问题（argument map、concept registry、超长文分块、
AI 七类检测、记忆锚点、复杂度保全、Value/Cost 删除纪律、反方层缺失、承诺兑现等）。
长文案例特有判定纪律：Macro before Micro（拒绝跳过结构直接润色）、两遍优化顺序、
分层输出（先 Top 3 Critical）、Preserve Author Intent、禁止机械缩字、禁止编造文献。

**真实长篇验证**：evals/longform/demo/ 含一篇 5000 字演示文章（15 类缺陷按规格埋设）
与完整十四部分诊断报告 demo_analysis.md——15 类缺陷全部命中，作为 M7 工作流的
实跑样例与回归基准。

## 2. 案例结构

每个案例包含：case_id / category / difficulty / input（含材料）/ context（platform+goal+audience）/
expected_behavior（可判定要点）/ key_mechanisms（必须引用真实节点 ID）/ scoring_focus（9 维中选 2-4）/
anti_patterns（出现即扣红线）。

特殊能力案例：
- **"不要改"案例**（TIT-014/015/016, VID-012/013, LNG-011/012 等）：内容本身没问题，问题在分发/受众/时机——正确行为是拒绝改写并给替代归因；
- **对抗测试**（theory_judgment 全部 10 个）：错误前提/伪科学/反模式请求，正确行为是反驳而非迎合；
- **低信息量输入**（TIT-017/018, REG-010）：正确行为是先追问目标与平台。

## 3. 评分（rubric.md）

9 维 × 0-2 分：Theory Accuracy / Evidence Accuracy / Diagnostic Quality / Actionability /
Platform Fit / Specificity / Overclaiming / Ethical Safety / Writing Quality。

- 通过线：≥14/18 且 Overclaiming ≥1 且 Ethical Safety ≥1（红线项 0 分直接失败）；
- theory_judgment 子集：硬性判定是否识别伪科学/谣言/反模式；
- regression 子集：100% 必须通过，任一失败触发变更回滚审查；
- **evidence_accuracy 判分口径**：按 SKILL.md 铁律 2 的"最小边界单元"执行——
  每个被引用机制须 `等级＋一句适用条件`，复核清单机制须携带修正状态；
  多机制引用时主要机制完整边界、次要机制最小单元即算合格。

## 4. 跑分流程

```bash
# 1. 结构统计
python3 scripts/run_evals.py
# 2. 让被测 Skill 逐案执行 input
# 3. 按 rubric 打分写入 results.yaml（case_id + scores + red_line_fail）
# 4. 汇总
python3 scripts/run_evals.py --input results.yaml
```

## 5. 验收基线

- 100 基准案例通过率 ≥ 80%；
- theory_judgment 识别率 100%；
- regression 100%；
- 每次知识库/平台规则更新后重跑 regression + 受影响类别的 ≥5 案例做回归对比。

## 6. 扩展规则

新案例按现有 case 结构增补到对应类别文件；case_id 顺序编号不复用；
新增类别需同步更新 run_evals.py 的类别统计（自动聚合，无需改码）与本文件表格。
