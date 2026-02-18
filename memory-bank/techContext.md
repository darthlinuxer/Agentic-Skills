# Tech Context

## Repository Type
Documentation-and-configuration-heavy orchestration repo for AI coding workflows.

## Top-Level Files
- `README.md`
- `LICENSE`
- `REQUIREMENTS.txt`
- `run-validations.sh`

## Major Directories
- `.cursor/` (commands, agents, rules, skills, scripts)
- `.claude/` (commands, agents, skills, scripts)
- `.agent/` (workflows, agents, skills, scripts)
- `.reports/` (validation outputs)

## Tooling/Execution
- Shell script validations run from repo root.
- Git-based workflow.
- Linux-compatible workspace environment.

## Constraints
- Maintain parity of behavior across platforms.
- Keep routing contracts explicit and cycle-free.
- Preserve clear role boundaries between orchestrator, agents, and skills.

## Usage Notes
- Primary user interface is command/workflow invocation.
- Mode semantics are documented in orchestrator docs per platform.
