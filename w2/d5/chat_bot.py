# chat_bot.py — 多模型聊天机器人（彩色终端版）
# 命令: /switch, /models, /clear, /help, /exit, /save, /load

import sys
import os

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import MODELS
from model_manager import ModelManager
from chat_session import ChatSession

# ANSI 颜色 —— 终端彩色输出
class Colors:
    CYAN = "\033[96m"       # 系统消息
    GREEN = "\033[92m"      # 用户消息
    YELLOW = "\033[93m"     # 助手消息
    RED = "\033[91m"        # 错误
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_header(model_name: str):
    """打印聊天窗口标题"""
    os.system("clear")  # macOS/Linux
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 60)
    print(f"         🤖 多模型聊天机器人")
    print(f"         当前模型: {model_name}")
    print("=" * 60)
    print(f"{Colors.RESET}")
    print(f"  命令: /switch <模型>  /models  /clear  /help  /exit  /save  /load")
    print()


def print_help():
    """打印帮助信息"""
    print(f"{Colors.CYAN}可用命令:{Colors.RESET}")
    print(f"  /switch <模型>  — 切换模型 (deepseek/qwen/glm/kimi)")
    print(f"  /models         — 列出所有可用模型")
    print(f"  /clear          — 清空当前对话历史")
    print(f"  /save [文件名]  — 保存对话到文件")
    print(f"  /load <文件名>  — 加载对话文件")
    print(f"  /help           — 显示此帮助")
    print(f"  /exit           — 退出程序")
    print()


def main():
    # ---------- 初始化 ----------
    manager = ModelManager()
    session = ChatSession("你是一个有帮助的 AI 助手，请用中文回答。")

    # 注册可用模型
    print(f"{Colors.YELLOW}正在注册模型...{Colors.RESET}")
    for key in ["deepseek", "qwen", "glm", "kimi"]:
        if MODELS.get(key, {}).get("api_key"):
            manager.register(key)
            print(f"  ✔ {MODELS[key]['name']} — 已注册")

    # 默认选择第一个可用的模型
    switched = False
    for key in ["deepseek", "qwen", "glm", "kimi"]:
        if manager.switch(key):
            switched = True
            break

    if not switched:
        print(f"{Colors.RED}错误: 没有可用的模型！请检查 API Key 配置{Colors.RESET}")
        sys.exit(1)

    print_header(manager.get_current_model())

    while True:
        # 显示用户输入提示
        try:
            user_input = input(f"\n{Colors.GREEN}你{Colors.RESET} > ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.YELLOW}再见！{Colors.RESET}")
            break

        if not user_input:
            continue

        # ──── 命令处理 ────
        if user_input.startswith("/"):
            parts = user_input.split()
            cmd = parts[0].lower()

            if cmd == "/exit":
                print(f"{Colors.YELLOW}再见！{Colors.RESET}")
                break

            elif cmd == "/models":
                print(f"\n{Colors.CYAN}可用模型:{Colors.RESET}")
                for key, info in manager.list_models():
                    current = " ← 当前" if key == manager.current_key else ""
                    print(f"  {key:12} — {info['name']}{current}")
                continue

            elif cmd == "/switch":
                if len(parts) < 2:
                    print(f"{Colors.RED}用法: /switch <模型名>{Colors.RESET}")
                    print(f"  可用: deepseek, qwen, glm, kimi")
                    continue
                model_key = parts[1]
                if manager.switch(model_key):
                    print_header(manager.get_current_model())
                continue

            elif cmd == "/clear":
                session.clear()
                print(f"{Colors.CYAN}对话已清空{Colors.RESET}")
                continue

            elif cmd == "/help":
                print_help()
                continue

            elif cmd == "/save":
                save_dir = os.path.join(os.path.dirname(__file__), "sessions")
                os.makedirs(save_dir, exist_ok=True)
                filename = parts[1] if len(parts) > 1 else \
                    f"chat_{session.created_at.strftime('%Y%m%d_%H%M%S')}.json"
                filepath = os.path.join(save_dir, filename)
                session.save(filepath)
                continue

            elif cmd == "/load":
                if len(parts) < 2:
                    print(f"{Colors.RED}用法: /load <文件名>{Colors.RESET}")
                    continue
                save_dir = os.path.join(os.path.dirname(__file__), "sessions")
                filepath = os.path.join(save_dir, parts[1])
                if not os.path.exists(filepath):
                    print(f"{Colors.RED}文件不存在: {filepath}{Colors.RESET}")
                    continue
                session = ChatSession.load(filepath)
                print(f"{Colors.CYAN}对话已加载（{len(session.get_messages())} 条消息）{Colors.RESET}")
                # 回显最近的对话
                for msg in session.get_messages()[-6:]:
                    role = "你" if msg["role"] == "user" else \
                           "AI" if msg["role"] == "assistant" else "系统"
                    color = Colors.GREEN if msg["role"] == "user" else Colors.YELLOW
                    content_preview = msg["content"][:80] + "..." if len(msg["content"]) > 80 else msg["content"]
                    print(f"  {color}{role}: {content_preview}{Colors.RESET}")
                continue

            else:
                print(f"未知命令: {cmd}   输入 /help 查看可用命令")
                continue

        # ──── 发送消息给 LLM ────
        session.add_user_message(user_input)

        if not manager.is_ready():
            print(f"{Colors.RED}错误: 未选择模型{Colors.RESET}")
            continue

        print(f"\n{Colors.YELLOW}{manager.get_current_model()}{Colors.RESET} > ", end="", flush=True)

        try:
            full_response = ""
            # 流式输出
            for chunk in manager.current_model.chat_stream(session.get_messages()):
                print(chunk, end="", flush=True)
                full_response += chunk
            print()  # 换行

            session.add_assistant_message(full_response)

        except Exception as e:
            print(f"\n{Colors.RED}请求出错: {e}{Colors.RESET}")
            # 移除刚才添加的用户消息（避免污染对话历史）
            session.messages.pop()


if __name__ == "__main__":
    main()
