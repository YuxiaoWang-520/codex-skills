#!/usr/bin/env python3
"""Initialize and continuously sync codex workspace files for a repository."""

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


STATE_VERSION = 2
MAX_HISTORY = 50


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def read_json_file(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(read_text(path))
    except Exception:
        return {}


def write_json_file(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def ensure_string_list(value: Any) -> List[str]:
    items = []
    for item in ensure_list(value):
        if item is None:
            continue
        text = str(item).strip()
        if text:
            items.append(text)
    return items


def unique_strings(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def merge_string_lists(existing: List[str], incoming: List[str], limit: Optional[int] = None) -> List[str]:
    merged = unique_strings(existing + incoming)
    if limit is not None:
        return merged[-limit:]
    return merged


def truncate_text(value: str, limit: int = 120) -> str:
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def first_meaningful_line(lines: List[str]) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def parse_readme(repo_root: Path) -> Dict[str, str]:
    for candidate in ["README.md", "README.mdx", "README.txt", "readme.md"]:
        readme_path = repo_root / candidate
        if readme_path.exists():
            lines = read_text(readme_path).splitlines()
            title = ""
            summary = ""
            paragraphs = []
            current_paragraph = []

            for line in lines:
                stripped = line.strip()
                if stripped.startswith("# ") and not title:
                    title = stripped[2:].strip()
                    continue
                if stripped:
                    current_paragraph.append(stripped)
                elif current_paragraph:
                    paragraphs.append(" ".join(current_paragraph))
                    current_paragraph = []

            if current_paragraph:
                paragraphs.append(" ".join(current_paragraph))

            if paragraphs:
                summary = paragraphs[0]

            return {"title": title, "summary": summary, "path": candidate}
    return {"title": "", "summary": "", "path": ""}


def npm_command_for_script(script_name: str, preferred_pm: str) -> str:
    if preferred_pm == "pnpm":
        return "pnpm {0}".format(script_name)
    if preferred_pm == "yarn":
        return "yarn {0}".format(script_name)
    return "npm run {0}".format(script_name)


def maybe_git_output(repo_root: Path, args: List[str]) -> str:
    try:
        output = subprocess.check_output(
            ["git", "-C", str(repo_root)] + args,
            stderr=subprocess.DEVNULL,
        )
        return output.decode("utf-8").strip()
    except Exception:
        return ""


def normalize_directory_entry(directory: str) -> Dict[str, str]:
    return {
        "path": "{0}/".format(directory),
        "description": "Needs deeper inspection.",
    }


def detect_repo_facts(repo_root: Path) -> Dict[str, Any]:
    readme = parse_readme(repo_root)
    repo_name = readme["title"] or repo_root.name
    repo_summary = readme["summary"] or "Repository summary not yet captured from source files."

    languages = []
    frameworks = []
    package_tools = []
    runtime_requirements = []
    external_dependencies = []
    config_files = []
    setup_cmds = []
    run_cmds = []
    build_cmds = []
    test_cmds = []
    lint_cmds = []
    directory_map = []
    known_unknowns = []
    repo_facts = []

    package_json = repo_root / "package.json"
    pnpm_lock = repo_root / "pnpm-lock.yaml"
    yarn_lock = repo_root / "yarn.lock"
    package_lock = repo_root / "package-lock.json"

    preferred_pm = "npm"
    if pnpm_lock.exists():
        preferred_pm = "pnpm"
        package_tools.append("pnpm")
    elif yarn_lock.exists():
        preferred_pm = "yarn"
        package_tools.append("yarn")
    elif package_lock.exists() or package_json.exists():
        package_tools.append("npm")

    if package_json.exists():
        languages.append("JavaScript")
        runtime_requirements.append("Node.js")
        pkg = read_json_file(package_json)
        deps = pkg.get("dependencies", {}) or {}
        dev_deps = pkg.get("devDependencies", {}) or {}
        scripts = pkg.get("scripts", {}) or {}
        all_dep_names = set(list(deps.keys()) + list(dev_deps.keys()))

        if "typescript" in all_dep_names or (repo_root / "tsconfig.json").exists():
            languages.append("TypeScript")

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
        for dep_name in framework_map:
            if dep_name in all_dep_names:
                frameworks.append(framework_map[dep_name])

        if scripts:
            setup_cmds.append("{0} install".format(preferred_pm))
            for candidate in ["dev", "start", "serve"]:
                if candidate in scripts:
                    run_cmds.append(npm_command_for_script(candidate, preferred_pm))
                    break
            for candidate in ["build", "compile"]:
                if candidate in scripts:
                    build_cmds.append(npm_command_for_script(candidate, preferred_pm))
                    break
            for candidate in ["test", "test:unit", "test:ci"]:
                if candidate in scripts:
                    test_cmds.append(npm_command_for_script(candidate, preferred_pm))
                    break
            for candidate in ["lint", "format", "check"]:
                if candidate in scripts:
                    lint_cmds.append(npm_command_for_script(candidate, preferred_pm))

        package_name = pkg.get("name")
        if package_name:
            repo_facts.append("Package name: {0}".format(package_name))

    pyproject = repo_root / "pyproject.toml"
    requirements = repo_root / "requirements.txt"
    if pyproject.exists() or requirements.exists():
        languages.append("Python")
        runtime_requirements.append("Python 3")
        if (repo_root / "uv.lock").exists():
            package_tools.append("uv")
            setup_cmds.append("uv sync")
        elif (repo_root / "poetry.lock").exists():
            package_tools.append("poetry")
            setup_cmds.append("poetry install")
        else:
            package_tools.append("pip")
            if requirements.exists():
                setup_cmds.append("python3 -m pip install -r requirements.txt")
        test_cmds.append("pytest")
        lint_cmds.append("ruff check .")

    if (repo_root / "go.mod").exists():
        languages.append("Go")
        runtime_requirements.append("Go toolchain")
        package_tools.append("go modules")
        build_cmds.append("go build ./...")
        test_cmds.append("go test ./...")

    if (repo_root / "Cargo.toml").exists():
        languages.append("Rust")
        runtime_requirements.append("Rust toolchain")
        package_tools.append("cargo")
        build_cmds.append("cargo build")
        test_cmds.append("cargo test")
        lint_cmds.append("cargo clippy --all-targets --all-features")

    if (repo_root / "Dockerfile").exists() or (repo_root / "docker-compose.yml").exists():
        external_dependencies.append("Docker")

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
        "README.md",
    ]:
        if (repo_root / candidate).exists():
            config_files.append(candidate)

    try:
        top_dirs = sorted(
            [
                entry.name
                for entry in repo_root.iterdir()
                if entry.is_dir() and entry.name not in {".git", "codex", "node_modules", ".venv", "venv", "__pycache__"}
            ]
        )
    except Exception:
        top_dirs = []

    for directory in top_dirs[:12]:
        directory_map.append(normalize_directory_entry(directory))

    git_branch = maybe_git_output(repo_root, ["rev-parse", "--abbrev-ref", "HEAD"])
    git_remote = maybe_git_output(repo_root, ["remote", "get-url", "origin"])
    if git_branch:
        repo_facts.append("Default working branch observed during bootstrap: {0}".format(git_branch))
    if git_remote:
        repo_facts.append("Remote origin: {0}".format(git_remote))

    if not directory_map:
        known_unknowns.append("Directory responsibilities still need a first-pass walkthrough.")
    if not run_cmds:
        known_unknowns.append("No obvious run command detected; capture one after the first successful local start.")
    if not build_cmds:
        known_unknowns.append("No obvious build command detected from top-level manifests.")
    if not test_cmds:
        known_unknowns.append("No obvious test command detected from top-level manifests.")
    if not readme["path"]:
        known_unknowns.append("README is missing or empty; repository purpose should be captured manually.")

    return {
        "repo_name": repo_name,
        "repo_summary": repo_summary,
        "readme_path": readme["path"],
        "languages": unique_strings(languages),
        "frameworks": unique_strings(frameworks),
        "package_tools": unique_strings(package_tools),
        "runtime_requirements": unique_strings(runtime_requirements),
        "external_dependencies": unique_strings(external_dependencies),
        "config_files": unique_strings(config_files),
        "setup_cmds": unique_strings(setup_cmds),
        "run_cmds": unique_strings(run_cmds),
        "build_cmds": unique_strings(build_cmds),
        "test_cmds": unique_strings(test_cmds),
        "lint_cmds": unique_strings(lint_cmds),
        "directory_map": directory_map,
        "known_unknowns": unique_strings(known_unknowns),
        "repo_facts": unique_strings(repo_facts),
    }


def normalize_decision(item: Dict[str, Any], timestamp: str) -> Dict[str, str]:
    return {
        "timestamp": item.get("timestamp") or timestamp,
        "summary": str(item.get("summary") or "Decision summary not captured.").strip(),
        "reason": str(item.get("reason") or "Reason not captured.").strip(),
        "tradeoff": str(item.get("tradeoff") or "Tradeoff not captured.").strip(),
    }


def normalize_blocker(item: Dict[str, Any]) -> Dict[str, str]:
    return {
        "item": str(item.get("item") or "Blocker not captured.").strip(),
        "owner": str(item.get("owner") or "Unassigned").strip(),
        "next_action": str(item.get("next_action") or "No next action recorded.").strip(),
    }


def normalize_risk(item: Dict[str, Any]) -> Dict[str, str]:
    return {
        "item": str(item.get("item") or "Risk not captured.").strip(),
        "impact": str(item.get("impact") or "Impact not captured.").strip(),
        "mitigation": str(item.get("mitigation") or "Mitigation not captured.").strip(),
    }


def normalize_question(item: Dict[str, Any]) -> Dict[str, str]:
    return {
        "question": str(item.get("question") or "Open question not captured.").strip(),
        "discovery_action": str(item.get("discovery_action") or "Next discovery action not captured.").strip(),
        "expected_source": str(item.get("expected_source") or "Expected source not captured.").strip(),
    }


def normalize_plan(plan: Optional[Dict[str, Any]], timestamp: str) -> Dict[str, Any]:
    plan = plan or {}
    steps = []
    for raw_step in ensure_list(plan.get("steps")):
        if not isinstance(raw_step, dict):
            continue
        steps.append(
            {
                "id": str(raw_step.get("id") or "P{0}".format(len(steps) + 1)).strip(),
                "step": str(raw_step.get("step") or "Step details not captured.").strip(),
                "why": str(raw_step.get("why") or "Why not captured.").strip(),
                "owner": str(raw_step.get("owner") or "Codex").strip(),
                "status": str(raw_step.get("status") or "pending").strip(),
            }
        )

    files = []
    for raw_file in ensure_list(plan.get("files")):
        if not isinstance(raw_file, dict):
            continue
        files.append(
            {
                "path": str(raw_file.get("path") or "Not captured").strip(),
                "change_type": str(raw_file.get("change_type") or "modify").strip(),
                "purpose": str(raw_file.get("purpose") or "Purpose not captured.").strip(),
                "linked_step": str(raw_file.get("linked_step") or (steps[0]["id"] if steps else "P1")).strip(),
            }
        )

    validation = plan.get("validation") or {}
    if not isinstance(validation, dict):
        validation = {}

    return {
        "request_summary": str(plan.get("request_summary") or "No active implementation plan recorded.").strip(),
        "in_scope": ensure_string_list(plan.get("in_scope")) or ["Not yet captured."],
        "out_of_scope": ensure_string_list(plan.get("out_of_scope")) or ["Not yet captured."],
        "assumptions": ensure_string_list(plan.get("assumptions")) or ["No explicit assumptions recorded."],
        "dependencies": ensure_string_list(plan.get("dependencies")) or ["No explicit dependencies recorded."],
        "steps": steps,
        "files": files,
        "validation": {
            "automated_checks": ensure_string_list(validation.get("automated_checks")) or ["No automated checks recorded."],
            "manual_checks": ensure_string_list(validation.get("manual_checks")) or ["No manual checks recorded."],
            "artifacts": ensure_string_list(validation.get("artifacts")) or ["No artifacts recorded."],
        },
        "risks": ensure_string_list(plan.get("risks")) or ["No active plan-specific risks recorded."],
        "mitigations": ensure_string_list(plan.get("mitigations")) or ["No active mitigations recorded."],
        "rollback": str(plan.get("rollback") or "Rollback approach not captured.").strip(),
        "execution_notes": [
            {
                "timestamp": timestamp,
                "note": str(plan.get("execution_note") or "Plan synchronized from structured state.").strip(),
            }
        ],
    }


def derive_checklist_from_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    mapping = []
    for step in plan.get("steps", []):
        status = "[x]" if step.get("status") == "completed" else "[ ]"
        mapping.append(
            {
                "plan_step": step.get("id", "P1"),
                "item": step.get("step", "Checklist item not captured."),
                "status": status,
                "evidence": step.get("why", "No evidence recorded."),
            }
        )

    files = []
    for plan_file in plan.get("files", []):
        files.append(
            {
                "path": plan_file.get("path", "Not captured"),
                "purpose": plan_file.get("purpose", "Purpose not captured."),
                "linked_step": plan_file.get("linked_step", "P1"),
                "status": "pending",
            }
        )

    validation_results = []
    for check in plan.get("validation", {}).get("automated_checks", []):
        validation_results.append(
            {
                "check": check,
                "result": "pending",
                "notes": "Awaiting execution.",
            }
        )

    return {
        "plan_mapping": mapping,
        "pre_implementation": [
            {"item": "Scope confirmed", "status": "[x]" if mapping else "[ ]"},
            {"item": "Risks reviewed", "status": "[x]" if plan.get("risks") else "[ ]"},
            {"item": "Validation plan defined", "status": "[x]" if validation_results else "[ ]"},
        ],
        "implementation_checks": [
            {"item": "Code changes completed for planned files", "status": "[ ]"},
            {"item": "Unplanned changes documented and justified", "status": "[ ]"},
            {"item": "Docs/config updates applied", "status": "[ ]"},
        ],
        "files": files,
        "validation_results": validation_results,
        "post_implementation": [
            {"item": "Plan and checklist synchronized", "status": "[x]" if mapping else "[ ]"},
            {"item": "Known follow-ups recorded", "status": "[ ]"},
            {"item": "Handoff notes recorded", "status": "[ ]"},
        ],
        "notes": [
            {
                "timestamp": now_text(),
                "note": "Checklist derived automatically from the current plan.",
            }
        ],
    }


def normalize_checklist(checklist: Optional[Dict[str, Any]], plan: Dict[str, Any], timestamp: str) -> Dict[str, Any]:
    if not checklist:
        return derive_checklist_from_plan(plan)

    mapping = []
    for item in ensure_list(checklist.get("plan_mapping")):
        if not isinstance(item, dict):
            continue
        mapping.append(
            {
                "plan_step": str(item.get("plan_step") or "P1").strip(),
                "item": str(item.get("item") or "Checklist item not captured.").strip(),
                "status": str(item.get("status") or "[ ]").strip(),
                "evidence": str(item.get("evidence") or "Evidence not captured.").strip(),
            }
        )

    implementation_checks = []
    for item in ensure_list(checklist.get("implementation_checks")):
        if isinstance(item, dict):
            implementation_checks.append(
                {
                    "item": str(item.get("item") or "Implementation item not captured.").strip(),
                    "status": str(item.get("status") or "[ ]").strip(),
                }
            )
        else:
            implementation_checks.append({"item": str(item).strip(), "status": "[ ]"})

    files = []
    for item in ensure_list(checklist.get("files")):
        if not isinstance(item, dict):
            continue
        files.append(
            {
                "path": str(item.get("path") or "Not captured").strip(),
                "purpose": str(item.get("purpose") or "Purpose not captured.").strip(),
                "linked_step": str(item.get("linked_step") or "P1").strip(),
                "status": str(item.get("status") or "pending").strip(),
            }
        )

    validation_results = []
    for item in ensure_list(checklist.get("validation_results")):
        if not isinstance(item, dict):
            continue
        validation_results.append(
            {
                "check": str(item.get("check") or "Check not captured.").strip(),
                "result": str(item.get("result") or "pending").strip(),
                "notes": str(item.get("notes") or "Notes not captured.").strip(),
            }
        )

    post_implementation = []
    for item in ensure_list(checklist.get("post_implementation")):
        if isinstance(item, dict):
            post_implementation.append(
                {
                    "item": str(item.get("item") or "Post-implementation item not captured.").strip(),
                    "status": str(item.get("status") or "[ ]").strip(),
                }
            )
        else:
            post_implementation.append({"item": str(item).strip(), "status": "[ ]"})

    pre_implementation = []
    for item in ensure_list(checklist.get("pre_implementation")):
        if isinstance(item, dict):
            pre_implementation.append(
                {
                    "item": str(item.get("item") or "Pre-implementation item not captured.").strip(),
                    "status": str(item.get("status") or "[ ]").strip(),
                }
            )
        else:
            pre_implementation.append({"item": str(item).strip(), "status": "[ ]"})

    notes = []
    for item in ensure_list(checklist.get("notes")):
        if isinstance(item, dict):
            notes.append(
                {
                    "timestamp": str(item.get("timestamp") or timestamp).strip(),
                    "note": str(item.get("note") or "Checklist note not captured.").strip(),
                }
            )
        else:
            notes.append({"timestamp": timestamp, "note": str(item).strip()})

    normalized = {
        "plan_mapping": mapping,
        "pre_implementation": pre_implementation or derive_checklist_from_plan(plan)["pre_implementation"],
        "implementation_checks": implementation_checks or derive_checklist_from_plan(plan)["implementation_checks"],
        "files": files or derive_checklist_from_plan(plan)["files"],
        "validation_results": validation_results or derive_checklist_from_plan(plan)["validation_results"],
        "post_implementation": post_implementation or derive_checklist_from_plan(plan)["post_implementation"],
        "notes": notes or [{"timestamp": timestamp, "note": "Checklist synchronized from structured state."}],
    }

    plan_step_ids = [step.get("id", "P1") for step in plan.get("steps", [])]
    for step_id in plan_step_ids:
        if not any(item.get("plan_step") == step_id for item in normalized["plan_mapping"]):
            matching_step = None
            for step in plan.get("steps", []):
                if step.get("id") == step_id:
                    matching_step = step
                    break
            normalized["plan_mapping"].append(
                {
                    "plan_step": step_id,
                    "item": matching_step.get("step", "Checklist item not captured.") if matching_step else "Checklist item not captured.",
                    "status": "[ ]",
                    "evidence": "Auto-added to stay aligned with plan.md.",
                }
            )

    for plan_file in plan.get("files", []):
        if not any(item.get("path") == plan_file.get("path") for item in normalized["files"]):
            normalized["files"].append(
                {
                    "path": plan_file.get("path", "Not captured"),
                    "purpose": plan_file.get("purpose", "Purpose not captured."),
                    "linked_step": plan_file.get("linked_step", "P1"),
                    "status": "pending",
                }
            )

    return normalized


def build_initial_state(repo_root: Path, facts: Dict[str, Any], timestamp: str) -> Dict[str, Any]:
    repo_facts = merge_string_lists(
        [
            "Repository root: {0}".format(repo_root),
            "Captured automatically during bootstrap from repository manifests and common config files.",
        ],
        facts.get("repo_facts", []),
        limit=MAX_HISTORY,
    )

    plan = normalize_plan({}, timestamp)
    checklist = derive_checklist_from_plan(plan)

    return {
        "schema_version": STATE_VERSION,
        "created_at": timestamp,
        "updated_at": timestamp,
        "archives": {},
        "repo": {
            "name": facts.get("repo_name") or repo_root.name,
            "summary": facts.get("repo_summary") or "Repository summary not yet captured.",
            "purpose": facts.get("repo_summary") or "Repository purpose needs manual capture.",
            "stakeholders": ["Developers and agents working in this repository."],
            "non_goals": ["Persistent project context should not depend on chat history alone."],
            "glossary": [],
            "languages": facts.get("languages", []),
            "frameworks": facts.get("frameworks", []),
            "package_tools": facts.get("package_tools", []),
            "runtime_requirements": facts.get("runtime_requirements", []),
            "external_dependencies": facts.get("external_dependencies", []),
            "config_files": facts.get("config_files", []),
            "commands": {
                "setup": facts.get("setup_cmds", []) or ["Capture setup commands after first successful bootstrap."],
                "run": facts.get("run_cmds", []) or ["Capture the local run command after first successful start."],
                "build": facts.get("build_cmds", []) or ["Capture build command when known."],
                "test": facts.get("test_cmds", []) or ["Capture test command when known."],
                "lint": facts.get("lint_cmds", []) or ["Capture lint/format command when known."],
            },
            "directory_map": facts.get("directory_map", []),
            "architecture": ["High-level architecture has not been reviewed yet beyond manifest detection."],
            "data_flow": ["Primary data and control flow still need a first-pass walkthrough."],
            "required_env_vars": [],
            "test_strategy": [
                "Use detected automated commands as the first validation entry point.",
                "Add project-specific quality gates as they are discovered.",
            ],
            "deployment_notes": ["Deployment process has not been captured yet."],
            "observability_notes": ["Observability entry points have not been captured yet."],
            "security_notes": ["Security boundaries have not been captured yet."],
            "known_gaps": facts.get("known_unknowns", []),
            "facts": repo_facts,
            "review_log": [
                {
                    "timestamp": timestamp,
                    "summary": "Bootstrap baseline created from repository inspection.",
                }
            ],
        },
        "memory": {
            "objective": "Establish durable Codex context for this repository.",
            "definition_of_done": "Codex can recover repo knowledge from disk and keep it synchronized across turns.",
            "latest_user_request": "No explicit user prompt captured during bootstrap.",
            "workstream": "Repository bootstrap",
            "why_now": "Persistent context reduces repeated rediscovery in future sessions.",
            "repo_facts": repo_facts,
            "assumptions": [
                "The codex directory stays local-only and remains ignored by git.",
                "Detected manifest files are the best first-pass source of repo facts.",
            ],
            "decisions": [
                {
                    "timestamp": timestamp,
                    "summary": "Bootstrap codex docs with a machine-readable state file.",
                    "reason": "A single source of truth makes markdown regeneration and rolling updates deterministic.",
                    "tradeoff": "Adds one local JSON file under codex/ for structure.",
                }
            ],
            "blockers": [],
            "risks": [
                {
                    "item": "Some repo facts are still inferred from manifests instead of code inspection.",
                    "impact": "The first baseline may be incomplete or shallow.",
                    "mitigation": "Refresh repowiki whenever deeper repository facts are learned.",
                }
            ],
            "open_questions": [
                {
                    "question": "What are the highest-value modules and workflows in this repository?",
                    "discovery_action": "Inspect the top-level directories and primary entrypoints next.",
                    "expected_source": "Repository code structure and README.",
                }
            ],
            "next_actions": [
                "Review generated codex documents for repo-specific details.",
                "Capture the latest user request on the next interaction.",
                "Refresh repowiki after the first code or architecture deep dive.",
            ],
            "change_log": [
                {
                    "timestamp": timestamp,
                    "summary": "Initialized codex memory baseline.",
                }
            ],
        },
        "prompt_log": {
            "latest_prompt": "Captured automatically during bootstrap because no explicit prompt was provided.",
            "intent": "Initialize or refresh durable Codex repository memory files.",
            "constraints": ["Keep /codex/ ignored by git."],
            "requested_output_format": "Updated codex markdown files backed by state.json.",
            "success_criteria": ["All codex docs exist with useful baseline content."],
            "history": [
                {
                    "timestamp": timestamp,
                    "prompt": "Captured automatically during bootstrap because no explicit prompt was provided.",
                    "summary": "Bootstrap repo codex docs",
                    "intent": "Initialize durable repo memory",
                    "constraints": ["Keep /codex/ ignored by git."],
                    "outcome_link": "codex/*.md",
                }
            ],
            "clarifications": [],
            "patterns": [
                {
                    "pattern": "Bootstrap or refresh codex docs after major repo discoveries.",
                    "works_for": "Repository setup, planning, and long-running implementation sessions.",
                    "notes": "Use a structured context payload when updating plan/checklist state.",
                }
            ],
        },
        "plan": plan,
        "checklist": checklist,
    }


def capture_legacy_docs(repo_root: Path, state: Dict[str, Any], timestamp: str) -> None:
    archives = state.setdefault("archives", {})
    for doc_name in ["memory.md", "prompt.md", "repowiki.md", "plan.md", "checklist.md"]:
        doc_path = repo_root / "codex" / doc_name
        if not doc_path.exists():
            continue
        existing_text = read_text(doc_path).strip()
        if not existing_text:
            continue
        archive_key = doc_name.replace(".md", "")
        entries = archives.setdefault(archive_key, [])
        if entries:
            continue
        entries.append(
            {
                "timestamp": timestamp,
                "note": "Legacy markdown snapshot captured before state-backed sync.",
                "content": existing_text,
            }
        )


def load_state(repo_root: Path, facts: Dict[str, Any], timestamp: str, force: bool) -> Dict[str, Any]:
    state_path = repo_root / "codex" / "state.json"
    state = {}

    if state_path.exists() and not force:
        state = read_json_file(state_path)

    if not state or force:
        state = build_initial_state(repo_root, facts, timestamp)
        capture_legacy_docs(repo_root, state, timestamp)

    state["schema_version"] = STATE_VERSION
    state.setdefault("archives", {})
    state.setdefault("repo", {})
    state.setdefault("memory", {})
    state.setdefault("prompt_log", {})
    state.setdefault("plan", normalize_plan({}, timestamp))
    state.setdefault("checklist", derive_checklist_from_plan(state.get("plan", {})))
    return state


def update_prompt_log(state: Dict[str, Any], context: Dict[str, Any], timestamp: str) -> None:
    prompt_log = state.setdefault("prompt_log", {})

    latest_prompt = str(
        context.get("latest_prompt")
        or prompt_log.get("latest_prompt")
        or "No prompt captured for this interaction."
    ).strip()
    intent = str(
        context.get("intent")
        or prompt_log.get("intent")
        or "Intent not captured."
    ).strip()
    constraints = ensure_string_list(context.get("constraints")) or prompt_log.get("constraints") or []
    success_criteria = ensure_string_list(context.get("success_criteria")) or prompt_log.get("success_criteria") or []
    requested_output_format = str(
        context.get("requested_output_format")
        or prompt_log.get("requested_output_format")
        or "Updated codex docs."
    ).strip()

    prompt_log["latest_prompt"] = latest_prompt
    prompt_log["intent"] = intent
    prompt_log["constraints"] = constraints
    prompt_log["success_criteria"] = success_criteria
    prompt_log["requested_output_format"] = requested_output_format

    summary = str(context.get("prompt_summary") or truncate_text(latest_prompt, 80)).strip()
    history = prompt_log.setdefault("history", [])
    bootstrap_placeholder = "Captured automatically during bootstrap because no explicit prompt was provided."
    if (
        history
        and latest_prompt != bootstrap_placeholder
        and len(history) == 1
        and history[0].get("prompt") == bootstrap_placeholder
    ):
        history[:] = []
    new_entry = {
        "timestamp": timestamp,
        "prompt": latest_prompt,
        "summary": summary,
        "intent": intent,
        "constraints": constraints,
        "outcome_link": str(context.get("outcome_link") or "codex/*.md").strip(),
    }

    if not history or history[-1].get("prompt") != latest_prompt or history[-1].get("intent") != intent:
        history.append(new_entry)
    prompt_log["history"] = history[-MAX_HISTORY:]

    for clarification in ensure_list(context.get("clarifications")):
        if isinstance(clarification, dict):
            prompt_log.setdefault("clarifications", []).append(
                {
                    "ambiguity": str(clarification.get("ambiguity") or "Ambiguity not captured.").strip(),
                    "assumption": str(clarification.get("assumption") or "Assumption not captured.").strip(),
                    "risk": str(clarification.get("risk") or "Risk not captured.").strip(),
                }
            )


def update_repo_state(state: Dict[str, Any], facts: Dict[str, Any], context: Dict[str, Any], timestamp: str) -> None:
    repo = state.setdefault("repo", {})
    repo["name"] = str(context.get("repo_name") or repo.get("name") or facts.get("repo_name")).strip()
    repo["summary"] = str(context.get("repo_summary") or repo.get("summary") or facts.get("repo_summary")).strip()
    repo["purpose"] = str(context.get("repo_purpose") or repo.get("purpose") or repo["summary"]).strip()
    repo["stakeholders"] = merge_string_lists(
        ensure_string_list(repo.get("stakeholders")),
        ensure_string_list(context.get("stakeholders")),
        limit=20,
    ) or ["Developers and agents working in this repository."]
    repo["non_goals"] = merge_string_lists(
        ensure_string_list(repo.get("non_goals")),
        ensure_string_list(context.get("non_goals")),
        limit=20,
    ) or ["Persistent project context should not depend on chat history alone."]

    for key in ["languages", "frameworks", "package_tools", "runtime_requirements", "external_dependencies", "config_files"]:
        repo[key] = merge_string_lists(
            ensure_string_list(repo.get(key)),
            ensure_string_list(facts.get(key)),
            limit=30,
        )

    commands = repo.setdefault("commands", {})
    commands["setup"] = merge_string_lists(ensure_string_list(commands.get("setup")), ensure_string_list(facts.get("setup_cmds")), limit=20)
    commands["run"] = merge_string_lists(ensure_string_list(commands.get("run")), ensure_string_list(facts.get("run_cmds")), limit=20)
    commands["build"] = merge_string_lists(ensure_string_list(commands.get("build")), ensure_string_list(facts.get("build_cmds")), limit=20)
    commands["test"] = merge_string_lists(ensure_string_list(commands.get("test")), ensure_string_list(facts.get("test_cmds")), limit=20)
    commands["lint"] = merge_string_lists(ensure_string_list(commands.get("lint")), ensure_string_list(facts.get("lint_cmds")), limit=20)

    existing_dirs = repo.get("directory_map") or []
    directory_index = {}
    for item in existing_dirs:
        if isinstance(item, dict) and item.get("path"):
            directory_index[item["path"]] = item

    for item in facts.get("directory_map", []):
        path = item.get("path")
        if path and path not in directory_index:
            directory_index[path] = item

    for item in ensure_list(context.get("directory_map")):
        if isinstance(item, dict) and item.get("path"):
            directory_index[item["path"]] = {
                "path": str(item.get("path")).strip(),
                "description": str(item.get("description") or "Needs deeper inspection.").strip(),
            }
    repo["directory_map"] = [directory_index[key] for key in sorted(directory_index.keys())]

    repo["architecture"] = merge_string_lists(
        ensure_string_list(repo.get("architecture")),
        ensure_string_list(context.get("architecture")),
        limit=20,
    ) or ["High-level architecture has not been reviewed yet beyond manifest detection."]
    repo["data_flow"] = merge_string_lists(
        ensure_string_list(repo.get("data_flow")),
        ensure_string_list(context.get("data_flow")),
        limit=20,
    ) or ["Primary data and control flow still need a first-pass walkthrough."]
    repo["required_env_vars"] = merge_string_lists(
        ensure_string_list(repo.get("required_env_vars")),
        ensure_string_list(context.get("required_env_vars")),
        limit=30,
    )
    repo["test_strategy"] = merge_string_lists(
        ensure_string_list(repo.get("test_strategy")),
        ensure_string_list(context.get("test_strategy")),
        limit=20,
    ) or ["Use detected automated commands as the first validation entry point."]
    repo["deployment_notes"] = merge_string_lists(
        ensure_string_list(repo.get("deployment_notes")),
        ensure_string_list(context.get("deployment_notes")),
        limit=20,
    ) or ["Deployment process has not been captured yet."]
    repo["observability_notes"] = merge_string_lists(
        ensure_string_list(repo.get("observability_notes")),
        ensure_string_list(context.get("observability_notes")),
        limit=20,
    ) or ["Observability entry points have not been captured yet."]
    repo["security_notes"] = merge_string_lists(
        ensure_string_list(repo.get("security_notes")),
        ensure_string_list(context.get("security_notes")),
        limit=20,
    ) or ["Security boundaries have not been captured yet."]

    repo["known_gaps"] = merge_string_lists(
        ensure_string_list(repo.get("known_gaps")),
        ensure_string_list(facts.get("known_unknowns")) + ensure_string_list(context.get("known_gaps")),
        limit=40,
    )
    repo["facts"] = merge_string_lists(
        ensure_string_list(repo.get("facts")),
        ensure_string_list(facts.get("repo_facts")) + ensure_string_list(context.get("repo_facts")),
        limit=MAX_HISTORY,
    )
    review_summary = str(
        context.get("repowiki_review")
        or context.get("work_summary")
        or "Repository facts reviewed during codex sync."
    ).strip()
    repo.setdefault("review_log", []).append({"timestamp": timestamp, "summary": review_summary})
    repo["review_log"] = repo["review_log"][-MAX_HISTORY:]


def update_memory(state: Dict[str, Any], context: Dict[str, Any], timestamp: str) -> None:
    memory = state.setdefault("memory", {})

    memory["objective"] = str(context.get("objective") or memory.get("objective") or "Objective not captured.").strip()
    memory["definition_of_done"] = str(
        context.get("definition_of_done")
        or memory.get("definition_of_done")
        or "Definition of done not captured."
    ).strip()
    memory["latest_user_request"] = str(
        context.get("latest_prompt")
        or context.get("latest_user_request")
        or memory.get("latest_user_request")
        or "Latest user request not captured."
    ).strip()
    memory["workstream"] = str(context.get("workstream") or memory.get("workstream") or "Current workstream not captured.").strip()
    memory["why_now"] = str(context.get("why_now") or memory.get("why_now") or "Why-now context not captured.").strip()
    memory["repo_facts"] = merge_string_lists(
        ensure_string_list(memory.get("repo_facts")),
        ensure_string_list(context.get("repo_facts")),
        limit=MAX_HISTORY,
    )
    memory["assumptions"] = merge_string_lists(
        ensure_string_list(memory.get("assumptions")),
        ensure_string_list(context.get("assumptions")),
        limit=30,
    )

    for raw_item in ensure_list(context.get("decisions")):
        if isinstance(raw_item, dict):
            memory.setdefault("decisions", []).append(normalize_decision(raw_item, timestamp))
    memory["decisions"] = memory.get("decisions", [])[-MAX_HISTORY:]

    for raw_item in ensure_list(context.get("blockers")):
        if isinstance(raw_item, dict):
            memory.setdefault("blockers", []).append(normalize_blocker(raw_item))
    memory["blockers"] = memory.get("blockers", [])[-MAX_HISTORY:]

    for raw_item in ensure_list(context.get("risks")):
        if isinstance(raw_item, dict):
            memory.setdefault("risks", []).append(normalize_risk(raw_item))
    memory["risks"] = memory.get("risks", [])[-MAX_HISTORY:]

    for raw_item in ensure_list(context.get("open_questions")):
        if isinstance(raw_item, dict):
            memory.setdefault("open_questions", []).append(normalize_question(raw_item))
    memory["open_questions"] = memory.get("open_questions", [])[-MAX_HISTORY:]

    next_actions = ensure_string_list(context.get("next_actions"))
    if next_actions:
        memory["next_actions"] = unique_strings(next_actions)
    else:
        memory["next_actions"] = ensure_string_list(memory.get("next_actions")) or ["No next actions recorded."]

    work_summary = str(context.get("work_summary") or "Codex state synchronized.").strip()
    memory.setdefault("change_log", []).append({"timestamp": timestamp, "summary": work_summary})
    memory["change_log"] = memory["change_log"][-MAX_HISTORY:]


def update_plan_and_checklist(state: Dict[str, Any], context: Dict[str, Any], timestamp: str) -> None:
    existing_plan = state.get("plan") or normalize_plan({}, timestamp)
    if context.get("plan") is not None:
        existing_plan = normalize_plan(context.get("plan"), timestamp)
    state["plan"] = existing_plan
    state["checklist"] = normalize_checklist(context.get("checklist"), existing_plan, timestamp)


def apply_context(state: Dict[str, Any], facts: Dict[str, Any], context: Dict[str, Any], timestamp: str) -> Dict[str, Any]:
    update_prompt_log(state, context, timestamp)
    update_repo_state(state, facts, context, timestamp)
    update_memory(state, context, timestamp)
    update_plan_and_checklist(state, context, timestamp)
    state["updated_at"] = timestamp
    return state


def format_bullets(items: List[str], empty_text: str) -> str:
    if not items:
        return "- {0}".format(empty_text)
    return "\n".join("- {0}".format(item) for item in items)


def format_code_block(commands: List[str], empty_text: str) -> str:
    body = "\n".join(commands) if commands else empty_text
    return "```bash\n{0}\n```".format(body)


def format_table_row(values: List[str]) -> str:
    return "| {0} |".format(" | ".join(value.replace("\n", " ").strip() for value in values))


def render_memory(state: Dict[str, Any]) -> str:
    memory = state.get("memory", {})
    decisions = memory.get("decisions", [])[-10:]
    blockers = memory.get("blockers", [])[-10:]
    risks = memory.get("risks", [])[-10:]
    questions = memory.get("open_questions", [])[-10:]
    change_log = memory.get("change_log", [])[-10:]

    decision_lines = []
    for item in decisions:
        decision_lines.append(
            "- [{0}] {1} | reason: {2} | tradeoff: {3}".format(
                item.get("timestamp", ""),
                item.get("summary", ""),
                item.get("reason", ""),
                item.get("tradeoff", ""),
            )
        )

    blocker_lines = []
    for item in blockers:
        blocker_lines.append(
            "- Blocker: {0} | Owner: {1} | Next action: {2}".format(
                item.get("item", ""),
                item.get("owner", ""),
                item.get("next_action", ""),
            )
        )

    risk_lines = []
    for item in risks:
        risk_lines.append(
            "- Risk: {0} | Impact: {1} | Mitigation: {2}".format(
                item.get("item", ""),
                item.get("impact", ""),
                item.get("mitigation", ""),
            )
        )

    question_lines = []
    for item in questions:
        question_lines.append("- Question: {0}".format(item.get("question", "")))
        question_lines.append("  - Discovery action: {0}".format(item.get("discovery_action", "")))
        question_lines.append("  - Expected source: {0}".format(item.get("expected_source", "")))

    change_lines = []
    for item in change_log:
        change_lines.append("- [{0}] {1}".format(item.get("timestamp", ""), item.get("summary", "")))

    return """# Memory

- Last Updated: {updated_at}
- Status: active
- Source of Truth: `codex/state.json`

## Current Objective
- Primary goal: {objective}
- Definition of done: {definition_of_done}

## Session Snapshot
- Latest user request: {latest_user_request}
- Current workstream: {workstream}
- Why this matters now: {why_now}

## Durable Context
{repo_facts}

## Assumptions
{assumptions}

## Decisions Log
{decisions}

## Blockers
{blockers}

## Risks
{risks}

## Open Questions
{questions}

## Next Actions
{next_actions}

## Change Notes
{change_log}
""".format(
        updated_at=state.get("updated_at", ""),
        objective=memory.get("objective", "Objective not captured."),
        definition_of_done=memory.get("definition_of_done", "Definition of done not captured."),
        latest_user_request=memory.get("latest_user_request", "Latest user request not captured."),
        workstream=memory.get("workstream", "Current workstream not captured."),
        why_now=memory.get("why_now", "Why-now context not captured."),
        repo_facts=format_bullets(memory.get("repo_facts", []), "Repository facts not captured."),
        assumptions=format_bullets(memory.get("assumptions", []), "No assumptions recorded."),
        decisions="\n".join(decision_lines) if decision_lines else "- No decisions recorded yet.",
        blockers="\n".join(blocker_lines) if blocker_lines else "- No active blockers recorded.",
        risks="\n".join(risk_lines) if risk_lines else "- No active risks recorded.",
        questions="\n".join(question_lines) if question_lines else "- No open questions recorded.",
        next_actions=format_bullets(memory.get("next_actions", []), "No next actions recorded."),
        change_log="\n".join(change_lines) if change_lines else "- No change notes recorded.",
    )


def render_prompt_log(state: Dict[str, Any]) -> str:
    prompt_log = state.get("prompt_log", {})
    history_lines = [
        "| Timestamp | Prompt Summary | Intent + Constraints | Outcome Link |",
        "| --- | --- | --- | --- |",
    ]
    for item in prompt_log.get("history", [])[-20:]:
        constraints = ", ".join(item.get("constraints", [])) or "No constraints captured."
        history_lines.append(
            format_table_row(
                [
                    item.get("timestamp", ""),
                    item.get("summary", ""),
                    "{0}; {1}".format(item.get("intent", ""), constraints),
                    item.get("outcome_link", ""),
                ]
            )
        )

    clarification_lines = []
    for item in prompt_log.get("clarifications", [])[-10:]:
        clarification_lines.append("- Ambiguity: {0}".format(item.get("ambiguity", "")))
        clarification_lines.append("  - Assumption taken: {0}".format(item.get("assumption", "")))
        clarification_lines.append("  - Risk of assumption: {0}".format(item.get("risk", "")))

    pattern_lines = []
    for item in prompt_log.get("patterns", [])[-10:]:
        pattern_lines.append("- Pattern: {0}".format(item.get("pattern", "")))
        pattern_lines.append("  - Works for: {0}".format(item.get("works_for", "")))
        pattern_lines.append("  - Notes: {0}".format(item.get("notes", "")))

    return """# Prompt Log

- Last Updated: {updated_at}
- Status: active
- Source of Truth: `codex/state.json`

## Latest Prompt
```text
{latest_prompt}
```

## Prompt Interpretation
- User intent: {intent}
- Constraints:
{constraints}
- Requested output format: {requested_output_format}
- Success criteria:
{success_criteria}

## Prompt History
{history}

## Clarifications and Ambiguities
{clarifications}

## Reusable Prompt Patterns
{patterns}
""".format(
        updated_at=state.get("updated_at", ""),
        latest_prompt=prompt_log.get("latest_prompt", "No prompt captured."),
        intent=prompt_log.get("intent", "Intent not captured."),
        constraints=format_bullets(prompt_log.get("constraints", []), "No constraints captured."),
        requested_output_format=prompt_log.get("requested_output_format", "Requested output format not captured."),
        success_criteria=format_bullets(prompt_log.get("success_criteria", []), "No success criteria captured."),
        history="\n".join(history_lines),
        clarifications="\n".join(clarification_lines) if clarification_lines else "- No clarifications recorded.",
        patterns="\n".join(pattern_lines) if pattern_lines else "- No reusable prompt patterns recorded.",
    )


def render_repowiki(state: Dict[str, Any]) -> str:
    repo = state.get("repo", {})

    component_lines = [
        "| Component | Path | Responsibility | Depends On |",
        "| --- | --- | --- | --- |",
    ]
    for entry in repo.get("directory_map", [])[:20]:
        component_lines.append(
            format_table_row(
                [
                    entry.get("path", ""),
                    entry.get("path", ""),
                    entry.get("description", ""),
                    "Needs deeper inspection",
                ]
            )
        )

    env_lines = [
        "| Variable | Required | Default | Purpose | Source |",
        "| --- | --- | --- | --- | --- |",
    ]
    required_env_vars = repo.get("required_env_vars", [])
    if required_env_vars:
        for item in required_env_vars:
            env_lines.append(format_table_row([item, "unknown", "unknown", "Captured from repository work", "manual"]))
    else:
        env_lines.append(format_table_row(["No env vars captured yet", "n/a", "n/a", "Add after config review", "manual"]))

    gaps_lines = [
        "| Type | Item | Impact | Owner | Next Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in repo.get("known_gaps", [])[:20]:
        gaps_lines.append(format_table_row(["Gap", item, "Repository context may be incomplete.", "Codex", "Update repowiki after discovery."]))

    review_lines = []
    for item in repo.get("review_log", [])[-10:]:
        review_lines.append("- [{0}] {1}".format(item.get("timestamp", ""), item.get("summary", "")))

    directory_lines = []
    for entry in repo.get("directory_map", [])[:20]:
        directory_lines.append("- `{0}`: {1}".format(entry.get("path", ""), entry.get("description", "")))

    return """# Repo Wiki

- Last Updated: {updated_at}
- Status: active
- Scope: living operational wiki for this repository
- Source of Truth: `codex/state.json`

## Repository Purpose
- Repository name: {repo_name}
- Problem this repo solves: {purpose}
- Primary users/stakeholders:
{stakeholders}
- Non-goals:
{non_goals}

## Product and Domain Glossary
{glossary}

## Tech Stack and Toolchain
- Languages:
{languages}
- Frameworks:
{frameworks}
- Package/build tools:
{package_tools}
- Runtime requirements:
{runtime_requirements}
- External services/dependencies:
{external_dependencies}

## Architecture Overview
- System shape (high level):
{architecture}
- Key components and responsibilities:
{component_table}

## Data and Control Flow
{data_flow}

## Directory Map
{directory_map}

## Configuration and Environment
- Config files:
{config_files}
- Required env vars:
{env_table}

## Local Development
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
{test_strategy}

## Deployment and Release Notes
{deployment_notes}

## Observability and Operations
{observability_notes}

## Security and Compliance Notes
{security_notes}

## Repository Facts Worth Preserving
{repo_facts}

## Known Gaps, Tech Debt, and Open Questions
{gaps_table}

## Wiki Change Log
{review_log}
""".format(
        updated_at=state.get("updated_at", ""),
        repo_name=repo.get("name", "Repository name not captured."),
        purpose=repo.get("purpose", "Repository purpose not captured."),
        stakeholders=format_bullets(repo.get("stakeholders", []), "No stakeholders captured."),
        non_goals=format_bullets(repo.get("non_goals", []), "No non-goals captured."),
        glossary=format_bullets(
            [
                "{0} -> {1}".format(item.get("term", ""), item.get("definition", ""))
                for item in repo.get("glossary", [])
                if isinstance(item, dict)
            ],
            "No glossary entries captured.",
        ),
        languages=format_bullets(repo.get("languages", []), "Languages not captured."),
        frameworks=format_bullets(repo.get("frameworks", []), "Frameworks not captured."),
        package_tools=format_bullets(repo.get("package_tools", []), "Package/build tools not captured."),
        runtime_requirements=format_bullets(repo.get("runtime_requirements", []), "Runtime requirements not captured."),
        external_dependencies=format_bullets(repo.get("external_dependencies", []), "No external dependencies captured."),
        architecture=format_bullets(repo.get("architecture", []), "Architecture notes not captured."),
        component_table="\n".join(component_lines),
        data_flow=format_bullets(repo.get("data_flow", []), "Data/control flow notes not captured."),
        directory_map="\n".join(directory_lines) if directory_lines else "- No directory map captured.",
        config_files=format_bullets(repo.get("config_files", []), "No config files captured."),
        env_table="\n".join(env_lines),
        setup_block=format_code_block(repo.get("commands", {}).get("setup", []), "Capture setup command after first successful bootstrap."),
        run_block=format_code_block(repo.get("commands", {}).get("run", []), "Capture run command after first successful start."),
        build_block=format_code_block(repo.get("commands", {}).get("build", []), "Capture build command when known."),
        test_block=format_code_block(repo.get("commands", {}).get("test", []), "Capture test command when known."),
        lint_block=format_code_block(repo.get("commands", {}).get("lint", []), "Capture lint/format command when known."),
        test_strategy=format_bullets(repo.get("test_strategy", []), "Test strategy not captured."),
        deployment_notes=format_bullets(repo.get("deployment_notes", []), "Deployment notes not captured."),
        observability_notes=format_bullets(repo.get("observability_notes", []), "Observability notes not captured."),
        security_notes=format_bullets(repo.get("security_notes", []), "Security notes not captured."),
        repo_facts=format_bullets(repo.get("facts", []), "No preserved repository facts captured."),
        gaps_table="\n".join(gaps_lines),
        review_log="\n".join(review_lines) if review_lines else "- No wiki review entries recorded.",
    )


def render_plan(state: Dict[str, Any]) -> str:
    plan = state.get("plan", {})
    step_lines = [
        "| Step ID | Step | Why | Owner | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in plan.get("steps", []):
        step_lines.append(
            format_table_row(
                [
                    item.get("id", ""),
                    item.get("step", ""),
                    item.get("why", ""),
                    item.get("owner", ""),
                    item.get("status", ""),
                ]
            )
        )
    if len(step_lines) == 2:
        step_lines.append(format_table_row(["P1", "No active implementation plan recorded.", "Add a structured plan when work becomes non-trivial.", "Codex", "pending"]))

    file_lines = [
        "| File Path | Change Type | Purpose | Linked Step |",
        "| --- | --- | --- | --- |",
    ]
    for item in plan.get("files", []):
        file_lines.append(
            format_table_row(
                [
                    item.get("path", ""),
                    item.get("change_type", ""),
                    item.get("purpose", ""),
                    item.get("linked_step", ""),
                ]
            )
        )
    if len(file_lines) == 2:
        file_lines.append(format_table_row(["No planned files yet", "n/a", "Capture when implementation starts.", "P1"]))

    note_lines = []
    for item in plan.get("execution_notes", [])[-10:]:
        note_lines.append("- [{0}] {1}".format(item.get("timestamp", ""), item.get("note", "")))

    return """# Plan

- Last Updated: {updated_at}
- Status: active
- Rule: update when planning is requested or non-trivial implementation starts.
- Source of Truth: `codex/state.json`

## Request Scope
- Request summary: {request_summary}
- In scope:
{in_scope}
- Out of scope:
{out_of_scope}

## Assumptions and Dependencies
- Assumptions:
{assumptions}
- Dependencies:
{dependencies}

## Step-by-Step Plan
{steps}

## File-Level Change Plan
{files}

## Validation Plan
- Automated checks:
{automated_checks}
- Manual checks:
{manual_checks}
- Expected artifacts/evidence:
{artifacts}

## Risk and Rollback Plan
- Risks:
{risks}
- Mitigations:
{mitigations}
- Rollback strategy: {rollback}

## Execution Notes
{notes}
""".format(
        updated_at=state.get("updated_at", ""),
        request_summary=plan.get("request_summary", "No active implementation plan recorded."),
        in_scope=format_bullets(plan.get("in_scope", []), "Not yet captured."),
        out_of_scope=format_bullets(plan.get("out_of_scope", []), "Not yet captured."),
        assumptions=format_bullets(plan.get("assumptions", []), "No assumptions recorded."),
        dependencies=format_bullets(plan.get("dependencies", []), "No dependencies recorded."),
        steps="\n".join(step_lines),
        files="\n".join(file_lines),
        automated_checks=format_bullets(plan.get("validation", {}).get("automated_checks", []), "No automated checks recorded."),
        manual_checks=format_bullets(plan.get("validation", {}).get("manual_checks", []), "No manual checks recorded."),
        artifacts=format_bullets(plan.get("validation", {}).get("artifacts", []), "No artifacts recorded."),
        risks=format_bullets(plan.get("risks", []), "No plan-specific risks recorded."),
        mitigations=format_bullets(plan.get("mitigations", []), "No mitigations recorded."),
        rollback=plan.get("rollback", "Rollback strategy not captured."),
        notes="\n".join(note_lines) if note_lines else "- No execution notes recorded.",
    )


def render_checklist(state: Dict[str, Any]) -> str:
    checklist = state.get("checklist", {})
    mapping_lines = [
        "| Plan Step | Checklist Item | Status | Evidence |",
        "| --- | --- | --- | --- |",
    ]
    for item in checklist.get("plan_mapping", []):
        mapping_lines.append(
            format_table_row(
                [
                    item.get("plan_step", ""),
                    item.get("item", ""),
                    item.get("status", ""),
                    item.get("evidence", ""),
                ]
            )
        )
    if len(mapping_lines) == 2:
        mapping_lines.append(format_table_row(["P1", "No checklist mapping recorded.", "[ ]", "Capture when a plan exists."]))

    file_lines = [
        "| File Path | Purpose | Linked Step | Status |",
        "| --- | --- | --- | --- |",
    ]
    for item in checklist.get("files", []):
        file_lines.append(
            format_table_row(
                [
                    item.get("path", ""),
                    item.get("purpose", ""),
                    item.get("linked_step", ""),
                    item.get("status", ""),
                ]
            )
        )
    if len(file_lines) == 2:
        file_lines.append(format_table_row(["No file changes recorded.", "Capture when implementation starts.", "P1", "pending"]))

    validation_lines = [
        "| Check | Result (pass/fail/skip/pending) | Notes |",
        "| --- | --- | --- |",
    ]
    for item in checklist.get("validation_results", []):
        validation_lines.append(
            format_table_row(
                [
                    item.get("check", ""),
                    item.get("result", ""),
                    item.get("notes", ""),
                ]
            )
        )
    if len(validation_lines) == 2:
        validation_lines.append(format_table_row(["No validation results recorded.", "pending", "Capture after running checks."]))

    notes = []
    for item in checklist.get("notes", [])[-10:]:
        notes.append("- [{0}] {1}".format(item.get("timestamp", ""), item.get("note", "")))

    return """# Change Checklist

- Last Updated: {updated_at}
- Status: active
- Rule: keep aligned with `codex/plan.md` when code changes are planned or executed.
- Source of Truth: `codex/state.json`

## Plan Mapping
{mapping}

## Pre-Implementation Checks
{pre_implementation}

## Implementation Checklist
{implementation_checks}

## File Change Ledger
{files}

## Validation Results
{validation}

## Post-Implementation
{post_implementation}

## Notes
{notes}
""".format(
        updated_at=state.get("updated_at", ""),
        mapping="\n".join(mapping_lines),
        pre_implementation=format_bullets(
            [
                "{0} {1}".format(item.get("status", "[ ]"), item.get("item", ""))
                for item in checklist.get("pre_implementation", [])
            ],
            "No pre-implementation checks recorded.",
        ),
        implementation_checks=format_bullets(
            [
                "{0} {1}".format(item.get("status", "[ ]"), item.get("item", ""))
                for item in checklist.get("implementation_checks", [])
            ],
            "No implementation checks recorded.",
        ),
        files="\n".join(file_lines),
        validation="\n".join(validation_lines),
        post_implementation=format_bullets(
            [
                "{0} {1}".format(item.get("status", "[ ]"), item.get("item", ""))
                for item in checklist.get("post_implementation", [])
            ],
            "No post-implementation checks recorded.",
        ),
        notes="\n".join(notes) if notes else "- No checklist notes recorded.",
    )


def render_docs(state: Dict[str, Any]) -> Dict[str, str]:
    return {
        "memory.md": render_memory(state),
        "prompt.md": render_prompt_log(state),
        "repowiki.md": render_repowiki(state),
        "plan.md": render_plan(state),
        "checklist.md": render_checklist(state),
    }


def write_file(path: Path, content: str) -> str:
    existed_before = path.exists()
    previous = read_text(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if not existed_before:
        return "created"
    if previous == content:
        return "unchanged"
    return "updated"


def ensure_codex_ignored(repo_root: Path) -> str:
    gitignore_path = repo_root / ".gitignore"
    ignore_entry = "/codex/"
    existed_before = gitignore_path.exists()

    if existed_before:
        lines = gitignore_path.read_text(encoding="utf-8").splitlines()
    else:
        lines = []

    normalized = set(line.strip() for line in lines)
    aliases = {"codex/", "/codex/", "codex"}
    if normalized.intersection(aliases):
        return "exists"

    if lines and lines[-1].strip():
        lines.append("")
    lines.append("# Local Codex context")
    lines.append(ignore_entry)
    gitignore_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "updated" if existed_before else "created"


def sync_codex_docs(repo_root: Path, context: Optional[Dict[str, Any]] = None, force: bool = False) -> Dict[str, Any]:
    repo_root = Path(repo_root).expanduser().resolve()
    timestamp = now_text()
    context = context or {}
    facts = detect_repo_facts(repo_root)
    state = load_state(repo_root, facts, timestamp, force)
    state = apply_context(state, facts, context, timestamp)

    docs_dir = repo_root / "codex"
    doc_statuses = {}
    for name, content in render_docs(state).items():
        doc_statuses[name] = write_file(docs_dir / name, content)

    state_status = write_file(docs_dir / "state.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    gitignore_status = ensure_codex_ignored(repo_root)

    return {
        "repo_root": str(repo_root),
        "timestamp": timestamp,
        "docs": doc_statuses,
        "state": state_status,
        "gitignore": gitignore_status,
    }


def parse_context_from_args(args: argparse.Namespace) -> Dict[str, Any]:
    context = {}
    if args.context_file:
        context.update(read_json_file(Path(args.context_file).expanduser().resolve()))
    if args.context_json:
        context.update(json.loads(args.context_json))

    if args.latest_prompt:
        context["latest_prompt"] = args.latest_prompt
    if args.intent:
        context["intent"] = args.intent
    if args.objective:
        context["objective"] = args.objective
    if args.workstream:
        context["workstream"] = args.workstream
    if args.work_summary:
        context["work_summary"] = args.work_summary
    if args.next_action:
        context["next_actions"] = ensure_string_list(context.get("next_actions")) + args.next_action

    return context


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize and sync codex folder and context markdown files."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root path (default: current directory).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild state from bootstrap defaults before applying the latest context.",
    )
    parser.add_argument(
        "--context-file",
        help="Path to a JSON file containing structured sync context.",
    )
    parser.add_argument(
        "--context-json",
        help="Inline JSON string containing structured sync context.",
    )
    parser.add_argument(
        "--latest-prompt",
        help="Latest user prompt to append to prompt history.",
    )
    parser.add_argument(
        "--intent",
        help="Interpreted intent for the latest prompt.",
    )
    parser.add_argument(
        "--objective",
        help="Current objective for memory.md.",
    )
    parser.add_argument(
        "--workstream",
        help="Current workstream label for memory.md.",
    )
    parser.add_argument(
        "--work-summary",
        help="Short summary to append to the memory change log.",
    )
    parser.add_argument(
        "--next-action",
        action="append",
        default=[],
        help="Repeatable next-action entry to store in memory.md.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    context = parse_context_from_args(args)
    result = sync_codex_docs(repo_root, context=context, force=args.force)

    print("Repo root: {0}".format(result["repo_root"]))
    print("Timestamp: {0}".format(result["timestamp"]))
    for doc_name in sorted(result["docs"].keys()):
        print("[{0}] {1}".format(result["docs"][doc_name], repo_root / "codex" / doc_name))
    print("[{0}] {1}".format(result["state"], repo_root / "codex" / "state.json"))
    print("[{0}] {1} (ensure /codex/ ignored)".format(result["gitignore"], repo_root / ".gitignore"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
