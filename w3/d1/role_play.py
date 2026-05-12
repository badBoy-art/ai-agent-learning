# 5.1 什么是角色扮演？
#
# 给 LLM 分配一个"身份"，让它以该身份的语气、知识范围、行为模式来回答。
#
# 核心：system prompt 中定义角色。
#
# 公式: system(角色定义) + user(问题)
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"


def role_play(system_prompt: str, question: str) -> str:
    """角色扮演对话"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


# ── 不同角色对比 ──
roles = {
    "老师": "你是一名小学语文老师，用简单易懂的语言和比喻解释问题。",
    "科学家": "你是一名物理学家，用专业术语和公式解释问题，引用科学原理。",
    "诗人": "你是一名古代诗人，用诗意的语言回答，说话押韵有韵律。",
}

question = "请解释一下：为什么天上的星星会发光？"

for role_name, system_prompt in roles.items():
    print(f"\n{'=' * 50}")
    print(f"角色: {role_name}")
    print(f"{'=' * 50}")
    result = role_play(system_prompt, question)
    print(f"回答: {result}")
