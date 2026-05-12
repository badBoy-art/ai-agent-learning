"""
练习 2: 多工具助手
目标: 实现 3 个工具 — get_weather, calculate, get_current_time
要求: 一次提问触发多个工具，执行结果回传给 LLM 生成自然语言回复
"""
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import pytz

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"


# ============================================================
# 1. 定义工具函数（本地真实执行）
# ============================================================

def get_weather(location: str) -> str:
    """获取指定城市的天气"""
    weather_data = {
        "北京": {"temperature": 22, "condition": "晴", "humidity": 30},
        "上海": {"temperature": 25, "condition": "多云", "humidity": 65},
        "广州": {"temperature": 30, "condition": "阵雨", "humidity": 80},
        "深圳": {"temperature": 28, "condition": "阴", "humidity": 75},
        "成都": {"temperature": 20, "condition": "小雨", "humidity": 85},
        "杭州": {"temperature": 24, "condition": "晴", "humidity": 55},
        "武汉": {"temperature": 26, "condition": "多云", "humidity": 60},
    }
    info = weather_data.get(location, {"temperature": "N/A", "condition": "未知", "humidity": "N/A"})
    return json.dumps(info, ensure_ascii=False)


def calculate(expression: str) -> str:
    """执行数学计算"""
    try:
        # 安全计算 — 仅允许数学运算
        allowed = set("0123456789+-*/.()% ")
        if not all(c in allowed for c in expression):
            return json.dumps({"error": "表达式包含非法字符"})
        result = eval(expression)
        return json.dumps({"expression": expression, "result": result})
    except Exception as e:
        return json.dumps({"expression": expression, "error": str(e)})


def get_current_time(timezone: str) -> str:
    """获取指定时区的当前时间"""
    timezone_map = {
        "北京": "Asia/Shanghai",
        "上海": "Asia/Shanghai",
        "东京": "Asia/Tokyo",
        "纽约": "America/New_York",
        "伦敦": "Europe/London",
        "巴黎": "Europe/Paris",
        "悉尼": "Australia/Sydney",
        "旧金山": "America/Los_Angeles",
        "莫斯科": "Europe/Moscow",
        "迪拜": "Asia/Dubai",
    }
    tz_name = timezone_map.get(timezone, timezone)
    try:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        return json.dumps({
            "timezone": timezone,
            "local_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "utc_offset": str(now.utcoffset())
        }, ensure_ascii=False)
    except Exception:
        return json.dumps({"timezone": timezone, "error": f"未知时区: {timezone}"})


# ============================================================
# 2. 工具描述（给 LLM 看的说明书）
# ============================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息，支持北京、上海、广州、深圳、成都等城市",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名，例如：北京、上海、广州"
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
            "description": "执行数学计算，支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，例如：25*4+10, (100-20)/8"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取指定城市或时区的当前时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "城市名或时区名，例如：北京、纽约、伦敦、Tokyo"
                    }
                },
                "required": ["timezone"]
            }
        }
    }
]

# ============================================================
# 3. 工具路由（收到指令 → 执行对应函数）
# ============================================================

FUNCTIONS = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_current_time": get_current_time,
}


def execute_tool_calls(tool_calls):
    """执行 LLM 请求的所有工具调用，返回结果列表"""
    results = []
    for tc in tool_calls:
        func_name = tc.function.name
        args = json.loads(tc.function.arguments)
        print(f"  → 调用工具: {func_name}({args})")

        func = FUNCTIONS.get(func_name)
        if func:
            result = func(**args)
        else:
            result = json.dumps({"error": f"未知工具: {func_name}"})

        results.append({
            "tool_call_id": tc.id,
            "role": "tool",
            "content": result
        })
        print(f"  ← 结果: {result}")
    return results


# ============================================================
# 4. 一次提问，触发多个工具
# ============================================================

print("=== 多工具助手 ===\n")

# 提问包含了天气+计算+时间，会触发多个工具调用
user_question = (
    "给我查一下以下信息：\n"
    "1. 北京的天气怎么样？\n"
    "2. 25*4+10 等于多少？\n"
    "3. 现在纽约是几点？"
)

messages = [
    {"role": "system", "content": "你是一个有用的工具助手，根据工具调用结果用中文回答用户。"},
    {"role": "user", "content": user_question}
]

print(f"用户: {user_question}\n")

# 第一轮：LLM 决定调哪些工具
print("--- 第一轮: LLM 决定工具调用 ---")
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools
)

assistant_msg = response.choices[0].message

if assistant_msg.tool_calls:
    print(f"LLM 请求调用 {len(assistant_msg.tool_calls)} 个工具:\n")

    # 执行所有工具
    tool_results = execute_tool_calls(assistant_msg.tool_calls)

    # 把工具结果回传给 LLM
    messages.append(assistant_msg)
    messages.extend(tool_results)

    # 第二轮：LLM 根据工具结果生成自然语言回复
    print("\n--- 第二轮: LLM 生成最终回答 ---")
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )
    print(f"\nAI: {final_response.choices[0].message.content}")

else:
    print(f"AI: {assistant_msg.content}")
