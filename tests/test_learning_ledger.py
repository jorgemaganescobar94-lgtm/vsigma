from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class LearningLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_learning_ledger")
        self.target_date = "2026-05-19"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_learning_ledger"))
        self.assertTrue(hasattr(self.module, "classify_learning_family"))

    def test_classifies_expired_prelock(self) -> None:
        row = {
            "official_action": "NO_BET",
            "final_block_reason": "KICKOFF_ALREADY_PASSED",
            "execution_family_status": "EXPIRED",
            "is_expired": "YES",
        }
        self.assertEqual(self.module.classify_learning_family(row), "EXPIRED_PRELOCK")
        status, priority, note = self.module.classify_learning_status(row, "EXPIRED_PRELOCK")
        self.assertEqual(status, "TIMING_REVIEW")
        self.assertEqual(priority, "P1")
        self.assertIn("timing", note.lower())

    def test_classifies_actionable_result(self) -> None:
        row = {"official_action": "EXECUTABLE", "result_status": "WIN", "is_actionable": "YES"}
        self.assertEqual(self.module.classify_learning_family(row), "ACTIONABLE_RESULT")
        status, priority, _note = self.module.classify_learning_status(row, "ACTIONABLE_RESULT")
        self.assertEqual(status, "COLLECT_MORE_SAMPLE")
        self.assertEqual(priority, "P3")

    def test_classifies_data_blocked(self) -> None:
        row = {"official_action": "NO_BET", "final_block_reason": "ODDS_NOT_AVAILABLE"}
        self.assertEqual(self.module.classify_learning_family(row), "DATA_BLOCKED")
        status, priority, _note = self.module.classify_learning_status(row, "DATA_BLOCKED")
        self.assertEqual(status, "DATA_REVIEW")
        self.assertEqual(priority, "P1")

    def test_generates_csv_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            ledger_dir = processed_dir / "ledger"
            today_dir = processed_dir / "today" / self.target_date
            ledger_dir.mkdir(parents=True)
            today_dir.mkdir(parents=True)
            (today_dir / "vsigma_decision_outcome_ledger.csv").write_text(
                "target_date,fixture_id,league,home_team,away_team,market_primary,official_action,executable_now,final_block_reason,execution_family_status,is_actionable,is_non_actionable,is_expired,accuracy_primary_risk,competition_calibrated_prob\n"
                "2026-05-19,123,Test League,Home,Away,OVER_1_5,EXECUTABLE,YES,NONE,PRELOCK_CONFIRMED,YES,NO,NO,LOW_RISK,0.72\n",
                encoding="utf-8",
            )
            (today_dir / "vsigma_decision_quality_review.csv").write_text(
                "target_date,fixture_id,market_primary,result_status,decision_quality_label,quality_bucket,improvement_signal,recommended_followup\n"
                "2026-05-19,123,OVER_1_5,WIN,ACTIONABLE_WIN,GOOD_DECISION,MONITOR_DECISION_QUALITY,Monitor sample\n",
                encoding="utf-8",
            )
            rows, paths = self.module.build_learning_ledger(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 19, 21, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.today_md.read_text(encoding="utf-8")

        self.assertEqual(len(rows), 1)
        self.assertIn("learning_family", csv_text)
        self.assertIn("ACTIONABLE_RESULT", csv_text)
        self.assertIn("# vSIGMA Learning Ledger", md_text)
        self.assertIn("predictive changes applied: NO", md_text)

    def test_empty_inputs_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            rows, paths = self.module.build_learning_ledger(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 19, 21, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.today_md.read_text(encoding="utf-8")

        self.assertEqual(rows, [])
        self.assertIn("target_date", csv_text)
        self.assertIn("rows reviewed: 0", md_text)


if __name__ == "__main__":
    unittest.main()
