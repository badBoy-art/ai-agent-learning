from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"


def zero_shot(prompt: str) -> str:
    """直接提问，零样本"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ── 对比测试 ──
bad_prompt = "翻译"
good_prompt = "请将以下英文翻译成中文，只返回翻译结果：\n\nHello, how are you?"

print("=== 差 Prompt ===")
print(f"输入: {bad_prompt}")
print(f"输出: {zero_shot(bad_prompt)}")

print("\n=== 好 Prompt ===")
print(f"输入: {good_prompt}")
print(f"输出: {zero_shot(good_prompt)}")
