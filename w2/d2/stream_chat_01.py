# 3.1 最简流式输出（打字机效果）
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)

MODEL = "deepseek-chat"
messages = [{"role": "user", "content": "请用 100 字介绍你自己"}]

# 流式调用
stream = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    stream=True
)

print("AI: ", end="", flush=True)

full_response = ""
for chunk in stream:
    # 每个 chunk 可能有 content，也可能没有
    if chunk.choices[0].delta.content:
        content = chunk.choices[0].delta.content
        full_response += content
        print(content, end="", flush=True)  # flush=True 立即输出

print()  # 最后换行

# 完整响应用于后续使用
print(f"\n(共 {len(full_response)} 个字符)")

# 3.2 检测流式结束
stream = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    stream=True
)

for chunk in stream:
    delta = chunk.choices[0].delta

    # 检测是否有内容
    if delta.content:
        print(delta.content, end="", flush=True)

    # 检测流式是否结束
    if chunk.choices[0].finish_reason:
        reason = chunk.choices[0].finish_reason
        print(f"\n\n[流式结束, 原因: {reason}]")
        # finish_reason 可能的取值:
        #   "stop"     - 正常结束
        #   "length"   - 达到 max_tokens
        #   "content_filter" - 内容过滤
        #   "tool_calls"     - 触发了函数调用

# 3.3 逐字加速效果（控制打印速度）
import time

stream = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    stream=True
)

SPEED = 0.03  # 每个字间隔 0.03 秒（模拟真人打字）

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
        time.sleep(SPEED)  # 减慢速度，更像真人打字
