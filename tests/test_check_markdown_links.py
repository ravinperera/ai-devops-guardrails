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


    def test_existing_local_images_pass(self) -> None:
        failures = self.run_check(
            "![Diagram](docs/diagram.png)\n![](docs/icon.svg)\n",
            ["docs/diagram.png", "docs/icon.svg"],
        )
        self.assertEqual(failures, [])

    def test_missing_local_images_fail_even_with_empty_alt_text(self) -> None:
        failures = self.run_check(
            "![Diagram](docs/missing.png)\n![](docs/missing-icon.svg)\n"
        )
        self.assertEqual(
            2, sum("missing local link target" in failure for failure in failures)
        )

    def test_local_image_cannot_escape_repository(self) -> None:
        failures = self.run_check("![Outside](../outside.png)\n")
        self.assertTrue(any("escapes repository" in failure for failure in failures))

    def test_remote_and_data_images_are_ignored(self) -> None:
        failures = self.run_check(
            "![Remote](https://example.com/image.png)\n"
            "![](data:image/png;base64,AAAA)\n"
        )
        self.assertEqual(failures, [])

    def test_image_inside_fenced_example_is_ignored(self) -> None:
        failures = self.run_check(
            "~~~markdown\n![Example](docs/missing.png)\n~~~\n"
        )
        self.assertEqual(failures, [])

    def test_quoted_link_titles_and_angle_paths_pass(self) -> None:
        failures = self.run_check(
            "[Guide](docs/guide.md \"Guide\")\n"
            "[Details](<docs/my guide.md> 'More details')\n"
            "![Diagram](docs/diagram.png \"Architecture diagram\")\n",
            ["docs/guide.md", "docs/my guide.md", "docs/diagram.png"],
        )
        self.assertEqual(failures, [])

    def test_missing_local_link_with_title_still_fails(self) -> None:
        failures = self.run_check('[Missing](docs/missing.md "Reference")\n')
        self.assertTrue(
            any("missing local link target" in failure for failure in failures)
        )


    def test_shorter_backtick_fence_does_not_close_longer_fence(self) -> None:
        failures = self.run_check(
            "````markdown\n"
            "[example](missing-hidden.md)\n"
            "```\n"
            "[still example](also-hidden.md)\n"
            "````\n"
            "[visible](missing-visible.md)\n"
        )
        self.assertEqual(len(failures), 1)
        self.assertIn("missing-visible.md", failures[0])

    def test_tilde_fence_requires_matching_character_and_length(self) -> None:
        failures = self.run_check(
            "~~~~markdown\n"
            "[example](missing-hidden.md)\n"
            "~~~\n"
            "[still example](also-hidden.md)\n"
            "```\n"
            "[also example](another-hidden.md)\n"
            "~~~~\n"
            "[visible](docs/real.md)\n",
            ["docs/real.md"],
        )
        self.assertEqual(failures, [])

    def test_closing_fence_cannot_have_info_string(self) -> None:
        failures = self.run_check(
            "````markdown\n"
            "[example](missing-hidden.md)\n"
            "````not-a-close\n"
            "[still example](also-hidden.md)\n"
            "````\n"
            "[visible](missing-visible.md)\n"
        )
        self.assertEqual(len(failures), 1)
        self.assertIn("missing-visible.md", failures[0])



if __name__ == "__main__":
    unittest.main()
