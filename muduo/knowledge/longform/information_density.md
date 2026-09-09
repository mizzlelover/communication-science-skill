# Information Density（长文信息密度工程）

> 机制依据：information_foraging（B）、information_scent（B）、processing_fluency（A-）、
> cognitive_fatigue（B）、semantic_redundancy 操作规范（见 semantic_redundancy.md）

## 定义

```text
Information Density = New Meaning / Reading Cost
```

每千字向读者交付的新含义量。两个极端都是病：

| 状态 | 症状 | 读者行为 | 处方 |
|---|---|---|---|
| **过低** | 水、重复、空话、AI 套话、无效铺垫 | 觅食判断"收益递减"→ 跳读/弃读（information_foraging） | 语义压缩：保留信息量最大的一句，删除同义重复 |
| **过高** | 密集概念、无锚定数据流、连续抽象 | 负荷超限 → 疲劳提前 + 无法记忆 | 加锚定（案例/类比）、拆概念、加小结（chunking） |

## 密度的三种假象

1. **字数多 ≠ 密度高**：AI 生成文本的典型特征是字数多而 New Meaning 趋零
   （ai_content_saturation, C）。检测法：对每段问"删掉后读者损失什么？"（Delete Test）。
2. **术语多 ≠ 密度高**：buzzword_density 是 New Meaning ≈ 0 的高成本文本——
   最差的密度比值。抽象名词必须兑换成具体所指（concreteness_in_language, B+）。
3. **案例多 ≠ 密度高**：case_stacking——多个案例证同一主张，第二例起边际信息量趋零
   （Evidence Redundancy）。

## 逐节密度标记

LOW / MEDIUM / HIGH 三档，与认知负荷曲线**联合审读**：

```text
密度低 + 负荷低 = 水区（Cut 候选）
密度低 + 负荷高 = 最差象限（抽象空转，Rewrite 候选）
密度高 + 负荷高 = 危险区（拆解 + 锚定，或移出 Fatigue Zone）
密度高 + 负荷低 = 理想态（案例讲透了复杂道理）
```

## 与信息觅食的联动

读者在每个 patch 边界（小标题、空行、小结）做"继续/离开"决策。
密度的**分布**比均值重要：全文平均密度合格但中段连续三节低密度，
仍会在 40-70% 区间制造弃读点。优化目标是"密度曲线无长洼地"，
而非"全文平均密度最高"。

## 删除的判据（重申）

删什么不删什么，标准是 Value/Cost：
- 有必要且无替代 → 保留（哪怕长）
- 同义重复 → 保留最优一句（semantic_redundancy.md 的保留判据）
- 离题但有趣 → Move 到另一篇/脚注，不是硬删
目标：**Maximum Meaning per Unit of Reader Effort**，不是 Minimum Word Count。
