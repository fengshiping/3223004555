#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文查重系统单元测试
"""

import unittest
import os
import tempfile
import shutil
import sys
import subprocess
import time

from main import PaperCheckSystem
from utils.file_manager import FileManager
from utils.text_processor import TextProcessor
from algorithms.lcs_algorithm import LCSEngine


class TestPaperCheckSystem(unittest.TestCase):
    """论文查重系统单元测试"""

    def setUp(self):
        """测试前准备"""
        self.system = PaperCheckSystem()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_text_standardization(self):
        """测试文本标准化处理"""
        test_cases = [
            ("Hello, World!", "hello world"),
            ("测试！@#文本", "测试 文本"),
            ("  多个  空格  ", "多个 空格"),
            ("", ""),
            (None, ""),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = TextProcessor.standardize_text(input_text)
                self.assertEqual(result, expected)

    def test_lcs_calculation(self):
        """测试LCS算法核心逻辑"""
        test_cases = [
            (["a", "b", "c"], ["a", "b", "c"], 3),
            (["a", "b", "c"], ["x", "y", "z"], 0),
            (["a", "b", "c", "d"], ["a", "c", "e", "d"], 3),
            ([], ["a", "b"], 0),
            (["a", "b"], [], 0),
        ]

        for seq_a, seq_b, expected in test_cases:
            with self.subTest(seq_a=seq_a, seq_b=seq_b):
                result = LCSEngine.calculate_lcs_length(seq_a, seq_b)
                self.assertEqual(result, expected)

    def test_similarity_computation(self):
        """测试相似度计算"""
        test_cases = [
            ("hello world", "hello world", 1.0),
            ("hello world", "goodbye world", 0.5),
            ("测试文本", "完全不同", 0.0),
            ("", "任何文本", 0.0),
            ("任何文本", "", 0.0),
        ]

        for text_a, text_b, expected in test_cases:
            with self.subTest(text_a=text_a, text_b=text_b):
                result = LCSEngine.compute_textual_similarity(text_a, text_b)
                self.assertAlmostEqual(result, expected, places=2)

    def test_file_operations(self):
        """测试文件操作模块"""
        test_file = os.path.join(self.test_dir, "test.txt")
        test_content = "测试文件内容"

        # 测试写入和读取
        FileManager.persist_content(test_file, test_content)
        content = FileManager.load_file_content(test_file)
        self.assertEqual(content, test_content)

    def test_invalid_file_paths(self):
        """测试无效文件路径验证"""
        invalid_paths = ["", None, "../test", "~/.bashrc", "test*.txt"]

        for path in invalid_paths:
            with self.subTest(path=path):
                self.assertFalse(FileManager.verify_path_safety(path))

    def test_system_integration(self):
        """测试系统集成流程"""
        orig_file = os.path.join(self.test_dir, "orig.txt")
        plag_file = os.path.join(self.test_dir, "plag.txt")
        output_file = os.path.join(self.test_dir, "ans.txt")

        # 创建测试文件
        with open(orig_file, 'w', encoding='utf-8') as f:
            f.write("今天是星期天，天气晴，今天晚上我要去看电影。")

        with open(plag_file, 'w', encoding='utf-8') as f:
            f.write("今天是周天，天气晴朗，我晚上要去看电影。")

        # 测试完整流程
        system = PaperCheckSystem()
        system.load_files(orig_file, plag_file)
        similarity = system.calculate_similarity()
        system.save_result(output_file, similarity)

        # 验证结果
        self.assertAlmostEqual(similarity, 0.85, places=1)
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, 'r', encoding='utf-8') as f:
            result = f.read().strip()
            self.assertTrue(result.replace('.', '').isdigit())

    def test_performance_large_text(self):
        """测试大文本处理性能"""
        # 生成大文本
        large_text = " ".join(["测试文本"] * 1000)
        orig_file = os.path.join(self.test_dir, "large_orig.txt")
        plag_file = os.path.join(self.test_dir, "large_plag.txt")
        output_file = os.path.join(self.test_dir, "large_ans.txt")

        with open(orig_file, 'w', encoding='utf-8') as f:
            f.write(large_text)

        with open(plag_file, 'w', encoding='utf-8') as f:
            f.write(large_text)

        # 性能测试
        start_time = time.time()

        system = PaperCheckSystem()
        system.load_files(orig_file, plag_file)
        similarity = system.calculate_similarity()
        system.save_result(output_file, similarity)

        end_time = time.time()
        execution_time = end_time - start_time

        # 确保在合理时间内完成
        self.assertLess(execution_time, 5.0)
        self.assertEqual(similarity, 1.0)

    def test_error_handling(self):
        """测试错误处理机制"""
        # 测试文件不存在
        with self.assertRaises(FileNotFoundError):
            FileManager.load_file_content("nonexistent_file.txt")

        # 测试无效参数
        system = PaperCheckSystem()
        with self.assertRaises(RuntimeError):
            system.calculate_similarity()

    def test_edge_cases(self):
        """测试边界情况"""
        # 空文件
        empty_file = os.path.join(self.test_dir, "empty.txt")
        open(empty_file, 'w').close()

        system = PaperCheckSystem()
        system.load_files(empty_file, empty_file)
        similarity = system.calculate_similarity()
        self.assertEqual(similarity, 0.0)

    def test_command_line_interface(self):
        """测试命令行接口"""
        orig_file = os.path.join(self.test_dir, "cli_orig.txt")
        plag_file = os.path.join(self.test_dir, "cli_plag.txt")
        output_file = os.path.join(self.test_dir, "cli_ans.txt")

        with open(orig_file, 'w', encoding='utf-8') as f:
            f.write("测试文本")

        with open(plag_file, 'w', encoding='utf-8') as f:
            f.write("测试文本")

        # 运行命令行程序
        command = [
            sys.executable, 'main.py',
            orig_file, plag_file, output_file
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            self.assertEqual(f.read().strip(), "1.00")


if __name__ == "__main__":
    unittest.main(verbosity=2)
