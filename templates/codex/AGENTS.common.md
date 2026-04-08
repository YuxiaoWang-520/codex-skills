# harness-craft Codex Guardrails

These instructions are the Codex adaptation of harness-craft's always-on
`rules/` layer. Claude loads short markdown rules directly; Codex uses
`AGENTS.md` as its always-on instruction mechanism, so the installer renders
the same guardrails into a managed `AGENTS.md` block.

## Workflow

- Research and reuse before writing net-new implementation. Prefer existing
  repo patterns, proven libraries, and battle-tested open-source approaches
  over rebuilding solved problems.
- For non-trivial work, plan before coding. Identify dependencies, risks,
  validation, and rollback intent.
- Prefer test-first or TDD workflow for new behavior and bug fixes.
- After substantial code changes, perform a review pass focused on bugs,
  regressions, security issues, and missing tests before closing the task.

## Coding Style

- Prefer immutable updates over mutating shared state unless the surrounding
  design clearly depends on mutation.
- Keep functions focused and files cohesive. As working targets, prefer
  functions under about 50 lines and files under about 800 lines when practical.
- Avoid deep nesting when a flatter control flow is clearer.
- Handle errors explicitly and never silently swallow failures.
- Validate inputs at system boundaries. Never trust external data.

## Security

- Never hardcode secrets, credentials, or tokens. Use environment variables or
  a secret manager.
- Before commit or handoff, check for input validation, injection risks, XSS,
  CSRF, auth/authz correctness, unsafe file access, and sensitive-data leakage
  in logs or errors.
- Treat authentication, payments, user data, database queries, filesystem
  operations, external API calls, and cryptography as security-sensitive areas.

## Testing And Review

- Do not mark implementation complete without relevant verification.
- When the repo supports it, aim for at least 80% coverage on changed behavior.
- Cover unit and integration behavior where applicable, and add E2E coverage
  for critical user flows.
- If a correct test fails, fix the implementation before weakening the test.
- Before review or PR, run relevant tests, lint, and type checks; resolve merge
  conflicts; and summarize the full change set, not just the latest commit.

## Git

- Use conventional commit types when committing:
  `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`.

## Learned Knowledge

- At the start of a session, if learned knowledge exists, load strong and
  medium entries from the global Codex store and the nearest project store.
- Prefer Codex-native paths:
  `~/.codex/learned/` and `<repo>/.codex/learned/`.
- During migration, legacy Claude paths may also exist:
  `~/.claude/learned/` and `<repo>/.claude/learned/`.
- Apply learned knowledge in this order:
  corrections, patterns, facts, preferences.
- Never let learned knowledge override explicit user instructions.
- When learned knowledge materially affects a decision, mention it briefly.

## Notes

- Keep long workflows in skills; keep always-on constraints here.
- Restart Codex after installing or updating this block so new sessions pick it up.
