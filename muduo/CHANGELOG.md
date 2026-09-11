# CHANGELOG

## v1.0.1（2026-09-11）· 补丁合规第二轮修复

对照「木铎」原始需求两份强制补丁的合规缺口，本轮无条件修复（外部盲测除外，其执行指南已交付）：

- **8 份命名审计文档物化**（补丁 §101）：SOURCE_ACQUISITION_AUDIT / KNOWLEDGE_PROVENANCE_AUDIT /
  PLATFORM_FRESHNESS_AUDIT / CASE_EVIDENCE_AUDIT / RESEARCH_COVERAGE / CASE_COVERAGE /
  EXISTING_PROJECT_AUDIT / GAP_REPORT → `audits/`，由 `scripts/generate_audit_docs.py`
  数据驱动生成，可随数据变更重跑
- **来源状态机推进**（§79）：232/233 来源 research_status → validated（条件：实读 +
  被机制节点引用 + 门禁覆盖；S127 未被引用 → hold_reason 如实标注），
  `scripts/advance_source_status.py`
- **research_log/** 目录建立（§76）：README 格式说明 + 2026-09 条目
  （平台实读/S215-S237 补强/降级事件/本轮修复）
- **节点 schema 升级**：knowledge_half_life 216/216（§62 分域映射）、valid_as_of 12
  （AI 域，§38）、culture_moderators 11（§48 有据提取）、provenance.conflicting_evidence 15 /
  case_sources 128 / platform_sources 67（§11 可推导子段）——`scripts/upgrade_node_schema.py`
- **社群案例 lifecycle**（§32）：100/100 community_case 九阶段结构化
  （99 条有材料覆盖，1 条诚实 not_documented）——`scripts/add_case_lifecycle.py`
- **detect_stale_platform_claims.py**（§60）：77 断言 0 过期 0 缺日期，--strict 模式可作门禁
- **evals/MATERIAL_TRACEABILITY.md**（§54）：真实材料关联 158/208 = 76%（≥60% ✓）；
  50 长文例显式标注 synthetic_scenario
- **FINAL_REPORT**：§13 补丁 §99 十五问逐条回答；§14 本轮修复记录；§10 新增盲测未执行
  与跨文化覆盖薄两项局限
- **evals/BLIND_TEST_GUIDE.md**：外部盲测分角色操作指南（R1/R2/R3、两种执行方式、
  通过线与校准预期）
- 回归：validate_schema ✓ · audit_integrity 无退化（Gates A97/B100/C100/D100）· build_graph ✓

## v1.0（2026-09-10）

首次公开发布：木铎 MUDUO · 人类传播与社群增长引擎。

- 216 机制节点（32 域，全部带 provenance）· 1200 条关系边（全图单连通）
- 210 来源全入库（206 份活跃 Evidence Package + 4 份合并墓碑）
- 354 实践案例（七类，全部带一手材料）
- 13 平台适配器（27 字段，事实四级标注 + last_updated）
- 11 工作流（6 基础 + 5 长文）· 208 评测案例（含 E2 专项与盲测协议）
- 研究诚信层：来源状态机、Evidence Grade A–E、常态化自动审计

core version / platform version / evidence version 三者独立演进，后续版本在此分别记录。
