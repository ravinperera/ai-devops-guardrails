#!/usr/bin/env python3
"""Validate repository-local links in tracked Markdown without network access."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path
from typing import Iterable

LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:")


def tracked_markdown_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "*.md"],
        check=True,
        capture_output=True,
    )
    return [
        root / item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    ]


def markdown_targets(text: str) -> Iterable[tuple[int, str]]:
    in_fence = False
    fence_marker: str | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            marker = "```"
        elif stripped.startswith("~~~"):
            marker = "~~~"
        else:
            marker = None

        if marker:
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
            continue

        if in_fence:
            continue

        for match in LINK_PATTERN.finditer(line):
            yield line_number, match.group(1).strip()


def check_markdown_links(path: Path, root: Path) -> list[str]:
    root = root.resolve()
    relative = path.resolve().relative_to(root)
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []

    for line_number, raw_target in markdown_targets(text):
        target = raw_target
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1].strip()

        lowered = target.casefold()
        if (
            not target
            or target.startswith("#")
            or lowered.startswith(EXTERNAL_PREFIXES)
            or "${{" in target
        ):
            continue

        decoded = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not decoded:
            continue

        resolved = (path.parent / decoded).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            failures.append(
                f"{relative}:{line_number}: local link escapes repository: {raw_target}"
            )
            continue

        if not resolved.exists():
            failures.append(
                f"{relative}:{line_number}: missing local link target: {raw_target}"
            )

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        type=Path,
        help="Repository root to validate (default: current directory)",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    failures: list[str] = []
    files = tracked_markdown_files(root)
    for path in files:
        failures.extend(check_markdown_links(path, root))

    if failures:
        print("Repository-local Markdown link validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated repository-local links in {len(files)} Markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
