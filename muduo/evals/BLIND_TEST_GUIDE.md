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
