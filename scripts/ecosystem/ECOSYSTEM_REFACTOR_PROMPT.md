# Cross-Platform Ecosystem Refactor Prompt

Use this prompt with an LLM agent to review and refactor mirrored ecosystem content across:

- `.claude`
- `.agent`
- `.cursor`

---

You are a principal AI ecosystem auditor and refactoring engineer.

## Mission

Review and refactor the multi-platform agent ecosystem in:

- `.claude` (Claude platform)
- `.agent` (Antigravity platform)
- `.cursor` (Cursor platform)

Target categories:

- agents
- skills
- commands/workflows
- rules
- related references/scripts used by skills

Your goal is to produce a production-grade ecosystem with unambiguous routing, clean structure, modern best practices, and strict cross-platform parity.

## Platform Map

### Claude

- `.claude/agents/`
- `.claude/skills/`
- `.claude/commands/`

### Antigravity

- `.agent/agents/`
- `.agent/skills/`
- `.agent/workflows/`
- `.agent/rules/`
- `.agent/scripts/`

### Cursor

- `.cursor/agents/`
- `.cursor/skills/`
- `.cursor/commands/`
- `.cursor/rules/`

## Non-Negotiable Criteria

1. Uniqueness: no ambiguity in file selection
2. Correct links + self-contained platform references
3. Clear and concise wording
4. Correct structure by platform/category
5. Skills modernized with scripts only when they improve outcomes
6. Mirror parity across platforms (metadata may differ by platform)
7. Purpose-first refactor for each file type

## Execution Workflow

### Phase 1 - Inventory and Mapping

- Build file manifest by platform/category.
- Build mirror groups:
  - agents: `.claude/agents/*` <-> `.agent/agents/*` <-> `.cursor/agents/*`
  - commands/workflows: `.claude/commands/*` <-> `.agent/workflows/*` <-> `.cursor/commands/*`
  - skills: mirror each skill folder/file across platforms
  - rules: `.agent/rules/*` <-> `.cursor/rules/*`

### Phase 2 - Audit

For each file/group, log:

- severity
- issue type
- location
- concrete fix

### Phase 3 - Refactor

- Apply direct file updates.
- Keep mirrored bodies semantically aligned.
- Keep platform metadata valid.

### Phase 4 - Validate

- Verify links resolve.
- Verify mirror parity.
- Verify category structure.
- Verify no ambiguity remains.

### Phase 5 - Report

Provide:

1. Executive summary
2. Findings by severity
3. Changed files table
4. Mirror parity table
5. Skill modernization summary
6. Scripts added/updated and rationale
7. Residual risks and follow-ups
