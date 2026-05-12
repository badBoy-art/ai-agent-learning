# exercise3.py — 对话对比模式
# 目标: 用一个问题同时询问多个模型，对比回复效果
# 要求:
#   - 添加 /compare <问题> 命令
#   - 依次询问所有已注册的模型
#   - 显示模型名称 + 回复 + 回复长度

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import MODELS
from model_manager import ModelManager
from chat_session import ChatSession


def compare_models(question: str):
    """用同一个问题询问所有已注册的模型"""
    manager = ModelManager()

    # 注册所有可用模型
    available_keys = []
    for key in ["deepseek", "qwen", "glm", "kimi"]:
        if MODELS.get(key, {}).get("api_key"):
            manager.register(key)
            available_keys.append(key)

    if not available_keys:
        print("❌ 没有可用的模型！请检查 API Key 配置")
        return

    print(f"\n📋 对比问题: \"{question}\"")
    print("=" * 60)

    for key in available_keys:
        manager.switch(key)
        info = manager.current_model.get_model_info()
        print(f"\n🤖 {info['name']} ({info['model']})")
        print("-" * 40)

        try:
            full_response = ""
            for chunk in manager.current_model.chat_stream([
                {"role": "system", "content": "请用简洁的语言回答。"},
                {"role": "user", "content": question}
            ]):
                full_response += chunk

            # 显示回复（截断显示）
            print(f"  {full_response[:200]}", end="")
            if len(full_response) > 200:
                print("...")
            else:
                print()

            print(f"\n  📊 长度: {len(full_response)} 字符")

        except Exception as e:
            print(f"  ❌ 请求失败: {e}")

    print("\n" + "=" * 60)
    print("对比完成！")


def main():
    print(f"{'='*60}")
    print(f"  多模型对比工具")
    print(f"{'='*60}")
    print()
    print("请输入你要对比的问题，或输入 /exit 退出")
    print()

    while True:
        try:
            user_input = input("问题 > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue
        if user_input == "/exit":
            break

        compare_models(user_input)

    print("再见！")


if __name__ == "__main__":
    main()
