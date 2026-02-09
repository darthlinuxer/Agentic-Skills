# Agentic-Skills

LLM-agnostic skills based on Anthropic’s Skills Framework. Each skill is a self-contained playbook (with optional scripts and references) that guides an LLM through a reliable workflow for a specific kind of task.

## What’s in this repo

- **Antigravity workspace**: `.agent/` contains agents, skills, rules, workflows, and scripts.
- **Cursor workspace**: `.cursor/` contains rules, commands, skills, and agents.
- **Claude workspace**: `.claude/` contains Claude-compatible skills and agents.
- **References & assets**: Some skills include `reference/`, `references/`, `assets/`, or `scripts/` for deeper guidance or automation.

## Skill index (Claude)

| Skill | Folder | What it does |
| --- | --- | --- |
| docx | `.claude/skills/docx/` | Create, edit, and analyze `.docx` files with tracked changes, comments, and OOXML workflows. |
| mcp-builder | `.claude/skills/mcp-builder/` | Build high-quality MCP servers with strong tool design, error handling, and evaluation guidance. |
| senior-agile-pm-budget-analyst | `.claude/skills/senior-agile-pm-budget-analyst/` | Create/review Agile artifacts with budget analysis, poker planning, Gantt, and critical path support. |
| senior-pmbok-pm | `.claude/skills/senior-pmbok-pm/` | Create/review PMBOK artifacts using provided templates and workflows. |
| senior-software-developer | `.claude/skills/senior-software-developer/` | Engineering standards and patterns for Python, C#, Node.js, and TypeScript work. |
| subagent-driven-development | `.claude/skills/subagent-driven-development/` | Execute plans via subagents with spec + code quality review cycles. |
| test-driven-development | `.claude/skills/test-driven-development/` | Enforce TDD (red-green-refactor) for features and bugfixes. |
| using-superpowers | `.claude/skills/using-superpowers/` | Guidance on when and how to invoke skills in workflows. |
| verification-before-completion | `.claude/skills/verification-before-completion/` | Require verification evidence before claiming work is complete. |
| writing-plans | `.claude/skills/writing-plans/` | Create detailed, executable implementation plans for complex tasks. |
| writing-prompts | `.claude/skills/writing-prompts/` | Craft high-quality prompts for LLM performance and consistency. |
| writing-skills | `.claude/skills/writing-skills/` | Author and validate skills using a TDD-style approach. |

## How to use these skills

### In Claude (Anthropic)

1. Pick the relevant skill folder under `.claude/skills/`.
2. Open the `SKILL.md` file and load its content into your session (paste it, or attach it if your client supports file attachments).
3. Follow the skill instructions while working on your task.

If your Claude client supports skills directories natively, point it at `.claude/skills/` or copy the specific skill folder into your configured skills path.

## Platform structure

```
.agent/   # Antigravity agents, skills, workflows, rules, scripts
.cursor/  # Cursor rules, commands, skills, agents
.claude/  # Claude skills, agents (project-level)
```

### In GitHub Copilot

Copilot does not currently provide a first-class “skills” installation mechanism like Anthropic’s framework. You can still use these skills effectively by:

1. Opening the relevant `SKILL.md` and pasting its instructions into Copilot Chat as a starting context.
2. Keeping the skill file open and asking Copilot to follow it while working.
3. (If available in your Copilot setup) adding repository-level or workspace-level **custom instructions** that reference the skill you want Copilot to follow.

> Note: Copilot features evolve; if your version supports workspace instructions or instruction files, you can point those instructions at the relevant skill folder.

## Contributing

Contributions are welcome! To add a new skill or improve an existing one:
1. Fork this repository.
2. Create a new branch for your feature or fix.
3. Add your skill folder with a `SKILL.md` and any necessary assets.
4. Submit a pull request with a description of your changes.
5. Ensure your code follows the existing style and conventions.
6. Include tests or examples if applicable.
7. Update this README to include your new skill in the index.
8. Respond to any feedback on your pull request.
9. Once approved, your changes will be merged into the main repository.
10. Celebrate your contribution to the Agentic-Skills community!

## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.