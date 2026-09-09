# demo_analysis — 长文工作流首次实战验证报告

> 被检对象：evals/longform/demo/demo_article.md（《为什么大多数企业的社群运营最终都会失败》，
> 约 5000 字 / 9 节 / thought_leadership / wechat_official / 企业中高管）
> 执行流程：workflows/longform_article_analysis.md 全管线（分块无需触发：5000 字 < 8000 字阈值）
> 本报告即十四部分输出的实跑样例。

---

## 1. Overall Assessment

文章文笔流畅、案例生动、观点有真实的行业洞察内核——但作为一篇论证文，它目前是
**"三段好素材 + 一条晚到的命题 + 一个未兑现的承诺"**。核心命题在 36% 处才出现；
第一部分承诺的"完整诊断框架"全文从未兑现；全文唯一的机制性案例（n=1）被用来支撑
"所有社群"的全称结论。**先做结构手术，再谈润色**（Macro before Micro）。

十四维评分（1-10）：

| 维度 | 分 | 一句原因 |
|---|---|---|
| Thesis Clarity | 4 | 命题清晰但 36% 才出现，Entry 阶段无锚 |
| Argument Coherence | 5 | 主线可还原，但 §5 与 §2 重复、claim 链有断点 |
| Structural Efficiency | 5 | §5-7 三节同构、信息密度洼地 |
| Evidence Strength | 3 | n=1 支撑全称结论；5 处"研究表明"无来源 |
| Cognitive Load | 4 | §5-7 连续高负荷且正落 Fatigue Zone |
| Information Density | 5 | 黑话段 + 语义重复组拉低均值 |
| Narrative Momentum | 5 | §2-4 推进好；§5-7 动力线停摆 |
| Concept Consistency | 3 | "身份感/认同感/归属感"漂移贯穿全文 |
| Reader Orientation | 4 | 读者在中段不知道"这跟我有什么关系" |
| Trust | 4 | 引用装饰 ×5 + 过度声称，专业读者会扣分 |
| Memory | 4 | "先身份，后活跃"一个好锚点，其余无设计 |
| Actionability | 6 | §8 七条建议具体，是全文最实在的部分 |
| Language Quality | 7 | 文笔流畅自然，作者声音鲜明（保全价值高） |
| Platform Fit | 5 | 公众号适配未做：无摘要、小标题非组块名、无分享钩子 |

## 2. Central Thesis

**一句话抽取：** "企业社群失败多因身份感缺失，而非激励不足——把社群从促销渠道
重构为身份共同体，活跃与转化才会作为副产品出现。"

- supporting_claims：C1 激励无法阻止沉寂（§2-3）；C2 身份感是留存决定变量（§4）；
  C3 六个心理概念构成社群地基（§5）；C4 补贴与活跃负相关（§6）；C5 服务 5% 核心贡献者（§7）
- counter_claims：**无**（全文零反方层——P0 级缺失）
- implications / recommendations：§8 七条建议（分散，未结构化）
- **抽取难度正常**（命题存在且明确）——问题不在"抽不出"，在"出现太晚"。

## 3. Article Argument Map

```text
Central Thesis（§4，36% 处才登场）
├── C1 激励无法阻止沉寂
│   ├── E1 三个死群案例（§2，anecdote/practitioner）
│   └── E2 "研究表明激励几乎无长期作用"（§3，citation decoration ❌不可核验）
├── C2 身份感是留存决定变量
│   ├── E3 精品咖啡案例（§4，n=1 anecdote）⚠️ warrant 缺失
│   └── ❌ "所有社群的失败，归根结底都是认同感的坍塌" —— conclusion_leap：
│        n=1 → 全称命题，无 qualifier、无替代解释（如自选择效应：
│        愿意参与投票的本来就是高粘性顾客）
├── C3 六概念心理地基（§5）—— unsupported_claim：概念仅罗列，无证据无案例
├── C4 补贴悖论（§6）—— 观察性断言，无数据
└── C5 5% 核心贡献者（§7）—— citation decoration（"有调查显示"）
```

八类缺陷命中：**conclusion_leap（C2）、unsupported_claim（C3）、
logical_gap（E3→C2 无 warrant）、weak_evidence（C1/C4/C5）、
duplicated_claim（§5 现象层复述 §2）、misplaced_evidence（咖啡案例应该当开篇钩子）**。
counterargument 三件套全缺（§20）：无反方、无替代解释、无边界条件。

## 4. Reader Journey

| 节 | 进度 | 阶段 | 状态 | 发现 |
|---|---|---|---|---|
| §1 | 0-9% | Entry | ⚠️ | 背景过载 ~430 字；可信度好（"咨询十多年"）；承诺"完整诊断框架" |
| §2 | 9-20% | Model Building | ✓- | 三案例引入节奏好，但三案同点（堆叠） |
| §3 | 20-30% | Model Building | ✓ | 设问推进好，是全文最顺的一节 |
| §4 | 30-40% | Model Building | ⚠️ | 命题迟到（应在 10-12% 前出现）；命题刚立即被全称化 |
| §5 | 40-50% | **Fatigue Zone** | ❌ | 概念倾倒（6 概念无锚定）+ 与 §2 信息重复 |
| §6 | 50-62% | **Fatigue Zone** | ❌ | 黑话段 + 抽象论述，动力线停摆 |
| §7 | 62-75% | **Fatigue Zone** | ❌ | 同构第三节；疲劳预算已透支 |
| §8 | 75-90% | Integration | ⚠️ | 建议具体但"无法给出万能手册"的自白坐实了承诺未兑现 |
| §9 | 90-100% | Closure | ⚠️ | 结尾复读（echo），但"先身份，后活跃"是好锚点 |

Fatigue Zone 风险清单：§5-7 连续三节无案例、无小结、无节奏变化——
这正是 cognitive_fatigue（B）预测的弃读窗口。处方见 §11 Editing Plan。

## 5. Top Structural Problems

1. **[P0] Delayed Thesis**：命题 36% 才出现（§4）。
   机制：information_foraging（B）——搜寻型读者在 Entry 阶段即评估"值不值得读"，
   36% 无命题 = 前 1/3 全在裸奔。**处方：咖啡案例前移做开篇钩子，命题进前 10%。**
2. **[P0] Promise 未兑现**：§1 承诺"一套完整的诊断框架"，§8 自认"无法给出"。
   机制：promise→delivery 断裂（§15）+ peak_end_rule（B）——结尾体验决定全文记忆。
   **处方：把 §5 六概念 + §8 七建议结构化为"社群身份诊断五问"框架，真正兑现承诺。**
3. **[P0] 全称化过度声称**：n=1 案例推出"所有社群的失败，归根结底都是认同感的坍塌"。
   机制：argumentation_structure（B）——warrant 缺失 + rebuttal 层空白。
   **处方：加 qualifier（"在非利益绑定的品牌社群中"）+ 补 warrant 段 + 补反方层
   （"这并不意味着激励设计无用——在交易型社群中……"）。**
4. **[P1] Fatigue Zone 结构性缺水**：§5-7 无案例无节奏变化（§11 Stage 3 处方未执行）。
5. **[P1] 概念漂移**：身份感/认同感/归属感混用（conceptual_coherence, B）——统一为
   "身份感"并首次定义。

## 6. Redundancy（§10 语义重复组）

| 组 | 内容 | 处理 |
|---|---|---|
| R1 | "发红包解决不了社群问题" ×4（§3/§6/§8/§9） | **保留 §3**（首次出现+承担设题功能）；§6 改写为补贴悖论的新证据句；§8/§9 压缩为一句回收 |
| R2 | §5"现象层"整段复述 §2 的死群图景 | **Merge**：§5 删现象段，直接从概念层进入 |
| R3 | §9 复述 §1 背景与中段命题（Conclusion Echo） | **Rewrite**：结尾改为框架回收 + 反方层 + 未决问题 |

预计压缩量：约 700-900 字（14-18%），全部来自零增量重复——
这不是"缩字"，是 Value/Cost（§31）：删的每一处都是 New Meaning = 0 的区域。

## 7. Evidence Problems（详见 longform_evidence_audit 口径）

- **E2/E4/E5/E6/E7 引用装饰**（citation decoration, AP-LF-017）：5 处"研究表明/调查显示"
  无来源。处方：能补真实来源的补（如 C5 的 5% 贡献者与 90-9-1 经验法则可注明
  practitioner heuristic, D 级）；不能补的降级为作者判断（"我的样本里……"）。
  **禁止补造文献。**
- **E3 咖啡案例 Evidence Too Weak + Too Far**：n=1 → 全称规律。替代解释未排除
  （自选择效应：愿意投票命名新品的核心顾客本就是高粘性人群——案例本身可能
  只是筛选效应而非身份效应）。
- **案例信息增量检查**：§2 三案例证同一点，第二个起边际信息量为零
  （case_stacking, AP-LF-005）→ 保留差异最大的两个（母婴品牌的"制度完备仍死"
  信息增量最大，它与"运营不努力"的替代解释相冲突）。

## 8. Cognitive Load

负荷曲线（§12）：§1 L-M → §2 L → §3 M → §4 M-H → §5 **H** → §6 **H** → §7 **M-H** → §8 L → §9 L。
连续 HIGH 区恰好落在 40-75%——违反"禁止连续多节 HIGH"。
修复后目标曲线：H（开篇案例+命题）→ L（样本）→ M（激励直觉为何失败）→
M-H（机制章，带案例锚定）→ L（**新：诊断框架=组块化低负荷节**）→ M（关系跃迁）→ L（建议+闭合）。

## 9. Narrative Thread

实际主线：背景 → 死群样本 → 激励直觉为何错 → 身份感命题 → 概念罗列 → 激励悖论 → 关系跃迁 → 建议 → 复读。
病灶：主线在 §5-7 停摆（无推进、无新问题）；§5 是 §2 的回声；§8 打破承诺造成终点悬空。
修复后的动力线：**一个反常识案例 → 命题 → 为什么激励直觉失败 → 身份感如何起作用
（机制章）→ 五问诊断框架（工具兑现）→ 边界与反方 → 行动建议 → 闭合**。
每节结尾补 Forward Momentum（§17）。

## 10. Proposed New Structure（Re-outline）

| # | 新结构 | 原位置 | WHY |
|---|---|---|---|
| 1 | 开篇=咖啡案例（钩子）+ 命题（前 10%） | 原§4 拆分 | misplaced_evidence 修复：最佳素材当前埋在 36%；serial_position（B）+ foraging |
| 2 | 三种死法（压缩为 2 案例带差异信息） | 原§2 | case_stacking 修复 |
| 3 | 为什么激励直觉总是失败 | 原§3 | 保留（全文最顺一节） |
| 4 | 身份感如何起作用（六概念重构+锚定案例） | 原§5-6 重写 | concept_dumping 修复；概念配案例、逐一锚定 |
| 5 | **社群身份诊断五问（新框架节）** | 新增 | 兑现 §1 承诺；chunking：全文压成 5 个组块；memory anchor 载体 |
| 6 | 边界与反方（这并不意味着什么） | 新增 | §20 反方层；防 overclaim |
| 7 | 从流量到关系 + 务实建议 | 原§7+§8 合并压缩 | 密度修复 |
| 8 | 闭合：框架回收 + 一个未决问题 | 原§9 重写 | peak_end_rule + retrieval_cue_design |

## 11. Cut / Merge / Move / Expand Plan

```text
Move  原§4 咖啡案例+命题 → 新§1        P0（命题前置 + 钩子）
Cut   原§1 背景 430 字 → 80 字          P0（background_overload, AP-LF-002）
Cut   原§5 现象层段（复述§2）           P1（duplicated_claim）
Merge 原§5+§6 → 新§4（机制章）          P1（六概念逐一锚定，消灭倾倒）
Cut   原§2 书店案例                     P1（第三案边际信息量为零）
Cut   原§6 黑话段 → 重写为一句具体判断   P2（buzzword_density, AP-LF-016）
Cut   原§9 复读段                       P2（summary_repetition, AP-LF-013）
Expand 新§5 诊断框架（五问）            P0（兑现承诺——唯一的 Expand，写的是工具不是字数）
Expand 新§6 反方层                      P1（"这并不意味着激励无用：交易型社群中……"）
Rewrite 原§8 承诺句                     P0（若不建框架则必须改口——二选一，推荐建框架）
```

## 12. Line-level Issues（仅清单，Pass 2 处理）

- 机械过渡 ×4（§2/§6/§7/§8："接下来我们来看看""与此同时"）（AP-LF-015）
- 黑话段 §6：生态/抓手/中台/闭环/颗粒度/赋能 ≥10 个（AP-LF-016）
- 对称偏置：§5-7 小标题同构"社群运营的X层"+ 三段式同构（AP-LF-019）
- 术语漂移实例：§4"身份感"→§4 末"认同感"→§5"身份认同、归属感"（AP-LF 概念漂移）
- 好的句子（保留）：全文作者声音鲜明，§3 的三段论讽刺、§8 的具体建议——
  Line Edit 阶段不得磨平个人语气（Preserve Author Intent，§43）

## 13. Platform Adaptation（wechat_official adapter）

- **标题**：现标题可用但偏"结论泄底"；候选：《你的社群不是死于红包，是死于
  "我在这里是谁"没有答案》（保留 curiosity_gap，暗含命题）
- **摘要**：缺——公众号摘要位应承载 thesis（前 40 字给"身份感 vs 激励"反差）
- **小标题**：改为组块名/主张句（information_scent）：如"五问诊断"而非"启示层"
- **阅读节奏**：5000 字公众号文应配 2-3 个视觉分隔/小结框（chunking 的视觉层）
- **朋友圈分享理由**：转发言口 = "先身份，后活跃"（已天然存在，Move 到更显眼位置）
- **结尾行为**：关注理由 = "下一篇给诊断框架的实操模板"（与框架兑现联动）
- 具体规则以平台最新公告为准（adapter fact_type 纪律）

## 14. Rewrite Options

1. **结构重排（推荐）**：按 §11 Editing Plan 执行 longform_restructure.md——
   预计 +1 节（框架），-800 字，动结构不动句子；
2. **证据补强**：先跑 longform_evidence_audit.md 处理 5 处引用装饰与 n=1 问题
   （需要作者确认哪些判断愿意降级为经验之谈）；
3. **全文重写**：不推荐——作者声音是本文资产（language_quality 7/10），
   重写为模板腔是净损失（§43）；
4. **只做 P0**：最小干预——命题前置 + 兑现承诺 + 加反方层，其余保留。

**交给用户选择；结构类操作须经 Proposed Outline 确认后落地（工作流纪律）。**

---

## 验证结论（工作流自检）

本报告验证了 longform 管线的全部关键环节：central_thesis 抽取（§6）✓、
argument map 八类缺陷标记（§7）✓、section role + Delete Test（§8-9）✓、
五阶段读者走查含 Fatigue Zone 定位（§11）✓、负荷曲线（§12）✓、
语义重复成组检测与保留判据（§10）✓、概念注册表（§14）✓、
promise_delivery 断裂检测（§15）✓、P0-P3 优先级（§29）✓、
十四维评分（§30）✓、类型化处方（§32）✓、分层输出（§42）✓、
作者意图保全判断（§43）✓。**15 类埋设缺陷全部命中**；workflows/longform_article_analysis.md 验收通过。
