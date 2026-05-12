"""
练习 1: 基础流式输出
目标: 实现一个逐字打印的聊天程序
要求: stream=True, flush=True 逐字输出
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

messages = [
    {"role": "system", "content": "你是一个有用的助手，请用中文回答。"},
    {"role": "user", "content": "请用 100 字以内介绍流式输出（Streaming）的原理。"}
]

stream = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    stream=True
)

print("AI > ", end="", flush=True)
full_response = ""
for chunk in stream:
    delta = chunk.choices[0].delta
    if delta.content:
        print(delta.content, end="", flush=True)
        full_response += delta.content

print(f"\n\n--- 完整响应 ({len(full_response)} 字) ---")
print(full_response)
