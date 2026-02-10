# LLM Agent Ecosystem Refactoring Roadmap

> Action plan based on audit results from February 9, 2026

---

## 📊 Current State Summary

### Ecosystem Inventory
- **20 Agents** across 3 platforms ✅
- **76 Skills** across 3 platforms (2 missing in some platforms)
- **4 Rules** across applicable platforms
- **17 Commands/Workflows** across 3 platforms ✅
- **20 Skills** with enhancement scripts (26% coverage)
- **5 Skills** with reference documentation

### Health Status: 🔴 NEEDS WORK

**Issues Found**:
- 🔴 **19 Critical Errors** (YAML errors, missing files, incorrect references)
- ⚠️ **109 Warnings** (content mismatches, cross-platform references)
- 📊 **Total**: 128 issues to address

---

## 🎯 Phase 1: Critical Fixes (Week 1) - PRIORITY

### 1.1 Fix YAML Syntax Errors

**Skills with YAML errors** (affects all 3 platforms):
1. `docx/SKILL.md` - Colon in description
2. `lint-and-validate/SKILL.md` - Colon in description  
3. `mcp-builder/SKILL.md` - Malformed frontmatter
4. `verification-before-completion/SKILL.md` - Malformed frontmatter

**Fix Action**:
```yaml
# BAD (causes YAML error)
description: Creating documents (.docx files) for: (1) Creating new documents

# GOOD (quote strings with colons)
description: "Creating documents (.docx files) for: (1) Creating new documents"
```

**Commands**:
```bash
# Fix each skill across all platforms
# Example for docx:
sed -i 's/^description: \(.*:\)/description: "\1"/' .agent/skills/docx/SKILL.md
sed -i 's/^description: \(.*:\)/description: "\1"/' .claude/skills/docx/SKILL.md
sed -i 's/^description: \(.*:\)/description: "\1"/' .cursor/skills/docx/SKILL.mdc
```

### 1.2 Fix Incorrect Reference in gemini.mdc

**Issue**: `.cursor/rules/gemini.mdc` references `SKILL.mdccc` instead of `SKILL.mdc`

**Location**: Line 17 (approximately)

**Fix**:
```bash
sed -i 's/SKILL\.mdccc/SKILL.mdc/g' .cursor/rules/gemini.mdc
```

### 1.3 Add Missing Skill: aesthetic

**Issue**: `aesthetic` skill folder exists in `.cursor` but missing `SKILL.md` in `.agent` and `.claude`

**Action**:
1. Check if `.cursor/skills/aesthetic/SKILL.mdc` exists and has content
2. Mirror to `.agent/skills/aesthetic/SKILL.md`
3. Mirror to `.claude/skills/aesthetic/SKILL.md`

### 1.4 Fix Missing Metadata in debugger.md

**Issue**: `debugger.md` missing `tools` and `model` metadata in `.agent` and `.cursor`

**Fix for .agent/agents/debugger.md**:
```yaml
---
name: debugger
description: [existing]
tools: Read, Grep, Glob, Bash, Edit, Write
model: inherit
skills: systematic-debugging
---
```

**Fix for .cursor/agents/debugger.md**:
```yaml
---
name: debugger
description: [existing]
tools: Read, Grep, Glob, Bash, Edit, Write
model: inherit
readonly: false
is_background: false
skills: systematic-debugging
---
```

---

## 🔄 Phase 2: Content Synchronization (Week 2-3)

### 2.1 Sync Agent Content (35 mismatches)

**Agents with content mismatches**:
- backend-specialist
- code-archaeologist
- database-architect
- debugger
- devops-engineer
- documentation-writer
- explorer-agent
- frontend-specialist
- game-developer
- mobile-developer
- orchestrator
- penetration-tester
- performance-optimizer
- product-manager
- product-owner
- project-planner
- qa-automation-engineer
- security-auditor
- seo-specialist
- test-engineer

**Strategy**:
1. Choose `.agent` as source of truth
2. Extract content (excluding frontmatter) from `.agent/agents/*.md`
3. Apply to `.claude/agents/*.md` and `.cursor/agents/*.md` with platform-specific metadata

**Automation**:
```python
# Use the mirror_content.py script (to be created in Phase 3)
python mirror_content.py --type agent --source .agent --sync-all
```

### 2.2 Sync Skill Content

**Skills with content mismatches**: Many (see audit report)

**Strategy**: Same as agents - use `.agent` as source of truth

---

## 🔗 Phase 3: Self-Containment (Week 4)

### 3.1 Remove Cross-Platform References

**Files with cross-platform references** (12 instances):
- `.claude/agents/project-planner.md` (references `.agent`)
- `.cursor/agents/project-planner.md` (references `.agent`)
- Various skill files

**Fix Pattern**:
```markdown
# BAD
See .agent/skills/frontend-design/SKILL.md for details

# GOOD (in .agent files)
See .agent/skills/frontend-design/SKILL.md for details

# GOOD (in .claude files)  
See .claude/skills/frontend-design/SKILL.md for details

# GOOD (in .cursor files)
See .cursor/skills/frontend-design/SKILL.mdc for details
```

**Automated Fix**:
```bash
# For .claude files, replace .agent references
find .claude -name "*.md" -exec sed -i 's/\.agent\//\.claude\//g' {} \;

# For .cursor files, replace .agent references  
find .cursor -name "*.md" -o -name "*.mdc" -exec sed -i 's/\.agent\//\.cursor\//g' {} \;

# Also need to update SKILL.md to SKILL.mdc in .cursor references
find .cursor -name "*.md" -o -name "*.mdc" -exec sed -i 's/SKILL\.md/SKILL.mdc/g' {} \;
```

---

## 📈 Phase 4: Enhancement (Week 5-8)

### 4.1 Add Scripts to More Skills

**Goal**: Increase from 20 skills (26%) to 30+ skills (40%) with scripts

**Candidates for script enhancement**:
1. `code-review-checklist` - Automated code review script
2. `architecture` - Diagram generator
3. `documentation-templates` - Doc generator
4. `i18n-localization` - Translation checker
5. `git` - Git flow automation
6. `deployment-procedures` - Deployment validator
7. `database-design` - Schema validator
8. `api-patterns` - API spec validator
9. `backend-development` - Backend health checker
10. `frontend-development` - Frontend bundle analyzer

**Script Template**:
```python
#!/usr/bin/env python3
"""
{skill_name}_helper.py - Automation for {skill_name} skill
"""

def main():
    """Main entry point"""
    pass

if __name__ == '__main__':
    main()
```

### 4.2 Add Reference Documentation

**Goal**: Increase from 5 skills (7%) to 20+ skills (26%) with references

**Candidates**:
- All major technical skills should have reference docs
- Templates, checklists, examples

### 4.3 Update Skills to 2025+ Best Practices

**Skills to update**:
- `nextjs-react-expert` - React 19, Next.js 15
- `typescript-expert` - TypeScript 5.5+
- `testing-patterns` - Vitest, modern patterns
- `api-patterns` - OpenAPI 3.1, GraphQL Federation v2
- `deployment-procedures` - GitHub Actions, modern CI/CD
- `vulnerability-scanner` - OWASP Top 10 2025

---

## 🧪 Phase 5: Validation (Week 9)

### 5.1 Re-run Audit

```bash
python ecosystem_audit.py
```

**Success Criteria**:
- 0 critical errors
- < 10 warnings
- 100% content mirroring
- 0 cross-platform references
- 0 broken links

### 5.2 Manual Testing

**Test Matrix**:
| Agent | Test Scenario | Platform | Result |
|-------|---------------|----------|--------|
| frontend-specialist | Create React component | .agent | ✅ |
| frontend-specialist | Create React component | .claude | ✅ |
| frontend-specialist | Create React component | .cursor | ✅ |
| backend-specialist | Create API endpoint | .agent | ✅ |
| ... | ... | ... | ... |

---

## 📝 Phase 6: Documentation (Week 10)

### 6.1 Update ARCHITECTURE.md

- Reflect current skill count (76)
- Update script coverage metrics
- Add new skills to categorization

### 6.2 Create CHANGELOG.md

Document all changes made during refactoring:
- Fixed YAML errors
- Synced content across platforms
- Removed cross-platform references
- Added X new scripts
- Updated Y skills to 2025 standards

### 6.3 Update README.md

- Quick start guide
- Platform differences table
- Link to ARCHITECTURE.md

---

## 🛠️ Automation Scripts Needed

### Script 1: Content Mirror Tool

**File**: `mirror_content.py`

**Purpose**: Sync content from source platform to others while preserving metadata

**Usage**:
```bash
# Sync single agent
python mirror_content.py --type agent --name frontend-specialist --source .agent

# Sync all agents
python mirror_content.py --type agent --source .agent --sync-all

# Sync single skill
python mirror_content.py --type skill --name clean-code --source .agent

# Sync all skills
python mirror_content.py --type skill --source .agent --sync-all
```

### Script 2: Cross-Reference Fixer

**File**: `fix_cross_refs.py`

**Purpose**: Automatically fix cross-platform references

**Logic**:
1. Scan all files in a platform
2. Find references to other platforms
3. Replace with platform-specific paths
4. Update file extensions (.md vs .mdc)

### Script 3: Metadata Validator

**File**: `validate_metadata.py`

**Purpose**: Ensure all files have required metadata for their platform

**Checks**:
- Required fields present
- Correct data types
- Valid values

### Script 4: Best Practices Updater

**File**: `update_best_practices.py`

**Purpose**: Scan skills for deprecated patterns and suggest updates

**Features**:
- Pattern matching for old frameworks/libraries
- Suggest modern alternatives
- Link to migration guides

---

## 📊 Success Metrics

Track these metrics before and after:

| Metric | Current | Target | Final |
|--------|---------|--------|-------|
| **Critical Errors** | 19 | 0 | ☐ |
| **Warnings** | 109 | <10 | ☐ |
| **Content Mismatches** | 35 | 0 | ☐ |
| **Cross-Platform Refs** | 12 | 0 | ☐ |
| **Broken Links** | 1 | 0 | ☐ |
| **YAML Errors** | 12 | 0 | ☐ |
| **Skills with Scripts** | 20 (26%) | 30 (40%) | ☐ |
| **Skills with References** | 5 (7%) | 20 (26%) | ☐ |
| **Metadata Compliance** | ~80% | 100% | ☐ |

---

## 🚀 Quick Start: Immediate Actions

### Today (February 9, 2026)

1. **Fix YAML errors** (30 min)
   ```bash
   # Run fix_yaml_errors.sh script (to be created)
   ./scripts/fix_yaml_errors.sh
   ```

2. **Fix gemini.mdc reference** (5 min)
   ```bash
   sed -i 's/SKILL\.mdccc/SKILL.mdc/g' .cursor/rules/gemini.mdc
   ```

3. **Fix debugger metadata** (10 min)
   - Manually add missing fields

4. **Re-run audit** (5 min)
   ```bash
   python ecosystem_audit.py
   ```
   - Should reduce errors from 19 to ~5

### This Week

- Complete Phase 1 (Critical Fixes)
- Start Phase 2 (Content Sync for top 10 agents)

### This Month

- Complete Phase 2 (Content Sync)
- Complete Phase 3 (Self-Containment)
- Start Phase 4 (Enhancement)

---

## 🎯 Priority Order

1. **🔴 CRITICAL** - Fix YAML errors (blocks LLM from reading files)
2. **🔴 CRITICAL** - Fix incorrect references (causes wrong file loads)
3. **🔴 CRITICAL** - Add missing metadata (causes agent failures)
4. **🟡 HIGH** - Sync content mismatches (inconsistent behavior)
5. **🟡 HIGH** - Remove cross-platform refs (breaks isolation)
6. **🟢 MEDIUM** - Add scripts to skills (enhancement)
7. **🟢 MEDIUM** - Update to 2025 best practices (quality)
8. **⚪ LOW** - Add reference docs (nice to have)

---

## 📞 Support Resources

- **Audit Tool**: `ecosystem_audit.py`
- **Review Prompt**: `ECOSYSTEM_REVIEW_PROMPT.md`
- **Architecture Doc**: `.agent/ARCHITECTURE.md`
- **This Roadmap**: `REFACTORING_ROADMAP.md`

---

## ✅ Sign-off Checklist

Before declaring refactoring complete:

- [ ] All YAML errors fixed
- [ ] All cross-platform references removed
- [ ] All content synced across platforms
- [ ] All agents have required metadata
- [ ] All skills have required metadata
- [ ] Audit shows 0 critical errors
- [ ] Audit shows <10 warnings
- [ ] At least 30 skills have scripts
- [ ] At least 20 skills have references
- [ ] Documentation updated (ARCHITECTURE.md, README.md, CHANGELOG.md)
- [ ] Manual testing completed on all 3 platforms
- [ ] Stakeholders approved

---

*Last Updated: February 9, 2026*  
*Status: Phase 1 Ready to Begin*
