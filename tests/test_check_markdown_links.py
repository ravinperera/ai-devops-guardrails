from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "check-markdown-links.py"
SPEC = importlib.util.spec_from_file_location("check_markdown_links", MODULE_PATH)
assert SPEC and SPEC.loader
links = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = links
SPEC.loader.exec_module(links)


class MarkdownLinkTests(unittest.TestCase):
    def run_check(self, markdown: str, targets: list[str] | None = None) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text(markdown, encoding="utf-8")
            for relative in targets or []:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("# Target\n", encoding="utf-8")
            return links.check_markdown_links(readme, root)

    def test_existing_local_link_passes(self) -> None:
        failures = self.run_check(
            "See [guide](docs/guide.md).\n",
            ["docs/guide.md"],
        )
        self.assertEqual(failures, [])

    def test_missing_local_link_fails(self) -> None:
        failures = self.run_check("See [missing](docs/missing.md).\n")
        self.assertTrue(any("missing local link target" in failure for failure in failures))

    def test_repository_escape_fails(self) -> None:
        failures = self.run_check("See [outside](../outside.md).\n")
        self.assertTrue(any("escapes repository" in failure for failure in failures))

    def test_external_urls_and_anchors_are_ignored(self) -> None:
        failures = self.run_check(
            "See [website](https://example.com) and [section](#details).\n"
        )
        self.assertEqual(failures, [])

    def test_links_inside_fences_are_ignored(self) -> None:
        failures = self.run_check(
            "```markdown\n[placeholder](docs/not-created.md)\n```\n"
        )
        self.assertEqual(failures, [])

    def test_url_encoded_local_link_passes(self) -> None:
        failures = self.run_check(
            "See [guide](docs/my%20guide.md#section).\n",
            ["docs/my guide.md"],
        )
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
