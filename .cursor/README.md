# Cursor Platform Package

This directory is a standalone Cursor distribution.

## Isolation Rule

- Keep all references inside `.cursor/`.
- Do not reference other platform roots from this package.

## Structure

- `agents/` - specialist agents
- `skills/` - modular skills
- `commands/` - command workflows
- `rules/` - global rules

## Contracts

Category-level contracts are defined in:

- `CATEGORY_CONTRACTS.md`

## Validation

From repository root:

```bash
python3 scripts/ecosystem/isolation_lint.py /workspace --platform .cursor
python3 scripts/ecosystem/ecosystem_audit.py /workspace --fail-on high
```
