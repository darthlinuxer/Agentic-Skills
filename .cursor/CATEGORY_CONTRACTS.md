# Category Contracts (.cursor)

This file defines minimum structure contracts for `.cursor` categories.

## Agents Contract (`.cursor/agents/*.md`)

Each agent file should include:

1. Purpose and scope
2. Activation signals
3. Non-goals or boundaries
4. Related skills under `.cursor/skills/`
5. Deterministic execution guidance

## Skills Contract (`.cursor/skills/*/SKILL.mdc`)

Each skill file should include:

1. Objective
2. When to use
3. When not to use
4. Selective reading map
5. Optional scripts usage criteria (only if useful)

## Commands Contract (`.cursor/commands/*.md`)

Each command file should include:

1. Trigger intent
2. Preconditions
3. Ordered execution steps
4. Output format contract
5. Failure handling guidance

## Rules Contract (`.cursor/rules/*.mdc`)

Each rule file should include:

1. Enforceable invariants
2. Scope and precedence
3. Conflict handling guidance
4. Explicit frontmatter (`alwaysApply` recommended)
5. No references outside `.cursor/`
