# OpenAI 微调教学大纲（SFT & RFT）

> 面向银行内部技术与业务同学，**总时长约 45 分钟**。所有示例仅供参考，不构成投资建议；AI 仅作"意图识别 & 参数收集"工具，核心交易须经过后台风控及合规校验。

---

## 1. 前言 ⭐（2 min）
* 为什么需要微调：行业术语、合规表达、业务流程定制
* SFT 与 RFT 的定位：离线监督学习 vs 在线奖励优化
* 学习目标与成果：
  * 理解两种微调原理与适用场景
  * 能够独立完成一次 SFT / RFT 流程
  * 构建银行合规审计闭环

---

## 2. Supervised Fine-Tuning (SFT) 模块（18 min）

### 2.1 核心概念（3 min）
* 定义：使用标注数据最小化交叉熵损失 \(L_{SFT} = -\sum \log p_\theta(y\,|\,x)\)
* 适用场景：FAQ、高准确率意图识别、基金产品说明生成
* SFT 流程总览：数据→上传→训练→评估→部署

### 2.2 数据准备与质量控制（4 min）
* 数据格式：OpenAI JSONL schema（`{"messages": [...]}`）
* 标注规范：脱敏 & 合规字段校验
* 数据分层：train / validation / test
* 质量提升技巧：
  * 反向标注法检查一致性
  * 确保类别分布均衡

### 2.3 微调实操步骤（6 min）
1. 上传文件：`openai file create -p fine-tune.jsonl`
2. 创建任务：`openai fine_tuning.jobs.create -m gpt-3.5-turbo`
3. 监控日志：`openai fine_tuning.jobs.follow <JOB_ID>`
4. 成本评估：token 计费公式与预算控制

*案例聚焦：以"基金产品 Q&A Bot (v1)"为示例数据集，完成一次 SFT 全流程*

### 2.4 评估与回归测试（3 min）
* 使用 Metrics API 查看 loss & accuracy
* 引入 Evals / Graders 做自动化测试
* 金融合规脚本示例：违规用语检测、风险提示检查

### 2.5 SFT 最佳实践（2 min）
* 小批量迭代 + 早停
* 合理设置 learning_rate & n_epochs
* Prompt 模板化：系统提示中植入"仅供参考"免责声明

---

## 3. Reinforcement Fine-Tuning (RFT) 模块（18 min）

### 3.1 核心概念（3 min）
* 奖励模型 (RM) 训练：基于偏好比较数据 \(D_p\)
* PPO / DPO 策略：最大化期望奖励 \(\mathbb{E}_{x\sim D}[R(x)]\)
* 与 SFT 关系：SFT 作为初始化权重，RFT 精调行为

### 3.2 奖励模型构建（4 min）
* 采集银行业务偏好对：回答 A vs 回答 B
* 使用 Graders 自动生成评分
* 过拟合检测 & 正则化方法

### 3.3 RFT 训练流程（6 min）
1. 准备 SFT-model 作为初始策略
2. 定义奖励函数：合规分 + 业务价值分 = 总分
3. 启动训练：`openai rl_fine_tuning.jobs.create`
4. 监控 KL-penalty & reward saturation

*同一案例延续：在"基金产品 Q&A Bot (v1)"基础上，通过 RFT (v2) 提升回复质量与合规性*

### 3.4 在线/离线评估（3 min）
* A/B 测试：客服回复点击率
* 合规指标：违规率 ≤ 0.1 %
* 复核：人工抽检 + 自动 grader

### 3.5 RFT 最佳实践（2 min）
* 奖励"三重底线"：合规 > 准确 > 流畅
* 防止模式崩溃：KL 控制、梯度裁剪
* 迭代节奏：SFT → RFT → 小样本人工评估

---

## 4. SFT vs RFT 对比与选型（3 min）
| 维度 | SFT | RFT |
|------|-----|-----|
| 数据 | 明确标注 | 偏好比较 / 评分 |
| 目标 | 拟合黄金标准 | 最大化奖励函数 |
| 成本 | 标注费高 | 计算费高 |
| 风险 | 数据偏差 | 奖励误导 |
| 典型场景 | FAQ、摘要 | 动态对话、推荐生成 |
| **案例实例** | Q&A Bot v1 (SFT) | Q&A Bot v2 (RFT) |

---

## 5. 银行业案例综合演练 ⭐（3 min）
* SFT：定制"基金产品 Q&A Bot"
* RFT：优化回复 → 自动加入风险提示 & 个性化推荐
* 现场演示：API 调用（streaming 输出）

---

## 6. 合规与风控要点（2 min）
* 数据脱敏 & 权限管理
* 输出需附"仅供参考，不构成投资建议"
* 后端审计日志 & 回放机制

---

## 7. 总结与提问（2 min）
* 两大路线：SFT 打基础，RFT 做精细化
* 银行场景闭环：数据→训练→评估→上线→监控
* 推荐阅读：官方文档 #1–9

---

> **下一步**：基于本大纲创建 Jupyter Notebook，遵循"前言→核心概念→实践示例→演示代码→总结"五段式结构，并实现所有 API 调用的 **流式输出**。
