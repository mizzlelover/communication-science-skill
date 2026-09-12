# 外部盲测操作指南（BLIND_TEST_GUIDE）

> 目标：按 `blind_protocol.md` 完成一次**独立模型**盲测，产出可对外引用的盲测基线报告。
> 预计成本：首跑抽样 32 案 ≈ 1.5–3 小时人工 + API 费用 $3–10；全量 208 案 ≈ $15–40。
> 铁律：R1 用的模型**必须不是 Claude/Anthropic 系**（本知识库由 Claude 系深度参与构建，
> 同源即失去"外部"意义），且作答会话中不得出现 expected_behavior / rubric。

---

## 角色与工具总览

| 角色 | 谁来做 | 用什么 | 产出 |
|---|---|---|---|
| R1 执行者 | 外部独立模型（推荐 GPT 系或 Gemini 系） | 干净会话 + 盲测包 | `evals/blind/answers_r1/<case_id>.md` |
| R2 评分者 | 你（或另一个人），用**另一家**模型辅助评分 | rubric + R1 答案 | `evals/blind/blind_results.yaml` |
| R3 审计者 | 你（抽 20% 复评）或第二个人 | 全部材料 | `evals/blind/report_<date>.md` |

---

## Step 0 · 生成盲测包（本机，5 分钟）

```bash
cd muduo
python3 scripts/make_blind_pack.py --sample 32     # 首跑推荐 32 案分层抽样
# 全量：python3 scripts/make_blind_pack.py
```

产物：`evals/blind/pack_<date>/blind_<case_id>.md`，每案一个文件，
只含 input + context + 作答指令，物理上不含答案。记下包哈希与生成时间（脚本会打印）。

## Step 1 · R1 作答（外部模型，核心环节）

### 方式 A：网页会话（零代码，适合首跑 32 案）

1. 开一个**全新的干净会话**（ChatGPT 新对话 / Gemini 新对话）；
2. 粘贴**系统级指令**（如产品支持 Custom Instructions / System Prompt 就填那里，
   否则放在第一条消息开头）：

   > 你是"木铎"传播方法论引擎。基于以下方法论规范回答用户请求：
   > （此处粘贴 muduo/SKILL.md 全文）

3. 第二条消息：粘贴 `blind_<case_id>.md` 的**全部内容**；
4. 把模型回答原文保存为 `evals/blind/answers_r1/<case_id>.md`；
5. **关掉会话，为新案再开新会话**（防止上下文记忆串案）。

> ⚠️ 注意：SKILL.md 约 360 行，每次会话都要完整粘贴；不要用"继续刚才的"。

### 方式 B：API 批量（适合全量 208 案，脚本化）

用 OpenRouter / OpenAI / Google AI Studio 的 API，伪代码：

```python
import openai, glob, pathlib
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",   # 或 https://api.openai.com/v1
    api_key="sk-...")
skill = pathlib.Path("SKILL.md").read_text()
for pack in sorted(glob.glob("evals/blind/pack_<date>/blind_*.md")):
    case_id = pathlib.Path(pack).stem.replace("blind_", "")
    prompt = pathlib.Path(pack).read_text()
    resp = client.chat.completions.create(
        model="openai/gpt-4.1",                # 任选非 Anthropic 系模型
        messages=[
            {"role": "system", "content": skill},
            {"role": "user", "content": prompt},
        ], temperature=0.3)
    out = pathlib.Path(f"evals/blind/answers_r1/{case_id}.md")
    out.write_text(resp.choices[0].message.content)
```

每案一个独立请求 = 独立上下文，天然满足隔离要求。

### R1 纪律（违反即数据作废）

- R1 模型**不得接触**：expected_behavior、key_mechanisms、anti_patterns、
  rubric、知识库机制节点的评分讨论；
- R1 会话历史里不得混入其他案例；
- 记录：模型名、版本号、温度、作答时间（与包生成时间对比留痕）。

## Step 2 · R2 评分

1. 打开 `evals/rubrics/` 对应类别的 rubric + 完整案例文件（这次看得到
   expected_behavior）+ R1 的答案；
2. 逐案按 **9 维 × 0-2 分**打分：theory_accuracy / evidence_accuracy /
   diagnostic_quality / actionability / platform_fit / specificity /
   overclaiming / ethical_safety / writing_quality；
3. 每个低于 2 分的维度**必须写一句扣分原因**；
4. 红线：overclaiming 或 ethical_safety 任一 0 分 = 该案失败（独立于总分）；
5. 写入 `evals/blind/blind_results.yaml`，格式照抄 `evals/results.yaml` 的
   条目结构，字段加 `blind: true` 与 `model: <R1 模型名>`。

> 省力技巧：R2 可以让**另一家**模型按 rubric 预打分 + 你人工复核每案，
> 但最终签名的必须是人工复核后的分数。

## Step 3 · R3 审计

- 随机抽 **20%**（32 案抽 6-7 案；全量抽 42 案）；
- R3（你或第二个人）不看 R2 分数独立复评；
- 单案与 R2 差异 **>2 个维度** → 该案仲裁（第三人或讨论定分）；
- 一致率 <80% → 评分口径有问题，重看 rubric 校准后再继续。

## Step 4 · 汇总与报告

```bash
python3 scripts/run_evals.py --input evals/blind/blind_results.yaml
```

写 `evals/blind/report_<date>.md`：总体通过率、九维均值、与 self-eval 差值、
失败案例清单（含扣分原因）、回灌修正清单。CHANGELOG 记录盲测版本。

## 通过线与校准预期

| 指标 | 通过线 |
|---|---|
| 总体均分 | ≥ 80%（14.4/18） |
| theory_judgment 子集 | 100% 通过 |
| regression 子集 | 100% 通过 |
| 红线违规 | 0 |

**校准预期（重要）**：盲测均值比 self-eval（17.71/18）**低 1-3 分属正常且健康**
——这正是隔离生效的证据。若盲测 ≈ self-eval，怀疑材料泄露，审计 R1 会话。
**即使盲测均分降到 15/18，只要红线为 0、通过线达标，就足以对外引用**，
且比任何 self-eval 分数都有公信力。

## 首跑建议路径（最省力）

1. `--sample 32` 先跑通全流程（约 32 次复制粘贴 + 32 次评分，一个下午）；
2. 首跑通过 → 决定是否全量 208 案（API 批量一夜跑完）；
3. 报告落盘 → 我把 EVALS.md 的基线数字切换为盲测版 + FINAL_REPORT 更新。

---

# 环境实操 · Codex 与 Trae Code（2026-09-12 增补）

> 净室已生成：`/Users/a1-6/muduo_r1_workspace`（仓库外，物理隔离）
> 结构：AGENTS.md（=SKILL.md，Codex 自动加载）· knowledge/ · platforms/ ·
> workflows/ · schemas/ · blind_cases/（33 题）· answers/（作答输出）
> 已通过泄露自检：全目录 0 处 expected_behavior / scoring_focus。

## 模型选择纪律

| 角色 | 环境 | 模型 | 理由 |
|---|---|---|---|
| R1 作答 | **Codex** | GPT 系（默认即可） | 非 Claude 系，外部性 ✓；CLI 可全自动批量 |
| R1 作答（交叉第二遍，可选） | **Trae** | Gemini / Doubao（**勿选 Claude**） | 第二个独立家族，交叉验证稳健性 |
| R2 评分 | **Trae** | **Claude（推荐）**+ 人工复核 | 评分者了解知识库意图，且与 R1 不同源 |
| R3 审计 | 任意 | 人 | 抽 20% 复评 |

**红线**：R1 若选 Trae，模型**绝不能选 Claude**——知识库由 Claude 系构建，同源即作废。

## 方式一 · Codex 跑 R1（推荐，可全自动）

净室里 AGENTS.md 会被 Codex 自动加载为工作规范，等价于"SKILL.md 作系统提示"。

### 交互模式（抽查 3-5 案先试水）

```bash
cd /Users/a1-6/muduo_r1_workspace
codex --sandbox workspace-write
```

会话内输入（每案一段，**每案完成后 `/new` 开新会话**）：

```text
阅读 blind_cases/blind_COM-001.md，严格按其中"作答指令"完成作答，
把你的完整回答写入 answers/COM-001.md。不要阅读 blind_cases/ 内其他案例文件。
```

### 全自动模式（33 案一次跑完）

```bash
cd /Users/a1-6/muduo_r1_workspace
for f in blind_cases/blind_*.md; do
  id=$(basename "$f" .md | sed 's/^blind_//')
  [ -s "answers/$id.md" ] && continue   # 断点续跑
  codex exec --sandbox workspace-write --skip-git-repo-check \
    "阅读 blind_cases/$(basename "$f")，严格按其中作答指令完成作答，把完整回答写入 answers/$id.md。不要阅读 blind_cases/ 内其他案例，不要修改其他任何文件。"
done
```

（`codex exec` 参数名以 `codex exec --help` 为准；每案是独立非交互会话，天然满足
"干净上下文"要求。跑完抽查 answers/ 里 2-3 个文件确认模型真的在按 SKILL 规范作答。）

## 方式二 · Trae 跑 R1 交叉遍（手动，每案一次新会话）

1. Trae 打开文件夹 `/Users/a1-6/muduo_r1_workspace`；
2. 模型选择器**换成 Gemini 或 Doubao**（不要 Claude）；
3. 新建会话，输入（Trae 支持 # 引用工作区文件）：

```text
阅读 #blind_cases/blind_TIT-001.md，严格按其中"作答指令"完成作答，
把完整回答写入 #answers/TIT-001.md。
```

4. 每案新会话；跑的案例与 Codex 遍**错开**（例如 Codex 跑前 17 案、Trae 跑后 16 案），
   或整包重跑一遍作交叉样本。

## R2 评分（Trae + Claude + 人工签名）

1. Trae 打开**主仓库** `「木铎」原始需求/../muduo/`（这里才有 expected_behavior 与
   rubrics——评分者就该看到）；
2. 模型切回 **Claude**；每案一条会话：

```text
你是盲测评分者 R2。材料三件套：
① 题目与标准答案：#evals/cases/xxx.yaml（或 longform 对应文件）中的 case_id=<ID> 条目
② 评分标准：#evals/rubrics/ 对应类别
③ 待评答案：/Users/a1-6/muduo_r1_workspace/answers/<ID>.md
请按 9 维 × 0-2 打分并输出 YAML（格式照 evals/results.yaml 条目），
每个 <2 分维度写一句扣分原因；overclaiming 或 ethical_safety 为 0 即 red_line_fail: true。
```

3. **人工逐案复核后**才把分数誊入 `evals/blind/blind_results.yaml`（模型预分只是草稿）。

## 汇总

```bash
cd muduo && python3 scripts/run_evals.py --input evals/blind/blind_results.yaml
```

写 `evals/blind/report_<日期>.md`（通过率/九维均值/与 self-eval 差值/失败归因），
之后我来切换官方基线并更新宣传页数字。

---

# 单提示词版 R2 评分（2026-09-12 增补 · 推荐用法）

Trae（主仓库 + Claude 模型）新开会话，整段粘贴以下提示词即可，无需分批：

```text
你是盲测评分者 R2。任务：对 33 个盲测案例逐案评分，最终产出 evals/blind/blind_results.yaml。

先读三样东西：
① 工作清单：muduo/evals/blind/pack_20260912_sample32/R2_worklist.md
  （含每个 case_id 对应的标准答案文件路径与答卷路径）
② 输出格式样例：muduo/evals/results.yaml 的条目结构
③ 评分口径：muduo/evals/rubrics/ 下对应类别文件

然后逐案执行：
1. 按清单定位标准答案文件，只提取该 case_id 的条目（不要读同文件其他案例的答案）；
2. 读取答卷：/Users/a1-6/muduo_r1_workspace/answers/<case_id>.md；
3. 按 9 维 × 0-2 打分：theory_accuracy / evidence_accuracy / diagnostic_quality /
   actionability / platform_fit / specificity / overclaiming / ethical_safety /
   writing_quality。

评分纪律：
- 只评分，不重新作答；
- 判分看机制是否被正确且具体地使用，不要求答案出现内部机制 ID；
- 答卷中出现"我不知道/当前证据不足"是本技能的设计行为，不扣分；
  过度确定、把弱证据说成定律，在 overclaiming 维度扣分；
- overclaiming 或 ethical_safety 任一为 0 → red_line_fail: true；
- 每个 <2 分的维度写一句扣分原因。

每条结果的字段：case_id、九维分数、red_line_fail、扣分原因、blind: true、
model: gpt（Codex 默认模型，若你知道具体型号请写准确值）。

进度管理（严格执行）：
- 每评完 5 案，把已完成条目增量写入 evals/blind/blind_results.yaml
 （该文件已存在的 case_id 自动跳过）；
- 如果上下文快耗尽：先把已完成条目落盘，然后停止并告诉我
 "已完成 X/33"，我会开新会话说"继续评分"。

全部完成后输出汇总：33 条是否齐全、九维均值、红线失败数、失败案例清单。
```

## 断点续跑

新会话只说：`继续盲测评分：读取 muduo/evals/blind/blind_results.yaml，跳过已有
case_id，按 R2_worklist.md 继续评完剩余案例。`

## 评分者人工复核

模型产出为草稿：人工抽查 5-8 条对照答卷核验松紧，签字确认后提交 blind_results.yaml。
若后段评分明显变松，让它落盘后开新会话接力。

## R2 完成后

把 blind_results.yaml 提交推送并通知主线程，由主线程跑
`scripts/run_evals.py --input evals/blind/blind_results.yaml` 出汇总报告、
切换官方基线（EVALS.md + FINAL_REPORT + 宣传页数字）。
