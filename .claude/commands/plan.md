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
