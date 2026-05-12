"""
练习 3: 打字机速度控制
目标: 实现可调节速度的流式输出
要求: time.sleep() 控制每个字间隔
"""
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"

# 速度级别: fast(0.01s) / normal(0.05s) / slow(0.15s) / typewriter(0.3s)
SPEED = {
    "fast": 0.01,
    "normal": 0.05,
    "slow": 0.15,
    "typewriter": 0.3,
}

def stream_with_speed(messages, speed="normal"):
    """带速度控制的流式输出"""
    delay = SPEED.get(speed, 0.05)
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )

    full_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
            time.sleep(delay)  # 核心：每个字之间等待
            full_response += delta.content

    return full_response

# 演示不同速度
question = "请用一句话介绍 Python 的 yield 关键字。"

for speed_name in ["fast", "normal", "typewriter"]:
    print(f"\n── 速度: {speed_name} ({SPEED[speed_name]}s/字) ──")
    input("按回车开始...")
    print("AI > ", end="", flush=True)
    result = stream_with_speed(
        [{"role": "user", "content": question}],
        speed=speed_name
    )
    print(f"\n  完整: {result}")
