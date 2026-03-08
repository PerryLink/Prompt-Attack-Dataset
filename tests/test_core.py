"""核心逻辑测试"""
import pytest
from prompt_attack_dataset import AttackDataset, AttackRunner, ResponseEvaluator
from prompt_attack_dataset.core import Attack


def test_attack_dataset_load(attack_dataset):
    """测试数据集加载"""
    attacks = attack_dataset.get_all_attacks()
    assert len(attacks) > 0
    assert all(isinstance(a, Attack) for a in attacks)


def test_attack_dataset_filter_by_category(attack_dataset):
    """测试按类别过滤"""
    attacks = attack_dataset.filter_attacks(category="prompt_injection")
    assert len(attacks) > 0
    assert all(a.category == "prompt_injection" for a in attacks)


def test_attack_dataset_filter_by_severity(attack_dataset):
    """测试按严重程度过滤"""
    attacks = attack_dataset.filter_attacks(severity="high")
    assert len(attacks) > 0
    assert all(a.severity == "high" for a in attacks)


def test_response_evaluator_safe():
    """测试响应评估器 - 安全响应"""
    evaluator = ResponseEvaluator()
    attack = Attack(
        id="test_001",
        category="test",
        name="Test Attack",
        prompt="Test prompt",
        severity="high",
        expected_behavior="refuse",
        tags=[]
    )

    safe_response = "I cannot help with that request. It goes against my guidelines."
    result = evaluator.evaluate(attack, safe_response)
    assert result == "SAFE"


def test_response_evaluator_failed():
    """测试响应评估器 - 失败响应（被攻破）"""
    evaluator = ResponseEvaluator()
    attack = Attack(
        id="test_001",
        category="test",
        name="Test Attack",
        prompt="Test prompt",
        severity="high",
        expected_behavior="refuse",
        tags=[]
    )

    unsafe_response = "Here's how to do that: Step 1: First, you need to..."
    result = evaluator.evaluate(attack, unsafe_response)
    assert result == "FAILED"


def test_attack_runner_safe(mock_provider, sample_attacks):
    """测试攻击执行器 - 安全模型"""
    runner = AttackRunner(mock_provider)
    result = runner.run_attack(sample_attacks[0])

    assert result.status == "SAFE"
    assert result.attack_id == sample_attacks[0].id
    assert result.latency > 0


def test_attack_runner_unsafe(mock_unsafe_provider, sample_attacks):
    """测试攻击执行器 - 不安全模型"""
    runner = AttackRunner(mock_unsafe_provider)
    result = runner.run_attack(sample_attacks[0])

    assert result.status == "FAILED"
    assert result.attack_id == sample_attacks[0].id


def test_attack_runner_batch(mock_provider, sample_attacks):
    """测试批量执行"""
    runner = AttackRunner(mock_provider)
    results = runner.run_batch(sample_attacks)

    assert len(results) == len(sample_attacks)
    assert all(r.status == "SAFE" for r in results)
