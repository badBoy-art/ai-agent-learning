#
from openai import OpenAI
import json

# DeepSeek API 配置
client = OpenAI(
    api_key="***",
    base_url="https://api.deepseek.com"
)


# 定义工具函数
def get_weather(location):
    weather_data = {
        "北京": {"temp": 25, "condition": "晴"},
        "上海": {"temp": 28, "condition": "多云"}
    }
    return weather_data.get(location, {"temp": 20, "condition": "未知"})


# 定义工具描述
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "城市名称"}
            },
            "required": ["location"]
        }
    }
}]

# 调用
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "北京天气怎么样"}],
    tools=tools
)

print(response.choices[0].message)
