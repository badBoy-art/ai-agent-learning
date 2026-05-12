from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"


def few_shot_classify(text: str) -> str:
    """用 Few-shot 做情感分类"""
    messages = [
        {"role": "system", "content": "你是一个情感分类器，只返回 '正面' 或 '负面' 或 '中性'。"},
        # ── 3 个示例 ──
        {"role": "user", "content": "这个产品太棒了，我非常喜欢！"},
        {"role": "assistant", "content": "正面"},
        {"role": "user", "content": "等了两个小时都没送到，差评。"},
        {"role": "assistant", "content": "负面"},
        {"role": "user", "content": "今天天气阴天，有点闷。"},
        {"role": "assistant", "content": "中性"},
        # ── 新输入 ──
        {"role": "user", "content": text}
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return response.choices[0].message.content


# 测试
tests = [
    "这家餐厅的服务态度特别好！",
    "电池用半小时就没电了，太失望了。",
    "今天去了趟超市，买了点菜。",
]

for t in tests:
    result = few_shot_classify(t)
    print(f"  [{result:4s}] {t}")
