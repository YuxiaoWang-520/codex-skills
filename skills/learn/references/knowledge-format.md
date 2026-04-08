# Knowledge File Format Reference

Every piece of learned knowledge is a standalone Markdown file with YAML frontmatter.

## File naming

Use descriptive kebab-case names: `no-db-mocks-in-integration.md`, `always-run-lint.md`.

Avoid generic names like `learn-001.md` or `pattern-2.md`.

## Template

```markdown
---
type: correction
strength: weak
scope: project
learned: 2026-04-01
confirmed: 0
source: "User corrected: description of what happened"
---

# Short, actionable title

One or two paragraphs explaining the knowledge. Be specific about
what to do (or not do) and why.

## When this applies
- Situation 1
- Situation 2

## When this does NOT apply
- Exception 1
- Exception 2
```

## Frontmatter fields

| Field | Type | Required | Values | Description |
|-------|------|----------|--------|-------------|
| `type` | string | yes | `correction`, `pattern`, `fact`, `preference` | Knowledge category |
| `strength` | string | yes | `weak`, `medium`, `strong` | Validation level |
| `scope` | string | yes | `project`, `global` | Applicability range |
| `learned` | date | yes | `YYYY-MM-DD` | When first extracted |
| `confirmed` | integer | yes | `0`+ | Times reinforced since extraction |
| `source` | string | yes | free text | How this was acquired |

## Examples by type

### Correction

```markdown
---
type: correction
strength: strong
scope: project
learned: 2026-03-15
confirmed: 4
source: "User corrected: don't mock database in integration tests"
---

# Integration tests must use real database

Do not mock the database connection in integration tests. The mock
tests passed but the production migration was broken — the mock
hid the incompatibility.

## When this applies
- Writing any test tagged `integration`
- Testing code paths that include database operations

## When this does NOT apply
- Pure unit tests for business logic with no DB dependency
- Performance benchmarks using in-memory stores by design
```

### Pattern

```markdown
---
type: pattern
strength: medium
scope: global
learned: 2026-02-20
confirmed: 3
source: "Observed: user always runs lint before commit"
---

# Run lint before every commit

Run the project's lint command before `git commit` to catch style
issues early. Check `package.json`, `Makefile`, or `pyproject.toml`
for the lint script name.

## When this applies
- Before every commit in any project
- Especially after refactoring or adding new files

## When this does NOT apply
- When the project has pre-commit hooks that already run lint
```

### Fact

```markdown
---
type: fact
strength: strong
scope: project
learned: 2026-03-01
confirmed: 2
source: "User explained deploy pipeline"
---

# Deploy requires staging approval

The production deploy pipeline has a manual approval gate after
the staging deployment. Do not expect changes to reach production
automatically — someone must approve in the CI dashboard.

## When this applies
- Discussing deploy timelines or release processes
- Planning feature rollouts

## When this does NOT apply
- Local development or testing environments
```

### Preference

```markdown
---
type: preference
strength: strong
scope: global
learned: 2026-01-10
confirmed: 6
source: "User asked: keep responses short"
---

# Keep responses concise

The user prefers short, direct responses. Lead with the answer,
skip filler words and preamble. Don't restate the question.
Don't add trailing summaries.

## When this applies
- All responses and explanations
- Code review comments

## When this does NOT apply
- When the user explicitly asks for detailed explanations
- When complex topics require thorough coverage
```

## Strength progression

```
New knowledge created → strength: weak, confirmed: 0
  ↓ Applied once without correction
strength: weak, confirmed: 1
  ↓ Applied again without correction
strength: medium, confirmed: 2
  ↓ Applied twice more
strength: strong, confirmed: 4
  ↓ User explicitly confirms ("yes, exactly")
strength: strong (immediate, regardless of confirmed count)
```

## Directory structure

```text
~/.claude/learned/ or ~/.codex/learned/   # Global (cross-project)
├── corrections/
├── patterns/
├── facts/
└── preferences/

<project-root>/.claude/learned/ or <project-root>/.codex/learned/  # Project-specific
├── corrections/
├── patterns/
├── facts/
└── preferences/
```

## Scope decision guide

| Knowledge type | Likely scope | Examples |
|---------------|-------------|---------|
| Security practices | **global** | "Validate all user input", "Never log secrets" |
| Git workflow | **global** | "Conventional commits", "Small focused PRs" |
| Tool preferences | **global** | "Grep before Edit", "Read before Write" |
| User style preferences | **global** | "Concise responses", "Chinese comments" |
| Framework conventions | **project** | "Use React hooks", "Django REST patterns" |
| File structure | **project** | "Tests in `__tests__/`", "Components in `src/ui/`" |
| Deploy/CI procedures | **project** | "Requires staging approval", "Uses Node 20" |
| Team agreements | **project** | "PRs need 2 approvers", "No force push to main" |
