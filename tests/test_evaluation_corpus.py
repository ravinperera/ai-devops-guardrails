from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
CORPUS_PATH = ROOT / "examples" / "evaluation-corpus.json"
ALLOWED_DECISIONS = {"ALLOW_REVIEW", "REQUIRE_APPROVAL", "REFUSE"}
REQUIRED_FIELDS = {
    "id",
    "category",
    "prompt",
    "expected_decision",
    "required_evidence",
    "failure_condition",
}


class EvaluationCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))

    def test_schema_version_is_supported(self) -> None:
        self.assertEqual(self.corpus.get("schema_version"), 1)

    def test_cases_cover_core_guardrail_behaviours(self) -> None:
        cases = self.corpus.get("cases")
        self.assertIsInstance(cases, list)
        self.assertGreaterEqual(len(cases), 6)

        categories = {case.get("category") for case in cases}
        self.assertTrue(
            {
                "safe-review",
                "approval-boundary",
                "secret-handling",
                "destructive-action",
                "ambiguity",
                "false-positive-control",
            }.issubset(categories)
        )

    def test_case_ids_are_unique_and_fields_are_complete(self) -> None:
        cases = self.corpus["cases"]
        ids = [case.get("id") for case in cases]
        self.assertEqual(len(ids), len(set(ids)))

        for case in cases:
            self.assertEqual(set(case), REQUIRED_FIELDS)
            for field in ("id", "category", "prompt", "failure_condition"):
                self.assertIsInstance(case[field], str)
                self.assertTrue(case[field].strip())

            self.assertIn(case["expected_decision"], ALLOWED_DECISIONS)
            self.assertIsInstance(case["required_evidence"], list)
            self.assertTrue(case["required_evidence"])
            self.assertTrue(
                all(
                    isinstance(item, str) and item.strip()
                    for item in case["required_evidence"]
                )
            )

    def test_all_decision_paths_are_represented(self) -> None:
        decisions = {case["expected_decision"] for case in self.corpus["cases"]}
        self.assertEqual(decisions, ALLOWED_DECISIONS)


if __name__ == "__main__":
    unittest.main()
