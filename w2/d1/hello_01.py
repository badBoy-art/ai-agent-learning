# 控制参数
# temperature
# - 范围: 0.0 ~ 2.0
# - 作用: 控制输出的随机性
# - 推荐值:
# * 0.0: 确定性输出，适合代码生成、事实回答
# * 0.7: 平衡的创造性，适合一般对话
# * 1.0: 较高的创造性，适合创意写作
# frequency_penalty=0.0,  # 频率惩罚，减少重复
# presence_penalty=0.0,   # 存在惩罚，鼓励新话题
# stop=["\n\n", "###"],   # 停止序列
# n=1,                   # 生成几个回复
# top_p=0.95,   核采样，与temperature二选一
# # 流式输出
# stream=False,          # 是否流式输出

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
        messages=[{"role": "user", "content": "写一句关于春天的诗"}],
        temperature=1,
        max_tokens=500  # 最大输出长度

    )
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

    question = "帮忙写首古诗"
    print(f"用户: {question}")
    answer = chat(question)
    print(f"AI: {answer}")
