# FINAL_REPORT — 木铎 MUDUO · 人类传播与社群增长引擎

- **报告日期**：2026-09-11
- **版本**：v1.0（任务书 §51 首次交付）
- **数据基准声明**：本报告全部数字由 `muduo/scripts/` 下脚本于 2026-09-11 实测生成
  （validate_schema / audit_integrity / generate_report / build_graph / 评测 results.yaml），
  未使用记忆值，未做估算；凡脚本未覆盖的陈述均注明"以文件为准"。

---

## 1. Project Overview

本项目按《项目总任务书》（「木铎」原始需求/writing-block.md）及其增量补丁
（长篇文章优化能力增量构建提示词.md）建成一套可被 AI Agent 实际调用的
**AI 时代社群营销与内容传播方法论系统**。

它回答的不是"怎么写爆款"，而是：**什么样的信息，在什么样的人、心理状态、
社会关系、媒介环境和平台机制下，会以什么方式改变注意、理解、记忆、判断、
表达、传播和行动**——并把答案转化为带证据等级与适用边界的可操作传播建议。

**总规模（实测）**：

| 维度 | 实测值 |
|---|---|
| 机制节点 | 216（32 个领域文件，全部有 provenance） |
| 机制关系边 | 1,200（独立引用对 888，平均度 11.1，全图连通） |
| 来源库 | 233（100 本种子文献全部入库；含 2026-09-11 两轮一手实读新建包 23 条：学术 OA 论文 17＋官方文档 6，全部实读） |
| 实践案例 | 354（无材料缺失 0，单案例泛化风险 0） |
| 反模式 | 29（主库 10 + 长文专项 19） |
| 理论冲突条目 | 6（情境化裁决，不强行二选一） |
| 平台适配器 | 13（generic + 12 平台） |
| 工作流 | 11（基础 6 + 长文 5） |
| Schema | 8 |
| 自动化脚本 | 17（任务书 §48 要求的 8 个全部在库） |
| 评测用例 | 208 |
| 文档 | README / ARCHITECTURE / METHODOLOGY / EVIDENCE / PLATFORM_ADAPTER / EVALS / CONTRIBUTING / INDEX / CHANGELOG / 本报告 |

**验收状态**：validate_schema 全部数据文件结构合法；audit_integrity 显示
无引用 0、边界不全 0、平台事实无证据级别 0、适配器来源登记 13/13；
12 个真实平台的标注缺口已全部清零（2026-09-11，本轮清零最后 16 处）。

## 2. Architecture

按任务书强制的四层结构实现，未反向绑定任何单一平台：

```text
Human Mechanism Core            人的底层机制（认知/情绪/动机/身份…）
        ↓
Communication Mechanism Layer   传播机制（说服/叙事/扩散/网络…）
        ↓
Platform Adapter                平台适配层（13 个 adapter，平台事实不进核心）
        ↓
Application Workflow            实践引擎（11 个工作流）
```

- **核心与传播层**：`knowledge/mechanisms/` 32 个领域文件，统一
  Knowledge Node Schema（定义/机制/因果链/变量/证据/边界/失效条件/误读/伦理风险/应用映射）。
- **平台适配层**：`platforms/` 每个适配器 20+ 字段，平台事实四级区分
  （official_rule＝官方规则实读 / verified_observation＝可验证观察 /
  industry_consensus＝行业共识 / experience_speculation＝经验推测），
  全部带 `last_updated`（2026-09）与来源登记；`update_platform_knowledge`
  更新流程引用已全库闭环（13/13，本轮实测）。
- **实践引擎**：SKILL.md 负责任务判定与 progressive disclosure 按需加载，
  工作流先诊断后改写（Diagnosis before Rewrite）。
- **伦理层落地**（任务书 §29）：评测设 ethical_safety 维度（实跑红线违规 0）、
  29 条反模式库（伪稀缺/标题党/虚假社会证明等）、E 级证据默认不得作为强建议依据。
- **自动化**：17 个脚本覆盖校验/去重/缺源检测/未引用断言检测/索引/图构建/
  评测/报告及完整性审计、盲测打包、长文状态校验等。

## 3. Knowledge Domains

**32 个一级领域文件 = 任务书 §9 建议的 30 个域全部覆盖 + 2 个增设域**
（comprehension 理解、ai_information_environment AI 信息环境——后者为
任务书 §23 单独要求的 AI 时代模块，含 12 个节点）。

实测节点分布（generate_report，合计 216）：

| 领域 | 节点 | 领域 | 节点 |
|---|---|---|---|
| ai_information_environment | 12 | cognitive_load | 6 |
| persuasion | 11 | emotion | 6 |
| platform_algorithmic | 11 | identity | 6 |
| community | 10 | perception | 6 |
| diffusion | 10 | trust | 6 |
| behavioral_economics | 9 | habit | 5 |
| brand_consumer | 9 | narrative | 5 |
| memory | 9 | prediction_surprise | 5 |
| network_effects | 9 | processing_fluency | 5 |
| comprehension | 8 | reward | 5 |
| decision_making | 8 | social_norms | 5 |
| attention | 7 | attitude_change | 4 |
| language_rhetoric | 7 | belonging | 4 |
| motivation | 7 | framing | 4 |
| social_proof | 7 | social_comparison | 4 |
| authority | 3 | complex_contagion | 3 |

## 4. Mechanism Count

- **216 个机制节点**（任务书目标 150–300 ✓），32 文件组织，不保留"书籍孤岛"。
- **关系边 1,200**（独立对 888），平均度 11.1，**连通分量 1**（全图连通，
  无孤立知识岛；build_graph 实测）。
- 枢纽节点（度数 Top 3）：processing_fluency 处理流畅性（25）、
  source_credibility_model 信源可信度模型（25）、psychological_reactance 心理逆反（23）。
- 长文补丁 §36 要求的机制节点实测在库：working_memory_limits（工作记忆限制）、
  chunking（组块化）、information_foraging（信息觅食）、information_scent（信息气味）、
  cognitive_fatigue（认知疲劳）、schema_formation（图式形成）、conceptual_coherence
  （概念一致性）、serial_position_effect（序列位置效应）、retrieval_cue_design
  （提取线索设计）、argumentation_structure（论证结构）、elaboration_likelihood_model
  （详尽可能性模型）、testing_effect（测试效应）。

## 5. Source Coverage

- **来源登记 233 条**（source_registry.yaml），其中 **232 条被机制节点实际引用**
  （generate_report 实测），无引用断言 0（detect_uncited_claims / audit_integrity）。
  2026-09-11 两轮一手实读新建包 23 条（S215–S237）：学术 17 篇逐字实读
  （Matz 2017 PNAS / Doshi & Hauser 2024 / Itti & Baldi 2009 / Wagemans 2012 /
  Bezdek 2015 / Páez 2015 JPSP / Halfaker 2013 / Aggarwal 2024 KDD / Aral & Walker
  2011 / Brynjolfsson et al. 2011 / Kim et al. 2025 第三空间 / Restivo & van de Rijt
  2012 / Zhang 2024 / Li et al. 2026 AJM / Reynaert & Sallee 2016 NBER /
  Mittal et al. 2026 等）＋官方 6 份（TikTok Newsroom、YouTube 官方博客、X Rules、
  bilibili 创作激励页、小红书社区规范、抖音自律公约——本项目已实读入册）。
- **100 本种子文献（S01–S100）全部入 Registry**（任务书 §50 验收项 ✓），
  并按 §43 蒸馏规则做跨来源合并而非逐书摘要。
- 证据包文件 237 个（含 4 个 MERGED_INTO 墓碑，用于合并溯源；validate_schema 实测）。
- 来源类型覆盖书籍/原始论文/meta-analysis/系统综述/官方文档等；平台侧官方来源
  实测示例：X 官方帮助与规则 10 条（S1–S10，2026-09-08/10 实读）、bilibili 帮助中心 7 条、
  YouTube 官方博客与帮助 4 条、知乎 3 条、小红书 3 条、抖音 3 条、TikTok Newsroom 2 条
  （其余 5 个适配器均已登记来源 13/13，条数以各文件为准）。
- 全部节点有 provenance；其中 10 个节点标注为 MEMORY_BASED 类型（如实保留）。

## 6. Evidence Distribution

实测证据等级分布（generate_report，216 节点）：

| 等级 | A | A- | B+ | B | B- | C | D | E |
|---|---|---|---|---|---|---|---|---|
| 节点数 | 28 | 41 | 28 | 80 | 0 | 33 | 5 | 1 |

- **A·B 级合计 82%**；任务书 §8 规则执行：输出建议优先调用 A/B/C，
  D（5 个）明确标记为实践经验，E（1 个）被隔离、默认不作为强建议依据。
- **Research Gates（按等级分域门槛）：A=97%，B=C=D=100%**（audit_integrity 实测；
  2026-09-11 三轮补强后由 83%→86%→94%→97%）。audit 一手口径说明：
  official_source 计入一手（任务书 §6 来源类型含官方来源；平台机制节点的最强一手
  即官方文档，且 6 份官方来源均为本项目实读、EP 记录实读方式）。
- 如实保留的审计提示：6 个节点暂无一手实证标注（37→30→14→6，三轮共补强 31）、
  1 个节点无反例记录（见 §10 Known Limitations——不粉饰）。
- 证据分布随 3 处有据升级变化：D 8→5、C 30→33
  （suspense_structure D→C：Bezdek fMRI 实验直接支撑；answer_engine_visibility
  D→C：Aggarwal KDD 受控基准实验支撑；viral_coefficient D→C：Aral & Walker
  随机现场实验支撑）；A·B 级占比保持 82%
  （其余升级须"多个独立研究"，不虚升）。
- 平台事实层：77 条平台断言全部带证据级别标注，无虚标 official_rule
  （本轮复核中再次将无官方文档支撑的条目降级并注明）。
- 经典理论复核机制在库（任务书 §26）：knowledge/evidence/classic_rechecks/
  rechecks_registry.yaml；冲突处理（§25）在库 6 条，按情境裁决输出
  "X 情境更支持 A / Y 情境更支持 B"。

## 7. Platform Adapters

- **13/13 全部在库**：generic（兜底模板）+ 任务书 §13 点名的 12 个平台
  （公众号/朋友圈/微信群/小红书/抖音/视频号/bilibili/知乎/微博/TikTok/YouTube/X）。
- **时效化**（任务书 §14）：全部 last_updated=2026-09；官方来源实取访问日期在案；
  update_platform_knowledge 更新流程引用 **13/13 闭环**（2026-09-11 实测，本轮补齐
  x/tiktok/youtube 三处）。
- **标注缺口清零**：12 个真实平台的全部事实字段与互动信号条目均带证据级别
  （2026-09-11 p1_audit 实测 0 缺口；generic 模板 23 处为设计性保留，
  新平台接入时按流程补标）。
- 每个适配器包含：内容形态、用户意图、分发与推荐模型、社交图、内容生命周期、
  入口、注意环境、行为、互动信号、分享/搜索/社群机制、算法特性、内容约束、
  标题/封面/开场/标签/评论/关注六角色、风险因子、平台模式库（含机制链接与
  L1–L4 证据级别）、来源清单。
- X 适配器支持 Articles（独立标题形态）与普通帖（无标题形态）的分形态诊断，
  标题职责按发布形态区分（2026-09-10 官方文档实读确认）。

## 8. Workflows

**11 个工作流 = 基础 6（任务书 §30）+ 长文 5（补丁 §3）**，全部在库：

- 基础：analyze_content（内容分析）/ improve_title（标题优化）/
  rewrite_content（改写）/ community_diagnosis（社群诊断）/
  campaign_design（活动设计）/ postmortem（传播复盘）——
  对应任务书 §15 的四类输入（内容分析/内容生成/社群诊断/传播复盘）与 §33 工作模式。
- 长文：longform_article_analysis / longform_article_optimization /
  longform_restructure / longform_evidence_audit / longform_line_edit——
  落实补丁的 Macro before Micro、两遍优化（先结构后句子）、Delete before Rewrite。
- 长文配套（补丁 §47）：schema 3 个（longform_article / argument_map /
  concept_registry）、knowledge/longform/ 专题 5 篇（认知负荷/信息密度/叙事线/
  语义冗余/读者旅程）、longform_state.example.yaml 跨轮编辑状态文件 +
  verify_longform_state.py 校验脚本。

## 9. Evaluation Results

**208 例评测（任务书要求 ≥100 ✓）**，构成实测如下：

| 模块 | 数量 | 对照要求 |
|---|---|---|
| 基线七类 | 100 | 任务书 §35 配额逐一对应：标题 20 / 长文 15 / 短视频 15 / 社群 15 / 平台适配 15 / 复盘 10 / 理论判断 10 |
| 长文子类 | 50 | 补丁 §40 要求 ≥50 精确达标：公众号 10 / 行业研究 10 / 管理咨询 10 / 方法论 5 / 教育 5 / 品牌 5 / AI 5 |
| 对抗评测 E2 | 48（6 类 × 8） | 任务书 §37：错误前提反驳/缺陷推理/过度断言/平台幻觉/短长对比/理论贴标签 |
| 回归测试 | 10 | 任务书 §38 |

**实跑结果（results.yaml，208/208 全量逐案留痕；E2 48 例于 2026-09-11 补齐）**：

- 评分维度 9 个＝任务书 §36 要求的九维（理论准确/证据准确/诊断质量/可操作性/
  平台适配/具体性/过度断言/伦理安全/写作质量），2 分制。
- 实测均分（208）：theory_accuracy 2.00 · overclaiming 2.00 · ethical_safety 2.00 ·
  writing_quality 2.00 · diagnostic_quality 1.99 · specificity 1.98 ·
  actionability 1.97 · evidence_accuracy 1.96 · platform_fit 1.88。
- **E2 对抗 48 例逐案实跑**：run_evals.py 汇总 208/208 通过（100%），E2 子集
  均分 17.73/18，逐案作答摘要＋九维评分＋实跑短点已落盘 results.yaml；
  诚实扣分点集中在平台适配层（generic 场景未接 adapter 字段）与替代方案具体度。
- **红线违规 0**。
- **性质声明（诚实）**：本轮 E2 实跑为 self-eval（同一模型既作答又评分，符合
  blind_protocol.md §1 的冒烟测试定位），**不得称为盲测基线**；独立模型路线的
  第三方盲测仍待执行（见 §10 第 2 条）。
- 盲测协议（blind_protocol.md）与盲测打包脚本（make_blind_pack.py）在库。

## 10. Known Limitations

如实列出，不含糊：

1. ~~E2 对抗评测 48 例无逐案实跑留痕~~ **已解决（2026-09-11）**：48 例逐案实跑已
   落盘 results.yaml（作答摘要＋九维评分＋实跑短点；run_evals.py 汇总 208/208
   通过、E2 均分 17.73/18、红线 0）。注意：属 self-eval 冒烟级留痕，
   独立模型盲测（下条）仍待执行。
2. **外部盲测未留执行结果**：协议与工具在库（blind_protocol.md /
   make_blind_pack.py），独立模型路线的盲测报告未见落盘。
3. **6 个节点暂无一手实证标注、1 个节点无反例记录**（audit_integrity 如实报告）。
   三轮补强 31 个（37→30→14→6）：第一轮现有语料挂链 7 个；第二轮新建包 15 条
   （S215–S229）覆盖 16 个节点；第三轮新建包 8 条（S230–S237）覆盖 8 个节点
   （病毒系数←Aral & Walker 2011；长尾←Brynjolfsson 2011；第三空间←Kim 2025；
   地位系统←Restivo & van de Rijt 2012；AI 内容饱和←Zhang 2024；感知购买风险←
   Li 2026 AJM；算法博弈←Reynaert & Sallee Goodhart 定律 NBER；AI 信息中介←
   Mittal 2026——全部逐字实读）。剩余 6 个（独特品牌资产/定位机制/任务达成/
   许可机制/集体身份叙事/鸿沟跨越）为**书源原生概念节点**：其奠基文献即从业者
   专著且已在库（S73–S79、S86、S91 等）——按 paper 型一手口径结构性无法满足，
   属口径边界而非证据缺陷；强行以弱相关论文挂链即凑数，已拒绝。
   **防误读声明**：这 6 个节点的引用链本身完整（2026-09-11 三方对账实测：
   奠基专著均已登记于 source_registry 并被节点 source_ids 引用，types=['book']）；
   audit 的"无一手"仅指缺少 paper/official **类型**来源，不代表引用缺失或主张无据。
4. **10 个节点 provenance 类型为 MEMORY_BASED**（保留标注，待补外部来源）。
5. **平台算法权重黑箱是精度天花板**：各平台推荐权重官方不公开，
   权重类断言全部停在行业共识/经验推测级，任何具体分值均不可引用——
   这是方法论约束，也意味着平台适配层不可能给出"精确权重"。
6. **中文平台官方文档可得性有限**：抖音/小红书部分"产品存在"类条目
   实取未获官方文档，已如实降级为 L3 并注明（降级机制正常运作的记录）。
7. **遗留小项**：bilibili 充电计划帮助页 qid 待定位（CHANGELOG 在案）；
   X 官方两页对 Articles 可用档位表述有出入（S6/S7 并读从宽，待官方澄清）。
8. **本报告（§51 交付物）生成于 2026-09-11**，在此之前缺失——如实记录。
9. **外部盲测未执行**：本轮 208 例评测为 self-eval 冒烟级，对外表述禁止引用其
   分数作为质量证明；操作指南已就绪（evals/BLIND_TEST_GUIDE.md）。
10. **跨文化调节变量结构化覆盖仍薄**：culture_moderators 显式提取 11/216 节点；
    多数社会心理机制的中国/东亚直接样本证据待补强（research_log 已列方向）。

## 11. Future Research

1. **一手实证补强**：优先任务书 §26 点名的高危经典区
   （priming / ego depletion / power posing / social contagion / scarcity /
   nudging / loss aversion / social proof / framing / choice overload /
   mere exposure / emotional contagion），在 classic_rechecks 基础上逐节点补
   Current Best Evidence 与反例。
2. **盲测执行**：E2 48 例已逐案落盘（self-eval 级，2026-09-11）；
   T7 外部盲测走独立模型路线出报告。
3. **平台规则时效化**：按 update_platform_knowledge 周期复核 13 个适配器，
   重点盯分档/限额/时长类易变规则（如 X Premium 档位、各平台字数上限）。
4. **AI 信息环境域扩容**：ai_search / zero-click / 合成社会证明等 12 节点
   基础上，跟进 AI 搜索与生成内容治理的官方规则演化。
5. **冲突库与失败案例扩容**：现冲突 6 条、案例 354 条；提高 failure_case
   占比以强化"案例不作因果证据"的纪律。
6. **新平台接入**：generic 模板 + 全字段标注流程已就绪，可低成本扩展。

## 12. Recommended Next Iteration

1. ~~补齐 E2 48 例实跑留痕~~ 已完成（2026-09-11，208/208 全量落盘，self-eval 级）；
   下一步转为盲测执行（第 2 条）。
2. 执行 T7 外部盲测（独立模型路线），产出盲测报告并归档。
3. ~~对 37 个无一手实证节点按域分批补强~~ 大幅完成（2026-09-11 三轮）：
   37→30→14→6，一手证据覆盖率 Gate A 83%→97%；3 处有据升级（悬念结构、答案引擎
   可见性、病毒系数 D→C）。剩余 6 个为书源原生概念节点（定位/JTBD/许可/鸿沟/
   品牌资产/集体身份叙事），奠基专著已在库——消除其"无一手"标注需要口径决策
   （是否承认书源为实践概念的一手）或人工获取付费论文，不自动凑数。
4. 启动 update_platform_knowledge 第一轮全库定期复核（引用已 13/13 闭环）。
5. 用真实诊断案例持续回流 evals/real_cases/（已有先例），保持评测与实战一致。
6. 版本化发布 v1.x，CHANGELOG 持续留痕（发布纪律：显式路径 add、仓库单提交历史）。

## 13. 任务书 §99 十五问逐条回答（2026-09-11）

1. **多少节点来自实际读取的原始研究？** 216/216 有 provenance 溯源链；一手
   （paper/official）覆盖 Gate A 97%（210/216），一手来源含 2026-09 两轮逐字实读
   的 23 个新建包（S215–S237）。
2. **多少节点只有实践经验支持？** D 级 5 节点（显式"实践经验"标注）；10 节点
   来源类型为 MEMORY_BASED（逐条在案）；二者与 A/B/C 级严格隔离。
3. **哪些经典理论近年明显修正？** ego depletion / power posing / 行为层语义启动
   → E 隔离；loss aversion A→B；nudge → C；choice overload 条件化；8 秒/金鱼
   注意力谣言拒绝（classic_rechecks 全记录）。
4. **哪些理论跨文化证据不足？** authority / social norms / community
   participation 的中国/东亚直接样本仍薄；culture_moderators 显式提取 11/216
   节点，其余以 boundary_conditions 文字承载——如实标注待补。
5. **哪些平台规则来自官方？** X 帮助与规则 10 条、bilibili 7 条、YouTube 4 条、
   知乎 3 条、小红书 3 条、抖音 3 条、TikTok 2 条官方来源实读入册（S-ID 可溯）。
6. **哪些只是行业观察？** L3 行业共识为平台断言主体（77 条断言的分级分布见
   audits/PLATFORM_FRESHNESS_AUDIT.md）。
7. **哪些平台知识已过期？** 0 条（77 断言全部 last_verified 2026-09；
   detect_stale_platform_claims 实测 0 命中）；分档/限额类列入周期复核。
8. **真实案例库成功/失败数量？** 354 案例：failure 100、community 100、
   platform 50、brand 30、content 30、growth 20、crisis 20、benchmark 8、
   research 2、campaign 2。
9. **是否存在单案例过度泛化？** audit_integrity 实测风险 0；升级
   Contextual Practice Pattern 需 ≥3 独立案例（§19 纪律入库）。
10. **是否真正区分相关与因果？** 案例层 causal_status 354/354（experimental/
    observational…分级）；E2 causal_reasoning 8 例实跑；复盘工作流含反事实检验。
11. **是否区分六目标？** 16 层行为链 + 六目标分离 + VCB 四象限真实基准 8 案例。
12. **AI 结论是否够新？** AI 域 12 节点全部 valid_as_of=2026-09；来源含 Doshi &
    Hauser 2024、Zhang 2024、Aggarwal 2024 KDD、Li 2026、Mittal 2026 等。
13. **高置信推荐能否回溯证据？** Recommendation → Mechanism → provenance →
    S-ID → evidence_packages 链路在库可走通；第三方复核=盲测待执行。
14. **哪些知识仍有争议？** conflicts 6 条按情境裁决；loss aversion / scarcity /
    nudge 修正状态入 EVIDENCE.md 复核清单。
15. **哪些应回答"不知道"？** 平台具体推荐权重（黑箱）；bilibili 充电计划 qid；
    X Articles 档位出入；中国样本直接实证薄的跨文化外推；6 个书源原生节点的
    paper 级一手——以上 Skill 均应输出"当前没有足够证据/需最新验证"。

## 14. 第二轮补丁合规修复（2026-09-11，本轮）

- 8 份命名审计文档物化（scripts/generate_audit_docs.py，数据驱动可重跑）；
- 来源状态机推进：232/233 → validated（条件化，1 条 hold 如实标注）；
- research_log/ 目录建立（README + 2026-09 条目）；
- 节点 schema 升级：knowledge_half_life 216/216、valid_as_of 12、
  culture_moderators 11、provenance.conflicting_evidence 15 / case_sources 128 /
  platform_sources 67；
- 社群案例 lifecycle 100/100（§32；99 条有材料覆盖）；
- detect_stale_platform_claims.py 时效检测工具（77 断言 0 过期）；
- evals/MATERIAL_TRACEABILITY.md：真实材料关联 158/208 = 76%（≥60% ✓），
  50 长文例显式标注 synthetic_scenario。
- 回归：validate_schema ✓ / audit_integrity 无退化 / build_graph 连通 ✓。

---

*报告生成：2026-09-11。数据来源脚本：validate_schema.py / audit_integrity.py /
generate_report.py / build_graph.py / 临时缺口审计（p1_audit）/ evals/results.yaml。
本报告自身即任务书 §51 的交付物。*
