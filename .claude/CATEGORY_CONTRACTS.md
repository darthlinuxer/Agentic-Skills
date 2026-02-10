# Category Contracts (.claude)

This file defines minimum structure contracts for `.claude` categories.

## Agents Contract (`.claude/agents/*.md`)

Each agent file should include:

1. Purpose and scope
2. Activation signals
3. Non-goals or boundaries
4. Related skills under `.claude/skills/`
5. Deterministic execution guidance

## Skills Contract (`.claude/skills/*/SKILL.md`)

Each skill file should include:

1. Objective
2. When to use
3. When not to use
4. Selective reading map
5. Optional scripts usage criteria (only if useful)

## Commands Contract (`.claude/commands/*.md`)

Each command file should include:

1. Trigger intent
2. Preconditions
3. Ordered execution steps
4. Output format contract
5. Failure handling guidance

## Isolation Contract

All references must remain within `.claude/` paths.
