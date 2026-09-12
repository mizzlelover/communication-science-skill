# CHANGELOG

## v1.0.0（2026-09-12）· 正式公开发布

木铎 MUDUO · 人类传播与社群增长引擎的第一个对外正式版本。

- **知识核心**：216 机制节点（32 域，全部带 provenance 溯源链）· 1,200 关系边（全图单连通）
- **证据体系**：232/233 来源 validated（状态机可追溯）· Gate A 97% / B·C·D 100% ·
  6 条理论冲突情境化裁决 · 29 反模式 · E 级隔离
- **实践层**：354 真实案例（failure 100 / community 100）· 500 平台内容样本（四层平衡）·
  13 平台适配器（77 断言 0 缺级别 0 过期）· 11 工作流 · 8 Schema · 19 自动化脚本
- **评测**：208 self-eval（历史参考）+ **外部双盲测 33 案正式基线：红线 0 · 均分
  17.88/18 · 回归 10/10**（R1=GPT/Codex 净室 · R2=豆包 Seed evolving · R3=审计；
  含校准审计与 REG-001 回归门修复闭环，报告见 evals/blind/report_20260912.md）
- **合规**：8 份命名审计文档（audits/，数据驱动可重跑）· research_log · §99 十五问
  逐条回答（FINAL_REPORT §13）

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
