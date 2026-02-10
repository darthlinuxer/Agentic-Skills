Before answering:
- Apply the most relevant skills and rules for this platform.
- Prefer the single most specific skill/rule when possible.
- If no skill or rule clearly matches, ignore all and answer normally.

# /preview - Preview Management

$ARGUMENTS

## Task
Manage preview server: start, stop, restart, status, health check.

### Commands
```
/preview           - Show current status
/preview start     - Start server
/preview stop      - Stop server
/preview restart   - Restart
/preview check     - Health check
```

## Usage Examples
### Start Server
```
/preview start

Response:
🚀 Starting preview...
   Port: 3000
   Type: Next.js

✅ Preview ready!
   URL: 
```

### Status Check
```
/preview

Response:
=== Preview Status ===

🌐 URL: 
📁 Project: /path/to/project
🏷️ Type: nextjs
💚 Health: OK
```

### Port Conflict
```
/preview start

Response:
⚠️ Port 3000 is in use.

Options:
1. Start on port 3001
2. Close app on 3000
3. Specify different port
```

## Routing
The `/preview` command delegates to the [agent-orchestrator](../agents/agent-orchestrator.md) agent in **`mode="preview"`**. The orchestrator:
- Uses [devops-engineer](../agents/devops-engineer.md) or preview scripts for the preview lifecycle (start, stop, restart, health).
- May use [explorer-agent](../agents/explorer-agent.md) for project and preview context. Aligns with status-like read-only behavior where applicable.

Users should call `/preview`; the orchestrator coordinates preview management internally.
