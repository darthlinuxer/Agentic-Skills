#!/usr/bin/env python3
"""Enforce strict platform isolation across .agent, .claude, and .cursor."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

PLATFORMS = (".agent", ".claude", ".cursor")
TEXT_EXTENSIONS = {
    ".md",
    ".mdc",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".sh",
    ".js",
    ".ts",
    ".toml",
}


@dataclass(frozen=True)
class IsolationIssue:
    severity: str
    code: str
    location: str
    message: str
    fix: str


class IsolationLinter:
    """Checks each platform directory for cross-domain reference leaks."""

    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()
        self.issues: List[IsolationIssue] = []

    def add_issue(self, code: str, path: Path | str, message: str, fix: str) -> None:
        if isinstance(path, Path):
            try:
                location = str(path.relative_to(self.workspace))
            except ValueError:
                location = str(path)
        else:
            location = path
        self.issues.append(
            IsolationIssue(
                severity="high",
                code=code,
                location=location,
                message=message,
                fix=fix,
            )
        )

    def scan_text_for_foreign_tokens(
        self, file_path: Path, content: str, platform_name: str
    ) -> None:
        for other in PLATFORMS:
            if other == platform_name:
                continue
            if f"{other}/" in content:
                self.add_issue(
                    code="cross_domain_reference",
                    path=file_path,
                    message=f"Contains foreign platform token '{other}/'.",
                    fix=f"Rewrite references to use local '{platform_name}/' paths only.",
                )

    def check_markdown_links(self, file_path: Path, content: str, platform_root: Path) -> None:
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for match in link_pattern.finditer(content):
            raw_target = match.group(1).strip().strip("<>").strip()
            if not raw_target:
                continue
            if raw_target.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue

            target = raw_target.split("#", 1)[0].strip()
            if not target:
                continue

            resolved = (file_path.parent / target).resolve()
            try:
                resolved.relative_to(platform_root.resolve())
            except ValueError:
                self.add_issue(
                    code="link_leaves_platform",
                    path=file_path,
                    message=f"Relative link escapes platform root: '{raw_target}'.",
                    fix="Use links that resolve within the current platform directory.",
                )
                continue

            if not resolved.exists():
                self.add_issue(
                    code="broken_internal_link",
                    path=file_path,
                    message=f"Broken internal link: '{raw_target}'.",
                    fix="Fix the target path or remove the outdated link.",
                )

    def lint_platform(self, platform_name: str) -> None:
        platform_root = self.workspace / platform_name
        if not platform_root.exists():
            self.add_issue(
                code="missing_platform_directory",
                path=platform_root,
                message=f"Platform directory '{platform_name}' is missing.",
                fix="Restore the missing platform directory.",
            )
            return

        for file_path in platform_root.rglob("*"):
            if not file_path.is_file():
                continue
            suffix = file_path.suffix.lower()
            if suffix not in TEXT_EXTENSIONS:
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError as exc:
                self.add_issue(
                    code="file_read_error",
                    path=file_path,
                    message=f"Cannot read file: {exc}",
                    fix="Ensure the file is readable and not corrupted.",
                )
                continue

            self.scan_text_for_foreign_tokens(file_path, content, platform_name)
            if suffix in {".md", ".mdc"}:
                self.check_markdown_links(file_path, content, platform_root)

    def run(self, platform: Optional[str] = None) -> int:
        targets = [platform] if platform else list(PLATFORMS)
        for platform_name in targets:
            self.lint_platform(platform_name)
        return 1 if self.issues else 0

    def summary(self) -> Dict[str, object]:
        return {
            "workspace": str(self.workspace),
            "issues": len(self.issues),
            "codes": sorted({issue.code for issue in self.issues}),
        }

    def write_report(self, output_path: Optional[Path]) -> None:
        if not output_path:
            return
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "summary": self.summary(),
            "issues": [asdict(issue) for issue in self.issues],
        }
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint platform isolation boundaries.")
    parser.add_argument(
        "workspace",
        nargs="?",
        default="/workspace",
        help="Workspace containing .agent/.claude/.cursor.",
    )
    parser.add_argument(
        "--platform",
        choices=PLATFORMS,
        help="Limit checks to one platform.",
    )
    parser.add_argument(
        "--report",
        help="Optional JSON report path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    linter = IsolationLinter(Path(args.workspace))
    exit_code = linter.run(platform=args.platform)
    report_path = Path(args.report) if args.report else None
    linter.write_report(report_path)

    summary = linter.summary()
    print("ISOLATION LINT")
    print(f"Workspace: {summary['workspace']}")
    print(f"Issues: {summary['issues']}")
    if linter.issues:
        for issue in linter.issues[:30]:
            print(f"- [{issue.code}] {issue.location}: {issue.message}")
        if len(linter.issues) > 30:
            print(f"... and {len(linter.issues) - 30} more")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
