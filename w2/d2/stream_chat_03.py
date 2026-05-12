from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"

# 定义工具 —— 告诉 LLM 有哪些函数可以调用
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "城市名，例如：北京、上海"}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式，例如：1+2*3"}
                },
                "required": ["expression"]
            }
        }
    }
]

messages = [{"role": "user", "content": "北京今天天气怎么样？顺便帮我算一下 25*4+10 等于多少？"}]

stream = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    stream=True,
    tools=tools          # ← 传入 tools，LLM 才知道可以调用函数
)

collected_tool_calls = {}

for chunk in stream:
    delta = chunk.choices[0].delta

    # 文本内容
    if delta.content:
        print(delta.content, end="", flush=True)

    # 函数调用增量
    if delta.tool_calls:
        for tc in delta.tool_calls:
            idx = tc.index
            if idx not in collected_tool_calls:
                collected_tool_calls[idx] = {
                    "id": tc.id or "",
                    "function_name": tc.function.name or "",
                    "arguments": tc.function.arguments or ""
                }
            else:
                if tc.function.arguments:
                    collected_tool_calls[idx]["arguments"] += tc.function.arguments
                if tc.id:
                    collected_tool_calls[idx]["id"] = tc.id
                if tc.function.name:
                    collected_tool_calls[idx]["function_name"] = tc.function.name

# 检查是否有函数调用
if collected_tool_calls:
    print("\n\n[LLM 调用了工具]")
    for idx, tc in collected_tool_calls.items():
        print(f"  → {tc['function_name']}({tc['arguments']})")

    # 实际执行函数调用
    print("\n[执行结果]")
    for idx, tc in collected_tool_calls.items():
        args = json.loads(tc["arguments"])
        if tc["function_name"] == "get_weather":
            print(f"  天气查询: {args['location']} → 晴, 25°C")
        elif tc["function_name"] == "calculate":
            result = eval(args["expression"])
            print(f"  计算: {args['expression']} = {result}")
else:
    print("\n[本次请求未触发函数调用]")
