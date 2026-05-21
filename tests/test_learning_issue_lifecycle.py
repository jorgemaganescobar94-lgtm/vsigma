from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class LearningIssueLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_learning_issue_lifecycle")
        self.target_date = "2026-05-21"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_learning_issue_lifecycle"))
        self.assertTrue(hasattr(self.module, "classify_issue"))

    def test_keeps_current_consolidated_issue_open(self) -> None:
        issue = {
            "number": 37,
            "title": "vSIGMA OPERATIONAL_REVIEW_REQUIRED 2026-05-21",
            "url": "https://example.test/37",
        }
        row = self.module.classify_issue(issue, self.target_date)
        self.assertEqual(row["lifecycle_status"], "KEEP_OPEN_CURRENT_CONSOLIDATED")
        self.assertEqual(row["recommended_action"], "KEEP_OPEN")
        self.assertEqual(row["auto_close"], "NO")

    def test_flags_old_unconsolidated_duplicate(self) -> None:
        issue = {
            "number": 31,
            "title": "vSIGMA learning alert: DATA_QUALITY_REVIEW_REQUIRED OVER_1_5::UNKNOWN_RISK (2026-05-21)",
            "url": "https://example.test/31",
        }
        row = self.module.classify_issue(issue, self.target_date)
        self.assertEqual(row["lifecycle_status"], "OLD_UNCONSOLIDATED_DUPLICATE")
        self.assertEqual(row["recommended_action"], "CLOSE_IF_SUPERSEDED")
        self.assertEqual(row["production_change"], "NO")

    def test_flags_stale_consolidated_review(self) -> None:
        issue = {
            "number": 40,
            "title": "vSIGMA DATA_QUALITY_REVIEW_REQUIRED 2026-05-20",
            "url": "https://example.test/40",
        }
        row = self.module.classify_issue(issue, self.target_date)
        self.assertEqual(row["lifecycle_status"], "STALE_CONSOLIDATED_REVIEW")
        self.assertEqual(row["recommended_action"], "REVIEW_FOR_MANUAL_CLOSE")

    def test_build_outputs_with_stubbed_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            original = self.module.fetch_open_learning_issues
            self.module.fetch_open_learning_issues = lambda _repo: [
                {
                    "number": 37,
                    "title": "vSIGMA OPERATIONAL_REVIEW_REQUIRED 2026-05-21",
                    "url": "https://example.test/37",
                },
                {
                    "number": 31,
                    "title": "vSIGMA learning alert: DATA_QUALITY_REVIEW_REQUIRED OVER_1_5::UNKNOWN_RISK (2026-05-21)",
                    "url": "https://example.test/31",
                },
            ]
            try:
                rows, paths = self.module.build_learning_issue_lifecycle(
                    self.target_date,
                    processed_dir=processed_dir,
                    repo="owner/repo",
                    now=datetime(2026, 5, 21, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
                )
            finally:
                self.module.fetch_open_learning_issues = original

            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.today_md.read_text(encoding="utf-8")

        self.assertEqual(len(rows), 2)
        self.assertIn("KEEP_OPEN_CURRENT_CONSOLIDATED", csv_text)
        self.assertIn("OLD_UNCONSOLIDATED_DUPLICATE", csv_text)
        self.assertIn("auto_close: NO", md_text)

    def test_empty_inputs_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            original = self.module.fetch_open_learning_issues
            self.module.fetch_open_learning_issues = lambda _repo: []
            try:
                rows, paths = self.module.build_learning_issue_lifecycle(
                    self.target_date,
                    processed_dir=processed_dir,
                    repo="owner/repo",
                    now=datetime(2026, 5, 21, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
                )
            finally:
                self.module.fetch_open_learning_issues = original
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.governance_md.read_text(encoding="utf-8")

        self.assertEqual(rows, [])
        self.assertIn("issue_number", csv_text)
        self.assertIn("open_learning_issues_reviewed: 0", md_text)


if __name__ == "__main__":
    unittest.main()
