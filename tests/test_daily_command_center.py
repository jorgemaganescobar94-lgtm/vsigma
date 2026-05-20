from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class DailyCommandCenterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_daily_command_center")
        self.target_date = "2026-05-19"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_daily_command_center"))
        self.assertTrue(hasattr(self.module, "build_verdict"))

    def test_waiting_for_prelock_maps_to_review_hold(self) -> None:
        text = """# vSIGMA Autonomous Monitoring Summary
- daily_classification: WAITING_FOR_PRELOCK
- operational_verdict: WAITING_FOR_PRELOCK
- action_level: REVIEW_REQUIRED
- predictive_failure: NO
- evidence_basis: decision_quality_review
## Operator Action
- Wait for next scheduled AUTO/PRELOCK run.
"""
        verdict = self.module.build_verdict(text)
        self.assertEqual(verdict.command_center_status, "REVIEW_HOLD")
        self.assertEqual(verdict.daily_classification, "WAITING_FOR_PRELOCK")
        self.assertEqual(verdict.predictive_failure, "NO")
        self.assertIn("Wait for next", verdict.next_action)

    def test_data_blocked_maps_to_action_required(self) -> None:
        text = """# vSIGMA Autonomous Monitoring Summary
- daily_classification: DATA_BLOCKED
- operational_verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA
- action_level: ACTION_REQUIRED
- predictive_failure: NO
- evidence_basis: decision_quality_review
## Operator Action
- Check provider/API coverage.
"""
        verdict = self.module.build_verdict(text)
        self.assertEqual(verdict.command_center_status, "ACTION_REQUIRED")
        self.assertEqual(verdict.daily_classification, "DATA_BLOCKED")
        self.assertIn("Check provider", verdict.next_action)

    def test_build_daily_command_center_outputs_markdown_and_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            (today_dir / "vsigma_autonomous_monitoring_summary.md").write_text(
                "\n".join(
                    [
                        "# vSIGMA Autonomous Monitoring Summary",
                        "- daily_classification: NO_BET_VALID",
                        "- operational_verdict: NO_EXECUTION_NO_BET_VALID",
                        "- action_level: NO_ACTION_REQUIRED",
                        "- predictive_failure: NO",
                        "- evidence_basis: decision_quality_review",
                        "## Operator Action",
                        "- No manual execution needed.",
                    ]
                ),
                encoding="utf-8",
            )
            (today_dir / "vsigma_decision_outcome_ledger.csv").write_text(
                "target_date,fixture_id,market_primary,official_action,execution_family_status\n"
                "2026-05-19,123,OVER_1_5,NO_BET,NO_EXECUTION\n",
                encoding="utf-8",
            )
            (today_dir / "vsigma_decision_quality_review.csv").write_text(
                "target_date,fixture_id,decision_quality_label,quality_bucket\n"
                "2026-05-19,123,NO_BET_UNRESOLVED,NEEDS_MORE_DATA\n",
                encoding="utf-8",
            )

            verdict, md_path, csv_path = self.module.build_daily_command_center(
                target_date=self.target_date,
                mode="auto",
                processed_dir=processed_dir,
                now=datetime(2026, 5, 19, 21, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
                run_url="https://example/run",
            )
            markdown = md_path.read_text(encoding="utf-8")
            csv_text = csv_path.read_text(encoding="utf-8")

        self.assertEqual(verdict.command_center_status, "NO_ACTION_REQUIRED")
        self.assertIn("# vSIGMA Daily Command Center - 2026-05-19", markdown)
        self.assertIn("decision_outcome_rows: 1", markdown)
        self.assertIn("NO_BET_VALID", csv_text)


if __name__ == "__main__":
    unittest.main()
