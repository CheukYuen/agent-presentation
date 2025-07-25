# OpenAI 微调教学大纲（SFT 快速实操版）

> 面向银行内部技术与业务同学，**总时长约 15 分钟**。所有示例仅供参考，不构成投资建议；AI 仅作"意图识别 & 参数收集"工具，核心交易须经过后台风控及合规校验。

---

## 1. 前言 ⭐（1 min）
* 为什么要做微调：银行业务术语、合规表达、标准化输出
* SFT 定义：使用少量高质量标注数据对现有大模型进行再训练，最小化交叉熵损失，实现特定任务最佳表现
* 交叉熵损失 (Cross-Entropy Loss)：衡量模型预测概率分布与真实分布之间差异的函数，公式 \(L = -\sum_{i} y_i \log p_{\theta}(y_i\,|\,x)\)。最小化该损失等价于最大化模型对正确标签的对数似然，从而提升分类准确率
* 价值：将基金类型分类准确率从≈50% 提升到≈95%，同时强制输出合规格式，减少人工校对
* 成本：60 条样本 ×3 epoch ≈ 30k token，训练费用<1 RMB；推理成本与原生 gpt-3.5 相同
* 本次案例：基金类型智能筛选（文本→标签分类）

---

## 2. 数据准备与质量控制（4 min）
* 数据格式：OpenAI JSONL（system+user+assistant三段式）
* 类别覆盖：**债券、股票、混合、指数、QDII、ETF、LOF**（共7类，均为开放式基金）
* 样本采集：爬取同花顺等公开基金列表 → 选取名称+官方类型 → 人工校验
* 自动脚本：`make_dataset.py` 一键生成 60 条 `fund_type_training.jsonl`
* 训练/测试拆分：脚本默认每类随机抽取 13 条（10 训练 + 3 测试），固定 `random_state=42`，输出 `fund_type_training.jsonl` 与 `fund_type_test.jsonl`
* 脚本源码：`scripts/make_dataset.py`（可提前运行并缓存结果，确保课堂不等待）
* 合规要求：assistant 仅输出类别+*仅供参考，不构成投资建议*
* **数据文件路径**：所有数据文件均位于 `fineture/` 目录下：
  - 原始全量数据：`fineture/fund_type_training.jsonl`
  - 训练集：`fineture/fund_type_train.jsonl`
  - 测试集：`fineture/fund_type_test.jsonl`

---

## 2.1 数据采集与拆分流程（补充）

* 本案例采用"从 0 到 1"最小可行流程，仅依赖公开数据源和一段 Python 脚本即可完成：
  - 训练集：≈ 60 条（每类基金 10 条）
  - 测试集：≈ 21 条（每类基金 3 条，保证不与训练集重复，7类*3=21）
  - 所有示例仅供参考，不构成投资建议

### 一、数据源在哪里找？
- 同花顺（https://fund.10jqka.com.cn/datacenter/jz/kfs/qdii/）等公开渠道：
- 采集基金类别包括：**债券、股票、混合、指数、QDII、ETF、LOF**
- 只需两列：
  - 基金简称（或代码+简称）
  - 基金类型（官方披露：债券/股票/混合/指数/QDII/ETF/LOF）

### 二、脚本① 清洗 & 采样（make_dataset.py）
- 见附录/脚本目录，自动完成数据清洗、分组、JSONL 生成

### 三、为什么这样分？
- "同一来源+随机拆分"确保两组数据分布一致，评估更可靠
- 固定 random_state=42，每次演示都得到同样切分，结果可复现
- 测试集不进训练流程，微调好后只在测试集上评估，确保不是"记忆"

### 四、检查清单
- [ ] 每类基金至少 10 条训练样本、3 条测试样本（7类共计约60+21条）
- [ ] assistant 输出格式完全一致（含星号与空格）
- [ ] fund_type_test.jsonl 从未上传给 OpenAI 训练，只在本地推理
- [ ] .env 中的 OPENAI_API_KEY 已配置好

按照上述脚本，你就拥有了可靠的训练集和测试集；训练完成后，在 fund_type_test.jsonl 上跑推理对比，就能看到准确率的大幅提升。

---

## 3. SFT 微调实操流程（6 min）
1. 生成训练数据
   * 运行 `python make_dataset.py`，产生 `fund_type_training.jsonl`
2. 上传文件 & 创建微调任务
   * `openai files create --purpose fine-tune --file fineture/fund_type_train.jsonl`
   * `openai fine_tuning.jobs.create --training_file <FILE_ID> --model gpt-4.1-nano-2025-04-14 --suffix fund-type-v1`
3. 监控日志 & 成本评估
   * `openai fine_tuning.jobs.follow <JOB_ID>` 查看进度与 token 消耗
4. API 测试对比
   * `test_accuracy.py`：原始模型 vs 微调模型 → 打印准确率提升

---

## 4. 自动化评测（Evals）（2 min）
* 推荐使用 OpenAI 官方 Evals Python 框架，对微调后的 gpt-4.1-nano-2025-04-14 模型进行自动化评测。
* 评测数据建议使用 `fineture/fund_type_test.jsonl`，可自动计算准确率等关键指标。
* 官方推荐通过 Python API 进行评测，示例代码如下：

```python
import openai
import json

def evaluate_model(model_name, test_file):
    with open(test_file, 'r', encoding='utf-8') as f:
        test_data = [json.loads(line) for line in f if line.strip()]
    correct = 0
    for sample in test_data:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": sample["system"]},
                {"role": "user", "content": sample["user"]}
            ],
            temperature=0
        )
        output = response["choices"][0]["message"]["content"].strip()
        if output == sample["assistant"]:
            correct += 1
    accuracy = correct / len(test_data)
    print(f"{model_name} Accuracy: {accuracy:.2%}")

# 对比两个模型
evaluate_model("gpt-4.1-nano-2025-04-14", "fineture/fund_type_test.jsonl")  # 基线
# 替换为你的微调模型名称
# evaluate_model("ft:gpt-4.1-nano-2025-04-14:your-org::xxxxxx", "fineture/fund_type_test.jsonl")  # 微调后
```
- 你可以根据业务需求自定义评测指标和输出格式。
- 推荐用表格或百分比直观展示提升：

```
| 模型名称                | 准确率   |
|------------------------|---------|
| gpt-4.1-nano-2025-04-14|  82.1%  |
| 微调后模型              |  97.4%  |
| 提升                    | +15.3%  |
```
- 评测结果可用于模型效果量化、合规归档和持续优化。

* **最佳实践**：
  - 训练、评测数据分离，保证评测客观性。
  - 评测时 temperature=0，保证输出稳定。
  - 评测结果归档，便于后续模型对比和合规审计。
  - 评测流程自动化，减少人工干预。

---

## 5. 效果评估与合规要点（3 min）
* 分类准确率提升（案例对比）
* 合规输出：仅标签+声明，杜绝解释性内容
* 数据安全与日志审计

---

## 6. 总结与提问（1 min）
* SFT 快速落地流程回顾
* 推荐阅读与后续进阶方向

---

## 附录 A．课堂演示成功技巧 & Checklist

### A1 让准确率显著提升的 8 个技巧
1. **数据三一致**：system 提示 & assistant 标签格式在训练/测试/线上完全一致。
2. **样本均衡 & 去重**：各类别样本数相近，测试集不含训练集名称。
3. **先做 Baseline，再微调**：原生 gpt-3.5 先跑测试集记录准确率。
4. **推理温度固定**：评估时 `temperature=0`，输出更稳定。
5. **训练轮次少而精**：60×3 epoch 足够，epoch 过多易过拟合。
6. **训练结束立即验证**：`openai fine_tuning.jobs.follow` 完成后立刻评估。
7. **评估脚本要"说人话"**：打印"原生 vs 微调"差值，如 `48% ➜ 97% (+49%)`。
8. **预演 + 缓存结果**：课前完整跑通，保存日志/截图，防网络波动。

### A2 Checklist
- [ ] assistant 标签格式统一（含星号和空格）
- [ ] Baseline 准确率已记录
- [ ] 评估脚本 `temperature=0`
- [ ] 测试集 (`fund_type_test.jsonl`) 未上传训练
- [ ] 合规声明始终保留：*仅供参考，不构成投资建议*

---

> **下一步**：基于本大纲创建 Jupyter Notebook，聚焦"基金类型智能筛选"SFT案例，所有API调用均为流式输出。
