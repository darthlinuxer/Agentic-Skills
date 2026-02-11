#!/usr/bin/env python3
"""
Detect dangling skills (skills not referenced by any agent/command/rule) per platform.

For each platform (.cursor, .agent, .claude):
- Discovers all SKILL.md under the platform's skills directory.
- Scans agents, commands, rules (or workflows) for references to skills via path
  patterns: skills/<id>/SKILL.md (with any prefix like ../ or .cursor/).
- Reports dangling skills (no references) and invalid references (path points to
  non-existent skill id).

Usage:
  python skills-dangling-check.py --platform cursor
  python skills-dangling-check.py --platform all
  python skills-dangling-check.py --platform cursor --no-fail
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SKILL_FILENAME = "SKILL.md"
# Matches skills/<id>/SKILL.md with optional path prefix (e.g. ../ or .cursor/)
SKILL_PATH_PATTERN = re.compile(
    r"(?:^|[\s\[\('\"])"  # start or preceded by space/bracket/paren/quote
    r"(?:\.\./)*(?:\.\w+/)*"  # optional ../ and .cursor/ etc.
    r"skills/([a-zA-Z0-9_.-]+)/SKILL\.md",
    re.IGNORECASE,
)

# Frontmatter name: line after --- , capture name: value
NAME_PATTERN = re.compile(r"^name:\s*([^\s#].*)$", re.MULTILINE)

PLATFORM_CONFIG = {
    "cursor": {
        "skills_dir": ".cursor/skills",
        "ref_dirs": [".cursor/agents", ".cursor/commands", ".cursor/rules"],
    },
    "agent": {
        "skills_dir": ".agent/skills",
        "ref_dirs": [".agent/agents", ".agent/workflows"],
    },
    "claude": {
        "skills_dir": ".claude/skills",
        "ref_dirs": [".claude/agents", ".claude/commands"],
    },
}


def repo_root() -> Path:
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent


def extract_skill_name(skill_path: Path) -> str:
    """Extract frontmatter name from SKILL.md; fallback to directory name."""
    try:
        text = skill_path.read_text(encoding="utf-8", errors="replace")
        head = text.split("---", 2)
        if len(head) >= 2:
            m = NAME_PATTERN.search(head[1])
            if m:
                return m.group(1).strip()
    except OSError:
        pass
    return skill_path.parent.name


def discover_skills(root: Path, skills_dir: Path) -> dict[str, dict[str, Any]]:
    """Discover all SKILL.md under skills_dir. Returns skill_id -> {name, path}."""
    skills: dict[str, dict[str, Any]] = {}
    if not skills_dir.is_dir():
        return skills
    for path in skills_dir.rglob(SKILL_FILENAME):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(skills_dir)
        except ValueError:
            continue
        parts = rel.parts
        if len(parts) < 2:
            continue
        skill_id = parts[0]
        if skill_id in skills:
            continue
        name = extract_skill_name(path)
        path_str = path.relative_to(root).as_posix()
        skills[skill_id] = {"name": name, "path": path_str}
    return skills


def iter_referrer_files(root: Path, ref_dirs: list[str]) -> list[Path]:
    """Return all .md and .mdc files under ref_dirs, sorted."""
    seen: set[Path] = set()
    for ref_dir in ref_dirs:
        d = root / ref_dir.replace("/", os_sep())
        if not d.is_dir():
            continue
        for ext in (".md", ".mdc"):
            for p in d.rglob(f"*{ext}"):
                if p.is_file():
                    seen.add(p)
    return sorted(seen)


def os_sep() -> str:
    return "\\" if __import__("sys").platform == "win32" else "/"


def find_skill_refs_in_text(text: str) -> list[str]:
    """Return list of skill ids found in text via skills/<id>/SKILL.md."""
    ids: list[str] = []
    for m in SKILL_PATH_PATTERN.finditer(text):
        ids.append(m.group(1))
    # Also match bare skills/ID/SKILL.md at start of string or after (
    alt = re.compile(r"skills/([a-zA-Z0-9_.-]+)/SKILL\.md", re.IGNORECASE)
    for m in alt.finditer(text):
        ids.append(m.group(1))
    return ids


def run_platform(
    root: Path,
    platform: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Run detection for one platform. Returns report dict."""
    skills_path = root / config["skills_dir"].replace("/", os_sep())
    skills = discover_skills(root, skills_path)
    valid_ids = set(skills.keys())

    references: dict[str, list[dict[str, str]]] = {sid: [] for sid in valid_ids}
    invalid_refs: list[dict[str, str]] = []

    ref_dirs = config["ref_dirs"]
    referrer_paths = list(iter_referrer_files(root, ref_dirs))

    for ref_path in referrer_paths:
        try:
            text = ref_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        ref_path_str = ref_path.relative_to(root).as_posix()
        found_ids = find_skill_refs_in_text(text)
        for sid in found_ids:
            if sid in valid_ids:
                references[sid].append(
                    {"referrerPath": ref_path_str, "patternType": "path"}
                )
            else:
                invalid_refs.append(
                    {"referrerPath": ref_path_str, "rawText": f"skills/{sid}/SKILL.md"}
                )

    dangling = [
        {"id": sid, "name": skills[sid]["name"], "path": skills[sid]["path"]}
        for sid in sorted(skills.keys())
        if not references[sid]
    ]
    referenced = [
        {
            "id": sid,
            "name": skills[sid]["name"],
            "path": skills[sid]["path"],
            "referrers": references[sid],
        }
        for sid in sorted(skills.keys())
        if references[sid]
    ]

    return {
        "platform": platform,
        "totalSkills": len(skills),
        "danglingCount": len(dangling),
        "invalidReferencesCount": len(invalid_refs),
        "dangling": dangling,
        "referenced": referenced,
        "invalidReferences": invalid_refs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect dangling skills and invalid skill references per platform."
    )
    parser.add_argument(
        "--platform",
        choices=["cursor", "agent", "claude", "all"],
        default="all",
        help="Platform(s) to check (default: all).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".reports",
        help="Directory for JSON reports (default: .reports).",
    )
    parser.add_argument(
        "--no-fail",
        action="store_true",
        help="Exit 0 even when dangling skills or invalid refs exist.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print per-skill and per-invalid-ref details.",
    )
    args = parser.parse_args()

    root = repo_root()
    if not root.joinpath(".github").is_dir():
        print("::error::Repo root not found or not a git repo.", file=sys.stderr)
        return 2

    platforms = ["cursor", "agent", "claude"] if args.platform == "all" else [args.platform]
    output_dir = root / args.output_dir.replace("/", os_sep())
    output_dir.mkdir(parents=True, exist_ok=True)

    total_dangling = 0
    total_invalid = 0

    for platform in platforms:
        config = PLATFORM_CONFIG[platform]
        report = run_platform(root, platform, config)
        total_dangling += report["danglingCount"]
        total_invalid += report["invalidReferencesCount"]

        out_file = output_dir / f"dangling-skills-{platform}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"\n--- {platform} ---")
        print(f"Total skills: {report['totalSkills']}")
        print(f"Dangling: {report['danglingCount']}")
        print(f"Invalid references: {report['invalidReferencesCount']}")

        if args.verbose and report["dangling"]:
            for s in report["dangling"]:
                print(f"  Dangling: {s['id']} ({s['path']})")
        if args.verbose and report["invalidReferences"]:
            for inv in report["invalidReferences"]:
                print(f"  Invalid: {inv['referrerPath']} -> {inv['rawText']}")

    if total_dangling > 0 or total_invalid > 0:
        print("\n::error::Dangling skills or invalid references found.")
        if not args.no_fail:
            return 1
    print("\nAll platforms checked. Reports written to", output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
