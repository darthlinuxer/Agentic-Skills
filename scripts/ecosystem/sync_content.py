#!/usr/bin/env python3
"""
Sync content across platforms while preserving platform-specific metadata
Source of truth: .agent
Target platforms: .claude, .cursor
"""

import re
import yaml
from pathlib import Path
from typing import Tuple, Optional

PLATFORMS = ('.agent', '.claude', '.cursor')


def extract_parts(file_path: Path) -> Tuple[Optional[dict], str]:
    """Extract metadata and content separately"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"    ❌ Cannot read {file_path}: {e}")
        return None, ""
    
    # Check if file has frontmatter
    if not content.startswith('---'):
        # No frontmatter - entire content is body
        return {}, content
    
    # Split frontmatter from content
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        print(f"    ⚠️  Malformed frontmatter in {file_path.name}")
        return {}, content
    
    try:
        metadata = yaml.safe_load(match.group(1)) or {}
        content_only = match.group(2)
        return metadata, content_only
    except yaml.YAMLError as e:
        print(f"    ❌ YAML error in {file_path.name}: {e}")
        return {}, content


def remap_content_for_platform(content: str, target_platform: str) -> str:
    """Remap platform-specific paths so targets stay domain-isolated."""
    remapped = content

    for platform_name in PLATFORMS:
        remapped = remapped.replace(f'{platform_name}/', f'{target_platform}/')

    # Keep SKILL filename references compatible with target platform.
    if target_platform == '.cursor':
        remapped = re.sub(r'(?<!\w)SKILL\.md(?!\w)', 'SKILL.mdc', remapped)
    else:
        remapped = re.sub(r'(?<!\w)SKILL\.mdc(?!\w)', 'SKILL.md', remapped)

    return remapped


def ensure_platform_isolation(content: str, target_platform: str) -> None:
    """Raise if remapped content still references foreign platform roots."""
    violations = [name for name in PLATFORMS if name != target_platform and f'{name}/' in content]
    if violations:
        joined = ', '.join(violations)
        raise ValueError(f"foreign platform references remain after remap: {joined}")


def write_file(file_path: Path, metadata: dict, content: str) -> bool:
    """Write file with metadata and content"""
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
        print(f"    ❌ Cannot write {file_path}: {e}")
        return False

def sync_agent_content():
    """Sync agent content from .agent to .claude and .cursor"""
    workspace = Path('/workspace')
    
    agent_source = workspace / '.agent' / 'agents'
    claude_target = workspace / '.claude' / 'agents'
    cursor_target = workspace / '.cursor' / 'agents'
    
    if not agent_source.exists():
        print("❌ Source .agent/agents/ not found")
        return 0
    
    print(f"\n{'='*60}")
    print("SYNCING AGENTS")
    print(f"{'='*60}\n")
    
    synced = 0
    agent_files = sorted(agent_source.glob('*.md'))
    
    for source_file in agent_files:
        agent_name = source_file.stem
        
        # Get source content (agents have no frontmatter now)
        _, source_content = extract_parts(source_file)
        
        # Sync to .claude (preserve metadata if any)
        claude_file = claude_target / f'{agent_name}.md'
        if claude_file.exists():
            claude_meta, _ = extract_parts(claude_file)
            try:
                claude_content = remap_content_for_platform(source_content, '.claude')
                ensure_platform_isolation(claude_content, '.claude')
            except ValueError as e:
                print(f"  ❌ {agent_name}.md → .claude ({e})")
                continue
            if write_file(claude_file, claude_meta, claude_content):
                print(f"  ✅ {agent_name}.md → .claude")
                synced += 1
        
        # Sync to .cursor (preserve metadata if any)
        cursor_file = cursor_target / f'{agent_name}.md'
        if cursor_file.exists():
            cursor_meta, _ = extract_parts(cursor_file)
            try:
                cursor_content = remap_content_for_platform(source_content, '.cursor')
                ensure_platform_isolation(cursor_content, '.cursor')
            except ValueError as e:
                print(f"  ❌ {agent_name}.md → .cursor ({e})")
                continue
            if write_file(cursor_file, cursor_meta, cursor_content):
                print(f"  ✅ {agent_name}.md → .cursor")
                synced += 1
    
    return synced

def sync_skill_content():
    """Sync skill content from .agent to .claude and .cursor"""
    workspace = Path('/workspace')
    
    agent_skills = workspace / '.agent' / 'skills'
    claude_skills = workspace / '.claude' / 'skills'
    cursor_skills = workspace / '.cursor' / 'skills'
    
    if not agent_skills.exists():
        print("❌ Source .agent/skills/ not found")
        return 0
    
    print(f"\n{'='*60}")
    print("SYNCING SKILLS")
    print(f"{'='*60}\n")
    
    synced = 0
    skill_dirs = sorted([d for d in agent_skills.iterdir() if d.is_dir() and not d.name.startswith('.')])
    
    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        
        # Get source content
        source_file = skill_dir / 'SKILL.md'
        if not source_file.exists():
            continue
        
        source_meta, source_content = extract_parts(source_file)
        if source_meta is None:
            continue
        
        # Sync to .claude
        claude_file = claude_skills / skill_name / 'SKILL.md'
        if claude_file.exists():
            claude_meta, _ = extract_parts(claude_file)
            if claude_meta is not None:
                try:
                    claude_content = remap_content_for_platform(source_content, '.claude')
                    ensure_platform_isolation(claude_content, '.claude')
                except ValueError as e:
                    print(f"  ❌ {skill_name}/SKILL.md → .claude ({e})")
                    continue
                if write_file(claude_file, claude_meta, claude_content):
                    synced += 1
        
        # Sync to .cursor
        cursor_file = cursor_skills / skill_name / 'SKILL.mdc'
        if cursor_file.exists():
            cursor_meta, _ = extract_parts(cursor_file)
            if cursor_meta is not None:
                try:
                    cursor_content = remap_content_for_platform(source_content, '.cursor')
                    ensure_platform_isolation(cursor_content, '.cursor')
                except ValueError as e:
                    print(f"  ❌ {skill_name}/SKILL.mdc → .cursor ({e})")
                    continue
                if write_file(cursor_file, cursor_meta, cursor_content):
                    synced += 1
    
    return synced

def sync_command_content():
    """Sync workflow/command content from .agent to .claude and .cursor"""
    workspace = Path('/workspace')
    
    agent_workflows = workspace / '.agent' / 'workflows'
    claude_commands = workspace / '.claude' / 'commands'
    cursor_commands = workspace / '.cursor' / 'commands'
    
    if not agent_workflows.exists():
        print("❌ Source .agent/workflows/ not found")
        return 0
    
    print(f"\n{'='*60}")
    print("SYNCING WORKFLOWS/COMMANDS")
    print(f"{'='*60}\n")
    
    synced = 0
    workflow_files = sorted(agent_workflows.glob('*.md'))
    
    for source_file in workflow_files:
        command_name = source_file.stem
        
        # Get source content
        source_meta, source_content = extract_parts(source_file)
        
        # Sync to .claude
        claude_file = claude_commands / f'{command_name}.md'
        if claude_file.exists():
            claude_meta, _ = extract_parts(claude_file)
            try:
                claude_content = remap_content_for_platform(source_content, '.claude')
                ensure_platform_isolation(claude_content, '.claude')
            except ValueError as e:
                print(f"  ❌ {command_name}.md → .claude ({e})")
                continue
            if write_file(claude_file, claude_meta, claude_content):
                print(f"  ✅ {command_name}.md → .claude")
                synced += 1
        
        # Sync to .cursor
        cursor_file = cursor_commands / f'{command_name}.md'
        if cursor_file.exists():
            cursor_meta, _ = extract_parts(cursor_file)
            try:
                cursor_content = remap_content_for_platform(source_content, '.cursor')
                ensure_platform_isolation(cursor_content, '.cursor')
            except ValueError as e:
                print(f"  ❌ {command_name}.md → .cursor ({e})")
                continue
            if write_file(cursor_file, cursor_meta, cursor_content):
                print(f"  ✅ {command_name}.md → .cursor")
                synced += 1
    
    return synced

def main():
    print("\n" + "="*60)
    print("CONTENT SYNCHRONIZATION")
    print("Source of Truth: .agent")
    print("Target Platforms: .claude, .cursor")
    print("="*60)
    
    total_synced = 0
    
    total_synced += sync_agent_content()
    total_synced += sync_skill_content()
    total_synced += sync_command_content()
    
    print(f"\n{'='*60}")
    print(f"✅ COMPLETE: Synced {total_synced} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
