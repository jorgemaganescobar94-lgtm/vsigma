#!/usr/bin/env python3
"""Guardrails for vSIGMA automerge governance."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Sequence

ALLOWED_PREFIXES = (
    ".github/workflows/",
    "tests/",
    "docs/",
    ".codex/",
)

ALLOWED_EXACT_FILES = {
    "scripts/build_autonomous_monitoring_summary.py",
    "scripts/dispatch_autonomous_monitoring_notification.py",
    "scripts/build_daily_command_center.py",
    "scripts/check_automerge_guardrails.py",
    "README.md",
    "AGENTS.md",
}

ALWAYS_BLOCK_PREFIXES = ("data/",)
ALWAYS_BLOCK_EXACT = {".env"}
ALWAYS_BLOCK_SUBSTRINGS = ("secret",)
BLOCKED_SCRIPT_KEYWORDS = (
    "scoring",
    "score",
    "model",
    "prediction",
    "calibration",
    "selection",
    "backtest",
    "odds",
    "enrich",
    "filter",
    "core",
    "threshold",
    "rank",
    "market",
    "result",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check file-level automerge guardrails")
    parser.add_argument("--base-ref", help="Base git ref for diff", default=None)
    parser.add_argument("--head-ref", help="Head git ref for diff", default=None)
    parser.add_argument(
        "--changed-files",
        nargs="*",
        default=None,
        help="Explicit changed files list; when omitted we read from git diff --name-only base...head",
    )
    return parser.parse_args()


def _normalize_paths(files: Iterable[str]) -> List[str]:
    normalized: List[str] = []
    for raw in files:
        value = raw.strip()
        if not value:
            continue
        normalized.append(value.replace("\\", "/"))
    return normalized


def get_changed_files(args: argparse.Namespace) -> List[str]:
    if args.changed_files is not None and len(args.changed_files) > 0:
        return _normalize_paths(args.changed_files)

    if not args.base_ref or not args.head_ref:
        raise ValueError("Either --changed-files or both --base-ref and --head-ref are required.")

    cmd = ["git", "diff", "--name-only", f"{args.base_ref}...{args.head_ref}"]
    proc = subprocess.run(cmd, check=True, text=True, capture_output=True)
    return _normalize_paths(proc.stdout.splitlines())


def is_allowlisted(path: str) -> bool:
    if path in ALLOWED_EXACT_FILES:
        return True
    return any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def evaluate_file(path: str) -> str | None:
    lower = path.lower()

    if path in ALWAYS_BLOCK_EXACT:
        return "exactly blocked (.env)."

    if any(path.startswith(prefix) for prefix in ALWAYS_BLOCK_PREFIXES):
        return "inside blocked data/ area."

    if any(token in lower for token in ALWAYS_BLOCK_SUBSTRINGS):
        return 'contains blocked substring "secret".'

    if path.startswith("scripts/"):
        filename = Path(path).name.lower()
        if any(keyword in filename for keyword in BLOCKED_SCRIPT_KEYWORDS):
            return "script filename matches blocked predictive/governance keyword."

    if not is_allowlisted(path):
        return "not in explicit automerge allowlist."

    return None


def evaluate_files(files: Sequence[str]) -> List[str]:
    failures: List[str] = []
    for path in files:
        reason = evaluate_file(path)
        if reason:
            failures.append(f"BLOCKED: {path} -> {reason}")
    return failures


def main() -> int:
    args = parse_args()
    try:
        changed_files = get_changed_files(args)
    except Exception as exc:
        print(f"ERROR: unable to resolve changed files: {exc}")
        return 1

    if not changed_files:
        print("ALLOW: no changed files detected.")
        return 0

    failures = evaluate_files(changed_files)

    print("Automerge guardrails report")
    print(f"Changed files: {len(changed_files)}")
    for path in changed_files:
        print(f" - {path}")

    if failures:
        print("\nResult: BLOCKED")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print("\nResult: ALLOWED (all files within safe allowlist and no blocklist hits)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
