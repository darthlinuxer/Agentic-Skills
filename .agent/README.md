# Antigravity Platform Package

This directory is a standalone Antigravity distribution.

## Isolation Rule

- Keep all references inside `.agent/`.
- Do not reference other platform roots from this package.

## Structure

- `agents/` - specialist agents
- `skills/` - modular skills
- `workflows/` - slash workflows
- `rules/` - global rules
- `scripts/` - platform automation scripts

## Contracts

Category-level contracts are defined in:

- `CATEGORY_CONTRACTS.md`

## Validation

From repository root:

```bash
python3 scripts/ecosystem/isolation_lint.py /workspace --platform .agent
python3 scripts/ecosystem/ecosystem_audit.py /workspace --fail-on high
```
