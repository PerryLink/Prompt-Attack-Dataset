"""工具函数模块"""
import csv
import json
from pathlib import Path
from typing import List, Dict

from .core import Attack, TestResult


def export_results_to_json(results: List[TestResult], output_path: str):
    """导出测试结果到 JSON 文件"""
    data = [result.model_dump() for result in results]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def export_results_to_csv(attacks: List[Attack], output_path: str):
    """导出攻击数据集到 CSV 文件"""
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "category", "name", "prompt", "severity", "expected_behavior", "tags"])

        for attack in attacks:
            writer.writerow([
                attack.id,
                attack.category,
                attack.name,
                attack.prompt,
                attack.severity,
                attack.expected_behavior,
                ",".join(attack.tags),
            ])


def calculate_statistics(results: List[TestResult]) -> Dict:
    """计算测试结果统计信息"""
    total = len(results)
    safe_count = sum(1 for r in results if r.status == "SAFE")
    failed_count = sum(1 for r in results if r.status == "FAILED")
    error_count = sum(1 for r in results if r.status == "ERROR")

    safe_rate = (safe_count / total * 100) if total > 0 else 0

    return {
        "total": total,
        "safe_count": safe_count,
        "failed_count": failed_count,
        "error_count": error_count,
        "safe_rate": safe_rate,
    }
