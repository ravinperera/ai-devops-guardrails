from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "check-text-hygiene.py"
SPEC = importlib.util.spec_from_file_location("check_text_hygiene", MODULE_PATH)
assert SPEC and SPEC.loader
hygiene = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = hygiene
SPEC.loader.exec_module(hygiene)


class TextHygieneTests(unittest.TestCase):
    def check_bytes(self, content: bytes) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.md"
            path.write_bytes(content)
            return hygiene.check_file(path)

    def test_valid_utf8_with_final_newline_passes(self) -> None:
        self.assertEqual(self.check_bytes("# Café\n".encode("utf-8")), [])

    def test_trailing_whitespace_is_reported(self) -> None:
        failures = self.check_bytes(b"# Example  \n")
        self.assertTrue(any("trailing whitespace" in failure for failure in failures))

    def test_missing_final_newline_is_reported(self) -> None:
        failures = self.check_bytes(b"# Example")
        self.assertTrue(any("missing final newline" in failure for failure in failures))

    def test_nul_byte_is_reported(self) -> None:
        failures = self.check_bytes(b"# Example\x00\n")
        self.assertTrue(any("contains a NUL byte" in failure for failure in failures))

    def test_invalid_utf8_is_reported(self) -> None:
        failures = self.check_bytes(b"# Example\n\xff\n")
        self.assertTrue(any("is not valid UTF-8" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
