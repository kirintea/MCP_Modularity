class ToolsPackageBase:
    """
    工具包基类，所有工具包都需要继承这个类
    
    1. 工具包名称：__name__
    2. 工具包描述：__doc__
    3. 工具包版本：__version__
    """

    __tools__: dict[str, "ToolsPackageBase"] = {}

    @classmethod
    def get_all_tool_packages(cls) -> list["ToolsPackageBase"]:
        return cls.__subclasses__()

    @classmethod
    def get_all_tool_packages_names(cls) -> list[str]:
        return [t.__name__ for t in cls.get_all_tool_packages()]

    @classmethod
    def get_package(cls, name: str) -> "ToolsPackageBase":
        if name not in cls.__tools__:
            for t in cls.get_all_tool_packages():
                cls.__tools__[t.__name__] = t
        return cls.__tools__.get(name)

    @classmethod
    def get_enum_items(cls):
        return [(t.__name__, t.__name__, t.__doc__.strip() or "", 1 << i) for i, t in enumerate(cls.get_all_tool_packages())]

    @classmethod
    def get_all_tools(cls):
        tools = []
        for pname in cls.__dict__:
            if pname.startswith("__"):
                continue
            p = getattr(cls, pname)
            if not callable(p):
                continue
            # 只添加函数
            tools.append(p)
        return tools
