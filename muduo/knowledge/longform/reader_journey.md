# Reader Journey（长文读者旅程模型）

> 机制依据：information_foraging（B）、information_scent（B）、cognitive_fatigue（B）、
> schema_formation（A-）、chunking（A-）、curiosity_gap（B）、peak_end_rule（B）、
> retrieval_cue_design（B）、argumentation_structure（B）

## 模型

读者不是匀速阅读的：不同进度点上，认知状态、评估标准、弃读风险完全不同。
诊断时按五阶段走查全文，每节标注所属阶段并核对检查项。

### Stage 1 — Entry（0-10%）：进入决策

读者在判断：与我有关吗 / 值得读吗 / 能得到什么 / 作者可信吗。
**机制核查**：relevance 与 identity（这是给谁的）、curiosity_gap（信息差在哪）、
specificity（承诺是否具体）、credibility（凭什么是你讲）。
**高危病症**：背景过长、delayed_thesis、"随着时代发展"式空转——
Entry 阶段每一句都在经受离开决策，空转即流失。
**产出要求**：前 10% 内完成 thesis 出现 + 全文回报地图（读完拿到什么）。

### Stage 2 — Model Building（10-40%）：建构图式

读者在组装心智模型：新概念、依赖关系、术语绑定。
**机制核查**：schema_formation（概念按依赖序引入 + 锚定材料充足）、
chunking（组块命名与层级）、概念注册表（concept_registry 无漂移）。
**高危病症**：concept_dumping（概念无锚定堆叠）、用到未定义概念（逻辑跳跃）。

### Stage 3 — Fatigue Zone（40-70%）：疲劳区

**长文最危险阶段**。认知疲劳累积（cognitive_fatigue）、新颖性衰减、
重复论证被识破、抽象过载的耐受度最低。
**处方**：结构补偿——案例、类比、数据、小结、转折、新问题、图示；
把全文最有力的案例或阶段性结论放在此区；把第二难的概念移出此区。
禁止用"更长的解释"对抗疲劳（那是加倍负荷）。

### Stage 4 — Integration（70-90%）：整合

读者开始把全文材料连接成整体：synthesis / implication / connection /
pattern recognition。此阶段读者**愿意**承受较高负荷（germane_load_learning），
但要给连接材料：跨节回连句（"这正是第二节的X"）、对照表、模型图。
**高危病症**：还在引入全新概念（图式又被撕开）、或直接跳到结尾（整合无处发生）。

### Stage 5 — Closure（90-100%）：闭合

必须完成：conclusion、takeaway、memory anchor（retrieval_cue_design：3-5 个锚点显式回收）、
action（按文章类型选）、必要时 unresolved question（为下一篇留口）。
结尾禁止 summary_repetition（把全文再说一遍）；Closure 类型选择见 longform_line_edit.md 七类检测
（Synthesis/Action/Perspective Shift/Prediction/Question/Framework/Principle）。
peak_end_rule（B）：结尾体验决定整篇的记忆评价。

## 走查输出格式

```text
| 节 | 进度% | 阶段 | 状态 | 发现 |
（每节一行；阶段转换点与风险点加注）
## 风险清单
（弃读点预测：位置 + 机制 + 处方）
```

## 与两类长度参数的换算

- 5000 字：Fatigue Zone ≈ 2000-3500 字处；
- 10000 字：≈ 4000-7000 字处（疲劳随绝对时长提前出现，区间相应前移加宽）。
越长的文章，Stage 3 的结构补偿预算越大——这是"长文不是短内容×更多字数"的最直接体现。
