#!/usr/bin/env python3
"""Initialize codex workspace markdown files for a repository."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class TemplateFile:
    relative_path: str
    body: str


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def build_templates(timestamp: str) -> list[TemplateFile]:
    return [
        TemplateFile(
            "codex/memory.md",
            f"""# Memory

- Last Updated: {timestamp}

## Conversation Snapshot
- Current objective: TODO
- Latest user request: TODO

## Decisions
- TODO

## Issues and Risks
- TODO

## Next Steps
- TODO
""",
        ),
        TemplateFile(
            "codex/prompt.md",
            f"""# Prompt Log

- Last Updated: {timestamp}

## Latest Prompt
```text
TODO
```

## Prompt History
- [{timestamp}] TODO
""",
        ),
        TemplateFile(
            "codex/repowiki.md",
            f"""# Repo Wiki

- Last Updated: {timestamp}

## Repository Purpose
- TODO

## Tech Stack
- TODO

## Architecture and Modules
- TODO

## Directory Map
- TODO

## Run and Build
- TODO

## Test and Validation
- TODO

## Known Gaps and Open Questions
- TODO
""",
        ),
        TemplateFile(
            "codex/plan.md",
            f"""# Plan

- Last Updated: {timestamp}
- Rule: update this file when a plan is explicitly requested.

## Request
- TODO

## Step-by-Step Plan
1. TODO

## File-Level Change Plan
- `path/to/file`: TODO

## Rationale
- Why this approach: TODO
- Why not alternatives: TODO
""",
        ),
        TemplateFile(
            "codex/checklist.md",
            f"""# Change Checklist

- Last Updated: {timestamp}
- Rule: keep this file aligned with `codex/plan.md` when code changes happen.

## Plan Mapping
- Plan step -> TODO

## File Changes
- [ ] `path/to/file`: TODO

## Validation
- [ ] TODO
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

    for template in build_templates(timestamp):
        target = repo_root / template.relative_path
        status = write_file(target, template.body, force=args.force)
        print(f"[{status}] {target}")

    gitignore_status = ensure_codex_ignored(repo_root)
    print(f"[{gitignore_status}] {repo_root / '.gitignore'} (ensure /codex/ ignored)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
