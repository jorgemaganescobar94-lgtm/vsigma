from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class AutonomousMonitoringSummaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_autonomous_monitoring_summary")
        self.target_date = "2026-05-19"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_autonomous_monitoring_summary"))
        self.assertTrue(hasattr(self.module, "infer_classification"))

    def test_uses_decision_quality_classification_as_primary_signal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            (today_dir / "vsigma_decision_quality_review.md").write_text(
                "\n".join(
                    [
                        "# vSIGMA Decision Quality Review",
                        "- daily_classification: EXPIRED_PRELOCK",
                        "- operational_verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA",
                        "- predictive_failure: NO",
                        "- operational note: Candidate expired before execution; this is not predictive failure.",
                    ]
                ),
                encoding="utf-8",
            )

            verdict, md_path, csv_path = self.module.build_autonomous_monitoring_summary(
                target_date=self.target_date,
                mode="auto",
                processed_dir=processed_dir,
                now=datetime(2026, 5, 19, 20, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
                run_url="https://github.example/run/1",
            )

            markdown = md_path.read_text(encoding="utf-8")
            csv_text = csv_path.read_text(encoding="utf-8")

        self.assertEqual(verdict.daily_classification, "EXPIRED_PRELOCK")
        self.assertEqual(verdict.action_level, "REVIEW_REQUIRED")
        self.assertEqual(verdict.predictive_failure, "NO")
        self.assertIn("- daily_classification: EXPIRED_PRELOCK", markdown)
        self.assertIn("vsigma_decision_quality_review.md", markdown)
        self.assertIn("EXPIRED_PRELOCK", csv_text)

    def test_system_review_no_bet_valid_when_decision_quality_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            (today_dir / "vsigma_system_review.md").write_text(
                "\n".join(
                    [
                        "# vSIGMA System Review",
                        "- Official action summary: NO_BET",
                        "- Current operational verdict: NO_EXECUTION_NO_BET_VALID",
                    ]
                ),
                encoding="utf-8",
            )

            verdict, md_path, _csv_path = self.module.build_autonomous_monitoring_summary(
                target_date=self.target_date,
                mode="health",
                processed_dir=processed_dir,
                now=datetime(2026, 5, 19, 20, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )

            markdown = md_path.read_text(encoding="utf-8")

        self.assertEqual(verdict.daily_classification, "NO_BET_VALID")
        self.assertEqual(verdict.action_level, "NO_ACTION_REQUIRED")
        self.assertIn("- evidence_basis: system_review", markdown)

    def test_missing_sources_classifies_broken(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            verdict, md_path, _csv_path = self.module.build_autonomous_monitoring_summary(
                target_date=self.target_date,
                mode="auto",
                processed_dir=processed_dir,
                now=datetime(2026, 5, 19, 20, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            markdown = md_path.read_text(encoding="utf-8")

        self.assertEqual(verdict.daily_classification, "BROKEN")
        self.assertEqual(verdict.action_level, "ACTION_REQUIRED")
        self.assertIn("decision_quality_review: missing", markdown)
        self.assertIn("## Classification Contract", markdown)


if __name__ == "__main__":
    unittest.main()
