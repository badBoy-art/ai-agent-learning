"""
练习 1: Zero-shot 优化
目标: 写一个函数，能自动给用户的 Prompt 打分和优化建议
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"


def evaluate_prompt(user_prompt: str):
    """分析 Prompt 的 4 要素完整度，给出分数和改进建议"""
    system_prompt = """你是一个 Prompt 工程专家。请分析用户输入的 Prompt 是否包含以下 4 个要素：
1. 角色 (Role) — 是否指定了 AI 的身份
2. 任务 (Task) — 是否说明了 AI 要做什么
3. 上下文 (Context) — 是否提供了背景信息
4. 格式 (Format) — 是否指定了输出格式

对每个要素判断：有(25分) / 无(0分)
返回 JSON 格式: {
    "role": 25, "task": 25, "context": 25, "format": 25,
    "total_score": 100,
    "missing": ["缺少的要素列表"],
    "optimized_prompt": "优化后的完整 Prompt"
}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    test_prompt = "帮我写个 Python 程序"
    print(f"原始 Prompt: {test_prompt}\n")
    result = evaluate_prompt(test_prompt)
    print("评估结果:")
    print(result)
