# Dangling Skills Check

The **dangling skills** check ensures every skill under a platform’s `skills/` directory is referenced by at least one agent, command, or rule (or workflow). Skills that are never referenced are “dangling” and may be obsolete or simply not yet wired into the ecosystem.

## What it does

- **Per platform** (`.cursor`, `.agent`, `.claude`):
  - Discovers all `SKILL.md` files under the platform’s `skills/` directory.
  - Scans agents, commands, rules (and workflows for `.agent`) for references of the form `skills/<id>/SKILL.md` (with any path prefix, e.g. `../skills/...` or `.cursor/skills/...`).
  - Classifies each skill as **referenced** (at least one reference) or **dangling** (no references).
  - Detects **invalid references**: paths that look like `skills/<id>/SKILL.md` but `<id>` does not match any existing skill directory.

- **Outputs**:
  - JSON reports under `.reports/dangling-skills-{platform}.json` with `dangling`, `referenced`, and `invalidReferences`.
  - Console summary: total skills, dangling count, invalid reference count.

## How to run

From the repo root:

```bash
# Check all platforms (default)
python .github/scripts/skills-dangling-check.py --platform all

# Single platform
python .github/scripts/skills-dangling-check.py --platform cursor

# Verbose (list each dangling skill and invalid ref)
python .github/scripts/skills-dangling-check.py --platform all --verbose

# Don’t exit with failure (e.g. for local audit)
python .github/scripts/skills-dangling-check.py --platform all --no-fail
```

The script is also run as part of `./run-validations.sh` and by the **Dangling Skills Check** GitHub Actions workflow on push/PR.

## Interpreting results

- **Dangling skills**: Skills that no agent/command/rule references. You can:
  - **Wire them up**: Add a reference in the appropriate agent or command (e.g. a markdown link `[label](../skills/<id>/SKILL.md)` or a mention of the skill path).
  - **Remove or archive**: If the skill is obsolete, remove it or move it out of `skills/` in a separate change.

- **Invalid references**: A file references `skills/<id>/SKILL.md` but there is no skill with that `<id>`. Fix by:
  - Correcting the path (typo), or
  - Adding the missing skill under `skills/<id>/SKILL.md` if the reference is intentional.

## Reference pattern

A skill is considered referenced when its path appears in a referrer file. The pattern is:

- `skills/<skill-id>/SKILL.md`

with any preceding path (e.g. `../`, `.cursor/`, etc.). Referrer files are:

- **Cursor**: `.cursor/agents/`, `.cursor/commands/`, `.cursor/rules/`
- **Agent**: `.agent/agents/`, `.agent/workflows/`
- **Claude**: `.claude/agents/`, `.claude/commands/`

Only `.md` and `.mdc` files are scanned.

## CI behavior

The check **fails the job** (exit code 1) when any platform has at least one dangling skill or invalid reference. To allow commits that still have dangling skills (e.g. during a gradual cleanup), run the script locally with `--no-fail` or temporarily adjust the workflow.
