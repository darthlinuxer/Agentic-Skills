---
description: Workflow for /plan - Project Planning Mode.
---

Before answering:
- Apply the most relevant skills and rules for this platform.
- Prefer the single most specific skill/rule when possible.
- If no skill or rule clearly matches, ignore all and answer normally.

# /plan - Project Planning Mode

$ARGUMENTS

## Critical Rules
1. **No code writing** - create a plan only
2. **Ask clarifying questions** before planning
3. **Plan file naming** - derive a short slug from the request

## Task
Create a plan file at `docs/PLAN-{task-slug}.md` that includes:
- Task breakdown
- Agent/skill assignments
- Verification checklist

## After Planning
Tell the user:
```
[OK] Plan created: docs/PLAN-{slug}.md

Next steps:
- Review the plan
- Run /create to start implementation
- Or modify the plan manually
```

## Usage
```
/plan e-commerce site with cart
/plan mobile app for fitness tracking
/plan SaaS dashboard with analytics
```

## Routing
This workflow delegates to the [orchestrator](../agents/orchestrator.md) agent in **`mode="plan"`**. The orchestrator:
- Uses [project-planner](../agents/project-planner.md) (and, when needed, [product-manager](../agents/product-manager.md)) as primary agents to create or update `PLAN-{slug}` documents.
- May use `intelligent-routing` to identify which domain agents will later own each part of the plan, but does not execute implementation in this mode.

Users should invoke this workflow to create or refine plans; orchestration and skill usage happen internally.
