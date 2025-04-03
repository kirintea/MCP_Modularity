from client.siliconflow import MCPClientSiliconflow

LLM_QUESTION_URL_CONFIG = "https://api.siliconflow.cn"
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
API_KEY = "sk-rmprjadkeedwjibjztyjzwmzxmvzmyjspvlwhpkwgqujzdjs"

def create_client_instance(mcp_url: str, llm_api_url: str, llm_api_key: str, llm_model: str, llm_stream: bool) -> MCPClientSiliconflow:
    """
    创建并初始化MCP客户端实例
    """
    # 创建客户端实例并初始化配置
    client = MCPClientSiliconflow()
    
    client.base_url = llm_api_url  # LLM API的URL
    client.api_key = llm_api_key  # LLM的API密钥
    client.model = llm_model  # LLM的模型名称
    client.stream = llm_stream  # 是否启用流式传输
    client.mcp_url = mcp_url  # MCP服务器的URL
    return client

def main():
    # 定义客户端连接参数
    config = {
        "mcp_url": "http://localhost:45677/sse",  # MCP服务器的URL
        "llm_api_url": LLM_QUESTION_URL_CONFIG,  # LLM的API URL
        "llm_api_key": API_KEY,  # LLM的API密钥
        "llm_model": MODEL_NAME,  # LLM的模型名称
        "llm_stream": True  # 是否启用流式传输
    }

    # 创建客户端实例
    client = create_client_instance(
        config["mcp_url"],
        config["llm_api_url"],
        config["llm_api_key"],
        config["llm_model"],
        config["llm_stream"],
    )

    # 启动客户端
    MCPClientSiliconflow.try_start_client()

    # 提供交互式命令行
    print("客户端已启动，输入 'exit' 退出程序。")
    while True:
        command = input(">>> ")  # 等待用户输入
        if command.strip().lower() == "exit":
            print("正在退出客户端...")
            MCPClientSiliconflow.stop_client()
            break
        else:
            # 处理命令
            client.command_queue.put(command)

if __name__ == "__main__":
    main()