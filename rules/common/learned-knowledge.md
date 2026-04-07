# Learned Knowledge

## Session Start: Load Accumulated Knowledge

At the beginning of every session, check for learned knowledge and load it:

1. **Global knowledge** (`~/.claude/learned/`): Load all `strong` and `medium` entries
2. **Project knowledge** (`.claude/learned/`): Load all `strong` and `medium` entries
3. **Skip** `weak` entries unless directly relevant to the current task

Use the helper script for a quick overview:

```bash
# Claude Code
python3 ~/.claude/skills/learn/scripts/learn_manager.py list

# Codex
python3 "$CODEX_HOME/skills/learn/scripts/learn_manager.py" list
```

If the directories do not exist, skip silently — the user has not used `/learn` yet.

## Priority Order

Apply learned knowledge in this order:

1. **Corrections** — highest priority; the user explicitly corrected the agent before
2. **Patterns** — recurring workflows or coding conventions
3. **Facts** — project/environment-specific truths
4. **Preferences** — user's personal style preferences

## Application Rules

- When a decision is influenced by learned knowledge, briefly cite it:
  > "Using real database for integration tests (learned: don't mock DB)"
- NEVER override explicit user instructions with learned knowledge
- If learned knowledge conflicts with the current request, follow the user's instruction and flag the conflict
- Do not load knowledge files that contain project-specific paths when working in a different project

## Session Announcement

When learned knowledge is loaded, briefly announce it:

```
Loaded 8 project entries and 15 global entries from learned knowledge.
```

Keep the announcement to one line. Do not list every entry.
