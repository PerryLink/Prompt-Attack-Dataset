"""PyTest 配置和 Fixtures"""
import pytest
from prompt_attack_dataset import AttackDataset


@pytest.fixture
def attack_dataset():
    """加载默认攻击数据集"""
    return AttackDataset.load_default()


@pytest.fixture
def sample_attacks(attack_dataset):
    """获取示例攻击案例"""
    return attack_dataset.get_all_attacks()[:5]


class MockProviderAdapter:
    """模拟 Provider 适配器用于测试"""

    def __init__(self, response: str = "I cannot help with that request."):
        self.response = response

    def send_prompt(self, prompt: str) -> str:
        return self.response


@pytest.fixture
def mock_provider():
    """模拟 Provider"""
    return MockProviderAdapter()


@pytest.fixture
def mock_unsafe_provider():
    """模拟不安全的 Provider（会顺从攻击）"""
    return MockProviderAdapter(response="Here's how to do that: Step 1...")
