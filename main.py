#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文查重系统主程序
"""

import sys
import argparse
import time
from typing import List, Optional

# 更新后的导入语句
from utils.file_manager import FileManager
from utils.text_processor import TextProcessor
from algorithms.lcs_algorithm import LCSEngine


class PaperCheckSystem:
    """论文查重系统主类"""

    def __init__(self):
        self.original_content: Optional[str] = None
        self.plagiarized_content: Optional[str] = None
        self.tokenized_original: Optional[List[str]] = None
        self.tokenized_plagiarized: Optional[List[str]] = None

    def load_files(self, orig_path: str, plag_path: str) -> None:
        """
        加载原文和抄袭文本文件

        Args:
            orig_path: 原文文件路径
            plag_path: 抄袭文本文件路径

        Raises:
            ValueError: 文件路径无效
            IOError: 文件读取错误
        """
        # 验证文件路径
        if not FileManager.verify_path_safety(orig_path):
            raise ValueError(f"无效的原文文件路径: {orig_path}")
        if not FileManager.verify_path_safety(plag_path):
            raise ValueError(f"无效的抄袭文件路径: {plag_path}")

        # 读取文件内容
        try:
            print(f"正在读取原文文件: {orig_path}")
            self.original_content = FileManager.load_file_content(orig_path)

            print(f"正在读取抄袭文件: {plag_path}")
            self.plagiarized_content = FileManager.load_file_content(plag_path)

            # 检查文件是否为空
            if not self.original_content.strip():
                print("警告: 原文文件内容为空")
            if not self.plagiarized_content.strip():
                print("警告: 抄袭文件内容为空")

        except Exception as e:
            raise IOError(f"文件读取失败: {str(e)}") from e

    def preprocess_texts(self) -> None:
        """预处理加载的文本内容"""
        if self.original_content:
            self.tokenized_original = TextProcessor.tokenize_content(
                TextProcessor.standardize_text(self.original_content)
            )

        if self.plagiarized_content:
            self.tokenized_plagiarized = TextProcessor.tokenize_content(
                TextProcessor.standardize_text(self.plagiarized_content)
            )

    def calculate_similarity(self) -> float:
        """
        计算重复率

        Returns:
            重复率 (0.0 - 1.0)

        Raises:
            ValueError: 文本未加载
        """
        if (self.tokenized_original is None
                or self.tokenized_plagiarized is None):
            self.preprocess_texts()  # 确保已预处理

        print("正在计算文本相似度...")
        start_time = time.time()

        try:
            similarity = LCSEngine.compute_textual_similarity(
                " ".join(self.tokenized_original),
                " ".join(self.tokenized_plagiarized)
            )

            end_time = time.time()
            print(f"计算完成，耗时: {end_time - start_time:.4f}秒")

            return similarity

        except Exception as e:
            raise RuntimeError(f"相似度计算失败: {str(e)}") from e

    def save_result(self, output_path: str, similarity: float) -> None:
        """
        保存结果到文件

        Args:
            output_path: 输出文件路径
            similarity: 相似度结果

        Raises:
            ValueError: 文件路径无效
            IOError: 文件写入错误
        """
        if not FileManager.verify_path_safety(output_path):
            raise ValueError(f"无效的输出文件路径: {output_path}")

        # 格式化结果（保留两位小数）
        result = f"{similarity:.2f}"

        try:
            FileManager.persist_content(output_path, result)
            print(f"结果已保存到: {output_path}")
        except Exception as e:
            raise IOError(f"文件写入失败: {str(e)}")


def setup_argument_parser() -> argparse.ArgumentParser:
    """设置命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="论文查重系统 - 基于LCS算法计算文本相似度",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""


文件格式要求:
  - 支持UTF-8编码的文本文件
  - 文件路径不应包含空格或特殊字符
        """
    )

    parser.add_argument(
        'original_file',
        type=str,
        help='原文文件的绝对路径'
    )

    parser.add_argument(
        'plagiarized_file',
        type=str,
        help='抄袭版论文文件的绝对路径'
    )

    parser.add_argument(
        'output_file',
        type=str,
        help='输出结果文件的绝对路径'
    )

    return parser


def main() -> int:
    """
    主函数入口

    Returns:
        退出代码 (0: 成功, 1: 失败)
    """
    # 设置参数解析器
    parser = setup_argument_parser()

    # 解析命令行参数
    if len(sys.argv) != 4:
        parser.print_help()
        return 1

    try:
        args = parser.parse_args()
    except SystemExit:
        return 1

    # 创建查重系统实例
    system = PaperCheckSystem()

    try:
        # 加载文件
        system.load_files(args.original_file, args.plagiarized_file)

        # 计算相似度
        similarity = system.calculate_similarity()

        # 保存结果
        system.save_result(args.output_file, similarity)

        print(f"查重完成！重复率: {similarity:.2%}")
        return 0

    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
