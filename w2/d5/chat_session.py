# chat_session.py — 对话历史管理

import json
import os
from datetime import datetime


class ChatSession:
    """管理单次对话的消息历史"""

    def __init__(self, system_prompt: str = "你是一个有用的助手"):
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_user_message(self, content: str):
        """添加用户消息"""
        self.messages.append({"role": "user", "content": content})
        self.updated_at = datetime.now()

    def add_assistant_message(self, content: str):
        """添加助手回复"""
        self.messages.append({"role": "assistant", "content": content})
        self.updated_at = datetime.now()

    def get_messages(self) -> list:
        """获取完整消息列表"""
        return self.messages

    def clear(self):
        """清空对话（保留 system prompt）"""
        system = self.messages[0]
        self.messages = [system]
        self.updated_at = datetime.now()

    def count_tokens(self) -> int:
        """粗略估算 token 数（中文≈2 tokens/字，英文≈1 token/词）"""
        total = 0
        for msg in self.messages:
            total += len(msg["content"]) * 2  # 粗略估算
        return total

    def update_system_prompt(self, new_prompt: str):
        """更新系统提示词"""
        self.messages[0] = {"role": "system", "content": new_prompt}
        self.updated_at = datetime.now()

    def save(self, filepath: str):
        """保存对话到文件"""
        data = {
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "messages": self.messages
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✔ 对话已保存到: {filepath}")

    @classmethod
    def load(cls, filepath: str) -> "ChatSession":
        """从文件加载对话"""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        session = cls(system_prompt="")
        session.messages = data["messages"]
        session.created_at = datetime.fromisoformat(data["created_at"])
        session.updated_at = datetime.fromisoformat(data["updated_at"])
        return session
