#!/usr/bin/env bash
# Run all CI validation scripts (link validation, platform isolation, docs secrets).
# Usage: ./run-validations.sh [REPO_ROOT]
#   REPO_ROOT: path to repo root (default: directory containing this script).
#
# Requirements: bash, git, Python 3. Run from repo root or pass root as first argument.
# On Windows: use Git Bash or WSL to run this script.

set -euo pipefail

REPO_ROOT="${1:-}"
if [[ -z "$REPO_ROOT" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
  REPO_ROOT="$SCRIPT_DIR"
fi
cd "$REPO_ROOT"

if [[ ! -d ".github/scripts" ]]; then
  echo "::error::Not a repo root (no .github/scripts): $REPO_ROOT"
  exit 2
fi

# Prefer python3; fall back to python for systems that only have python in PATH
PYTHON=""
for cmd in python3 python; do
  if command -v "$cmd" &>/dev/null; then
    PYTHON="$cmd"
    break
  fi
done
if [[ -z "$PYTHON" ]]; then
  echo "::error::Python 3 required (python3 or python not found)"
  exit 2
fi

FAILED=0

run_step() {
  local name="$1"
  shift
  echo "--- $name ---"
  if "$@"; then
    echo ""
    return 0
  else
    echo "::error::$name failed."
    FAILED=1
    return 1
  fi
}

run_step "Link validation (.cursor, .claude, .agent)" \
  "$PYTHON" .github/scripts/validate-links.py --platform .cursor --platform .claude --platform .agent

run_step "Dangling skills check (.cursor, .agent, .claude)" \
  "$PYTHON" .github/scripts/skills-dangling-check.py --platform all

run_step "Platform isolation" \
  bash .github/scripts/check-platform-isolation.sh .

run_step "Docs secrets check" \
  "$PYTHON" .github/scripts/sanitize-docs-secrets.py --check .

if [[ $FAILED -ne 0 ]]; then
  echo "One or more validations failed."
  exit 1
fi
echo "All validations passed."
