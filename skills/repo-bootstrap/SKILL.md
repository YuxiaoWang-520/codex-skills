---
name: repo-bootstrap
description: Initialize and continuously maintain repository-level agent context under `codex/` using a state-backed memory system. Keeps `memory.md`, `prompt.md`, `repowiki.md`, `plan.md`, and `checklist.md` synchronized from `codex/state.json`, and keeps `/codex/` ignored by git. Use when the user asks for repository bootstrap, durable project memory, rolling context updates, or plan/checklist-driven implementation review.
---

# Repo Bootstrap

Create and maintain a `codex/` workspace in the repository root so future turns keep stable project memory, structured plan state, and reviewable execution artifacts.

This skill now uses `codex/state.json` as a local machine-readable source of truth. The five markdown files are rendered from that state so the agent can keep updating them without losing prior knowledge.

## When To Use It

- First-time repository bootstrap
- Ongoing work where the agent should persist memory across turns
- Non-trivial implementation that needs plan/checklist tracking
- Periodic repo-wiki refresh after architecture or workflow discovery
- Long-running sessions where prompt history and decisions should survive context-window loss

## Core Model

The durable memory model has two layers:

1. `codex/state.json`
   - structured source of truth for current memory, prompt log, repo facts, plan, and checklist state
   - preserves rolling history and allows deterministic markdown regeneration
2. Rendered markdown views
   - `codex/memory.md`
   - `codex/prompt.md`
   - `codex/repowiki.md`
   - `codex/plan.md`
   - `codex/checklist.md`

`/codex/` must remain gitignored.

## Quick Start

1. Resolve repository root.
2. Run a bootstrap or sync command:

Claude Code:
```bash
python3 ~/.claude/skills/repo-bootstrap/scripts/init_docs.py \
  --repo-root <repo-root> \
  --latest-prompt "Summarize and improve this repo bootstrap skill." \
  --intent "Persist durable repo memory and update the codex docs." \
  --objective "Upgrade repo-bootstrap to support rolling updates." \
  --workstream "skill enhancement" \
  --work-summary "Synced codex state for the current task." \
  --next-action "Run verification"
```

Codex:
```bash
python3 "$CODEX_HOME/skills/repo-bootstrap/scripts/init_docs.py" \
  --repo-root <repo-root> \
  --latest-prompt "Summarize and improve this repo bootstrap skill." \
  --intent "Persist durable repo memory and update the codex docs." \
  --objective "Upgrade repo-bootstrap to support rolling updates." \
  --workstream "skill enhancement" \
  --work-summary "Synced codex state for the current task." \
  --next-action "Run verification"
```

3. For richer updates, write a JSON payload and pass `--context-file`:

Claude Code:
```bash
python3 ~/.claude/skills/repo-bootstrap/scripts/init_docs.py \
  --repo-root <repo-root> \
  --context-file /tmp/codex-context.json
```

Codex:
```bash
python3 "$CODEX_HOME/skills/repo-bootstrap/scripts/init_docs.py" \
  --repo-root <repo-root> \
  --context-file /tmp/codex-context.json
```

4. Confirm these files exist:
   - `codex/state.json`
   - `codex/memory.md`
   - `codex/prompt.md`
   - `codex/repowiki.md`
   - `codex/plan.md`
   - `codex/checklist.md`
5. Confirm `.gitignore` contains `/codex/`.

## Required Turn Workflow

Apply this workflow every time the skill is invoked.

1. Read `codex/memory.md` and `codex/prompt.md` before analysis.
2. For code or architecture tasks, also read `codex/repowiki.md` before planning.
3. Before finishing the turn, sync the latest task context back into `codex/state.json`.
4. Let the script re-render the five markdown files from state.
5. If facts changed, update `repowiki.md` through the structured state instead of editing only the markdown view.

The skill is only doing its job if the state is refreshed continuously. Bootstrap alone is not enough.

## Non-Negotiable Rules

1. `codex/state.json` is the canonical local memory store.
2. `memory.md` and `prompt.md` must be refreshed on every invocation.
3. `repowiki.md` must be refreshed whenever repository facts evolve, or at minimum receive a review entry.
4. `plan.md` and `checklist.md` must stay aligned through shared step IDs or explicit mapping.
5. `/codex/` must stay ignored in `.gitignore`.
6. Do not wipe history just to keep docs tidy; summarize or trim old entries instead.
7. Do not rely on placeholder-only content after bootstrap.

## First-Run Baseline Expectations

The first run should produce useful baseline content automatically:

- repo name and summary from README when available
- stack/toolchain guesses from manifests and lockfiles
- detected run/build/test/lint commands
- top-level directory map placeholders with concrete paths
- initial memory objective, risks, next actions, and decisions
- initial prompt record even when no explicit prompt was supplied

Unknown facts are allowed, but they must be framed as explicit gaps or discovery actions, not empty stubs.

## Structured Update Payload

The script accepts structured context through `--context-file` or `--context-json`.

Supported top-level fields:

- `latest_prompt`
- `prompt_summary`
- `intent`
- `constraints`
- `success_criteria`
- `requested_output_format`
- `objective`
- `definition_of_done`
- `workstream`
- `why_now`
- `work_summary`
- `repo_facts`
- `assumptions`
- `decisions`
- `blockers`
- `risks`
- `open_questions`
- `next_actions`
- `repo_name`
- `repo_summary`
- `repo_purpose`
- `stakeholders`
- `non_goals`
- `directory_map`
- `architecture`
- `data_flow`
- `required_env_vars`
- `test_strategy`
- `deployment_notes`
- `observability_notes`
- `security_notes`
- `known_gaps`
- `repowiki_review`
- `plan`
- `checklist`

Recommended shapes:

- `decisions`: array of `{summary, reason, tradeoff}`
- `blockers`: array of `{item, owner, next_action}`
- `risks`: array of `{item, impact, mitigation}`
- `open_questions`: array of `{question, discovery_action, expected_source}`
- `plan.steps`: array of `{id, step, why, owner, status}`
- `plan.files`: array of `{path, change_type, purpose, linked_step}`
- `checklist.plan_mapping`: array of `{plan_step, item, status, evidence}`
- `checklist.files`: array of `{path, purpose, linked_step, status}`
- `checklist.validation_results`: array of `{check, result, notes}`

If `plan` is present and `checklist` is omitted, the script auto-derives a checklist skeleton from the plan.

## Five-Document Responsibility Contract

| File | Primary responsibility | Minimum useful content | Update trigger |
| --- | --- | --- | --- |
| `memory.md` | Durable working memory across turns/sessions | current objective, decisions, blockers, risks, open questions, next actions, change log | every interaction |
| `prompt.md` | Prompt and intent history | latest prompt, interpretation, constraints, success criteria, prompt timeline | every interaction |
| `repowiki.md` | Repository operational wiki | repo purpose, stack, commands, directory map, repo facts, known gaps | whenever facts are learned or reviewed |
| `plan.md` | Execution design for non-trivial work | request scope, assumptions, steps, file plan, validation, rollback | when planning is requested or work is non-trivial |
| `checklist.md` | Execution ledger and validation status | plan mapping, file ledger, validation results, post-implementation status | when code change is planned or executed |

## RepoWiki Depth Standard

`codex/repowiki.md` must remain a practical wiki, not a summary paragraph. It should stay useful for future sessions by including:

1. repository purpose and non-goals
2. architecture notes and control/data-flow hints
3. module or directory responsibility map
4. local development commands
5. runtime/config notes
6. test strategy and quality gates
7. operational/security notes when they become known
8. known gaps and explicit discovery actions

## Plan and Checklist Contract

When `plan.md` is active:

- record assumptions, dependencies, risks, mitigations, and rollback intent
- include explicit file-level change plans
- define validation before implementation

When `checklist.md` is active:

- track execution progress honestly
- include every modified file and one-line purpose
- record validation outcomes as `pass`, `fail`, `skip`, or `pending`
- stay aligned with plan step IDs

## Migration Behavior

If legacy codex markdown files exist but `codex/state.json` does not, the script captures those markdown files into state archives before rendering the new state-backed versions. This prevents silent knowledge loss during upgrade.

## Anti-Patterns

- Running bootstrap once and never syncing again
- Editing markdown views while ignoring `state.json`
- Letting `memory.md` or `prompt.md` go stale
- Allowing `plan.md` and `checklist.md` to drift apart
- Replacing explicit unknowns with generic TODO-only stubs
- Removing historical context without a summary

## Resources

### scripts/

- `scripts/init_docs.py`: bootstraps and continuously syncs `codex/state.json` plus the rendered markdown files.
