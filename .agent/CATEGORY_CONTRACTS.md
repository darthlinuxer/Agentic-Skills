# Category Contracts (.agent)

This file defines minimum structure contracts for `.agent` categories.

## Agents Contract (`.agent/agents/*.md`)

Each agent file should include:

1. Purpose and scope
2. Activation signals
3. Non-goals or boundaries
4. Related skills under `.agent/skills/`
5. Deterministic execution guidance

## Skills Contract (`.agent/skills/*/SKILL.md`)

Each skill file should include:

1. Objective
2. When to use
3. When not to use
4. Selective reading map
5. Optional scripts usage criteria (only if useful)

## Workflows Contract (`.agent/workflows/*.md`)

Each workflow file should include:

1. Trigger intent
2. Preconditions
3. Ordered execution steps
4. Output format contract
5. Failure handling guidance

## Rules Contract (`.agent/rules/*.md`)

Each rule file should include:

1. Enforceable invariants
2. Scope and precedence
3. Conflict handling guidance
4. No references outside `.agent/`
