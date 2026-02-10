#!/usr/bin/env python3
"""
ecosystem_audit.py - Comprehensive audit of LLM agent ecosystem

Audits agents, skills, rules, and commands/workflows across .agent, .claude, and .cursor platforms.
Checks for:
- File existence across platforms
- Content consistency (mirroring)
- Metadata correctness
- Cross-platform references (should be self-contained)
- Broken internal links
"""

import os
import re
import yaml
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

PLATFORMS = {
    '.agent': {
        'skill_file': 'SKILL.md',
        'rule_ext': '.md',
        'commands_folder': 'workflows',
        'required_agent_metadata': [],  # Agents should have NO metadata (plain markdown)
        'required_skill_metadata': ['description'],  # Only description required (name optional)
        'required_rule_metadata': []  # Rules should have NO metadata (activation via UI)
    },
    '.claude': {
        'skill_file': 'SKILL.md',
        'rule_ext': '.md',
        'commands_folder': 'commands',
        'required_agent_metadata': [],  # Agents should have NO metadata (plain markdown)
        'required_skill_metadata': ['name', 'description'],  # name and description required
        'required_rule_metadata': []  # Rules should have NO metadata
    },
    '.cursor': {
        'skill_file': 'SKILL.mdc',
        'rule_ext': '.mdc',
        'commands_folder': 'commands',
        'required_agent_metadata': [],  # Agents should have NO metadata (plain markdown)
        'required_skill_metadata': ['name', 'description'],  # name and description required
        'required_rule_metadata': []  # Rules metadata is optional (alwaysApply, globs, description)
    }
}

class EcosystemAuditor:
    def __init__(self, workspace_path: str = '/workspace'):
        self.workspace = Path(workspace_path)
        self.issues = []
        self.warnings = []
        self.info = []
        self.metrics = defaultdict(int)
        
    def log_issue(self, message: str, severity: str = 'error'):
        """Log an issue"""
        if severity == 'error':
            self.issues.append(message)
        elif severity == 'warning':
            self.warnings.append(message)
        else:
            self.info.append(message)
    
    def extract_frontmatter(self, file_path: Path) -> Tuple[Optional[dict], str]:
        """Extract YAML frontmatter and content"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            self.log_issue(f"Cannot read {file_path}: {e}")
            return None, ""
        
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if not match:
            self.log_issue(f"No frontmatter in {file_path}", 'warning')
            return {}, content
        
        try:
            metadata = yaml.safe_load(match.group(1))
            content_only = match.group(2).strip()
            return metadata or {}, content_only
        except yaml.YAMLError as e:
            self.log_issue(f"YAML error in {file_path}: {e}")
            return {}, content
    
    def content_hash(self, content: str) -> str:
        """Generate hash of content (excluding metadata)"""
        # Normalize whitespace for comparison
        normalized = re.sub(r'\s+', ' ', content.strip())
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def audit_agents(self):
        """Audit all agent files"""
        print("\n" + "="*60)
        print("AUDITING AGENTS")
        print("="*60)
        
        # Collect all unique agent names
        agent_names = set()
        for platform in PLATFORMS.keys():
            agents_dir = self.workspace / platform / 'agents'
            if agents_dir.exists():
                for agent_file in agents_dir.glob('*.md'):
                    agent_names.add(agent_file.stem)
        
        print(f"Found {len(agent_names)} unique agent names across platforms")
        self.metrics['total_agents'] = len(agent_names)
        
        for agent_name in sorted(agent_names):
            self.audit_agent_across_platforms(agent_name)
    
    def audit_agent_across_platforms(self, agent_name: str):
        """Audit a single agent across all platforms"""
        agent_data = {}
        
        for platform, config in PLATFORMS.items():
            agent_file = self.workspace / platform / 'agents' / f'{agent_name}.md'
            
            if not agent_file.exists():
                self.log_issue(f"MISSING: {platform}/agents/{agent_name}.md")
                self.metrics['missing_agents'] += 1
                continue
            
            metadata, content = self.extract_frontmatter(agent_file)
            
            if metadata is None:
                continue
            
            agent_data[platform] = {
                'metadata': metadata,
                'content': content,
                'hash': self.content_hash(content),
                'file': agent_file
            }
            
            # Check required metadata
            for field in config['required_agent_metadata']:
                if field not in metadata:
                    self.log_issue(
                        f"Missing metadata '{field}' in {platform}/agents/{agent_name}.md"
                    )
                    self.metrics['metadata_issues'] += 1
            
            # Check for cross-platform references
            other_platforms = [p for p in PLATFORMS.keys() if p != platform]
            for other in other_platforms:
                if other in content and f"{other}/" in content:
                    self.log_issue(
                        f"Cross-platform reference to '{other}' in {platform}/agents/{agent_name}.md",
                        'warning'
                    )
                    self.metrics['cross_platform_refs'] += 1
        
        # Check content consistency across platforms
        if len(agent_data) >= 2:
            hashes = [data['hash'] for data in agent_data.values()]
            if len(set(hashes)) > 1:
                self.log_issue(
                    f"Content mismatch for agent '{agent_name}' across platforms",
                    'warning'
                )
                self.metrics['content_mismatches'] += 1
    
    def audit_skills(self):
        """Audit all skill files"""
        print("\n" + "="*60)
        print("AUDITING SKILLS")
        print("="*60)
        
        # Collect all unique skill names
        skill_names = set()
        for platform in PLATFORMS.keys():
            skills_dir = self.workspace / platform / 'skills'
            if skills_dir.exists():
                for skill_dir in skills_dir.iterdir():
                    if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                        skill_names.add(skill_dir.name)
        
        print(f"Found {len(skill_names)} unique skill names across platforms")
        self.metrics['total_skills'] = len(skill_names)
        
        skills_with_scripts = 0
        skills_with_references = 0
        
        for skill_name in sorted(skill_names):
            has_scripts, has_refs = self.audit_skill_across_platforms(skill_name)
            if has_scripts:
                skills_with_scripts += 1
            if has_refs:
                skills_with_references += 1
        
        self.metrics['skills_with_scripts'] = skills_with_scripts
        self.metrics['skills_with_references'] = skills_with_references
        
        print(f"  - Skills with scripts: {skills_with_scripts}")
        print(f"  - Skills with references: {skills_with_references}")
    
    def audit_skill_across_platforms(self, skill_name: str) -> Tuple[bool, bool]:
        """Audit a single skill across all platforms. Returns (has_scripts, has_references)"""
        skill_data = {}
        has_scripts = False
        has_references = False
        
        for platform, config in PLATFORMS.items():
            skill_file = self.workspace / platform / 'skills' / skill_name / config['skill_file']
            
            if not skill_file.exists():
                self.log_issue(
                    f"MISSING: {platform}/skills/{skill_name}/{config['skill_file']}"
                )
                self.metrics['missing_skills'] += 1
                continue
            
            metadata, content = self.extract_frontmatter(skill_file)
            
            if metadata is None:
                continue
            
            skill_data[platform] = {
                'metadata': metadata,
                'content': content,
                'hash': self.content_hash(content),
                'file': skill_file
            }
            
            # Check required metadata
            for field in config['required_skill_metadata']:
                if field not in metadata:
                    self.log_issue(
                        f"Missing metadata '{field}' in {platform}/skills/{skill_name}/{config['skill_file']}",
                        'warning'
                    )
                    self.metrics['metadata_issues'] += 1
            
            # Check for scripts and references
            scripts_dir = skill_file.parent / 'scripts'
            references_dir = skill_file.parent / 'references'
            
            if scripts_dir.exists() and any(scripts_dir.iterdir()):
                has_scripts = True
            
            if references_dir.exists() and any(references_dir.iterdir()):
                has_references = True
            
            # Check for cross-platform references
            other_platforms = [p for p in PLATFORMS.keys() if p != platform]
            for other in other_platforms:
                if other in content and f"{other}/" in content:
                    self.log_issue(
                        f"Cross-platform reference to '{other}' in {platform}/skills/{skill_name}/{config['skill_file']}",
                        'warning'
                    )
                    self.metrics['cross_platform_refs'] += 1
        
        # Check content consistency across platforms
        if len(skill_data) >= 2:
            hashes = [data['hash'] for data in skill_data.values()]
            if len(set(hashes)) > 1:
                self.log_issue(
                    f"Content mismatch for skill '{skill_name}' across platforms",
                    'warning'
                )
                self.metrics['content_mismatches'] += 1
        
        return has_scripts, has_references
    
    def audit_rules(self):
        """Audit rules files"""
        print("\n" + "="*60)
        print("AUDITING RULES")
        print("="*60)
        
        # Collect rule names from .agent
        agent_rules_dir = self.workspace / '.agent' / 'rules'
        cursor_rules_dir = self.workspace / '.cursor' / 'rules'
        
        rule_names = set()
        
        if agent_rules_dir.exists():
            for rule_file in agent_rules_dir.glob('*.md'):
                rule_names.add(rule_file.stem)
        
        if cursor_rules_dir.exists():
            for rule_file in cursor_rules_dir.glob('*.mdc'):
                rule_names.add(rule_file.stem)
        
        print(f"Found {len(rule_names)} unique rule names")
        self.metrics['total_rules'] = len(rule_names)
        
        for rule_name in sorted(rule_names):
            self.audit_rule_across_platforms(rule_name)
    
    def audit_rule_across_platforms(self, rule_name: str):
        """Audit a single rule across platforms"""
        # .agent
        agent_rule = self.workspace / '.agent' / 'rules' / f'{rule_name}.md'
        if agent_rule.exists():
            metadata, content = self.extract_frontmatter(agent_rule)
            if metadata is not None:
                if 'trigger' not in metadata:
                    self.log_issue(f"Missing 'trigger' in .agent/rules/{rule_name}.md", 'warning')
        else:
            self.log_issue(f"MISSING: .agent/rules/{rule_name}.md", 'warning')
        
        # .cursor
        cursor_rule = self.workspace / '.cursor' / 'rules' / f'{rule_name}.mdc'
        if cursor_rule.exists():
            metadata, content = self.extract_frontmatter(cursor_rule)
            if metadata is not None:
                if 'alwaysApply' not in metadata:
                    self.log_issue(f"Missing 'alwaysApply' in .cursor/rules/{rule_name}.mdc", 'warning')
                
                # Check for incorrect SKILL.mdccc reference (should be SKILL.mdc)
                if 'SKILL.mdccc' in content:
                    self.log_issue(
                        f"Incorrect reference 'SKILL.mdccc' in .cursor/rules/{rule_name}.mdc (should be 'SKILL.mdc')"
                    )
                    self.metrics['incorrect_references'] += 1
        else:
            self.log_issue(f"MISSING: .cursor/rules/{rule_name}.mdc", 'warning')
    
    def audit_commands_workflows(self):
        """Audit commands/workflows"""
        print("\n" + "="*60)
        print("AUDITING COMMANDS/WORKFLOWS")
        print("="*60)
        
        # Collect command names
        command_names = set()
        
        for platform, config in PLATFORMS.items():
            cmd_dir = self.workspace / platform / config['commands_folder']
            if cmd_dir.exists():
                for cmd_file in cmd_dir.glob('*.md'):
                    command_names.add(cmd_file.stem)
        
        print(f"Found {len(command_names)} unique command/workflow names")
        self.metrics['total_commands'] = len(command_names)
        
        for command_name in sorted(command_names):
            self.audit_command_across_platforms(command_name)
    
    def audit_command_across_platforms(self, command_name: str):
        """Audit a single command across platforms"""
        command_data = {}
        
        for platform, config in PLATFORMS.items():
            cmd_file = self.workspace / platform / config['commands_folder'] / f'{command_name}.md'
            
            if not cmd_file.exists():
                self.log_issue(
                    f"MISSING: {platform}/{config['commands_folder']}/{command_name}.md",
                    'warning'
                )
                self.metrics['missing_commands'] += 1
                continue
            
            metadata, content = self.extract_frontmatter(cmd_file)
            
            if metadata is None:
                continue
            
            command_data[platform] = {
                'metadata': metadata,
                'content': content,
                'hash': self.content_hash(content)
            }
        
        # Check content consistency
        if len(command_data) >= 2:
            hashes = [data['hash'] for data in command_data.values()]
            if len(set(hashes)) > 1:
                self.log_issue(
                    f"Content mismatch for command '{command_name}' across platforms",
                    'warning'
                )
                self.metrics['content_mismatches'] += 1
    
    def check_broken_links(self):
        """Check for broken internal links (basic implementation)"""
        print("\n" + "="*60)
        print("CHECKING BROKEN LINKS")
        print("="*60)
        
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        broken_links_found = 0
        
        for platform in PLATFORMS.keys():
            platform_dir = self.workspace / platform
            
            if not platform_dir.exists():
                continue
            
            for md_file in platform_dir.rglob('*.md'):
                try:
                    with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except:
                    continue
                
                for match in link_pattern.finditer(content):
                    link_target = match.group(2)
                    
                    # Skip external links
                    if link_target.startswith('http'):
                        continue
                    
                    # Skip mailto
                    if link_target.startswith('mailto:'):
                        continue
                    
                    # Skip anchors only
                    if link_target.startswith('#'):
                        continue
                    
                    # Handle links with anchors
                    if '#' in link_target:
                        link_target = link_target.split('#')[0]
                        if not link_target:  # Was anchor-only
                            continue
                    
                    # Resolve relative path
                    try:
                        target_path = (md_file.parent / link_target).resolve()
                        
                        if not target_path.exists():
                            self.log_issue(
                                f"Broken link in {md_file.relative_to(self.workspace)}: {link_target}",
                                'warning'
                            )
                            broken_links_found += 1
                    except:
                        pass
        
        self.metrics['broken_links'] = broken_links_found
        print(f"  - Broken links found: {broken_links_found}")
    
    def generate_report(self):
        """Generate audit report"""
        print("\n" + "="*60)
        print("ECOSYSTEM AUDIT REPORT")
        print("="*60)
        
        # Summary
        print(f"\n📊 SUMMARY")
        print(f"  Total Agents: {self.metrics.get('total_agents', 0)}")
        print(f"  Total Skills: {self.metrics.get('total_skills', 0)}")
        print(f"  Total Rules: {self.metrics.get('total_rules', 0)}")
        print(f"  Total Commands/Workflows: {self.metrics.get('total_commands', 0)}")
        print(f"  Skills with scripts: {self.metrics.get('skills_with_scripts', 0)}")
        print(f"  Skills with references: {self.metrics.get('skills_with_references', 0)}")
        
        # Issues
        print(f"\n🔴 ERRORS: {len(self.issues)}")
        if self.issues:
            for i, issue in enumerate(self.issues[:20], 1):  # Show first 20
                print(f"  {i}. {issue}")
            if len(self.issues) > 20:
                print(f"  ... and {len(self.issues) - 20} more")
        
        print(f"\n⚠️  WARNINGS: {len(self.warnings)}")
        if self.warnings:
            for i, warning in enumerate(self.warnings[:20], 1):  # Show first 20
                print(f"  {i}. {warning}")
            if len(self.warnings) > 20:
                print(f"  ... and {len(self.warnings) - 20} more")
        
        # Metrics
        print(f"\n📈 KEY METRICS")
        print(f"  Missing agents: {self.metrics.get('missing_agents', 0)}")
        print(f"  Missing skills: {self.metrics.get('missing_skills', 0)}")
        print(f"  Missing commands: {self.metrics.get('missing_commands', 0)}")
        print(f"  Content mismatches: {self.metrics.get('content_mismatches', 0)}")
        print(f"  Cross-platform references: {self.metrics.get('cross_platform_refs', 0)}")
        print(f"  Metadata issues: {self.metrics.get('metadata_issues', 0)}")
        print(f"  Incorrect references: {self.metrics.get('incorrect_references', 0)}")
        print(f"  Broken links: {self.metrics.get('broken_links', 0)}")
        
        # Overall health
        total_issues = len(self.issues) + len(self.warnings)
        print(f"\n{'='*60}")
        if total_issues == 0:
            print("✅ ECOSYSTEM HEALTH: EXCELLENT - No issues found!")
        elif len(self.issues) == 0 and len(self.warnings) <= 10:
            print("✅ ECOSYSTEM HEALTH: GOOD - Only minor warnings")
        elif len(self.issues) <= 5:
            print("⚠️  ECOSYSTEM HEALTH: FAIR - Some issues need attention")
        else:
            print("🔴 ECOSYSTEM HEALTH: NEEDS WORK - Multiple issues found")
        print(f"{'='*60}")
        
        # Save to file
        report_data = {
            'summary': {
                'total_agents': self.metrics.get('total_agents', 0),
                'total_skills': self.metrics.get('total_skills', 0),
                'total_rules': self.metrics.get('total_rules', 0),
                'total_commands': self.metrics.get('total_commands', 0),
                'skills_with_scripts': self.metrics.get('skills_with_scripts', 0),
                'skills_with_references': self.metrics.get('skills_with_references', 0),
            },
            'issues': {
                'errors': self.issues,
                'warnings': self.warnings,
                'info': self.info
            },
            'metrics': dict(self.metrics)
        }
        
        report_path = self.workspace / 'AUDIT_REPORT.json'
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Full report saved to: {report_path}")
    
    def run_full_audit(self):
        """Run complete ecosystem audit"""
        print("\n" + "="*60)
        print("LLM AGENT ECOSYSTEM AUDIT")
        print("="*60)
        print(f"Workspace: {self.workspace}")
        
        self.audit_agents()
        self.audit_skills()
        self.audit_rules()
        self.audit_commands_workflows()
        self.check_broken_links()
        
        self.generate_report()

if __name__ == '__main__':
    import sys
    
    workspace = sys.argv[1] if len(sys.argv) > 1 else '/workspace'
    
    auditor = EcosystemAuditor(workspace)
    auditor.run_full_audit()
