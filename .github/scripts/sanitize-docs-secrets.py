#!/usr/bin/env python3
"""
Scan documentation for .env references and API keys; report or replace with placeholders.
Only replaces values that look like real secrets (known key prefixes, long hex/tokens).
Usage:
  python sanitize-docs-secrets.py [--check] [--fix] [root_dir]
  --check: only report violations, exit 1 if any found (no writes)
  --fix: replace secrets with placeholders in place
  root_dir: repo root (default: .)
"""

import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER = "<REDACTED>"
DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".mdc"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", ".vs"}

# Known secret prefixes (real API keys / tokens)
SECRET_PREFIXES = re.compile(
    r"^(sk[-_](?:live|test)|ghp_|gho_|AKIA[0-9A-Z]|"
    r"[0-9a-f]{32,}$|"  # 32+ hex (e.g. MD5/session)
    r"[0-9A-Za-z\-_]{40,}$)",  # 40+ alnum (e.g. JWT/token)
    re.IGNORECASE,
)

# KEY=secret or KEY: secret (env-style); value must look like a secret
ENV_LINE = re.compile(
    r"^(?P<key>[A-Z][A-Z0-9_]*)\s*[:=]\s*"
    r"(?P<value>[^\s\n#]+|\"[^\"]*\"|'[^']*')",
    re.MULTILINE | re.IGNORECASE,
)

BEARER = re.compile(r"(Bearer\s+)([a-zA-Z0-9_\-\.]{20,})", re.IGNORECASE)
AUTH_HEADER = re.compile(
    r"(Authorization\s*:\s*Bearer\s+)([a-zA-Z0-9_\-\.]{20,})",
    re.IGNORECASE,
)
INLINE_SECRET = re.compile(
    r"(\b(?:api[_-]?key|secret|password|token|auth)\s*[:=]\s*[\"']?)([a-zA-Z0-9_\-\.]{16,})([\"']?)",
    re.IGNORECASE,
)


def should_skip(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    for part in rel.parts:
        if part in SKIP_DIRS:
            return True
    return False


def collect_doc_files(root: Path) -> list[Path]:
    out = []
    for ext in DOC_EXTENSIONS:
        for p in root.rglob(f"*{ext}"):
            if not p.is_file() or should_skip(p, root):
                continue
            try:
                p.relative_to(root)
            except ValueError:
                continue
            out.append(p)
    return sorted(out)


def looks_like_secret(value: str) -> bool:
    v = value.strip().strip("'\"").strip()
    if not v or len(v) < 16:
        return False
    if v in ("<REDACTED>", "YOUR_API_KEY", "your-api-key", "xxx", "...") or re.match(
        r"YOUR_.*_KEY", v, re.IGNORECASE
    ):
        return False
    if "/" in v or " " in v or ".md" in v or v.startswith(".") or "http" in v:
        return False
    if SECRET_PREFIXES.search(v):
        return True
    if re.match(r"^[0-9a-fA-F]{32,}$", v):
        return True
    if re.match(r"^[A-Za-z0-9_\-\.]{40,}$", v) and not v.replace(".", "").replace("-", "").replace("_", "").isalpha():
        return True
    return False


def apply_replacements(text: str) -> tuple[str, int]:
    count = 0

    def bear_repl(m):
        nonlocal count
        if looks_like_secret(m.group(2)):
            count += 1
            return m.group(1) + PLACEHOLDER
        return m.group(0)

    text = BEARER.sub(bear_repl, text)

    def auth_repl(m):
        nonlocal count
        if looks_like_secret(m.group(2)):
            count += 1
            return m.group(1) + PLACEHOLDER
        return m.group(0)

    text = AUTH_HEADER.sub(auth_repl, text)

    def inline_repl(m):
        nonlocal count
        if looks_like_secret(m.group(2)):
            count += 1
            return m.group(1) + PLACEHOLDER + (m.group(3) or "")
        return m.group(0)

    text = INLINE_SECRET.sub(inline_repl, text)

    def env_repl(m):
        nonlocal count
        val = m.group("value").strip().strip("'\"")
        if looks_like_secret(val):
            count += 1
            return m.group("key") + "=" + PLACEHOLDER
        return m.group(0)

    text = ENV_LINE.sub(env_repl, text)
    return text, count


def scan_file(path: Path, root: Path, fix: bool) -> int:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    new_text, n = apply_replacements(raw)
    if n > 0 and fix:
        path.write_text(new_text, encoding="utf-8")
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description="Sanitize docs for .env/API keys")
    ap.add_argument("--check", action="store_true", help="Only report; do not modify files")
    ap.add_argument("--fix", action="store_true", help="Replace secrets with placeholders")
    ap.add_argument("root_dir", nargs="?", default=".", help="Repo root")
    args = ap.parse_args()
    root = Path(args.root_dir).resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2
    fix = not args.check if not (args.check or args.fix) else args.fix

    doc_files = collect_doc_files(root)
    total = 0
    for p in doc_files:
        n = scan_file(p, root, fix=fix)
        if n > 0:
            rel = p.relative_to(root)
            print(f"{rel}: {n} replacement(s)" + (" (applied)" if fix else " (use --fix to replace)"))
            total += n
    if total > 0:
        if not fix:
            print("Run with --fix to replace secrets with placeholders.", file=sys.stderr)
        return 1
    print("No secrets found in documentation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
