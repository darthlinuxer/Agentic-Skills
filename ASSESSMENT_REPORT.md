# Agentic-Skills Comprehensive Assessment Report

**Report Date:** February 22, 2026
**Assessment Period:** February 22, 2026
**Analyst:** Autonomous Agent

---

## Executive Summary

This report presents the findings from a comprehensive assessment of the Agentic-Skills project across three platforms: Agent (`.agent`), Claude Code (`.claude`), and Cursor IDE (`.cursor`). The assessment evaluated skill structure, format guidelines, conflicts, uniqueness, workflows, and platform-specific features.

**Key Finding:** The project contains 67-68 skills per platform with massive content duplication, but critically - **all skills with the same name have DIFFERENT content across platforms**, representing a major architectural conflict that undermines skill consistency and shareability.

---

## 1. Structure Analysis (AS-001)

### Platform Overview

| Platform | Skills | Agents | Commands/Workflows |
|----------|--------|--------|-------------------|
| `.agent` | 69 | 15+ | workflows/ |
| `.claude` | 68 | 19 | commands/ |
| `.cursor` | 67 | 19 | commands/, rules/ |

### Directory Structure

All three platforms share a similar structure:
- `skills/` - Skill definitions (SKILL.md files)
- `agents/` - Agent definitions
- `scripts/` - Utility scripts
- Platform-specific: `workflows/` (.agent), `commands/` (.claude, .cursor), `rules/` (.cursor)

### Skills Count
- **Total unique skill names:** ~67 common across all platforms
- **Root level:** 2 skills (prd, ralph) in skills/ directory

---

## 2. Format Guidelines (AS-002)

### Skills Format (Consistent Across All Platforms)

All skills follow the SKILL.md format with YAML frontmatter:
```yaml
---
name: skill-name
description: Skill description
---
```

### Agents Format (Platform Differences)

| Platform | Format | Key Differences |
|----------|--------|------------------|
| `.agent` | YAML frontmatter | name, description, model, color |
| `.claude` | Plain markdown | "Referenced skills" section |
| `.cursor` | YAML frontmatter | name, description, model, color, "Workspace Integration" |

### Commands/Workflows Format

| Platform | Format | Pattern |
|----------|--------|---------|
| `.agent` | YAML frontmatter | trigger, description |
| `.claude` | $ARGUMENTS | "Before answering" preamble |
| `.cursor` | $ARGUMENTS | "Before answering" preamble |

---

## 3. Conflicts and Duplicates (AS-003)

### Critical Conflicts

#### 3.1 Content Divergence (HIGH PRIORITY)
**Finding:** All 67 common skills have **DIFFERENT content** across platforms.

This is the most critical finding - skills with identical names contain substantially different implementations:
- `.claude` vs `.cursor`: 16 skills differ
- `.agent` vs others: Content differs from both

**Impact:** Skills cannot be shared or synchronized across platforms. Each platform maintains independent versions.

#### 3.2 Incorrectly Placed Files
- `doc.md` in `.agent/skills/` - This is documentation about creating skills, not a valid skill

#### 3.3 Duplicate Skills
- `gemini` skill exists in both `.agent` and `.claude` (should be consolidated)

#### 3.4 Missing Skills
- `gemini` skill missing from `.cursor`

### Naming Consistency
- All skills follow kebab-case naming convention
- Exception: `doc.md` is malformed

---

## 4. Validation Results (AS-004)

### Validation Checks Passed
- All skills have required SKILL.md files
- All skills have proper YAML frontmatter with name and description
- All skills follow kebab-case naming convention
- Template files (TEMPLATE.md) follow same frontmatter format

### Validation Issues
- 1 file misplaced: `doc.md` in `.agent/skills/`

---

## 5. Workflow and Command Flow Analysis (AS-005)

### Interaction Flow
```
User Command → Command/Workflow File → Agent (orchestrator) → Skills
```

### Key Findings
1. **Platform Isolation:** Strictly enforced - no cross-platform links allowed
2. **Command Similarity:** `.claude/commands/` and `.cursor/commands/` are nearly identical
3. **Orchestration:** All commands delegate to orchestrator agent with mode parameter
4. **Validation:** All checks pass (67-68 skills, 0 dangling references, valid links)

### Persistent Issue
- Skills referenced in agents have different content across platforms (per AS-003)

---

## 6. Platform-Specific Features (AS-006)

### Feature Comparison

| Feature | `.agent` | `.claude` | `.cursor` |
|---------|----------|-----------|-----------|
| Workflows/Commands | workflows/ | commands/ | commands/ |
| Memory | None | MEMORY.md | None |
| Unique Agent | - | - | verifier |
| Rules Directory | rules/ | - | - |
| Skill Count | 68 | 68 | 67 |

### Enhancement Opportunities Identified
1. Add persistent memory to `.agent` and `.cursor` (like `.claude`)
2. Add 'verifier' agent to `.agent` and `.claude` (unique to `.cursor`)
3. Align skill content across platforms to resolve AS-003 conflicts
4. Add `gemini` skill to `.cursor` (missing)

---

## 7. Enhancements Applied (AS-007)

### Skills Enhanced (.claude platform)
1. **intelligent-routing** - Added memory/recall patterns
2. **app-builder** - Added subagent orchestration patterns
3. **create-subagent** - Added memory integration

### Validations Passed
- Link validation
- Dangling skills check
- Platform isolation
- HTTP policy
- Docs secrets

---

## 8. Prioritized Action Items

### Critical (Must Fix)
1. **[HIGHEST]** Resolve content divergence - Decide on single source of truth per skill or implement merge strategy
2. **Move** `doc.md` out of `.agent/skills/` - It's documentation, not a skill
3. **Consolidate** `gemini` skill - Single source across platforms

### High Priority
4. **Add** missing `gemini` skill to `.cursor`
5. **Add** persistent memory to `.agent` and `.cursor` platforms
6. **Add** 'verifier' agent to `.agent` and `.claude`

### Medium Priority
7. **Standardize** agent format across all platforms
8. **Align** 16 differing skills between `.claude` and `.cursor`
9. **Create** synchronization mechanism for cross-platform skill updates

### Low Priority
10. Document skill development guidelines
11. Create validation for content consistency checks

---

## 9. Recommendations Summary

### Immediate Actions
1. Establish single source of truth for each skill to eliminate content divergence
2. Clean up misplaced documentation files
3. Standardize skill count across platforms (currently: 68, 68, 67)

### Strategic Recommendations
1. **Consolidation Strategy:** Choose one platform as the "master" for skill content, propagate to others
2. **Validation Pipeline:** Add content consistency checks to CI/CD
3. **Platform Parity:** Ensure feature parity (memory, verifier agent) across all platforms

### Technical Debt
1. Content divergence across 67 skills
2. 16 skills with different implementations between `.claude` and `.cursor`
3. Missing platform-specific features in `.agent` and `.cursor`

---

## Appendix: Skills Comparison Matrix

### Skills Present in All Platforms (~67 common)
All skills exist in all three platforms but with varying content.

### Skills Unique to Platforms
- `.agent`: - (none uniquely identified)
- `.claude`: 68 skills
- `.cursor`: 67 skills (missing gemini)

### Differing Skills Between .claude and .cursor (16)
1. architecture
2. create-rule
3. create-subagent
4. geo-fundamentals
5. intelligent-routing
6. lint-and-validate
7. mcp-builder
8. mobile-design
9. parallel-agents
10. senior-agile-pm-budget-analyst
11. senior-software-developer
12. sequential-thinking
13. update-cursor-settings
14. using-superpowers
15. writing-prompts
16. writing-skills

---

*Report generated from AS-001 through AS-007 assessments*
