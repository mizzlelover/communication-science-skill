# Workflow: Long-form Evidence Audit（长文证据审计）

用途：对长文执行证据架构审计。既用于诊断阶段（Evidence Problems 输出），
也用于优化阶段（Expand 时的补强方向）。证据等级体系复用根目录 EVIDENCE.md（A-E）与
citation 纪律（禁止编造出处，无法核实标 verification_required）。

## 1. 建 Evidence Map

从 argument map 的每个 Claim 出发，把全文证据分入十一类并标注强度：

```text
Theory / Meta-analysis / Systematic Review / Experimental Evidence /
Observational Evidence / Survey / Statistics / Case Study / Expert Opinion /
Anecdote / Author Interpretation
```

对每个重要 Claim 追问：**它到底靠什么支撑？**

## 2. Evidence-to-Claim Matching

| 缺陷 | 特征 | 处理建议 |
|---|---|---|
| **Evidence Too Weak** | 一个案例（anecdote/case_study）支撑普遍规律（overclaim） | 降级主张表述（"在X情境下可能"）或标注需要更强证据；不得用更多案例堆叠替代（那是 Evidence Redundancy） |
| **Evidence Too Far** | 数据与结论之间逻辑距离过长（调查数据推因果、相关性说成因果） | 指出推理断点（logical_gap）；建议补对照/机制论证或弱化结论 |
| **Evidence Redundancy** | 多个案例证同一件事，无新增信息 | 保留信息量最大的一例，其余 Cut 或一笔带过（同源原则） |
| **Citation Decoration** | "研究表明"不说什么研究 | 要求作者补来源；无法补则降级为 author_interpretation 并明示 |
| **Evidence Dumping** | 证据堆叠但不指向任何 Claim | 归位到对应 Claim 或 Cut（knowledge/anti_patterns/longform_anti_patterns.yaml: evidence_dumping） |

## 3. Counterargument Layer

对核心 Claim 检查三件套：
```yaml
counterargument:        # 最强的反方观点是什么
alternative_explanation: # 同一现象的其他解释
boundary_condition:     # 主张在什么条件下不成立
```
高质量长文不能只有单向论证。原文缺失时建议加入"这并不意味着……"式限定，
防止过度外推（overclaim/conclusion_leap 的主要解药）。

## 4. Long-form Trust System

逐项评估并给 1-10 分（附原因）：authority / evidence / specificity / transparency /
intellectual honesty / uncertainty / counterargument / source quality。
重点：大量"研究表明"无来源是长文信任的头号杀手；对不确定结论是否明示了不确定性
（uncertainty 是信任资产，不是弱点——trust_calibration（B））。

## 5. 与知识库的联动

- 审计中引用证据等级时使用 EVIDENCE.md 口径（A/A-/B+/B/B-/C/D/E）；
- 经典理论复核清单中的条目（loss_aversion、nudge、choice_overload、ego depletion 等）
  被文章引用时，检查文章是否携带修正状态——使用过时结论本身记为 evidence 问题；
- 建议补强时只指向真实存在的证据类型与来源方向，**禁止编造具体文献/数据**；
  可建议"补 meta-analysis 级证据"但不可虚构其内容。

## 输出格式

```text
## Evidence Map 摘要
（Claim → 证据类型×强度 总览；最薄弱的 3 个 Claim）
## Evidence Problems（P0-P3）
（每条：位置 / 缺陷类型 / **对应 AP-LF 编号**（AP-LF-004/005/011/012/017 等，便于与
Editing Plan 对账）/ 为什么 / 建议——降级表述、补反方、还是换证据）
## Counterargument Gap
（核心主张缺反方层的具体位置与建议插入点）
## Trust 评分（8 子项 + 一句总因）
## 补强清单
（需要作者补充的材料清单；区分"必须补否则降级"与"建议补"）
```

## 禁止
- 用堆叠案例解决证据不足（Evidence Redundancy）；
- 建议作者引用具体"研究"却无法指明真实存在的研究方向（编造出处）；
- 把 anecdote 当 experimental 级证据使用。
