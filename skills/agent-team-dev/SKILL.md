---
name: agent-team-dev
description: Coordinate coding tasks with a lean sub-agent team (max 4 sub-agents) using explicit role ownership and strict quality gates. Use when tasks need parallel design/implementation/testing/review handoffs with correctness as the top priority, efficiency second, and token optimization third.
---

# Agent Team Dev

Run coding as a compact accountable team: one Team Lead in main thread, plus up to 4 sub-agents.

Priority order for all decisions:

1. Correctness and requirement fulfillment.
2. Execution efficiency and cycle time.
3. Token/cost optimization (only when it does not reduce 1 or 2).

## Team Topology

Keep the main thread as Team Lead. Add up to 4 sub-agents from the roles below.

| Role | Agent Type | Ownership | Output |
| --- | --- | --- | --- |
| Team Lead (main thread) | n/a | Task contract, delegation plan, integration, final verification | Integrated solution and final report |
| Solution Architect | `explorer` | Read-only analysis | Design brief, file impact map, execution plan |
| Feature Engineer | `worker` | Production code files only | Minimal patch implementing behavior |
| Test Engineer | `worker` | Tests, fixtures, test config only | Failing-then-passing tests and test notes |
| Reviewer/Verifier | `explorer` | Read-only review | Risk-ranked findings and release recommendation |

## Real-World Problems This Skill Solves

- Scope drift across agents: fix with task contract + explicit non-goals.
- Merge conflicts from overlapping edits: fix with disjoint file ownership.
- Quality regressions from rushed parallel work: fix with staged verification and independent review.
- Slow progress from over-delegation: fix with mode-based staffing and round limits.
- Unnecessary token waste from repeated analysis: fix with one canonical architecture brief and short delta updates.

## Activation Checklist

1. Write a task contract before delegation.
2. Choose the collaboration mode that best protects correctness for current risk.
3. Assign disjoint file ownership per sub-agent.
4. Define stop conditions (round cap, no-op cutoff, escalation triggers).
5. Spawn only sidecar work in parallel; keep immediate blockers in main thread.
6. Enforce quality gates before final delivery.

## Task Contract Format

Create this in the main thread first:

```markdown
Objective:
Non-goals:
Constraints:
Definition of done:
Target files/modules:
Verification commands:
Risk level: low | medium | high
Collaboration mode:
Round cap:
Output budget:
```

## Collaboration Modes (Token-Aware)

- `Mode A: Fast Patch` (0-1 sub-agents): small low-risk change, clear implementation path.
- `Mode B: Build + Test` (2 sub-agents): behavior + tests can run in parallel.
- `Mode C: Full Safety` (3-4 sub-agents): high-risk change needs architecture and independent review.
- Prefer the smallest mode that still protects correctness.
- Escalate mode immediately when correctness risk is non-trivial.
- Never exceed 4 active sub-agents.

## Delegation Protocol

Send every sub-agent a scoped work packet:

```markdown
Role:
Objective:
Owned files/directories:
Do not edit:
Inputs:
Deliverables:
Validation to run:
Output budget:
```

For all `worker` roles, include this sentence:

```text
You are not alone in the codebase. Do not revert edits you did not make; adapt to existing changes.
```

## Output Contract (Keep Responses Compact)

- Solution Architect: <=12 bullets, include file impact map and top 3 risks only.
- Feature Engineer: changed file list + <=8 bullets + commands run.
- Test Engineer: changed test list + covered scenarios + pass/fail.
- Reviewer/Verifier: findings by severity, max 10 items total, include file references.
- Keep reports concise, but include all details required to validate correctness.

## Execution Sequence

1. Run architecture pass (if needed) with Solution Architect.
2. Run Feature Engineer and Test Engineer in parallel with non-overlapping write scopes.
3. Integrate patches in main thread and resolve conflicts centrally.
4. Run Reviewer/Verifier after integration for an independent pass.
5. Execute verification commands in main thread and close unresolved findings.
6. Stop when quality gates pass or escalate if blocked.

Round policy:

- Default round cap: 2 delegation rounds.
- Allow a 3rd round only for unresolved high-severity issues.
- If two consecutive sub-agent turns produce no actionable delta, stop delegating and continue in main thread.
- Override round caps whenever additional iteration is required to satisfy quality gates.

## Boundary Enforcement

- Enforce file-level ownership before spawn and before merge.
- Reject and re-scope any patch that edits files outside ownership.
- Keep integration centralized in Team Lead; sub-agents do not self-merge each other.
- Use `Do not edit` paths for shared infrastructure files unless explicitly assigned.

## Quality Gates

Do not mark complete until all gates pass:

1. Behavior gate: implementation satisfies task contract.
2. Test gate: relevant tests pass; new behavior has coverage.
3. Regression gate: no unrelated breakage in touched flows.
4. Review gate: Reviewer/Verifier has no unaddressed high-severity findings.
5. Evidence gate: final report includes changed files, commands run, and residual risks.

## Token and Throughput Guardrails

- These guardrails are secondary to correctness and required validation.
- Reuse prior artifacts; do not ask multiple agents to rediscover the same context.
- Use delta-first handoffs: only what changed since last checkpoint.
- Prefer one strong scoped prompt over multiple iterative clarifications.
- Use `wait_agent` only when the main thread is blocked on that output.
- Reuse existing sub-agent threads for follow-ups; avoid unnecessary respawns.
- Close idle agents once their output is integrated.
- Skip architecture/review roles on trivial low-risk edits where they add no value.

## Escalation Rules

- Escalate to user only for missing credentials, destructive irreversible operations, legal/policy risk, or contradictory requirements.
- If assumptions are needed, choose the safest reversible option and document it.
- If sub-agent outputs conflict, Team Lead reconciles and keeps a single source of truth in main thread.

## Anti-Patterns

- Do not let multiple sub-agents edit the same files unless explicitly planned.
- Do not parallelize tasks when the second task depends on the first task's result.
- Do not skip independent review on high-risk changes.
- Do not keep agents running without clear ownership or pending work.
- Do not request full restatements of repo context in every handoff.

## Reference

Read `references/operating-contract.md` for role-specific prompt templates, severity rubric, and a full runbook.
