# {
#     "type": "function",
#     "function": {
#         "name": "get_weather", 函数名（见名知意）
#         "description": "获取天气信息", 告诉 LLM 什么时候用
#         "parameters": { 参数定义 (JSON Schema)
#             "type": "object",
#             "properties": {
#                 "location": {
#                     "type": "string",
#                     "description": "城市名称" 参数说明越详细越好
#                 }
#             },
#             "required": [ 必填参数
#                 "location"
#             ]
#         }
#     }
# }

# 2.2 三种可能的响应
#
# 1. 直接回复文本       → LLM 认为不需要调用函数
# 2. 调用 1 个函数      → LLM 返回 tool_calls
# 3. 同时调用多个函数   → 并行调用多个工具
#
# 3.1定义工具和函数
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)

# ---- 1. 定义工具描述 ----
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，如 北京、上海"
                    }
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
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 2+3*4"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# ---- 2. 定义函数实现 ----
def get_weather(location):
    """模拟天气查询（实际项目中应调用天气 API）"""
    weather_db = {
        "北京": {"temp": 25, "condition": "晴"},
        "上海": {"temp": 28, "condition": "多云"},
        "广州": {"temp": 30, "condition": "阵雨"},
        "深圳": {"temp": 27, "condition": "多云"},
        "成都": {"temp": 22, "condition": "阴"}
    }
    data = weather_db.get(location, {"temp": 20, "condition": "未知"})
    return json.dumps(data, ensure_ascii=False)


def calculate(expression):
    """执行数学计算"""
    try:
        result = eval(expression)
        return json.dumps({"result": result, "expression": expression})
    except Exception as e:
        return json.dumps({"error": str(e)})


# 3.2基础调用：接收tool_calls

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "衡水天气怎么样？"}],
    tools=tools
)

message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(f"[LLM 决定调用] {name}({args})")
else:
    print(f"[AI 直接回复] {message.content}")


# 输出:[LLM 决定调用]get_weather({"location": "北京"})


# 3.3 完整交互：执行函数 + 回传结果

def execute_tool(tool_call):
    """根据 tool_call 执行对应函数"""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    if name == "get_weather":
        return get_weather(args["location"])
    elif name == "calculate":
        return calculate(args["expression"])
    else:
        return json.dumps({"error": f"未知函数: {name}"})


messages = [{"role": "user", "content": "北京的天气怎么样？25+30 等于多少？"}]

# 第一轮：发给 LLM
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools
)

message = response.choices[0].message
messages.append(message)  # 把 LLM 的回复追加到历史

if message.tool_calls:
    # 执行每个函数
    for tool_call in message.tool_calls:
        result = execute_tool(tool_call)
        # 把函数结果以 tool 角色返回
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })
        print(f"[工具] {tool_call.function.name}({tool_call.function.arguments}) = {result}")

    # 第二轮：把函数结果给 LLM，生成自然语言回复
    response2 = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )

    final = response2.choices[0].message
    print(f"[AI] {final.content}")
else:
    print(f"[AI] {message.content}")
