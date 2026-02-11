# Agentic-Skills

A **multi-platform agentic ecosystem** for AI-assisted development. It provides commands (or workflows), an orchestrator, specialist agents, and reusable skills so you can plan, implement, fix, test, deploy, and document projects in a consistent way across **Cursor**, **Claude Code**, and **Google Anthropic Agent**.

---

## Quick Start

1. **Pick your platform** — Cursor (`.cursor/commands/`), Claude Code (`.claude/commands/`), or Google Anthropic Agent (`.agent/workflows/`).
2. **Run a command** — e.g. `/plan`, `/implement`, `/fix`, or `/docs` from the command palette or chat.
3. **Be specific** — e.g. `/plan e-commerce site with cart and auth`. The orchestrator routes to the right agents and skills.

---

## What this repo is

- **Entry points**: 17 commands (Cursor/Claude) or workflows (Agent) that you invoke—e.g. `/plan`, `/implement`, `/fix`, `/docs`.
- **Orchestrator**: A single coordinator per platform that receives your request by *mode*, selects the right agents and skills, and runs the workflow. You don’t call agents or skills directly.
- **Agents**: Domain specialists (e.g. backend-specialist, frontend-specialist, documentation-writer, test-engineer) and process roles (e.g. project-planner, verifier). Each has its own skills and a **domain color** so the orchestrator (and logs) can see at a glance which area of responsibility is active.
- **Skills**: Reusable guidance and patterns (e.g. test-driven-development, writing-plans, frontend-design) used by the orchestrator and agents. Skills never call commands or the orchestrator.

> **Contract:** You use **only** the entry points (commands or workflows). They route to the orchestrator; the orchestrator uses agents and skills. No cycles: skills don’t call commands or the orchestrator; agents don’t call commands.

---

## Agent domains and colors

Agents are grouped by domain and share a **basic color** across all three platforms. This keeps roles non-overlapping and makes it easy for the orchestrator (and future colored logs) to see who owns what:

| Domain | Color | Cursor / Claude / Agent agents (examples) |
|--------|--------|-------------------------------------------|
| Orchestration & planning | blue / violet | `orchestrator`, `project-planner`, `product-manager` |
| Discovery & legacy | cyan | `explorer-agent`, `code-archaeologist` |
| Verification & QA | amber | `test-engineer`, `verifier` (Cursor) |
| Security | red | `security-auditor`, `penetration-tester` |
| Backend & data | green | `backend-specialist`, `database-architect` |
| Frontend | indigo | `frontend-specialist` |
| DevOps & infra | slate | `devops-engineer` |
| Mobile | pink | `mobile-developer` |
| Documentation | zinc | `documentation-writer` |
| Performance | lime | `performance-optimizer` |
| SEO / marketing | yellow | `seo-specialist` |
| Games | emerald | `game-developer` |

On each platform, agents declare this in frontmatter (for example `color: green` on `backend-specialist`), and the orchestrator never asks an agent to work outside its domain.

## Features

- **Plan & create** — Task breakdown, agent/skill assignments; new apps or modules from plan to implementation.
- **Implement, fix & debug** — Features and bugfixes with tests; systematic root-cause analysis.
- **Test & review** — Generate and run tests; multi-agent code review.
- **Deploy & operate** — Staging/production deployment; preview server and status.
- **Document** — Create or update docs in sync with the codebase.
- **Explore & design** — Brainstorm, enhance features, explain concepts, UI/UX design intelligence.

## Platforms and entry points

| Platform | Entry path | How you start |
|----------|------------|----------------|
| **Cursor** | `.cursor/commands/` | Run a **command** (e.g. `/plan`, `/implement`) from the Cursor command palette or chat. |
| **Claude** | `.claude/commands/` | Run a **command** in Claude Code; it routes to the agent-orchestrator. |
| **Agent** (Google Anthropic) | `.agent/workflows/` | Invoke a **workflow**; workflows are the entry point (no commands directory). |

Same 17 entry names on all platforms:

| Command / workflow | Typical use |
|--------------------|-------------|
| `/plan` | Create or refine a plan (task breakdown, agent/skill assignments). No code. |
| `/create` | New app or major module; full lifecycle from plan to initial implementation. |
| `/implement` | Implement features from an existing plan. |
| `/fix` | Fix bugs and regressions with tests. |
| `/debug` | Systematic debugging and root-cause analysis. |
| `/refactor` | Refactor without changing behavior. |
| `/test` | Generate and run tests, improve coverage. |
| `/review` | Multi-agent code review. |
| `/docs` | Create or update documentation (sync with code). |
| `/deploy` | Coordinate deployment (staging/production). |
| `/status` | Report project/agent/preview status (read-only). |
| `/preview` | Manage preview server (start, stop, status, health). |
| `/brainstorm` | Explore options before committing to implementation. |
| `/enhance` | Add or update features in an existing app. |
| `/explain` | Explain code or concepts (educator mode). |
| `/ui-ux-pro-max` | Design intelligence (UI/UX, design system). |
| `/orchestrate` | Multi-domain orchestration; orchestrator chooses agents/skills. |

You can chain modes (e.g. `/brainstorm` then `/plan` then `/implement`) for one task.

---

## How to use the ecosystem

1. **Start with a command (or workflow).**  
   In Cursor or Claude, use the command (e.g. `/plan`, `/implement`, `/docs`). On Agent, invoke the matching workflow. Do not call the orchestrator or agents directly.

2. **Be specific.**  
   Example: `/plan e-commerce site with cart and auth` or `/docs add README for the API module`. The orchestrator will route to the right agents and skills.

3. **If your prompt has no command.**  
   The workspace rule is: figure out which command(s) apply and mention them (e.g. “Use `/plan` then `/implement`”). Commands live in the platform’s commands (or workflows) directory.

4. **Plans.**  
   Plans are written to `docs/PLAN-{task-slug}.md`. After `/plan`, use `/create` or `/implement` to execute; the orchestrator uses the plan to assign work.

5. **Documentation.**  
   Use `/docs` for anything doc-related; the orchestrator uses the documentation-writer agent and doc-related skills so docs stay aligned with the codebase.

---

## Directory layout (per platform)

Layout is parallel across the three platforms; only the top-level folder and “commands vs workflows” differ.

| Directory | Purpose |
|-----------|---------|
| **`.cursor/`** | Cursor IDE: commands, agents, rules, skills, scripts. |
| **`.claude/`** | Claude Code: commands, agents, skills, scripts. |
| **`.agent/`** | Google Anthropic Agent: workflows (no commands dir), agents, skills, scripts. |
| **`docs/`** | Project docs and plans (e.g. `docs/PLAN-*.md`). |

Under each platform:

- **`commands/`** (or **`workflows/`** for `.agent/`) — Entry points; each file has a **Routing** section to the orchestrator and a mode.
- **`agents/`** — Orchestrator plus specialist agents (e.g. `orchestrator.md`, `documentation-writer.md`, `backend-specialist.md`). Cursor also has `verifier.md`.
- **`skills/`** — Reusable skills (e.g. `documentation-templates`, `writing-plans`, `test-driven-development`). Agents reference skills; skills do not call commands or the orchestrator.
- **`rules/`** (Cursor/Agent) — Workspace rules (e.g. entry-point, coding-style, git).
- **`scripts/`** — Helper scripts (e.g. preview, verification).

---

## Validations

From the repo root, run `./run-validations.sh` to execute link validation, **dangling skills check**, platform isolation, and docs secrets check. Reports are written to `.reports/`.

---

## More detail

 **Orchestrator and modes:** See the Command Modes (or Workflow Modes) table in the platform’s orchestrator:  
  `.cursor/agents/orchestrator.md`, `.claude/agents/agent-orchestrator.md`, `.agent/agents/orchestrator.md`.
- **Skills:** Browsable under `.cursor/skills/` (and `.claude/skills/`, `.agent/skills/`). Each skill has a `SKILL.md` describing when and how it’s used.

---

## Contributing

Open an issue or pull request on the repository.

---

## License

See [LICENSE](LICENSE).
