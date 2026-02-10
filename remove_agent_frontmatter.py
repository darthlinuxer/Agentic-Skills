#!/usr/bin/env python3
"""
Remove frontmatter from agent files - make them plain markdown
Per official specs: Agents should have NO frontmatter
"""

import re
from pathlib import Path

def remove_frontmatter(file_path: Path) -> bool:
    """Remove YAML frontmatter from markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has frontmatter
        if not content.startswith('---'):
            print(f"  ℹ️  No frontmatter: {file_path.name}")
            return False
        
        # Extract content after frontmatter
        match = re.match(r'^---\s*\n.*?\n---\s*\n(.*)', content, re.DOTALL)
        if not match:
            print(f"  ⚠️  Malformed frontmatter: {file_path.name}")
            return False
        
        # Get content without frontmatter
        new_content = match.group(1)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ Removed frontmatter: {file_path.name}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path.name}: {e}")
        return False

def main():
    workspace = Path('/workspace')
    platforms = ['.agent', '.claude', '.cursor']
    
    total_modified = 0
    
    for platform in platforms:
        agents_dir = workspace / platform / 'agents'
        
        if not agents_dir.exists():
            print(f"⚠️  {platform}/agents/ not found")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing {platform}/agents/")
        print(f"{'='*60}")
        
        agent_files = sorted(agents_dir.glob('*.md'))
        print(f"Found {len(agent_files)} agent files\n")
        
        for agent_file in agent_files:
            if remove_frontmatter(agent_file):
                total_modified += 1
    
    print(f"\n{'='*60}")
    print(f"✅ COMPLETE: Modified {total_modified} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
