<div align="center">

# Prompt-Attack-Dataset

**开箱即用的 LLM 提示词注入攻击测试套件，含 28 个精选案例、覆盖 5 大类别。**

*已移植至 [dsh-defend](https://github.com/PerryLink/dsh-defend) —— 属于 PerryLink DSH 插件家族。*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

[English](README.md) · [简体中文](README.zh.md)

</div>

---

## 功能简介

Prompt-Attack-Dataset 内置一份精选的提示词注入攻击案例 JSON 数据集，并提供运行器将每个案例发送给目标模型，然后判断模型是否保持安全。结果以红色 `FAILED`（被攻破）或绿色 `SAFE`（安全）展示。

## 核心特性

- **开箱即用的数据集** —— 28 个攻击案例，覆盖 5 大类别（提示词注入、越狱、数据提取、操纵、编码绕过）
- **自动化测试** —— 批量发送攻击提示词到目标模型
- **直观结果** —— `SAFE` vs `FAILED`，并显示每个案例的延迟
- **PyTest 集成** —— 可作为测试套件在 CI 中运行
- **CLI 工具** —— 提供 `list`、`run`、`export`、`stats` 命令

## 快速开始

```bash
pip install prompt-attack-dataset

# 列出所有攻击案例
prompt-attack-dataset list

# 对 OpenAI 运行攻击测试
prompt-attack-dataset run --provider openai --model gpt-4 --api-key $OPENAI_API_KEY

# 对 Anthropic 运行攻击测试
prompt-attack-dataset run --provider anthropic --model claude-3-opus-20240229 --api-key $ANTHROPIC_API_KEY

# 按类别过滤
prompt-attack-dataset run --provider openai --model gpt-4 --api-key $OPENAI_API_KEY --category prompt_injection

# 导出数据集并查看统计信息
prompt-attack-dataset export --format csv --output attacks.csv
prompt-attack-dataset stats
```

## 使用指南

### Python API

```python
from prompt_attack_dataset import AttackDataset, AttackRunner
from prompt_attack_dataset.core import OpenAIAdapter

dataset = AttackDataset.load_default()
adapter = OpenAIAdapter(api_key="...", model="gpt-4")
runner = AttackRunner(adapter)

results = runner.run_batch(dataset.get_all_attacks())
for result in results:
    print(result.attack_id, result.status)
```

`AttackDataset.filter_attacks(category=..., severity=...)` 可将测试范围缩小到部分案例。

### PyTest 集成

```python
import pytest
from prompt_attack_dataset import AttackDataset, AttackRunner
from prompt_attack_dataset.core import OpenAIAdapter

@pytest.fixture
def runner():
    adapter = OpenAIAdapter(api_key="...", model="gpt-4")
    return AttackRunner(adapter)

def test_prompt_injection_safety(runner):
    attacks = AttackDataset.load_default().filter_attacks(category="prompt_injection")
    for attack in attacks:
        result = runner.run_attack(attack)
        assert result.status == "SAFE", f"Model failed to handle {attack.name}"
```

## 开发

```bash
poetry install
poetry run pytest
```

## 许可证

[Apache License 2.0](LICENSE) © 2026 PerryLink

---

**仅限安全研究与教育用途。** 请勿将本工具用于非法或未经授权的测试。
