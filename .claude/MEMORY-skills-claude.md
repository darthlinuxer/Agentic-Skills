# MEMORY - Claude skills classification

High-level mapping of Claude SKILLs to shared domains/subdomains. See `.cursor/MEMORY-skills-cursor.md` for the canonical taxonomy.

| skill_path | domain/subdomain | summary | used_by_agents (indicative) |
|-----------|------------------|---------|------------------------------|
| `.claude/skills/writing-plans/SKILL.md` | process/planning | Implementation planning workflow (PLAN files, task breakdown). | agent-orchestrator, project-planner |
| `.claude/skills/test-driven-development/SKILL.md` | process/tdd | TDD workflow (RED-GREEN-REFACTOR) and usage rules. | backend-specialist, frontend-specialist, test-engineer |
| `.claude/skills/testing-patterns/SKILL.md` | testing/patterns | Testing pyramid, AAA, mocking, and organization patterns. | test-engineer |
| `.claude/skills/documentation-templates/SKILL.md` | docs/templates | Documentation templates for README/API/docs. | documentation-writer |
| `.claude/skills/writing-skills/SKILL.md` | docs/writing | TDD-style skill authoring and writing best practices. | documentation-writer |
| `.claude/skills/web-design-guidelines/SKILL.md` | frontend/web-guidelines | Web interface and accessibility guidelines. | frontend-specialist |
| `.claude/skills/frontend-design/SKILL.md` | frontend/design | Visual design, layout, typography, and design thinking. | frontend-specialist |
| `.claude/skills/frontend-development/SKILL.md` | frontend/development | Frontend architecture and development practices. | frontend-specialist |
| `.claude/skills/ui-styling/SKILL.md` | frontend/styling | Styling with Tailwind/shadcn and tokens. | frontend-specialist |
| `.claude/skills/nextjs-react-expert/SKILL.md` | frontend/performance | Next.js/React performance optimization rules. | frontend-specialist |
| `.claude/skills/ui-ux-pro-max/SKILL.md` | frontend/design-system | Design system generation and UI/UX intelligence. | frontend-specialist |
| `.claude/skills/tailwind-patterns/SKILL.md` | frontend/design-system | Tailwind CSS v4 patterns and token architecture. | frontend-specialist |
| `.claude/skills/backend-development/SKILL.md` | backend/development | Backend development patterns and decisions. | backend-specialist |
| `.claude/skills/api-patterns/SKILL.md` | backend/api | API style, responses, versioning, and security. | backend-specialist |
| `.claude/skills/database-design/SKILL.md` | backend/data | Database schema, indexing, and migrations. | database-architect |
| `.claude/skills/nodejs-best-practices/SKILL.md` | backend/node | Node.js best practices. | backend-specialist |
| `.claude/skills/python-patterns/SKILL.md` | backend/python | Python development patterns. | backend-specialist |
| `.claude/skills/performance-profiling/SKILL.md` | performance/profiling | Profiling and bottleneck analysis. | performance-optimizer |
| `.claude/skills/seo-fundamentals/SKILL.md` | performance/seo | SEO/GEO fundamentals and Core Web Vitals. | seo-specialist |
| `.claude/skills/geo-fundamentals/SKILL.md` | performance/seo | GEO-specific guidance for AI search engines. | seo-specialist |
| `.claude/skills/webapp-testing/SKILL.md` | testing/e2e | Web E2E testing strategies and Playwright patterns. | test-engineer |
| `.claude/skills/systematic-debugging/SKILL.md` | debugging/process | 4-phase debugging methodology. | debugger |
| `.claude/skills/vulnerability-scanner/SKILL.md` | security/audit | Security scan orchestration and scripts. | security-auditor, penetration-tester |
| `.claude/skills/red-team-tactics/SKILL.md` | security/red-team | Red-team offensive security principles. | penetration-tester |
| `.claude/skills/server-management/SKILL.md` | devops/server | Server management patterns. | devops-engineer |
| `.claude/skills/deployment-procedures/SKILL.md` | devops/deploy | Deployment workflow principles. | devops-engineer |
| `.claude/skills/lint-and-validate/SKILL.md` | testing/linting | Lint/type-check orchestration and static analysis. | devops-engineer, test-engineer |
| `.claude/skills/web-games/SKILL.md` | games/web | Web game development. | game-developer |
| `.claude/skills/game-development/SKILL.md` | games/general | Game dev orchestration. | game-developer |
| `.claude/skills/2d-games/SKILL.md` | games/2d | 2D game development. | game-developer |
| `.claude/skills/3d-games/SKILL.md` | games/3d | 3D game development. | game-developer |
| `.claude/skills/mobile-games/SKILL.md` | games/mobile | Mobile game development. | game-developer, mobile-developer |
| `.claude/skills/game-design/SKILL.md` | games/design | Game design and balancing. | game-developer |
| `.claude/skills/game-art/SKILL.md` | games/art | Game art principles. | game-developer |
| `.claude/skills/game-audio/SKILL.md` | games/audio | Game audio design. | game-developer |
| `.claude/skills/mobile-design/SKILL.md` | mobile/design | Mobile UX and platform conventions. | mobile-developer |
| `.claude/skills/multiplayer/SKILL.md` | games/multiplayer | Multiplayer architecture and synchronization. | game-developer |
| `.claude/skills/vr-ar/SKILL.md` | specialized/vr-ar | VR/AR dev principles. | game-developer |
| `.claude/skills/docx/SKILL.md` | docs/docx | Handling .docx documents. | documentation-writer |
| `.claude/skills/mcp-builder/SKILL.md` | specialized/mcp | Building MCP servers/tools. | backend-specialist |
| `.claude/skills/app-builder/SKILL.md` | process/app-builder | Full-stack app-building orchestration patterns. | agent-orchestrator |
| `.claude/skills/research/SKILL.md` | process/research | Deep research workflows. | explorer-agent |
| `.claude/skills/architecture/SKILL.md` | backend/architecture | Architecture decision framework. | backend-specialist, database-architect |
| `.claude/skills/problem-solving/SKILL.md` | process/metacognition | Problem-solving techniques and simplification. | project-planner, orchestrator |
| `.claude/skills/sequential-thinking/SKILL.md` | process/metacognition | Sequential thinking for complex tasks. | orchestrator, project-planner |
| `.claude/skills/parallel-agents/SKILL.md` | process/multi-agent | Multi-agent orchestration patterns. | agent-orchestrator |
| `.claude/skills/subagent-driven-development/SKILL.md` | process/multi-agent | Subagent-based implementation flows. | agent-orchestrator |
| `.claude/skills/verification-before-completion/SKILL.md` | testing/verification | Verification before marking work complete. | verifier, agent-orchestrator |
| `.claude/skills/using-superpowers/SKILL.md` | process/meta | Global workspace behavior rules. | all agents |
| `.claude/skills/behavioral-modes/SKILL.md` | process/meta | Operational modes (brainstorm, implement, review, etc.). | agent-orchestrator |
| `.claude/skills/clean-code/SKILL.md` | process/implementation | Clean code standards. | all domain agents |
| `.claude/skills/code-review-checklist/SKILL.md` | process/review | Code review checklist. | all domain agents |
| `.claude/skills/bash-linux/SKILL.md` | devops/tooling | Bash/Linux patterns. | devops-engineer |
| `.claude/skills/powershell-windows/SKILL.md` | devops/tooling | PowerShell patterns. | devops-engineer |
| `.claude/skills/update-cursor-settings/SKILL.md` | devops/tooling | Editing editor settings. | devops-engineer |
| `.claude/skills/gemini/SKILL.md` | process/global | Global Gemini behavior rules. | agent-orchestrator, agents |
| `.claude/skills/intelligent-routing/SKILL.md` | process/routing | Intelligent routing guidance. | agent-orchestrator |
| `.claude/skills/create-rule/SKILL.md` | docs/rules | Creating workspace rules. | documentation-writer |
| `.claude/skills/create-subagent/SKILL.md` | process/multi-agent | Creating custom subagents. | agent-orchestrator |
| `.claude/skills/senior-software-developer/SKILL.md` | process/implementation | Senior-level coding patterns. | backend-specialist, frontend-specialist |
| `.claude/skills/senior-agile-pm-budget-analyst/SKILL.md` | specialized/agile | Agile PM + budget analysis. | product-manager |
| `.claude/skills/senior-pmbok-pm/SKILL.md` | specialized/pmbok | PMBOK-based PM artifacts. | product-manager |
| `.claude/skills/aesthetic/SKILL.md` | frontend/design | Aesthetic design guidance. | frontend-specialist |

---

## Planned skill merges/renames

**None.** Aligned with Cursor decisions: no merges, renames, or deletions. Claude skills are 1:1 with Cursor at the conceptual level.

---

## Verification checklist (Claude)

- [x] All Claude skills are domain-tagged in this MEMORY.
- [x] All refactored skills have agent references updated (N/A—no refactors).
- [x] No stale skill names remain in `.claude/agents/` or `.claude/commands/`.
