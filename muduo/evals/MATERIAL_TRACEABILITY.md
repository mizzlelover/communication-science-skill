# 评测真实材料追溯报告（补丁 §54）

> 生成：2026-09-11 · 覆盖 208 例评测

## 结论

**真实材料关联 158/208 = 76.0% ≥ 60% 要求 ✓**

| 类别 | 例数 | material_ref | 说明 |
|---|---|---|---|
| 基线七类（标题/社群/短视频/平台适配/复盘/理论判断/长文） | 100 | 100（100%） | 每例指向案例语料 CASE-*、内容样本 XHS-* 或来源 S-* |
| 长文子类 50 | 50 | 0（显式 synthetic_scenario） | 基于真实诊断经验编写的场景模拟，结构化字段与演示数据标注"演示" |
| 对抗评测 E2 六类 | 48 | 48（100%） | 指向机制节点锚点、平台 adapter 来源、案例语料 |
| 回归测试 | 10 | 10（100%） | 指向历史基线案例 |

## 引用格式

`material_ref` 支持四种可解析形态：
1. **案例语料 ID**：`CASE-COM-002` → `knowledge/cases/cases.yaml`
2. **内容样本 ID**：`XHS-B-LOW-005` → `knowledge/cases/content_corpus.yaml`
3. **来源 ID**：`S158` → `knowledge/sources/source_registry.yaml`
4. **URL / 文件锚点**：报道原文链接、`knowledge/mechanisms/...#节点id`、
   `platforms/.../adapter.yaml#platform_sources`、多引用用 `;` 分隔

## 幸存者偏差防护（§28）

内容语料 500 样本按表现分层：high 120 / medium 135 / low 125 / failed 120——
非只采爆款。

## 待办

- 50 长文合成场景若后续基于真实文章改写，补挂 material_ref 并移除
  synthetic_scenario 标注。
