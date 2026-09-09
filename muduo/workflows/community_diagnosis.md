# Workflow: Community Diagnosis（社群诊断）

用途：Mode 5。诊断社群为什么形成/活跃/沉寂/裂变/瓦解。**不做表面归因**（"发红包""多搞活动"是症状药）。

## 输入
社群定位、成员构成与规模、活跃数据（发言人数/频次/留存）、运营规则、当前问题、历史动作。

## 流程
1. **社群分类**：先判断类型（消费型/学习型/兴趣型/关系型/协作型），
   不同类型的功能性门槛不同（学习型要 identity+progress，消费型只需 utility+norm）。
2. **结构诊断**（按以下 10 层逐层检查，定位结构性缺口）：
   - **Identity**（social_identity_theory / collective_identity_narrative）：成员能说出"我们是谁"吗？有无共同身份标签？
   - **Boundary**（community_boundaries）：谁属于/不属于清楚吗？无边界=无认同
   - **Norm**（descriptive_injunctive_norms / norm_enforcement_reputation）：新人知道这里"怎么说话"吗？规范是明示的还是靠猜？
   - **Status**（status_systems）：什么行为能获得地位？发言有回应吗（地位回路）？无人回应=发言无收益=沉默理性化
   - **Reputation**（reputation_systems）：贡献被记住吗？有无可见的记录/身份/权限成长？
   - **Role**（participation_ladder）：有没有消费者→贡献者的阶梯？所有人被期待做"活跃者"吗？
   - **Ritual**（community_rituals）：有固定重复的共同事件吗（每周例会/打卡/复盘）？
   - **Reciprocity**（reciprocity_norm / reciprocity_exchange_networks）：助人有没有社会收益？还是只消耗？
   - **Newcomer Onboarding**（newcomer_onboarding）：新人 24-48 小时的体验是什么？无引导=首日沉默=永久沉默
   - **Network Structure**（weak_ties_strength / network_density / homophily）：
     群内是星型（都围着群主）还是网状（成员互联）？星型结构群主停更即死。
3. **规模校验**：用参与阶梯校准预期——大群低发言率是常态不是病；
   真正的问题是"预期管理"与"分层运营"（核心群/普通群）。
4. **动力学诊断**（沉寂/裂变/瓦解分别对应）：
   - 沉寂：多为 Norm 模糊 + Status 回路断裂 + Ritual 缺失三联征
   - 裂变失败：多为 weak ties 未激活 / 复杂行为需要多重社会确认（complex_contagion）却只给了一次触达
   - 瓦解：多为 identity 冲突 / 规范执行失灵 / 价值失衡（付出>收益持续累积）
5. **输出**：结构性缺口 ≤3 个（按因果排序）+ 每个缺口的机制依据 + 分层动作方案 + 预期时间线。

## 输出格式
```text
## 社群诊断
类型判定 + 结构总评（哪几层缺失）

## 核心缺口（≤3）
1. [缺口] —— 机制：<中文名（English）>（证据 x）；表现：[你描述的现象如何由它解释]
2. ...

## 动作方案
分阶段（0-2周 / 2-6周 / 长期），每条动作注明针对哪个缺口、预期指标变化。
不承诺具体数字，给"该观测什么指标"。

## 常见误判提醒
- 别用发红包解决结构问题（外部激励挤出内在动机：intrinsic_extrinsic_motivation）
- 大群低活跃≠失败：检查预期与分层
- 拉新解决不了沉寂：先修容器再进水
```

## 禁止
- 把所有问题归因"缺少激励"
- 建议刷活跃/买水军（bot_amplified_social_proof 反模式）
- 无规模校验直接判"活跃度差"
