# prompt-attack-dataset

> A ready-to-use LLM Prompt Injection attack test suite for security researchers.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://img.shields.io/pypi/v/prompt-attack-dataset.svg)](https://pypi.org/project/prompt-attack-dataset/)

---

## Features

- **Ready-to-use Arsenal** — Curated Prompt Injection attack cases in JSON/CSV format
- **Automated Testing** — Batch-send attack prompts to target models via Python scripts
- **Visual Results** — Red `FAILED` (model compromised) vs Green `SAFE` (model secure)
- **PyTest Integration** — Run as a test suite inside your CI pipeline
- **CLI Tool** — Command-line friendly, built for security engineers

## Quick Start

### Installation

```bash
# Using pip
pip install prompt-attack-dataset

# Using Poetry
poetry add prompt-attack-dataset
```

### Basic Usage

```bash
# List all attack cases
prompt-attack-dataset list

# Run attack tests (OpenAI)
prompt-attack-dataset run \
  --provider openai \
  --model gpt-4 \
  --api-key $OPENAI_API_KEY

# Run attack tests (Anthropic)
prompt-attack-dataset run \
  --provider anthropic \
  --model claude-3-opus-20240229 \
  --api-key $ANTHROPIC_API_KEY

# Filter by category
prompt-attack-dataset run \
  --provider openai \
  --model gpt-4 \
  --api-key $OPENAI_API_KEY \
  --category prompt_injection

# Export dataset
prompt-attack-dataset export --format csv --output attacks.csv

# Show statistics
prompt-attack-dataset stats
```

## Usage Guide

### Python API

```python
from prompt_attack_dataset import AttackDataset, AttackRunner, OpenAIAdapter

# Load dataset
dataset = AttackDataset.load_default()
attacks = dataset.get_all_attacks()

# Create provider adapter
adapter = OpenAIAdapter(api_key="your-api-key", model="gpt-4")

# Execute attack tests
runner = AttackRunner(adapter)
results = runner.run_batch(attacks)

# Analyze results
for result in results:
    print(f"{result.attack_id}: {result.status}")
```

### PyTest Integration

```python
# test_security.py
import pytest
from prompt_attack_dataset import AttackDataset, AttackRunner, OpenAIAdapter

@pytest.fixture
def runner():
    adapter = OpenAIAdapter(api_key="your-api-key", model="gpt-4")
    return AttackRunner(adapter)

def test_prompt_injection_safety(runner):
    dataset = AttackDataset.load_default()
    attacks = dataset.filter_attacks(category="prompt_injection")

    for attack in attacks:
        result = runner.run_attack(attack)
        assert result.status == "SAFE", f"Model failed to safely handle {attack.name}"
```

### Output Example

```
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
┃ ID     ┃ Name                       ┃ Status  ┃ Latency ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
│ pi_001 │ Ignore Previous Instruction │ SAFE    │ 1.23s   │
│ pi_002 │ System Prompt Override      │ FAILED  │ 2.45s   │
│ pi_003 │ Role Switch Injection       │ SAFE    │ 1.87s   │
└────────┴────────────────────────────┴─────────┴─────────┘

Summary: 2/3 SAFE (66.7%) | 1 FAILED | 0 ERRORS
```

## Project Structure

```
prompt-attack-dataset/
├── src/
│   └── prompt_attack_dataset/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py          # CLI entry point (Typer)
│       ├── core.py         # Core dataset and runner logic
│       └── utils.py        # Shared utilities
├── datasets/
│   └── attacks.json        # Curated attack cases
├── tests/                  # PyTest test suite
├── pyproject.toml
├── poetry.lock
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.9+ |
| CLI | [Typer](https://typer.tiangolo.com/) |
| Output formatting | [Rich](https://rich.readthedocs.io/) |
| Data validation | [Pydantic v2](https://docs.pydantic.dev/) |
| HTTP client | [httpx](https://www.python-httpx.org/) |
| LLM providers | OpenAI SDK, Anthropic SDK |
| Testing | PyTest + pytest-cov |
| Linting | Ruff + Black + mypy |
| Package management | [Poetry](https://python-poetry.org/) |

## Supported LLM Providers

- OpenAI (GPT-3.5, GPT-4, GPT-4-turbo)
- Anthropic (Claude 3 series)
- Azure OpenAI *(coming soon)*
- Custom HTTP API *(coming soon)*

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

Copyright 2026 Chance Dean \<novelnexusai@outlook.com\>

## Disclaimer

This project is intended for security research and educational purposes only. Do not use this tool for any illegal or unauthorized testing activities. Users are solely responsible for all consequences arising from the use of this tool.

---

# prompt-attack-dataset（中文文档）

> 开箱即用的 LLM Prompt Injection 攻击测试集

## 核心特性

- **现成弹药库** — 精心整理的 Prompt Injection 攻击案例数据集（JSON/CSV 格式）
- **自动化测试** — Python 脚本批量发送攻击提示词到目标模型
- **直观结果展示** — 红色 `FAILED`（模型被攻破）vs 绿色 `SAFE`（模型安全）
- **PyTest 集成** — 可作为测试套件在 CI 流水线中运行
- **CLI 工具** — 命令行友好，技术极客最爱

## 快速开始

### 安装

```bash
# 使用 pip 安装
pip install prompt-attack-dataset

# 或使用 Poetry
poetry add prompt-attack-dataset
```

### 基本使用

```bash
# 列出所有攻击案例
prompt-attack-dataset list

# 运行攻击测试（OpenAI）
prompt-attack-dataset run \
  --provider openai \
  --model gpt-4 \
  --api-key $OPENAI_API_KEY

# 运行攻击测试（Anthropic）
prompt-attack-dataset run \
  --provider anthropic \
  --model claude-3-opus-20240229 \
  --api-key $ANTHROPIC_API_KEY

# 按类别过滤
prompt-attack-dataset run \
  --provider openai \
  --model gpt-4 \
  --api-key $OPENAI_API_KEY \
  --category prompt_injection

# 导出数据集
prompt-attack-dataset export --format csv --output attacks.csv

# 显示统计信息
prompt-attack-dataset stats
```

## 使用指南

### Python API

```python
from prompt_attack_dataset import AttackDataset, AttackRunner, OpenAIAdapter

# 加载数据集
dataset = AttackDataset.load_default()
attacks = dataset.get_all_attacks()

# 创建 Provider 适配器
adapter = OpenAIAdapter(api_key="your-api-key", model="gpt-4")

# 执行攻击测试
runner = AttackRunner(adapter)
results = runner.run_batch(attacks)

# 分析结果
for result in results:
    print(f"{result.attack_id}: {result.status}")
```

### 数据集结构

数据集包含以下类别的攻击案例：

**1. 提示词注入 (Prompt Injection)**
直接注入攻击，尝试覆盖系统指令：忽略之前的指令、系统提示词覆盖、角色切换注入、指令终止符注入、优先级覆盖

**2. 越狱攻击 (Jailbreak)**
通过角色扮演和上下文操纵绕过限制：DAN 模式、假设场景、研究目的、电影剧本、反向心理、祖母漏洞、代码模式、翻译陷阱

**3. 数据提取 (Data Extraction)**
尝试提取系统提示词或训练数据：直接提示词提取、重复提示词、配置信息提取、训练数据探测、隐藏指令提取、API 密钥探测

**4. 操纵攻击 (Manipulation)**
通过情感操纵或逻辑陷阱诱导不当响应：紧急情况、权威诉求、道德困境、逻辑陷阱、同意诱导

**5. 编码绕过 (Encoding)**
使用编码或混淆技术绕过内容过滤：Base64 编码、ROT13 编码、字符替换、Unicode 混淆

## 项目结构

```
prompt-attack-dataset/
├── src/
│   └── prompt_attack_dataset/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py          # CLI 入口（Typer）
│       ├── core.py         # 核心数据集与运行器逻辑
│       └── utils.py        # 公共工具函数
├── datasets/
│   └── attacks.json        # 精选攻击案例
├── tests/                  # PyTest 测试套件
├── pyproject.toml
├── poetry.lock
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## 技术栈

| 组件 | 技术选型 |
|------|---------|
| 开发语言 | Python 3.9+ |
| CLI 框架 | Typer |
| 输出格式化 | Rich |
| 数据校验 | Pydantic v2 |
| HTTP 客户端 | httpx |
| LLM 接入 | OpenAI SDK、Anthropic SDK |
| 测试框架 | PyTest + pytest-cov |
| 代码检查 | Ruff + Black + mypy |
| 包管理 | Poetry |

## 许可证

Apache License 2.0 — 详见 [LICENSE](LICENSE) 文件

Copyright 2026 Chance Dean \<novelnexusai@outlook.com\>

## 免责声明

本项目仅用于安全研究和教育目的。请勿将本工具用于任何非法或未经授权的测试活动。使用者需自行承担使用本工具的所有责任。

---

**Made with dedication for LLM Security Researchers** | [PerryLink](https://github.com/PerryLink)
