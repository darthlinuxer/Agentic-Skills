# Skill Content Consolidation Strategy

## Overview

This document establishes the single source of truth for skill content across all three platforms (.agent, .claude, .cursor).

## Master Platform

**`.claude`** is designated as the master platform for skill content.

Rationale:
- Most comprehensive skill coverage
- Primary development platform
- Most frequently updated

## Consolidation Approach

### 1. Common Skills (67 skills)

All skills that exist in all three platforms use `.claude/skills/<skill>/SKILL.md` as the source of truth.

### 2. Platform-Specific Skills

| Platform | Unique Skills |
|----------|---------------|
| .agent | gemini |
| .claude | (none unique) |
| .cursor | verifier |

### 2.1 Platform-Specific Exceptions

The following skill MUST remain platform-specific (not synced) due to platform isolation requirements:

| Skill | Reason |
|-------|--------|
| create-subagent | Contains platform-specific path references (e.g., `.agent/agents/`, `.claude/agents/`) |

### 3. Sync Process

For each common skill:
1. Read content from `.claude/skills/<skill>/SKILL.md`
2. Copy to `.agent/skills/<skill>/SKILL.md`
3. Copy to `.cursor/skills/<skill>/SKILL.md`

### 4. Validation

A content consistency check should be added to the validation pipeline to detect future divergence.

## Verification

After consolidation, run:
```bash
# Verify no differences remain
for skill in $(comm -12 <(ls .agent/skills/) <(ls .claude/skills/) | comm -12 - <(ls .cursor/skills/)); do
  diff .agent/skills/$skill/SKILL.md .claude/skills/$skill/SKILL.md
  diff .claude/skills/$skill/SKILL.md .cursor/skills/$skill/SKILL.md
done
```

## Last Updated

2026-02-22
