# Drift-Resistant Mirror Policy

This repository maintains parallel platform packages:

- `.agent`
- `.claude`
- `.cursor`

## Policy

1. **Metadata may differ by platform**
   - File frontmatter can use platform-specific keys and extensions.

2. **Instructional body should remain aligned**
   - Core guidance should stay semantically equivalent across mirrors.

3. **Path references must stay platform-local**
   - `.agent` files may only reference `.agent/...`
   - `.claude` files may only reference `.claude/...`
   - `.cursor` files may only reference `.cursor/...`

4. **Sync must remap platform paths**
   - `scripts/ecosystem/sync_content.py` rewrites platform roots and SKILL file names.

5. **Isolation gate is mandatory**
   - `scripts/ecosystem/isolation_lint.py` must pass.

6. **Audit gate is mandatory**
   - `scripts/ecosystem/ecosystem_audit.py --fail-on high` must pass.
