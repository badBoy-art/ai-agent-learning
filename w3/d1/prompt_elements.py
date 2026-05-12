# 1. 角色 (Role)
# 定义 AI 的身份和知识范围
# "你是一名 Python 后端开发专家"
#
# 2. 任务 (Task)
# AI 需要完成的具体工作
# "审查以下代码，找出潜在的性能问题"
#
# 3. 上下文 (Context)
# AI 回答问题所需的背景信息
# "这是一个电商系统的订单模块，用户量 100 万"
#
# 4. 格式 (Format)
# AI 输出的具体格式要求
# "用 markdown 表格列出：函数名 | 问题 | 优化建议"

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"


def structured_prompt(role, task, context, format_req, question):
    """构建结构化 Prompt"""
    prompt = f"""{role}

{task}

背景信息:
{context}

{format_req}

问题: {question}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# 使用
result = structured_prompt(
    role="你是一名资深 Java 架构师，擅长性能优化。",
    task="分析以下代码的性能问题，并给出优化建议。",
    context="这是一个用户登录接口，QPS 峰值约 5000。",
    format_req="用表格列出：问题 | 影响 | 优化方案 | 优先级(P0-P2)",
    question="""
    public User login(String username, String password) {
        String sql = "SELECT * FROM users WHERE username='" + username + "'";
        // ...
    }
    """
)
print(result)
