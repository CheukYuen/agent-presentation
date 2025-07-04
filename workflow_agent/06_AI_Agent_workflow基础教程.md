# AI Agent Workflow 基础教程（15分钟精简版）

## 🎯 学习目标
- **深度理解 AI Agent vs Workflow 核心定义**
- **掌握银行场景下的智能代理设计原则**
- **学会构建简单、透明、稳健的 Agent 系统**
- **实践银行业务中的实际应用场景**

## 📊 课程结构
| 时间 | 内容 | 重点 |
|------|------|------|
| 0-3分钟 | 核心定义对比 | Agent vs Workflow 本质区别 |
| 3-6分钟 | 设计模式精要 | 关键模式快速掌握 |
| 6-10分钟 | Workflow实战 | 资讯摘要流程实现 |
| 10-14分钟 | Agent实战 | 交易分析智能体构建 |
| 14-15分钟 | 总结与实践 | 银行应用最佳实践 |

---

## 📋 核心定义对比（3分钟）

### 🔑 Anthropic 官方定义

| 特征 | **Workflow** | **Agent** |
|------|-------------|----------|
| **本质定义** | 预定义的代码执行路径 | LLM驱动的自主决策系统 |
| **控制方式** | 人类预先设计固定步骤 | AI动态规划和调整策略 |
| **适用场景** | 固定步骤、可预测任务 | 开放式、复杂决策任务 |
| **银行应用** | 晨报生成、合规检查、标准化审核 | 复杂投研分析、客户问题处理 |
| **成本控制** | 低成本、快速响应 | 高成本、深度分析 |
| **可预测性** | 高度可预测，路径固定 | 不完全可预测，智能适应 |
| **调试难度** | 容易调试和优化 | 需要复杂的监控和评估 |

### 🏦 银行业务选择策略

**⭐ 核心原则：Anthropic建议寻找最简单的解决方案**

1. **单次LLM调用** → 60%的银行查询场景
2. **Workflow模式** → 标准化流程（资讯摘要、风险检查）
3. **Agent模式** → 复杂决策（投资组合分析、客户咨询）

### 🔧 设计原则（Anthropic三大支柱）

1. **Simplicity 简洁优先**：能用单步解决就别用多步
2. **Transparency 透明可诊断**：显式输出思考过程  
3. **Robust ACI 稳健接口**：工具描述要"傻瓜化"

> **关键区别**：Workflow是"程序化执行"，Agent是"智能化决策"

---

## 🔗 核心设计模式精要（3分钟）

基于 Anthropic 官方指南的五大模式：

### 1. **Prompt Chaining 串行链式** ⭐ 
- **机制**：任务分解为固定步骤序列（Workflow模式）
- **银行应用**：资讯摘要 → 风险评估 → 合规审查
- **优势**：可控、可预测、易调试

### 2. **Routing 智能路由**
- **机制**：分类输入，导向专门的子流程
- **银行应用**：客户问题分类（行情查询/政策解读/风险咨询）

### 3. **Parallelization 并行处理**
- **银行应用**：多指标并行计算（RSI + MACD + KDJ）

### 4. **Orchestrator-Workers 编排-执行** ⭐
- **机制**：中央LLM动态分解任务（Agent模式）
- **银行应用**：复杂投研报告（基本面+技术面+风险面）

### 5. **Evaluator-Optimizer 评估-优化**
- **银行应用**：投资建议书撰写与风险措辞优化

> **⚠️ 选择策略**：优先考虑简单模式，只有在必要时才增加复杂性

---

## 💻 技术实现：JSON文件存储系统

```python
# JSON文件存储系统
class BankDataStorage:
    """银行数据存储 - 使用JSON文件"""
    
    def __init__(self, base_path="bank_data"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        
        # 初始化存储文件
        self.files = {
            "news_analysis": f"{base_path}/news_analysis.json",
            "trading_analysis": f"{base_path}/trading_analysis.json"
        }
        
        # 确保文件存在
        for file_path in self.files.values():
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
    
    def save_news_analysis(self, data: Dict):
        """保存新闻分析结果"""
        data["timestamp"] = datetime.now().isoformat()
        data["id"] = f"news_{int(datetime.now().timestamp())}"
        
        with open(self.files["news_analysis"], 'r', encoding='utf-8') as f:
            records = json.load(f)
        
        records.append(data)
        
        with open(self.files["news_analysis"], 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    
    def save_trading_analysis(self, data: Dict):
        """保存交易分析结果"""
        data["timestamp"] = datetime.now().isoformat()
        data["id"] = f"trade_{int(datetime.now().timestamp())}"
        
        with open(self.files["trading_analysis"], 'r', encoding='utf-8') as f:
            records = json.load(f)
        
        records.append(data)
        
        with open(self.files["trading_analysis"], 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
```

---

## 🔗 Workflow实战：资讯摘要系统（4分钟）

### 特征：Prompt Chaining 模式
- ✅ **固定步骤**：信息提取 → 摘要生成 → 合规检查
- ✅ **路径可预测**：每次执行相同的3个步骤
- ✅ **适合标准化**：银行资讯处理的标准流程

### 实现代码

```python
class NewsAnalysisWorkflow:
    """资讯分析工作流 - 基于Prompt Chaining模式（Workflow）"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def step1_extract_info(self, news_content: str) -> Dict:
        """步骤1：信息提取（固定步骤）"""
        system_prompt = """你是银行资讯分析专家。从新闻中提取关键信息，输出JSON格式：
        {
            "title": "新闻标题",
            "key_points": ["要点1", "要点2"],
            "mentioned_stocks": ["股票代码"],
            "policy_impact": "政策影响描述"
        }"""
        
        prompt = f"请分析以下财经新闻：\\n\\n{news_content}"
        
        print("🔍 步骤1：信息提取中...")
        response = call_claude_stream(prompt, system_prompt, max_tokens=500, temperature=0.3)
        
        # 解析JSON结果
        return parse_json_response(response)
    
    def step2_generate_summary(self, extracted_info: Dict) -> str:
        """步骤2：生成摘要（固定步骤）"""
        system_prompt = """你是银行投资顾问，为客户撰写简洁的投资资讯摘要。
        要求：1. 100字以内 2. 突出投资相关性 3. 语言专业但易懂"""
        
        prompt = f"""基于提取的信息生成摘要：
        标题：{extracted_info.get('title', '')}
        要点：{extracted_info.get('key_points', [])}
        政策影响：{extracted_info.get('policy_impact', '')}"""
        
        print("📝 步骤2：摘要生成中...")
        return call_claude_stream(prompt, system_prompt, max_tokens=300, temperature=0.5)
    
    def step3_compliance_check(self, summary: str) -> str:
        """步骤3：合规检查（固定步骤）"""
        system_prompt = """你是银行合规官员，审查投资资讯的合规性。
        要求：1. 添加风险提示 2. 避免直接投资建议 3. 符合金融机构规范"""
        
        prompt = f"请审查以下资讯摘要的合规性：\\n\\n{summary}"
        
        print("⚖️ 步骤3：合规检查中...")
        return call_claude_stream(prompt, system_prompt, max_tokens=400, temperature=0.2)
    
    def execute_workflow(self, news_content: str) -> str:
        """执行完整的工作流程（Workflow特征：固定路径）"""
        print("🚀 开始执行资讯分析Workflow\\n" + "="*50)
        
        # 固定的3步执行路径
        extracted_data = self.step1_extract_info(news_content)
        summary = self.step2_generate_summary(extracted_data)
        final_result = self.step3_compliance_check(summary)
        
        # 保存结果
        self.storage.save_news_analysis({
            "title": extracted_data.get('title', ''),
            "content": news_content[:200],
            "summary": final_result,
            "workflow_type": "prompt_chaining"
        })
        
        print("✅ 工作流执行完成！")
        return final_result
```

### 🔑 Workflow特征体现：
- ✅ 固定3步骤：提取→摘要→合规
- ✅ 路径可预测：每次都相同的执行顺序
- ✅ 适合标准化：银行资讯处理的标准流程

---

## 🤖 Agent实战：交易分析智能体（4分钟）

### Agent vs Workflow 关键区别展示

**刚才的资讯摘要**是 **Workflow**：
- ✅ 固定3步骤：提取 → 摘要 → 合规
- ✅ 路径可预测，适合标准化处理

**接下来的交易分析**是 **Agent**：
- 🧠 LLM自主决定分析深度和工具选择
- 🔄 基于数据反馈动态调整策略
- 🎯 适合复杂的、步骤不可预测的分析任务

### 实现代码

```python
class TradingAnalysisAgent:
    """
    交易趋势分析智能体 - 基于Agent模式
    特点：自主规划、动态工具选择、智能决策
    """
    
    def __init__(self, storage):
        self.storage = storage
        self.tools = {
            "get_stock_data": self._get_stock_data,
            "calculate_indicators": self._calculate_indicators,
            "get_market_sentiment": self._get_market_sentiment
        }
    
    def _get_stock_data(self, symbol: str) -> Dict:
        """模拟获取股票数据"""
        return {
            "symbol": symbol,
            "current_price": round(15.0 + random.uniform(-1, 1), 2),
            "volume": random.randint(8000000, 15000000),
            "change_percent": round(random.uniform(-3, 3), 2)
        }
    
    def _calculate_indicators(self, stock_data: Dict) -> Dict:
        """模拟计算技术指标"""
        return {
            "RSI": round(45 + random.uniform(-20, 20), 2),
            "MACD": round(random.uniform(-0.5, 0.5), 3),
            "trend": random.choice(["看涨", "看跌", "震荡"])
        }
    
    def _get_market_sentiment(self, symbol: str) -> Dict:
        """模拟获取市场情绪"""
        return {
            "sentiment": random.choice(["积极", "中性", "谨慎"]),
            "institutional_rating": random.choice(["买入", "持有", "卖出"]),
            "confidence": round(random.uniform(0.5, 0.9), 2)
        }
    
    def analyze_stock(self, stock_symbol: str) -> str:
        """
        主分析方法 - Agent自主决定分析策略（Agent特征：智能决策）
        """
        print(f"🤖 交易分析Agent启动，目标股票：{stock_symbol}")
        
        # Agent自主规划分析步骤（区别于Workflow的固定步骤）
        plan_prompt = f"""
        你是专业的银行投资分析师，需要分析股票 {stock_symbol}。
        
        可用工具：
        1. get_stock_data - 获取股价数据
        2. calculate_indicators - 计算技术指标
        3. get_market_sentiment - 获取市场情绪
        
        请制定你的分析计划，说明你将如何使用这些工具。
        """
        
        print("🧠 Agent智能规划分析策略...")
        plan = call_claude_stream(plan_prompt, "", max_tokens=300, temperature=0.3)
        
        # Agent根据计划执行分析（动态决策）
        return self._execute_intelligent_analysis(stock_symbol)
    
    def _execute_intelligent_analysis(self, stock_symbol: str) -> str:
        """执行智能分析（Agent特征：基于数据反馈调整）"""
        
        # Agent动态调用工具
        print("📊 Agent动态获取数据...")
        stock_data = self._get_stock_data(stock_symbol)
        indicators = self._calculate_indicators(stock_data)
        sentiment = self._get_market_sentiment(stock_symbol)
        
        # Agent基于数据进行智能综合分析
        analysis_prompt = f"""
        作为银行投资分析师，基于以下数据进行智能分析：
        
        股票：{stock_symbol}
        价格：{stock_data['current_price']}元 ({stock_data['change_percent']:+.1f}%)
        RSI：{indicators['RSI']}
        趋势：{indicators['trend']}
        市场情绪：{sentiment['sentiment']}
        机构评级：{sentiment['institutional_rating']}
        
        请提供专业分析报告，包含投资建议和风险提示。
        """
        
        print("🔍 Agent智能综合分析中...")
        analysis_result = call_claude_stream(
            analysis_prompt, 
            "你是专业银行投资分析师，分析要客观、专业，必须包含风险提示。",
            max_tokens=600, 
            temperature=0.4
        )
        
        # 保存分析结果
        self.storage.save_trading_analysis({
            "symbol": stock_symbol,
            "analysis_type": "intelligent_agent",
            "stock_data": stock_data,
            "indicators": indicators,
            "sentiment": sentiment,
            "recommendation": analysis_result[:200]
        })
        
        return analysis_result
```

### 🔑 Agent特征体现：
- 🧠 智能规划：AI自主制定分析策略
- 🔄 动态调整：基于数据反馈智能决策
- 🎯 复杂任务：适合不可预测的分析场景

---

## 📚 总结与银行应用最佳实践（1分钟）

### 🎯 核心要点回顾

1. **本质区别**：
   - **Workflow**：预定义代码路径，固定步骤执行
   - **Agent**：LLM驱动的自主决策系统，智能规划

2. **选择策略**：
   ```
   简单查询 → 单次LLM调用
   标准流程 → Workflow模式（资讯摘要、合规检查）
   复杂决策 → Agent模式（投资分析、客户咨询）
   ```

3. **设计原则**：
   - **Simplicity**：优先选择最简单的解决方案
   - **Transparency**：显式输出思考过程
   - **Robust ACI**：精心设计工具接口

### 🏦 银行实施建议

**实施路径**：
1. **阶段1**：从Workflow开始（资讯摘要、标准审核）
2. **阶段2**：引入简单Agent（单一投资分析）
3. **阶段3**：构建复杂Agent系统（多维度分析）

**合规要求**：
- ⚠️ AI仅作"分析工具"，不自动执行交易
- ⚠️ 所有输出必须包含免责声明
- ⚠️ 完整记录分析过程便于审计

**技术优势**：
- 📁 JSON文件存储：轻量级、易调试、便于备份
- 🔄 模块化设计：Workflow和Agent可独立部署
- 📊 透明监控：每步操作都有明确记录

> **记住**：成功的AI系统不在于复杂性，而在于恰到好处地解决实际业务问题！

---

## ⚠️ 重要提醒

**本教程所有投资分析内容仅供学习参考，不构成投资建议。银行实际应用中，所有交易决策必须经过严格的风控审批流程。**

### 基于 Anthropic 官方最佳实践
> 参考资料：[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)