# METHODOLOGY — 知识蒸馏方法（Evidence-Aware Knowledge Distillation）

## 1. 核心立场

回答的问题不是"某本书说了什么"，而是：

> **关于某一机制，目前最可靠的知识是什么？**

书籍只是知识来源。知识结构必须 Book-centric → **Theory-centric / Mechanism-centric**。

## 2. 蒸馏管道

```text
多个来源（S01-S100 + 原始论文/综述）
    ↓
Candidate Claims（候选主张：可检验的陈述）
    ↓
Normalize（统一术语：canonical English ID，中文对照展示）
    ↓
Merge（跨来源合并；先查重——已有节点不重建）
    ↓
Conflict Detection（冲突登记至 evidence/conflicts/，不强行二选一）
    ↓
Evidence Evaluation（按 EVIDENCE.md 定级 A-E，复制危机敏感清单强制复核）
    ↓
Mechanism Node（入图：related_nodes / conflicting_nodes 连边）
```

**禁止**：一本书 → 一个摘要。

## 3. 节点生成规范

- 每个节点必须有：definition / core_claim（可检验形式）/ mechanism（过程性解释，非同义反复）/
  causal_chain / variables（inputs-moderators-mediators-outputs）/ evidence 四栏 /
  evidence_grade / boundary_conditions ≥2 / failure_conditions ≥2 / common_misinterpretations /
  ethical_risks / examples / source_ids ≥1。
- **来源纪律**：禁止编造 DOI、页码、统计量。经典实验只作描述性引用且必须是确证存在的
  （Asch 线段实验、Milgram 服从实验、Cialdini 酒店毛巾实验等）。无法核实的标
  `verification_required: true`。
- 相邻节点必须写明区别（如 curiosity_gap vs suspense_structure vs zeigarnik_effect），
  防止概念蔓延。

## 4. 冲突处理

理论冲突不二选一。登记格式：

```yaml
conflict_type: context | sample | methodology | historical | definition | effect_size
resolution: "在 X 情境更支持 A；在 Y 情境更支持 B"
```

当前已登记 6 条（见 knowledge/evidence/conflicts/conflicts_index.yaml），包括：
loss_aversion 普遍性争议、choice_overload 条件化、filter_bubble 混合证据、
nudge 平均效应修正、conformity 现代复制缩水、anecdote vs narrative 的适用边界。

## 5. 经典理论复核

对 priming、ego depletion、power posing、scarcity、nudging、loss aversion、social proof、
framing、choice overload、mere exposure、emotional contagion 等执行"当前最佳证据"复核，
修正状态固化在 EVIDENCE.md 复核清单与相应节点的 replication 栏。目标不是推翻经典，
而是携带修正继续使用。

## 6. 案例的从属地位

案例库（knowledge/cases/）只用于示例与直觉校准。每条案例强制携带 ≥2 条
alternative_explanations，且 evidence_quality 标注为 anecdote / practitioner_report /
observational / experimental。**案例不得作为因果证据**（Correlation ≠ Causation）。

## 7. 平台知识的隔离蒸馏

平台事实走独立管道，与理论管道完全隔离：

```text
平台观察 → fact_type 四级标注（official_rule / verified_observation / industry_consensus / experience_speculation）
        → last_updated 时效标记 → adapter 字段
未经人工或证据验证的新平台规则不得进入核心机制层。
```

## 8. 更新与去版本化

- 任何证据变化 → 评估是否升级/降级节点 → CHANGELOG 的 evidence version 留痕；
- 平台变化 → 只更新对应 adapter 的 last_updated，不动 core；
- 新机制 → CONTRIBUTING.md 流程（查重 → 建节点 → 连边 → 校验 → evals 回归）。

## 9. 质量门禁

入库前必须通过：
1. `scripts/validate_schema.py`（结构/引用/等级/边界全检）；
2. `scripts/detect_duplicate_nodes.py`（去重）；
3. `scripts/detect_uncited_claims.py`（引用纪律）；
4. 相关 eval 回归子集不退化。
