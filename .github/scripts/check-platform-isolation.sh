#!/usr/bin/env bash
# Ensures each platform (.agent, .claude, .cursor) is self-contained:
# no references to files or paths outside the platform's own directory.
# Excludes debug/temporary docs (paths containing DEBUG) that may legitimately reference other platforms.
set -euo pipefail

REPO_ROOT="${1:-.}"
cd "$REPO_ROOT"
FAILED=0

# Pathspec to exclude debug docs (e.g. .cursor/DEBUG-MERGE-PR9-DEVELOP-TO-MAIN.md) from isolation check
EXCLUDE_DEBUG=':(exclude)*DEBUG*'

check_platform() {
  local platform="$1"
  shift
  local others=("$@")
  local other_pattern
  other_pattern="\.($(IFS='|'; echo "${others[*]}"))/"
  if git grep -n -E "$other_pattern" -- "$platform" "$EXCLUDE_DEBUG" 2>/dev/null; then
    echo "::error::[${platform}] Found reference to another platform (${other_pattern}). Platform must be self-contained."
    FAILED=1
  fi
  if git grep -n -E '\.\./\.\./\.(agent|claude|cursor)/' -- "$platform" "$EXCLUDE_DEBUG" 2>/dev/null; then
    echo "::error::[${platform}] Found path escaping platform (../../.agent/ or ../../.claude/ or ../../.cursor/)."
    FAILED=1
  fi
}

check_platform ".agent" "cursor" "claude"
check_platform ".claude" "cursor" "agent"
check_platform ".cursor" "agent" "claude"

if [[ $FAILED -ne 0 ]]; then
  echo "Platform isolation check failed. Each of .agent, .claude, .cursor must not reference the others."
  exit 1
fi
echo "Platform isolation check passed."
