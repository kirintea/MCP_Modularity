import functools
import logging
import json
from .utils import rounding_dumps
from logger import getLogger

logger = getLogger("Executor")


class Executor:
    """
    Executor类, 用于执行函数调用
    """
    instance = None

    @classmethod
    def get(cls) -> "Executor":
        """
        获取Executor实例, 如果实例不存在, 则创建一个新的实例
        :return: Executor实例
        """
        return cls.instance or cls()

    @classmethod
    def __new__(cls, *args, **kwargs):
        """
        创建Executor实例, 如果实例不存在, 则创建一个新的实例
        :param args: 其他参数
        :param kwargs: 其他参数
        :return: Executor实例
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def send_function_call(self, func, params):
        """
        发送函数调用请求, 并返回结果
        :param func: 要调用的函数
        :param params: 函数参数, 可以是字典或列表
        :return: 函数执行结果
        """
        # if not func:
        #     raise ValueError("func must be a callable")
        # if not callable(func):
        #     raise ValueError("func must be callable")
        # if not isinstance(params, (dict, list)):
        #     raise ValueError("params must be a dict or list")
        
        name = func.__name__
        command = {"func": func, "name": name, "params": params or {}}

        logger.info(f"Received command: {name} with parameters: {params}")
        response = self.execute_function(command)
        logger.info(f"Execution status: {response.get('status', 'unknown')}")

        if response.get("status") == "error":
            logger.error(f"Error: {response.get('message')}")
            raise Exception(response.get("message", "Unknown error"))
        result_str = rounding_dumps(response.get("result", {}), ensure_ascii=False)
        print("\n--------------------------------", flush=True)
        print(f"\tSelected function: {name}")
        print(f"\tExecution result: {result_str}")
        print("--------------------------------\n", flush=True)
        return result_str

    def execute_function(self, command):
        """
        执行函数调用, 并返回结果
        :param command: 函数调用命令, 包含函数和参数
        :return: 函数执行结果
        """
        # if not isinstance(command, dict):
        #     raise ValueError("command must be a dict")
        # if "func" not in command:
        #     raise ValueError("command must contain func key")
        # if "name" not in command:
        #     raise ValueError("command must contain name key")
        # if "params" not in command:
        #     raise ValueError("command must contain params key")
        
        func = command.get("func")
        name = command.get("name") or func.__name__
        try:
            params = command.get("params", {})
            logger.info(f"Executing function: {name} with parameters: {params}")
            result = func(**params)
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Error executing {name}: {str(e)}")
            return {"status": "error", "message": str(e)}