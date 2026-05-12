"""
练习 4: Prompt 模板系统
目标: 创建 3 个常用的 Prompt 模板，支持快速复用
"""

from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"


# ============= 模板定义 =============

TEMPLATES = {
    "code_review": {
        "name": "代码审查",
        "system": """你是一名字级高级程序员，擅长代码审查。
请按以下维度审查代码：
1. 正确性 — 代码逻辑是否有 Bug
2. 性能 — 是否存在性能问题
3. 可读性 — 命名、结构是否清晰
4. 安全性 — 是否有安全漏洞
5. 改进建议 — 具体的优化方案

输出格式：Markdown 列表，每条建议标注严重程度 [高/中/低]。"""
    },
    "translate": {
        "name": "翻译（中 ↔ 英）",
        "system": """你是一名专业翻译，精通中英文。
要求：
- 准确传达原文意思
- 符合目标语言表达习惯
- 保留专业术语
- 如果是技术文档，保持术语一致性

输出格式：先给出翻译结果，然后附上关键术语对照表。"""
    },
    "summarize": {
        "name": "文本总结",
        "system": """你是一个文本分析专家。
请对以下文本进行总结：
1. 核心观点（1-2句话）
2. 关键要点（3-5条）
3. 结论/建议

限制：如果原文超过 1000 字，先分段总结再合并。"""
    }
}


def use_template(template_name: str, content: str) -> str:
    """使用指定模板处理内容"""
    if template_name not in TEMPLATES:
        return f"错误: 未找到模板「{template_name}」，可用模板: {', '.join(TEMPLATES.keys())}"

    template = TEMPLATES[template_name]
    messages = [
        {"role": "system", "content": template["system"]},
        {"role": "user", "content": content}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return response.choices[0].message.content


def list_templates():
    """列出所有可用模板"""
    print("\n可用模板:")
    for key, t in TEMPLATES.items():
        print(f"  {key}: {t['name']}")
    print()


if __name__ == "__main__":
    list_templates()

    while True:
        print("\n" + "=" * 50)
        cmd = input("输入模板名(code_review / translate / summarize)，或 q 退出: ").strip().lower()

        if cmd == "q":
            break

        if cmd not in TEMPLATES:
            print(f"未知模板，可用: {', '.join(TEMPLATES.keys())}")
            continue

        print(f"\n选中的模板: {TEMPLATES[cmd]['name']}")
        print("输入要处理的内容（输入 --- 结束）:")

        lines = []
        while True:
            line = input()
            if line.strip() == "---":
                break
            lines.append(line)

        content = "\n".join(lines)
        if not content.strip():
            print("内容为空，跳过")
            continue

        print("\n正在处理...\n")
        result = use_template(cmd, content)
        print("=" * 50)
        print(result)
        print("=" * 50)
