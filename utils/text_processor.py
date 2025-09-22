"""
文本处理工具模块
"""
import re
from typing import List


class TextProcessor:
    """文本处理工具类（标准化处理流程）"""

    @staticmethod
    def standardize_text(raw_input: str) -> str:
        """
        文本标准化处理四步流程

        Args:
            raw_input: 原始文本输入

        Returns:
            标准化后的文本
        """
        # 空文本处理
        if not raw_input or not isinstance(raw_input, str):
            return ""

        # 1. 大小写归一化
        normalized_text = raw_input.lower()

        # 2. 符号过滤（保留中文字符+英文+数字+空格）
        normalized_text = re.sub(r'[^\u4e00-\u9fff\u0030-\u0039\u0041-\u005a\u0061-\u007a\s]',
                                 ' ', normalized_text)

        # 3. 连续空格压缩
        normalized_text = re.sub(r'\s{2,}', ' ', normalized_text)

        # 4. 首尾空格修剪
        return normalized_text.strip()

    @staticmethod
    def tokenize_content(processed_text: str) -> List[str]:
        """
        内容分词处理

        Args:
            processed_text: 标准化后的文本

        Returns:
            词元列表
        """
        # 空文本处理
        if not processed_text:
            return []

        # 基于空格的简单分词
        return processed_text.split()

    @staticmethod
    def compute_word_count(input_text: str) -> int:
        """
        计算文本词数（通过标准化处理）

        Args:
            input_text: 原始文本

        Returns:
            有效词数
        """
        # 完整处理流程
        processed = TextProcessor.standardize_text(input_text)
        return len(TextProcessor.tokenize_content(processed))
