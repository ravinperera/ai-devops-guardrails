#!/usr/bin/env python3
"""Check that provider adapters explicitly defer to the canonical AGENTS.md policy."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

DEFAULT_ADAPTERS = (
    Path("CLAUDE.md"),
    Path(".github/copilot-instructions.md"),
)
CANONICAL = "AGENTS.md"


def adapter_errors(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing adapter: {path}"]

    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    errors: list[str] = []
    if CANONICAL not in text:
        errors.append(f"{path}: must reference {CANONICAL}")
    if "canonical" not in lowered:
        errors.append(f"{path}: must identify {CANONICAL} as canonical policy")
    if "conflict" not in lowered and "precedence" not in lowered:
        errors.append(f"{path}: must state which instructions win if guidance conflicts")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    failures = 0
    for relative_path in DEFAULT_ADAPTERS:
        path = args.root / relative_path
        errors = adapter_errors(path)
        if errors:
            failures += 1
            for error in errors:
                print(f"ERROR {error}")
        else:
            print(f"PASS  {relative_path}")

    if failures:
        print(f"\nAdapter policy check failed for {failures} file(s).")
        return 1

    print("\nAll supported provider adapters reference the canonical policy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
