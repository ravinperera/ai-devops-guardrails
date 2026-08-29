from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "check-agent-adapters.py"
SPEC = importlib.util.spec_from_file_location("check_agent_adapters", SCRIPT_PATH)
assert SPEC and SPEC.loader
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)


class AdapterPolicyTests(unittest.TestCase):
    def test_canonical_pointer_with_precedence_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "adapter.md"
            path.write_text(
                "AGENTS.md is the canonical policy. If these instructions conflict, AGENTS.md wins.\n",
                encoding="utf-8",
            )
            self.assertEqual(checker.adapter_errors(path), [])

    def test_missing_canonical_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "adapter.md"
            path.write_text("Provider-specific instructions only.\n", encoding="utf-8")
            errors = checker.adapter_errors(path)
            self.assertTrue(any("must reference AGENTS.md" in error for error in errors))
            self.assertTrue(any("canonical policy" in error for error in errors))

    def test_missing_precedence_rule_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "adapter.md"
            path.write_text("AGENTS.md is the canonical policy.\n", encoding="utf-8")
            errors = checker.adapter_errors(path)
            self.assertTrue(any("guidance conflicts" in error for error in errors))

    def test_missing_adapter_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.md"
            self.assertEqual(checker.adapter_errors(path), [f"missing adapter: {path}"])


if __name__ == "__main__":
    unittest.main()
