# Workflow: Long-form Line Edit（长文逐句编辑 = Pass 2）

前置条件：**Pass 1（结构编辑）已完成且大纲经用户确认**（longform_article_optimization.md）。
本阶段不得引入结构变动；发现结构问题立即退回 Pass 1。

## 1. 处理范围（Pass 2）

句子长度 / 表达清晰度 / 节奏 / 用词 / 转折 / 重复 / 段落连接 / 术语一致性 / 可读性。
执行时以 concept_registry 为术语基准：同一概念全文用同一叫法，别名仅在有意的修辞场合出现。

## 2. AI 写作七类检测（逐节扫描）

| 检测项 | 特征 | 处理 |
|---|---|---|
| **AI Semantic Repetition** | 同一观点反复换句话说（"AI降低生产成本"↔"AI让内容更廉价"↔"AI时代内容成本快速下降"） | 语义压缩：**判断哪句最好并保留**，删除其余——不是把三句都润色得更漂亮 |
| **Artificial Completeness** | 为显全面机械罗列大量维度 | 按信息密度筛选：删除对主线无贡献的维度（information_overload, B） |
| **Symmetry Bias** | 每节结构完全一样（AI 生成长文的标志性特征，ai_content_saturation, C） | 按各节功能（role）差异化结构；uniformity 是无记忆点的来源 |
| **Empty Transition** | "此外/与此同时/值得注意的是"高频空转 | 换成回答"为什么现在讲这个"的实质过渡 |
| **Abstract Inflation** | 大量抽象名词无具体所指 | 具体化（concreteness_in_language, B+）：加主语、加数字、加场景 |
| **Fake Depth** | 语言复杂但无新增观点 | Delete Test：无新增信息的"深度表达"整句删除 |
| **Conclusion Echo** | 结尾只是把开头再说一遍 | 改为真正的 Closure：Synthesis/Action/Perspective Shift/Prediction/Question/Framework/Principle |

同源反模式（knowledge/anti_patterns/longform_anti_patterns.yaml）一并对照：
background_overload / concept_dumping / case_stacking / overexplaining / underexplaining /
narrative_drift / argument_jump / premature_conclusion / summary_repetition / over_sectioning /
buzzword_density / delayed_thesis / mechanical_transition / false_depth。

## 3. 逐句层规则

0. **AP-LF 对账（强制）**：Pass 1 诊断命中的 AP-LF 中，修复动作绑定 line_edit 的条目
   （AP-LF-001/006/008/011/013/015/016 等，见 analysis §3b 对照表第三列）必须在本阶段
   实际执行；每处修复在"典型修改"清单中标注对应 AP-LF 编号，未执行项写入"遗留"并说明理由——
   检测→修复在编号层可追溯。

1. **节奏**：连续长句拆分；每 3-5 段设一个低负荷呼吸点（短句、设问、小结）——
   服务认知负荷曲线在微观层的延续。
2. **术语一致性**：以 concept_registry 为准；术语首次出现后不再重复定义
   （overexplaining），除非新章节面向新读者群。
3. **过渡**：每节结尾检查 Forward Momentum（continuation hook）；
   机械过渡句全部重写为"承接上节结论 → 提出下节问题"。
4. **段落连接**：段落首句承担路标功能（gist_vs_verbatim_memory, A-：扫读者只读首句）；
   首句必须能独立传达该段主张。
5. **不改写立场**：Preserve Author Intent——语气、人称、观点强度保持作者原貌；
   只动表达不动观点。
6. **不复写复杂度**：把复杂句改简单时核对语义是否等价；
   Simplify Expression, Not Reality。

## 4. 输出格式

不做全文逐句 Diff。输出四元组清单（5-15 条典型修改）+ 全文终稿：

```text
## 典型修改
| # | 位置 | Problem | Change | Reason | Mechanism（最小边界单元：等级＋一句适用条件） |
## 终稿
## 遗留
（P3 未处理项与理由）
```

## 质量出口检查

- [ ] AI 七类检测全部清零或有意识保留（保留需说明理由，如修辞性重复）
- [ ] 术语全文一致（concept_registry 复核）
- [ ] 抽查 5 个段落：只读每段首句能否还原文章主线（gist 路径测试）
- [ ] 语言层评分（language_quality）较改前提升且有记录

## 禁止
- 越权改结构（退回 Pass 1）；
- 把作者的个人语气统一成"AI 标准腔"；
- 为消灭重复而删除有修辞功能的重复（区别对待：信息重复删，修辞重复留）。
