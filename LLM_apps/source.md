
人工智能时代的软件

# Part1:  人工智能时代的软件

https://by-andrej-karpathy-7z87dvh.gamma.site/ycaistartup2025

新未来趋势

# 演示 cursor
- **Cursor**：AI 辅助代码编辑器
- **OpenAI Deep Research**：深度研究助手
- **Google NotebookLM**：智能笔记系统
- **Anthropic Artifacts**：可执行内容生成
BOA
robinhood

# 设立自己的评估体系， 行业落地
红杉中国在2025年5月26日发布的论文《xbench: tracking agents productivity scaling with profession-aligned real-world evaluations》介绍了针对AI实际产业落地能力评估的benchmark——xbench。以下是关于xbench的具体介绍：
评估体系
双轨评估体系：创新性地将评测任务分为两条互补的主线。第一，评估AI系统的能力上限与技术边界；第二，量化AI系统在真实场景的效用价值（utility value）。后者需要动态对齐现实世界的应用需求，基于实际工作流程和具体社会角色，为各垂直领域构建具有明确业务价值的测评标准。
长青评估机制：通过持续维护并动态更新测试内容，以确保时效性和相关性。定期测评市场主流agent产品，跟踪模型能力演进，捕捉agent产品迭代过程中的关键突破，进而预测下一个agent应用的技术-市场契合点（tmf，tech-market fit）。
评估方法
真实业务需求驱动任务设计：任务直接来源于行业专家的真实业务需求。例如，在招聘评估中，agent需要根据职位描述（jd）完成企业映射（company mapping）、人才信息补全（people-to-info）和信息到人才的匹配（info-to-people）等任务；营销评估则要求agent根据广告主的产品信息和推广需求，筛选出合适的网红。
专业化评分标准：采用基于大语言模型（llm）的评分机制（llm-as-a-judge），结合行业专家制定的评分细则，对agent的输出进行1-5分的评分。例如，在招聘任务中，评分标准包括覆盖率、幻觉检测、信息质量等。
技术-市场契合度（tmf）分析：通过分析agent的性能与成本的关系，预测其技术-市场契合度（tmf）。将市场接受曲线（基于任务价值和成本）和技术可行性曲线（基于agent性能）结合，找到两者的交集，量化agent的单位任务价值。
动态评估与xbench-index：引入xbench-index，通过项目反应理论估算agent的能力值。这种方法能够从不完整的评分矩阵中提取能力主成分，跟踪agent在不同时间点的能力增长趋势。
评估结果
领先agent的表现：在招聘和营销基准测试中，o3以78.5和50.8的平均分位居榜首，显示出其在职业化任务中的强大能力。
技术并非唯一：模型规模更大的agent（如gemini-2.5-pro）并不一定表现优于较小的模型（如gemini-2.5-flash），表明搜索能力和任务适配性更为关键。
幻觉问题需警惕：某些agent（如perplexity-research）在扩展研究过程中可能引入更多幻觉，影响其在招聘任务中的表现。