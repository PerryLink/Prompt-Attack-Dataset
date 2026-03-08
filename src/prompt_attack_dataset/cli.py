"""CLI 命令接口"""
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .core import (
    AttackDataset,
    AttackRunner,
    OpenAIAdapter,
    AnthropicAdapter,
    ResponseEvaluator,
)
from .utils import export_results_to_json, export_results_to_csv, calculate_statistics

app = typer.Typer(help="LLM Prompt Injection 攻击测试工具")
console = Console()


@app.command()
def list(
    category: Optional[str] = typer.Option(None, help="按类别过滤"),
    severity: Optional[str] = typer.Option(None, help="按严重程度过滤"),
):
    """列出所有攻击案例"""
    dataset = AttackDataset.load_default()
    attacks = dataset.filter_attacks(category=category, severity=severity)

    table = Table(title="攻击案例列表")
    table.add_column("ID", style="cyan")
    table.add_column("类别", style="yellow")
    table.add_column("名称", style="white")
    table.add_column("严重程度", style="red")

    for attack in attacks:
        table.add_row(attack.id, attack.category, attack.name, attack.severity)

    console.print(table)
    console.print(f"\n总计: {len(attacks)} 个攻击案例")


@app.command()
def run(
    provider: str = typer.Option(..., help="LLM Provider (openai/anthropic)"),
    model: str = typer.Option(..., help="模型名称"),
    api_key: str = typer.Option(..., help="API 密钥"),
    category: Optional[str] = typer.Option(None, help="按类别过滤"),
    severity: Optional[str] = typer.Option(None, help="按严重程度过滤"),
    output: Optional[str] = typer.Option(None, help="输出文件路径 (JSON)"),
):
    """运行攻击测试"""
    # 加载数据集
    dataset = AttackDataset.load_default()
    attacks = dataset.filter_attacks(category=category, severity=severity)

    if not attacks:
        console.print("[red]没有找到匹配的攻击案例[/red]")
        raise typer.Exit(1)

    # 创建 Provider 适配器
    if provider == "openai":
        adapter = OpenAIAdapter(api_key=api_key, model=model)
    elif provider == "anthropic":
        adapter = AnthropicAdapter(api_key=api_key, model=model)
    else:
        console.print(f"[red]不支持的 Provider: {provider}[/red]")
        raise typer.Exit(1)

    # 执行攻击
    runner = AttackRunner(adapter)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"正在执行 {len(attacks)} 个攻击测试...", total=len(attacks))
        results = []
        for attack in attacks:
            result = runner.run_attack(attack)
            results.append(result)
            progress.advance(task)

    # 显示结果
    table = Table(title="测试结果")
    table.add_column("ID", style="cyan")
    table.add_column("名称", style="white")
    table.add_column("状态", style="bold")
    table.add_column("延迟", justify="right")

    for result in results:
        status_style = "green" if result.status == "SAFE" else "red"
        table.add_row(
            result.attack_id,
            result.attack_name,
            f"[{status_style}]{result.status}[/{status_style}]",
            f"{result.latency:.2f}s",
        )

    console.print(table)

    # 统计信息
    stats = calculate_statistics(results)
    safe_count = stats["safe_count"]
    failed_count = stats["failed_count"]
    error_count = stats["error_count"]
    total = stats["total"]
    safe_rate = stats["safe_rate"]

    console.print(
        f"\n总结: {safe_count}/{total} SAFE ({safe_rate:.1f}%) | "
        f"{failed_count} FAILED | {error_count} ERRORS"
    )

    # 导出结果
    if output:
        export_results_to_json(results, output)
        console.print(f"\n结果已导出到: {output}")


@app.command()
def export(
    format: str = typer.Option("json", help="导出格式 (json/csv)"),
    output: str = typer.Option(..., help="输出文件路径"),
):
    """导出攻击数据集"""
    dataset = AttackDataset.load_default()
    attacks = dataset.get_all_attacks()

    if format == "json":
        data = [attack.model_dump() for attack in attacks]
        with open(output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    elif format == "csv":
        export_results_to_csv(attacks, output)
    else:
        console.print(f"[red]不支持的格式: {format}[/red]")
        raise typer.Exit(1)

    console.print(f"数据集已导出到: {output}")


@app.command()
def stats():
    """显示数据集统计信息"""
    dataset = AttackDataset.load_default()
    attacks = dataset.get_all_attacks()

    # 按类别统计
    category_counts = {}
    for attack in attacks:
        category_counts[attack.category] = category_counts.get(attack.category, 0) + 1

    # 按严重程度统计
    severity_counts = {}
    for attack in attacks:
        severity_counts[attack.severity] = severity_counts.get(attack.severity, 0) + 1

    console.print(f"[bold]数据集统计信息[/bold]\n")
    console.print(f"总攻击案例数: {len(attacks)}\n")

    console.print("[bold]按类别:[/bold]")
    for category, count in category_counts.items():
        console.print(f"  {category}: {count}")

    console.print("\n[bold]按严重程度:[/bold]")
    for severity, count in severity_counts.items():
        console.print(f"  {severity}: {count}")


if __name__ == "__main__":
    app()
