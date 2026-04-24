from openai import OpenAI

# DeepSeek API 配置
client = OpenAI(
    api_key="***",
    base_url="https://api.deepseek.com"
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
    return response.choices[0].message.content


# 测试
if __name__ == "__main__":
    print("=== 第一个 LLM 程序 ===\n")

    question = "你好，请介绍一下你自己"
    print(f"用户: {question}")
    answer = chat(question)
    print(f"AI: {answer}")
