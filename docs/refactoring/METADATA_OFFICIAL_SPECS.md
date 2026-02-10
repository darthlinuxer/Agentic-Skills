# Official Platform Metadata Specifications

**Date**: February 9, 2026  
**Source**: Official platform documentation  
**Status**: ✅ Verified

---

## 📋 Official Requirements by Platform

### Claude (Anthropic)

| Component | Required Metadata | Optional Metadata | File Extension |
|-----------|------------------|-------------------|----------------|
| **Agents** | None (plain markdown) | Custom fields (name, description) in community examples | .md |
| **Skills** | `name`, `description` | `license`, `model`, `permissions`, `metadata`, `disable-model-invocation` | .md |
| **Rules** | None (plain markdown) | `description` in some examples; often embedded in CLAUDE.md | .md |
| **Commands** | None (plain markdown) | None | .md |

**Skills name requirements:**
- kebab-case
- lowercase letters/numbers/hyphens only
- max 64 chars
- matches folder name
- no XML/reserved words

---

### Cursor

| Component | Required Metadata | Optional Metadata | File Extension |
|-----------|------------------|-------------------|----------------|
| **Agents** | None (plain markdown) | None; subagents maintain separate context | .md |
| **Skills** | `name`, `description` | `license`, `compatibility`, `metadata`, `disable-model-invocation` | .md |
| **Rules** | None | `description`, `globs`, `alwaysApply` | .md or .mdc |
| **Commands** | None (plain markdown) | None | .md |

**Skills name requirements:**
- lowercase letters/numbers/hyphens
- matches folder name

**Rules configuration** (`.cursor/rules/` directory):

Rules are configured through frontmatter in `.md` or `.mdc` files. The mode is set via UI or properties:

- **Always Apply**: `alwaysApply: true` - Applied to every chat session. For universal project standards.
- **Apply Intelligently**: `alwaysApply: false` with `description` - AI decides relevance based on description.
- **Apply to Specific Files**: `globs: "*.ts,*.tsx"` - Applied when files match glob patterns. For file-type specific rules.
- **Apply Manually**: No alwaysApply/globs - Activated via @-mention in chat (e.g., `@my-rule`). For on-demand use.

Rules can be user-level (global) or project-specific. Edit via settings UI or directly in files.

---

### Google Antigravity (Windsurf/Gemini)

| Component | Required Metadata | Optional Metadata | File Extension |
|-----------|------------------|-------------------|----------------|
| **Agents** | None (plain markdown) | None; AGENTS.md is plain markdown | .md |
| **Skills** | `description` | `name` (defaults to folder name) | .md |
| **Rules** | None (plain markdown) | None; activation defined at rule level, not in frontmatter | .md |
| **Workflows** | None (plain markdown) | None; invoked via /workflow-name | .md |

**Rules configuration**:

Rules are Markdown files (12k char limit) stored:
- Globally: `~/.gemini/GEMINI.md`
- Workspace-specific: `.agent/rules/`

Activation modes (defined at rule level, configured via UI or content):

- **Always On**: Always applied to the agent, regardless of context
- **Model Decision**: Model decides based on natural language description
- **Glob**: Applied automatically to files matching pattern (e.g., `*.js`, `src/**/*.ts`)
- **Manual**: Activated via @-mention in input (e.g., `@rule-name`)

Rules can reference other files with `@filename` (relative or absolute paths). Create via Customizations panel in UI.

**Limits:**
- Rules: 12k chars max
- Workflows: 12k chars max

---

## 🚨 Issues Found in Current Implementation

### ❌ Non-Standard Metadata Added

We added metadata fields that are **NOT part of official specs**:

#### In Agents (ALL platforms):
- ❌ `tools` - Not required by any platform
- ❌ `model` - Not required (Claude: optional in skills only)
- ❌ `skills` - Not required
- ❌ `color` - Not in official spec (Claude)
- ❌ `readonly` - Not in official spec (Cursor)
- ❌ `is_background` - Not in official spec (Cursor)

#### In Skills:
- ❌ `allowed-tools` - Not in official spec
- ❌ `version` - Not in official spec (should use `metadata` if needed)
- ❌ `priority` - Not in official spec
- ❌ `author`, `source`, `importedFrom`, `importedAt` - Should be in `metadata` block if kept

#### In Rules:
- ❌ `trigger: always_on` - Not in official spec (Antigravity) - activation configured via UI, not frontmatter
- ✅ `alwaysApply` - Valid for Cursor .md/.mdc files (for Always Apply mode)
- ✅ `description` - Valid for Cursor rules (especially for Apply Intelligently mode)
- ✅ `globs` - Valid for Cursor rules (for Apply to Specific Files mode)

---

## ✅ Correct Metadata Format

### Claude Skills
```yaml
---
name: skill-name
description: "Brief description of what this skill does"
license: MIT
---
```

### Cursor Skills
```yaml
---
name: skill-name
description: "Brief description of what this skill does"
license: MIT
---
```

### Cursor Rules (.md or .mdc)

**Always Apply mode:**
```yaml
---
description: "Global project standards"
alwaysApply: true
---
```

**Apply Intelligently mode:**
```yaml
---
description: "Use when working with TypeScript and type safety is important"
alwaysApply: false
---
```

**Apply to Specific Files mode:**
```yaml
---
description: "TypeScript/TSX specific linting rules"
globs: "*.ts,*.tsx"
---
```

**Apply Manually mode (no frontmatter needed):**
```markdown
# My Custom Rule

[Plain markdown content]
```

### Antigravity Rules

**No frontmatter** - Plain markdown files:
```markdown
# Rule Name

[Plain markdown content - activation configured via UI]
```

Rules are configured via Customizations panel UI for activation mode (Always On, Model Decision, Glob, Manual).

### Antigravity Skills
```yaml
---
description: "Brief description of what this skill does"
---
```

OR with explicit name:
```yaml
---
name: skill-name
description: "Brief description of what this skill does"
---
```

### All Agents, Antigravity Rules, All Commands/Workflows
**No frontmatter required** - Plain markdown files

---

## 🔧 Correction Plan

### Phase 1.5: Metadata Cleanup

#### 1. Remove Non-Standard Fields from Agents (60 files)

**Before** (.agent/agents/frontend-specialist.md):
```yaml
---
name: frontend-specialist
description: Senior Frontend Architect...
tools: Read, Grep, Glob, Bash, Edit, Write
model: inherit
skills: clean-code, nextjs-react-expert
---
```

**After** (plain markdown):
```markdown
# Senior Frontend Architect

> Specialist in React/Next.js systems with performance-first mindset

[Content continues...]
```

#### 2. Clean Up Skills Metadata (228 files)

**Before** (.agent/skills/clean-code/SKILL.md):
```yaml
---
name: clean-code
description: Pragmatic coding standards
allowed-tools: Read, Write, Edit
version: 2.0
priority: CRITICAL
---
```

**After**:
```yaml
---
description: "Pragmatic coding standards - concise, direct, no over-engineering"
---
```

**Before** (.claude/skills/clean-code/SKILL.md):
```yaml
---
name: clean-code
description: Pragmatic coding standards
version: 2.0
---
```

**After**:
```yaml
---
name: clean-code
description: "Pragmatic coding standards - concise, direct, no over-engineering"
---
```

**Before** (.cursor/skills/clean-code/SKILL.md or .mdc):
```yaml
---
name: clean-code
description: Pragmatic coding standards
version: 2.0
---
```

**After**:
```yaml
---
name: clean-code
description: "Pragmatic coding standards - concise, direct, no over-engineering"
---
```

#### 3. Fix Rules Metadata (8 files)

**Antigravity Rules** (.agent/rules/*.md) - Remove frontmatter:

**Before** (.agent/rules/gemini.md):
```yaml
---
trigger: always_on
---
```

**After** (plain markdown - activation configured via UI):
```markdown
# gemini.md - Antigravity Kit

> This file defines how the AI behaves in this workspace.

[Content continues...]
```

**Cursor Rules** (.cursor/rules/*.mdc) - Keep or add proper frontmatter:

**Current** (.cursor/rules/gemini.mdc):
```yaml
---
alwaysApply: true
---
```

**Action**: Keep as-is (valid for Always Apply mode) ✅

**OR** if you want Apply Intelligently mode:
```yaml
---
description: "Core Antigravity Kit behavior and agent routing protocol"
alwaysApply: false
---
```

#### 4. Commands/Workflows - Remove Metadata (51 files)

**Before** (.agent/workflows/create.md):
```yaml
---
description: Workflow for /create - Create Application.
---
```

**After** (remove frontmatter):
```markdown
# /create - Create Application

$ARGUMENTS

## Task
Start a new application creation process.

[Content continues...]
```

---

## 📊 Impact Analysis

### Files to Modify

| Platform | Component | Count | Action |
|----------|-----------|-------|--------|
| .agent | Agents | 20 | Remove all frontmatter |
| .claude | Agents | 20 | Remove all frontmatter |
| .cursor | Agents | 20 | Remove all frontmatter |
| .agent | Skills | 76 | Keep only `description` |
| .claude | Skills | 76 | Keep only `name`, `description` |
| .cursor | Skills | 76 | Keep only `name`, `description` |
| .agent | Rules | 4 | Remove frontmatter |
| .cursor | Rules | 4 | Keep `alwaysApply` if .mdc |
| .agent | Workflows | 17 | Remove frontmatter |
| .claude | Commands | 17 | Already no frontmatter (mostly) |
| .cursor | Commands | 17 | Already no frontmatter (mostly) |

**Total files to modify**: ~300+ files

---

## ✅ Benefits of Spec-Compliant Metadata

1. **Platform Compatibility**: Files will work correctly in official platforms
2. **Future-Proof**: Won't break with platform updates
3. **Cleaner Files**: Less clutter, easier to read
4. **Standard Compliance**: Follows official documentation
5. **Better Portability**: Easier to share and reuse

---

## 🎯 Implementation Strategy

### Batch 1: Agents (Priority: High)
- Remove all frontmatter from 60 agent files
- Keep content as plain markdown
- Test loading in each platform

### Batch 2: Skills (Priority: Critical)
- Simplify metadata to required fields only
- Antigravity: `description` only
- Claude/Cursor: `name` + `description`
- Move optional info (version, author) to content or remove

### Batch 3: Rules (Priority: Medium)
- Antigravity: Remove frontmatter
- Cursor: Keep `alwaysApply` for .mdc files
- No changes to content

### Batch 4: Commands/Workflows (Priority: Low)
- Remove frontmatter where present
- Most already have no frontmatter
- Keep content unchanged

---

## 📝 Special Cases to Handle

### Skills with Import Metadata

Files like `mcp-builder`, `verification-before-completion` that have:
```yaml
author: "anthropics"
source: "github"
importedFrom: ""
importedAt: "2026-02-04T09:22:46.437Z"
```

**Solution**: Move to content as a comment or remove entirely:
```markdown
---
name: mcp-builder
description: "Guide for creating high-quality MCP servers..."
---

# MCP Server Development Guide

> Originally imported from Anthropics GitHub, 2026-02-04

[Content...]
```

### Skills with License

Skills with `license: MIT` or `license: Proprietary`:

**Solution**: Keep in metadata (it's optional but valid):
```yaml
---
name: docx
description: "Comprehensive document creation..."
license: "Proprietary. Complete terms in LICENSE.txt"
---
```

---

## ⚠️ Risk Assessment

### Low Risk
- Removing non-standard metadata shouldn't break functionality
- Platforms ignore unknown fields anyway
- Content remains unchanged

### Medium Risk
- Some community tools might expect certain fields
- Need to test in actual platforms after changes

### Mitigation
- Make changes in branch
- Test before merging
- Keep backup of current state

---

## ✅ Next Steps

1. **Confirm Approach**: User approval to proceed with cleanup
2. **Create Backup**: Commit current state before changes
3. **Batch Processing**: Modify files in batches with commits
4. **Testing**: Verify files load correctly in each platform
5. **Documentation**: Update ARCHITECTURE.md and README

---

*Official specifications retrieved: February 9, 2026*  
*Ready to implement spec-compliant metadata structure*
