#!/usr/bin/env python3
"""
Simplify skills metadata to match official specs:
- Antigravity (.agent): description only
- Claude (.claude): name, description (optional: license)
- Cursor (.cursor): name, description (optional: license)
"""

import re
import yaml
from pathlib import Path
from typing import Optional, Dict

def extract_metadata_and_content(file_path: Path) -> tuple[Optional[dict], str]:
    """Extract YAML frontmatter and content"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"    ❌ Cannot read {file_path.name}: {e}")
        return None, ""
    
    if not content.startswith('---'):
        print(f"    ℹ️  No frontmatter: {file_path.name}")
        return {}, content
    
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        print(f"    ⚠️  Malformed frontmatter: {file_path.name}")
        return None, content
    
    try:
        metadata = yaml.safe_load(match.group(1)) or {}
        content_only = match.group(2)
        return metadata, content_only
    except yaml.YAMLError as e:
        print(f"    ❌ YAML error in {file_path.name}: {e}")
        return None, content

def simplify_metadata(metadata: dict, platform: str) -> dict:
    """Keep only required and optional valid fields per platform"""
    if platform == '.agent':
        # Antigravity: description only (name optional, defaults to folder)
        new_meta = {}
        if 'description' in metadata:
            new_meta['description'] = metadata['description']
        # Optionally keep name if explicitly set
        if 'name' in metadata:
            new_meta['name'] = metadata['name']
        return new_meta
    
    elif platform in ['.claude', '.cursor']:
        # Claude/Cursor: name, description (optional: license)
        new_meta = {}
        if 'name' in metadata:
            new_meta['name'] = metadata['name']
        if 'description' in metadata:
            new_meta['description'] = metadata['description']
        # Keep license if present (it's valid optional field)
        if 'license' in metadata:
            new_meta['license'] = metadata['license']
        return new_meta
    
    return metadata

def write_skill_file(file_path: Path, metadata: dict, content: str) -> bool:
    """Write skill file with simplified metadata"""
    try:
        if metadata:
            # Write with frontmatter
            metadata_str = yaml.dump(metadata, default_flow_style=False, sort_keys=False, allow_unicode=True)
            full_content = f"---\n{metadata_str}---\n\n{content}"
        else:
            # No metadata - plain markdown
            full_content = content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return True
    except Exception as e:
        print(f"    ❌ Error writing {file_path.name}: {e}")
        return False

def process_skill(skill_dir: Path, platform: str) -> tuple[bool, str]:
    """Process a single skill directory"""
    # Determine skill file name
    if platform == '.cursor':
        skill_file = skill_dir / 'SKILL.mdc'
    else:
        skill_file = skill_dir / 'SKILL.md'
    
    if not skill_file.exists():
        return False, f"missing {skill_file.name}"
    
    # Extract current metadata and content
    metadata, content = extract_metadata_and_content(skill_file)
    
    if metadata is None:
        return False, "YAML error"
    
    # Check if already simplified
    if platform == '.agent':
        required = {'description'}
        optional = {'name', 'license'}
    else:  # .claude or .cursor
        required = {'name', 'description'}
        optional = {'license'}
    
    current_keys = set(metadata.keys())
    expected_keys = required | optional
    
    if current_keys <= expected_keys:
        return False, "already clean"
    
    # Simplify metadata
    old_meta = metadata.copy()
    new_meta = simplify_metadata(metadata, platform)
    
    # Write back
    if write_skill_file(skill_file, new_meta, content):
        removed = set(old_meta.keys()) - set(new_meta.keys())
        return True, f"removed: {', '.join(sorted(removed))}"
    else:
        return False, "write error"

def main():
    workspace = Path('/workspace')
    platforms = ['.agent', '.claude', '.cursor']
    
    total_modified = 0
    total_skipped = 0
    total_errors = 0
    
    for platform in platforms:
        skills_dir = workspace / platform / 'skills'
        
        if not skills_dir.exists():
            print(f"⚠️  {platform}/skills/ not found")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing {platform}/skills/")
        print(f"{'='*60}")
        
        skill_dirs = sorted([d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')])
        print(f"Found {len(skill_dirs)} skills\n")
        
        for skill_dir in skill_dirs:
            modified, msg = process_skill(skill_dir, platform)
            
            if modified:
                print(f"  ✅ {skill_dir.name}: {msg}")
                total_modified += 1
            elif "error" in msg.lower():
                print(f"  ❌ {skill_dir.name}: {msg}")
                total_errors += 1
            else:
                # Silently skip if already clean
                total_skipped += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Modified: {total_modified}")
    print(f"ℹ️  Skipped (already clean): {total_skipped}")
    print(f"❌ Errors: {total_errors}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
