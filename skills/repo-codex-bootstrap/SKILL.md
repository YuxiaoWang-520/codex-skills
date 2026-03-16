---
name: repo-codex-bootstrap
description: Initialize and maintain repository-level Codex context files under a `codex/` folder (`memory.md`, `prompt.md`, `repowiki.md`, `plan.md`, `checklist.md`) and keep `/codex/` ignored by git. Use when the user asks for one-click repository bootstrap, persistent context tracking, rolling memory updates, or plan/checklist-driven implementation review.
---

# Repo Codex Bootstrap

Create and maintain a `codex/` workspace in the repository root so future turns keep stable project memory and reviewable planning artifacts.

## Quick Start

1. Resolve repository root (default: current working directory).
2. Run:

```bash
python3 "$CODEX_HOME/skills/repo-codex-bootstrap/scripts/init_codex_docs.py" --repo-root <repo-root>
```

3. Confirm these files exist:
   - `codex/memory.md`
   - `codex/prompt.md`
   - `codex/repowiki.md`
   - `codex/plan.md`
   - `codex/checklist.md`
4. Confirm `.gitignore` contains `/codex/` so these files are never pushed.
5. Immediately fill in initial useful content for `memory.md`, `prompt.md`, and `repowiki.md`.

## Session-Start Required Read

Apply this at the start of every session where this skill is invoked.

1. Before analysis, planning, or edits, read `codex/memory.md` and `codex/prompt.md`.
2. Use both files as required context sources for the current session.
3. If either file is missing, initialize it first, then continue.
4. Do not skip this step, even for short or follow-up requests.

## Session and Turn-by-Turn Update Rules

Apply these rules on every interaction when this skill is invoked.

1. Always update `codex/memory.md`
   - Roll forward context for this interaction (append/update, do not reset).
   - Capture conversation summary for this turn.
   - Capture decisions, blockers, and next actions.
   - Keep old context concise instead of deleting it.
2. Always update `codex/prompt.md`
   - Roll forward the prompt history for this interaction (append/update, do not reset).
   - Append the user prompt from this turn.
   - Add a short "intent + constraints" interpretation.
3. Always update `codex/repowiki.md`
   - Keep it structured and current: purpose, architecture, stack, directory map, run/test/build commands, known gaps.
4. Update `codex/plan.md` only when user explicitly asks for a plan or asks for implementation that requires plan review first.
5. Update `codex/checklist.md` only when code changes are planned or executed.
   - Checklist must map to `plan.md` and include all modified files.
6. Ensure `/codex/` remains in `.gitignore` when initializing or updating docs.
7. Treat `memory.md` and `prompt.md` maintenance as mandatory recurring work for every session and every interaction using this skill.

## Plan and Checklist Contract

When `plan.md` is requested:
- Explain each step and why this approach is chosen.
- Include alternatives briefly only when useful.
- Include explicit file-level code change plan.

When `checklist.md` is requested:
- Record every code change after implementation.
- Include file path and one-line purpose per change.
- Keep entries aligned with `plan.md` steps.

## Content Quality Rules

- Prefer short, high-signal bullets.
- Use timestamps when appending new entries.
- Preserve existing information unless it is outdated or incorrect.
- If repository facts are unknown, write `TODO` placeholders instead of guessing.

## Resources

### scripts/
- `scripts/init_codex_docs.py`: idempotently creates `codex/` and the five markdown files with starter templates.
