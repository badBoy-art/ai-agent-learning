# exercise2.py — 系统提示词定制（增强版聊天机器人）
# 目标: 让用户可以通过命令修改系统提示词
# 要求:
#   - 添加 /system <新的系统提示词> 命令
#   - 调用后更新 ChatSession 的 system prompt
#   - 打印当前系统提示词确认

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


def print_header(model_name: str):
    os.system("clear")
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 60)
    print(f"         🤖 多模型聊天机器人（增强版）")
    print(f"         当前模型: {model_name}")
    print("=" * 60)
    print(f"{Colors.RESET}")
    print(f"  命令: /switch <模型>  /system <提示词>  /models  /clear  /help  /exit")
    print()


def print_help():
    print(f"{Colors.CYAN}可用命令:{Colors.RESET}")
    print(f"  /switch <模型>    — 切换模型 (deepseek/qwen/glm/kimi)")
    print(f"  /system <提示词>  — 设置系统提示词")
    print(f"  /models           — 列出所有可用模型")
    print(f"  /clear            — 清空当前对话历史")
    print(f"  /help             — 显示此帮助")
    print(f"  /exit             — 退出程序")
    print()


def main():
    manager = ModelManager()
    session = ChatSession()

    # 注册模型
    for key in ["deepseek", "qwen", "glm", "kimi"]:
        if MODELS.get(key, {}).get("api_key"):
            manager.register(key)

    if not manager.switch("deepseek"):
        for key in ["qwen", "glm"]:
            if manager.switch(key):
                break
        else:
            print("❌ 没有可用的模型！")
            sys.exit(1)

    print_header(manager.get_current_model())

    while True:
        try:
            user_input = input(f"\n{Colors.GREEN}你{Colors.RESET} > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            parts = user_input.split()
            cmd = parts[0].lower()

            if cmd == "/exit":
                break

            elif cmd == "/system":
                system_prompt = " ".join(parts[1:]) if len(parts) > 1 else "你是一个有用的助手"
                session.update_system_prompt(system_prompt)
                print(f"{Colors.CYAN}✔ 系统提示词已更新: \"{system_prompt}\"{Colors.RESET}")
                continue

            elif cmd == "/switch":
                if len(parts) < 2:
                    print(f"用法: /switch <模型名>")
                    continue
                if manager.switch(parts[1]):
                    print_header(manager.get_current_model())
                continue

            elif cmd == "/models":
                for key, info in manager.list_models():
                    mark = " ← 当前" if key == manager.current_key else ""
                    print(f"  {key:12} — {info['name']}{mark}")
                continue

            elif cmd == "/clear":
                session.clear()
                print(f"{Colors.CYAN}对话已清空{Colors.RESET}")
                continue

            elif cmd == "/help":
                print_help()
                continue
            else:
                print(f"未知命令: {cmd}")
                continue

        if not manager.is_ready():
            print("❌ 未选择模型")
            continue

        session.add_user_message(user_input)
        print(f"\n{Colors.YELLOW}{manager.get_current_model()}{Colors.RESET} > ", end="", flush=True)

        try:
            full_response = ""
            for chunk in manager.current_model.chat_stream(session.get_messages()):
                print(chunk, end="", flush=True)
                full_response += chunk
            print()
            session.add_assistant_message(full_response)
        except Exception as e:
            print(f"\n{Colors.RED}请求出错: {e}{Colors.RESET}")
            session.messages.pop()


if __name__ == "__main__":
    main()
