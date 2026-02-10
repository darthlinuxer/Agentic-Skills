# Ecosystem Automation Scripts

**Purpose**: Automated tools for maintaining the LLM agent ecosystem across platforms

---

## 📋 Available Scripts

### 1. ecosystem_audit.py
**Purpose**: Comprehensive ecosystem health checker

**Checks**:
- File existence across platforms
- Content synchronization (mirroring)
- Metadata compliance per platform specs
- Cross-platform references
- Broken internal links
- YAML syntax errors

**Usage**:
```bash
cd /workspace
python3 scripts/ecosystem/ecosystem_audit.py

# View results
cat AUDIT_REPORT.json
```

**Output**: Console report + `AUDIT_REPORT.json`

---

### 2. sync_content.py
**Purpose**: Synchronize content across platforms

**Strategy**:
- Source of truth: `.agent`
- Targets: `.claude`, `.cursor`
- Preserves platform-specific metadata
- Syncs only content (after frontmatter)

**Usage**:
```bash
cd /workspace
python3 scripts/ecosystem/sync_content.py
```

**Syncs**: Agents, Skills, Commands/Workflows

---

### 3. remove_agent_frontmatter.py
**Purpose**: Remove frontmatter from agent files

**Why**: Per official specs, agents should be plain markdown

**Usage**:
```bash
cd /workspace
python3 scripts/ecosystem/remove_agent_frontmatter.py
```

**Processes**: 60 files (20 agents × 3 platforms)

---

### 4. simplify_skills_metadata.py
**Purpose**: Clean up skills metadata to match specs

**Keeps**:
- Antigravity: `description` (+ optional `name`)
- Claude/Cursor: `name`, `description` (+ optional `license`)

**Removes**: All non-standard fields

**Usage**:
```bash
cd /workspace
python3 scripts/ecosystem/simplify_skills_metadata.py
```

**Processes**: 228 files (76 skills × 3 platforms)

---

### 5. add_mcp_references.py
**Purpose**: Add MCP tool references to complex skills

**Adds**:
- Context7 references (documentation search)
- Sequential Thinking references (complex reasoning)
- Both (for highly complex skills)

**Usage**:
```bash
cd /workspace
python3 scripts/ecosystem/add_mcp_references.py
```

**Edit**: Modify skill categorization in script if needed

---

## 🔄 Maintenance Workflow

### Monthly
```bash
# Check ecosystem health
python3 scripts/ecosystem/ecosystem_audit.py
```

### After Major Changes
```bash
# Re-sync content if source of truth (.agent) was updated
python3 scripts/ecosystem/sync_content.py

# Re-run audit
python3 scripts/ecosystem/ecosystem_audit.py
```

### When Adding New Skills
1. Add to `.agent/skills/new-skill/SKILL.md`
2. Run `sync_content.py` to mirror to other platforms
3. If complex, edit `add_mcp_references.py` and run it
4. Run audit to verify

---

## 📊 Expected Results

After running all scripts correctly:

- ✅ Critical Errors: 0
- ✅ Content Mismatches: 0
- ✅ Metadata Issues: 0
- ✅ Spec Compliance: 100%

---

*Scripts created: February 9, 2026*  
*Location: /workspace/scripts/ecosystem/*
