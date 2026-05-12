# clients/glm_client.py — 智谱 GLM API 客户端（OpenAI 兼容格式）

from w2.d5.llm_client import LLMClient


class GLMClient(LLMClient):
    """智谱 GLM API 客户端"""

    def chat(self, messages: list, stream: bool = False):
        response = self.client.chat.completions.create(
            model=self.config["model"],
            messages=messages,
            stream=stream
        )
        if not stream:
            return response.choices[0].message.content
        return response

    def chat_stream(self, messages: list):
        response = self.client.chat.completions.create(
            model=self.config["model"],
            messages=messages,
            stream=True
        )
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content
