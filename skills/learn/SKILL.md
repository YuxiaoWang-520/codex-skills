---
name: "learn"
description: "Use when the user wants to save knowledge from the current session, review accumulated knowledge, or when the session has been long and instructive. Enables agents to extract reusable patterns from interactions and get smarter over time."
---

# Learn

**Turn conversations into lasting knowledge.** Extract, accumulate, and apply reusable knowledge from user interactions — across sessions and across projects.

## Why This Skill Exists

Every conversation between a developer and an agent contains high-value knowledge: corrections, patterns, facts, and preferences. Without a learning system, this knowledge evaporates when the session ends. The agent starts from zero next time, and the user has to teach the same things again.

This skill solves that by giving agents a structured way to:

1. **Extract** — identify reusable knowledge from the current session
2. **Evaluate** — filter noise, check duplicates, decide scope
3. **Store** — save as human-readable Markdown files
4. **Apply** — load learned knowledge in future sessions
5. **Evolve** — strengthen validated knowledge, prune outdated entries

## Quick Start

### Set up learned knowledge directories

```bash
# Claude Code
export SKILLS_HOME="${HOME}/.claude/skills"

# Codex
export SKILLS_HOME="${CODEX_HOME:-$HOME/.codex}/skills"

# Initialize directories
python3 "$SKILLS_HOME/learn/scripts/learn_manager.py" init
```

This creates:

```text
~/.claude/learned/            # Global knowledge (cross-project)
  corrections/
  patterns/
  facts/
  preferences/
```

For project-level knowledge, the directories are created under `.claude/learned/` in the project root when needed.

### Two commands, that's it

| Command | When to use |
|---------|-------------|
| `/learn` | Extract knowledge from the current session |
| `/learn-review` | Review, curate, and manage accumulated knowledge |

## Core Workflow: `/learn`

### Step 1 — Review the session

Scan the conversation for four types of reusable knowledge:

| Type | What to look for | Example |
|------|-----------------|---------|
| **Corrections** | User corrected the agent's approach | "Don't mock the DB in integration tests" |
| **Patterns** | Repeated workflow or coding convention | "Always run lint before commit in this repo" |
| **Facts** | Project/environment-specific truth | "Deploy pipeline requires staging approval" |
| **Preferences** | User's personal style preference | "Keep responses concise, no trailing summaries" |

**Priority order**: Corrections > Patterns > Facts > Preferences. Corrections are the highest value because they represent explicit user feedback that the agent got wrong.

### Step 2 — Filter noise

Skip these — they are NOT worth saving:

- Trivial fixes (typos, simple syntax errors)
- One-time issues (specific API outages, ephemeral bugs)
- Things already documented in CLAUDE.md, AGENTS.md, or project docs
- Information derivable from reading the current codebase
- Overly specific details that won't generalize

### Step 3 — Quality gate

For each candidate, make one of three decisions:

| Decision | Criteria | Action |
|----------|----------|--------|
| **Save** | Unique, actionable, will save time in future | Create new knowledge file |
| **Merge** | Valuable but overlaps existing knowledge | Append to existing file |
| **Skip** | Too specific, redundant, or low value | Do not save |

Before deciding, run these checks:

- [ ] Search existing `~/.claude/learned/` and `.claude/learned/` for keyword overlap
- [ ] Check if appending to an existing knowledge file would be better
- [ ] Confirm this is reusable, not a one-off

### Step 4 — Determine scope

Ask: "Would this knowledge be useful in a different project?"

| Scope | Where it saves | When to use |
|-------|---------------|-------------|
| **Global** | `~/.claude/learned/` | Generic patterns: security, git, debugging, tool usage, user preferences |
| **Project** | `.claude/learned/` | Project-specific: architecture conventions, deploy procedures, team agreements |

**When unsure, choose project.** It is safer to keep knowledge scoped and promote later than to pollute the global space.

### Step 5 — Save and report

Save each piece of knowledge as a Markdown file (see format below), then report to the user:

```
Learned from this session:

  [correction] Don't mock DB in integration tests  → .claude/learned/corrections/
  [pattern]    Use AppError class for all API errors → .claude/learned/patterns/
  [preference] Keep responses concise               → ~/.claude/learned/preferences/

  Merged 1 into existing knowledge:
    [fact] Deploy checklist updated (added staging step)

  Skipped 2 (too specific / already known)
```

This report is critical for user "feel" — it makes learning visible and tangible.

## Knowledge File Format

Each knowledge file is a standalone Markdown document with YAML frontmatter:

```markdown
---
type: correction
strength: medium
scope: project
learned: 2026-04-01
confirmed: 1
source: "User corrected: don't mock database in integration tests"
---

# Integration tests must use real database

Do not mock the database connection in integration tests. Mocked tests
can pass while the actual database migration is broken.

## When this applies
- Writing integration tests that involve database operations
- Setting up test fixtures for database-backed features

## When this does NOT apply
- Pure unit tests with no database dependency
- Testing business logic that is fully decoupled from storage
```

### Frontmatter fields

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `type` | yes | `correction`, `pattern`, `fact`, `preference` | Knowledge category |
| `strength` | yes | `weak`, `medium`, `strong` | How well-validated this knowledge is |
| `scope` | yes | `project`, `global` | Applicability range |
| `learned` | yes | `YYYY-MM-DD` | Date first learned |
| `confirmed` | yes | integer | Times validated/reinforced |
| `source` | yes | string | How this knowledge was acquired |

### Strength model

Three tiers — no floating-point pseudo-precision:

| Strength | Meaning | How to reach |
|----------|---------|-------------|
| `weak` | Seen once, not yet validated | Default for new knowledge |
| `medium` | Validated 2–3 times | `confirmed >= 2` or user said "that's right" |
| `strong` | Thoroughly validated | `confirmed >= 4` or user explicitly confirmed |

**Strength changes:**

- Knowledge applied successfully and not corrected → `confirmed += 1`
- User says "yes, exactly" or similar confirmation → jump to `strong`
- User says "no, that's wrong" → downgrade or delete
- Knowledge not used for extended period → no automatic decay (unlike ECC's float-based system, manual review handles cleanup)

## Review Workflow: `/learn-review`

### What it does

Lists all accumulated knowledge with statistics and lets the user curate.

### Step 1 — Show overview

Run the helper script to display statistics:

```bash
# Claude Code
python3 ~/.claude/skills/learn/scripts/learn_manager.py stats

# Codex
python3 "$CODEX_HOME/skills/learn/scripts/learn_manager.py" stats
```

Present the output to the user, showing counts by type, strength, and scope.

### Step 2 — List knowledge

```bash
python3 ~/.claude/skills/learn/scripts/learn_manager.py list
```

Show each entry with its type, strength, confirmed count, and one-line summary.

### Step 3 — User actions

The user can ask to:

| Action | How |
|--------|-----|
| **Delete** a knowledge entry | Remove the file |
| **Promote** project → global | Move file and update `scope` field |
| **Demote** global → project | Move file and update `scope` field |
| **Merge** two entries | Combine into one, sum confirmed counts |
| **Edit** an entry | Update content directly |
| **Strengthen** an entry | Set strength to `strong` |

### Promotion criteria

Suggest promoting a project-scoped knowledge entry to global when:

1. `strength` is `strong`
2. The knowledge does not reference project-specific details (file paths, team names, etc.)
3. The user confirms

```bash
python3 ~/.claude/skills/learn/scripts/learn_manager.py promote
```

This lists promotion candidates. The user decides — no automatic promotion.

## Knowledge Application

### In new sessions

At the start of a new session, the agent should:

1. Check if `~/.claude/learned/` exists — load `strong` and `medium` global knowledge
2. Check if `.claude/learned/` exists — load `strong` and `medium` project knowledge
3. Use loaded knowledge to inform behavior (respect corrections, follow patterns, remember facts, honor preferences)

### Selective loading

To avoid context window bloat:

- **Always load**: `strong` entries (these are validated, high-value)
- **Load if relevant**: `medium` entries (check if the current task domain matches)
- **Skip**: `weak` entries (too tentative to take action on — only surface if directly relevant)

### Application feedback

When the agent applies learned knowledge, briefly mention it:

> "Using real database for integration tests (learned: don't mock DB in integration tests)"

This reinforces the user's confidence that the agent is learning.

## Integration with repo-bootstrap

`learn` and `repo-bootstrap` are complementary:

| | repo-bootstrap | learn |
|--|----------------|-------|
| **What it stores** | Current project state, plans, progress | Reusable knowledge from interactions |
| **Where** | `.harness/` (project-internal) | `~/.claude/learned/` + `.claude/learned/` |
| **Lifecycle** | Changes with project activity | Accumulates over time |
| **Update frequency** | Every session | When knowledge is extracted |
| **Analogy** | Working memory | Long-term memory |

When both are active:

- `repo-bootstrap` handles "what is the project doing right now"
- `learn` handles "what has the agent learned from working with this user"
- No overlap — they serve different purposes

## Storage Structure

```text
~/.claude/learned/              # Global (cross-project)
├── corrections/
│   ├── no-db-mocks-in-integration.md
│   └── use-const-not-let.md
├── patterns/
│   ├── run-lint-before-commit.md
│   └── grep-before-edit.md
├── facts/
│   └── (global facts are rare)
└── preferences/
    ├── concise-responses.md
    └── chinese-comments.md

.claude/learned/                # Project-specific
├── corrections/
├── patterns/
│   └── use-repository-pattern.md
├── facts/
│   ├── deploy-needs-staging.md
│   └── ci-uses-node-20.md
└── preferences/
```

## Guardrails

- **One knowledge per file.** Do not create mega-files with multiple unrelated learnings.
- **Human-readable names.** File names should describe the knowledge: `no-db-mocks-in-integration.md`, not `learn-001.md`.
- **No code dumps.** Knowledge files capture patterns and rules, not entire code blocks.
- **No secrets.** Never save API keys, passwords, or credentials in knowledge files.
- **User consent.** Always show what will be saved and get confirmation before writing.
- **Don't duplicate rules.** If something is already enforced by a rule in `~/.claude/rules/`, don't save it as learned knowledge.
- **Don't duplicate memory.** If something belongs in auto-memory (`~/.claude/projects/.../memory/`), it's probably context, not reusable knowledge. Knowledge is about *how to work*, memory is about *what happened*.

## When to Suggest `/learn`

Proactively suggest running `/learn` when:

- The session has been long (15+ messages) and productive
- The user corrected the agent's approach
- A non-obvious debugging technique was used
- A project-specific convention was discovered
- The user explicitly taught the agent something

Do NOT suggest `/learn` for:

- Short sessions with simple tasks
- Sessions that only involved reading/exploring
- When the user seems busy or time-pressed

## References

- Knowledge file format details: `references/knowledge-format.md`
- Helper script usage: `scripts/learn_manager.py --help`

## Scripts

- `scripts/learn_manager.py`: Manage learned knowledge files — init directories, list entries, show statistics, search by keyword, promote scope, check for duplicates.
