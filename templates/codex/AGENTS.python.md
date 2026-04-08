## Python

When editing Python files:

- Follow PEP 8 and add type annotations to touched APIs when practical.
- Prefer immutable data structures such as frozen dataclasses when they fit.
- Prefer `pytest` for tests.
- Use repo-standard tooling such as `black`, `isort`, `ruff`, `mypy`, or
  `pyright` when those tools are present.
- Prefer `logging` over stray `print()` statements in non-trivial code.
- For security-sensitive Python work, run `bandit` or equivalent if available.
