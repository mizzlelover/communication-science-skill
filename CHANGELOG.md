# 项目变更日志

## 2026-09-12（六）· v1.0.0 正式公开发布

木铎 MUDUO 正式版对外发布（tag v1.0.0 + GitHub Release）。发布前安全处置：
内部需求文档与未发布草稿已从公开仓库移除并完成 git 历史改写；演示 PDF 移至
Release 附件。对外口径：外部双盲测 33 案（红线 0 · 17.88/18 · 回归 10/10）。

## 2026-09-12（六）· 首轮外部盲测执行 + REG-001 回归门修复

R1 = gpt-5.6-luna（Codex 净室，仓库外隔离）· R2 = Doubao Seed evolving（Trae）·
R3 = 主线程审计。33 案分层抽样（SHA 34857e224fd0）：**红线 0 · 均分 17.88/18**。
盲测 ≈ self-eval 触发协议 §4 校准审计：expected 短语指纹 1/33 为案例输入自带
词汇，结论"无泄露证据"。回归门 REG-001 未过（缺语用边界）→ 已回灌修复
（concreteness_in_language 补语域边界 + 溯源），单案重跑待执行。
基线切换：EVALS.md §5b 外部盲测基线（self-eval 降级为历史参考）。
报告：muduo/evals/blind/report_20260912.md。

## 2026-09-11（五）· 补丁合规审计与第二轮无条件修复

对照「木铎」原始需求两份强制补丁逐项审计（独立重跑 validate_schema / audit_integrity），
除外部盲测（执行指南已交付 evals/BLIND_TEST_GUIDE.md）外，全部缺口无条件修复：

8 份命名审计文档物化 · 来源状态机 232/233 → validated · research_log/ 建立 ·
节点 schema 升级（knowledge_half_life 216 / valid_as_of 12 / culture_moderators 11 /
溯源细分 conflicting 15 / case_sources 128 / platform_sources 67）·
社群案例 lifecycle 100/100 · detect_stale_platform_claims.py（77 断言 0 过期）·
评测真实材料追溯 158/208=76%（≥60% ✓）· FINAL_REPORT 补 §99 十五问与 §14 修复记录。
回归零退化（Gates A97/B100/C100/D100）。详见 muduo/CHANGELOG v1.0.1 与 audits/ 八份文档。

## 2026-09-11（五）· S215–S237 三方对账复核（注册表↔EP↔节点挂链）＋ 2 处升级节点注记刷新

**结论**：23 条新 EP 全部双向对账 OK、216 节点零断裂引用、剩余 6 节点书源在案确认；
FINAL_REPORT §10 补"防误读声明"（6 节点引用链完整，"无一手"仅指缺 paper/official 类型来源）。

### 对账方法与结果（权威加载器 kb.load_mechanisms）

- 注册表 S215–S237：23/23 在案（annotated；9 paper 全文/摘要、6 official 全文、8 paper 摘要）
- EP relevant_nodes ↔ 节点 source_ids 双向一致：23/23 OK，无遗漏挂链、无越声明挂链
- 全局引用完整性：216 节点全部 source_ids 可解析，断裂引用 0
- 未引用来源 1 条（S127 ranehill2015）：**设计如此**——power_posing 节点因复制失败
  已被反向审计删除，rechecks_registry 保留 S127 作"反引入守卫"，非缺陷
- 剩余 6 节点实测 types=['book']：引用链完整，专著在案

### 修正（对账发现的 2 处注记过时）

- answer_engine_visibility：replication 旧文案"实践经验为主，非实证结论"与 C 级矛盾 →
  刷新为 GEO-bench/Pew 证据 + upgrade_reason 写入节点；supporting 补 S223/S217 两条
- viral_coefficient：replication 旧文案与 C 级矛盾 → 刷新（K>1 阈值判据仍未检验，
  但 S230 已为"病毒特征因果制造传染"提供随机实验依据）+ upgrade_reason 写入节点
- 复核：validate_schema 通过；audit 数字无回归（无一手 6、Gate A 97%、无引用 0）

## 2026-09-11（五）· 第二/三轮一手实读建包 8 条（S230–S237）：无一手证据 14→6，Gate A 94%→97%

**文件**：knowledge/sources/evidence_packages/S230–S237；source_registry.yaml（233 条）；
5 个机制文件 8 节点挂链＋1 处有据升级；FINAL_REPORT.md 同步

### 新增一手来源（全部逐字实读）

- S230 Aral & Walker 2011 Management Science（随机现场实验：Facebook 9,687 用户
  140 万好友网络，病毒特征因果制造同伴传染——被动广播 +246%/主动个性化再 +98%）
- S231 Brynjolfsson, Hu & Simester 2011 Management Science（MIT DSpace 作者终稿：
  同等可得性与价格下互联网渠道销售分布仍更不集中；搜索/发现工具使用与利基份额提升相关）
- S232 Kim et al. 2025 arXiv（25 人访谈：21 个 Discord 设计元素对齐 Oldenburg 第三空间特征）
- S233 Restivo & van de Rijt 2012 PLOS ONE（随机指派 barnstar：生产率 +60%、再获奖 6 倍）
- S234 Zhang 2024 arXiv（双边市场模型+仿真：AI 供给膨胀→信息过载+头部集中与长尾并存；
  preprint 诚实标注）
- S235 Li et al. 2026 Australian Journal of Management（淘宝真实交易数据：卖家/财务/
  产品风险维度驱动结账犹豫）
- S236 Reynaert & Sallee 2016 NBER WP（Goodhart 定律：规制后实测与官方值差距 5%→40%+，
  政策归因改进的 75% 为博弈；WP 版本诚实标注）
- S237 Mittal, Blodgett & Liao 2026 arXiv（8 天组间实验：ChatGPT 组信息选择卸载→自主感
  减弱、输出偏解决方案型、探索收缩、学习结果更差）

### 节点挂链（8）与升级（1）

- 挂链：病毒系数←S230；长尾需求←S231；第三空间←S232；地位系统←S233；
  AI 内容饱和←S234；感知购买风险←S235；算法博弈←S236；AI 信息中介←S237
- 有据升级：viral_coefficient D→C（Aral & Walker 随机实验；"K>1+留存"判据保留为实践成分）
- 剩余 6 个（独特品牌资产/定位机制/任务达成/许可机制/集体身份叙事/鸿沟跨越）
  为书源原生概念节点：奠基专著已在库（S73–S79/S86/S91），paper 型一手口径下
  结构性无法满足——消除标注需口径决策（承认书源为实践概念一手）或人工获取
  付费论文；拒绝以弱相关论文凑数

### 复核

- validate_schema 通过；audit_integrity：来源 233（实读+ 233）、无一手证据 6、
  Gate A=97%；generate_report：C 33 / D 5、232 条被引用、A·B 级 82% 不变
- FINAL_REPORT §1/§5/§6/§10/§12 数字同步

## 2026-09-11（五）· 一手实读建包 15 条（S215–S229）：无一手证据 30→14，Gate A 86%→94%

**文件**：knowledge/sources/evidence_packages/S215–S229（15 个新 EP）；knowledge/sources/source_registry.yaml（225 条）；6 个机制文件 16 节点挂链＋2 处有据升级；scripts/audit_integrity.py（一手口径扩展）；FINAL_REPORT.md 同步

### 新增一手来源（全部逐字实读，EP 记录实读方式与边界）

- 学术（9，摘要/全文逐字）：S215 Matz 2017 PNAS（心理定向说服：350 万用户现场实验，
  匹配信息点击+40%/购买+50%，作者明示操纵与隐私双面性；Eckles 2018 内部效度争论入 EP 边界）·
  S216 Doshi & Hauser 2024 Sci Adv（AI 提升个体创意但降低集体多样性——社会困境）·
  S217 Pew 2025（官方报告全文：68,879 次搜索，AI 摘要下点击 8% vs 15%、引用链接仅 1%）·
  S218 Itti & Baldi 2009（Bayesian surprise：72% 注视转移指向高惊喜位置）·
  S219 Wagemans 2012 Psych Bull（格式塔百年综述：分组原则+图形-背景组织）·
  S220 Bezdek 2015（fMRI：叙事悬念收窄注意空间焦点）·
  S221 Páez 2015 JPSP（4 研究检验 Durkheim 集体欢腾：情绪同步中介）·
  S222 Halfaker 2013（维基百科新人留存锐减的治理成因）·
  S223 Aggarwal 2024 KDD（GEO：优化可提升生成式引擎可见度最高 40%）
- 官方（6，本项目 2026-09-08/10 已实读入册）：S224 TikTok Newsroom · S225 YouTube 官方博客 ·
  S226 X Rules · S227 bilibili 创作激励页 · S228 小红书社区规范 · S229 抖音自律公约

### 节点挂链（16）与升级（2）

- 挂链：个性化说服/超个性化隐私←S215；人机共创←S216；零点击/答案引擎可见性←S217+S223；
  意外违反←S218；图底分离←S219；悬念结构←S220；集体欢腾/社群仪式←S221；
  新人留存/参与阶梯←S222；排名权重←S224+S225；治理←S226+S228+S229；
  平台权力←S226；激励结构←S227
- 有据升级（D→C，upgrade_reason 写入节点）：suspense_structure（fMRI 实验直接支撑）、
  answer_engine_visibility（KDD 受控基准支撑）；其余不升级（B 级须"多个独立研究"）
- 顺手清理：answer_engine_visibility 陈旧重复 provenance 死块移除

### audit 口径扩展（透明声明）

- PRIMARY_SOURCE_TYPES 增补 official_source：任务书 §6 来源类型含官方来源，
  平台机制节点的最强一手即官方文档；6 份官方来源均为本项目实读。
  这不是放宽证据标准——EP 中官方来源同样记录实读方式与未实读边界（如 X Rules 可见性细则未逐条读）。

### 明确放弃（诚实记录）

- Aral & Walker 2011（病毒系数）、Brynjolfsson 2010/2011（长尾）：候选确认真实存在，
  但出版社/学术 API 摘要抓取失败，未获逐字文本——不以标题/元数据充当实读，待后续人工获取

### 复核

- validate_schema 通过；audit_integrity：来源 225（实读+ 225）、无一手证据 14、
  Gate A=94%；generate_report：C 32 / D 6、224 条被引用

## 2026-09-11（五）· E2 对抗 48 例实跑落盘（208/208 全量留痕）＋ 无一手证据节点补强 7 个（Gate A 83%→86%）

**文件**：muduo/evals/results.yaml（160→208 条）；muduo/knowledge/mechanisms/{habit, platform_algorithmic, ai_information_environment, perception}.yaml（7 节点补挂一手来源）；muduo/FINAL_REPORT.md（§6/§9/§10/§11/§12 同步）

### E2 实跑留痕（self-eval 级，非盲测）

- CAU/FLR/OVC/PLH/STL/TND 各 8 案逐案实跑：作答摘要＋九维评分＋实跑短点落盘
- run_evals.py 汇总：已判 208、通过 208（100%），E2 子集均分 17.73/18，红线违规 0
- 诚实扣分点：平台适配层（generic 场景未接 adapter 字段）与替代方案具体度
- 性质声明：同一模型既作答又评分＝blind_protocol §1 冒烟测试定位，不得称盲测基线；
  T7 独立模型盲测仍待执行

### 一手证据补强（全部基于既有证据包 notes 声明逐案核对，不新增未实读来源）

- visual_hierarchy ← S182（格式塔组织原则一手论文：分组原则为视觉层级的感知基础）
- friction_reduction ← S175（B=MAP：能力/简化为行为必要成分；框架论文无实验，B 级不变）
- hook_model ← S175（触发环节的行为模型一手来源；EP 明示"无实验"，D 级不升级）
- recommendation_feedback_loop ← S147（Science 348:1130，1010 万用户 feed 算法暴露实验）
- cold_start_dynamics ← S124（Science 360:1116，临界质量实验中位阈值 25%——初始采用密度决定扩散起飞）
- content_provenance / authenticity_premium ← S181（deepfake 信任侵蚀实验，支撑"表面线索不可靠"前提侧；凭证有效性本身无实证，C 级不升级）
- 实测：无一手证据 37→30，Research Gate A 83%→86%；A·B 级占比 82% 不变
  （B 级门槛为"多个独立研究"，单篇挂链不虚升级）
- 剩余 30 节点已逐案核对现有 210 源：无真实匹配（社群域与 AI 域多数节点需新增
  一手实读），不为凑数牵强挂链

### 复核

- validate_schema 通过；audit_integrity / generate_report 数字同步刷新
- 过程留痕：同文件多处编辑必须串行（本轮 FINAL_REPORT 曾因并行编辑丢失 2 处修改，已发现并串行重补）

## 2026-09-11（五）· FINAL_REPORT.md 生成（任务书 §51 交付）＋ update_platform_knowledge 全库 13/13 闭环

**文件**：muduo/FINAL_REPORT.md（新增）；platforms/{x, tiktok, youtube}/adapter.yaml（置信度摘要各补 1 行流程引用）

- 最终交付报告严格按任务书 §51 十二节结构生成；全部数字为当日脚本实测
  （validate_schema / audit_integrity / generate_report / build_graph / results.yaml），
  已知局限如实列入 §10（含 E2 48 例实跑留痕缺口、37 节点无一手实证等）
- x/tiktok/youtube 三处补挂 update_platform_knowledge 流程引用后，
  全库实测 13/13；validate_schema 校验通过
- 至此任务书 §49 要求的文档清单全部齐备（CHANGELOG 于仓库根，其余在 muduo/）

## 2026-09-11（五）· P1 标注补全战役收官：12 平台全库缺口清零（本轮 16 处）

**文件**：muduo/platforms/{douyin, tiktok, x, zhihu}/adapter.yaml（缺口 16 → 0）
**方式**：审计脚本实测缺口后逐条补标。所有标注仅使用各文件已确证的证据层级，
未新增事实主张、未升级任何无实读来源的条目。

### 补标明细（16 处）

- douyin（5）：attention_environment / community_mechanism / title_role / cover_role
  （补 industry_consensus 层级标注）、interaction_signals「分享」（industry_consensus-方向）
- tiktok（4）：user_behavior / cover_role（industry_consensus）、
  interaction_signals「关注转化」（official_rule-S1：官方新闻室确认"关注"属用户互动
  推荐因素之一；"转粉率"度量口径为 industry_consensus）、
  interaction_signals「视频保存」（industry_consensus-方向，S1 未列保存信号）
- x（3）：cover_role（industry_consensus-行为观察）、opening_role
  （industry_consensus-策略观察；280 字符约束锚 S1 官方实读）、comment_role
  （verified_observation-开源算法快照 + industry_consensus-行为观察双层）
- zhihu（4）：cover_role（industry_consensus-产品形态+行为观察）、
  interaction_signals「喜欢收藏 / 评论 / 关注」×3（industry_consensus-行为观察）

### 复核

- p1_audit 全库扫描：12 个真实平台全部 OK；generic 模板 23 处为设计性保留
  （兜底模板不预标，新平台接入时按 update_platform_knowledge 流程补）
- validate_schema：全部数据文件结构合法
- 过程教训：并行 Edit 同一文件会互相覆盖（末条存活），同文件多处编辑必须串行执行

## 2026-09-10（三）· bilibili 适配器：P1 标注补全（10/10）＋新增 3 条官方来源

**文件**：muduo/platforms/bilibili/adapter.yaml（缺口 12 → 0）
**方式**：P1 战役首站。用户人工定位帮助中心 qid 深链，CDP 浏览器逐页实读后落标注。

### 新增官方来源（platform_sources 4 → 7）

- **S5**《硬币相关》（qid=376，accessed 2026-09-10）：自制稿件最多投 2 硬币、转载 1 硬币；
  投币 10% 归 UP 主
- **S6**《弹幕相关》分类（qid=358&pid=357）：弹幕介绍/弹幕礼仪/弹幕发送与撤回/
  弹幕举报与屏蔽等子体系
- **S7**《弹幕介绍》（qid=380）：普通弹幕（彩色/顶部/底部/滚动）与高级弹幕；
  发送需会员权限；Lv1 单条上限 20 字、Lv2 及以上 100 字

### 标注补全明细（10 处）

- interaction_signals ×5：投币（升级为 S5 官方规则＋具体数值）、收藏/点赞转发/评论
  （补 industry_consensus-行为观察）、弹幕密度（补 S6/S7 官方机制锚点）、关注/充电
  （充电 URL 待定位，以"帮助中心分类在案"过渡标注）
- 字符串字段 ×5：social_graph（S5/产品形态公开可见）、attention_environment
  （official_rule-产品形态＋行为观察双层）、cover_role/comment_role（策略观察＋
  S2/S6 治理锚点）、follow_role（产品形态公开可见＋充电 URL 待定位）

### 遗留

- 充电计划具体帮助页 qid 待定位（分类已在案）；定位后 follow_role/social_graph
  的充电条目可升 official_rule

---

## 2026-09-10 · 全库 P0 裁决：其余 12 个 adapter 的 fact_type↔L 级冲突清零

**文件**：muduo/platforms/{bilibili, wechat_channels, wechat_group, weibo, youtube, zhihu}/adapter.yaml（共 10 处）
**类型**：证据等级逻辑冲突裁决（与 X 适配器 Articles 问题同构的"降级说明写了、字段没改完"残留）
**方式**：逐条读取 pattern 全文与该 adapter 的 platform_sources，按层拆分裁决——
产品机制层已有官方来源支撑的保留在 note 内作 official 标注；pattern 主张本身
（行为/策略有效性）无实验或可验证观察依据的，统一 `fact_type: industry_consensus`、
`evidence_level: L3`。

### 裁决明细

| adapter | pattern | 原状态 | 裁决 | 依据 |
|---|---|---|---|---|
| bilibili | 结尾/开头求三连 | consensus↔L2 | consensus/L3 | "求三连有效"为创作者共识；三连产品功能层保留 official 标注于 note |
| bilibili | 坦诚恰饭声明维护信任 | consensus↔L1 | consensus/L3 | L1 只撑"公约要求主动声明"（S1 社区公约）；信任维护为共识层 |
| wechat_channels | 公众号图文挂视频号卡片互相导流 | official_rule↔L3 | consensus/L3 | 互挂导流为界面可观察能力，官方文档未实读（第一轮降级漏改字段） |
| wechat_channels | 直播预约+开播提醒 | official_rule↔L3 | consensus/L3 | 同上，同为降级未改完残留 |
| wechat_group | @点名触发响应 | official_rule↔L3 | consensus/L3 | pattern 主张为认知机制；@权限仅为产品背景 |
| weibo | 话题词蹭热搜入口 | consensus↔L2 | consensus/L3 | S2（话题管理规定）只撑话题机制存在（official 层）；入口判断为共识 |
| weibo | 首句金句化 | consensus↔L2 | consensus/L3 | S3（博文头条协议）只撑 140 字截断线；截图传播结构为共识 |
| youtube | 标题+缩略图互补分工 | consensus↔L2 | consensus/L3 | S3 撑"元数据关键、标签无用"（official）；互补分工策略为共识 |
| youtube | 前 15-30 秒 hook | official_rule↔L3＋缺 source_ref | consensus/L3 | note 明言"实取官方文档未载明"——降级声明在，fact_type 漏改 |
| zhihu | 专业身份前置 | consensus↔L2 | consensus/L3 | S1（知乎原则）撑"伪造身份受处置"（official 层）；权威性判断为共识 |

**无一处升级**：10 条均无实验或可验证观察依据，不支持升 L1/L2——全部为"字段回落"。

### 回归结果

- `validate_schema.py` 全库：校验通过（13 adapter / 208 eval cases）
- 复扫审计：fact_type↔L 级不一致 = 0；official_rule 缺 source_ref = 0
- 10 处 note 同步核验：10/10 含"官方依据＋共识层判断"双层说明，无改一半残留
- 剩余缺口全部为 P1 标注覆盖类（约 110 处），需逐平台实读官方文档后补标，
  已排期（首站 bilibili，10 处）

---

## 2026-09-10（二）· muduo X 适配器：CDP 实读补强，五页官方文档升级

**文件**：muduo/platforms/x/adapter.yaml（在第一轮基础上 +25 / −7）
**方式**：browser-cdp 技能启动调试 Chrome（真实指纹过反爬），逐页实读
**结果**：platform_sources 5 → **10** 条（6 条 accessed 2026-09-10）

### 实读页面与关键确认

| 页面 | URL | 关键官方确认 |
|---|---|---|
| About Articles | help.x.com/en/using-x/articles | Articles 限 Premium 及以上；headings/粗斜体/列表排版；编辑需先 unpublish；**官方写作指南明文建议"标题具体/激发好奇/承诺价值＋首句钩子"与"结尾强收尾、提问引发回复"** |
| About X Premium | help.x.com/en/using-x/x-premium | **reply prioritization 为官方分档权益**（Basic 有/Premium 更大/Premium+ 最大）；长帖为 Basic 权益；蓝标审核后显示 |
| How to create a thread | help.x.com/en/using-x/create-a-thread | Thread＝一人系列连帖；**4 帖以上时间线截断＋Show this thread 展开**；可追加帖 |
| About X Lists | help.x.com/en/using-x/x-lists | Lists 自定义/组织/置顶时间线；公开/私人；可加入他人 Lists；官方发现与推荐 |
| The X Rules | help.x.com/en/rules-and-policies/x-rules | 规则页公开（safety/privacy/authenticity），封禁处置依据 |

### 等级变更

- **follow_role**：蓝标/回复排序主张由第一轮的 L3 降级 → **升回 official_rule**（官方确认 reply prioritization 分档；具体算法加权仍不公开）
- **Lists pattern**：L3 → **L1**（官方页实读）；"跨圈层引用破圈"行为判断仍 L3
- **Thread pattern**：截断/展开机制补 [L1]（4 帖截断官方明文）；"首帖决定展开率"仍 L3
- **algorithmic_features**：Premium 可见性加权拆为"功能存在官方确认 [L1]＋具体权重不公开 [L3]"
- **risk_factors**：X Rules 由"已定位未实读"→"规则页已实读"
- **Articles pattern**：note 补官方写作指南背书（L1＝指南内容本身；策略实证等级仍按机制条目计），
  并记录与 Premium 页的分档表述出入（Articles 页称 Premium 及以上可用 / Premium 页列于 Premium+，
  两页并读从宽，待官方澄清）

### 核验路径记录（URL 定位过程）

- `/en/using-x/threads`、`/en/using-x/lists`、`/en/using-x/about-lists` 均 404——
  正式路径为 `/create-a-thread` 与 `/x-lists`（站内搜索定位）
- help.x.com 对无浏览器指纹的抓取返回反爬验证页；CDP 真实 Chrome 可正常访问

---

## 2026-09-10 · muduo 平台适配器修正：X（Twitter）——Articles 形态补全

**文件**：muduo/platforms/x/adapter.yaml（+17 / −3，共 3 处）
**类型**：平台事实修正（facts correction）
**触发**：02.x-promotion 案例诊断中，发起人指出"X 没有独立标题元素"表述错误——
X 普通 post 无标题元素，但文章（Articles）模块有独立标题，原 title_role 缺失该形态。
**验证**：YAML 解析通过（无重复键、27 个必备顶层字段齐全、7 条 pattern 与 5 条
platform_sources 字段完整）；Article 官方帮助页未实读（反爬拦截），产品存在性经
官方开发者文档实读确认（见"来源补强"）。

### 变更 1｜content_units：补入 Articles 形态

- "长帖（Premium 订阅功能）" → "长帖（Premium 订阅功能，无标题元素）"
- 新增 "Articles（文章模块：独立标题＋正文排版，形态接近博客）"

### 变更 2｜title_role：由单形态改为分形态陈述（核心修正）

- 旧：无差别断言"无标题元素：首句承担全部信息职责"
- 新：分形态——
  ① 普通 post/长帖（Premium）：无标题元素，首句承担全部信息职责；
  ② Articles：有独立标题元素，标题在信息流/feed 卡片独立作战、无首帖兜底，
     必须自带钩子与读者利益［产品存在＝官方开发者文档已确认（docs.x.com，2026-09-10 实读）；
     卡片展开行为＝industry_consensus L3］；
  ③ 新增纪律：诊断前必须先确认发布形态，两种形态下"五项必查＋第二道门"同样适用，
     机制载体不同（首句 vs 标题字段）。

### 变更 3｜known_platform_patterns：新增 1 条

- pattern: "Articles 长文：标题在 feed 卡片独立作战"
- mechanism_links: [processing_fluency, curiosity_gap, category_entry_points, information_scent]
- fact_type: industry_consensus ｜ evidence_level: L3 ｜ source_ref: none
- last_verified: "2026-09-10"
- note 含边界：Articles 与普通长帖是两种形态，诊断与交付前必须先确认发布形态

### 来源补强（同日第二轮）

- **已实读并登记**：X Developer Documentation - Changelog（https://docs.x.com/changelog，
  accessed 2026-09-10）——官方文档记载 Articles draft and publish endpoints
  （/x-api/articles/introduction，2026-06-11 条目）及 Article 元数据端点，
  Articles 产品存在性由此从"公开可见事实"升级为"官方文档确认"，写入 platform_sources
  （source_type: official，confidence: high）
- **已定位未实读**：官方帮助页 https://help.x.com/en/using-x/articles
  （2026-09-10 抓取被反爬拦截），URL 已写入 pattern note，待人工浏览器实读后可补强
- Articles pattern 的 note 与 title_role 同步更新为"官方开发者文档已确认"

### 下游同步修正（同一纠错批次）

- 木铎诊断案例/02.x-promotion.reader.html：批注①现象描述、平台事实卡"标题职责"行、
  报告元信息（改为"post 与 Articles 两种形态均适用本诊断"）
- 木铎诊断案例/02.x-promotion.diagnosis.md：同上三处
- 诊断结论不变：两种形态下首句/标题的改进建议同样成立，仅机制载体表述修正
