#!/usr/bin/env python3
"""
learn_manager.py — Manage learned knowledge files for the learn skill.

Commands:
    init      Create the learned knowledge directory structure
    list      List all knowledge entries with summaries
    stats     Show knowledge statistics
    search    Search knowledge by keyword
    promote   List or execute project-to-global promotions
    check-dup Check for duplicate knowledge entries

Usage:
    python3 learn_manager.py init [--project-root DIR]
    python3 learn_manager.py list [--scope global|project|all] [--type TYPE] [--strength STRENGTH]
    python3 learn_manager.py stats
    python3 learn_manager.py search KEYWORD
    python3 learn_manager.py promote [--execute] [--project-root DIR]
    python3 learn_manager.py check-dup TITLE
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

KNOWLEDGE_TYPES = ("corrections", "patterns", "facts", "preferences")
STRENGTHS = ("weak", "medium", "strong")


def get_global_dir() -> Path:
    """Return the global learned knowledge directory."""
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "learned"
    return Path.home() / ".claude" / "learned"


def get_project_dir(project_root: str | None = None) -> Path | None:
    """Return the project-level learned knowledge directory, or None."""
    if project_root:
        p = Path(project_root) / ".claude" / "learned"
        return p if p.exists() else None
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / ".claude" / "learned"
        if candidate.exists():
            return candidate
        if (parent / ".git").exists():
            return parent / ".claude" / "learned"
    return None


def parse_frontmatter(filepath: Path) -> dict:
    """Parse YAML-like frontmatter from a Markdown file."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm_block = text[3:end].strip()
    result = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.isdigit():
            result[key] = int(value)
        else:
            result[key] = value
    return result


def get_title(filepath: Path) -> str:
    """Extract the first heading from a knowledge file."""
    for line in filepath.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return filepath.stem.replace("-", " ").title()


def collect_entries(
    scope: str = "all",
    knowledge_type: str | None = None,
    strength: str | None = None,
    project_root: str | None = None,
) -> list[dict]:
    """Collect knowledge entries matching filters."""
    entries = []
    dirs_to_scan: list[tuple[Path, str]] = []

    if scope in ("all", "global"):
        gdir = get_global_dir()
        if gdir.exists():
            dirs_to_scan.append((gdir, "global"))

    if scope in ("all", "project"):
        pdir = get_project_dir(project_root)
        if pdir and pdir.exists():
            dirs_to_scan.append((pdir, "project"))

    for base, entry_scope in dirs_to_scan:
        type_dirs = [knowledge_type] if knowledge_type else KNOWLEDGE_TYPES
        for t in type_dirs:
            type_dir = base / t
            if not type_dir.is_dir():
                continue
            for f in sorted(type_dir.glob("*.md")):
                fm = parse_frontmatter(f)
                if strength and fm.get("strength") != strength:
                    continue
                # Normalize type to directory name (plural)
                raw_type = fm.get("type", t)
                norm_type = raw_type if raw_type in KNOWLEDGE_TYPES else raw_type + "s"
                if norm_type not in KNOWLEDGE_TYPES:
                    norm_type = t  # fallback to directory name
                entries.append({
                    "path": f,
                    "scope": entry_scope,
                    "type": norm_type,
                    "strength": fm.get("strength", "weak"),
                    "confirmed": fm.get("confirmed", 0),
                    "learned": fm.get("learned", "unknown"),
                    "title": get_title(f),
                    "source": fm.get("source", ""),
                })

    return entries


# ── Commands ─────────────────────────────────────────────────────────


def cmd_init(args: argparse.Namespace) -> None:
    """Create the learned knowledge directory structure."""
    global_dir = get_global_dir()
    print(f"[init] Global directory: {global_dir}")
    for t in KNOWLEDGE_TYPES:
        d = global_dir / t
        d.mkdir(parents=True, exist_ok=True)
        print(f"  [OK] {d}")

    if args.project_root:
        proj_dir = Path(args.project_root) / ".claude" / "learned"
        print(f"\n[init] Project directory: {proj_dir}")
        for t in KNOWLEDGE_TYPES:
            d = proj_dir / t
            d.mkdir(parents=True, exist_ok=True)
            print(f"  [OK] {d}")

    print("\n[init] Done. Directories are ready.")


def cmd_list(args: argparse.Namespace) -> None:
    """List all knowledge entries."""
    entries = collect_entries(
        scope=args.scope,
        knowledge_type=args.type,
        strength=args.strength,
        project_root=args.project_root,
    )
    if not entries:
        print("No knowledge entries found.")
        if not get_global_dir().exists():
            print("Hint: run 'learn_manager.py init' first.")
        return

    current_type = None
    for e in sorted(entries, key=lambda x: (x["type"], -x["confirmed"])):
        if e["type"] != current_type:
            current_type = e["type"]
            print(f"\n{'─' * 60}")
            print(f"  {current_type.upper()}")
            print(f"{'─' * 60}")
        scope_tag = "G" if e["scope"] == "global" else "P"
        strength_tag = {"weak": "○", "medium": "◐", "strong": "●"}[e["strength"]]
        print(
            f"  {strength_tag} [{scope_tag}] {e['title']}"
            f"  (confirmed: {e['confirmed']}, learned: {e['learned']})"
        )
        print(f"    {e['path']}")

    print(f"\nTotal: {len(entries)} entries")


def cmd_stats(args: argparse.Namespace) -> None:
    """Show knowledge statistics."""
    entries = collect_entries(project_root=args.project_root)

    if not entries:
        print("No knowledge entries found.")
        return

    # Counts by scope
    global_count = sum(1 for e in entries if e["scope"] == "global")
    project_count = sum(1 for e in entries if e["scope"] == "project")

    # Counts by type
    type_counts = {}
    for e in entries:
        type_counts[e["type"]] = type_counts.get(e["type"], 0) + 1

    # Counts by strength
    strength_counts = {}
    for e in entries:
        strength_counts[e["strength"]] = strength_counts.get(e["strength"], 0) + 1

    print("╔══════════════════════════════════════════╗")
    print("║         LEARNED KNOWLEDGE STATS          ║")
    print("╠══════════════════════════════════════════╣")
    print(f"║  Total entries:  {len(entries):<24}║")
    print(f"║  Global:         {global_count:<24}║")
    print(f"║  Project:        {project_count:<24}║")
    print("╠══════════════════════════════════════════╣")
    print("║  By type:                                ║")
    for t in KNOWLEDGE_TYPES:
        c = type_counts.get(t, 0)
        if c > 0:
            print(f"║    {t:<16} {c:<22}║")
    print("╠══════════════════════════════════════════╣")
    print("║  By strength:                            ║")
    for s in STRENGTHS:
        c = strength_counts.get(s, 0)
        icon = {"weak": "○", "medium": "◐", "strong": "●"}[s]
        print(f"║    {icon} {s:<14} {c:<22}║")
    print("╚══════════════════════════════════════════╝")


def cmd_search(args: argparse.Namespace) -> None:
    """Search knowledge by keyword."""
    keyword = args.keyword.lower()
    entries = collect_entries(project_root=args.project_root)
    matches = []

    for e in entries:
        text = e["path"].read_text(encoding="utf-8").lower()
        if keyword in text or keyword in e["title"].lower():
            matches.append(e)

    if not matches:
        print(f"No knowledge entries matching '{args.keyword}'.")
        return

    print(f"Found {len(matches)} entries matching '{args.keyword}':\n")
    for e in matches:
        scope_tag = "G" if e["scope"] == "global" else "P"
        strength_tag = {"weak": "○", "medium": "◐", "strong": "●"}[e["strength"]]
        print(f"  {strength_tag} [{scope_tag}] [{e['type']}] {e['title']}")
        print(f"    {e['path']}")


def cmd_promote(args: argparse.Namespace) -> None:
    """List or execute project-to-global promotions."""
    project_dir = get_project_dir(args.project_root)
    if not project_dir or not project_dir.exists():
        print("No project-level knowledge directory found.")
        return

    global_dir = get_global_dir()
    candidates = []
    for e in collect_entries(scope="project", project_root=args.project_root):
        if e["strength"] == "strong":
            # Check if content is project-specific
            text = e["path"].read_text(encoding="utf-8")
            has_project_refs = any(
                marker in text.lower()
                for marker in [
                    "this project", "this repo", "our team",
                    "in this codebase", ".env", "deploy to",
                ]
            )
            if not has_project_refs:
                candidates.append(e)

    if not candidates:
        print("No promotion candidates found.")
        print("Criteria: strength=strong, no project-specific references.")
        return

    print(f"Found {len(candidates)} promotion candidates:\n")
    for i, e in enumerate(candidates):
        print(f"  {i + 1}. [{e['type']}] {e['title']}")
        print(f"     confirmed: {e['confirmed']}, learned: {e['learned']}")
        print(f"     from: {e['path']}")

    if not args.execute:
        print("\nRun with --execute to promote these entries.")
        return

    for e in candidates:
        src = e["path"]
        dest = global_dir / e["type"] / src.name
        if dest.exists():
            print(f"  [SKIP] {src.name} — already exists in global")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Update scope in frontmatter
        content = src.read_text(encoding="utf-8")
        content = re.sub(r"^scope:\s*project", "scope: global", content, flags=re.MULTILINE)
        dest.write_text(content, encoding="utf-8")
        src.unlink()
        print(f"  [OK] {src.name} → global/{e['type']}/")

    print("\nPromotion complete.")


def cmd_check_dup(args: argparse.Namespace) -> None:
    """Check for duplicate knowledge entries."""
    title_lower = args.title.lower()
    entries = collect_entries(project_root=args.project_root)
    dupes = []

    for e in entries:
        if title_lower in e["title"].lower() or title_lower in e["path"].stem.replace("-", " "):
            dupes.append(e)

    if not dupes:
        print(f"No duplicates found for '{args.title}'.")
    else:
        print(f"Possible duplicates for '{args.title}':\n")
        for e in dupes:
            print(f"  [{e['scope']}] [{e['type']}] {e['title']}")
            print(f"    {e['path']}")


# ── Main ─────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manage learned knowledge files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # init
    p_init = sub.add_parser("init", help="Create directory structure")
    p_init.add_argument("--project-root", help="Also create project-level dirs here")

    # list
    p_list = sub.add_parser("list", help="List knowledge entries")
    p_list.add_argument("--scope", choices=["global", "project", "all"], default="all")
    p_list.add_argument("--type", choices=KNOWLEDGE_TYPES, default=None)
    p_list.add_argument("--strength", choices=STRENGTHS, default=None)
    p_list.add_argument("--project-root", default=None)

    # stats
    p_stats = sub.add_parser("stats", help="Show statistics")
    p_stats.add_argument("--project-root", default=None)

    # search
    p_search = sub.add_parser("search", help="Search by keyword")
    p_search.add_argument("keyword", help="Keyword to search for")
    p_search.add_argument("--project-root", default=None)

    # promote
    p_promote = sub.add_parser("promote", help="Promote project knowledge to global")
    p_promote.add_argument("--execute", action="store_true", help="Actually move files")
    p_promote.add_argument("--project-root", default=None)

    # check-dup
    p_dup = sub.add_parser("check-dup", help="Check for duplicate entries")
    p_dup.add_argument("title", help="Title or keyword to check")
    p_dup.add_argument("--project-root", default=None)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "init": cmd_init,
        "list": cmd_list,
        "stats": cmd_stats,
        "search": cmd_search,
        "promote": cmd_promote,
        "check-dup": cmd_check_dup,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
