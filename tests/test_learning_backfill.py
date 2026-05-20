from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class LearningBackfillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_learning_backfill")

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_learning_backfill"))
        self.assertTrue(hasattr(self.module, "load_historical_inputs"))

    def test_collects_dates_from_multiple_sources(self) -> None:
        rows = [
            {"target_date": "2026-05-18"},
            {"date": "2026-05-19T20:00:00+01:00"},
            {"fixture_date": "not-a-date"},
            {"match_date": "2026-05-20"},
        ]
        self.assertEqual(self.module.collect_dates(rows), ["2026-05-18", "2026-05-19", "2026-05-20"])

    def test_backfills_multiple_dates_and_dedupes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            ledger_dir = processed_dir / "ledger"
            today_18 = processed_dir / "today" / "2026-05-18"
            today_19 = processed_dir / "today" / "2026-05-19"
            ledger_dir.mkdir(parents=True)
            today_18.mkdir(parents=True)
            today_19.mkdir(parents=True)

            (ledger_dir / "vsigma_decision_outcome_ledger.csv").write_text(
                "target_date,fixture_id,league,home_team,away_team,market_primary,official_action,executable_now,final_block_reason,execution_family_status,is_actionable,is_non_actionable,is_expired\n"
                "2026-05-18,111,League A,A,B,OVER_1_5,NO_BET,NO,KICKOFF_ALREADY_PASSED,EXPIRED,NO,YES,YES\n"
                "2026-05-19,222,League B,C,D,OVER_2_5,EXECUTABLE,YES,NONE,PRELOCK_CONFIRMED,YES,NO,NO\n",
                encoding="utf-8",
            )
            (today_18 / "vsigma_decision_quality_review.csv").write_text(
                "target_date,fixture_id,market_primary,result_status,decision_quality_label,quality_bucket,improvement_signal,recommended_followup\n"
                "2026-05-18,111,OVER_1_5,UNRESOLVED,EXPIRED_PRELOCK_UNRESOLVED,NEEDS_MORE_DATA,REVIEW_AUTO_TIMING,Review timing\n",
                encoding="utf-8",
            )
            (today_19 / "vsigma_decision_quality_review.csv").write_text(
                "target_date,fixture_id,market_primary,result_status,decision_quality_label,quality_bucket,improvement_signal,recommended_followup\n"
                "2026-05-19,222,OVER_2_5,WIN,ACTIONABLE_WIN,GOOD_DECISION,MONITOR_DECISION_QUALITY,Monitor\n",
                encoding="utf-8",
            )

            rows, paths = self.module.build_learning_backfill(
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.all_csv.read_text(encoding="utf-8")
            md_text = paths.all_md.read_text(encoding="utf-8")

        self.assertEqual(len(rows), 2)
        self.assertIn("EXPIRED_PRELOCK", csv_text)
        self.assertIn("ACTIONABLE_RESULT", csv_text)
        self.assertIn("source_dates_seen", csv_text)
        self.assertIn("rows reviewed: 2", md_text)
        self.assertIn("predictive changes applied: NO", md_text)

    def test_empty_inputs_generate_empty_backfill_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            rows, paths = self.module.build_learning_backfill(
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.all_csv.read_text(encoding="utf-8")
            md_text = paths.report_md.read_text(encoding="utf-8")

        self.assertEqual(rows, [])
        self.assertIn("target_date", csv_text)
        self.assertIn("rows reviewed: 0", md_text)


if __name__ == "__main__":
    unittest.main()
