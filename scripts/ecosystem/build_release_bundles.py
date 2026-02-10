#!/usr/bin/env python3
"""Build standalone platform release bundles under dist/."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from isolation_lint import IsolationLinter

PLATFORM_MAP = {
    "agent": ".agent",
    "claude": ".claude",
    "cursor": ".cursor",
}


def build_bundle(workspace: Path, output_root: Path, bundle_name: str, source_dir_name: str) -> Dict[str, object]:
    source_dir = workspace / source_dir_name
    target_dir = output_root / bundle_name
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir)

    # Re-host copied bundle under a temporary workspace shape so isolation linter can run.
    temp_workspace = output_root / f".tmp_isolation_{bundle_name}"
    if temp_workspace.exists():
        shutil.rmtree(temp_workspace)
    temp_workspace.mkdir(parents=True, exist_ok=True)
    platform_root = temp_workspace / source_dir_name
    shutil.move(str(target_dir), str(platform_root))

    linter = IsolationLinter(temp_workspace)
    lint_exit = linter.run(platform=source_dir_name)
    issues = [issue for issue in linter.issues]

    # Move back to final bundle destination after checks.
    shutil.move(str(platform_root), str(target_dir))
    shutil.rmtree(temp_workspace, ignore_errors=True)

    file_count = sum(1 for p in target_dir.rglob("*") if p.is_file())
    manifest = {
        "bundle": bundle_name,
        "source": source_dir_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "file_count": file_count,
        "isolation_passed": lint_exit == 0,
        "isolation_issue_count": len(issues),
        "isolation_issues": [
            {
                "code": issue.code,
                "location": issue.location,
                "message": issue.message,
                "fix": issue.fix,
            }
            for issue in issues
        ],
    }
    (target_dir / "BUNDLE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build standalone platform bundles.")
    parser.add_argument(
        "workspace",
        nargs="?",
        default="/workspace",
        help="Workspace containing platform directories.",
    )
    parser.add_argument(
        "--output",
        default="/workspace/dist",
        help="Output directory for bundles.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete output directory before building bundles.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    output_root = Path(args.output).resolve()

    if args.clean and output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    manifests = []
    for bundle_name, source_dir_name in PLATFORM_MAP.items():
        manifest = build_bundle(workspace, output_root, bundle_name, source_dir_name)
        manifests.append(manifest)
        status = "PASS" if manifest["isolation_passed"] else "FAIL"
        print(
            f"[{status}] {bundle_name}: files={manifest['file_count']} "
            f"isolation_issues={manifest['isolation_issue_count']}"
        )

    index_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "bundles": manifests,
    }
    (output_root / "BUNDLES_INDEX.json").write_text(
        json.dumps(index_payload, indent=2), encoding="utf-8"
    )

    failures = [bundle for bundle in manifests if not bundle["isolation_passed"]]
    if failures:
        print("Bundle build failed isolation checks.")
        return 1

    print(f"Bundle build complete: {output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
