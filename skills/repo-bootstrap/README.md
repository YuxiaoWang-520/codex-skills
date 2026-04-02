# Repo Bootstrap

`repo-bootstrap` gives a repository a local agent memory system that survives context-window loss.

It maintains a `codex/` workspace in the repo root and keeps these files synchronized:

- `codex/state.json`
- `codex/memory.md`
- `codex/prompt.md`
- `codex/repowiki.md`
- `codex/plan.md`
- `codex/checklist.md`

`codex/state.json` is the source of truth. The markdown files are rendered views for humans and agents.

## What It Solves

Without durable local state, an agent has to rediscover repository context repeatedly. This skill is designed to:

- persist working memory across turns and sessions
- preserve prompt history and intent
- accumulate repository knowledge over time
- keep plan/checklist tracking aligned with implementation work
- prevent knowledge loss when the conversation context resets

## Current Model

The skill now works as a rolling sync system instead of a one-time template bootstrap.

On each invocation it can:

- inspect repo manifests and common files to refresh baseline facts
- merge the latest task context into `codex/state.json`
- preserve useful history instead of replacing it
- regenerate the markdown files from structured state
- keep `/codex/` ignored in `.gitignore`

It also captures legacy `codex/*.md` files into state archives when upgrading an older repo that did not have `codex/state.json`.

## Quick Start

Run a basic sync:

Claude Code:
```bash
python3 ~/.claude/skills/repo-bootstrap/scripts/init_docs.py \
  --repo-root <repo-root> \
  --latest-prompt "Analyze and improve this repository." \
  --intent "Persist durable repo knowledge for future turns." \
  --objective "Keep codex docs continuously synchronized." \
  --workstream "repository analysis" \
  --work-summary "Synced codex state for the current turn." \
  --next-action "Review generated docs"
```

Codex:
```bash
python3 "$CODEX_HOME/skills/repo-bootstrap/scripts/init_docs.py" \
  --repo-root <repo-root> \
  --latest-prompt "Analyze and improve this repository." \
  --intent "Persist durable repo knowledge for future turns." \
  --objective "Keep codex docs continuously synchronized." \
  --workstream "repository analysis" \
  --work-summary "Synced codex state for the current turn." \
  --next-action "Review generated docs"
```

For richer updates, pass a structured JSON payload:

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

You can also pass inline JSON:

Claude Code:
```bash
python3 ~/.claude/skills/repo-bootstrap/scripts/init_docs.py \
  --repo-root <repo-root> \
  --context-json '{"latest_prompt":"Update repo memory","intent":"Persist new repo knowledge"}'
```

Codex:
```bash
python3 "$CODEX_HOME/skills/repo-bootstrap/scripts/init_docs.py" \
  --repo-root <repo-root> \
  --context-json '{"latest_prompt":"Update repo memory","intent":"Persist new repo knowledge"}'
```

## Structured Context Payload

Supported top-level fields include:

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

Recommended object shapes:

- `decisions`: `{summary, reason, tradeoff}`
- `blockers`: `{item, owner, next_action}`
- `risks`: `{item, impact, mitigation}`
- `open_questions`: `{question, discovery_action, expected_source}`
- `plan.steps`: `{id, step, why, owner, status}`
- `plan.files`: `{path, change_type, purpose, linked_step}`
- `checklist.plan_mapping`: `{plan_step, item, status, evidence}`
- `checklist.files`: `{path, purpose, linked_step, status}`
- `checklist.validation_results`: `{check, result, notes}`

If you provide `plan` without `checklist`, the script will derive a checklist skeleton automatically.

## Expected Workflow

When using this skill in an agent workflow:

1. Read `codex/memory.md` and `codex/prompt.md` before starting analysis.
2. Read `codex/repowiki.md` before non-trivial code or architecture work.
3. Gather the latest task context during the turn.
4. Sync that context into `codex/state.json`.
5. Let the script regenerate all five markdown files.

This is what makes the skill improve over time instead of resetting to templates.

## Files

- `SKILL.md`: skill contract and usage rules
- `README.md`: human-readable overview and usage guide
- `agents/openai.yaml`: agent-facing display metadata and default prompt
- `scripts/init_docs.py`: bootstrap and rolling-sync implementation
- `tests/test_init_docs.py`: regression tests for bootstrap, rolling memory updates, and plan/checklist alignment

## Verification

The current implementation is covered by automated tests for:

- useful first-run baseline generation
- rolling prompt and memory history updates
- plan/checklist synchronization

Run:

```bash
python3 skills/repo-bootstrap/tests/test_init_docs.py
```

## Notes

- `codex/state.json` is local memory and should remain out of git.
- The markdown files are rendered views, not the canonical state.
- Unknown facts should be recorded as explicit gaps or next discovery actions, not left as empty placeholders.
