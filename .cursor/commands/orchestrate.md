Before answering:
- Apply the most relevant skills and rules for this platform.
- Prefer the single most specific skill/rule when possible.
- If no skill or rule clearly matches, ignore all and answer normally.

# /orchestrate - Multi-Agent Orchestration

$ARGUMENTS

## Purpose
Coordinate multiple specialist perspectives for complex tasks.

## Minimum Requirement
Use at least 3 distinct expert perspectives. If fewer are used, orchestration is incomplete.

## Phases
### Phase 1: Planning (sequential)
1. Create a plan file
2. Ask for user approval

### Phase 2: Implementation (parallel)
1. Execute domain work in parallel
2. Run verification scripts
3. Synthesize results

## Output Format
```markdown
## 🎼 Orchestration Report

### Task
[Original task summary]

### Mode
[Current mode]

### Agents Invoked (MINIMUM 3)
| # | Agent | Focus Area | Status |
|---|-------|------------|--------|
| 1 | project-planner | Task breakdown | ✅ |
| 2 | frontend-specialist | UI implementation | ✅ |
| 3 | test-engineer | Verification | ✅ |

### Verification Scripts Executed
- [x] security_scan.py → Pass/Fail
- [x] lint_runner.py → Pass/Fail

### Key Findings
1. **[Agent 1]**: Finding
2. **[Agent 2]**: Finding
3. **[Agent 3]**: Finding

### Deliverables
- [ ] Plan created
- [ ] Code implemented
- [ ] Tests passing
- [ ] Scripts verified

### Summary
[One paragraph synthesis of all agent work]
```

## Exit Gate
Before completing orchestration, verify:
- ✅ Invoked 3+ expert perspectives
- ✅ Verification scripts ran
- ✅ Report generated
