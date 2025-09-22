"""
文件操作工具模块
"""
import os



class FileManager:
    """文件操作工具类（系统级文件操作封装）"""

    @staticmethod
    def load_file_content(file_path_str: str, encoding_type: str = 'utf-8') -> str:
        """
        安全读取文件内容（含异常处理）

        Args:
            file_path_str: 文件绝对路径
            encoding_type: 文本编码格式

        Returns:
            解码后的文本内容

        Raises:
            FileNotFoundError: 路径无效
            PermissionError: 权限不足
            UnicodeDecodeError: 编码错误
        """
        # 路径有效性验证
        if not os.path.exists(file_path_str):
            raise FileNotFoundError(f"指定路径不存在: {file_path_str}")

        if not os.path.isfile(file_path_str):
            raise ValueError(f"非文件路径: {file_path_str}")

        try:
            # 带缓冲的文本读取
            with open(file_path_str, 'r', encoding=encoding_type, buffering=8192) as file_obj:
                return file_obj.read()
        except PermissionError as perm_err:
            raise PermissionError(f"文件读取权限不足: {file_path_str}") from perm_err
        except UnicodeDecodeError as decode_err:
            raise UnicodeDecodeError(f"编码解析失败: {file_path_str}",
                                     decode_err.encoding,
                                     decode_err.reason,
                                     decode_err.object,
                                     decode_err.start,
                                     decode_err.end) from decode_err

    @staticmethod
    def persist_content(file_path_str: str,
                        content_str: str,
                        encoding_type: str = 'utf-8') -> None:
        """
        安全写入文件内容（自动创建目录）

        Args:
            file_path_str: 输出文件路径
            content_str: 待写入内容
            encoding_type: 文本编码格式

        Raises:
            PermissionError: 写权限不足
            OSError: 路径创建失败
        """
        # 自动创建父目录
        target_dir = os.path.dirname(file_path_str)
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        try:
            # 原子写入操作
            with open(file_path_str, 'w', encoding=encoding_type) as file_obj:
                file_obj.write(content_str)
        except PermissionError as perm_err:
            raise PermissionError(f"文件写入权限不足: {file_path_str}") from perm_err

    @staticmethod
    def verify_path_safety(file_path_str: str) -> bool:
        """
        验证文件路径安全性

        Args:
            file_path_str: 待验证路径

        Returns:
            路径是否安全
        """
        # 类型校验
        if not isinstance(file_path_str, str):
            return False

        # 空路径检测
        if not file_path_str.strip():
            return False

        # 危险模式检测
        unsafe_patterns = ['..', '~', '*', '?', '|', '<', '>', '"', ';']
        return not any(pattern in file_path_str for pattern in unsafe_patterns)
