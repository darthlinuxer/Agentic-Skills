# Testing Strategy

## Purpose
Define practical validation practices for the Agentic-Skills repository so changes remain consistent, safe, and cross-platform compatible.

## Testing Layers

### 1) Repository-level validation (primary)
Use the repo validation script as the default quality gate:
- `run-validations.sh`

Expected checks (from README context):
- link validation
- dangling skills check
- platform isolation check
- docs secrets check

Validation outputs are written to `.reports/`.

### 2) Structural consistency checks
When changing commands/workflows/agents/skills:
- verify naming parity for equivalent modes across `.cursor/`, `.claude/`, `.agent/`
- verify entry-point routing still targets platform orchestrator
- verify no forbidden routing cycles are introduced

### 3) Documentation checks
For README, command docs, and orchestrator guidance updates:
- verify links resolve
- verify command/workflow names and counts are accurate
- verify examples match current structure and paths

## Change-Type Test Matrix

### A. Command/workflow changes
- Run full repo validations
- Manually inspect counterpart files on other platforms for parity
- Confirm mode intent still maps correctly in orchestrator docs

### B. Agent definition changes
- Run full repo validations
- Confirm domain ownership boundaries are preserved
- Confirm referenced skills exist and are appropriate to agent domain

### C. Skill changes
- Run full repo validations
- Confirm no dangling references from agents/commands/workflows
- Confirm skill remains reusable and does not violate architecture contract

### D. Documentation-only changes
- Run full repo validations (at minimum link/docs checks)
- Spot-check examples and paths against workspace

## PR / Review Checklist
- [ ] Change is scoped and backward compatible where expected
- [ ] Cross-platform parity considered
- [ ] Validation script run and reports reviewed
- [ ] Memory bank updated for meaningful process/architecture changes

## Failure Handling
If validations fail:
1. Fix root cause first (not just symptoms).
2. Re-run validations after each targeted fix.
3. Document any non-obvious rationale in docs or memory-bank notes.

## Ownership Notes
- Orchestrator/process consistency: orchestration/planning domain
- Technical quality and regressions: QA/test domain
- Security-sensitive findings: security domain
