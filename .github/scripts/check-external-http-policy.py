#!/usr/bin/env python3
"""
Check that agent/skill docs do not instruct direct connection to external HTTP services.
Agents must only use allowed tools inside the user's IDE and must not be instructed
to access the internet directly.

Scans .agent, .claude, .cursor for external http(s) links and flags lines that
instruct the reader/agent to fetch, navigate, or connect to external URLs.
No HTTP requests are made; local file scan and regex only.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

DOC_EXTENSIONS = {".md", ".mdc"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", ".vs"}

# External URL: http:// or https://, then non-whitespace/paren/bracket/quote/angle
URL_PATTERN = re.compile(r"https?://[^\s\)\]\"\'<>]+")

# Directive phrases (case-insensitive) that instruct direct use of external URL/internet
DIRECTIVE_PATTERNS = [
    re.compile(r"\bfetch\s+(?:the\s+latest|fresh|from|additional)", re.I),
    re.compile(r"\buse\s+webfetch\b", re.I),
    re.compile(r"\bwebfetch\s+to\s+", re.I),
    re.compile(r"\bnavigate\s+to\s+", re.I),
    re.compile(r"\bopen\s+(?:url|https?://)", re.I),
    re.compile(r"\bconnect\s+to\s+.*(?:http|url)", re.I),
    re.compile(r"\bretrieve\s+from\s+", re.I),
    re.compile(r"\bcall\s+.*\bapi\b", re.I),
    re.compile(r"\buse\s+.*\s+to\s+load\s+", re.I),
    re.compile(r"\bfetch\s+from\s+", re.I),
    re.compile(r"\bfetch\s+(?:specific\s+)?pages?\s+", re.I),
    re.compile(r"\buse\s+web\s+search\s+and\s+webfetch", re.I),
    re.compile(r"\buse\s+webfetch\s+as\s+needed", re.I),
]


def should_skip(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    for part in rel.parts:
        if part in SKIP_DIRS:
            return True
    return False


def iter_doc_files(platform_roots: List[Path]) -> List[Path]:
    out: List[Path] = []
    for root in platform_roots:
        if not root.is_dir():
            continue
        for ext in DOC_EXTENSIONS:
            for p in root.rglob(f"*{ext}"):
                if not p.is_file() or should_skip(p, root):
                    continue
                out.append(p)
    return sorted(out)


def trim_url(url: str) -> str:
    # Trim trailing punctuation that might be sentence-ending
    return url.rstrip(".,;:!?)")


def line_contains_external_url(line: str) -> bool:
    return bool(URL_PATTERN.search(line))


def line_contains_directive(line: str) -> bool:
    for pat in DIRECTIVE_PATTERNS:
        if pat.search(line):
            return True
    return False


def check_file(path: Path) -> Tuple[List[Tuple[int, str]], List[Tuple[int, str, str]]]:
    """
    Returns (external_links, violations).
    external_links: [(line_no, url), ...]
    violations: [(line_no, line_snippet, reason), ...]
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return [], []

    external_links: List[Tuple[int, str]] = []
    violations: List[Tuple[int, str, str]] = []

    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        has_url = line_contains_external_url(line)
        if has_url:
            for m in URL_PATTERN.finditer(line):
                external_links.append((idx, trim_url(m.group(0))))
        if has_url and line_contains_directive(line):
            snippet = line.strip()[:100] + ("..." if len(line) > 100 else "")
            violations.append((idx, snippet, "instructs direct connection to external HTTP"))

    return external_links, violations


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check agent/skill docs for forbidden instructions to connect to external HTTP."
    )
    parser.add_argument(
        "--platform",
        dest="platforms",
        action="append",
        default=[],
        help="Platform root (e.g. .cursor). Can be repeated. Default: .cursor .claude .agent",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="List links and violations but exit 0 (do not fail CI)",
    )
    args = parser.parse_args(argv or sys.argv[1:])

    repo_root = Path(".").resolve()
    if not args.platforms:
        args.platforms = [".cursor", ".claude", ".agent"]

    platform_roots = [repo_root / p for p in args.platforms]
    doc_files = iter_doc_files(platform_roots)

    all_links: List[Tuple[Path, int, str]] = []
    all_violations: List[Tuple[Path, int, str, str]] = []

    for path in doc_files:
        links, violations = check_file(path)
        for line_no, url in links:
            all_links.append((path, line_no, url))
        for line_no, snippet, reason in violations:
            all_violations.append((path, line_no, snippet, reason))

    # Summary
    rel_links = [(p.relative_to(repo_root), ln, u) for p, ln, u in all_links]
    rel_violations = [(p.relative_to(repo_root), ln, sn, r) for p, ln, sn, r in all_violations]

    print(f"External HTTP(S) links found: {len(all_links)}")
    print(f"Policy violations (instruct direct external access): {len(all_violations)}")

    if all_violations:
        print("\nViolations:", file=sys.stderr)
        for rel_path, line_no, snippet, reason in rel_violations:
            print(f"  {rel_path}:{line_no}: {reason}", file=sys.stderr)
            print(f"    {snippet}", file=sys.stderr)

    if all_violations and not args.report_only:
        print("\n[FAIL] Agent/skill docs must not instruct direct connection to external HTTP.", file=sys.stderr)
        return 1

    print("[OK] No policy violations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
