# Narrative Thread（长文阅读动力线）

> 机制依据：narrative_transportation（B+）、curiosity_gap（B）、suspense_structure（D）、
> zeigarnik_effect（B）、prediction_error（A）、information_foraging（B）

## 原则

研究型、咨询型长文同样需要 Narrative Thread——不是编故事，
而是**阅读动力线**：让读者在每个节点都有"想知道下一步"的理由。
叙事传输（narrative_transportation, B+）不依赖虚构：一个展开良好的论证
本身就是一种传输体验。

## 主线建模

把全文压缩成一条动力线（示例）：

```text
Problem → Unexpected Cause → Theory → Evidence → New Model → Practice
```

或咨询型：Situation → Complication → Question → Answer → Proof → Action（SCQA 变体）。
诊断时先从文本中**还原**作者实际的主线（不是理想的），再对比检查五类病灶：

| 病灶 | 特征 | 机制后果 |
|---|---|---|
| 主线中断 | 某节与前后节无推进关系 | 读者在断点做"继续值得吗"评估（foraging） |
| 旁枝过长 | 背景资料/支线超过 2 节 | narrative_drift：读者忘了在读什么 |
| 背景失控 | context 功能节占比 > 20% | delayed_thesis，Entry 阶段信心流失 |
| 案例抢线 | 案例自身展开过长，挤掉论点推进 | 案例成为新 patch，读者注意力换轨 |
| 中途换题 | 全文出现第二条平行主线 | 论证图分叉，读者必须二选一跟随 |

## Hook 三层与动力线的关系

- **Entry Hook**（为什么开始读）：由主线第一步的张力承担（问题/反差/代价）。
- **Continuation Hook**（为什么继续下一节）：每节结尾的 Forward Momentum——
  未闭合的问题（zeigarnik）、预告的反转（prediction_error）、未兑现的承诺。
- **Macro Hook**（为什么值得读完整篇）：全文终点价值的预告——
  "读到这里你将拿到什么"。三 Hook 缺一，动力线都会在对应位置断。

## 与两遍优化的衔接

- Pass 1（结构）：主线断裂靠 Move/Merge/Cut 修复——先保证线是通的；
- Pass 2（逐句）：节尾 continuation hook 句的打磨——线通之后加固每一段接口。
  顺序不可反（Macro before Micro）。

## 检查问题清单

- [ ] 能否用一句话说出全文动力线？
- [ ] 每节结尾：读者有什么理由翻到下一节？
- [ ] 最长的一段"无新进展"区间有多长（字数/阅读分钟）？
- [ ] 有没有哪条支线可以砍掉而不伤主线？
- [ ] 结尾是闭合了主线，还是开了新头？
