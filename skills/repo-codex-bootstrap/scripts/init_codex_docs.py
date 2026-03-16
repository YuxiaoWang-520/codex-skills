#!/usr/bin/env python3
"""Initialize codex workspace markdown files for a repository."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class TemplateFile:
    relative_path: str
    body: str


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_unique(items: List[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def lines_or_todo(items: List[str], todo_text: str) -> str:
    if items:
        return "\n".join(f"  - {item}" for item in items)
    return f"  - {todo_text}"


def code_block(commands: List[str], todo_text: str) -> str:
    body = "\n".join(commands) if commands else todo_text
    return f"```bash\n{body}\n```"


def read_json_file(path: Path) -> Dict[str, object]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def npm_command_for_script(script_name: str, preferred_pm: str) -> str:
    if preferred_pm == "pnpm":
        return f"pnpm {script_name}"
    if preferred_pm == "yarn":
        return f"yarn {script_name}"
    return f"npm run {script_name}"


def detect_repo_facts(repo_root: Path) -> Dict[str, List[str] | str]:
    languages: List[str] = []
    frameworks: List[str] = []
    package_tools: List[str] = []
    runtime_requirements: List[str] = []
    external_dependencies: List[str] = []
    config_files: List[str] = []
    setup_cmds: List[str] = []
    run_cmds: List[str] = []
    build_cmds: List[str] = []
    test_cmds: List[str] = []
    lint_cmds: List[str] = []
    directory_map: List[str] = []

    package_json = repo_root / "package.json"
    pnpm_lock = repo_root / "pnpm-lock.yaml"
    yarn_lock = repo_root / "yarn.lock"
    package_lock = repo_root / "package-lock.json"

    preferred_pm = "npm"
    if pnpm_lock.exists():
        preferred_pm = "pnpm"
        add_unique(package_tools, "pnpm")
    elif yarn_lock.exists():
        preferred_pm = "yarn"
        add_unique(package_tools, "yarn")
    elif package_lock.exists() or package_json.exists():
        preferred_pm = "npm"
        add_unique(package_tools, "npm")

    if package_json.exists():
        add_unique(languages, "JavaScript")
        add_unique(runtime_requirements, "Node.js")
        pkg = read_json_file(package_json)
        deps = pkg.get("dependencies", {}) or {}
        dev_deps = pkg.get("devDependencies", {}) or {}
        all_dep_names = set(deps.keys()) | set(dev_deps.keys())

        if "typescript" in all_dep_names or (repo_root / "tsconfig.json").exists():
            add_unique(languages, "TypeScript")

        framework_map = {
            "next": "Next.js",
            "react": "React",
            "vue": "Vue",
            "svelte": "Svelte",
            "nuxt": "Nuxt",
            "express": "Express",
            "fastify": "Fastify",
            "nestjs": "NestJS",
        }
        for dep_name, framework_name in framework_map.items():
            if dep_name in all_dep_names:
                add_unique(frameworks, framework_name)

        scripts = pkg.get("scripts", {}) or {}
        if scripts:
            add_unique(setup_cmds, f"{preferred_pm} install")

            for candidate in ["dev", "start", "serve"]:
                if candidate in scripts:
                    add_unique(run_cmds, npm_command_for_script(candidate, preferred_pm))
                    break

            for candidate in ["build", "compile"]:
                if candidate in scripts:
                    add_unique(build_cmds, npm_command_for_script(candidate, preferred_pm))
                    break

            for candidate in ["test", "test:unit", "test:ci"]:
                if candidate in scripts:
                    add_unique(test_cmds, npm_command_for_script(candidate, preferred_pm))
                    break

            lint_candidates = ["lint", "format", "check"]
            for candidate in lint_candidates:
                if candidate in scripts:
                    add_unique(lint_cmds, npm_command_for_script(candidate, preferred_pm))

    pyproject = repo_root / "pyproject.toml"
    requirements = repo_root / "requirements.txt"
    if pyproject.exists() or requirements.exists():
        add_unique(languages, "Python")
        add_unique(runtime_requirements, "Python 3.x")
        if (repo_root / "uv.lock").exists():
            add_unique(package_tools, "uv")
            add_unique(setup_cmds, "uv sync")
        elif (repo_root / "poetry.lock").exists():
            add_unique(package_tools, "poetry")
            add_unique(setup_cmds, "poetry install")
        else:
            add_unique(package_tools, "pip")
            if requirements.exists():
                add_unique(setup_cmds, "python3 -m pip install -r requirements.txt")

        add_unique(test_cmds, "pytest")
        add_unique(lint_cmds, "ruff check .")

    if (repo_root / "go.mod").exists():
        add_unique(languages, "Go")
        add_unique(package_tools, "go modules")
        add_unique(runtime_requirements, "Go toolchain")
        add_unique(build_cmds, "go build ./...")
        add_unique(test_cmds, "go test ./...")

    if (repo_root / "Cargo.toml").exists():
        add_unique(languages, "Rust")
        add_unique(package_tools, "cargo")
        add_unique(runtime_requirements, "Rust toolchain")
        add_unique(build_cmds, "cargo build")
        add_unique(test_cmds, "cargo test")
        add_unique(lint_cmds, "cargo clippy --all-targets --all-features")

    if (repo_root / "Dockerfile").exists() or (repo_root / "docker-compose.yml").exists():
        add_unique(external_dependencies, "Docker")

    for candidate in [
        ".env",
        ".env.example",
        ".env.local",
        "pyproject.toml",
        "package.json",
        "tsconfig.json",
        "go.mod",
        "Cargo.toml",
        "docker-compose.yml",
    ]:
        if (repo_root / candidate).exists():
            add_unique(config_files, f"`{candidate}`")

    top_dirs = sorted(
        [
            entry.name
            for entry in repo_root.iterdir()
            if entry.is_dir() and entry.name not in {".git", "codex", "node_modules", ".venv", "venv"}
        ]
    )

    for directory in top_dirs[:12]:
        directory_map.append(f"`{directory}/`: TODO describe responsibility")

    if not setup_cmds:
        add_unique(setup_cmds, "TODO")
    if not run_cmds:
        add_unique(run_cmds, "TODO")
    if not build_cmds:
        add_unique(build_cmds, "TODO")
    if not test_cmds:
        add_unique(test_cmds, "TODO")
    if not lint_cmds:
        add_unique(lint_cmds, "TODO")

    return {
        "languages": languages,
        "frameworks": frameworks,
        "package_tools": package_tools,
        "runtime_requirements": runtime_requirements,
        "external_dependencies": external_dependencies,
        "config_files": config_files,
        "setup_cmds": setup_cmds,
        "run_cmds": run_cmds,
        "build_cmds": build_cmds,
        "test_cmds": test_cmds,
        "lint_cmds": lint_cmds,
        "directory_map": directory_map,
    }


def build_templates(timestamp: str, repo_root: Path) -> list[TemplateFile]:
    facts = detect_repo_facts(repo_root)

    languages_lines = lines_or_todo(
        facts["languages"], "TODO identify languages from repository files"
    )
    frameworks_lines = lines_or_todo(
        facts["frameworks"], "TODO identify framework(s)"
    )
    package_tools_lines = lines_or_todo(
        facts["package_tools"], "TODO identify package/build tool"
    )
    runtime_lines = lines_or_todo(
        facts["runtime_requirements"], "TODO identify runtime requirements"
    )
    external_lines = lines_or_todo(
        facts["external_dependencies"], "TODO identify external services/dependencies"
    )
    config_file_lines = lines_or_todo(
        facts["config_files"], "TODO list configuration files"
    )
    directory_map_lines = lines_or_todo(
        facts["directory_map"], "`path/`: TODO describe key directory"
    )

    setup_block = code_block(facts["setup_cmds"], "TODO")
    run_block = code_block(facts["run_cmds"], "TODO")
    build_block = code_block(facts["build_cmds"], "TODO")
    test_block = code_block(facts["test_cmds"], "TODO")
    lint_block = code_block(facts["lint_cmds"], "TODO")

    return [
        TemplateFile(
            "codex/memory.md",
            f"""# Memory

- Last Updated: {timestamp}
- Status: bootstrapped

## Current Objective
- Primary goal: TODO
- Definition of done: TODO

## Session Snapshot
- Latest user request: TODO
- Current workstream: TODO
- Why this matters now: TODO

## Durable Context
- Repository facts to preserve: TODO
- Active constraints (technical/product/time): TODO
- Important assumptions: TODO

## Decisions Log
- [{timestamp}] TODO: decision + reason + tradeoff

## Blockers and Risks
- Blocker: TODO | Owner: TODO | Next action: TODO
- Risk: TODO | Impact: TODO | Mitigation: TODO

## Open Questions
- Question: TODO
  - Discovery action: TODO
  - Expected source: TODO

## Next Actions (Priority Order)
1. TODO
2. TODO
3. TODO

## Change Notes
- [{timestamp}] Initialized memory baseline.
""",
        ),
        TemplateFile(
            "codex/prompt.md",
            f"""# Prompt Log

- Last Updated: {timestamp}
- Status: bootstrapped

## Latest Prompt
```text
TODO
```

## Prompt Interpretation
- User intent: TODO
- Constraints: TODO
- Requested output format: TODO
- Success criteria: TODO

## Prompt History
| Timestamp | Prompt Summary | Intent + Constraints | Outcome Link |
| --- | --- | --- | --- |
| {timestamp} | TODO | TODO | TODO |

## Clarifications and Ambiguities
- Ambiguity: TODO
  - Assumption taken: TODO
  - Risk of assumption: TODO

## Reusable Prompt Patterns
- Pattern: TODO
  - Works for: TODO
  - Notes: TODO
""",
        ),
        TemplateFile(
            "codex/repowiki.md",
            f"""# Repo Wiki

- Last Updated: {timestamp}
- Status: bootstrapped
- Scope: living operational wiki for this repository

## Repository Purpose
- Problem this repo solves: TODO
- Primary users/stakeholders: TODO
- Non-goals: TODO

## Product and Domain Glossary
- Term: TODO -> definition

## Tech Stack and Toolchain
- Languages:
{languages_lines}
- Frameworks:
{frameworks_lines}
- Package/build tools:
{package_tools_lines}
- Runtime requirements:
{runtime_lines}
- External services/dependencies:
{external_lines}

## Architecture Overview
- System shape (high level): TODO
- Key components and responsibilities:

| Component | Path | Responsibility | Depends On |
| --- | --- | --- | --- |
| TODO | `path/to/module` | TODO | TODO |

## Data and Control Flow
- Main request/processing path: TODO
- State storage and lifecycle: TODO
- Side effects and integrations: TODO

## Directory Map
{directory_map_lines}

## Configuration and Environment
- Config files:
{config_file_lines}
- Required env vars:

| Variable | Required | Default | Purpose | Source |
| --- | --- | --- | --- | --- |
| `TODO_VAR` | yes/no | TODO | TODO | TODO |

## Local Development
- Prerequisites: TODO
- Setup/bootstrap:
{setup_block}
- Run app/service:
{run_block}
- Build:
{build_block}
- Test:
{test_block}
- Lint/format:
{lint_block}

## Test Strategy and Quality Gates
- Test layers (unit/integration/e2e): TODO
- Required checks before merge: TODO
- Typical failure points: TODO

## Deployment and Release Notes
- Deployment process: TODO
- Environments (dev/stage/prod): TODO
- Rollback mechanism: TODO

## Observability and Operations
- Logging/metrics/tracing entry points: TODO
- Debug commands/playbooks: TODO
- On-call or incident notes: TODO

## Security and Compliance Notes
- AuthN/AuthZ boundaries: TODO
- Sensitive data handling: TODO
- Secret management boundaries: TODO

## Known Gaps, Tech Debt, and Open Questions
| Type | Item | Impact | Owner | Next Action |
| --- | --- | --- | --- | --- |
| Gap | TODO | TODO | TODO | TODO |

## Wiki Change Log
- [{timestamp}] Initialized wiki baseline template with auto-detected repo hints.
""",
        ),
        TemplateFile(
            "codex/plan.md",
            f"""# Plan

- Last Updated: {timestamp}
- Status: template-ready
- Rule: update when planning is requested or non-trivial implementation starts.

## Request Scope
- Request summary: TODO
- In scope: TODO
- Out of scope: TODO

## Assumptions and Dependencies
- Assumption: TODO
- Dependency: TODO

## Step-by-Step Plan
| Step ID | Step | Why | Owner | Status |
| --- | --- | --- | --- | --- |
| P1 | TODO | TODO | TODO | pending |
| P2 | TODO | TODO | TODO | pending |

## File-Level Change Plan
| File Path | Change Type | Purpose | Linked Step |
| --- | --- | --- | --- |
| `path/to/file` | modify/add/delete | TODO | P1 |

## Validation Plan
- Automated checks: TODO
- Manual checks: TODO
- Expected artifacts/evidence: TODO

## Risk and Rollback Plan
- Risk: TODO
- Mitigation: TODO
- Rollback strategy: TODO

## Execution Notes
- [{timestamp}] Plan template initialized.
""",
        ),
        TemplateFile(
            "codex/checklist.md",
            f"""# Change Checklist

- Last Updated: {timestamp}
- Status: template-ready
- Rule: keep aligned with `codex/plan.md` when code changes are planned or executed.

## Plan Mapping
| Plan Step | Checklist Item | Status | Evidence |
| --- | --- | --- | --- |
| P1 | TODO | [ ] | TODO |

## Pre-Implementation Checks
- [ ] Scope confirmed
- [ ] Risks reviewed
- [ ] Validation plan defined

## Implementation Checklist
- [ ] Code changes completed for planned files
- [ ] Unplanned changes documented and justified
- [ ] Docs/config updates applied

## File Change Ledger
| File Path | Purpose | Linked Step | Status |
| --- | --- | --- | --- |
| `path/to/file` | TODO | P1 | pending |

## Validation Results
| Check | Result (pass/fail/skip) | Notes |
| --- | --- | --- |
| TODO | TODO | TODO |

## Post-Implementation
- [ ] Plan and checklist synchronized
- [ ] Known follow-ups recorded
- [ ] Handoff notes recorded

## Notes
- [{timestamp}] Checklist template initialized.
""",
        ),
    ]


def write_file(path: Path, content: str, force: bool) -> str:
    existed_before = path.exists()
    if existed_before and not force:
        return "exists"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "updated" if existed_before else "created"


def ensure_codex_ignored(repo_root: Path) -> str:
    gitignore_path = repo_root / ".gitignore"
    ignore_entry = "/codex/"
    existed_before = gitignore_path.exists()

    if existed_before:
        lines = gitignore_path.read_text(encoding="utf-8").splitlines()
    else:
        lines = []

    normalized = {line.strip() for line in lines}
    aliases = {"codex/", "/codex/", "codex"}
    if normalized & aliases:
        return "exists"

    if lines and lines[-1].strip():
        lines.append("")
    lines.append("# Local Codex context")
    lines.append(ignore_entry)
    gitignore_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return "updated" if existed_before else "created"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize codex folder and context markdown files."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root path (default: current directory).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files with template content.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    timestamp = now_text()

    print(f"Repo root: {repo_root}")
    print(f"Timestamp: {timestamp}")

    for template in build_templates(timestamp, repo_root):
        target = repo_root / template.relative_path
        status = write_file(target, template.body, force=args.force)
        print(f"[{status}] {target}")

    gitignore_status = ensure_codex_ignored(repo_root)
    print(f"[{gitignore_status}] {repo_root / '.gitignore'} (ensure /codex/ ignored)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
