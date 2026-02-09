# LLM Agent Ecosystem Review & Refactoring Prompt

> Comprehensive audit checklist for `.claude`, `.agent`, and `.cursor` platform configurations

---

## 🎯 Review Objectives

This prompt guides the systematic review and refactoring of a multi-platform LLM agent ecosystem following 7 critical guidelines:

1. **Uniqueness** - LLM should have no doubts which file to choose
2. **Self-Containment** - Correct links and platform-specific references
3. **Clarity** - Clear and concise content
4. **Structure Compliance** - Follows platform-specific documentation standards
5. **Modern Guidelines** - Ultimate best practices with enhanced scripts/references
6. **Content Mirroring** - Same content across platforms (only metadata differs)
7. **Purpose Clarity** - Understand and optimize each file's role in the ecosystem

---

## 📋 Platform Structure Overview

### Platform Directories

```
/workspace/
├── .agent/          # Antigravity Kit (Gemini/Windsurf)
│   ├── agents/      # 20 specialist agents
│   ├── skills/      # 75 skills
│   ├── workflows/   # 17 slash commands
│   ├── rules/       # 4 global rules (.md)
│   └── scripts/     # Master validation scripts
│
├── .claude/         # Claude Platform
│   ├── agents/      # 20 specialist agents
│   ├── skills/      # 75 skills
│   ├── commands/    # 17 commands
│   └── (rules may be embedded)
│
└── .cursor/         # Cursor Platform
    ├── agents/      # 20 specialist agents
    ├── skills/      # 75 skills
    ├── commands/    # 17 commands
    └── rules/       # 4 global rules (.mdc)
```

### File Extension Standards

| Platform | Agents | Skills | Rules | Commands/Workflows |
|----------|--------|--------|-------|-------------------|
| `.agent` | `.md` | `SKILL.md` | `.md` | `workflows/*.md` |
| `.claude` | `.md` | `SKILL.md` | `.md` (embedded?) | `commands/*.md` |
| `.cursor` | `.md` | `SKILL.mdc` | `.mdc` | `commands/*.md` |

### Metadata Format Differences

#### .agent (Antigravity)
```yaml
---
name: frontend-specialist
description: Senior Frontend Architect...
tools: Read, Grep, Glob, Bash, Edit, Write
model: inherit
skills: clean-code, nextjs-react-expert, web-design-guidelines
---
```

#### .claude
```yaml
---
name: frontend-specialist
description: Senior Frontend Architect...
model: inherit
color: blue
tools: ["Read", "Grep", "Glob", "Bash", "Edit", "Write"]
---
```

#### .cursor
```yaml
---
name: frontend-specialist
description: Senior Frontend Architect...
tools: Read, Grep, Glob, Bash, Edit, Write
model: inherit
readonly: false
is_background: false
skills: clean-code, nextjs-react-expert, web-design-guidelines
---
```

#### Rules Metadata
- `.agent`: `trigger: always_on`
- `.claude`: (check format)
- `.cursor`: `alwaysApply: true`

---

## 🔍 Review Checklist by Category

### 1. AGENTS (20 Files per Platform)

**Purpose**: Role-based AI personas that activate for specific domains

**Location**: 
- `.agent/agents/*.md`
- `.claude/agents/*.md`
- `.cursor/agents/*.md`

**Expected Agents**:
1. orchestrator
2. project-planner
3. frontend-specialist
4. backend-specialist
5. database-architect
6. mobile-developer
7. game-developer
8. devops-engineer
9. security-auditor
10. penetration-tester
11. test-engineer
12. debugger
13. performance-optimizer
14. seo-specialist
15. documentation-writer
16. product-manager
17. product-owner
18. qa-automation-engineer
19. code-archaeologist
20. explorer-agent

#### Agent Review Questions

For each agent file across all 3 platforms:

- [ ] **Uniqueness**: Is the agent name and description distinct enough that LLM can clearly identify when to use it?
- [ ] **Self-Containment**: Do all internal links reference platform-specific paths?
  - `.agent/skills/` for Antigravity
  - `.claude/skills/` for Claude
  - `.cursor/skills/` for Cursor
- [ ] **Metadata Correctness**:
  - `.agent`: Has correct `tools:`, `model:`, `skills:` format?
  - `.claude`: Has `color:` field, tools as array?
  - `.cursor`: Has `readonly:`, `is_background:` fields?
- [ ] **Content Mirror**: Is content identical across platforms (except metadata)?
- [ ] **Skills Reference**: Are referenced skills actually present in the skills folder?
- [ ] **Clarity**: Is the agent's purpose, expertise areas, and when-to-activate clear?
- [ ] **Modern Best Practices**: Does it reflect 2025+ standards?

#### Agent-Specific Audit Script

```bash
# Check agent consistency across platforms
for agent in orchestrator project-planner frontend-specialist backend-specialist database-architect mobile-developer game-developer devops-engineer security-auditor penetration-tester test-engineer debugger performance-optimizer seo-specialist documentation-writer product-manager product-owner qa-automation-engineer code-archaeologist explorer-agent; do
  echo "Checking: $agent"
  ls -l .agent/agents/$agent.md .claude/agents/$agent.md .cursor/agents/$agent.md 2>/dev/null || echo "  MISSING in one or more platforms"
done
```

---

### 2. SKILLS (75+ Files per Platform)

**Purpose**: Modular knowledge domains that agents load on-demand

**Location**:
- `.agent/skills/*/SKILL.md`
- `.claude/skills/*/SKILL.md`
- `.cursor/skills/*/SKILL.mdc`

**Structure**:
```
skill-name/
├── SKILL.md (or SKILL.mdc for .cursor)
├── scripts/           # Optional: Python/Bash automation
├── references/        # Optional: Templates, docs, examples
├── data/              # Optional: CSV data, configs
└── assets/            # Optional: Images, icons
```

#### Expected Skills (Current Count: 75)

**Frontend & UI** (5):
- nextjs-react-expert
- web-design-guidelines
- tailwind-patterns
- frontend-design
- ui-ux-pro-max

**Backend & API** (4):
- api-patterns
- nestjs-expert (if exists)
- nodejs-best-practices
- python-patterns

**Database** (2):
- database-design
- prisma-expert (if exists)

**TypeScript/JavaScript** (1):
- typescript-expert (if exists)

**Cloud & Infrastructure** (3):
- docker-expert (if exists)
- deployment-procedures
- server-management

**Testing & Quality** (5):
- testing-patterns
- webapp-testing
- tdd-workflow
- code-review-checklist
- lint-and-validate

**Security** (2):
- vulnerability-scanner
- red-team-tactics

**Architecture & Planning** (4):
- app-builder
- architecture
- plan-writing
- brainstorming

**Mobile** (2):
- mobile-design
- mobile-games

**Game Development** (7):
- game-development
- game-design
- game-audio
- game-art
- 2d-games
- 3d-games
- pc-games
- web-games
- multiplayer

**SEO & Growth** (2):
- seo-fundamentals
- geo-fundamentals

**Shell/CLI** (2):
- bash-linux
- powershell-windows

**Other Critical** (36+):
- clean-code
- behavioral-modes
- parallel-agents
- mcp-builder
- documentation-templates
- i18n-localization
- performance-profiling
- systematic-debugging
- ui-styling
- sequential-thinking
- templates
- toc
- intelligent-routing
- gemini
- git
- frontend-development
- backend-development
- verification-before-completion
- subagent-driven-development
- senior-software-developer
- senior-pmbok-pm
- senior-agile-pm-budget-analyst
- rust-pro
- research
- problem-solving
- using-superpowers
- update-cursor-settings
- writing-skills
- writing-plans
- writing-prompts
- vr-ar
- create-skill
- create-rule
- create-subagent
- migrate-to-skills
- docx
- test-driven-development

#### Skill Review Questions

For each skill across all 3 platforms:

- [ ] **Uniqueness**: Is the skill name and purpose non-overlapping with other skills?
- [ ] **File Extension**:
  - `.agent/skills/*/SKILL.md` ✓
  - `.claude/skills/*/SKILL.md` ✓
  - `.cursor/skills/*/SKILL.mdc` ✓
- [ ] **Self-Containment**: 
  - All script references point to `./scripts/` (relative)
  - All reference links point to `./references/` (relative)
  - No cross-platform absolute paths
- [ ] **Metadata Completeness**:
  - `name:` matches folder name?
  - `description:` is concise and clear?
  - `version:` present and updated?
  - `priority:` set if critical (e.g., clean-code)?
- [ ] **Content Mirror**: Content identical across platforms?
- [ ] **Scripts Enhancement**:
  - If skill uses scripts, are they in Python or Bash?
  - Do scripts enhance the skill's objective?
  - Are scripts documented in README.md?
- [ ] **References Organization**:
  - Are references logically organized?
  - Do they follow modern 2025+ best practices?
  - Are they actually referenced in SKILL.md?
- [ ] **Modern Best Practices**:
  - Does content reflect latest industry standards?
  - Are deprecated patterns removed?
  - Are AI-optimized patterns included?

#### Skill-Specific Audit Script

```python
# skills_audit.py
import os
from pathlib import Path

platforms = ['.agent', '.claude', '.cursor']
skill_extensions = {'.agent': 'SKILL.md', '.claude': 'SKILL.md', '.cursor': 'SKILL.mdc'}

for platform in platforms:
    skills_path = Path(platform) / 'skills'
    skill_dirs = [d for d in skills_path.iterdir() if d.is_dir()]
    
    print(f"\n{platform}: {len(skill_dirs)} skills")
    
    for skill_dir in skill_dirs:
        skill_file = skill_dir / skill_extensions[platform]
        if not skill_file.exists():
            print(f"  ❌ MISSING: {skill_dir.name}/{skill_extensions[platform]}")
        
        # Check for scripts
        scripts_dir = skill_dir / 'scripts'
        if scripts_dir.exists():
            script_count = len(list(scripts_dir.glob('*.py'))) + len(list(scripts_dir.glob('*.sh')))
            print(f"  📜 {skill_dir.name}: {script_count} scripts")
```

---

### 3. RULES (4 Files per Platform)

**Purpose**: Global rules that apply across all interactions

**Location**:
- `.agent/rules/*.md`
- `.claude/rules/*.md` (or embedded in skills?)
- `.cursor/rules/*.mdc`

**Expected Rules**:
1. coding-style
2. gemini (master orchestration rules)
3. git
4. toc (table of contents / navigation)

#### Rules Review Questions

For each rule across platforms:

- [ ] **Uniqueness**: Is each rule's scope clearly defined and non-overlapping?
- [ ] **File Extension**:
  - `.agent/rules/*.md` ✓
  - `.claude/rules/*.md` ✓
  - `.cursor/rules/*.mdc` ✓
- [ ] **Metadata**:
  - `.agent`: `trigger: always_on`
  - `.cursor`: `alwaysApply: true`
  - `.claude`: (check format)
- [ ] **Self-Containment**: 
  - References to skills use platform-specific paths
  - References to agents use platform-specific paths
- [ ] **Content Mirror**: Identical content except metadata?
- [ ] **Clarity**: 
  - Are rules concise?
  - Are they actionable?
  - Do they avoid ambiguity?
- [ ] **Priority System**: Is rule priority/precedence clearly defined?
- [ ] **Gemini.md Special**:
  - Does it reference the correct skill file extensions for each platform?
  - `.agent`: references `SKILL.md`
  - `.cursor`: references `SKILL.mdc` (not `SKILL.mdccc`)

**Critical**: The gemini rule has a typo referencing `SKILL.mdccc` instead of `SKILL.mdc` for Cursor!

---

### 4. COMMANDS/WORKFLOWS (17 Files per Platform)

**Purpose**: Slash command procedures that orchestrate agents and skills

**Location**:
- `.agent/workflows/*.md`
- `.claude/commands/*.md`
- `.cursor/commands/*.md`

**Expected Commands/Workflows**:
1. brainstorm
2. create
3. debug
4. deploy
5. docs
6. enhance
7. explain
8. fix
9. implement
10. orchestrate
11. plan
12. preview
13. refactor
14. review
15. status
16. test
17. ui-ux-pro-max

#### Commands/Workflows Review Questions

For each command/workflow:

- [ ] **Uniqueness**: Is the command trigger word unique?
- [ ] **Naming Consistency**:
  - `.agent`: Located in `workflows/` folder
  - `.claude`: Located in `commands/` folder
  - `.cursor`: Located in `commands/` folder
- [ ] **Self-Containment**:
  - References to agents use platform paths
  - References to skills use platform paths
- [ ] **Metadata** (.agent only):
  - `description:` matches command purpose?
- [ ] **Content Mirror**: Identical across platforms?
- [ ] **Clarity**:
  - Is the command purpose clear?
  - Are usage examples provided?
  - Are steps well-defined?
- [ ] **Agent Orchestration**: Does it correctly invoke relevant agents?
- [ ] **Skill Loading**: Does it load appropriate skills?

---

### 5. SCRIPTS (Master + Skill-Level)

**Purpose**: Automation scripts that enhance skill capabilities and validate ecosystem

**Location**:
- `.agent/scripts/` (master scripts)
- `.agent/skills/*/scripts/` (skill-level scripts)
- (mirrored in .claude and .cursor)

**Master Scripts** (.agent/scripts/):
- checklist.py
- verify_all.py
- session_manager.py
- auto_preview.py

**Skill-Level Scripts** (examples):
- `vulnerability-scanner/scripts/security_scan.py`
- `testing-patterns/scripts/test_runner.py`
- `seo-fundamentals/scripts/seo_checker.py`
- `ui-ux-pro-max/scripts/design_system.py`
- `sequential-thinking/scripts/process-thought.js`

#### Scripts Review Questions

- [ ] **Purpose Alignment**: Does each script enhance its skill's objective?
- [ ] **Language Choice**: Python or Bash only (avoid complex multi-language setups)?
- [ ] **Self-Containment**: Scripts use relative paths within their skill directory?
- [ ] **Documentation**: Is there a README.md in scripts/ folder?
- [ ] **Modern Standards**:
  - Python: Type hints, async/await, modern libraries?
  - Bash: POSIX-compliant, error handling?
- [ ] **Cross-Platform**: Scripts mirrored across all 3 platforms?
- [ ] **Executable**: Proper shebang and permissions?
- [ ] **Dependencies**: Clear requirements.txt or package.json if needed?

---

## 🔧 Refactoring Guidelines

### Guideline 1: Uniqueness

**Problem**: LLM confused between similar skills/agents
**Solution**:
- Add unique trigger keywords to descriptions
- Ensure no overlap in scope
- Use distinct naming patterns

**Example**:
```yaml
# BAD
name: frontend-expert
description: Frontend development

# GOOD
name: frontend-specialist
description: Senior Frontend Architect who builds maintainable React/Next.js systems with performance-first mindset. Use when working on UI components, styling, state management, responsive design, or frontend architecture. Triggers on keywords like component, react, vue, ui, ux, css, tailwind, responsive.
```

### Guideline 2: Self-Containment

**Problem**: Cross-platform references break when files are used independently
**Solution**:
- Use platform-specific paths in all internal links
- Use relative paths for scripts/references within a skill

**Example**:
```markdown
# BAD (in .agent/agents/frontend-specialist.md)
For design patterns, see .cursor/skills/frontend-design/SKILL.mdc

# GOOD
For design patterns, see .agent/skills/frontend-design/SKILL.md

# BAD (in a skill)
See /workspace/.agent/skills/ui-styling/references/tailwind.md

# GOOD
See ./references/tailwind.md
```

### Guideline 3: Clarity

**Problem**: Verbose, unclear, or ambiguous content
**Solution**:
- Use tables for structured data
- Use clear headings and navigation
- Provide examples
- Avoid jargon without definitions

**Template**:
```markdown
# [Skill Name]

> One-line description of purpose

## When to Use
- Trigger keyword 1
- Trigger keyword 2

## Core Concepts
| Concept | Description |
|---------|-------------|
| X | Y |

## Examples
[Clear, concise examples]

## Quick Reference
[Cheat sheet format]
```

### Guideline 4: Structure Compliance

**Platform-Specific Requirements**:

#### .agent (Antigravity)
- Metadata: `trigger:`, `skills:`, `tools:`, `model:`
- References: `SKILL.md`, `.agent/` paths
- Workflows use `workflows/` folder

#### .claude
- Metadata: `color:`, `tools:` as array
- References: `SKILL.md`, `.claude/` paths
- Commands use `commands/` folder

#### .cursor
- Metadata: `alwaysApply:`, `readonly:`, `is_background:`
- Skills use `SKILL.mdc` extension
- Rules use `.mdc` extension
- References: `.cursor/` paths

### Guideline 5: Modern Guidelines

**2025+ Best Practices to Include**:

**Frontend**:
- React 19+ features (Server Components, Actions)
- Next.js 15+ App Router patterns
- TypeScript 5.5+ satisfies operator
- Core Web Vitals 2025 thresholds
- View Transitions API

**Backend**:
- Edge runtime patterns
- Serverless best practices
- OpenTelemetry observability
- GraphQL Federation v2

**Testing**:
- Vitest over Jest
- Playwright for E2E
- Visual regression testing

**Security**:
- OWASP Top 10 2025
- Supply chain security
- AI/ML security patterns

**DevOps**:
- GitHub Actions modern patterns
- Docker multi-stage builds
- Kubernetes 1.30+ features

### Guideline 6: Content Mirroring

**Process**:
1. Identify the "source of truth" platform (recommend: `.agent`)
2. For each file, extract content (excluding metadata)
3. Apply to other platforms with platform-specific metadata
4. Automate with script:

```python
# mirror_content.py
import re
from pathlib import Path

def extract_content(file_path):
    """Extract content after frontmatter"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split frontmatter from content
    parts = re.split(r'^---\s*$', content, 2, re.MULTILINE)
    if len(parts) >= 3:
        return parts[2].strip()
    return content

def apply_to_platform(content, platform, file_type, metadata):
    """Apply content with platform-specific metadata"""
    frontmatter = "---\n" + metadata + "\n---\n\n"
    return frontmatter + content

# Usage: Mirror skills from .agent to .claude and .cursor
```

### Guideline 7: Purpose Clarity

**For Each File Type, Define**:

**Agents**:
- **Purpose**: Specialist persona for domain X
- **When Activated**: Trigger keywords, request patterns
- **Skills Used**: Which skills it loads
- **Output Style**: How it communicates

**Skills**:
- **Purpose**: Knowledge module for domain X
- **When Loaded**: Which agents use it, what requests trigger it
- **Components**: Scripts, references, data
- **Integration**: How it enhances agent capabilities

**Rules**:
- **Purpose**: Global constraint/guideline for all interactions
- **Priority**: P0 (highest) to P2 (lowest)
- **Scope**: When it applies
- **Precedence**: How it interacts with other rules

**Commands/Workflows**:
- **Purpose**: Orchestrated multi-step procedure
- **Trigger**: Slash command
- **Agents Involved**: Which specialists participate
- **Skills Loaded**: Required knowledge modules
- **Output**: Expected deliverable

---

## 🎯 Systematic Review Process

### Phase 1: Inventory (Week 1)

1. **Count Files**:
   ```bash
   echo "Agents:"
   ls .agent/agents/*.md | wc -l
   ls .claude/agents/*.md | wc -l
   ls .cursor/agents/*.md | wc -l
   
   echo "Skills:"
   ls .agent/skills/*/SKILL.md | wc -l
   ls .claude/skills/*/SKILL.md | wc -l
   ls .cursor/skills/*/SKILL.mdc | wc -l
   
   echo "Rules:"
   ls .agent/rules/*.md | wc -l
   ls .cursor/rules/*.mdc | wc -l
   
   echo "Commands/Workflows:"
   ls .agent/workflows/*.md | wc -l
   ls .claude/commands/*.md | wc -l
   ls .cursor/commands/*.md | wc -l
   ```

2. **Create Inventory Spreadsheet**:
   - Column A: File name
   - Column B: Exists in .agent?
   - Column C: Exists in .claude?
   - Column D: Exists in .cursor?
   - Column E: Content identical?
   - Column F: Metadata correct?
   - Column G: Links self-contained?
   - Column H: Modern best practices?

### Phase 2: Uniqueness Audit (Week 2)

1. **Check for Name Collisions**:
   ```bash
   # Find duplicate skill names
   (ls .agent/skills/*/SKILL.md | xargs grep -h "^name:" | sort | uniq -d) || echo "No duplicates"
   ```

2. **Review Descriptions**:
   - Extract all descriptions
   - Check for overlap
   - Ensure LLM can differentiate

3. **Test Agent Selection**:
   - Create test prompts
   - Verify correct agent activates
   - Refine descriptions if needed

### Phase 3: Self-Containment Audit (Week 3)

1. **Find Cross-Platform References**:
   ```bash
   # In .agent files, find references to .claude or .cursor
   grep -r "\.claude\|\.cursor" .agent/
   
   # In .claude files, find references to .agent or .cursor
   grep -r "\.agent\|\.cursor" .claude/
   
   # In .cursor files, find references to .agent or .claude
   grep -r "\.agent\|\.claude" .cursor/
   ```

2. **Fix Absolute Paths**:
   - Convert to platform-specific paths
   - Use relative paths within skills

3. **Validate Links**:
   - Ensure all referenced files exist
   - Check markdown link syntax

### Phase 4: Content Mirror Verification (Week 4)

1. **Generate Content Hashes**:
   ```python
   import hashlib
   from pathlib import Path
   
   def content_hash(file_path):
       content = extract_content(file_path)  # From earlier script
       return hashlib.md5(content.encode()).hexdigest()
   
   # Compare hashes across platforms
   agent_files = [
       ('.agent/agents/frontend-specialist.md',
        '.claude/agents/frontend-specialist.md',
        '.cursor/agents/frontend-specialist.md')
   ]
   
   for agent_trio in agent_files:
       hashes = [content_hash(f) for f in agent_trio]
       if len(set(hashes)) > 1:
           print(f"MISMATCH: {agent_trio[0]}")
   ```

2. **Identify Discrepancies**:
   - Log all content mismatches
   - Determine source of truth
   - Sync content across platforms

### Phase 5: Metadata Standardization (Week 5)

1. **Validate Metadata Format**:
   ```python
   import yaml
   
   def validate_metadata(file_path, platform):
       with open(file_path, 'r') as f:
           content = f.read()
       
       # Extract frontmatter
       match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
       if not match:
           print(f"No frontmatter: {file_path}")
           return
       
       metadata = yaml.safe_load(match.group(1))
       
       # Platform-specific checks
       if platform == '.agent':
           required = ['name', 'description', 'tools', 'model']
       elif platform == '.claude':
           required = ['name', 'description', 'color']
       elif platform == '.cursor':
           required = ['name', 'description', 'readonly']
       
       for field in required:
           if field not in metadata:
               print(f"Missing {field}: {file_path}")
   ```

2. **Standardize Fields**:
   - Ensure all required fields present
   - Format values consistently
   - Remove deprecated fields

### Phase 6: Modern Best Practices Update (Week 6-8)

1. **Review Each Skill**:
   - Check content against 2025 standards
   - Update deprecated patterns
   - Add new techniques

2. **Enhance with Scripts**:
   - Identify skills that would benefit from automation
   - Create Python/Bash scripts
   - Document in skill's README

3. **Add References**:
   - Create reference documents for complex topics
   - Link from skill main file
   - Organize in `references/` folder

### Phase 7: Final Validation (Week 9)

1. **Run Master Scripts**:
   ```bash
   python .agent/scripts/checklist.py .
   python .agent/scripts/verify_all.py .
   ```

2. **Manual Spot Checks**:
   - Test 10 random skills
   - Test all agents
   - Test all commands

3. **Documentation Update**:
   - Update ARCHITECTURE.md
   - Update README.md
   - Create CHANGELOG.md

---

## 📊 Quality Metrics

Track these metrics before and after refactoring:

| Metric | Target | Current | After |
|--------|--------|---------|-------|
| Files with correct metadata | 100% | ? | ? |
| Content mirroring accuracy | 100% | ? | ? |
| Self-contained links | 100% | ? | ? |
| Skills with modern best practices | 90%+ | ? | ? |
| Skills with enhancement scripts | 30%+ | ? | ? |
| Agent description uniqueness score | 90%+ | ? | ? |
| Broken internal links | 0 | ? | ? |
| Cross-platform references | 0 | ? | ? |
| Files missing required metadata | 0 | ? | ? |

---

## 🚀 Automation Scripts

### 1. Full Ecosystem Audit Script

```python
#!/usr/bin/env python3
"""
ecosystem_audit.py - Comprehensive audit of LLM agent ecosystem
"""

import os
import re
import yaml
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
import json

PLATFORMS = {
    '.agent': {
        'skill_file': 'SKILL.md',
        'rule_ext': '.md',
        'commands_folder': 'workflows',
        'required_metadata': ['name', 'description', 'tools', 'model']
    },
    '.claude': {
        'skill_file': 'SKILL.md',
        'rule_ext': '.md',
        'commands_folder': 'commands',
        'required_metadata': ['name', 'description', 'color']
    },
    '.cursor': {
        'skill_file': 'SKILL.mdc',
        'rule_ext': '.mdc',
        'commands_folder': 'commands',
        'required_metadata': ['name', 'description', 'readonly']
    }
}

class EcosystemAuditor:
    def __init__(self, workspace_path: str = '/workspace'):
        self.workspace = Path(workspace_path)
        self.issues = []
        self.metrics = {}
    
    def extract_frontmatter(self, file_path: Path) -> Tuple[dict, str]:
        """Extract YAML frontmatter and content"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if not match:
            return {}, content
        
        try:
            metadata = yaml.safe_load(match.group(1))
            content_only = match.group(2)
            return metadata or {}, content_only
        except yaml.YAMLError as e:
            self.issues.append(f"YAML error in {file_path}: {e}")
            return {}, content
    
    def content_hash(self, content: str) -> str:
        """Generate hash of content (excluding metadata)"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def audit_agents(self):
        """Audit all agent files"""
        print("\n=== AUDITING AGENTS ===")
        
        agent_names = set()
        for platform in PLATFORMS.keys():
            agents_dir = self.workspace / platform / 'agents'
            if agents_dir.exists():
                for agent_file in agents_dir.glob('*.md'):
                    agent_names.add(agent_file.stem)
        
        print(f"Found {len(agent_names)} unique agent names")
        
        for agent_name in sorted(agent_names):
            self.audit_agent_across_platforms(agent_name)
    
    def audit_agent_across_platforms(self, agent_name: str):
        """Audit a single agent across all platforms"""
        agent_data = {}
        
        for platform, config in PLATFORMS.items():
            agent_file = self.workspace / platform / 'agents' / f'{agent_name}.md'
            
            if not agent_file.exists():
                self.issues.append(f"MISSING: {platform}/agents/{agent_name}.md")
                continue
            
            metadata, content = self.extract_frontmatter(agent_file)
            agent_data[platform] = {
                'metadata': metadata,
                'content': content,
                'hash': self.content_hash(content)
            }
            
            # Check required metadata
            for field in config['required_metadata']:
                if field not in metadata:
                    self.issues.append(
                        f"Missing metadata '{field}' in {platform}/agents/{agent_name}.md"
                    )
        
        # Check content consistency
        if len(agent_data) >= 2:
            hashes = [data['hash'] for data in agent_data.values()]
            if len(set(hashes)) > 1:
                self.issues.append(
                    f"Content mismatch for agent '{agent_name}' across platforms"
                )
    
    def audit_skills(self):
        """Audit all skill files"""
        print("\n=== AUDITING SKILLS ===")
        
        skill_names = set()
        for platform in PLATFORMS.keys():
            skills_dir = self.workspace / platform / 'skills'
            if skills_dir.exists():
                for skill_dir in skills_dir.iterdir():
                    if skill_dir.is_dir():
                        skill_names.add(skill_dir.name)
        
        print(f"Found {len(skill_names)} unique skill names")
        
        for skill_name in sorted(skill_names):
            self.audit_skill_across_platforms(skill_name)
    
    def audit_skill_across_platforms(self, skill_name: str):
        """Audit a single skill across all platforms"""
        skill_data = {}
        
        for platform, config in PLATFORMS.items():
            skill_file = self.workspace / platform / 'skills' / skill_name / config['skill_file']
            
            if not skill_file.exists():
                self.issues.append(
                    f"MISSING: {platform}/skills/{skill_name}/{config['skill_file']}"
                )
                continue
            
            metadata, content = self.extract_frontmatter(skill_file)
            skill_data[platform] = {
                'metadata': metadata,
                'content': content,
                'hash': self.content_hash(content)
            }
            
            # Check for cross-platform references
            other_platforms = [p for p in PLATFORMS.keys() if p != platform]
            for other in other_platforms:
                if other in content:
                    self.issues.append(
                        f"Cross-platform reference to '{other}' in {platform}/skills/{skill_name}/{config['skill_file']}"
                    )
        
        # Check content consistency
        if len(skill_data) >= 2:
            hashes = [data['hash'] for data in skill_data.values()]
            if len(set(hashes)) > 1:
                self.issues.append(
                    f"Content mismatch for skill '{skill_name}' across platforms"
                )
    
    def audit_commands_workflows(self):
        """Audit commands/workflows"""
        print("\n=== AUDITING COMMANDS/WORKFLOWS ===")
        
        for platform, config in PLATFORMS.items():
            cmd_dir = self.workspace / platform / config['commands_folder']
            if cmd_dir.exists():
                cmd_files = list(cmd_dir.glob('*.md'))
                print(f"{platform}: {len(cmd_files)} commands/workflows")
    
    def check_broken_links(self):
        """Check for broken internal links"""
        print("\n=== CHECKING BROKEN LINKS ===")
        
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        
        for platform in PLATFORMS.keys():
            platform_dir = self.workspace / platform
            
            for md_file in platform_dir.rglob('*.md'):
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for match in link_pattern.finditer(content):
                    link_target = match.group(2)
                    
                    # Skip external links
                    if link_target.startswith('http'):
                        continue
                    
                    # Skip anchors
                    if link_target.startswith('#'):
                        continue
                    
                    # Resolve relative path
                    target_path = (md_file.parent / link_target).resolve()
                    
                    if not target_path.exists():
                        self.issues.append(
                            f"Broken link in {md_file.relative_to(self.workspace)}: {link_target}"
                        )
    
    def generate_report(self):
        """Generate audit report"""
        print("\n" + "="*60)
        print("ECOSYSTEM AUDIT REPORT")
        print("="*60)
        
        if not self.issues:
            print("\n✅ No issues found! Ecosystem is healthy.")
        else:
            print(f"\n❌ Found {len(self.issues)} issues:\n")
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue}")
        
        # Save to file
        report_path = self.workspace / 'AUDIT_REPORT.json'
        with open(report_path, 'w') as f:
            json.dump({
                'total_issues': len(self.issues),
                'issues': self.issues,
                'metrics': self.metrics
            }, f, indent=2)
        
        print(f"\n📊 Full report saved to: {report_path}")
    
    def run_full_audit(self):
        """Run complete ecosystem audit"""
        print("Starting full ecosystem audit...")
        
        self.audit_agents()
        self.audit_skills()
        self.audit_commands_workflows()
        self.check_broken_links()
        
        self.generate_report()

if __name__ == '__main__':
    auditor = EcosystemAuditor()
    auditor.run_full_audit()
```

### 2. Content Mirroring Script

```python
#!/usr/bin/env python3
"""
mirror_content.py - Mirror content across platforms while preserving metadata
"""

import re
import yaml
from pathlib import Path
from typing import Tuple

def extract_parts(file_path: Path) -> Tuple[dict, str]:
    """Extract metadata and content separately"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content
    
    metadata = yaml.safe_load(match.group(1)) or {}
    content_only = match.group(2)
    return metadata, content_only

def write_file(file_path: Path, metadata: dict, content: str):
    """Write file with metadata and content"""
    metadata_str = yaml.dump(metadata, default_flow_style=False, sort_keys=False)
    full_content = f"---\n{metadata_str}---\n\n{content}"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

def mirror_skill(skill_name: str, source_platform: str = '.agent'):
    """Mirror a skill from source platform to others"""
    workspace = Path('/workspace')
    
    # Read source
    if source_platform == '.cursor':
        source_file = workspace / source_platform / 'skills' / skill_name / 'SKILL.mdc'
    else:
        source_file = workspace / source_platform / 'skills' / skill_name / 'SKILL.md'
    
    if not source_file.exists():
        print(f"Source file not found: {source_file}")
        return
    
    source_metadata, content = extract_parts(source_file)
    
    # Mirror to .agent
    if source_platform != '.agent':
        target_file = workspace / '.agent' / 'skills' / skill_name / 'SKILL.md'
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Adapt metadata for .agent
        agent_metadata = {
            'name': source_metadata.get('name', skill_name),
            'description': source_metadata.get('description', ''),
            'allowed-tools': source_metadata.get('allowed-tools', 'Read, Write, Edit'),
            'version': source_metadata.get('version', '1.0'),
        }
        
        write_file(target_file, agent_metadata, content)
        print(f"✓ Mirrored to .agent/skills/{skill_name}/SKILL.md")
    
    # Mirror to .claude
    if source_platform != '.claude':
        target_file = workspace / '.claude' / 'skills' / skill_name / 'SKILL.md'
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Adapt metadata for .claude
        claude_metadata = {
            'name': source_metadata.get('name', skill_name),
            'description': source_metadata.get('description', ''),
            'color': 'blue',
        }
        
        write_file(target_file, claude_metadata, content)
        print(f"✓ Mirrored to .claude/skills/{skill_name}/SKILL.md")
    
    # Mirror to .cursor
    if source_platform != '.cursor':
        target_file = workspace / '.cursor' / 'skills' / skill_name / 'SKILL.mdc'
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Adapt metadata for .cursor
        cursor_metadata = {
            'name': source_metadata.get('name', skill_name),
            'description': source_metadata.get('description', ''),
            'readonly': False,
        }
        
        write_file(target_file, cursor_metadata, content)
        print(f"✓ Mirrored to .cursor/skills/{skill_name}/SKILL.mdc")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python mirror_content.py <skill_name> [source_platform]")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    source_platform = sys.argv[2] if len(sys.argv) > 2 else '.agent'
    
    mirror_skill(skill_name, source_platform)
```

---

## 🎓 Training & Rollout

### For LLM Agents

**Update System Prompt**:
```markdown
You are part of a multi-platform LLM ecosystem with:
- 20 specialist agents
- 75 skills (modular knowledge)
- 17 workflows/commands
- 4 global rules

Before any task:
1. Identify the correct agent for the domain
2. Load required skills
3. Apply global rules
4. Execute with platform-specific paths

Platform detection:
- `.agent` → Use `SKILL.md`, reference `.agent/` paths
- `.claude` → Use `SKILL.md`, reference `.claude/` paths  
- `.cursor` → Use `SKILL.mdc`, reference `.cursor/` paths
```

### For Human Operators

**Quick Start Guide**:
1. Know the 20 agents and when to use each
2. Know the top 10 most-used skills
3. Know the 17 commands
4. Understand the 4 global rules

**Regular Maintenance**:
- Monthly: Run ecosystem audit
- Quarterly: Update skills for new best practices
- Yearly: Major refactor and cleanup

---

## 📚 Reference Links

### Platform Documentation

- **Claude**: [Anthropic Platform Docs](https://docs.anthropic.com/)
- **Cursor**: [Cursor Documentation](https://cursor.sh/docs)
- **Windsurf/Gemini**: [Antigravity Kit Documentation](.agent/ARCHITECTURE.md)

### Best Practices Sources

- **React/Next.js**: [Next.js Docs](https://nextjs.org/docs), [Vercel Guidelines](https://vercel.com/docs)
- **TypeScript**: [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- **Testing**: [Vitest](https://vitest.dev/), [Playwright](https://playwright.dev/)
- **Security**: [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- **Accessibility**: [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/)

---

## ✅ Completion Checklist

Before considering the refactoring complete:

- [ ] All agents exist in all 3 platforms
- [ ] All skills exist in all 3 platforms (with correct extensions)
- [ ] All rules exist in all platforms where applicable
- [ ] All commands/workflows exist in all 3 platforms
- [ ] Content is mirrored (identical except metadata)
- [ ] Metadata follows platform-specific format
- [ ] No cross-platform references (all self-contained)
- [ ] No broken internal links
- [ ] All agent descriptions are unique and clear
- [ ] All skill purposes are non-overlapping
- [ ] Modern 2025+ best practices reflected
- [ ] At least 20 skills have enhancement scripts
- [ ] All scripts are documented
- [ ] Ecosystem audit passes with 0 errors
- [ ] ARCHITECTURE.md is updated
- [ ] README.md is updated
- [ ] CHANGELOG.md documents changes

---

## 🏆 Success Criteria

The refactoring is successful when:

1. **LLM agents can confidently choose** the right agent/skill without ambiguity
2. **Each platform operates independently** with no broken references
3. **Content is consistent** across platforms (verified by hash comparison)
4. **Modern best practices** are reflected in all content
5. **Scripts enhance** at least 30% of skills with automation
6. **Documentation is clear** and navigable
7. **Audit script runs clean** with 0 critical issues

---

*This prompt was generated as a comprehensive guide for reviewing and refactoring the LLM agent ecosystem across Claude, Antigravity, and Cursor platforms.*

**Version**: 1.0  
**Last Updated**: 2026-02-09  
**Maintained By**: Ecosystem Steward
