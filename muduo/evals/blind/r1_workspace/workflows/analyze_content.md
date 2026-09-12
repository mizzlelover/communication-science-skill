# Workflow: Analyze Content（内容传播分析）

用途：分析一篇内容为什么可能/不可能传播。Mode 1（快速）或 Mode 2（机制级深析）。

## 输入
标题/正文/脚本/封面文字/CTA/标签（部分即可），可选：平台、受众、传播目标、数据。

## 流程

### 快速档（M1，≤600 字输出）
1. 确认平台与目标（未给出则按内容类型推断并声明假设）
2. 加载 `platforms/<platform>/adapter.yaml`（title_role/cover_role/opening_role/tag_role/comment_role）
3. 按 SKILL.md §6 内容解剖模型快扫 23 个维度
4. 找出 3 个以内最影响结果的要素问题
5. 按输出格式给出：诊断 → 核心问题 → 为什么（机制级一句话）→ 建议 → 示例 → 平台注意

### 深析档（M2）
1. **Task/Audience/Platform/Goal Detection**（SKILL.md §5 步骤 1-4）
2. **Content Parsing**：逐维度拆解：
   - 承诺层：Promise/Title/Cover 是否一致？Title 兑现率如何？
   - 注意层：Hook 是否触发 bottom_up/top_down capture？前 3 秒/前 2 行？
   - 认知层：Cognitive Load 是否超载？结构是否可扫描（gestalt/visual_hierarchy）？
   - 理解层：抽象 vs 具体（concreteness_in_language）？信息密度（information_overload）？
   - 情绪层：Emotion 是否被设计？arousal 水平与目标匹配吗？
   - 证据层：Trust Signal 是否存在且可信（source_credibility_model）？
   - 身份层：Identity Signal 让谁觉得"这说的是我"（social_identity_theory）？
   - 行动层：CTA 与 Behavior Goal 是否对齐？friction 有多大？
   - 传播层：Share Trigger/Comment Trigger 是否真的给了转发言口与评论靶子？
3. **Mechanism Mapping**：每个要素映射到机制节点，标注 evidence_grade
4. **Bottleneck Detection**：定位行为链最短板（不是列全部问题）
5. **Evidence Loop（证据回路，强制）**：
   - **Evidence Retrieval**：核对所引机制节点是否真实存在于知识库、证据等级是否如实转写；
     知识库没有的机制不得现场编造（铁律 5）
   - **Confidence Calibration**：每条建议标注置信级别 HIGH/MEDIUM/LOW/EXPERIMENTAL；
     D/E 级机制最高 LOW/EXPERIMENTAL；机制库为 MEMORY_BASED 基线，语气不得超出证据
   - **Counterfactual Check**：反事实检验——如果拿掉该机制/要素，结果差异是否真的可解释？
     同一结果是否有竞争性解释（分发/时机/受众错配）？至少核对一次再定稿
6. **边界检查**：用各节点 failure_conditions 排除误判；检查是否其实是
   distribution/audience mismatch/timing 问题（此时结论是"内容不用改"）
7. **Platform Adjustment**：用 adapter 的角色字段修正建议；平台主张分两层陈述
   （机制层理论 + 平台层观察带 L1-L4），不得混成"根据认知科学，某平台必须……"
8. 输出：完整诊断报告（含 Recommendation Schema，内部携带 confidence/causal_status/
   alternative/risk）

## 输出格式
```text
## 传播诊断
一句话总判：内容处在行为链哪一层、最短板是什么。

## 核心问题（≤3 个，按影响力排序）
1. [问题] —— 机制：<中文名（English）>（证据 <A-E>）
2. ...

## 为什么
每个问题一段机制解释（引用节点定义的通俗版）。

## 修改建议
对应的具体改法 + Boundary（适用/不适用）。

## 示例
关键处给改写前后对照。

## 平台注意事项
来自 adapter 的角色字段与 risk_factors；具体规则提醒"以平台最新公告为准"。
平台主张必须带证据级别（L1 官方规则 / L2 已验证观察 / L3 行业共识 / L4 假设），
无官方证据时写"行业观察，未确认"；现状：13/13 adapter 已实读官方正文，
其余平台主张仍按 L 级标注并提示"以平台最新公告为准"。
```

## 交付物（铁律 13 Reader Language）
- 用户要 HTML/结构化呈现时，默认使用 `templates/diagnosis_reader_v1.html`
  （批注式对照阅读器），按模板头注释 7 步填充；规范与自包含门禁见
  `templates/DELIVERABLE_SPEC.md`（零内部词汇/引用即内联/阅读说明/术语清查留痕）。
- 要轻量文本时降级为分层 Markdown（总判→关键问题→决策区→附录），门禁不豁免。
- 交付前先走 Intake 五问（目标定位/发布状态与数据/受众圈层/预算/禁忌，SPEC §5）；
  无表现数据时预测类结论封顶"中低置信"。

## 禁止
- 不给目标就笼统评价"传播效果"
- 把 D 级实践技巧说成科学结论
- 跳过受众与目标直接改文案
- 无证据的"心理学研究表明"
- **理论名堆砌**：只罗列"社会证明+稀缺+损失厌恶"而不解释机制 = 分析失败；
  每次引用机制必须回答——机制究竟是什么/什么条件激活它/影响什么行为/竞争性机制是什么/
  证据强度如何/边界在哪（）
- **三条附加纪律**：
  1. **输入内反证必须显式引用**——用户给的数据序列中已可见的反证（如递减序列、
     基线对照）必须在诊断中点名引用，不得只作泛化预期处理（E2 盲测 CAU-006 扣分项）；
  2. **条件化结论必须配验证出口**——凡给"取决于 X 条件"的结论，同句给出验证方式
     （A/B 对照、回忆/转化测试、基线测量），不留无出口的条件化（回归盲测 THY-003/005 扣分项）；
  3. **机制等级标注原子规则在长答案中同样强制**——次要机制至少给"中文名（等级）"
     最小单元，主要机制给完整边界句（E2 盲测 FLR-004/OVC-002 漏标项）。
- **平台幻觉**：被问"平台是否官方把 X 作为推荐权重"时，无官方证据必须回答
  "未确认/行业观察/需要最新验证"，禁止编造算法规则（）
- **爆款倒推**：帖子爆了不能直接归因单一要素——必须核对账号体量/时机/话题/
  分发/外部流量/既有社群等混杂因素（）
