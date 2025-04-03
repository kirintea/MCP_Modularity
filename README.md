# MCP_Modularity 项目 README

## 项目概述
MCP_Modularity 是一个用于与多个大语言模型（LLM）进行交互的客户端项目。该项目支持多种 LLM 服务，包括 OpenAI、OpenRouter、DeepSeek、Siliconflow、Ollama、Claude 等，提供了统一的接口来处理用户查询和工具调用。

## 功能特性
- **多模型支持**：支持多种大语言模型，如 OpenAI、OpenRouter、DeepSeek 等。
- **工具调用**：允许模型调用预定义的工具来解决用户的问题。
- **流式响应**：支持流式响应，提供实时交互体验。
- **配置管理**：可以通过配置文件或代码设置模型的基本 URL、API 密钥、模型名称等参数。

## 目录结构
```
MCP_Modularity/
├── client/
│   ├── __init__.py
│   ├── base.py
│   ├── openai.py
│   ├── deepseek.py
│   ├── siliconflow.py
│   ├── ollama.py
│   ├── claude.py
│   └── ...
├── server/
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── common.py
│   │   ├── common_tools.py
│   │   └── modifier_tools.py
├── test/
│   └── test_llm_api.py
├── __init__.py
├── start_client.py
└── logger.py
```

## 安装依赖
确保你已经安装了 Python 3.x，然后使用以下命令安装项目依赖：
```bash
pip install -r requirements.txt
```
由于没有提供 `requirements.txt` 文件，你需要根据代码中的 `import` 语句手动安装依赖，主要依赖包括：
- `requests`
- `asyncio`
- `dataclasses`
- `json`
- `re`
- `queue`
- `threading`
- `contextlib`
- `mcp`（需要确保该库已正确安装）

## 配置信息
在 `start_client.py` 文件中，你可以配置客户端连接参数：
```python
config = {
    "mcp_url": "http://localhost:45677/sse",  # MCP服务器的URL
    "llm_api_url": LLM_QUESTION_URL_CONFIG,  # LLM的API URL
    "llm_api_key": API_KEY,  # LLM的API密钥
    "llm_model": MODEL_NAME,  # LLM的模型名称
    "llm_stream": True  # 是否启用流式传输
}
```

## 启动客户端
运行以下命令启动客户端：
```bash
python start_client.py
```
启动后，你可以在命令行中输入查询语句，输入 `exit` 退出程序。

## 代码说明
### 客户端类
- `MCPClientBase`：所有客户端类的基类，提供了基本的客户端功能，如连接服务器、处理查询、调用工具等。
- `MCPClientOpenAI`：与 OpenAI 兼容的客户端类，继承自 `MCPClientBase`。
- `MCPClientDeepSeek`、`MCPClientSiliconflow`、`MCPClientLocalOllama`、`MCPClientClaude`、`MCPClientOpenRouter`：分别是与 DeepSeek、Siliconflow、Ollama、Claude、OpenRouter 对应的客户端类，继承自 `MCPClientOpenAI`。

### 工具包
- `ModifierTools`：修改器工具包，继承自 `ToolsPackageBase`。

### 测试代码
- `test_llm_api.py`：包含一个简单的测试函数 `chat_completions`，用于测试 LLM 的聊天完成功能。

## 注意事项
- 确保你已经正确配置了 LLM 的 API 密钥和基本 URL。
- 某些模型可能不支持工具调用，当遇到不支持的情况时，会在日志中输出相应的错误信息。

## 贡献与反馈
如果你有任何问题、建议或想要贡献代码，请在项目的 GitHub 仓库中提交 issue 或 pull request。