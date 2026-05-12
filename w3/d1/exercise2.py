"""
练习 2: Few-shot 分类器
目标: 用 Few-shot 实现意图分类器，支持 4 个意图
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"


def classify_intent(user_input: str) -> str:
    """用 Few-shot 示例判断用户输入属于哪个意图类别"""
    messages = [
        {"role": "system", "content": "请判断用户输入的意图，只返回意图名称，不要多余文字。"},
        # --- Few-shot 示例 ---
        {"role": "user", "content": "北京明天会下雨吗"},
        {"role": "assistant", "content": "查询天气"},
        {"role": "user", "content": "上海的气温是多少"},
        {"role": "assistant", "content": "查询天气"},
        # 数学计算
        {"role": "user", "content": "25 乘以 4 等于多少"},
        {"role": "assistant", "content": "数学计算"},
        {"role": "user", "content": "1024 开平方根"},
        {"role": "assistant", "content": "数学计算"},
        # 新闻查询
        {"role": "user", "content": "今天有什么科技新闻"},
        {"role": "assistant", "content": "新闻查询"},
        {"role": "user", "content": "最近 AI 领域有什么大事"},
        {"role": "assistant", "content": "新闻查询"},
        # 闲聊
        {"role": "user", "content": "你好，今天心情怎么样"},
        {"role": "assistant", "content": "闲聊"},
        {"role": "user", "content": "讲个笑话"},
        {"role": "assistant", "content": "闲聊"},
        # --- 真正的输入 ---
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    test_inputs = [
        "深圳今天多少度",
        "999 除以 3",
        "特朗普最近干啥了",
        "你觉得人生意义是什么",
        "杭州明天刮风吗",
        "512 + 256",
        "苹果发布了什么新产品",
        "嗨"
    ]

    print("Few-shot 意图分类测试:\n")
    for inp in test_inputs:
        intent = classify_intent(inp)
        print(f"  「{inp}」  →  {intent}")
