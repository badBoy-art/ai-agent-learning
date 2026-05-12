"""
练习 3: 角色扮演生成器
目标: 用户输入场景，AI 自动生成角色定义，然后用该角色回答问题
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


def generate_role(scenario: str) -> str:
    """根据场景生成角色定义"""
    system_prompt = """你是角色设计专家。根据用户输入的场景，生成一个角色定义。
返回 JSON 格式：
{
    "name": "角色名",
    "identity": "身份描述",
    "knowledge_scope": "知识范围",
    "tone": "语气风格",
    "constraints": ["行为约束1", "行为约束2", "行为约束3"]
}
只返回 JSON，不要多余文字。"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"场景: {scenario}\n请为此场景设计一个 AI 角色。"}
        ]
    )
    return response.choices[0].message.content


def ask_with_role(role_json: str, question: str) -> str:
    """用指定的角色定义去回答问题"""
    import json
    try:
        role = json.loads(role_json)
        system_prompt = f"""你是{role.get('name', '助手')}。
{role.get('identity', '')}

知识范围: {role.get('knowledge_scope', '不限')}
语气: {role.get('tone', '专业')}
约束:
{chr(10).join('- ' + c for c in role.get('constraints', []))}"""
    except json.JSONDecodeError:
        system_prompt = f"请你扮演一个与以下场景匹配的角色:\n{role_json}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    scenario = input("请输入场景（例如「我想学习微积分」）: ").strip()
    if not scenario:
        scenario = "我想学习微积分"

    print(f"\n场景: {scenario}")
    print("正在生成角色...\n")
    role_json = generate_role(scenario)
    print("=== 生成的角色 ===")
    print(role_json)

    print("\n=== 用该角色回答问题 ===")
    question = input("\n请输入你想问的问题: ").strip()
    if not question:
        question = "导数的基本定义是什么？"
    answer = ask_with_role(role_json, question)
    print(f"\n回答: {answer}")
