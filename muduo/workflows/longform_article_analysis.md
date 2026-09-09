# Workflow: Long-form Article Analysis（长篇文章认知与论证诊断）

触发条件（满足其一即进入本 workflow，而非通用 analyze_content）：
- 字数 ≥ 3000；或多章节结构；或行业研究/咨询/方法论/教育/品牌思想类文章；或用户明确要求结构优化；
- 长视频完整文字稿（≥3000 字）。
不机械依赖字数：短而多节的文章同样适用。

## 0. 行为约束（优先级高于一切润色冲动）

**Macro before Micro · Structure before Style · Argument before Polish ·
Delete before Rewrite · Evidence before Eloquence · Reader State before Word Count ·
Global Coherence before Local Beauty**

诊断阶段禁止给出句子级改写建议（那是 optimization 的 Pass 2）。
删除的标准是 **Value/Cost**，不是字数——目标是 Maximum Meaning per Unit of Reader Effort，
不是 Minimum Word Count。

## 1. 诊断管线（按序执行，不得跳步）

```text
Input → Task/Goal Detection → Audience Detection → Platform Detection
→ 1. Central Thesis Extraction
→ 2. Argument Mapping（产出 argument map）
→ 3. Section Function Mapping（章节功能标记）
→ 4. Reader Journey Analysis（五阶段）
→ 5. Cognitive Load Analysis（负荷曲线）
→ 6. Evidence Audit（深查走 longform_evidence_audit.md）
→ 7. Redundancy Detection（语义重复 + knowledge/longform/semantic_redundancy.md）
→ 8. Concept Consistency Check（概念注册表）
→ 9. Narrative Thread Analysis（阅读动力线）
→ 10. Priority Diagnosis（P0-P3）
```

超长文（超出单次上下文或 > 8000 字）必须走分块协议（见第 4 节），禁止只分析开头。

## 2. 各步骤执行要点

### 2.1 Central Thesis Extraction
一句话回答：**这篇文章究竟想让读者相信什么？** 产出 `central_thesis`。
随后识别 supporting_claims / counter_claims / evidence / implications / recommendations。
**抽不出一句话中心命题 = P0 结构问题**（常见于 Delayed Thesis 与信息堆叠型文章）。

### 2.2 Argument Mapping
按 `schemas/argument_map.yaml` 建论证图（Central Thesis → Claims → Evidence/Example/Counterargument）。
逐 Claim 检查八类缺陷：unsupported_claim / logical_gap / duplicated_claim /
misplaced_evidence / weak_evidence / overclaim / contradiction / conclusion_leap。

### 2.3 Section Function Mapping
每节标记 13 种功能之一：hook / context / problem / thesis / explanation / theory /
evidence / example / counterargument / synthesis / transition / recommendation / conclusion。
对每节追问：**这一节真的有必要存在吗？** 运行 Paragraph Value Test（Delete Test），
标记 ESSENTIAL / SUPPORTING / EXAMPLE / TRANSITION / OPTIONAL / REDUNDANT / OFF_TOPIC。
重点识别：同义重复、AI 式改写重复、同一概念多次解释、无新增价值的案例堆叠、无作用铺垫。

### 2.4 Reader Journey——五个阶段逐段核对
| 阶段 | 位置 | 读者在做什么 | 检查要点 |
|---|---|---|---|
| Entry | 0-10% | 判断与我有关/值得读/能得到什么/作者可信吗 | relevance、curiosity_gap、specificity、credibility、identity |
| Model Building | 10-40% | 建立认知模型 | 核心概念是否解释、有无跳跃、认知负荷、chunking |
| Fatigue Zone | 40-70% | **长文最危险阶段** | novelty decay、cognitive fatigue、重复论证、节奏、抽象过载；应适时插入案例/类比/数据/小结/转折/新问题/图示 |
| Integration | 70-90% | 整合信息 | synthesis、implication、connection、pattern recognition |
| Closure | 90-100% | 收获与行动 | conclusion、takeaway、memory anchor、action、必要时的 unresolved question |

### 2.5 Cognitive Load Curve
每节标记 LOW/MEDIUM/HIGH/VERY_HIGH（依据：新概念数、术语数、抽象度、句法复杂度、
数据量、理论密度、前置知识要求）。**禁止连续多节 HIGH**；应形成 HIGH→LOW→MEDIUM→HIGH 的节奏。
连续高负荷区通常正落在 Fatigue Zone——这是长文弃读的第一死因。

### 2.6 Information Density
Information Density = New Meaning / Reading Cost。两端都要标记：
过低（水/重复/空话/AI 套话）与过高（难懂/疲劳/无法记忆/缺少解释）。

### 2.7 Concept Registry
按 `schemas/concept_registry.yaml` 注册全文概念，检测六类问题：
一个概念多个名字、同一个词多种含义、首次出现未解释、前后定义变化、缩写未说明、概念层级混乱。

### 2.8 Long-range Coherence
建立 open_question → resolution 与 promise → delivery 映射。
第一部分提出的问题，后续是否有回答？所有重要承诺是否兑现？未兑现 = 结构问题。

### 2.9 Narrative Thread
研究型文章也需要阅读动力线（不要求编故事）：
Problem → Unexpected Cause → Theory → Evidence → New Model → Practice 之类的主线。
检测：主线中断、旁枝过长、背景资料失控、案例抢走主线、中途更换主题。

### 2.10 Hooks
区分三类：Entry Hook（为什么开始读）、Continuation Hook（为什么继续下一节）、
Macro Hook（为什么值得读完整篇）。逐节检查节尾是否产生 Forward Momentum。

### 2.11 Opening / Transition / Ending
- 开头查：Relevance/Promise/Problem/Novelty/Credibility/Specificity/Cognitive Friction；
  识别背景过长、主题出现太晚、"随着时代发展/众所周知"式空转。
- 过渡回答"为什么现在讲下一部分"，禁止"接下来我们看看"式机械过渡。
- 结尾禁止复述全文；判断最适合的 Closure：Synthesis/Action/Perspective Shift/
  Prediction/Question/Framework/Principle。

### 2.12 Memory Design
回答：读完后读者能记住哪 3-5 件事？产出 memory_anchors（框架/关键词/对比/类比/模型/结论句/图表）。
如果列不出——文章没有记忆设计，P1。

## 3. 超长文分块协议（强制）

内容超出单次上下文或 > 8000 字时：
```text
Step 1 建立全局 Outline（先扫标题/首尾段/小结句）
Step 2 按 section 分块
Step 3 逐块产出 section 摘要：section_id / claim / evidence / role / concepts / links_to_previous / links_to_next / issues
Step 4 汇总为 Global Representation
Step 5 在全局表示上做跨章节分析（论证图/重复/一致性/长程连贯）
Step 6 再分块优化，每步核对不破坏 Global Coherence
```
**禁止只分析前几千字就下结论。**

跨会话任务维护 `longform_state.yaml`：central_thesis / outline / completed_sections /
concept_registry / open_questions / editing_decisions / pending_issues。
**§3b 走查结果必须写入状态文件**：`ap_lf_hits`（命中的 AP-LF 编号 + 位置）与
`ap_lf_fixes`（已执行/待执行的修复动作）——保证超长文多轮修复时命中清单不丢失、
修复闭环可跨会话对账。

## 3b. 长文反模式对照表（M7 检测路径索引，强制逐条走查）

19 条长文反模式（knowledge/anti_patterns/longform_anti_patterns.yaml, AP-LF-001..019）
在诊断管线中的检测入口如下。**每次诊断必须逐条过表**，命中即计入对应输出部分。
**检测不是终点**：每条命中必须同步产出修复动作（第三列），映射进 Editing Plan
——检测→修复在 longform_article_optimization.md 中闭环执行。

| 反模式 | 检测入口（管线步骤） | 检测信号 | 修复动作（绑定工作流） |
|---|---|---|---|
| AP-LF-001 AI Semantic Repetition | 步骤 7 Redundancy | 同主张多措辞组；信息增量为零 | semantic_redundancy.md 保留判据 → restructure **Cut/Merge**，line_edit 删复读 |
| AP-LF-002 Background Overload | 步骤 1 + Opening 检查 + 旅程 Stage1 | context 占比 >20%；thesis >15% | restructure **Cut** 背景至 ≤10% + line_edit 重写开场 |
| AP-LF-003 Concept Dumping | 步骤 5 Cognitive Load + Concept Registry | 单节新概念 >3 无锚定 | restructure **Rewrite/Expand**：逐概念配锚定案例，按依赖序重排 |
| AP-LF-004 Evidence Dumping | 步骤 6 Evidence Audit | 孤儿证据（无对应 claim） | evidence_audit 归位到 claim 或 **Cut** |
| AP-LF-005 Case Stacking | 步骤 2 Argument Map | 同 claim 案例 >2 增量趋零 | restructure **Cut**（保留差异最大案例）+ evidence_audit 补异质证据 |
| AP-LF-006 False Depth | 步骤 3 Delete Test + 密度检查 | 删繁从句后主张不变 | line_edit **Delete/Rewrite**：删零增量表达，具体化 |
| AP-LF-007 Delayed Thesis | 步骤 1 Central Thesis | 首现 >15% 或抽取失败 | restructure **Move**（thesis 前移至 ≤10%）+ 开场重写 |
| AP-LF-008 Overexplaining | 步骤 7 + Concept Registry | 同一概念解释 >1 次 | line_edit **Cut** 重复解释（concept registry 复核） |
| AP-LF-009 Underexplaining | 步骤 2 Argument Map | 概念首用未定义；缺 warrant | restructure **Expand** 定义/锚定 + 补 warrant 段（argumentation_structure） |
| AP-LF-010 Narrative Drift | 步骤 9 Narrative Thread | 连续 2+ 节无推进；平行主线 | restructure **Move/Cut** 支线（可拆另一篇）+ 主线回连 |
| AP-LF-011 Argument Jump | 步骤 2 Argument Map | warrant 缺失；logical_gap | 补 warrant 段（line_edit/Expand）：桥梁假设显式化 |
| AP-LF-012 Premature Conclusion | 步骤 2 + 步骤 6 | 无 qualifier；反方三件套全缺 | evidence_audit 补 **counterargument 三件套** + 结论加限定词 |
| AP-LF-013 Summary Repetition | 步骤 8 Ending + 步骤 7 | 结尾信息增量为零 | line_edit **Rewrite** Closure（八型选择）+ 锚点回收（retrieval_cue_design） |
| AP-LF-014 Over-sectioning | 步骤 3 + 步骤 5 | 节长 <300 字无推进；纯切分标题 | restructure **Merge** 碎片节 + 小标题改组块名 |
| AP-LF-015 Mechanical Transition | 步骤 8 Transition | 空过渡词；节尾无钩子 | line_edit 重写过渡：承接上节结论→提出下节问题 |
| AP-LF-016 Buzzword Density | 步骤 5 Information Density | 抽象名词密度超标 | line_edit **Rewrite**：黑话兑换为具体场景句（concreteness, B+） |
| AP-LF-017 Citation Decoration | 步骤 6 Evidence Audit | "研究表明"不可回溯 | evidence_audit：补真实来源或降级为作者判断（**禁止编造文献**） |
| AP-LF-018 Artificial Completeness | 步骤 3 + 步骤 5 | 维度 >5 无优先级论证 | restructure **Cut** 非主线维度 + 补优先级论证 |
| AP-LF-019 Symmetry Bias | 步骤 3 Section Mapping | 相邻节同构；标题句式雷同 | restructure 按 role 差异化节结构 + line_edit 小标题改组块名（von_restorff） |

闭环规则（强制）：**诊断输出中命中的每条 AP-LF，必须在 Editing Plan 中有一条对应
action（六操作之一）**；用户选择"只诊断不优化"时，修复动作仍需列出（作为
Rewrite Options 的一部分），只是不执行。

## 4. 诊断输出格式（十四部分，分层）

先给 **Top 3 Critical Issues**（P0-P1，各一段：问题—证据—为什么是 P0），再按以下结构展开：

```text
1. Overall Assessment        （总评 + 十四维评分，1-10 分，每维一句原因）
2. Central Thesis            （抽取结果；抽不出即 P0）
3. Article Argument Map      （论证图 + 八类缺陷标记）
4. Reader Journey            （五阶段走查 + Fatigue Zone 风险）
5. Top Structural Problems   （按 P0→P3，每条：问题/位置/机制/为什么）
6. Redundancy                （语义重复组 + 建议保留哪句，而非全部润色）
7. Evidence Problems         （weak/too far/redundant + 证据类型标注）
8. Cognitive Load            （负荷曲线 + 连续高负荷区）
9. Narrative Thread          （主线图 + 断点）
10. Proposed New Structure   （原结构 vs 新结构，每项调整 WHY）
11. Cut / Merge / Move / Expand Plan
12. Line-level Issues        （只列清单，留待 Pass 2；本阶段不改写）
13. Platform Adaptation      （强制槽位，见下方硬规则）
14. Rewrite Options          （下一步选项：结构重排/证据审计/逐句编辑/全文重写——交用户选）
```

**Platform Adaptation 硬规则（针对 self-eval 暴露的 44/50 扣分根因）**：
1. 本槽位**不可省略**：即使是最压缩的输出（用户只要"最要命的几件事"），
   也必须保留至少一行平台修正——省略 Platform Adaptation = 输出不完整；
2. 修正必须**引用 adapter 的具体字段名**（title_role / cover_role / opening_role /
   content_lifecycle / interaction_signals / sharing_mechanism / search_mechanism /
   risk_factors 至少 2 个），"注意平台调性"这类无字段空话不计为完成；
3. 诊断阶段（步骤 2 Platform Detection）读到的 adapter 信息必须在本槽位落地——
   管线前段读取、后段输出，两端绑定；
4. Editing Plan 中的每条 action 若影响平台要素（标题/小标题/结尾 CTA），
   必须标注对应的 adapter 字段。
5. **下一步选项槽位（第 14 部分不可省略）**：Rewrite Options 是给用户的行动出口，
   任何档位（含最压缩档）必须保留 ≥2 个选项（结构重排 / 证据审计 / 逐句编辑 /
   只做 P0 / 保持不动）；需要确认的结构决策显式声明"待确认"——
   诊断结论不是终点，省略选项 = 输出不完整（actionability 弱点对策）。
6. **品类必查清单（SKILL.md §3 两遍检索）**：机制映射必须按案例类型走查必查清单
   （平台适配类三组 / 标题类五项 / 社群类五件套），逐项判断"适用/不适用并说明理由"，
   不许静默跳过——key_mechanisms 覆盖以清单为准（theory_accuracy 弱点对策）。
7. **边界与风险槽位（不可省略）**：任何档位输出必须含至少一行边界/风险/合规提示
   （适用条件 / 平台规则时效 / 合规风险 / 反模式排除 / 收入疗效类宣称真实性提示任一）——
   新增槽位（平台/选项/品类走查）不得挤占本槽位（ethical_safety 弱点对策：
   盲测 v3 中 8/16 案无风险提示的根因即槽位互挤）。

文章类型判定改变优化侧重：thought_leadership 重 originality+argument；
research 重 evidence+methodology；consulting 重 problem→framework→recommendation；
educational 重 learning progression；story_essay 重 narrative+emotion；
platform_longform 重 retention+shareability。**不同类型禁用同一模板。**

全报告的机制引用一律执行铁律 2 的**最小边界单元**（`等级＋一句适用条件`；复核清单机制
如 peak_end_rule / cognitive_fatigue 必须携带修正状态）——压缩输出只压篇幅不压原子单元，
此规则在十四部分的任何一档输出下都不可豁免。

## 5. 禁止

- 跳过诊断直接润色（用户说"帮我润色"但存在 P0/P1 结构问题时，必须先提示：
  Structural Editing 优先于 Line Editing，征得确认再继续）；
- 只分析开头（超长文不走分块协议）；
- 一次平铺几十条建议（违反分层输出）；
- 机械缩字（Value/Cost 才是删除标准）；
- 把复杂问题简化成错误结论（Simplify Expression, Not Reality）。
