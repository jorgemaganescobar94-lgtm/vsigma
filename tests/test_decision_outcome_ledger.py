from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


class DecisionOutcomeLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.update_vsigma_decision_outcome_ledger")
        self.target_date = "2026-05-18"
        self.tz = ZoneInfo("Atlantic/Canary")

    def write_inputs(
        self,
        today_dir: Path,
        *,
        fixture_id: str = "123",
        official_action: str = "EXECUTABLE",
        executable_now: str = "YES",
        final_block_reason: str = "NONE",
        execution_family_status: str = "PRELOCK_CONFIRMED",
    ) -> None:
        base = {
            "target_date": self.target_date,
            "fixture_id": fixture_id,
            "league": "Test League",
            "home_team": "Home",
            "away_team": "Away",
            "market_primary": "OVER_1_5",
            "competition_calibrated_prob": 0.71,
            "accuracy_confidence_score": 123.4,
            "accuracy_primary_risk": "LOW_RISK",
        }
        pd.DataFrame([{**base, "run_id": "run-1"}]).to_csv(today_dir / "vsigma_today_competition_top.csv", index=False)
        pd.DataFrame(
            [
                {
                    **base,
                    "official_action": official_action,
                    "executable_now": executable_now,
                    "final_block_reason": final_block_reason,
                    "retry_allowed": "NO",
                    "next_retry_time": "",
                    "execution_family_status": execution_family_status,
                    "decision_state": execution_family_status,
                }
            ]
        ).to_csv(today_dir / "vsigma_cloud_decision_summary.csv", index=False)
        pd.DataFrame(
            [
                {
                    **base,
                    "generated_at": "2026-05-18T12:00:00+01:00",
                    "official_action": official_action,
                    "executable_now": executable_now,
                    "final_block_reason": final_block_reason,
                    "retry_allowed": "NO",
                    "next_retry_time": "",
                    "data_gap_flags": "",
                    "execution_family_status": execution_family_status,
                    "decision_source": "test",
                }
            ]
        ).to_csv(today_dir / "vsigma_prelock_decision_resolver.csv", index=False)

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "update_decision_outcome_ledger"))
        self.assertTrue(hasattr(self.module, "parse_args"))

    def test_ledger_id_is_stable(self) -> None:
        first = self.module.ledger_id_for(self.target_date, "123", "OVER_1_5", "NO_BET")
        second = self.module.ledger_id_for(self.target_date, "123", "over_1_5", "no_bet")
        self.assertEqual(first, second)
        self.assertEqual(first, "2026-05-18::123::OVER_1_5::NO_BET")

    def test_update_replaces_existing_ledger_id_without_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            self.write_inputs(today_dir, official_action="EXECUTABLE", executable_now="YES")

            first, paths = self.module.update_decision_outcome_ledger(
                target_date=self.target_date,
                timezone_name="Atlantic/Canary",
                processed_dir=processed_dir,
                now=datetime(2026, 5, 18, 12, 0, tzinfo=self.tz),
            )
            second, _paths = self.module.update_decision_outcome_ledger(
                target_date=self.target_date,
                timezone_name="Atlantic/Canary",
                processed_dir=processed_dir,
                now=datetime(2026, 5, 18, 12, 5, tzinfo=self.tz),
            )

            written = pd.read_csv(paths.csv_path)

        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.assertEqual(len(written), 1)
        self.assertEqual(written["ledger_id"].nunique(), 1)

    def test_executable_is_actionable(self) -> None:
        row = self.module.classify_row("EXECUTABLE", "YES", "NONE", "PRELOCK_CONFIRMED")
        self.assertEqual(row["is_actionable"], "YES")
        self.assertEqual(row["is_non_actionable"], "NO")

    def test_no_bet_expired_is_expired_and_not_actionable(self) -> None:
        row = self.module.classify_row("NO_BET", "NO", "KICKOFF_ALREADY_PASSED", "EXPIRED")
        self.assertEqual(row["is_expired"], "YES")
        self.assertEqual(row["is_actionable"], "NO")
        self.assertEqual(row["is_non_actionable"], "YES")

    def test_wait_is_waiting(self) -> None:
        row = self.module.classify_row("WAIT", "NO", "OUTSIDE_PRELOCK_WINDOW", "WAITING_FOR_WINDOW")
        self.assertEqual(row["is_waiting"], "YES")
        self.assertEqual(row["is_actionable"], "NO")

    def test_technical_review_is_technical_review(self) -> None:
        row = self.module.classify_row("TECHNICAL_REVIEW", "NO", "PRELOCK_STATE_UNCLASSIFIED", "TECHNICAL_REVIEW")
        self.assertEqual(row["is_technical_review"], "YES")
        self.assertEqual(row["is_actionable"], "NO")


if __name__ == "__main__":
    unittest.main()
