Before answering:
- Apply the most relevant skills and rules for this platform.
- Prefer the single most specific skill/rule when possible.
- If no skill or rule clearly matches, ignore all and answer normally.

# /debug - Systematic Problem Investigation

$ARGUMENTS

## Purpose
Systematically investigate issues, errors, or unexpected behavior.

## Behavior
1. **Gather information**
   - Error message
   - Reproduction steps
   - Expected vs actual behavior
   - Recent changes
2. **Form hypotheses**
   - List possible causes
   - Order by likelihood
3. **Investigate systematically**
   - Test each hypothesis
   - Check logs and data flow
4. **Fix and prevent**
   - Apply fix
   - Explain root cause
   - Add prevention measures

## Output Format
```markdown
## 🔍 Debug: [Issue]

### 1. Symptom
[What's happening]

### 2. Information Gathered
- Error: `[error message]`
- File: `[filepath]`
- Line: [line number]

### 3. Hypotheses
1. ❓ [Most likely cause]
2. ❓ [Second possibility]
3. ❓ [Less likely cause]

### 4. Investigation

**Testing hypothesis 1:**
[What I checked] → [Result]

**Testing hypothesis 2:**
[What I checked] → [Result]

### 5. Root Cause
🎯 **[Explanation of why this happened]**

### 6. Fix
```[language]
// Before
[broken code]

// After
[fixed code]
```

### 7. Prevention
🛡️ [How to prevent this in the future]
```

## Examples
```
/debug login not working
/debug API returns 500
/debug form doesn't submit
/debug data not saving
```

## Key Principles
- **Ask before assuming** - get full error context
- **Test hypotheses** - don't guess randomly
- **Explain why** - not just what to fix
- **Prevent recurrence** - add tests and validation

## Routing
The `/debug` command delegates to the [orchestrator](../agents/orchestrator.md) agent in **`mode="debug"`**. The orchestrator:
- Uses [intelligent-routing](../skills/intelligent-routing/SKILL.md) to select [debugger](../agents/debugger.md) as the primary agent, and may bring in other domain agents (such as [backend-specialist](../agents/backend-specialist.md), [frontend-specialist](../agents/frontend-specialist.md), [database-architect](../agents/database-architect.md)) based on where the issue appears.
- Ensures [test-engineer](../agents/test-engineer.md) participates to add or adjust tests that prevent recurrence.

Users should call `/debug`; the orchestrator manages which agents and skills participate in the investigation and fix plan.
