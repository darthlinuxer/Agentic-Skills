# Ecosystem Automation Scripts

Automation for auditing and synchronizing the mirrored agent ecosystem in:

- `.agent` (Antigravity)
- `.claude` (Claude)
- `.cursor` (Cursor)

## Goal

Keep all platforms aligned with these rules:

1. Unique routing (no ambiguity between skills/agents/commands/rules)
2. Correct links and self-contained platform paths
3. Clear and concise instructions
4. Structure compliance per platform/category
5. Modern skill guidance with scripts only when useful
6. Mirror parity across platforms (metadata may differ)
7. Purpose-first refactoring (rule vs workflow vs skill vs agent)

---

## Scripts

### `ecosystem_audit.py`

Comprehensive cross-platform audit engine.

Checks:

- Missing mirrored files/assets
- Content parity drift across mirrors
- Cross-platform path leaks (e.g. `.agent/` inside `.cursor` files)
- Broken internal links
- Required metadata by platform
- Basic structure and clarity heuristics
- Skill script usage signals
- Uniqueness/overlap heuristics

Output:

- `docs/refactoring/reports/AUDIT_REPORT.json` (machine-friendly)
- `docs/refactoring/reports/ECOSYSTEM_REVIEW_REPORT.md` (human-readable)

Usage:

```bash
python3 scripts/ecosystem/ecosystem_audit.py /workspace
```

---

### `sync_content.py`

Synchronizes mirrored content from `.agent` to `.claude` and `.cursor` while preserving target frontmatter.

Isolation guarantee:

- Rewrites platform paths during sync so each target stays self-contained.
- Prevents leaking `.agent/`, `.claude/`, or `.cursor/` references into other platform domains.

Usage:

```bash
python3 scripts/ecosystem/sync_content.py
```

---

### `fix_cross_platform_refs.py`

Fixes known cross-platform path leaks in selected files.

Usage:

```bash
python3 scripts/ecosystem/fix_cross_platform_refs.py
```

---

### `remove_agent_frontmatter.py`

Removes frontmatter from agent files where plain markdown is expected.

---

### `simplify_skills_metadata.py`

Normalizes skill metadata fields to expected platform format.

---

### `add_mcp_references.py`

Adds MCP-related references to selected complex skills.

---

## Recommended Workflow

1. Sync mirrors:

```bash
python3 scripts/ecosystem/sync_content.py
```

2. Run audit:

```bash
python3 scripts/ecosystem/ecosystem_audit.py /workspace
```

3. Fix high/medium findings first, then re-run audit.

4. Treat low findings as optional quality improvements.

---

## Reference Prompt

Use the consolidated review prompt in:

- `docs/refactoring/ECOSYSTEM_REFACTOR_PROMPT.md`
