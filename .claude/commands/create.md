Before answering:
- Apply the most relevant skills and rules for this platform.
- Prefer the single most specific skill/rule when possible.
- If no skill or rule clearly matches, ignore all and answer normally.

# /create - Create Application

$ARGUMENTS

## Task
Start a new application creation process.

### Steps
1. **Request analysis**
   - Understand what the user wants
   - Ask clarifying questions when needed
2. **Project planning**
   - Determine tech stack
   - Plan file structure
   - Create plan file and proceed to building
3. **Application building**
   - Orchestrate with relevant skills
   - Coordinate specialist knowledge across domains
4. **Preview**
   - Start preview after completion
   - Present URL to user

## Usage Examples
```
/create blog site
/create e-commerce app with product listing and cart
/create todo app
/create Instagram clone
/create crm system with customer management
```

## Before Starting
If request is unclear, ask:
- What type of application?
- What are the basic features?
- Who will use it?

## Routing
The `/create` command delegates to the [agent-orchestrator](../agents/agent-orchestrator.md) agent in **`mode="create"`**. The orchestrator:
- Uses [project-planner](../agents/project-planner.md), [product-manager](../agents/product-manager.md), and [explorer-agent](../agents/explorer-agent.md) to analyze requirements and plan the new application.
- Uses `intelligent-routing` to select implementation agents ([frontend-specialist](../agents/frontend-specialist.md), [backend-specialist](../agents/backend-specialist.md), [database-architect](../agents/database-architect.md), [devops-engineer](../agents/devops-engineer.md), [test-engineer](../agents/test-engineer.md), etc.) and coordinates them using process skills like `writing-plans`, `using-superpowers`, and `subagent-driven-development`.

Users should call `/create`; the orchestrator manages the full multi-agent lifecycle from planning through initial implementation.
