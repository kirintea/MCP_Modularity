import re
import asyncio

from functools import update_wrapper
from typing import Callable
from threading import Thread

from mcp.server.fastmcp import FastMCP
from .executor import Executor
from logger import getLogger

logger = getLogger("MCPServer")


class MakeTool:
    """
    装饰器, 用于将函数转换为工具
    """
    def __init__(self, func):
        self.executor = Executor.get()
        update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.executor.send_function_call(self.func, kwargs)


class MCPServer(FastMCP):
    """
    MCPServer类, 用于创建MCP服务器
    """
    def __init__(self, *args, **settings):
        super().__init__(*args, **settings)
        self.make_tool = MakeTool

    def add_tool(self, *arg, **kwargs):
        """
        添加工具, 该方法会自动添加工具的描述信息
        """
        
        res = super().add_tool(*arg, **kwargs)
        # self.list_tools 是异步方法
        tool = asyncio.run(self.list_tools())[-1]
        try:
            properties = tool.inputSchema["properties"]
            description = tool.description
            for name, info in properties.items():
                # - name: description.....\n
                find_description = re.search(f"- {name}: (.*)\n", description)
                if not find_description:
                    continue
                info["description"] = find_description.group(1)
                logger.debug(f"添加描述 - {name}: {info['description']}")
                # 从description中获取属性描述
        except Exception as e:
            logger.warning(f"Build property description failed: {e}")
        return res


class Server:
    """
    MCPServer的单例类, 用于管理MCPServer的生命周期和工具注册
    params: name: str = "MCPServer"
    params: host: str = "localhost"
    params: port: int = 45677
    params: server: "MCPServer" = None
    params: tools: dict[Callable, None] = {}
    params: make_tool = MakeTool
    params: tool_wraper: None
    """

    @classmethod
    def __init__(
        self, 
        name: str = "MCPServer", 
        host: str = "localhost", 
        port: int = 45677
        ):
        """
        初始化MCPServer, 创建MCPServer实例
        """
        self.name = name
        self.host = host
        self.port = port
        self.server = None
        self.tools = {}
        self.make_tool = MakeTool
        self.tool_wrapper = None
        self.init()

    @classmethod
    def init(cls):
        """
        初始化MCPServer, 创建MCPServer实例
        """
        cls.server = MCPServer(name=cls.name, host=cls.host, port=cls.port)
        cls.tool_wraper = cls.server.tool()

    @classmethod
    def register_tool(cls, tool: Callable) -> None:
        """
        注册工具, 如果工具已经注册, 则不再注册
        """
        if tool in cls.tools:
            return
        t = cls.make_tool(tool)
        cls.tools[tool] = t
        cls.tool_wraper(t)

    @classmethod
    def register_tools(cls, tools: list[Callable]) -> None:
        """
        （多个）注册工具, 如果工具已经注册, 则不再注册
        """
        for tool in tools:
            cls.register_tool(tool)

    @classmethod
    def unregister_tool(cls, tool: Callable) -> None:
        """
        卸载工具, 如果工具没有注册, 则不再卸载
        """
        if tool not in cls.tools:
            return
        try:
            t = cls.tools.pop(tool, None)
            cls.server._tool_manager._tools.pop(t.__name__)
        except Exception as e:
            logger.warning(f"Unregister tool failed: {e}")

    @classmethod
    def unregister_tools(cls, tools: list[Callable]) -> None:
        """
        （多个）卸载工具, 如果工具没有注册, 则不再卸载
        """
        for tool in tools:
            cls.unregister_tool(tool)

    @classmethod
    def main(cls):
        if not cls.server:
            cls.init()
        logger.info(f"MCPServer实例: {cls.name}正在运转...")
        cls.server.run(transport="sse")

    @classmethod
    def run(cls, block=True):
        """Run the MCP server

        Args:
            block (bool): 是否阻塞当前终端，默认阻塞。
        """
        if block:
            # 阻塞模式，直接调用 main 方法
            cls.main()
        else:
            # 非阻塞模式，启动后台线程
            job = Thread(target=cls.main, daemon=True)
            job.start()


def register(block=True):
    """启动 MCP 服务器

    Args:
        block (bool): 是否阻塞当前终端，默认阻塞。
    """
    Server.init()
    Server.run(block=block)


def unregister():
    pass
