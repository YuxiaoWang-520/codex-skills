#!/usr/bin/env python3
"""Bootstrap deterministic long-running development harness artifacts."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


@dataclass
class StackHints:
    stack: str
    dep_setup: str
    smoke_test: str
    notes: List[str]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_checked(cmd: List[str], cwd: Path) -> str:
    try:
        out = subprocess.check_output(cmd, cwd=str(cwd), text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return ""
    return out.strip()


def detect_stack(repo_root: Path) -> StackHints:
    notes: List[str] = []

    package_json = repo_root / "package.json"
    if package_json.exists():
        try:
            package = json.loads(package_json.read_text(encoding="utf-8"))
            scripts = package.get("scripts", {}) if isinstance(package, dict) else {}
        except Exception:
            scripts = {}

        if (repo_root / "pnpm-lock.yaml").exists():
            dep_setup = "pnpm install --frozen-lockfile || pnpm install"
            runner = "pnpm"
        elif (repo_root / "yarn.lock").exists():
            dep_setup = "yarn install --frozen-lockfile || yarn install"
            runner = "yarn"
        else:
            dep_setup = "npm ci || npm install"
            runner = "npm"

        smoke_test = "echo '[WARN] No smoke command configured yet. Update .codex-longrun/init.sh.'"
        for candidate in ("test:smoke", "test:e2e", "test", "lint"):
            if candidate in scripts:
                if runner == "npm":
                    smoke_test = f"npm run {candidate}"
                elif runner == "pnpm":
                    smoke_test = f"pnpm {candidate}"
                else:
                    smoke_test = f"yarn {candidate}"
                break

        if not scripts:
            notes.append("Detected package.json but no scripts were readable.")

        return StackHints(
            stack="node",
            dep_setup=dep_setup,
            smoke_test=smoke_test,
            notes=notes,
        )

    if (repo_root / "pyproject.toml").exists() or (repo_root / "requirements.txt").exists():
        dep_cmds = []
        if (repo_root / "requirements.txt").exists():
            dep_cmds.append("python3 -m pip install -r requirements.txt")
        if (repo_root / "pyproject.toml").exists():
            dep_cmds.append("python3 -m pip install -e .")

        dep_setup = " && ".join(dep_cmds) if dep_cmds else "echo '[INFO] Python project detected.'"
        smoke_test = "pytest -q || python3 -m pytest -q"

        return StackHints(
            stack="python",
            dep_setup=dep_setup,
            smoke_test=smoke_test,
            notes=notes,
        )

    if (repo_root / "go.mod").exists():
        return StackHints(
            stack="go",
            dep_setup="go mod download",
            smoke_test="go test ./...",
            notes=notes,
        )

    if (repo_root / "Cargo.toml").exists():
        return StackHints(
            stack="rust",
            dep_setup="cargo fetch",
            smoke_test="cargo test",
            notes=notes,
        )

    notes.append("Could not auto-detect stack. Customize .codex-longrun/init.sh manually.")
    return StackHints(
        stack="unknown",
        dep_setup="echo '[WARN] Unknown dependency setup. Update .codex-longrun/init.sh.'",
        smoke_test="echo '[WARN] Unknown smoke test. Update .codex-longrun/init.sh.'",
        notes=notes,
    )


def make_feature_list(goal: str, now: str) -> Dict[str, object]:
    features = [
        {
            "id": "F-000",
            "category": "planning",
            "priority": "P0",
            "description": "Expand the project goal into concrete end-to-end features with testable acceptance criteria.",
            "acceptance_criteria": [
                "feature_list.json contains at least 12 concrete product features",
                "each feature has user-visible behavior and acceptance criteria",
                "no existing feature items are deleted without explicit reason",
            ],
            "passes": False,
            "evidence": "",
            "notes": "Run this first if list is still generic.",
            "updated_at": "",
        },
        {
            "id": "F-001",
            "category": "infrastructure",
            "priority": "P0",
            "description": "Make startup and smoke checks deterministic via .codex-longrun/init.sh.",
            "acceptance_criteria": [
                "init.sh exits with code 0 when baseline is healthy",
                "init.sh fails fast with non-zero status on broken baseline",
                "dependency and smoke commands are documented in init.sh",
            ],
            "passes": False,
            "evidence": "",
            "notes": "",
            "updated_at": "",
        },
        {
            "id": "F-002",
            "category": "quality",
            "priority": "P1",
            "description": "Add or improve automated checks for changed behavior.",
            "acceptance_criteria": [
                "changed logic has targeted tests or deterministic validation",
                "regression checks cover previously passing core path",
            ],
            "passes": False,
            "evidence": "",
            "notes": "",
            "updated_at": "",
        },
    ]

    return {
        "project_goal": goal,
        "created_at": now,
        "rules": {
            "single_feature_per_session": True,
            "require_validation_evidence": True,
            "forbid_completion_if_any_feature_fails": True,
            "status_fields_only_update": ["passes", "evidence", "notes", "updated_at"],
        },
        "features": features,
    }


def make_progress_md(goal: str, now: str, stack: str, notes: List[str]) -> str:
    note_lines = "\n".join(f"- {n}" for n in notes) if notes else "- None"

    return f"""# Codex Long-Run Progress Log

- Original goal: {goal}
- Initialized at (UTC): {now}
- Detected stack: {stack}

## Session {now}
- Feature: HARNESS-INIT
- Objective: Bootstrap long-running harness artifacts.
- Changes:
  - Added .codex-longrun/init.sh
  - Added .codex-longrun/feature_list.json
  - Added .codex-longrun/session_state.json
- Validation:
  - bootstrap script completed successfully
- Outcome: pass
- Next:
  - Execute F-000 or F-001 first, then continue one feature per session.
- Blockers:
{note_lines}
"""


def make_init_sh(dep_setup: str, smoke_test: str) -> str:
    return f"""#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   .codex-longrun/init.sh            # deps + smoke
#   .codex-longrun/init.sh deps       # deps only
#   .codex-longrun/init.sh smoke      # smoke only

MODE="${{1:-all}}"

run_deps() {{
  echo "[init] Running dependency setup"
  {dep_setup}
}}

run_smoke() {{
  echo "[init] Running smoke checks"
  {smoke_test}
}}

case "$MODE" in
  deps)
    run_deps
    ;;
  smoke)
    run_smoke
    ;;
  all)
    run_deps
    run_smoke
    ;;
  *)
    echo "Unknown mode: $MODE"
    echo "Use: deps | smoke | all"
    exit 2
    ;;
esac
"""


def ensure_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | 0o111)


def write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, obj: Dict[str, object], force: bool) -> None:
    if path.exists() and not force:
        return
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bootstrap long-run Codex harness artifacts")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--goal", required=True, help="Original project goal")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing harness files if they already exist",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if not repo_root.exists():
        parser.error(f"repo root does not exist: {repo_root}")

    harness_dir = repo_root / ".codex-longrun"
    harness_dir.mkdir(parents=True, exist_ok=True)

    now = utc_now()
    stack_hints = detect_stack(repo_root)

    init_sh_path = harness_dir / "init.sh"
    feature_list_path = harness_dir / "feature_list.json"
    progress_path = harness_dir / "progress.md"
    session_state_path = harness_dir / "session_state.json"

    write_text(init_sh_path, make_init_sh(stack_hints.dep_setup, stack_hints.smoke_test), args.force)
    ensure_executable(init_sh_path)

    write_json(feature_list_path, make_feature_list(args.goal, now), args.force)
    write_text(progress_path, make_progress_md(args.goal, now, stack_hints.stack, stack_hints.notes), args.force)

    session_state = {
        "created_at": now,
        "updated_at": now,
        "last_session_utc": now,
        "last_green_commit": run_checked(["git", "rev-parse", "HEAD"], repo_root),
        "last_feature_id": "HARNESS-INIT",
        "status": "ready",
    }
    write_json(session_state_path, session_state, args.force)

    created = []
    for p in (init_sh_path, feature_list_path, progress_path, session_state_path):
        state = "overwritten" if args.force else "created-or-preserved"
        created.append(f"- {p}: {state}")

    print("[OK] Long-run harness bootstrap complete")
    print(f"[OK] Repo root: {repo_root}")
    print("\n".join(created))
    if stack_hints.notes:
        print("[INFO] Notes:")
        for note in stack_hints.notes:
            print(f"- {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
