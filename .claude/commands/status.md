Before answering:
- Apply the most relevant skills and rules for this platform.
- Prefer the single most specific skill/rule when possible.
- If no skill or rule clearly matches, ignore all and answer normally.

# /status - Show Status

$ARGUMENTS

## Task
Show current project and agent status.

### What It Shows
1. **Project Info**
   - Project name and path
   - Tech stack
   - Current features
2. **Agent Status Board**
   - Which tasks are completed
   - Pending work
3. **File Statistics**
   - Files created count
   - Files modified count
4. **Preview Status**
   - Server running
   - URL
   - Health check

## Example Output
```
=== Project Status ===

📁 Project: my-ecommerce
📂 Path: /path/to/my-ecommerce
🏷️ Type: nextjs-ecommerce
📊 Status: active

🔧 Tech Stack:
   Framework: next.js
   Database: postgresql
   Auth: clerk
   Payment: stripe

✅ Features (5):
   • product-listing
   • cart
   • checkout
   • user-auth
   • order-history

⏳ Pending (2):
   • admin-panel
   • email-notifications

📄 Files: 73 created, 12 modified

=== Agent Status ===

✅ database-architect → Completed
✅ backend-specialist → Completed
🔄 frontend-specialist → Dashboard components (60%)
⏳ test-engineer → Waiting

=== Preview ===
🌐 URL: 
💚 Health: OK
```

## Routing
The `/status` command delegates to the [agent-orchestrator](../agents/agent-orchestrator.md) agent in **`mode="status"`**. The orchestrator:
- Uses [explorer-agent](../agents/explorer-agent.md) and project-planning information (for example from `PLAN-{slug}` documents) to summarize project, agent, and preview status.
- May consult domain agents for additional details when needed, but `/status` itself remains read-only and does not trigger implementations.

Users should call `/status` to inspect the current state; orchestration and data gathering from agents are handled internally.
