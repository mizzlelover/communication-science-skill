# EVIDENCE.md — 证据等级体系

本库所有机制节点必须标注 evidence_grade。等级只描述**当前最佳证据状态**（Current Best Evidence），
不是对"真理"的判定；新证据出现时等级必须更新（见 CHANGELOG 的 evidence version）。

## A — Strong（强证据）
- 多个独立研究团队支持；
- 有 Meta-analysis 或 Systematic review；
- 有高质量预注册复制；
- 跨人群、跨情境相对稳定。
- 用法：可作为强建议的核心依据。

## B — Moderate（中等证据）
- 有多项研究支持，效应存在；
- 但 effect size 中等或偏小，边界条件明显；
- 部分复制有波动。
- 用法：可作为建议主要依据，但必须同时给出边界条件。

## C — Emerging / Contextual（新兴/情境依赖）
- 有研究依据，但样本或情境有限；
- 尚缺大量独立复制；
- 机制理论合理但实证尚薄（如多数 AI 时代新现象）。
- 用法：建议时必须明示"情境依赖、证据尚新"。

## D — Practitioner Heuristic（从业者经验）
- 行业共识、案例型知识、无系统科学检验；
- 可能真实有效，也可能被幸存者偏差美化。
- 用法：**必须显式标注"实践经验，非实证结论"**；不得写成科学规律。

## E — Contested / Weak（有争议/弱）
- 复制失败、存在严重方法学争议、或被营销过度宣传。
- 用法：**默认不得作为强建议依据**；仅在讨论"为什么这个说法不可靠"时引用。

## 证据感知型知识蒸馏（Evidence-Aware Knowledge Distillation）

回答的问题不是"某本书说了什么"，而是"关于某一机制，目前最可靠的知识是什么"：

```text
多个来源 → Candidate Claims → Normalize（统一术语）
→ Merge（跨来源合并，先查重） → Conflict Detection（冲突登记）
→ Evidence Evaluation（定级） → Mechanism Node（入图）
```

## 复制危机敏感清单（重点复核对象）

以下经典结论已登记于 `evidence/classic_rechecks/rechecks_registry.yaml`（2026-09-09 落盘；
），使用时必须携带修正状态：

| 结论 | 状态摘要 | 等级趋势 |
|---|---|---|
| Semantic/Language priming（行为层） | 大规模复制失败，效应远小于原始报告 | E→谨慎 |
| Ego depletion | 大规模预注册复制失败；机制存疑 | E |
| Power posing | 感受效应有、生理/行为效应复制失败 | E |
| Loss aversion | 存在但幅度有争议，个体差异大；或主要为框架效应产物 | B（降级自 A） |
| Scarcity（带宽税） | 大相关+实验证据，但部分大规模复制效应缩水 | B/C |
| Nudge 平均效应 | Maier et al. 2022：控制发表偏差后效应大幅缩水，部分政策有效 | C（按具体 nudge 分） |
| Social proof | 基础效应稳健（A-），但效果受规范类型与身份匹配调节 | A- |
| Mere exposure | Meta-analysis 稳健，但单调重复会衰减 | A- |
| Emotional contagion | 存在；线上大田野实验（Kramer 2014）有伦理争议 | B |
| Choice overload | Meta-analysis 显示平均效应≈0，有明确调节变量（Mochon 等） | B（条件化） |
| "人类注意力只有 8 秒" | 无原始研究支持，为媒体讹传；Gloria Mark 数据被误读 | 谣言，不采用 |
| "金鱼注意力"比较 | 无学术来源，纯营销讹传 | 谣言，不采用 |

> 复核来源登记（2026-09 实取，见 evidence_packages/）：ego depletion ← S125（Hagger et al. 2016 RRR，23 实验室/2141 人，效应≈0）；priming ← S126（Doyen et al. 2012，行为启动复制失败+期望效应）；power posing ← S127（Ranehill et al. 2015，N=200，激素/行为失败、自报感受保留）；scarcity ← S128（Mani et al. 2013 Science 原始论文）+ Carvalho 2016/Shah 2023 边界；loss aversion ← S113（K&T 1979 原始）+ S129（Gal & Rucker 2018 批判）+ Camerer 2024 元分析（系数 1.955 [1.820, 2.102]）。

## 证据等级判定留痕（EVIDENCE_GRADE_JUSTIFICATION）

等级必须来自证据，而不是模型感觉。A/B/C 级节点必须能在 `grade_justification` 中回答
"为什么给这个等级"：

```yaml
evidence_grade: B
justification:
  independent_studies: 多项独立研究支持
  effect_size: 中等偏小
  replication_status: 部分复制波动
  context_dependency: 边界条件明显
```

不得以"因为它很经典"作为定级理由。升降级原因（如复制危机修正）必须记录
`downgrade_upgrade_reason`。当前实况（2026-09-09）：grade_justification
147/216 · downgrade_upgrade_reason 145/216——尚有 69 个节点（多为 P0/MEMORY_BASED）
无定级留痕，按"引用时如实标注记忆级"纪律运行，升级随一手 EP 建包推进。

## 知识半衰期与证据新鲜度分开

- **knowledge_half_life** 分层：very_long（人类认知：working memory / social identity）
  · long · medium · short · very_short（平台算法 / AI 环境现象）
- 人类认知机制不需要每 3 个月重研；X 算法 / 小红书搜索机制 / YouTube 推荐需要频繁复核
- 复审频率按半衰期分层设定，不做一刀切；平台类知识另受 PLATFORM_FRESHNESS_AUDIT
  阈值约束（official 12 月 · algorithm 3-6 月 · UI 1-3 月）

规则：
1. 经典结论被修正时，**保留修正**而非保留旧结论；
2. 无法核实出处的心理学断言不得入库；
3. 营销行业"爆款玄学"一律按 D 或 E 处理；
4. 节点降级/升级必须在 CHANGELOG evidence version 留痕。
