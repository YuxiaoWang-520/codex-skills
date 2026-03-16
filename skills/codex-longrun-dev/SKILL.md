---
name: "codex-longrun-dev"
description: "Run stable long-horizon autonomous software development across many context windows with no routine human confirmations. Use when tasks require hours/days of coding, reliable cross-session handoff, one-feature-at-a-time progress, strict end-to-end verification, and clean-state commits after every session."
---

# Codex Longrun Dev

Execute long-running development as a repeatable harness, not as ad-hoc coding.

## Quick Start

1. Bootstrap harness artifacts in the repository root:

```bash
python3 "$CODEX_HOME/skills/codex-longrun-dev/scripts/bootstrap_longrun_harness.py" \
  --repo-root "$(pwd)" \
  --goal "<original user goal>"
```

2. Review and adjust `.codex-longrun/init.sh` so it can reliably run dependency setup + smoke checks.
3. Commit the harness files before implementing product features.

## Session Protocol

Follow this order in every new context window.

1. Get bearings
- Run `pwd`.
- Read `.codex-longrun/progress.md`.
- Read `.codex-longrun/feature_list.json`.
- Read `git log --oneline -20`.

2. Re-establish baseline
- Run `.codex-longrun/init.sh` (or `bash .codex-longrun/init.sh`).
- Fix existing breakage before building anything new.

3. Pick one feature
- Select exactly one highest-priority item with `passes: false`.
- Keep scope narrow enough to finish with validation in the same session.

4. Implement incrementally
- Make minimal code changes to satisfy the selected feature.
- Avoid unrelated refactors unless required to unblock the feature.

5. Validate like a user
- Run unit/integration checks relevant to changed code.
- Run end-to-end or realistic flow verification when applicable.
- Do not mark a feature done without evidence.

6. Update artifacts
- In `.codex-longrun/feature_list.json`, only update status fields (`passes`, `evidence`, `updated_at`, optional `notes`).
- Append a structured session entry to `.codex-longrun/progress.md`.

7. Leave clean handoff
- Ensure repo is in a mergeable state.
- Commit with a descriptive message tied to the feature ID.

## Autonomy Rules (No Human-in-the-loop by Default)

- Continue making reasonable implementation decisions without asking for confirmation.
- Ask only when blocked by missing external credentials, legal/policy risk, destructive irreversible operations, or contradictory requirements.
- Never declare project complete while required features still have `passes: false`.
- Never skip regression checks that could invalidate previously passing features.

## Definition Of Done Per Session

A session is complete only if all conditions are true:

1. One selected feature advanced to a verified state (or intentionally kept failing with explicit blocker notes).
2. `.codex-longrun/feature_list.json` and `.codex-longrun/progress.md` are updated.
3. Baseline smoke checks pass after the change.
4. A commit captures the session output.

## Recovery Rules

- If new changes break baseline behavior, restore a known-good state before continuing.
- Prefer `git revert` or targeted fixes over rewriting large areas.
- Record failure cause and recovery action in `progress.md`.

## References

- Read `references/operating-contract.md` for detailed templates, feature schema, and a strict per-session checklist.

## Scripts

- `scripts/bootstrap_longrun_harness.py`: Create `.codex-longrun/` artifacts (`init.sh`, `feature_list.json`, `progress.md`, `session_state.json`) with deterministic defaults.
