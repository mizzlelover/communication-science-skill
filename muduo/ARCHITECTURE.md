# ARCHITECTURE — 人类传播与社群增长引擎（Human Communication & Community Growth Engine）

> 核心公理：**底层人类机制稳定，平台机制变化。**
> 因此：Human Mechanism Core 永远是主体；平台永远只是 Adapter。

---

## 1. 四层架构总览

```text
┌─────────────────────────────────────────────────────────────┐
│  Layer 4  PRACTICE ENGINE（应用工作流层）                      │
│  workflows/: analyze_content · improve_title · rewrite       │
│             community_diagnosis · campaign_design · postmortem│
│             + Long-form Intelligence 链：             │
│             longform_article_analysis → optimization         │
│             （restructure · evidence_audit · line_edit）      │
│  输入：内容/社群/数据/长文 → 输出：诊断 + 建议 + 改写          │
├─────────────────────────────────────────────────────────────┤
│  Layer 3  PLATFORM ADAPTER（平台适配层）                       │
│  platforms/: generic + 12 个平台 adapter.yaml                 │
│  只描述"平台如何改变机制的表达条件"，不新增理论                  │
├─────────────────────────────────────────────────────────────┤
│  Layer 2  COMMUNICATION MECHANISM LAYER（传播机制层）          │
│  Mechanism Graph：216 机制节点（32 域）+ 11 种关系边           │
│  传播行为链：Attention → … → Sharing → Diffusion → Community  │
├─────────────────────────────────────────────────────────────┤
│  Layer 1  HUMAN MECHANISM CORE（人类机制核心层）               │
│  各 Domain 下的认知/情绪/动机/社会机制                          │
│  （comprehension 域：长阅读的理解与论证机制）          │
│  与任何平台无关、与任何时代无关的底层机制                       │
└─────────────────────────────────────────────────────────────┘
        ↑ 证据供给                ↑ 证据供给
   knowledge/sources/       knowledge/evidence/
   （100 Seed Corpus）       （冲突与经典复核记录）
```

## 2. 目录结构

```text
muduo/
├── SKILL.md                 # Agent 入口：任务判断 + 动态加载策略
├── README.md
├── ARCHITECTURE.md          # 本文件
├── METHODOLOGY.md           # Evidence-Aware Knowledge Distillation 方法
├── EVIDENCE.md              # Evidence Grade A–E 体系
├── PLATFORM_ADAPTER.md      # 平台适配规则与事实时效规范
├── EVALS.md                 # 评测方法与评分标准
├── CONTRIBUTING.md          # 如何新增知识
├── CHANGELOG.md             # 版本记录（core / platform / evidence 三线）
│
├── knowledge/
│   ├── sources/
│   │   └── source_registry.yaml      # 210 来源（206 份 Evidence Package）
│   ├── domains/                      # 32 个一级 Domain 索引
│   │   ├── _index.yaml
│   │   ├── *.md
│   │   └── ai_information_environment/   # AI 时代新增研究模块
│   ├── mechanisms/                   # Mechanism Graph 节点（YAML，按 domain 分文件）
│   ├── evidence/
│   │   ├── conflicts/                # 理论冲突处理记录
│   │   └── classic_rechecks/         # 经典理论复核记录
│   ├── cases/                        # 实践案例库
│   ├── anti_patterns/                # 反模式库
│   │   └── glossary/                     # 中英术语表
│
├── platforms/                        # 平台适配器
│   ├── _adapter_schema.yaml
│   └── <platform>/adapter.yaml
│
├── workflows/                        # 应用工作流（Layer 4）
├── schemas/                          # 所有数据 Schema
├── evals/                            # 208 benchmark cases + rubric + regression
└── scripts/                          # 自动化工具
```

## 3. 数据流：一次分析请求如何穿过四层

以用户请求"优化这篇小红书标题"为例：

```text
1. SKILL.md 判断任务类型 → Mode 1 Quick Diagnosis / 改标题 workflow
2. Retrieval 按需加载，而非全库：
   - Layer 3: platforms/xiaohongshu/adapter.yaml
   - Layer 2: attention / curiosity_gap / processing_fluency /
              identity / social_currency / specificity / framing 节点
   - Layer 1: 上述节点的边界条件与证据等级
3. Diagnostic Engine（诊断流程）定位瓶颈 → 输出 Recommendation（输出 Schema）
4. 输出格式：诊断 → 核心问题 → 为什么 → 建议 → 示例 → 平台注意
```

## 4. Mechanism Graph 设计

- 节点：每个机制一个 YAML 节点，统一 Knowledge Node Schema（schemas/knowledge_node.schema.yaml）。
- 关系（11 种）：`SUPPORTS / CONTRADICTS / MODERATES / MEDIATES / PRECEDES / AMPLIFIES / REDUCES / REQUIRES / OVERLAPS_WITH / IS_SUBTYPE_OF / APPLIES_TO`。
- 节点 ID 规则：snake_case 英文术语（如 `social_proof`），全库唯一、永不复用。
- 文件组织：每个 domain 一个 YAML 文件（`knowledge/mechanisms/<domain>.yaml`），内含 `nodes:` 列表；`related_nodes` / `conflicting_nodes` 只引用节点 ID，保证图可在不加载全文的情况下重建。
- `scripts/build_graph.py` 从节点文件重建整图并检查悬空引用。

## 5. 证据与来源的隔离

- **Source ≠ Knowledge Node**：source_registry.yaml 只登记证据来源；机制节点通过 `source_ids` 引用来源。
- 每条关键 claim 的来源按统一格式登记；无法核实的标 `verification_required: true`。
- 严禁编造 DOI/论文/数据。案例（knowledge/cases/）永远只是案例，不得作为因果证据。
- 证据等级 A–E 见 EVIDENCE.md；Skill 输出建议优先引用 A/B/C 级，D 必须标注为实践经验，E 默认不得作为强建议依据。

## 6. 版本机制

```text
core version       # Layer 1+2：人类机制 + 传播机制。平台变化不影响它。
platform version   # Layer 3：各 adapter 独立 last_updated，可单独刷新。
evidence version   # 证据库：复核新研究后更新，可降级/升级节点等级。
```

三者独立演进，在 CHANGELOG.md 分别记录。

## 7. 扩展规则

- 新平台：复制 platforms/generic/adapter.yaml 起步，只填平台事实，不发明理论。
- 新机制：走 CONTRIBUTING.md 流程——先查重，再建节点，再连边。
- 新 AI 时代现象：进入 knowledge/domains/ai_information_environment/，先收集证据再定级。

## 8. 设计原则（全库强制）

Mechanism before Tactic · Evidence before Confidence · Human before Platform ·
Platform as Adapter · Diagnosis before Rewrite · Theory + Boundary + Practice ·
Short-term Performance ≠ Long-term Value · Virality ≠ Community ·
Correlation ≠ Causation · Useful ≠ Manipulative
