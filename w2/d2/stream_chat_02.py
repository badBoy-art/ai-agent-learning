# 四、完整流式对话系统

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)

MODEL = "deepseek-chat"


def chat_stream():
    """带流式输出的多轮对话"""
    messages = [{"role": "system", "content": "你是一个有用的助手"}]

    print("=" * 50)
    print("流式对话系统 (输入 quit 退出)")
    print("=" * 50)

    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("再见！")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        # 流式调用
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )

        full_response = ""
        print("AI: ", end="", flush=True)

        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                print(content, end="", flush=True)

        print()  # 换行

        # 保存完整响应到对话历史
        messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    chat_stream()


