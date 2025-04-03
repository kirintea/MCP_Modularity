import traceback
from .common import ToolsPackageBase


class CommonTools(ToolsPackageBase):
    """
    (备注) 常用工具包
    """

    def get_system_info() -> dict:
        """
        cn: 获取系统信息
        en: Get system information
        """
        import platform
        import os

        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.architecture(),
            "python_version": platform.python_version(),
            "current_directory": os.getcwd(),
        }

    def get_file_info(file_path: str) -> dict:
        """
        cn: 获取文件信息
        en: Get file information
        """
        import os

        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            file_info = {
                "file_path": file_path,
                "size": os.path.getsize(file_path),
                "is_directory": os.path.isdir(file_path),
                "is_file": os.path.isfile(file_path),
                "last_modified": os.path.getmtime(file_path),
            }
            return file_info
        except Exception as e:
            print(f"Error in get_file_info: {str(e)}")
            traceback.print_exc()
            return {"error": str(e)}

    def execute_python_code(code: str) -> dict:
        """
        cn: 执行Python代码
        en:Execute arbitrary Python code.

        Args:
        - code: The Python code to execute
        """
        # This is powerful but potentially dangerous - use with caution
        try:
            # Create a local namespace for execution
            namespace = {}
            exec(code, namespace)
            return {"executed": True, "namespace": namespace}
        except Exception as e:
            print(f"Error in execute_python_code: {str(e)}")
            traceback.print_exc()
            return {"error": str(e)}

    def list_directory_contents(directory_path: str) -> dict:
        """
        cn: 列出目录内容
        en: List the contents of a directory.

        Args:
        - directory_path: The path of the directory to list
        """
        import os

        try:
            if not os.path.exists(directory_path):
                raise FileNotFoundError(f"Directory not found: {directory_path}")

            contents = os.listdir(directory_path)
            return {"directory": directory_path, "contents": contents}
        except Exception as e:
            print(f"Error in list_directory_contents: {str(e)}")
            traceback.print_exc()
            return {"error": str(e)}