# Deployment Notes

## Scope
This repository mainly ships orchestration assets (commands/workflows, agents, skills, docs, scripts) rather than a runtime service. "Deployment" is therefore release/distribution readiness and workflow reliability.

## Deployment Objectives
- Ensure cross-platform command/workflow integrity.
- Ensure orchestrator routing contracts remain valid.
- Ensure documentation and examples reflect current repo state.
- Prevent leaking secrets in docs/config artifacts.

## Pre-Deployment Checklist
1. Run repository validations (`run-validations.sh`).
2. Review `.reports/` outputs and resolve issues.
3. Confirm key docs are up to date (`README.md`, platform orchestrator docs).
4. Confirm command/workflow parity for the 17 standard entry modes.
5. Confirm no architecture rule violations (cycles, direct low-level user entry).

## Release Notes Guidance
For each release, summarize:
- Added/updated commands, workflows, agents, or skills.
- Behavioral changes in orchestration logic or routing.
- Breaking changes and migration guidance, if any.
- Validation status and notable risk mitigations.

## Rollback Approach
Because this is Git-managed configuration/docs logic, rollback should prefer:
1. Revert offending commits.
2. Re-run validations to confirm clean state.
3. Publish corrective release notes.

## Environment Considerations
- Linux-friendly shell validation path is first-class.
- If platform-specific scripts are added later, include compatibility notes and fallback instructions.

## Operational Monitoring (Lightweight)
Use periodic checks during active development:
- validation report trends in `.reports/`
- issue/PR feedback about routing mismatches
- doc drift reports and broken links

## Future Enhancements
- Add CI pipeline gate mirroring `run-validations.sh`.
- Add release automation and changelog generation.
- Add explicit support matrix and versioning policy.
