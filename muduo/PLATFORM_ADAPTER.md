# PLATFORM_ADAPTER — 平台适配规则

## 1. 平台只是适配层

底层机制（knowledge/mechanisms/）**不绑定任何平台**。平台 adapter 只回答一个问题：

> 这个平台如何改变各机制的表达条件（分发模型、元素角色、信号语义、生命周期、风险）？

禁止在 adapter 中发明理论；禁止把平台经验写成科学规律。

## 2. 适配器清单（13 个）

generic（基线）· wechat_official · wechat_moments · wechat_group · xiaohongshu · douyin ·
wechat_channels · bilibili · zhihu · weibo · tiktok · youtube · x

每个 adapter 覆盖 schema 全部 27 个 required 字段（schemas/platform_adapter.schema.yaml），
核心字段包括：distribution_model / content_lifecycle / title_role / cover_role / opening_role /
tag_role / comment_role / follow_role / sharing_mechanism / search_mechanism /
community_mechanism / risk_factors / known_platform_patterns（带 mechanism_links）。

## 3. 事实四级标注（强制）

| fact_type | 含义 | 使用纪律 |
|---|---|---|
| official_rule | 官方公开规则 | 硬数字（字数/时长上限）必须 100% 确证才可标；否则降级并加"以平台最新公告为准" |
| verified_observation | 可验证观察 | 产品可见行为（如开源算法快照、功能存在性） |
| industry_consensus | 行业共识 | 多方从业者交叉印证但官方未证实（适配器主体） |
| experience_speculation | 经验推测 | 必须显式声明需验证，不得作为强建议依据 |

当前统计：industry_consensus 为主体（≈80%），official_rule 46 条，verified_observation 9 条，
experience_speculation 3 条。

## 4. 时效化

- 每个 adapter 必须有 `last_updated: "YYYY-MM"`；
- 本版 adapter 撰写于模型知识截止状态、**未经联网核实**，fact_confidence_summary 已声明；
- 更新流程（`update_platform_knowledge`）：检查平台官方规则/推荐机制/搜索机制/标签机制/
  内容格式/创作者政策 → 更新对应字段 → 刷新 last_updated → 变更记录入 CHANGELOG 的
  platform version；
- **未经人工或证据验证的新规则不得直接进入核心知识**（只改 adapter，不改机制层）。

## 5. confidence 体系

- generic：high（跨平台共性）
- 12 个具体平台：medium（结构性事实可靠，权重类细节以 industry_consensus 为主）
- 任何单条事实的强度以 fact_type 为准，confidence 是整体评级。

## 6. 使用规则（给 Skill）

1. 涉及具体平台先加载对应 adapter；未指明平台用 generic；
2. 建议输出必须做 Platform Adjustment（用 adapter 的角色字段修正通用建议）；
3. 引用具体数字类规则时提醒"以平台最新公告为准"；
4. 平台间结论不可迁移：信号语义（收藏 vs 完播 vs 转发）由各平台目标函数决定
   （见 mechanism: ranking_signal_weighting）。
