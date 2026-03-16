# Long-Run Operating Contract

Use this contract when running long-horizon coding across many context windows.

## File Contract

All files live under `.codex-longrun/`.

1. `init.sh`
- Run dependency setup and smoke checks deterministically.
- Exit non-zero on failure.
- Keep idempotent.

2. `feature_list.json`
- Track required functionality as structured machine-editable records.
- Prefer adding new feature items rather than rewriting existing accepted criteria.
- Only mark `passes: true` after explicit validation evidence is available.

3. `progress.md`
- Append-only session handoff log.
- Include what changed, what passed, what failed, and what should happen next.

4. `session_state.json`
- Track lightweight machine state (`last_green_commit`, `last_feature_id`, timestamps).

## Feature Schema

Use this JSON shape per feature item.

```json
{
  "id": "F-001",
  "category": "functional",
  "priority": "P0",
  "description": "Describe user-visible behavior.",
  "acceptance_criteria": [
    "Given/when/then style check 1",
    "Given/when/then style check 2"
  ],
  "passes": false,
  "evidence": "",
  "notes": "",
  "updated_at": ""
}
```

## Session Checklist (Strict)

1. Read state
- Read `progress.md`, `feature_list.json`, and `git log --oneline -20`.

2. Restore health
- Run `.codex-longrun/init.sh`.
- If broken, fix baseline first.

3. Select work
- Choose highest-priority failing feature.
- Lock to one feature.

4. Implement
- Deliver smallest safe patch.

5. Verify
- Run targeted tests.
- Run realistic E2E flow where applicable.
- Capture verification commands/results in `evidence`.

6. Persist handoff
- Update feature status fields.
- Append `progress.md` section with template below.

7. Finish clean
- Re-run smoke checks.
- Commit with `feat(F-XYZ): ...` / `fix(F-XYZ): ...` style.

## Progress Entry Template

```markdown
## Session <UTC timestamp>
- Feature: F-XYZ
- Objective: <one sentence>
- Changes:
  - <file and intent>
- Validation:
  - <command>: <result>
- Outcome: <pass/fail/partial>
- Next:
  - <next concrete action>
- Blockers:
  - <none or itemized blockers>
```

## Completion Gate

Declare project done only when:

1. Every required feature in `feature_list.json` has `passes: true`.
2. Baseline smoke checks pass from a clean session start.
3. Remaining risks (if any) are documented as explicit deferred items.
