#!/usr/bin/env python3
"""
Add MCP Context7 and Sequential Thinking references to complex skills
"""

import re
from pathlib import Path
from typing import Optional

# Skill categorization
CONTEXT7_SKILLS = {
    'nextjs-react-expert', 'api-patterns', 'testing-patterns', 'performance-profiling',
    'seo-fundamentals', 'vulnerability-scanner', 'deployment-procedures',
    'nodejs-best-practices', 'python-patterns', 'mcp-builder', 'web-design-guidelines',
    'mobile-design'
}

SEQUENTIAL_THINKING_SKILLS = {
    'architecture', 'systematic-debugging', 'problem-solving', 'game-development',
    'game-design', 'security-auditor', 'red-team-tactics', 'database-design',
    'subagent-driven-development', 'parallel-agents'
}

BOTH_SKILLS = {
    'app-builder', 'frontend-design', 'backend-development', 'performance-optimizer',
    'brainstorming', 'research', 'plan-writing'
}

MCP_CONTEXT7_REF = """
> **💡 MCP Tool Available**: Use **Context7** to search for the latest documentation, best practices, and updates. This ensures you're using current standards and approaches.
"""

MCP_SEQUENTIAL_REF = """
> **🧠 MCP Tool Available**: Use **Sequential Thinking** for complex problem-solving in this domain. Break down decisions, debug chains, or design processes into structured reasoning steps.
"""

MCP_BOTH_REF = """
> **🛠️ MCP Tools Available**: 
> - **Context7**: Search for latest documentation and best practices
> - **Sequential Thinking**: Break down complex problems into structured reasoning steps
"""

def has_mcp_reference(content: str) -> bool:
    """Check if content already has MCP reference"""
    return 'MCP Tool' in content or 'Context7' in content or 'Sequential Thinking' in content

def add_mcp_reference(skill_name: str, file_path: Path) -> bool:
    """Add appropriate MCP reference to skill file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ Cannot read {file_path.name}: {e}")
        return False
    
    # Check if already has reference
    if has_mcp_reference(content):
        return False
    
    # Determine which reference to add
    if skill_name in BOTH_SKILLS:
        mcp_ref = MCP_BOTH_REF
    elif skill_name in CONTEXT7_SKILLS:
        mcp_ref = MCP_CONTEXT7_REF
    elif skill_name in SEQUENTIAL_THINKING_SKILLS:
        mcp_ref = MCP_SEQUENTIAL_REF
    else:
        return False  # Skill not in our list
    
    # Find insertion point (after frontmatter, before or in first major section)
    # Look for patterns like "## Overview", "## When to Use", or first # heading
    
    # Split frontmatter from content
    parts = re.split(r'^---\s*$', content, 2, re.MULTILINE)
    
    if len(parts) >= 3:
        # Has frontmatter
        frontmatter = f"---{parts[1]}---\n"
        body = parts[2]
    else:
        # No frontmatter
        frontmatter = ""
        body = content
    
    # Find first major heading (# or ##)
    lines = body.split('\n')
    insert_index = 0
    
    for i, line in enumerate(lines):
        if line.strip().startswith('# ') or line.strip().startswith('## '):
            # Found first heading, insert after it
            insert_index = i + 1
            # Skip blank lines after heading
            while insert_index < len(lines) and lines[insert_index].strip() == '':
                insert_index += 1
            break
    
    # Insert MCP reference
    lines.insert(insert_index, mcp_ref.strip())
    lines.insert(insert_index + 1, '')  # Add blank line after
    
    # Reconstruct content
    new_content = frontmatter + '\n'.join(lines)
    
    # Write back
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"  ❌ Cannot write {file_path.name}: {e}")
        return False

def main():
    workspace = Path('/workspace')
    platforms = {
        '.agent': 'SKILL.md',
        '.claude': 'SKILL.md',
        '.cursor': 'SKILL.mdc'
    }
    
    all_target_skills = CONTEXT7_SKILLS | SEQUENTIAL_THINKING_SKILLS | BOTH_SKILLS
    
    total_modified = 0
    total_skipped = 0
    
    for platform, skill_file_name in platforms.items():
        skills_dir = workspace / platform / 'skills'
        
        if not skills_dir.exists():
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing {platform}/skills/")
        print(f"{'='*60}\n")
        
        for skill_name in sorted(all_target_skills):
            skill_file = skills_dir / skill_name / skill_file_name
            
            if not skill_file.exists():
                continue
            
            if add_mcp_reference(skill_name, skill_file):
                category = (
                    "Both" if skill_name in BOTH_SKILLS
                    else "Context7" if skill_name in CONTEXT7_SKILLS
                    else "Sequential"
                )
                print(f"  ✅ {skill_name}: Added {category}")
                total_modified += 1
            else:
                if has_mcp_reference(skill_file.read_text()):
                    total_skipped += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Added MCP references: {total_modified}")
    print(f"ℹ️  Skipped (already present): {total_skipped}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
