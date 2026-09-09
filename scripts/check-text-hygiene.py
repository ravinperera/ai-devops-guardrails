#!/usr/bin/env python3
"""Check tracked repository text files for portable text hygiene issues."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

CHECKED_SUFFIXES = {".json", ".md", ".py", ".yml", ".yaml"}
SECRET_PATTERNS = (
    ("AWS access key ID", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub classic personal access token", re.compile(r"\bghp_[A-Za-z0-9]{36}\b")),
    (
        "GitHub fine-grained personal access token",
        re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    ),
    ("OpenAI-style API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    (
        "PEM private key header",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
)


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

        for label, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                failures.append(
                    f"{path}:{line_number}: possible unredacted {label}"
                )

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

    print(
        "Validated UTF-8, final newlines, trailing whitespace, and high-confidence "
        f"credential shapes in {checked} text files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
