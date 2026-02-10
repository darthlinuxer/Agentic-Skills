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
