# Agent Team Operating Contract

Use this runbook when applying `agent-team-dev` to real coding tasks.

## 0. Operating Principles

- Correctness and requirement fulfillment are always first priority.
- Efficiency is second priority.
- Token/cost optimization is third priority and must never weaken correctness or verification.
- Default to the smallest team that can safely finish the task.
- Keep one canonical task contract in main thread; all sub-agent work derives from it.
- Optimize for useful delta, not verbose narration.
- Prefer bounded parallelism over maximal parallelism.

## 1. Role Contracts

### Team Lead (main thread)

- Own the task contract, staffing plan, and final integration.
- Keep one source of truth for scope and acceptance criteria.
- Decide what to do locally versus delegate.
- Resolve merge conflicts and contradictory recommendations.
- Run final verification commands and publish final status.

### Solution Architect (`explorer`)

- Work read-only.
- Produce a concise design brief before coding starts.
- Define boundaries, risks, and file impact map.
- Recommend a staffing plan and write-scope split.

Deliverable:

```markdown
Architecture Brief
- Proposed approach:
- Alternatives considered:
- File impact map:
- Risk hotspots:
- Recommended team composition:
- Artifact ID: A1
```

### Feature Engineer (`worker`)

- Edit production code in assigned files only.
- Implement smallest safe patch that satisfies acceptance criteria.
- Avoid unrelated refactors.
- Return changed files and verification notes.

Deliverable:

```markdown
Implementation Report
- Changed files:
- Behavior implemented:
- Commands run:
- Remaining risks:
- Artifact ID: I1
```

### Test Engineer (`worker`)

- Own tests, fixtures, and test-only helpers/config.
- Add or update tests that demonstrate intended behavior and guard regressions.
- Prefer deterministic assertions over fragile timing checks.
- Return failing-before/passing-after evidence when feasible.

Deliverable:

```markdown
Test Report
- Changed test files:
- Scenarios covered:
- Commands run:
- Current pass/fail:
- Artifact ID: T1
```

### Reviewer/Verifier (`explorer`)

- Work on integrated diff only.
- Perform independent review for correctness, regressions, and maintainability.
- Report findings with severity and actionable fixes.

Deliverable:

```markdown
Review Findings
- High:
- Medium:
- Low:
- Recommendation: ship / fix-first
- Artifact ID: R1
```

## 2. Mode Selection Matrix

- Mode A (0-1 sub-agents): narrow, low-risk, single-module changes.
- Mode B (2 sub-agents): implementation and tests can run in parallel.
- Mode C (3-4 sub-agents): high-risk or architecture-sensitive work.
- Keep Team Lead in main thread at all times.
- Keep active sub-agents <= 4.
- Escalate mode whenever correctness risk, ambiguity, or regression risk justifies it.

## 3. Token Budget Policy

Set a response budget per role before spawning.
Apply these budgets only as soft constraints.
If more detail is required for correctness, request and allow expanded output.

- Solution Architect: <=350 tokens, <=12 bullets.
- Feature Engineer: <=450 tokens, changed files + <=8 bullets.
- Test Engineer: <=350 tokens, tests + scenario list + pass/fail.
- Reviewer/Verifier: <=350 tokens, max 10 findings.

Token-saving rules:

- Send only missing context, not full repo restatements.
- Use artifact references (`A1`, `I1`, `T1`, `R1`) in follow-up prompts.
- Ask for diff-focused updates, not repeated summaries.
- Reject outputs that exceed budget without adding actionable delta.
- Do not truncate outputs that contain necessary correctness evidence.

## 4. Prompt Templates

## 4.1 Solution Architect template

```text
You are the Solution Architect.
Objective: <task objective>
Constraints: <constraints>
Repository context: <key modules>
Output budget: <=350 tokens, <=12 bullets
Deliverable:
1) architecture brief
2) file impact map
3) risk hotspots
4) recommended staffing plan (<=4 sub-agents)
5) artifact id A1
Do not edit files.
```

## 4.2 Feature Engineer template

```text
You are the Feature Engineer.
Objective: <task objective>
Owned files/directories: <write scope>
Do not edit: <protected paths>
Acceptance criteria: <done conditions>
Validation commands: <commands>
Output budget: <=450 tokens
You are not alone in the codebase. Do not revert edits you did not make; adapt to existing changes.
Return:
- changed file list
- concise implementation delta
- commands run
- remaining risks
- artifact id I1
```

## 4.3 Test Engineer template

```text
You are the Test Engineer.
Objective: verify and guard <behavior>
Owned files/directories: <tests scope>
Do not edit: <production files unless explicitly allowed>
Validation commands: <commands>
Output budget: <=350 tokens
You are not alone in the codebase. Do not revert edits you did not make; adapt to existing changes.
Return changed test files, covered scenarios, pass/fail status, artifact id T1.
```

## 4.4 Reviewer/Verifier template

```text
You are the Reviewer/Verifier.
Review integrated changes for correctness and risk.
Deliver findings grouped by severity (High/Medium/Low) with exact file references.
Output budget: <=350 tokens, max 10 findings.
Return artifact id R1.
Do not edit files.
```

## 5. Integration Checklist (Team Lead)

1. Confirm each sub-agent stayed within owned files.
2. Merge production patch and test patch in main thread.
3. Re-run verification commands locally in main thread.
4. Ask Reviewer/Verifier for independent assessment on final integrated state.
5. Fix high-severity findings before declaring done.
6. Publish final evidence pack: changed files, commands, results, residual risks.

## 6. Boundary Control Checklist

1. Pre-spawn: write explicit `Owned files` and `Do not edit`.
2. Mid-run: if agent requests out-of-scope edits, re-scope before allowing changes.
3. Pre-merge: reject boundary-violating diffs and redelegate with corrected ownership.
4. Post-merge: ensure no overlap remained unresolved in final diff.

## 7. Round Limits and No-op Breaker

- Default max delegation rounds: 2.
- Third round allowed only for unresolved high-severity findings.
- If two consecutive outputs add no actionable delta, stop delegation and proceed in Team Lead.
- Close completed agents immediately to reduce coordination overhead.
- If quality gates are not met, continue with additional rounds or switch modes until resolved.

## 8. Severity Rubric

- High: security issues, data loss risk, broken core flow, wrong business logic.
- Medium: edge-case bugs, partial regressions, significant maintainability risks.
- Low: style issues, minor clarity improvements, non-blocking cleanup.

## 9. Failure and Recovery

- If a sub-agent is blocked, narrow scope and re-delegate with tighter constraints.
- If two sub-agents conflict, Team Lead decides based on acceptance criteria and tests.
- If verification fails, route fix to the role that owns the failing scope.
- If missing external credentials or irreversible operations are required, escalate to user.
