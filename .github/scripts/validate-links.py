#!/usr/bin/env python3
"""
Validate intra-platform markdown links for Agentic-Skills platforms.

Checks that all markdown links in .md/.mdc files under a given platform root:
- Use relative paths (no absolute filesystem paths).
- Point to existing targets when they reference .md, .mdc, or .py files.
- Stay within the same platform directory tree (no cross-platform links).

Usage:
  python validate-links.py --platform .cursor
  python validate-links.py --platform .cursor --platform .claude --platform .agent
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

DOC_EXTENSIONS = {".md", ".mdc"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", ".vs"}

# Basic markdown link pattern: [label](target)
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def should_skip(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    for part in rel.parts:
        if part in SKIP_DIRS:
            return True
    return False


def is_external_target(target: str) -> bool:
    t = target.strip()
    if not t:
        return True
    # Pure anchors like "#section"
    if t.startswith("#"):
        return True
    # URLs and mailto
    if "://" in t or t.startswith("mailto:"):
        return True
    return False


def iter_doc_files(root: Path) -> Iterable[Path]:
    for ext in DOC_EXTENSIONS:
        for p in root.rglob(f"*{ext}"):
            if not p.is_file() or should_skip(p, root):
                continue
            yield p


def path_within_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def check_links_in_file(path: Path, platform_root: Path) -> List[Tuple[int, str, str]]:
    """
    Return a list of (line_number, target, reason) for invalid links in this file.
    Only checks links whose targets look like .md/.mdc/.py paths (optionally with #anchors).
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    errors: List[Tuple[int, str, str]] = []
    lines = text.splitlines()

    for idx, line in enumerate(lines, start=1):
        for match in MARKDOWN_LINK.finditer(line):
            target_raw = match.group(2).strip()

            # Skip external URLs/anchors
            if is_external_target(target_raw):
                continue

            # Absolute filesystem paths are not allowed
            if target_raw.startswith("/"):
                errors.append((idx, target_raw, "absolute path not allowed; use relative path within platform"))
                continue

            # Strip any in-file anchor (file.md#section)
            target_no_anchor = target_raw.split("#", 1)[0]
            if not target_no_anchor:
                # link like []( #anchor ) is fine
                continue

            suffix = Path(target_no_anchor).suffix.lower()
            # Only validate links that explicitly point to .md/.mdc/.py targets
            if suffix not in {".md", ".mdc", ".py"}:
                continue

            resolved = (path.parent / target_no_anchor).resolve()

            # Must remain inside the same platform root
            if not path_within_root(resolved, platform_root):
                errors.append((idx, target_raw, "target escapes platform root; links must stay within this platform"))
                continue

            if not resolved.exists():
                errors.append((idx, target_raw, "target file does not exist"))

    return errors


def validate_platform(platform_root: Path) -> int:
    if not platform_root.is_dir():
        print(f"[ERROR] Platform root is not a directory: {platform_root}", file=sys.stderr)
        return 1

    print(f"Validating links under platform: {platform_root}")
    total_errors = 0

    for doc in sorted(iter_doc_files(platform_root)):
        file_errors = check_links_in_file(doc, platform_root)
        if not file_errors:
            continue
        rel = doc.relative_to(platform_root)
        for line_no, target, reason in file_errors:
            print(f"{platform_root.name}/{rel}:{line_no}: invalid link '{target}': {reason}")
        total_errors += len(file_errors)

    if total_errors == 0:
        print(f"[OK] No invalid links found in {platform_root}")
        return 0

    print(f"[FAIL] {total_errors} invalid link(s) found in {platform_root}", file=sys.stderr)
    return 1


def parse_args(argv: List[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Validate intra-platform markdown links.")
    ap.add_argument(
        "--platform",
        dest="platforms",
        action="append",
        default=[],
        help="Platform root to validate (e.g. .cursor, .claude, .agent). Can be passed multiple times.",
    )
    return ap.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)

    if not args.platforms:
        print("No platforms specified. Use --platform .cursor (and/or .claude, .agent).", file=sys.stderr)
        return 2

    repo_root = Path(".").resolve()
    exit_code = 0

    for platform in args.platforms:
        root = (repo_root / platform).resolve()
        rc = validate_platform(root)
        if rc != 0:
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

