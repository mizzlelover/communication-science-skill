# CONTRIBUTING — 如何新增知识

## 原则

**先查重，再建节点；先诊断，再改结构。** 质量优先于数量；宁缺毋滥。

## A. 新增机制节点

1. **查重**：检索 knowledge/mechanisms/ 与 INDEX.md——已有相近节点（同义/上下位）
   时改为扩充原节点（aliases/related_nodes/evidence），不新建。
   运行 `python3 scripts/detect_duplicate_nodes.py` 确认。
2. **写节点**：按 schemas/knowledge_node.schema.yaml 全字段撰写；
   - core_claim 必须可检验；mechanism 必须是过程性解释；
   - boundary_conditions ≥2、failure_conditions ≥2、ethical_risks ≥1；
   - source_ids ≥1 且真实（禁止编造出处，无法核实标 verification_required）；
   - 中文正文 + English 术语原词；evidence_grade 按 EVIDENCE.md 诚实定级。
3. **连边**：related_nodes / conflicting_nodes 引用现有节点 ID；真实冲突登记到
   knowledge/evidence/conflicts/conflicts_index.yaml。
4. **入索引**：把节点 ID 加进 knowledge/domains/_index.yaml 对应 domain 的 nodes 列表。
5. **过门禁**：
   ```bash
   cd scripts
   python3 validate_schema.py && python3 detect_duplicate_nodes.py && python3 detect_uncited_claims.py
   ```
6. **回归**：跑 evals/cases/regression.yaml 相关案例确认无退化；CHANGELOG 记录
   core version 变更。

## B. 新增来源

在 knowledge/sources/source_registry.yaml 追加条目（source_id 顺序递增，永不复用）；
字段按 schemas/source.schema.yaml；isbn/doi/url 仅在可确证时填写。
注意：**Source ≠ Knowledge Node**——登记后仍需按 METHODOLOGY.md 蒸馏进机制节点才算入知识。

## C. 新增/更新平台

1. 复制 platforms/generic/adapter.yaml 到新目录；
2. 只填平台事实，全部事实标 fact_type 四级；
3. known_platform_patterns 的 mechanism_links 只能引用现有节点；
4. 填 last_updated 与 confidence；CHANGELOG 记录 platform version；
5. **平台经验不得进入机制层。**

## D. 新增 AI 时代现象

进入 knowledge/domains/ai_information_environment/：先收集证据（原始论文/meta-analysis 优先），
机制解释必须挂回底层节点；默认 C 级起步，证据成熟后升级并留痕。

## E. 新增反模式/案例

反模式（anti_patterns/）必须写明 why_short_term_works（挂钩真实机制）与 long_term_harms；
案例（cases/）必须 ≥2 条 alternative_explanations，且不得作为因果证据。

## F. 新增 Eval

按 EVALS.md 案例结构增补；key_mechanisms 引用真实节点；expected_behavior 必须可判定；
CHANGELOG 记录 evals 变更。
