#!/usr/bin/env python3
"""
Fix cross-platform references - make files self-contained
Replace .agent/, .claude/, .cursor/ references with platform-specific paths
"""

import re
from pathlib import Path

def fix_file_references(file_path: Path, current_platform: str) -> bool:
    """Fix cross-platform references in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ Cannot read {file_path}: {e}")
        return False
    
    original_content = content
    other_platforms = [p for p in ['.agent', '.claude', '.cursor'] if p != current_platform]
    
    # Replace cross-platform references with current platform
    for other_platform in other_platforms:
        # Replace platform directory references
        content = content.replace(f'{other_platform}/', f'{current_platform}/')
    
    # Special case: For .cursor, also update SKILL.md to SKILL.mdc
    if current_platform == '.cursor':
        content = re.sub(r'/SKILL\.md(?!\w)', '/SKILL.mdc', content)
    
    # Check if anything changed
    if content == original_content:
        return False
    
    # Write back
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  ❌ Cannot write {file_path}: {e}")
        return False

def main():
    workspace = Path('/workspace')
    
    # Files to check (from audit findings)
    files_to_check = [
        # Agents
        ('.claude', 'agents/project-planner.md'),
        ('.cursor', 'agents/project-planner.md'),
        
        # Rules
        ('.cursor', 'rules/gemini.mdc'),
        
        # Skills
        ('.agent', 'skills/create-rule/SKILL.md'),
        ('.agent', 'skills/create-skill/SKILL.md'),
        ('.agent', 'skills/create-subagent/SKILL.md'),
        ('.agent', 'skills/migrate-to-skills/SKILL.md'),
        ('.agent', 'skills/plan-writing/SKILL.md'),
        ('.claude', 'skills/create-rule/SKILL.md'),
        ('.claude', 'skills/create-skill/SKILL.md'),
        ('.claude', 'skills/create-subagent/SKILL.md'),
        ('.claude', 'skills/migrate-to-skills/SKILL.md'),
        ('.claude', 'skills/plan-writing/SKILL.md'),
    ]
    
    print("\n" + "="*60)
    print("FIXING CROSS-PLATFORM REFERENCES")
    print("="*60 + "\n")
    
    total_fixed = 0
    
    for platform, relative_path in files_to_check:
        file_path = workspace / platform / relative_path
        
        if not file_path.exists():
            print(f"  ⚠️  Not found: {platform}/{relative_path}")
            continue
        
        if fix_file_references(file_path, platform):
            print(f"  ✅ Fixed: {platform}/{relative_path}")
            total_fixed += 1
        else:
            print(f"  ℹ️  No changes: {platform}/{relative_path}")
    
    print(f"\n{'='*60}")
    print(f"✅ Fixed {total_fixed} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
