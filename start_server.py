from server.server import Server
from server.tools.common_tools import CommonTools
from logger import getLogger

logger = getLogger("MCPServer_1111")


if __name__ == "__main__":
    # 创建 Server 实例
    server = Server(name="MCPServer_11111", host="localhost", port=45677)

    # 获取 CommonTools 中的所有工具
    tools = CommonTools.get_all_tools()

    # 注册工具
    server.register_tools(tools)

    # 启动服务器
    server.run(block=True)