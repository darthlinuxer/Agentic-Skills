# Claude Platform Package

This directory is a standalone Claude distribution.

## Isolation Rule

- Keep all references inside `.claude/`.
- Do not reference other platform roots from this package.

## Structure

- `agents/` - specialist agents
- `skills/` - modular skills
- `commands/` - command workflows

## Contracts

Category-level contracts are defined in:

- `CATEGORY_CONTRACTS.md`

## Validation

From repository root:

```bash
python3 scripts/ecosystem/isolation_lint.py /workspace --platform .claude
python3 scripts/ecosystem/ecosystem_audit.py /workspace --fail-on high
```
