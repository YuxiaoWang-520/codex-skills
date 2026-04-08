#!/usr/bin/env python3
"""Install harness-craft skills and always-on guardrails for Claude or Codex."""

from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path


FLAGSHIP_SKILLS = ("repo-bootstrap", "longrun-dev", "learn", "agent-team-dev")
MANAGED_BEGIN = "<!-- BEGIN harness-craft managed AGENTS block -->"
MANAGED_END = "<!-- END harness-craft managed AGENTS block -->"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def skills_root() -> Path:
    return repo_root() / "skills"


def rules_root() -> Path:
    return repo_root() / "rules"


def template_root() -> Path:
    return repo_root() / "templates" / "codex"


def available_skills() -> list[str]:
    return sorted(
        entry.name
        for entry in skills_root().iterdir()
        if entry.is_dir() and not entry.name.startswith(".")
    )


def resolve_skill_names(profile: str, requested: list[str]) -> list[str]:
    if requested:
        names = requested
    elif profile == "all":
        names = available_skills()
    else:
        names = list(FLAGSHIP_SKILLS)

    valid = set(available_skills())
    invalid = [name for name in names if name not in valid]
    if invalid:
        raise ValueError("Unknown skills: {0}".format(", ".join(invalid)))
    return names


def copy_tree(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest, dirs_exist_ok=True)


def install_skills(assistant: str, skill_names: list[str]) -> Path:
    if assistant == "claude":
        dest_root = Path.home() / ".claude" / "skills"
    else:
        codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        dest_root = codex_home / "skills"

    dest_root.mkdir(parents=True, exist_ok=True)
    for name in skill_names:
        copy_tree(skills_root() / name, dest_root / name)
    return dest_root


def render_codex_guardrails(include_python: bool) -> str:
    common = (template_root() / "AGENTS.common.md").read_text(encoding="utf-8").strip()
    sections = [common]
    if include_python:
        sections.append((template_root() / "AGENTS.python.md").read_text(encoding="utf-8").strip())
    body = "\n\n".join(section for section in sections if section)
    return "{0}\n{1}\n{2}\n".format(MANAGED_BEGIN, body, MANAGED_END)


def upsert_managed_block(existing_text: str, managed_block: str) -> str:
    pattern = re.compile(
        r"{0}.*?{1}\n?".format(re.escape(MANAGED_BEGIN), re.escape(MANAGED_END)),
        re.DOTALL,
    )
    if pattern.search(existing_text):
        updated = pattern.sub(managed_block, existing_text)
    else:
        stripped = existing_text.rstrip()
        if stripped:
            updated = "{0}\n\n{1}".format(stripped, managed_block)
        else:
            updated = managed_block
    if not updated.endswith("\n"):
        updated += "\n"
    return updated


def install_codex_guardrails(scope: str, project_root: Path | None, include_python: bool) -> Path:
    if scope == "project":
        if project_root is None:
            raise ValueError("--project-root is required when --scope project is used.")
        agents_path = project_root / ".codex" / "AGENTS.md"
    else:
        codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        agents_path = codex_home / "AGENTS.md"

    agents_path.parent.mkdir(parents=True, exist_ok=True)
    existing = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    agents_path.write_text(
        upsert_managed_block(existing, render_codex_guardrails(include_python)),
        encoding="utf-8",
    )
    return agents_path


def install_claude_rules(scope: str, project_root: Path | None, include_python: bool) -> Path:
    if scope == "project":
        if project_root is None:
            raise ValueError("--project-root is required when --scope project is used.")
        dest_root = project_root / ".claude" / "rules"
    else:
        dest_root = Path.home() / ".claude" / "rules"

    copy_tree(rules_root() / "common", dest_root / "common")
    if include_python:
        copy_tree(rules_root() / "python", dest_root / "python")
    return dest_root


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install harness-craft skills and always-on guardrails.",
    )
    parser.add_argument("--assistant", choices=["claude", "codex"], required=True)
    parser.add_argument("--profile", choices=["flagship", "all"], default="flagship")
    parser.add_argument("--skill", action="append", default=[], help="Install specific skill (repeatable).")
    parser.add_argument(
        "--scope",
        choices=["user", "project"],
        default="user",
        help="Guardrail installation scope. Skills are always installed at the user level.",
    )
    parser.add_argument(
        "--project-root",
        default=None,
        help="Project root for project-scoped guardrails. Defaults to current working directory.",
    )
    parser.add_argument(
        "--with-python-rules",
        action="store_true",
        help="Also install Python-specific rules/guardrails.",
    )
    parser.add_argument("--skip-skills", action="store_true")
    parser.add_argument("--skip-guardrails", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve() if args.project_root else Path.cwd().resolve()

    try:
        skill_names = resolve_skill_names(args.profile, args.skill)
    except ValueError as exc:
        parser.error(str(exc))

    if args.skip_skills and args.skip_guardrails:
        parser.error("Nothing to do: both --skip-skills and --skip-guardrails were set.")

    if not args.skip_skills:
        skills_dest = install_skills(args.assistant, skill_names)
        print("Installed {0} skill(s) to {1}".format(len(skill_names), skills_dest))
        for name in skill_names:
            print("  - {0}".format(name))

    if not args.skip_guardrails:
        if args.assistant == "claude":
            guardrail_dest = install_claude_rules(args.scope, project_root, args.with_python_rules)
            print("Installed Claude rules to {0}".format(guardrail_dest))
        else:
            guardrail_dest = install_codex_guardrails(args.scope, project_root, args.with_python_rules)
            print("Installed Codex guardrails to {0}".format(guardrail_dest))
            print("Restart Codex so new sessions pick up the updated AGENTS instructions.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
