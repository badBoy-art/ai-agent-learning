# model_manager.py — 模型管理器：注册、切换、列表展示

from llm_client import LLMClientFactory


class ModelManager:
    """管理多个 LLM 模型"""

    def __init__(self):
        self.current_model = None   # 当前使用的模型
        self.current_key = None     # 当前模型 key
        self.models = {}            # 所有已注册模型: {key: LLMClient}

    def register(self, model_key: str) -> bool:
        """注册一个模型"""
        try:
            client = LLMClientFactory.create(model_key)
            self.models[model_key] = client
            return True
        except Exception as e:
            print(f"  [注册失败] {model_key}: {e}")
            return False

    def switch(self, model_key: str) -> bool:
        """切换到指定模型"""
        if model_key not in self.models:
            print(f"  模型 '{model_key}' 未注册")
            return False
        self.current_key = model_key
        self.current_model = self.models[model_key]
        info = self.current_model.get_model_info()
        print(f"  ✔ 已切换到: {info['name']} ({info['model']})")
        return True

    def get_current_model(self) -> str:
        """获取当前模型名称"""
        if self.current_model:
            return self.current_model.get_model_info()["name"]
        return "未选择"

    def list_models(self) -> list:
        """列出所有已注册的模型"""
        return [(key, client.get_model_info())
                for key, client in self.models.items()]

    def is_ready(self) -> bool:
        """检查是否已选择模型"""
        return self.current_model is not None
