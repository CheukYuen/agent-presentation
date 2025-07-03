import os
import httpx
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量，确保OPENAI_API_KEY已配置
load_dotenv()

# 配置OpenAI客户端（如需代理可自行调整）
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(proxy="http://127.0.0.1:7890/")  # 如无代理可去掉此行
)

def stream_openai_chat(prompt, model="gpt-4.1-nano-2025-04-14", system_prompt="", max_tokens=512, temperature=0.7):
    """
    调用OpenAI API的流式输出函数
    :param prompt: 用户输入内容
    :param model: 使用的模型名称
    :param system_prompt: 系统提示词
    :param max_tokens: 最大生成长度
    :param temperature: 随机性参数
    :return: 最终完整回复字符串
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    full_response = ""
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
    except Exception as e:
        print(f"\n❌ API 调用错误: {e}")
        return None
    print()  # 输出换行
    return full_response

# 示例用法
if __name__ == "__main__":
    print("\n=== OpenAI 流式输出演示 ===")
    result = stream_openai_chat(
        prompt="永赢医药健康A 是什么类型基金？",
        system_prompt="你是银行金融分析助手，所有输出仅供参考，不构成投资建议。",
        max_tokens=200,
        temperature=0.3
    )
    print("\n⚠️ 免责声明：以上内容仅供参考，不构成投资建议。投资有风险，决策需谨慎。")
