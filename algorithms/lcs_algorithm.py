"""
最长公共子序列(LCS)算法实现模块
"""
from typing import List
from utils.text_processor import TextProcessor

class LCSEngine:
    """最长公共子序列算法引擎"""

    @staticmethod
    def calculate_lcs_length(seq_a: List[str], seq_b: List[str]) -> int:
        """
        动态规划计算两个序列的LCS长度（滚动数组优化版）

        Args:
            seq_a: 输入序列A
            seq_b: 输入序列B

        Returns:
            LCS长度值
        """
        n, m = len(seq_a), len(seq_b)

        # 边界条件处理
        if n == 0 or m == 0:
            return 0

        # 初始化滚动数组（仅保留两行状态）
        dp_table = [[0] * (m + 1) for _ in range(2)]

        # 动态规划填表
        for idx_a in range(1, n + 1):
            current_row = idx_a % 2
            prev_row = (idx_a - 1) % 2

            for idx_b in range(1, m + 1):
                if seq_a[idx_a - 1] == seq_b[idx_b - 1]:
                    dp_table[current_row][idx_b] \
                        = dp_table[prev_row][idx_b - 1] + 1
                else:
                    dp_table[current_row][idx_b] = max(
                        dp_table[prev_row][idx_b],
                        dp_table[current_row][idx_b - 1]
                    )

        return dp_table[n % 2][m]

    @staticmethod
    def compute_textual_similarity(text_a: str, text_b: str, ) -> float:
        """
        基于LCS的文本相似度计算（归一化到[0,1]区间）

        Args:
            text_a: 原始文本A
            text_b: 原始文本B

        Returns:
            相似度值（四舍五入保留4位小数）
        """
        # 导入工具类（避免循环依赖）


        # 文本预处理流程
        clean_text_a = TextProcessor.standardize_text(text_a)
        clean_text_b = TextProcessor.standardize_text(text_b)

        # 生成标准化词元序列
        token_list_a = TextProcessor.tokenize_content(clean_text_a)
        token_list_b = TextProcessor.tokenize_content(clean_text_b)

        # 核心LCS长度计算
        lcs_value = LCSEngine.calculate_lcs_length(token_list_a, token_list_b)

        # 相似度归一化处理
        base_length = len(token_list_a) or 1  # 避免除零
        similarity_ratio = lcs_value / base_length

        # 边界约束与精度控制
        return round(max(0.0, min(1.0, similarity_ratio)), 4)
