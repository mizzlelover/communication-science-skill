# Workflow: Long-form Restructure（长文结构重排）

用途：执行 longform_article_analysis 诊断后的**结构级重构**（Editing Plan → Proposed Outline → 重排落地）。
只动结构与内容组织，不动句子表达（表达归 longform_line_edit.md）。

## 输入
诊断报告（Top Structural Problems + Editing Plan）、原文、文章类型、
用户对 Proposed Outline 的确认。

## 操作库

| 操作 | 判定依据 | 关键检查 |
|---|---|---|
| **Cut** | Delete Test = REDUNDANT / OFF_TOPIC / OPTIONAL 且非主线 | 删除后 argument map 是否出现断链；被删段是否有唯一信息需先迁移 |
| **Merge** | 多节证一同论（duplicated_claim）或多节同功能 | 合并后保留最好的表述（语义压缩：判断哪句最好，而非全部润色）；小标题层级是否仍平衡 |
| **Move** | misplaced_evidence / 论点依赖反转 / 主题错位 | 移动后前后过渡是否成立；不动读者的认知依赖顺序（先概念后应用、先问题后方案） |
| **Rewrite** | 该节功能必须存在但现有实现失败（如 thesis 节藏在解释里） | 重写范围仅限该节；不得顺手改变其他节 |
| **Expand** | 核心主张证据不足（weak_evidence）或承诺未兑现（promise_delivery 缺失） | 扩的是证据/反方/边界，不是字数；不得引入编造出处 |
| **Keep** | Delete Test = ESSENTIAL / 高价值 SUPPORTING | 无 |

## Re-outline 输出格式

```text
## Original Structure
1. ...（role: context）
2. ...
## Proposed Structure
1. ...（原§4 前移：thesis 应在 10% 内出现——机制：serial_position_effect（B）+ reader_journey Stage1）
   ...
## 每项调整 WHY
- §2+§3 合并：两节共同支撑 C2，且 §3 无独立信息（Delete Test: REDUNDANT）
- §5 前移至 §4 前：C3 的证据被引用于其后才出现的概念——logical_gap
- ...
## 重排后预期
（负荷曲线 / 叙事主线 / 长程承诺兑现的变化）
```

## 执行纪律

1. **顺序**：先 Cut（删掉不该存在的）→ Merge → Move → Expand → Rewrite。
   先删再排，避免为将死内容做无谓搬运。
2. **每次 Move/Merge/Cut 后**：核对 argument_map 的 section_refs、concept_registry 的
   first_appearance、long-range coherence 映射，更新之（Local Edit 不破坏 Global Coherence）。
3. **认知节奏**：重排后重画 Cognitive Load Curve 与 Fatigue Zone 排布，
   HIGH 负荷节之间必须有 LOW/MEDIUM 缓冲；40-70% 区间至少一个节奏变化点。
4. **作者意图**：Move/Rewrite 不得改变作者立场与论证方向；对核心论证的重排
   必须在 Proposed Outline 阶段获得用户确认后才落地。
5. **超长文**：按分块协议逐块执行，每块完成即更新 longform_state.yaml
   （completed_sections / editing_decisions / pending_issues）。

## 输出

```text
## 新大纲（定稿）
## 执行记录（对账要求）

每项操作标注：操作 / 位置 / WHY / **对应的 AP-LF 编号**（来自 analysis §3b 对照表第三列；
无对应反模式的结构性调整标注"general"）/ 对论证图与负荷曲线的影响——
检测→修复在编号层可追溯，重排完成后与诊断命中的 AP-LF 清单逐条核对，未处理项说明理由。

## 重排后核查
（argument map 无断链 / 概念注册表一致 / 承诺全兑现 / 三类 Hook 齐备）
## 交接
（结构定稿 → 转 longform_line_edit.md 做逐句层）
```

## 禁止
- 未经用户确认直接落地结构重排；
- 重排顺手润色句子（层级越权）；
- 删除有价值复杂内容以凑"精炼"。
