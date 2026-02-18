# Product Context

## Why this project exists
Developers using different AI coding environments need a reliable, repeatable way to move from idea to production changes without reinventing process each time.

Agentic-Skills provides a shared operating model: invoke a high-level mode, let the orchestrator route work to specialized agents/skills, and keep outputs consistent.

## Problems solved
- Fragmented workflows across tooling ecosystems.
- Inconsistent quality when planning/implementing/testing/documenting.
- Ambiguity about who/what should handle a task.
- Drift between code, docs, and process standards.

## How it should work
1. User invokes a command/workflow (entry point).
2. Platform orchestrator interprets mode + prompt.
3. Appropriate specialist agents and skills are selected.
4. Outputs are produced and validated with repository checks.

## UX goals
- Predictable, low-friction command surface.
- Strong separation of concerns (entry point → orchestrator → agents/skills).
- Fast onboarding: clear docs and discoverable structure.
- High trust via validation and explicit domain ownership.
