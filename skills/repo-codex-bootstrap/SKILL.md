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
5. First invocation in a repo must produce useful baseline content for all five docs (not placeholder-only content).

## Non-Negotiable Rules

1. At session start, read `codex/memory.md` and `codex/prompt.md` before analysis or edits.
2. For code or architecture tasks, also read `codex/repowiki.md` before planning implementation.
3. Do not leave any of the five files as single-line stubs or TODO-only placeholders.
4. Keep `/codex/` ignored in `.gitignore`.
5. Treat this as a living system: every invocation should either update content or explicitly confirm review status.

## Five-Document Responsibility Contract

| File | Primary responsibility | Minimum useful content | Update trigger |
| --- | --- | --- | --- |
| `memory.md` | Durable working memory across turns/sessions | latest objective, decisions, blockers, next actions, open questions | every interaction |
| `prompt.md` | Prompt and intent history | latest user prompt, interpreted intent/constraints, prompt history timeline | every interaction |
| `repowiki.md` | Repository operational wiki | architecture, module map, commands, env/config, testing, known gaps | when new repo facts are learned or changed |
| `plan.md` | Execution design for non-trivial work | request scope, assumptions, steps, file-level plan, validation/rollback | when plan is requested or non-trivial implementation starts |
| `checklist.md` | Execution ledger and completion tracking | task checklist mapped to plan, changed files, validation outcomes | when code change is planned/executed |

## First-Run Baseline Requirements

When bootstrapping a repo for the first time, fill all five docs with concrete baseline info.

1. `memory.md`
   - include current objective, key context, known risks, and immediate next actions.
2. `prompt.md`
   - include the exact latest prompt and a concise interpretation of intent + constraints.
3. `repowiki.md`
   - include at least: repo purpose, stack/toolchain, key directories, run/test/build commands, and known unknowns.
4. `plan.md`
   - include a reusable planning skeleton with assumptions, step format, file-impact section, and validation section.
5. `checklist.md`
   - include a reusable checklist skeleton with plan mapping, file-change log format, and validation checklist.

## Session and Turn-by-Turn Update Rules

Apply these rules on every interaction when this skill is invoked.

1. Always update `codex/memory.md`
   - roll context forward (append/update, never reset).
   - capture summary, decisions, blockers, and next actions.
2. Always update `codex/prompt.md`
   - append latest prompt and interpretation.
   - preserve historical prompts with timestamps.
3. Update `codex/repowiki.md` whenever repository facts evolve
   - architecture changes, command changes, new module ownership, env var changes, testing changes.
   - if nothing changed, add a short review timestamp note instead of rewriting the whole file.
4. Update `codex/plan.md` when planning is requested or implementation is non-trivial.
5. Update `codex/checklist.md` when code changes are planned or executed.
6. Keep `plan.md` and `checklist.md` aligned (step IDs or clear textual mapping).

## RepoWiki Depth Standard (Must Not Be Superficial)

`codex/repowiki.md` should be usable as a practical wiki, not a short summary. It must include:

1. Repository purpose and non-goals
2. Architecture overview and key data/control flow
3. Module ownership or responsibility map (by directory or component)
4. Directory map with important paths and what lives there
5. Local development prerequisites and commands (run, build, test, lint, format)
6. Runtime/config notes (env vars, config files, secrets handling boundaries)
7. Testing strategy and quality gates
8. Known gaps, tech debt, and open questions with next action hints

Quality checks for `repowiki.md`:
- commands are copy-runnable where possible.
- sections use concrete paths/names, not generic wording.
- unknowns are written as explicit TODO questions with discovery hints.

## Plan and Checklist Contract

When `plan.md` is active:
- include assumptions, dependencies, risks, and rollback intent.
- include explicit file-level change plan.
- include validation strategy before coding.

When `checklist.md` is active:
- reflect real execution progress (not generic template-only checkboxes).
- include every modified file and one-line purpose.
- include validation outcomes (pass/fail/skipped with reason).

## Content Quality Rules

- prefer short, high-signal bullets.
- use timestamps for appended entries.
- preserve useful history; summarize old content instead of deleting it.
- if facts are unknown, write explicit TODO questions and next discovery action.

## Anti-Patterns (Disallowed)

- One-paragraph `repowiki.md` with no runnable commands.
- `memory.md` or `prompt.md` not updated on an interaction where this skill is invoked.
- `plan.md` and `checklist.md` drifting with no mapping.
- wiping historical context instead of rolling it forward.

## Resources

### scripts/
- `scripts/init_codex_docs.py`: idempotently creates `codex/` and the five markdown files with detailed starter templates.
