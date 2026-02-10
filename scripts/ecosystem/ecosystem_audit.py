#!/usr/bin/env python3
"""
Comprehensive ecosystem audit for .agent, .claude, and .cursor.

Audit scope is aligned to the 7 refactor criteria:
1) uniqueness (low routing ambiguity)
2) self-contained links and correct references
3) clarity and concision heuristics
4) structure checks by category/platform
5) skill modernization and script-usage checks
6) cross-platform mirror parity
7) purpose-first category-aware validation
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import yaml


@dataclass(frozen=True)
class PlatformConfig:
    name: str
    skill_file: str
    command_folder: str
    command_ext: str
    rules_folder: Optional[str]
    rule_ext: Optional[str]
    required_skill_metadata: Tuple[str, ...]


@dataclass
class Issue:
    severity: str
    category: str
    code: str
    location: str
    message: str
    fix: str


PLATFORMS: Dict[str, PlatformConfig] = {
    ".agent": PlatformConfig(
        name=".agent",
        skill_file="SKILL.md",
        command_folder="workflows",
        command_ext=".md",
        rules_folder="rules",
        rule_ext=".md",
        required_skill_metadata=("description",),
    ),
    ".claude": PlatformConfig(
        name=".claude",
        skill_file="SKILL.md",
        command_folder="commands",
        command_ext=".md",
        rules_folder=None,
        rule_ext=None,
        required_skill_metadata=("name", "description"),
    ),
    ".cursor": PlatformConfig(
        name=".cursor",
        skill_file="SKILL.mdc",
        command_folder="commands",
        command_ext=".md",
        rules_folder="rules",
        rule_ext=".mdc",
        required_skill_metadata=("name", "description"),
    ),
}

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
MARKDOWN_EXTENSIONS = {".md", ".mdc"}
TEXT_EXTENSIONS_FOR_MIRROR = {
    ".md",
    ".mdc",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".csv",
    ".xml",
    ".html",
    ".py",
    ".sh",
    ".js",
    ".ts",
    ".ps1",
    ".puml",
    ".mmd",
}
ALLOWED_SCRIPT_EXTENSIONS = {".py", ".sh", ".js", ".ts", ".ps1"}


class EcosystemAuditor:
    def __init__(self, workspace_path: str):
        self.workspace = Path(workspace_path).resolve()
        self.reports_dir = self.workspace / "docs" / "refactoring" / "reports"
        self.issues: List[Issue] = []
        self.metrics: Counter = Counter()
        self.platform_roots = {name: (self.workspace / name) for name in PLATFORMS}
        self.category_descriptors: Dict[str, Dict[str, str]] = defaultdict(dict)

    def add_issue(
        self,
        severity: str,
        category: str,
        code: str,
        location: Path | str,
        message: str,
        fix: str = "",
    ) -> None:
        issue = Issue(
            severity=severity,
            category=category,
            code=code,
            location=self._rel(location),
            message=message,
            fix=fix,
        )
        self.issues.append(issue)
        self.metrics[f"{severity}_issues"] += 1
        self.metrics[f"{category}_issues"] += 1
        self.metrics[f"code_{code}"] += 1

    def _rel(self, path: Path | str) -> str:
        if isinstance(path, str):
            return path
        try:
            return str(path.relative_to(self.workspace))
        except Exception:
            return str(path)

    def is_within(self, child: Path, parent: Path) -> bool:
        try:
            child.resolve().relative_to(parent.resolve())
            return True
        except Exception:
            return False

    def normalize_text(self, content: str) -> str:
        stripped = content.replace("\r\n", "\n").replace("\r", "\n").strip()
        normalized_lines = []
        for line in stripped.split("\n"):
            if line.strip() == "---":
                continue
            normalized_lines.append(line.rstrip())
        return "\n".join(normalized_lines).strip()

    def normalize_platform_markers(self, content: str) -> str:
        normalized = content
        normalized = re.sub(r"\.agent/", "{platform}/", normalized)
        normalized = re.sub(r"\.claude/", "{platform}/", normalized)
        normalized = re.sub(r"\.cursor/", "{platform}/", normalized)
        normalized = re.sub(r"SKILL\.mdc", "SKILL.core", normalized)
        normalized = re.sub(r"SKILL\.md", "SKILL.core", normalized)
        return normalized

    def normalize_for_mirror(self, content: str) -> str:
        return self.normalize_platform_markers(self.normalize_text(content))

    def is_text_file(self, path: Path) -> bool:
        return path.suffix.lower() in TEXT_EXTENSIONS_FOR_MIRROR

    def register_descriptor(
        self, category: str, name: str, identity: str, platform_name: str
    ) -> None:
        if not identity.strip():
            return

        existing = self.category_descriptors[category]
        if name in existing:
            return

        # Platform iteration is .agent -> .claude -> .cursor, so first write wins.
        existing[name] = identity.strip()

    def parse_frontmatter(self, file_path: Path) -> Tuple[dict, str, bool]:
        try:
            raw = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            self.add_issue(
                "high",
                "io",
                "file_read_error",
                file_path,
                f"Cannot read file: {exc}",
                "Ensure file is readable and not corrupted.",
            )
            return {}, "", False

        if not raw.startswith("---"):
            return {}, raw, False

        match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, re.DOTALL)
        if not match:
            self.add_issue(
                "medium",
                "structure",
                "malformed_frontmatter",
                file_path,
                "Frontmatter is malformed.",
                "Use valid YAML frontmatter delimiters.",
            )
            return {}, raw, False

        frontmatter = match.group(1)
        body = match.group(2)
        try:
            metadata = yaml.safe_load(frontmatter) or {}
            if not isinstance(metadata, dict):
                self.add_issue(
                    "medium",
                    "structure",
                    "frontmatter_not_mapping",
                    file_path,
                    "Frontmatter must be a key/value mapping.",
                    "Convert frontmatter to a YAML mapping object.",
                )
                return {}, body, True
            return metadata, body, True
        except yaml.YAMLError as exc:
            self.add_issue(
                "high",
                "structure",
                "frontmatter_yaml_error",
                file_path,
                f"Frontmatter YAML parsing failed: {exc}",
                "Fix YAML syntax errors in frontmatter.",
            )
            return {}, body, True

    def file_bytes(self, path: Path) -> bytes:
        try:
            return path.read_bytes()
        except Exception as exc:
            self.add_issue(
                "high",
                "io",
                "file_read_error",
                path,
                f"Cannot read file bytes: {exc}",
                "Ensure file can be read for parity checks.",
            )
            return b""

    def has_heading(self, body: str) -> bool:
        return bool(re.search(r"(?m)^\s{0,3}#{1,6}\s+\S", body))

    def first_identity_line(self, body: str) -> str:
        for line in body.splitlines():
            trimmed = line.strip()
            if not trimmed:
                continue
            if trimmed.startswith("#"):
                continue
            if trimmed.startswith(">"):
                continue
            if trimmed.startswith("- ") or trimmed.startswith("* "):
                continue
            return trimmed
        return body.strip().splitlines()[0].strip() if body.strip() else ""

    def extract_identity(self, metadata: dict, body: str) -> str:
        description = metadata.get("description")
        if isinstance(description, str) and description.strip():
            return description.strip()
        return self.first_identity_line(body)

    def detect_clarity_issues(self, body: str, category: str, location: Path) -> None:
        lines = body.splitlines()
        if not lines:
            return

        long_lines = [line for line in lines if len(line) > 220]
        if len(long_lines) > 5:
            self.add_issue(
                "low",
                "clarity",
                "long_lines",
                location,
                f"File has {len(long_lines)} very long lines (>220 chars).",
                "Break long lines to improve readability.",
            )

        if category in {"commands", "rules"} and len(lines) > 280:
            self.add_issue(
                "low",
                "clarity",
                "overly_long_instructions",
                location,
                f"{category} file is very long ({len(lines)} lines).",
                "Trim repetitive text and keep operational steps concise.",
            )

    def check_cross_platform_tokens(self, content: str, current_platform: str, location: Path) -> None:
        other_platforms = [name for name in PLATFORMS if name != current_platform]
        for other in other_platforms:
            if re.search(rf"(?<!\w){re.escape(other)}/", content):
                self.add_issue(
                    "high",
                    "links",
                    "cross_platform_reference",
                    location,
                    f"References {other}/ which breaks self-contained platform boundaries.",
                    f"Replace {other}/ references with local {current_platform}/ equivalents.",
                )

    def clean_link_target(self, link_target: str) -> str:
        target = link_target.strip().strip("<>").strip()
        if " " in target and not target.startswith(("http://", "https://")):
            target = target.split(" ", 1)[0]
        return target

    def check_markdown_links(self) -> None:
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

        for platform_name, platform_root in self.platform_roots.items():
            if not platform_root.exists():
                self.add_issue(
                    "critical",
                    "structure",
                    "missing_platform_directory",
                    platform_root,
                    "Platform directory is missing.",
                    "Restore required platform directory.",
                )
                continue

            for file_path in platform_root.rglob("*"):
                if not file_path.is_file():
                    continue
                if file_path.suffix not in MARKDOWN_EXTENSIONS:
                    continue

                raw = file_path.read_text(encoding="utf-8", errors="ignore")
                self.check_cross_platform_tokens(raw, platform_name, file_path)

                for match in link_pattern.finditer(raw):
                    link_target = self.clean_link_target(match.group(1))
                    if not link_target:
                        continue
                    if link_target.startswith(("http://", "https://", "mailto:", "tel:")):
                        continue
                    if link_target.startswith("#"):
                        continue

                    base_target = link_target.split("#", 1)[0]
                    if not base_target:
                        continue

                    resolved = (file_path.parent / base_target).resolve()
                    if not self.is_within(resolved, platform_root):
                        self.add_issue(
                            "high",
                            "links",
                            "link_outside_platform",
                            file_path,
                            f"Link points outside {platform_name}: {link_target}",
                            "Rewrite link to a file within the same platform directory.",
                        )
                        continue

                    if not resolved.exists():
                        self.add_issue(
                            "medium",
                            "links",
                            "broken_link",
                            file_path,
                            f"Broken internal link: {link_target}",
                            "Fix or remove the broken link target.",
                        )

    def compare_mirrored_bodies(
        self, category: str, name: str, files: Dict[str, Path], parse_frontmatter: bool = True
    ) -> None:
        bodies: Dict[str, str] = {}
        for platform_name, path in files.items():
            if parse_frontmatter:
                _, body, _ = self.parse_frontmatter(path)
            else:
                body = path.read_text(encoding="utf-8", errors="ignore")
            bodies[platform_name] = self.normalize_for_mirror(body)

        if len(set(bodies.values())) > 1:
            joined_locations = ", ".join(f"{platform}:{self._rel(path)}" for platform, path in files.items())
            self.add_issue(
                "high",
                "mirror",
                "content_mismatch",
                joined_locations,
                f"{category} '{name}' body differs across mirrored files.",
                "Sync mirrored file bodies and keep only metadata platform-specific.",
            )

    def audit_agents(self) -> None:
        category = "agents"
        agent_names = set()
        for platform_name in PLATFORMS:
            agents_dir = self.platform_roots[platform_name] / "agents"
            if agents_dir.exists():
                agent_names.update(path.stem for path in agents_dir.glob("*.md"))
        self.metrics["agent_groups"] = len(agent_names)

        for name in sorted(agent_names):
            mirrored_files: Dict[str, Path] = {}
            for platform_name in PLATFORMS:
                file_path = self.platform_roots[platform_name] / "agents" / f"{name}.md"
                if not file_path.exists():
                    self.add_issue(
                        "high",
                        category,
                        "missing_mirror",
                        file_path,
                        f"Missing mirrored agent file for '{name}'.",
                        "Create missing agent mirror with aligned body content.",
                    )
                    continue

                metadata, body, _ = self.parse_frontmatter(file_path)
                mirrored_files[platform_name] = file_path

                if metadata:
                    self.add_issue(
                        "low",
                        category,
                        "unexpected_agent_metadata",
                        file_path,
                        "Agent file contains frontmatter metadata.",
                        "Prefer plain markdown body for mirrored agent instructions.",
                    )

                if not self.has_heading(body):
                    self.add_issue(
                        "medium",
                        "structure",
                        "missing_heading",
                        file_path,
                        "Agent file has no markdown heading.",
                        "Add a clear top-level heading for agent role and scope.",
                    )

                self.detect_clarity_issues(body, category, file_path)
                self.register_descriptor(
                    category, name, self.extract_identity(metadata, body), platform_name
                )

            if len(mirrored_files) >= 2:
                self.compare_mirrored_bodies(category, name, mirrored_files, parse_frontmatter=True)

    def collect_skill_assets(self, skill_dir: Path) -> Dict[str, Path]:
        assets: Dict[str, Path] = {}
        for file_path in skill_dir.rglob("*"):
            if not file_path.is_file():
                continue
            rel = file_path.relative_to(skill_dir)
            if any(part.startswith(".") for part in rel.parts):
                continue
            rel_posix = rel.as_posix()
            if rel_posix.endswith(":Zone.Identifier"):
                continue
            key = "SKILL" if rel_posix in {"SKILL.md", "SKILL.mdc"} else rel_posix
            assets[key] = file_path
        return assets

    def compare_skill_assets(self, skill_name: str, asset_map: Dict[str, Dict[str, Path]]) -> None:
        all_keys = set()
        for assets in asset_map.values():
            all_keys.update(assets.keys())

        for key in sorted(all_keys):
            present_platforms = {platform for platform, assets in asset_map.items() if key in assets}
            missing_platforms = set(PLATFORMS) - present_platforms

            if missing_platforms and present_platforms:
                for missing in sorted(missing_platforms):
                    expected_path = self.platform_roots[missing] / "skills" / skill_name / key
                    if key == "SKILL":
                        expected_path = self.platform_roots[missing] / "skills" / skill_name / PLATFORMS[missing].skill_file
                    self.add_issue(
                        "high",
                        "mirror",
                        "missing_mirror_asset",
                        expected_path,
                        f"Skill '{skill_name}' is missing mirrored asset '{key}'.",
                        "Mirror this asset in all platforms with matching relative path and content.",
                    )

            if len(present_platforms) < 2:
                continue

            present_files = {platform: asset_map[platform][key] for platform in sorted(present_platforms)}
            if key == "SKILL":
                self.compare_mirrored_bodies("skills", f"{skill_name}/SKILL", present_files, parse_frontmatter=True)
                continue

            if all(self.is_text_file(path) for path in present_files.values()):
                normalized_text = {}
                for platform, path in present_files.items():
                    raw = path.read_text(encoding="utf-8", errors="ignore")
                    normalized_text[platform] = self.normalize_for_mirror(raw)
                is_mismatch = len(set(normalized_text.values())) > 1
            else:
                binary_hashes = {}
                for platform, path in present_files.items():
                    binary_hashes[platform] = self.file_bytes(path)
                is_mismatch = len(set(binary_hashes.values())) > 1

            if is_mismatch:
                joined_locations = ", ".join(f"{platform}:{self._rel(path)}" for platform, path in present_files.items())
                self.add_issue(
                    "high",
                    "mirror",
                    "skill_asset_content_mismatch",
                    joined_locations,
                    f"Skill asset mismatch for '{skill_name}/{key}'.",
                    "Keep mirrored skill assets byte-identical across platforms.",
                )

    def audit_skill_script_usage(
        self, skill_name: str, core_bodies: Dict[str, str], asset_map: Dict[str, Dict[str, Path]]
    ) -> None:
        script_keys = sorted({key for assets in asset_map.values() for key in assets if key.startswith("scripts/")})
        if not script_keys:
            return

        for key in script_keys:
            if key.endswith(":Zone.Identifier"):
                continue
            if key.startswith("scripts/tests/") or key.startswith("scripts/templates/"):
                continue
            if key.count("/") != 1:
                continue
            suffix = Path(key).suffix.lower()
            if suffix in {
                "",
                ".md",
                ".txt",
                ".json",
                ".yaml",
                ".yml",
                ".xml",
                ".csv",
                ".html",
                ".puml",
                ".mmd",
                ".pdf",
            }:
                continue
            if suffix and suffix not in ALLOWED_SCRIPT_EXTENSIONS:
                self.add_issue(
                    "medium",
                    "skills",
                    "unsupported_script_extension",
                    f"skills/{skill_name}/{key}",
                    f"Top-level script asset uses uncommon extension '{suffix}'.",
                    "Prefer Python/Bash/JS/TS/PS1 for executable scripts.",
                )

        source_body = core_bodies.get(".agent") or next(iter(core_bodies.values()), "")
        source_body_lc = source_body.lower()
        if "scripts/" not in source_body_lc and "script" not in source_body_lc:
            self.add_issue(
                "low",
                "skills",
                "scripts_not_documented",
                f"skills/{skill_name}/SKILL",
                "Skill includes scripts but SKILL content does not describe when to use them.",
                "Add short guidance for script purpose and invocation conditions.",
            )

    def audit_skills(self) -> None:
        category = "skills"
        skill_names = set()
        for platform_name in PLATFORMS:
            skills_dir = self.platform_roots[platform_name] / "skills"
            if not skills_dir.exists():
                continue
            skill_names.update(
                path.name
                for path in skills_dir.iterdir()
                if path.is_dir() and not path.name.startswith(".")
            )
        self.metrics["skill_groups"] = len(skill_names)

        for skill_name in sorted(skill_names):
            core_bodies: Dict[str, str] = {}
            asset_map: Dict[str, Dict[str, Path]] = {}

            for platform_name, config in PLATFORMS.items():
                skill_dir = self.platform_roots[platform_name] / "skills" / skill_name
                if not skill_dir.exists():
                    self.add_issue(
                        "high",
                        category,
                        "missing_skill_directory",
                        skill_dir,
                        f"Missing skill directory for '{skill_name}'.",
                        "Create mirrored skill directory in all platforms.",
                    )
                    continue

                core_file = skill_dir / config.skill_file
                if not core_file.exists():
                    self.add_issue(
                        "high",
                        category,
                        "missing_skill_core_file",
                        core_file,
                        f"Missing {config.skill_file} for skill '{skill_name}'.",
                        "Add missing skill core file and mirror body content.",
                    )
                    continue

                metadata, body, _ = self.parse_frontmatter(core_file)
                core_bodies[platform_name] = body
                asset_map[platform_name] = self.collect_skill_assets(skill_dir)

                for field in config.required_skill_metadata:
                    if not isinstance(metadata.get(field), str) or not metadata.get(field, "").strip():
                        self.add_issue(
                            "medium",
                            "structure",
                            "missing_required_metadata",
                            core_file,
                            f"Required metadata '{field}' missing for {platform_name}.",
                            "Add required metadata fields per platform skill specification.",
                        )

                if not self.has_heading(body):
                    self.add_issue(
                        "medium",
                        "structure",
                        "missing_heading",
                        core_file,
                        "Skill core file has no markdown heading.",
                        "Add a top-level heading that states objective and scope.",
                    )

                self.detect_clarity_issues(body, category, core_file)
                self.register_descriptor(
                    category, skill_name, self.extract_identity(metadata, body), platform_name
                )

            if asset_map:
                self.compare_skill_assets(skill_name, asset_map)
                self.audit_skill_script_usage(skill_name, core_bodies, asset_map)

    def audit_commands(self) -> None:
        category = "commands"
        command_names = set()
        for platform_name, config in PLATFORMS.items():
            command_dir = self.platform_roots[platform_name] / config.command_folder
            if not command_dir.exists():
                continue
            command_names.update(path.stem for path in command_dir.glob(f"*{config.command_ext}"))
        self.metrics["command_groups"] = len(command_names)

        for name in sorted(command_names):
            mirrored_files: Dict[str, Path] = {}
            for platform_name, config in PLATFORMS.items():
                file_path = self.platform_roots[platform_name] / config.command_folder / f"{name}{config.command_ext}"
                if not file_path.exists():
                    self.add_issue(
                        "high",
                        category,
                        "missing_mirror",
                        file_path,
                        f"Missing mirrored command/workflow file '{name}'.",
                        "Create mirrored command/workflow with aligned body content.",
                    )
                    continue

                metadata, body, _ = self.parse_frontmatter(file_path)
                mirrored_files[platform_name] = file_path

                has_pre_answering = "Before answering:" in body
                if not has_pre_answering and not self.has_heading(body):
                    self.add_issue(
                        "medium",
                        "structure",
                        "weak_command_structure",
                        file_path,
                        "Command/workflow lacks both pre-answer guard and headings.",
                        "Include a clear pre-answer block and/or structured headings.",
                    )

                self.detect_clarity_issues(body, category, file_path)
                self.register_descriptor(
                    category, name, self.extract_identity(metadata, body), platform_name
                )

            if len(mirrored_files) >= 2:
                self.compare_mirrored_bodies(category, name, mirrored_files, parse_frontmatter=True)

    def audit_rules(self) -> None:
        category = "rules"
        rule_names = set()
        agent_rules_dir = self.platform_roots[".agent"] / "rules"
        cursor_rules_dir = self.platform_roots[".cursor"] / "rules"

        if agent_rules_dir.exists():
            rule_names.update(path.stem for path in agent_rules_dir.glob("*.md"))
        if cursor_rules_dir.exists():
            rule_names.update(path.stem for path in cursor_rules_dir.glob("*.mdc"))

        self.metrics["rule_groups"] = len(rule_names)

        for name in sorted(rule_names):
            mirrored_files: Dict[str, Path] = {}

            agent_rule = self.platform_roots[".agent"] / "rules" / f"{name}.md"
            if not agent_rule.exists():
                self.add_issue(
                    "high",
                    category,
                    "missing_mirror",
                    agent_rule,
                    f"Missing .agent rule mirror '{name}.md'.",
                    "Add the rule mirror in .agent/rules.",
                )
            else:
                metadata, body, _ = self.parse_frontmatter(agent_rule)
                mirrored_files[".agent"] = agent_rule
                if not self.has_heading(body):
                    self.add_issue(
                        "medium",
                        "structure",
                        "missing_heading",
                        agent_rule,
                        "Rule file has no markdown heading.",
                        "Add a top-level heading with enforceable rule intent.",
                    )
                self.detect_clarity_issues(body, category, agent_rule)
                self.register_descriptor(
                    category, name, self.extract_identity(metadata, body), ".agent"
                )

            cursor_rule = self.platform_roots[".cursor"] / "rules" / f"{name}.mdc"
            if not cursor_rule.exists():
                self.add_issue(
                    "high",
                    category,
                    "missing_mirror",
                    cursor_rule,
                    f"Missing .cursor rule mirror '{name}.mdc'.",
                    "Add the rule mirror in .cursor/rules.",
                )
            else:
                metadata, body, has_frontmatter = self.parse_frontmatter(cursor_rule)
                mirrored_files[".cursor"] = cursor_rule
                if not has_frontmatter:
                    self.add_issue(
                        "low",
                        "structure",
                        "missing_frontmatter",
                        cursor_rule,
                        "Cursor rule has no frontmatter metadata.",
                        "Add frontmatter with at least alwaysApply where applicable.",
                    )
                elif "alwaysApply" not in metadata:
                    self.add_issue(
                        "low",
                        "structure",
                        "missing_always_apply",
                        cursor_rule,
                        "Cursor rule frontmatter does not include alwaysApply.",
                        "Set alwaysApply to true/false explicitly for rule behavior.",
                    )

                if not self.has_heading(body):
                    self.add_issue(
                        "medium",
                        "structure",
                        "missing_heading",
                        cursor_rule,
                        "Rule file has no markdown heading.",
                        "Add a top-level heading with enforceable rule intent.",
                    )
                self.detect_clarity_issues(body, category, cursor_rule)

            if len(mirrored_files) >= 2:
                self.compare_mirrored_bodies(category, name, mirrored_files, parse_frontmatter=True)

    def audit_uniqueness(self) -> None:
        for category, descriptors in self.category_descriptors.items():
            cleaned_descriptors = [
                (name, re.sub(r"\s+", " ", text.strip().lower()))
                for name, text in descriptors.items()
                if text and text.strip()
            ]

            if len(cleaned_descriptors) < 2:
                continue

            by_text: Dict[str, List[str]] = defaultdict(list)
            for name, text in cleaned_descriptors:
                by_text[text].append(name)

            for text, names in by_text.items():
                if len(names) > 1 and len(text) > 20:
                    self.add_issue(
                        "medium",
                        "uniqueness",
                        "duplicate_identity_text",
                        f"{category}: {', '.join(sorted(set(names)))}",
                        "Multiple files share identical identity/description text.",
                        "Sharpen scope statements so file routing is unambiguous.",
                    )

            seen_pairs = set()
            for i in range(len(cleaned_descriptors)):
                for j in range(i + 1, len(cleaned_descriptors)):
                    name_a, text_a = cleaned_descriptors[i]
                    name_b, text_b = cleaned_descriptors[j]
                    pair = tuple(sorted((name_a, name_b)))
                    if pair in seen_pairs:
                        continue
                    seen_pairs.add(pair)

                    if len(text_a) < 24 or len(text_b) < 24:
                        continue

                    similarity = SequenceMatcher(None, text_a, text_b).ratio()
                    if similarity >= 0.95:
                        self.add_issue(
                            "medium",
                            "uniqueness",
                            "high_semantic_overlap",
                            f"{category}: {name_a} <> {name_b}",
                            f"Identity text overlap is high ({similarity:.2f}).",
                            "Differentiate usage boundaries and non-goals.",
                        )

    def summary(self) -> dict:
        severities = Counter(issue.severity for issue in self.issues)
        categories = Counter(issue.category for issue in self.issues)
        codes = Counter(issue.code for issue in self.issues)

        return {
            "workspace": str(self.workspace),
            "platforms": list(PLATFORMS.keys()),
            "totals": {
                "issues": len(self.issues),
                "critical": severities.get("critical", 0),
                "high": severities.get("high", 0),
                "medium": severities.get("medium", 0),
                "low": severities.get("low", 0),
            },
            "coverage": {
                "agent_groups": self.metrics.get("agent_groups", 0),
                "skill_groups": self.metrics.get("skill_groups", 0),
                "command_groups": self.metrics.get("command_groups", 0),
                "rule_groups": self.metrics.get("rule_groups", 0),
            },
            "category_counts": dict(categories),
            "code_counts": dict(codes),
            "metric_counters": dict(self.metrics),
        }

    def write_reports(self) -> None:
        sorted_issues = sorted(
            self.issues,
            key=lambda issue: (
                SEVERITY_ORDER.get(issue.severity, 99),
                issue.category,
                issue.code,
                issue.location,
            ),
        )

        summary = self.summary()
        json_report = {
            "summary": summary,
            "issues": [asdict(issue) for issue in sorted_issues],
        }

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        json_path = self.reports_dir / "AUDIT_REPORT.json"
        json_path.write_text(json.dumps(json_report, indent=2), encoding="utf-8")

        md_lines = []
        md_lines.append("# Ecosystem Review Report")
        md_lines.append("")
        md_lines.append("## Executive Summary")
        md_lines.append("")
        md_lines.append(f"- Total issues: **{summary['totals']['issues']}**")
        md_lines.append(f"- Critical: **{summary['totals']['critical']}**")
        md_lines.append(f"- High: **{summary['totals']['high']}**")
        md_lines.append(f"- Medium: **{summary['totals']['medium']}**")
        md_lines.append(f"- Low: **{summary['totals']['low']}**")
        md_lines.append("")
        md_lines.append("## Coverage")
        md_lines.append("")
        md_lines.append("| Category | Mirror Groups |")
        md_lines.append("|---|---:|")
        md_lines.append(f"| Agents | {summary['coverage']['agent_groups']} |")
        md_lines.append(f"| Skills | {summary['coverage']['skill_groups']} |")
        md_lines.append(f"| Commands/Workflows | {summary['coverage']['command_groups']} |")
        md_lines.append(f"| Rules | {summary['coverage']['rule_groups']} |")
        md_lines.append("")

        for severity in ("critical", "high", "medium", "low"):
            severity_issues = [issue for issue in sorted_issues if issue.severity == severity]
            md_lines.append(f"## Findings: {severity.title()} ({len(severity_issues)})")
            md_lines.append("")
            if not severity_issues:
                md_lines.append("_No findings._")
                md_lines.append("")
                continue
            for issue in severity_issues:
                md_lines.append(f"- **[{issue.category}/{issue.code}]** `{issue.location}`")
                md_lines.append(f"  - Issue: {issue.message}")
                if issue.fix:
                    md_lines.append(f"  - Fix: {issue.fix}")
            md_lines.append("")

        md_path = self.reports_dir / "ECOSYSTEM_REVIEW_REPORT.md"
        md_path.write_text("\n".join(md_lines).strip() + "\n", encoding="utf-8")

        print("\n" + "=" * 72)
        print("ECOSYSTEM AUDIT COMPLETE")
        print("=" * 72)
        print(f"Workspace: {self.workspace}")
        print(
            "Coverage:"
            f" agents={summary['coverage']['agent_groups']},"
            f" skills={summary['coverage']['skill_groups']},"
            f" commands={summary['coverage']['command_groups']},"
            f" rules={summary['coverage']['rule_groups']}"
        )
        print(
            "Issues:"
            f" critical={summary['totals']['critical']},"
            f" high={summary['totals']['high']},"
            f" medium={summary['totals']['medium']},"
            f" low={summary['totals']['low']}"
        )
        print(f"JSON report: {json_path}")
        print(f"Markdown report: {md_path}")
        print("=" * 72)

    def run(self) -> int:
        self.audit_agents()
        self.audit_skills()
        self.audit_commands()
        self.audit_rules()
        self.check_markdown_links()
        self.audit_uniqueness()
        self.write_reports()

        return 1 if self.metrics.get("critical_issues", 0) > 0 else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit cross-platform agent ecosystem.")
    parser.add_argument(
        "workspace",
        nargs="?",
        default="/workspace",
        help="Workspace path containing .agent/.claude/.cursor directories.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    auditor = EcosystemAuditor(args.workspace)
    return auditor.run()


if __name__ == "__main__":
    raise SystemExit(main())
