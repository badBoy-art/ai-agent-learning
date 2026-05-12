# exercise1.py — 添加 Kimi 客户端
# 目标: 基于已有客户端模板，添加 Kimi (Moonshot) 支持
# 要求:
#   - 创建 clients/kimi_client.py（已提供）
#   - 在 config.py 中添加 Kimi 配置（已提供）
#   - 在工厂中注册 Kimi（已提供）
#   - 用 /switch kimi 切换测试
#
# 本练习: 通过 chat_bot.py 直接测试 Kimi

# 确保项目根目录在 Python 路径中
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clients.kimi_client import KimiClient
from config import MODELS


def test_kimi_direct():
    """直接测试 Kimi 客户端"""
    kimi_config = MODELS.get("kimi")
    if not kimi_config or not kimi_config["api_key"]:
        print("❌ Kimi 未配置 API Key。请在 .env 中设置 KIMI_API_KEY")
        print("   获取方式: https://platform.moonshot.cn/console/api-keys")
        return

    print(f"🔍 正在测试 Kimi...")
    client = KimiClient(kimi_config)
    info = client.get_model_info()
    print(f"   模型: {info['name']} ({info['model']})")

    # 测试非流式
    print("\n📨 非流式请求:")
    response = client.chat([
        {"role": "system", "content": "你是一个有用的助手。"},
        {"role": "user", "content": "请用一句话介绍你自己。"}
    ])
    print(f"   {response}")

    # 测试流式
    print("\n📡 流式请求:")
    print("   ", end="", flush=True)
    for chunk in client.chat_stream([
        {"role": "system", "content": "你是一个有用的助手。"},
        {"role": "user", "content": "请用 10 个字以内回答: 今天的天气怎么样？"}
    ]):
        print(chunk, end="", flush=True)
    print()


if __name__ == "__main__":
    test_kimi_direct()
