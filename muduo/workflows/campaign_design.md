# Workflow: Campaign Design（传播/活动设计）

用途：Mode 5。从目标出发设计一次传播或活动。**先定目标行为，再倒推机制组合**，禁止"先想创意再找理由"。

## 输入
主题/产品、目标受众、平台、传播目标（§4 六目标：Reach/Virality/Engagement/Community/Conversion/Retention，可多选但必须排序）、品牌约束、预算与资源、时间窗。

## 流程
1. **目标排序**：让用户对六个目标排序。目标冲突必须显式说明
   （如 Reach 与 Conversion 常冲突：广传播内容转化弱，强转化内容传播弱——机制上因为
   social currency 与 purchase intent 调用的机制不同）。
2. **受众画像**：身份（社会认同）、所处情境（注意力环境）、与产品的
   关系（jobs_to_be_done）、在他们已有的信息环境里内容会遇到什么竞争。
3. **机制组合设计**（按目标从 SKILL.md §3 检索表选机制，形成"机制组合卡"）：
   - Reach：attention 层组合（curiosity_gap + processing_fluency + 平台信号）
   - Virality：stepps_sharing_framework 逐项打勾（社交货币/触发物/情绪/公开性/实用价值/故事）
     + 确认分享成本（转发渠道顺畅度、转发言口）
   - Engagement：emotional_arousal + 评论靶子 + 身份表达位
   - Community：complex_contagion 意识（加入行为需要多重社会确认）+ Ritual 设计 + Boundary + Status
   - Conversion：perceived_purchase_risk 拆解 + friction_reduction + 承诺阶梯 + 真实稀缺（如有）
   - Retention：hook_model(D) 的习惯结构 + 内在动机保护（self_determination_needs）
4. **内容矩阵**：为各平台角色分工（不要求全平台同款）：
   主阵地（深度内容）+ 引流位（算法平台短内容）+ 私域承接（社群/私聊）。
   每个位置写明：目标 Behavior Goal、核心机制、成功指标。
5. **复杂行为专项检查**：目标行为越重（入群>关注>点赞>观看），
   越需要多次曝光与多重确认（complex_contagion, B+）：设计触达序列而非单点爆炸。
6. **伦理与合规审查**：过 anti_patterns 清单（fake scarcity/clickbait/engagement bait 等）；
   高唤醒手段检查 emotional_arousal 边界；承诺必须可兑现（trust_calibration）。
7. **指标设计**：每个目标给观测指标与合格线区间（不承诺数字效果，
   因为分发结果受平台/竞争/时机外生变量影响——诚实声明）。

## 输出格式
```text
## 目标排序与冲突说明
## 受众与情境
## 机制组合卡
| 目标 | 机制 | 用法 | 证据 |
## 内容矩阵
| 位置 | 平台 | 目标 | 形式 | 指标 |
## 触达序列（复杂行为）
## 伦理检查（已排除的反模式）
## 指标与观测点
## 主要风险与边界
```

## 禁止
- 承诺具体涨粉/转化数字
- 用案例反推因果（"别人这么做过成了"≠因果）
- 单平台押注而不做风险对冲（platform_power_gatekeeping）
- 把 viral 当默认目标（多数业务应该 Optimize Community/Conversion/Retention）
