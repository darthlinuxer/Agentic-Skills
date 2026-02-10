---
description: Workflow for /brainstorm - Structured Idea Exploration.
---

Before answering:
- Apply the most relevant skills and rules for this platform.
- Prefer the single most specific skill/rule when possible.
- If no skill or rule clearly matches, ignore all and answer normally.

# /brainstorm - Structured Idea Exploration

$ARGUMENTS

## Purpose
Explore multiple options before committing to implementation.

## Behavior
1. **Understand the goal**
   - What problem are we solving?
   - Who is the user?
   - What constraints exist?
2. **Generate options**
   - Provide at least 3 approaches
   - Include pros and cons
3. **Compare and recommend**
   - Summarize tradeoffs
   - Recommend with reasoning

## Output Format
```markdown
## 🧠 Brainstorm: [Topic]

### Context
[Brief problem statement]

---

### Option A: [Name]
[Description]

✅ **Pros:**
- [benefit 1]
- [benefit 2]

❌ **Cons:**
- [drawback 1]

📊 **Effort:** Low | Medium | High

---

### Option B: [Name]
[Description]

✅ **Pros:**
- [benefit 1]

❌ **Cons:**
- [drawback 1]
- [drawback 2]

📊 **Effort:** Low | Medium | High

---

### Option C: [Name]
[Description]

✅ **Pros:**
- [benefit 1]

❌ **Cons:**
- [drawback 1]

📊 **Effort:** Low | Medium | High

---

## 💡 Recommendation

**Option [X]** because [reasoning].
What direction would you like to explore?
```

## Examples
```
/brainstorm authentication system
/brainstorm state management for complex form
/brainstorm database schema for social app
/brainstorm caching strategy
```

## Key Principles
- **No code** - this is about ideas, not implementation
- **Visual when helpful** - use diagrams for architecture
- **Honest tradeoffs** - don't hide complexity
- **Defer to user** - present options, let them decide

## Routing
This workflow delegates to the [orchestrator](../agents/orchestrator.md) agent in **`mode="brainstorm"`**. The orchestrator:
- Uses the `brainstorming` and `research` skills (and may consult [project-planner](../agents/project-planner.md) or domain agents) to explore options without committing to implementation.
- Keeps the outcome as options and recommendations that can later be fed into plan, implement, or orchestrate workflows as needed.

Users should invoke this workflow for idea exploration; orchestration and skill usage remain internal.
