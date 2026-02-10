# Metadata Verification Required

**Date**: February 9, 2026  
**Status**: ⏸️ Paused - Awaiting Official Documentation

---

## 🎯 Purpose

Before continuing with Phase 2, we need to verify that metadata formats match official platform documentation for:
1. **Claude** (.claude directory)
2. **Cursor** (.cursor directory)  
3. **Antigravity/Windsurf** (.agent directory)

---

## 📋 What Needs Verification

### For Each Platform:

#### 1. Agent Files (agents/*.md)
**Current metadata fields observed**:

**.agent** (Antigravity):
```yaml
---
name: string
description: string
tools: string (comma-separated) OR array
model: string
skills: string (comma-separated)
---
```

**.claude**:
```yaml
---
name: string
description: string
model: string
color: string
tools: array
---
```

**.cursor**:
```yaml
---
name: string
description: string
tools: string (comma-separated)
model: string
readonly: boolean
is_background: boolean
skills: string (comma-separated)
---
```

**Questions**:
- Are these the correct required fields per platform?
- Are there additional optional fields we should include?
- What are the valid values for each field?

#### 2. Skill Files (skills/*/SKILL.md or SKILL.mdc)
**Current metadata fields observed**:

**.agent** (SKILL.md):
```yaml
---
name: string
description: string
allowed-tools: string
version: string
priority: string (optional, e.g., "CRITICAL")
---
```

**.claude** (SKILL.md):
```yaml
---
name: string
description: string
version: string (optional)
---
```

**.cursor** (SKILL.mdc):
```yaml
---
name: string
description: string
version: string (optional)
---
```

**Questions**:
- Are there platform-specific metadata fields for skills?
- Should skills reference tools or other dependencies?
- What's the correct format for versioning?

#### 3. Rules Files
**Current metadata fields observed**:

**.agent** (rules/*.md):
```yaml
---
trigger: string (e.g., "always_on")
---
```

**.cursor** (rules/*.mdc):
```yaml
---
alwaysApply: boolean
---
```

**.claude**: 
- No rules directory observed - are rules embedded differently?

**Questions**:
- What's the correct metadata for rules in each platform?
- Does Claude support rules files?
- Are there other trigger/apply options?

#### 4. Commands/Workflows
**Current metadata fields observed**:

**.agent** (workflows/*.md):
```yaml
---
description: string
---
```

**.claude** (commands/*.md):
- Often no frontmatter

**.cursor** (commands/*.md):
- Often no frontmatter

**Questions**:
- Should commands/workflows have metadata?
- What fields are supported?
- Are they invoked differently per platform?

---

## 🔍 Documentation Links Needed

Please provide official documentation URLs for:

### 1. Claude Platform
- [ ] Custom instructions / Project knowledge format
- [ ] Agent/skill metadata specification
- [ ] Command structure
- **Suggested search**: "Claude Projects custom instructions format", "Anthropic Claude agent metadata"

### 2. Cursor Platform  
- [ ] .cursorrules format specification
- [ ] Agent metadata format
- [ ] Skill (.mdc) file format
- **Suggested search**: "Cursor rules documentation", "Cursor .mdc format", "Cursor agent configuration"

### 3. Antigravity/Windsurf (Codeium)
- [ ] Agent configuration format
- [ ] Skill metadata specification  
- [ ] Workflow/slash command format
- **Suggested search**: "Windsurf agent configuration", "Codeium Cascade custom agents", "Antigravity kit documentation"

---

## 🔧 Current Assumptions (To Be Verified)

Based on code analysis, here are assumptions we're making:

### Assumption 1: Content Mirroring
**Assumption**: Content (everything after frontmatter) should be identical across platforms, only metadata differs.
- ✅ **Verify**: Is this correct?

### Assumption 2: File Extensions
**Assumption**: 
- Claude uses `.md`
- Cursor uses `.mdc` for skills and rules
- Antigravity uses `.md`
- ✅ **Verify**: Are these the correct extensions?

### Assumption 3: Directory Structure
**Assumption**:
- Claude: agents/, skills/, commands/
- Cursor: agents/, skills/, commands/, rules/
- Antigravity: agents/, skills/, workflows/, rules/
- ✅ **Verify**: Is this structure correct?

### Assumption 4: Metadata Parsing
**Assumption**: All platforms parse YAML frontmatter between `---` delimiters
- ✅ **Verify**: Do all platforms use YAML? Any exceptions?

---

## 🎯 Expected Outcomes

After verification:

1. **Corrected Metadata Templates** for each file type per platform
2. **Documentation References** embedded in files pointing to official sources
3. **Validation Rules** in audit script to check metadata compliance
4. **Migration Script** to update existing files if formats need correction

---

## 📝 Interim Actions (What I Can Do Now)

While waiting for documentation:

### 1. Analyze Existing Patterns
- [x] Examined 20 agent files across platforms
- [x] Examined 76 skill files across platforms
- [ ] Document pattern inconsistencies
- [ ] Create metadata comparison matrix

### 2. Check for Internal Documentation
- [x] Checked for README files
- [x] Checked for config files
- [x] Found mcp_config.json with Context7 configured
- [ ] Search for any embedded documentation

### 3. Prepare Metadata Standardization Scripts
- [ ] Create metadata validator for each platform
- [ ] Create metadata migration tool
- [ ] Add platform-specific validation to audit script

---

## 🚨 Risks of Proceeding Without Verification

1. **Incorrect Metadata**: Files may not load or behave correctly in platforms
2. **Missing Features**: May not utilize platform-specific capabilities
3. **Breaking Changes**: Future platform updates may break non-standard metadata
4. **Inconsistent Behavior**: LLM may interpret files differently than intended

---

## ✅ Recommended Next Steps

1. **User Provides Documentation Links** (fastest)
   - Official platform docs for metadata formats
   - Any example repositories or templates
   
2. **Use MCP Context7** (if available)
   - Search for latest platform documentation
   - Verify current metadata standards
   
3. **Manual Platform Testing** (slowest but thorough)
   - Create test files with different metadata
   - Load in each platform
   - Document what works

---

## 📞 Questions for User

1. Do you have links to official documentation for:
   - Claude custom instructions/agents?
   - Cursor .cursorrules and agent formats?
   - Antigravity/Windsurf agent configuration?

2. Are you using specific versions of these platforms?
   - Claude: Claude.ai, Claude Desktop, API?
   - Cursor: Version number?
   - Antigravity: Windsurf IDE version?

3. Do you have example files from each platform that are known to work correctly?

4. Should I use MCP Context7 to search for this documentation automatically?
   - I can see it's configured in .agent/mcp_config.json
   - Need API key to be set up

---

## 🔄 Current Status

**PAUSED**: Awaiting documentation verification before:
- Completing Phase 2 (Content Synchronization)
- Potential Phase 1.5 (Metadata Correction)
- Adding MCP Context7 and Sequential Thinking references

**READY TO RESUME**: Once documentation is provided or verified

---

*Created: February 9, 2026*  
*Status: Awaiting user input on documentation sources*
