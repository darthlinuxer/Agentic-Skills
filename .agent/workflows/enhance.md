---
description: Workflow for /enhance - Update Application.
---

Before answering:
- Apply the most relevant skills and rules for this platform.
- Prefer the single most specific skill/rule when possible.
- If no skill or rule clearly matches, ignore all and answer normally.

# /enhance - Update Application

$ARGUMENTS

## Task
Add features or make updates to an existing application.

### Steps
1. **Understand current state**
   - Review existing features and tech stack
2. **Plan changes**
   - Determine what will be added/changed
   - Detect affected files
   - Check dependencies
3. **Present plan to user** (for major changes)
4. **Apply**
   - Use relevant skills
   - Make changes
   - Test
5. **Update preview**
   - Hot reload or restart if needed

## Usage Examples
```
/enhance add dark mode
/enhance build admin panel
/enhance integrate payment system
/enhance add search feature
/enhance edit profile page
/enhance make responsive
```

## Caution
- Get approval for major changes
- Warn on conflicting requests (e.g., "use Firebase" when project uses PostgreSQL)
- Commit each change with git

## Routing
This workflow delegates to the [orchestrator](../agents/orchestrator.md) agent in **`mode="enhance"`**. The orchestrator:
- Uses `intelligent-routing` to select domain agents and process skills for planning and applying updates.
- May use [project-planner](../agents/project-planner.md) for larger enhancements that need task breakdown.

Users should invoke this workflow; the orchestrator decides which agents and skills participate in the update workflow.
