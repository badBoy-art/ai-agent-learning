# exercise4.py — Token 消耗追踪
# 目标: 每次调用后显示 token 使用量
# 要求:
#   - 从响应中提取 usage 信息
#   - 显示 prompt_tokens / completion_tokens / total_tokens
#   - 累计统计总消耗
#   - 添加 /usage 命令查看统计

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import MODELS
from model_manager import ModelManager
from chat_session import ChatSession


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


class UsageTracker:
    """追踪和管理 API Token 使用统计"""

    def __init__(self):
        self.total_prompt = 0
        self.total_completion = 0
        self.total_tokens = 0
        self.request_count = 0

    def add(self, response) -> dict:
        """解析 API 响应中的 usage 信息并累加
        注意: 流式模式下 response 可能不含 usage，
        需要从非流式响应中提取。
        """
        usage = getattr(response, "usage", None) if hasattr(response, "usage") else None
        if usage:
            self.total_prompt += usage.prompt_tokens
            self.total_completion += usage.completion_tokens
            self.total_tokens += usage.total_tokens
            self.request_count += 1
            return {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            }
        return {}

    def add_estimate(self, prompt_chars: int, response_chars: int):
        """流式模式下没有 usage 信息，用字符数估算 token"""
        prompt_tokens = prompt_chars // 2  # 粗略：中文字≈2 tokens
        completion_tokens = response_chars // 2
        total = prompt_tokens + completion_tokens
        self.total_prompt += prompt_tokens
        self.total_completion += completion_tokens
        self.total_tokens += total
        self.request_count += 1
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total,
            "note": "估算值（流式模式）"
        }

    def summary(self) -> str:
        """返回使用统计摘要"""
        return (
            f"📊 Token 使用统计\n"
            f"{'='*40}\n"
            f"  请求次数:      {self.request_count} 次\n"
            f"  输入 Token:    {self.total_prompt:,}\n"
            f"  输出 Token:    {self.total_completion:,}\n"
            f"  总消耗:        {self.total_tokens:,}\n"
            f"{'='*40}\n"
            f"  DeepSeek 参考价: ¥{self.total_tokens * 0.000001:.4f}\n"
            f"  （按输入 ¥0.001/1K, 输出 ¥0.002/1K 估算）"
        )


def main():
    manager = ModelManager()
    session = ChatSession("你是一个有帮助的 AI 助手，请用中文回答。")
    tracker = UsageTracker()

    # 注册模型
    for key in ["deepseek", "qwen", "glm", "kimi"]:
        if MODELS.get(key, {}).get("api_key"):
            manager.register(key)

    if not manager.switch("deepseek"):
        for key in ["qwen", "glm", "kimi"]:
            if manager.switch(key):
                break
        else:
            print("❌ 没有可用的模型！")
            sys.exit(1)

    # 使用非流式请求以获得 usage 信息
    print(f"\n{Colors.CYAN}当前模型: {manager.get_current_model()}{Colors.RESET}")
    print(f"输入 /usage 查看消费统计，/exit 退出")
    print()

    while True:
        try:
            user_input = input(f"{Colors.GREEN}你{Colors.RESET} > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            cmd = user_input.split()[0].lower()

            if cmd == "/exit":
                break
            elif cmd == "/usage":
                print(f"\n{Colors.CYAN}{tracker.summary()}{Colors.RESET}")
                continue
            elif cmd == "/clear":
                session.clear()
                print("对话已清空")
                continue
            elif cmd == "/help":
                print("命令: /usage /clear /exit")
                continue
            else:
                print(f"未知命令: {cmd}")
                continue

        if not manager.is_ready():
            print("❌ 未选择模型")
            continue

        session.add_user_message(user_input)

        try:
            # 非流式请求 —— 才能拿到 usage
            response = manager.current_model.chat(session.get_messages(), stream=False)
            usage_info = tracker.add_estimate(len(user_input), len(response))
            print(f"\n{Colors.YELLOW}{manager.get_current_model()}{Colors.RESET} > {response}")

            session.add_assistant_message(response)

            # 显示本次消耗
            used = usage_info.get("total_tokens", "?")
            note = usage_info.get("note", "")
            print(f"{Colors.CYAN}  [本次消耗: {used} tokens{ ' (' + note + ')' if note else ''}]"
                  f"  累计: {tracker.total_tokens:,} tokens{Colors.RESET}")

        except Exception as e:
            print(f"\n{Colors.RED}请求出错: {e}{Colors.RESET}")
            session.messages.pop()

    # 退出时打印最终统计
    print(f"\n{Colors.YELLOW}{tracker.summary()}{Colors.RESET}")


if __name__ == "__main__":
    main()
