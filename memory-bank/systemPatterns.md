# System Patterns

## Architecture Pattern
Layered orchestration pattern:
1. Entry points (commands/workflows)
2. Orchestrator (mode-aware router)
3. Specialist agents (domain ownership)
4. Skills (reusable execution guidance)

## Key Design Rules
- Users call only entry points.
- Orchestrator coordinates all downstream work.
- Agents do not expose entry-point APIs to users.
- Skills are reusable guidance; they do not call commands/orchestrator.
- Avoid cyclic dependencies among layers.

## Domain Ownership Pattern
Agents are grouped by technical domain (backend, frontend, security, docs, QA, etc.) with shared domain colors for role clarity and routing transparency.

## Cross-Platform Consistency Pattern
Parallel platform structure with minimal conceptual divergence:
- Cursor and Claude use `commands/`.
- Agent platform uses `workflows/`.
- All map to equivalent intent/modes.

## Validation Pattern
Repository-level validation (`run-validations.sh`) acts as quality gate:
- link checks
- dangling skill checks
- platform isolation checks
- docs secrets checks

Reports are written to `.reports/`.
