"""集成测试"""
import pytest
from prompt_attack_dataset import AttackDataset, AttackRunner


# 注意：这些测试需要真实的 API 密钥才能运行
# 可以通过环境变量或 pytest 标记来控制是否运行

@pytest.mark.skip(reason="需要真实 API 密钥")
def test_openai_integration():
    """测试 OpenAI 集成（需要 API 密钥）"""
    import os
    from prompt_attack_dataset.core import OpenAIAdapter

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("未设置 OPENAI_API_KEY 环境变量")

    dataset = AttackDataset.load_default()
    attacks = dataset.filter_attacks(category="prompt_injection")[:3]

    adapter = OpenAIAdapter(api_key=api_key, model="gpt-4")
    runner = AttackRunner(adapter)

    results = runner.run_batch(attacks)
    assert len(results) == 3
    assert all(r.status in ["SAFE", "FAILED", "ERROR"] for r in results)


@pytest.mark.skip(reason="需要真实 API 密钥")
def test_anthropic_integration():
    """测试 Anthropic 集成（需要 API 密钥）"""
    import os
    from prompt_attack_dataset.core import AnthropicAdapter

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("未设置 ANTHROPIC_API_KEY 环境变量")

    dataset = AttackDataset.load_default()
    attacks = dataset.filter_attacks(category="jailbreak")[:3]

    adapter = AnthropicAdapter(api_key=api_key, model="claude-3-opus-20240229")
    runner = AttackRunner(adapter)

    results = runner.run_batch(attacks)
    assert len(results) == 3
    assert all(r.status in ["SAFE", "FAILED", "ERROR"] for r in results)
