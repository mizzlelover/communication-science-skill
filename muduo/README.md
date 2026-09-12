# README — 人类传播与社群增长引擎（木铎 MUDUO）

基于认知科学、社会心理学、传播学、网络科学、说服科学与平台机制研究的**证据感知型**传播方法论 Skill。

## 它能做什么

- 分析一篇内容为什么可能传播或不传播（标题/首屏/结构/叙事/证据/情绪/CTA/标签逐要素诊断）
- **长篇文章深度优化（Long-form Intelligence）**：3000 字以上文章的理解、诊断、
  重构与优化——中心命题抽取、论证地图、读者五阶段旅程、认知负荷曲线、语义重复压缩、
  概念一致性、证据审计、结构重排（两遍优化：先结构后逐句）；支持公众号深度文/行业研究/
  管理咨询/方法论/教育/品牌思想文/AI 生成长文检测与超长文分块处理
- 判断用户为什么可能点击、阅读、记忆、相信、评论、收藏、分享或行动（16 层行为链逐层定位）
- 诊断社群为什么形成、活跃、沉寂、裂变或瓦解（Identity/Boundary/Norm/Status/Ritual…10 层结构）
- 按平台机制适配建议（13 个平台适配器，事实四级标注+时效化）
- 复盘传播数据，定位漏斗环节（先排除外生变量，再归因内容）
- 每条建议携带理论依据、Evidence Grade 与适用边界

## 快速使用

把 `SKILL.md` 作为 Agent 的 Skill 入口即可（Trae 放置于 `.trae/skills/` 或直接引用本目录）。
十一个工作流：`workflows/`（6 基础：analyze_content / improve_title / rewrite_content / community_diagnosis / campaign_design / postmortem；5 长文：longform_article_analysis / longform_article_optimization / longform_restructure / longform_evidence_audit / longform_line_edit）。

示例请求：
- "帮我看看这篇小红书标题为什么没人点"（M1/M3）
- "复盘：这条视频曝光 20 万只有 2% 完播（演示数据）"（M6）
- "我们的付费社群 800 人只有 20 人说话，怎么救"（M5）

## 核心设计

```text
Human Mechanism Core（32 域 / 216 机制节点，证据等级 A-E）
        ↓
Communication Mechanism Layer（11 种关系边连成机制图，单连通）
        ↓
Platform Adapter（13 平台 × 27 字段，official_rule/verified_observation/industry_consensus/experience_speculation 四级事实标注）
        ↓
Practice Engine（11 工作流 + 208 eval 案例 + rubric）
```

铁律：**Mechanism before Tactic · Evidence before Confidence · Human before Platform ·
Platform as Adapter · Diagnosis before Rewrite · Virality ≠ Community · Useful ≠ Manipulative ·
Research Integrity**。

## 研究诚信层

**书目不是知识库，引用不是研究。** 全库执行来源分级与常态化诚信审计：

- **现状**：210/210 来源实读或佐证级（206 份活跃 Evidence Package，另含 4 份同书合并
  MERGED_INTO 墓碑）· 216/216 节点带 provenance（其中 10 个显式保持 MEMORY_BASED）·
  案例 354（全部带一手材料，七类达标）· 平台核验 13/13 · 评测案例 208 ·
  **Research Gate A 97% / B 100% / C 100% / D 100%**
- **状态机**：来源 PLANNED→FOUND→ACQUIRED→READ→ANNOTATED→VALIDATED→DISTILLED；
  只有 VALIDATED+ 才能作为知识核心主要证据（Found ≠ Researched · Cited ≠ Read）
- **平台证据四级**：L1 官方规则（须实读官方正文）/ L2 已验证观察 / L3 行业共识 / L4 假设；
  半衰期阈值 official 12 月 · algorithm 3-6 月 · UI 1-3 月
- **能说"不知道"**：证据不足/规则未知/未核验时输出"当前没有足够证据"，禁止确定语气填补空洞
- 自动审计：`python3 scripts/audit_integrity.py --write-tables`

## 目录

| 目录 | 内容 |
|---|---|
| `knowledge/sources/` | 210 来源注册表 + 206 份 Evidence Package（Source ≠ Knowledge；另含 4 份 MERGED_INTO 墓碑） |
| `knowledge/mechanisms/` | 216 个机制节点（32 个 YAML，按域组织） |
| `knowledge/domains/` | 域索引 + AI 时代信息环境研究模块 |
| `knowledge/evidence/` | 冲突登记、经典复核登记（classic_rechecks）、图统计摘要 |
| `knowledge/cases/` | 354 个实践案例（七类，全部带 original_material） |
| `knowledge/anti_patterns/` | 反模式库（为何短期有效/为何长期受损） |
| `platforms/` | 13 个平台适配器（官方正文实读核验） |
| `workflows/` | 11 个应用工作流（6 基础 + 5 长文） |
| `schemas/` | 8 个数据 Schema |
| `evals/` | 208 评测案例（含 E2 六类专项与长文专项）+ rubric |
| `scripts/` | 自动化工具（校验/查重/覆盖/索引/建图/评测/报告/诚信审计/盲测包） |

## 工程命令

```bash
cd scripts
python3 validate_schema.py          # 全库结构与引用校验
python3 detect_duplicate_nodes.py   # 节点查重
python3 detect_uncited_claims.py    # 无出处断言检测
python3 detect_missing_sources.py   # 来源覆盖报告
python3 build_index.py              # 生成 INDEX.md
python3 build_graph.py              # 重建机制图并输出统计
python3 run_evals.py                # 评测统计（--input 评分结果）
python3 generate_report.py          # 报告数据段草稿
python3 audit_integrity.py          # 研究诚信审计（--write-tables 回填审计文档表格）
```

依赖：Python 3.9+ / PyYAML。

## 文档

ARCHITECTURE.md（架构）· METHODOLOGY.md（蒸馏方法）· EVIDENCE.md（证据体系）·
PLATFORM_ADAPTER.md（平台规范）· EVALS.md（评测方法）· CONTRIBUTING.md（扩展指南）·
CHANGELOG.md（版本记录）。

## 当前状态

v1.0（2026-09-09）：研究资产完备——210/210 来源实读或佐证级、216 机制节点
（全部带 provenance，P0=0）、案例 354（七类达标，全部带一手材料）、平台核验 13/13、
评测 208（含长文专项 65 例）+ 外部盲测 33 案、Research Gate A 97% / B·C·D 100%；外部双盲测 33 案红线 0；
自动化校验与诚信审计齐备（scripts/）。已知限制与证据边界见 EVIDENCE.md。
