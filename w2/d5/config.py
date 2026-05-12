# config.py — 多模型聊天机器人配置文件
# 从 .env 加载 API Key，统一管理模型参数

from dotenv import load_dotenv
import os

load_dotenv()

# 模型配置
MODELS = {
    "deepseek": {
        "name": "DeepSeek Chat",
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
        "description": "DeepSeek V3 — 性价比极高"
    },
    "qwen": {
        "name": "通义千问",
        "api_key": os.getenv("QWEN_API_KEY"),
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
        "description": "阿里云通义千问 — 国内稳定快速"
    },
    "glm": {
        "name": "智谱 GLM",
        "api_key": os.getenv("GLM_API_KEY"),
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4-flash",
        "description": "智谱 GLM-4 — 中文能力优秀"
    },
    "kimi": {
        "name": "Kimi",
        "api_key": os.getenv("KIMI_API_KEY"),
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k",
        "description": "Moonshot Kimi — 长上下文支持"
    }
}


def list_models():
    """返回可用的模型列表（仅含已配置 API Key 的模型）"""
    available = []
    for key, config in MODELS.items():
        if config["api_key"]:
            available.append((key, config))
        else:
            print(f"  [跳过] {config['name']} — 未配置 API Key")
    return available
