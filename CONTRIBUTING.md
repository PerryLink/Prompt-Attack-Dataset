# Contributing to prompt-attack-dataset

Thank you for your interest in this project!

---

## Current Project Status

This is a **personal project** maintained solely by [Chance Dean](https://github.com/PerryLink). At this stage, the project is not open for external contributions via pull requests. However, **bug reports and feature suggestions are very welcome**.

---

## Reporting Issues

If you find a bug or have a feature request, please open a GitHub Issue and include:

- A clear title describing the problem
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Your environment: OS, Python version, package version
- Any relevant error messages or stack traces

Contact: novelnexusai@outlook.com

---

## Development Setup

If you want to explore the code locally:

### Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/) (recommended) or pip

### Clone and Install

```bash
git clone https://github.com/PerryLink/prompt-attack-dataset.git
cd prompt-attack-dataset

# Install all dependencies (including dev)
poetry install

# Activate the virtual environment
poetry shell
```

### Run Tests

```bash
poetry run pytest
```

### Code Formatting and Linting

```bash
# Format code
poetry run black src/

# Lint
poetry run ruff check src/

# Type check
poetry run mypy src/
```

---

## Code Style

This project follows [PEP 8](https://pep8.org/) with the following configuration:

- **Line length**: 100 characters
- **Formatter**: [Black](https://black.readthedocs.io/)
- **Linter**: [Ruff](https://docs.astral.sh/ruff/)
- **Type checker**: [mypy](https://mypy.readthedocs.io/)

All code must pass `black`, `ruff`, and `mypy` checks before being committed.

---

## Pull Request Process

> Note: Since this is currently a personal project, PRs are not actively solicited. This section is provided for reference should the project open to external contributors in the future.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes following the code style guidelines above
4. Write or update tests to cover your changes
5. Ensure all tests pass: `poetry run pytest`
6. Commit your changes with a clear message:
   ```
   feat: add support for Azure OpenAI provider
   fix: handle timeout errors in AttackRunner
   docs: update CLI usage examples
   ```
7. Push to your fork and open a Pull Request against `main`
8. Describe what your PR does and reference any related issues

---

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).

Copyright 2026 Chance Dean \<novelnexusai@outlook.com\>
