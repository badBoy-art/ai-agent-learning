"""
练习 4: 流式 + 保存历史
目标: 流式对话 + 保存/加载历史记录
要求: 支持 save/load/clear 命令
"""
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)
MODEL = "deepseek-chat"

SAVE_DIR = os.path.join(os.path.dirname(__file__), "sessions")
os.makedirs(SAVE_DIR, exist_ok=True)

messages = [
    {"role": "system", "content": "你是一个有帮助的 AI 助手，请用中文回答。"}
]


def stream_chat(messages):
    """流式对话，返回完整响应"""
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )
    full_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
            full_response += delta.content
    return full_response


def save_history(messages, filename=None):
    """保存对话历史到文件"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{timestamp}.json"
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    print(f"\n  ✓ 已保存到: {filepath}")
    return filepath


def load_history(filename):
    """从文件加载对话历史"""
    filepath = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"\n  ✗ 文件不存在: {filepath}")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def list_sessions():
    """列出所有保存的对话"""
    files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
    if not files:
        print("  暂无保存的对话")
        return
    print(f"\n  已保存的对话 ({len(files)}):")
    for f in sorted(files, reverse=True)[:10]:
        size = os.path.getsize(os.path.join(SAVE_DIR, f))
        print(f"    • {f} ({size} bytes)")


print("=== 流式对话（支持命令: /save /load /list /clear /exit）===")
print(f"  保存目录: {SAVE_DIR}\n")

while True:
    user_input = input("你 > ").strip()
    if not user_input:
        continue

    # ── 命令处理 ──
    if user_input.startswith("/"):
        cmd = user_input[1:].split()
        action = cmd[0].lower()

        if action == "exit":
            print("再见！")
            break

        elif action == "save":
            filename = cmd[1] if len(cmd) > 1 else None
            save_history(messages, filename)
            continue

        elif action == "list":
            list_sessions()
            continue

        elif action == "load":
            if len(cmd) < 2:
                print("  用法: /load <文件名>")
                continue
            loaded = load_history(cmd[1])
            if loaded:
                messages = loaded
                print(f"  ✓ 已加载 {len(messages)} 条消息")
                # 显示最近的对话
                for msg in messages[-4:]:
                    role = "你" if msg["role"] == "user" else "AI"
                    preview = msg["content"][:60] + "..." if len(msg["content"]) > 60 else msg["content"]
                    print(f"    {role}: {preview}")
            continue

        elif action == "clear":
            system = messages[0]
            messages = [system]
            print("  ✓ 对话已清空")
            continue

        else:
            print(f"  未知命令: /{action}  (可用: save, load, list, clear, exit)")
            continue

    # ── 正常对话 ──
    messages.append({"role": "user", "content": user_input})
    print("AI > ", end="", flush=True)
    full_response = stream_chat(messages)
    print()  # 换行
    messages.append({"role": "assistant", "content": full_response})
    print(f"  [共 {len(messages)} 条消息]")
