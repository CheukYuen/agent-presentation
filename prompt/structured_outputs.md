# Structured Outputs（结构化输出）基础教程

## 学习目标 ⭐
* 理解 Structured Output 的定义与优势
* 掌握在 Prompt 中引导 Claude 生成 JSON / YAML 等结构化数据的技巧
* 能够在资讯摘要与交易趋势场景中设计高质量结构化输出
* 熟练使用 Claude API（流式模式）获取结构化结果并进行后续处理

> **预计耗时**：约 15 分钟

---

## 1. 前言（2 分钟）
在银行业务实践中，我们常需要将大模型输出直接交由后端系统解析并进入风控、合规或报表流程。与自然语言相比，**结构化输出（Structured Output）**更易于机器读取和后续自动化处理，因此成为 Prompt 工程的重要补充模块。

---

## 2. 核心概念（4 分钟）
1. **定义**：通过精心设计的 Prompt，让大模型直接输出符合 JSON / YAML / CSV 等格式规范的文本，避免后续正则解析。
2. **优势**：
   * 易解析、少歧义 → 提升自动化程度
   * 方便风控校验 → 提高合规性
   * 与前端 / 后端系统快速集成 → 降低工程复杂度
3. **Claude 支持**：
   * `"output": "json"` 风格提示词
   * `system` / `user` 多角色配合
4. **TACOS 框架补充**：在 **Output** 维度中明确指定格式与字段，示例：`"请以合法 JSON 格式输出，不要添加多余文本"`。

---

## 3. Prompt 设计模式（4 分钟）
| 场景 | 要求 | Prompt 关键片段 |
| --- | --- | --- |
| 财经新闻摘要 | 摘要要点 & 情感极性 | `键名: title, summary, sentiment` |
| 交易趋势分析 | 技术指标 & 风险评级 | `键名: symbol, trend, indicators, risk_level` |

> **提示**：尽量提供 **示例输出（Few-Shot）** 帮助模型对齐字段顺序和数据类型。

---

## 4. 实践示例（示范代码 + 流式输出）⭐（5 分钟）

以下示例演示如何调用 Claude，要求模型输出符合 JSON Schema 的结果，并使用**流式**打印。请确保已在环境变量中配置 `ANTHROPIC_API_KEY`。

```python
# 安装依赖（如首次运行）
%pip install anthropic python-dotenv httpx --quiet
```

```python
import os, httpx, json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    http_client=httpx.Client(proxy="http://127.0.0.1:7890/")
)

def stream_claude(prompt, system="", max_tokens=1024):
    full = ""
    with client.messages.stream(
        model="claude-4-sonnet-20250514",
        max_tokens=max_tokens,
        temperature=0,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    ) as s:
        for chunk in s.text_stream:
            print(chunk, end="", flush=True)
            full += chunk
    print()
    return full
```

### 4.1 资讯摘要结构化输出
```python
news_article = """央行今日发布2024年第四季度货币政策执行报告，报告显示人民币汇率保持基本稳定…"""

prompt = f"""
你是一名金融分析助手。请从下列财经新闻中提取关键信息，并按 JSON 格式输出，字段包括：\n
- title (string)\n- summary (string, 不超过 40 字)\n- sentiment (string, 取值: positive | neutral | negative)\n- publish_time (string: YYYY-MM-DD HH:MM:SS)\n
严格要求：\n1. 仅输出合法 JSON，不要添加解释或注释；\n2. 字段顺序与示例一致；\n3. 中文内容；\n
示例：\n{{\n  \"title\": \"示例标题\",\n  \"summary\": \"示例摘要\",\n  \"sentiment\": \"neutral\",\n  \"publish_time\": \"2024-01-01 10:00:00\"\n}}\n\n正文：\n{news_article}
"""

json_str = stream_claude(prompt)
result = json.loads(json_str)
print("解析后的 Python 对象:", result)
```

> **合规提示**：结果仅供参考，不构成投资建议。

### 4.2 交易趋势结构化输出
```python
price_data = [15.20, 15.35, 15.18, 15.42, 15.38]

prompt = f"""
作为资深量化分析师，请根据以下股价序列 {price_data} 生成趋势分析报告，并以 JSON 格式返回：\n
- symbol: string\n- trend: string (upward | downward | volatile)\n- indicators: object {{\n    ma5: float,\n    rsi: float\n  }}\n- risk_level: string (low | medium | high)\n
返回要求：\n* 仅输出合法 JSON，无其他文字。\n* 数值保留两位小数。\n"""

json_str = stream_claude(prompt)
print(json_str)
```

---

## 5. 常见错误与防御（1 分钟）
| 错误类型 | 说明 | 应对策略 |
| --- | --- | --- |
| 混入自然语言 | 模型在 JSON 前后添加解释 | 在 Prompt 中强调"仅输出合法 JSON"并提供示例 |
| 字段缺失/拼写错误 | 与 Schema 不匹配 | 在后处理阶段使用 `jsonschema` 校验并重试 |
| 数值格式不一致 | 小数位数不统一 | 明确格式要求，如"保留两位小数" |

---

## 6. 总结（1 分钟）
通过在 Prompt 中明确 **字段、格式、示例输出**，可以显著提升大模型生成结构化数据的稳定性与可解析性，为银行风控与合规系统打下坚实基础。下一步，我们将在 Jupyter Notebook 中进一步演示并配合 `jsonschema` 做自动校验。

