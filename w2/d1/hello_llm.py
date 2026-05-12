import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

# DeepSeek API 配置 - 从环境变量读取
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)


def chat(message):
    response = client.chat.completions.create(
        model="deepseek-chat",  # DeepSeek 模型名称
        messages=[
            {"role": "system", "content": "你是一个有用的助手"},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
        max_tokens=500
    )
    # 打印回复
    print("AI回复:", response.choices[0].message.content)

    # 查看完整响应结构
    print("\n完整响应结构:")
    print(f"ID: {response.id}")
    print(f"模型: {response.model}")
    print(f"创建时间: {response.created}")
    print(f"使用token数: {response.usage.total_tokens}")
    return response.choices[0].message.content


# 测试
if __name__ == "__main__":
    print("=== 第一个 LLM 程序 ===\n")

    question = "你好，请介绍一下你自己"
    print(f"用户: {question}")
    answer = chat(question)
    print(f"AI: {answer}")
