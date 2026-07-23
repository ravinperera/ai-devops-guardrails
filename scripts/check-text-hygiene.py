#!/usr/bin/env python3
"""Check tracked Markdown and YAML files for portable text hygiene issues."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CHECKED_SUFFIXES = {".md", ".yml", ".yaml"}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [Path(item.decode("utf-8")) for item in result.stdout.split(b"\0") if item]


def check_file(path: Path) -> list[str]:
    failures: list[str] = []
    raw = path.read_bytes()

    if b"\0" in raw:
        failures.append(f"{path}: contains a NUL byte")
        return failures

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        failures.append(f"{path}: is not valid UTF-8 ({exc})")
        return failures

    if text and not text.endswith("\n"):
        failures.append(f"{path}: missing final newline")

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.rstrip(" \t") != line:
            failures.append(f"{path}:{line_number}: trailing whitespace")

    return failures


def main() -> int:
    failures: list[str] = []
    checked = 0

    for path in tracked_files():
        if path.suffix.lower() not in CHECKED_SUFFIXES:
            continue
        checked += 1
        failures.extend(check_file(path))

    if failures:
        print("Text hygiene validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated UTF-8, final newlines, and trailing whitespace in {checked} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
