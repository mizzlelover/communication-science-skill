# Workflow: Long-form Article Optimization（长文两遍优化：结构编辑 → 逐句编辑）

前置条件：**必须已完成 longform_article_analysis.md 的诊断**（P0 问题已识别）。
无诊断不优化；用户只要"润色"而存在 P0/P1 结构问题时，先提示 Structural Editing 优先并征得确认（Case F 假润色情形）。

## 0. 两遍优化铁律

```text
Pass 1 — Structural Editing（结构编辑）
  处理：中心命题 / 整体逻辑 / 章节排序 / 删除 / 合并 / 补充 / 证据 / 案例 / 论点 / 认知节奏
  禁止：此阶段优先润色句子。
  原因：不应花成本润色最终应该删除的段落。

Pass 2 — Line Editing（逐句编辑，见 longform_line_edit.md）
  结构确认后才处理：句子长度 / 清晰度 / 节奏 / 用词 / 转折 / 重复 / 段落连接 / 术语一致性 / 可读性
```

## Pass 1 执行流程

### 1. 编辑计划（Structural Compression）
对每节/每段给出六类操作，形成 Editing Plan：

```text
Keep / Merge / Move / Cut / Rewrite / Expand
例：Section 2 + Section 3 → Merge（同证一论）
    Section 5 → Move before Section 4（论点依赖反转）
    Section 6 → Cut 40%（同义重复区）
    Section 8 → Expand evidence（核心主张只有案例支撑）
```
每项必须附 WHY 与优先级（P0-P3）。**禁止 P0 未解决就投入 P3。**
删除标准：Value/Cost。确有必要的长内容保留——目标是
**Maximum Meaning per Unit of Reader Effort**，不是 Minimum Word Count。

### 2. Re-outline
产出 Proposed Outline：Original Structure vs Proposed Structure 对照 +
每项调整的 WHY。这是与用户确认结构的载体——**结构未经用户确认不得进入逐句编辑**。

### 3. 结构执行中的保全规则
- **Preserve Author Intent**：保持 author voice / argument intention / tone /
  originality；除非用户明确要求改变风格，禁止把文章重写成"AI 标准模板"。
- **Preserve Valuable Complexity**：Simplify Expression, Not Reality——
  复杂问题不许为了易读降级成错误简单结论；可以拆解、举例、分层，不可偷换。
- **Global Coherence**：每次局部编辑后核对 argument map / concept registry /
  long-range coherence 是否仍成立。超长文按分块执行，每块完成后更新 longform_state.yaml。

### 4. 结构层 Quality Check（Pass 1 出口条件）
- [ ] central_thesis 一句话成立且在合适位置出现（通常前 10-15%；典型情形：前三千字无观点→前移 Thesis）
- [ ] argument map 无 P0 级 unsupported_claim / conclusion_leap / contradiction
- [ ] 认知负荷曲线不再有连续 HIGH 区
- [ ] Fatigue Zone（40-70%）至少安排了一次节奏变化（案例/类比/小结/转折）
- [ ] 语义重复组已压缩（保留最好的一句，删除其余）
- [ ] 概念注册表无 multiple_names / shifting_definition
- [ ] open_question / promise 全部有 resolution / delivery
- [ ] 三类 Hook 齐备（Entry / Continuation / Macro）

## Pass 2 执行流程

转交 `longform_line_edit.md` 执行，聚焦：句子长度与节奏、表达清晰度、转折与连接、
术语一致性、AI 写作七类检测、可读性。**逐句编辑不得引入新的结构变动**；
若编辑中发现结构问题，回到 Pass 1。

## 对比输出

支持 Original vs Optimized 对比，但**不做全文逐句 Diff**。重要修改按四元组说明：

```text
Problem（原稿问题） → Change（改了什么） → Reason（为什么） → Mechanism（机制依据＋最小边界单元：等级＋一句适用条件，铁律 2）
```

**反模式闭环规则（强制）**：诊断命中并进 Editing Plan 的每条 AP-LF
（见 longform_article_analysis.md §3b 对照表第三列），必须在结构重排或逐句编辑中
实际执行其修复动作，并在"改动说明"里以 AP-LF 编号对账——检测→修复可追溯。
用户只要求部分优化时，未处理的 AP-LF 项列入"遗留项"并说明理由。

**Platform Fit 字段绑定（强制）**：优化输出的 "Platform Fit" 部分（分层输出）
必须引用 adapter 具体字段名 ≥2 个（title_role / cover_role / opening_role /
interaction_signals / sharing_mechanism / search_mechanism / risk_factors 等），
说明哪些优化动作对应哪个平台要素——禁止"注意平台调性"式空话。

## 最终输出（分层）

```text
## Top 3 Critical Issues（改前改后对照）
## Structural（结构层改动清单：Editing Plan 执行结果 + 新大纲）
## Evidence（证据层：补强/降级/处理记录）
## Reader Experience（负荷曲线变化 + Fatigue Zone 处理 + Memory Anchors）
## Language（Pass 2 摘要：典型修改 5-10 处，四元组格式）
## Platform Fit（标题/摘要/小标题/分享理由等平台适配，引用 adapter 字段）
## 遗留项与建议（P2/P3 未处理项 + 理由）
```

## 评分

优化前后各出一次十四维评分（1-10 分，每维附原因）：
Thesis Clarity / Argument Coherence / Structural Efficiency / Evidence Strength /
Cognitive Load / Information Density / Narrative Momentum / Concept Consistency /
Reader Orientation / Trust / Memory / Actionability / Language Quality / Platform Fit。

## 禁止

- 无诊断直接改写；结构未确认进入逐句润色；
- 一次给几十条平铺建议（先 Top 3 Critical，再 Structural/Evidence/Reader Experience/Language 分层）；
- 为"易读"破坏论证；为"字数"删除有价值内容；
- 重写成模板腔；隐藏作者观点或改写立场。
