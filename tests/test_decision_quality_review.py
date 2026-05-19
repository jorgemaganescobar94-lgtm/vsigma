from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


class DecisionQualityReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_decision_quality_review")
        self.target_date = "2026-05-18"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_decision_quality_review"))
        self.assertTrue(hasattr(self.module, "parse_args"))

    def test_executable_win_is_good(self) -> None:
        label, bucket = self.module.classify_decision_quality(official_action="EXECUTABLE", result_status="WIN")
        self.assertEqual(label, "ACTIONABLE_WIN")
        self.assertEqual(bucket, "GOOD_DECISION")

    def test_executable_loss_is_bad(self) -> None:
        label, bucket = self.module.classify_decision_quality(official_action="EXECUTABLE", result_status="LOSS")
        self.assertEqual(label, "ACTIONABLE_LOSS")
        self.assertEqual(bucket, "BAD_DECISION")

    def test_no_bet_win_is_missed_win(self) -> None:
        label, bucket = self.module.classify_decision_quality(official_action="NO_BET", result_status="WIN")
        self.assertEqual(label, "NO_BET_MISSED_WIN")
        self.assertEqual(bucket, "BAD_DECISION")

    def test_no_bet_loss_is_correct_avoided_loss(self) -> None:
        label, bucket = self.module.classify_decision_quality(official_action="NO_BET", result_status="LOSS")
        self.assertEqual(label, "NO_BET_CORRECT_AVOIDED_LOSS")
        self.assertEqual(bucket, "GOOD_DECISION")

    def test_expired_prelock_win_is_not_predictive_missed_win(self) -> None:
        label, bucket = self.module.classify_decision_quality(
            official_action="NO_BET",
            result_status="WIN",
            final_block_reason="KICKOFF_ALREADY_PASSED",
            execution_family_status="EXPIRED",
        )
        self.assertEqual(label, "EXPIRED_PRELOCK_RESULT_WIN")
        self.assertEqual(bucket, "NEUTRAL_OR_UNRESOLVED")

    def test_missing_result_needs_more_data(self) -> None:
        label, bucket = self.module.classify_decision_quality(official_action="EXECUTABLE", result_status="")
        self.assertEqual(label, "ACTIONABLE_UNRESOLVED")
        self.assertEqual(bucket, "NEEDS_MORE_DATA")

    def test_build_maps_ledger_to_labeled_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            ledger_dir = processed_dir / "ledger"
            today_dir = processed_dir / "today" / self.target_date
            ledger_dir.mkdir(parents=True)
            today_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {
                        "ledger_id": "2026-05-18::123::OVER_1_5::EXECUTABLE",
                        "target_date": self.target_date,
                        "fixture_id": "123",
                        "league": "Test League",
                        "home_team": "Home",
                        "away_team": "Away",
                        "market_primary": "OVER_1_5",
                        "official_action": "EXECUTABLE",
                        "executable_now": "YES",
                        "final_block_reason": "NONE",
                        "execution_family_status": "PRELOCK_CONFIRMED",
                        "is_actionable": "YES",
                        "is_non_actionable": "NO",
                        "is_expired": "NO",
                        "competition_calibrated_prob": 0.71,
                        "accuracy_confidence_score": 100.0,
                        "accuracy_primary_risk": "LOW_RISK",
                    }
                ]
            ).to_csv(ledger_dir / "vsigma_decision_outcome_ledger.csv", index=False)
            pd.DataFrame(
                [
                    {
                        "target_date": self.target_date,
                        "fixture_id": "123",
                        "market_primary": "OVER_1_5",
                        "primary_result": "WIN",
                    }
                ]
            ).to_csv(today_dir / "vsigma_market_results_labeled.csv", index=False)

            review, paths = self.module.build_decision_quality_review(
                self.target_date,
                "Atlantic/Canary",
                processed_dir,
                now=datetime(2026, 5, 18, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )

            self.assertTrue(paths.governance_csv.exists())
            self.assertEqual(len(review), 1)
            self.assertEqual(review.iloc[0]["decision_quality_label"], "ACTIONABLE_WIN")
            self.assertEqual(review.iloc[0]["quality_bucket"], "GOOD_DECISION")

    def test_expired_daily_review_classifies_operational_no_bet_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            ledger_dir = processed_dir / "ledger"
            today_dir = processed_dir / "today" / self.target_date
            ledger_dir.mkdir(parents=True)
            today_dir.mkdir(parents=True)
            row = {
                "ledger_id": "2026-05-18::1392197::OVER_1_5::NO_BET",
                "target_date": self.target_date,
                "fixture_id": "1392197",
                "league": "Segunda",
                "home_team": "Leganes",
                "away_team": "Huesca",
                "market_primary": "OVER_1_5",
                "official_action": "NO_BET",
                "executable_now": "NO",
                "final_block_reason": "KICKOFF_ALREADY_PASSED",
                "execution_family_status": "EXPIRED",
                "is_actionable": "NO",
                "is_non_actionable": "YES",
                "is_expired": "YES",
                "is_waiting": "NO",
                "is_blocked": "NO",
                "is_technical_review": "NO",
            }
            pd.DataFrame([row]).to_csv(ledger_dir / "vsigma_decision_outcome_ledger.csv", index=False)
            pd.DataFrame([row | {"minutes_to_kickoff": -120.25, "decision_state": "POST_PENDING"}]).to_csv(
                today_dir / "vsigma_cloud_decision_summary.csv",
                index=False,
            )
            pd.DataFrame([row | {"minutes_to_kickoff": -120.25}]).to_csv(
                today_dir / "vsigma_prelock_decision_resolver.csv",
                index=False,
            )

            review, paths = self.module.build_decision_quality_review(
                self.target_date,
                "Atlantic/Canary",
                processed_dir,
                now=datetime(2026, 5, 18, 21, 46, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            markdown = paths.today_md.read_text(encoding="utf-8")

        self.assertEqual(len(review), 1)
        self.assertEqual(review.loc[0, "decision_quality_label"], "EXPIRED_PRELOCK_UNRESOLVED")
        self.assertIn("- daily_classification: EXPIRED_PRELOCK", markdown)
        self.assertIn("- no_bet_classification: NO_BET_VALID", markdown)
        self.assertIn("- operational_verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA", markdown)
        self.assertIn("not a predictive failure", markdown.lower())

    def test_empty_csvs_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            ledger_dir = processed_dir / "ledger"
            today_dir = processed_dir / "today" / self.target_date
            ledger_dir.mkdir(parents=True)
            today_dir.mkdir(parents=True)
            pd.DataFrame(columns=["target_date", "fixture_id", "market_primary"]).to_csv(
                ledger_dir / "vsigma_decision_outcome_ledger.csv",
                index=False,
            )
            pd.DataFrame(columns=["target_date", "fixture_id", "market_primary", "primary_result"]).to_csv(
                today_dir / "vsigma_market_results_labeled.csv",
                index=False,
            )

            review, paths = self.module.build_decision_quality_review(
                self.target_date,
                "Atlantic/Canary",
                processed_dir,
                now=datetime(2026, 5, 18, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )

            self.assertTrue(paths.today_md.exists())
            self.assertTrue(review.empty)
            self.assertEqual(list(review.columns), self.module.OUTPUT_COLUMNS)


if __name__ == "__main__":
    unittest.main()
