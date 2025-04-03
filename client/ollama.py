import requests
import json
from copy import deepcopy
from .openai import MCPClientOpenAI, logger


class MCPClientLocalOllama(MCPClientOpenAI):
    """
    本地 Ollama 客户端，继承自 MCPClientOpenAI。
    提供与本地 Ollama 服务的交互功能。
    """

    @classmethod
    def info(cls):
        """
        返回客户端的基本信息。
        """
        return {
            "name": "LocalOllama",
            "description": "Local Ollama client",
            "version": "1.0.0",
        }

    @classmethod
    def default_config(cls):
        """
        返回默认配置。
        """
        return {
            "base_url": "http://localhost:11434",
            "api_key": "",
            "model": "llama3.2:3b",
        }

    def __init__(self, base_url="http://localhost:11434", api_key="ollama", model="", stream=True):
        """
        初始化本地 Ollama 客户端。 

        :param base_url: Ollama 服务的基本 URL。
        :param api_key: API 密钥。
        :param model: 模型名称。
        :param stream: 是否使用流式响应。
        """
        super().__init__(base_url, api_key=api_key, model=model, stream=stream)


    def response_raise_status(self, response: requests.Response):
        """
        检查响应状态，如果状态不为 200，则抛出异常。
        
        :param response: 响应对象。
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            try:
                json_data = response.json()
                error = json_data.get("error", "")
                if message := error.get("message", ""):
                    if "does not support tools" in message:
                        logger.error("当前模型不支持工具调用, 请更换模型")
                    raise Exception(message)
                print(json_data)
            except json.JSONDecodeError:
                raise
