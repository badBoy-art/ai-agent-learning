# llm_client.py — LLM 客户端抽象基类 + 工厂模式

from abc import ABC, abstractmethod
from openai import OpenAI


class LLMClient(ABC):
    """LLM 客户端抽象基类"""

    def __init__(self, config: dict):
        self.config = config
        self.client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )

    @abstractmethod
    def chat(self, messages: list, stream: bool = False):
        """发送聊天请求（子类实现）"""
        pass

    @abstractmethod
    def chat_stream(self, messages: list):
        """流式聊天（子类实现）"""
        pass

    def get_model_info(self) -> dict:
        """返回模型信息"""
        return {
            "name": self.config["name"],
            "model": self.config["model"],
            "description": self.config.get("description", "")
        }


class LLMClientFactory:
    """工厂：根据模型名称创建对应的客户端实例"""

    @staticmethod
    def create(model_key: str) -> LLMClient:
        from clients.deepseek_client import DeepSeekClient
        from clients.qwen_client import QwenClient
        from clients.glm_client import GLMClient
        from clients.kimi_client import KimiClient

        registry = {
            "deepseek": DeepSeekClient,
            "qwen": QwenClient,
            "glm": GLMClient,
            "kimi": KimiClient,
        }
        from config import MODELS
        client_class = registry.get(model_key)
        if not client_class:
            raise ValueError(f"不支持的模型: {model_key}")
        return client_class(MODELS[model_key])
