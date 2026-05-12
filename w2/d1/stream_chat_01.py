import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()


class ChatBot:
    def __init__(self, api_key, base_url="https://api.deepseek.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.messages = [
            {"role": "system", "content": "你是一个有帮助的助手"}
        ]

    def chat(self, user_input):
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})

        # 调用API
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            temperature=0.7,
            max_tokens=500
        )

        # 获取AI回复
        ai_reply = response.choices[0].message.content

        # 添加AI回复到历史
        self.messages.append({"role": "assistant", "content": ai_reply})

        return ai_reply

    def get_history(self):
        """获取对话历史"""
        return self.messages

    def clear_history(self):
        """清空对话历史"""
        self.messages = [
            {"role": "system", "content": "你是一个有帮助的助手"}
        ]


# 使用示例
bot = ChatBot(api_key=os.getenv("DEEPSEEK_API_KEY"))
print(bot.chat("你好"))
print(bot.chat("刚才我们说了什么？"))  # AI会记住上下文


# 带token限制的对话历史
class SmartChatBot(ChatBot):
    def __init__(self, api_key, max_history_tokens=2000):
        super().__init__(api_key)
        self.max_history_tokens = max_history_tokens

    def _trim_history(self):
        """如果历史太长，保留最重要的部分"""
        if len(self.messages) > 10:  # 简单策略：最多保留10轮
            # 保留系统消息和最近9轮对话
            self.messages = [self.messages[0]] + self.messages[-9:]
