"""
练习 2: 流式多轮对话
目标: 实现带记忆的流式对话
要求: 保存完整响应到 messages 历史
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"

# 初始化对话历史
messages = [
    {"role": "system", "content": "你是一个有帮助的 AI 助手，请用中文回答。"}
]

print("=== 流式多轮对话（输入 /exit 退出）===\n")

while True:
    user_input = input("\n你 > ").strip()
    if user_input.lower() in ("/exit", "/quit"):
        print("再见！")
        break
    if not user_input:
        continue

    # 添加用户消息
    messages.append({"role": "user", "content": user_input})

    # 流式调用
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )

    # 收集完整响应
    full_response = ""
    print("AI > ", end="", flush=True)
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
            full_response += delta.content
    print()  # 换行

    # 保存完整响应到历史（关键：带记忆的核心）
    messages.append({"role": "assistant", "content": full_response})

    # 显示当前消息数
    print(f"  [历史: {len(messages)} 条消息]")
