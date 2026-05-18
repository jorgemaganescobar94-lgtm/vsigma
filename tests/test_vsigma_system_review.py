from __future__ import annotations

import importlib
import tempfile
import unittest
from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = [
    "target_date",
    "priority",
    "category",
    "title",
    "reason",
    "expected_impact",
    "risk",
    "recommended_action",
    "apply_now",
    "evidence",
]


class VsigmaSystemReviewTests(unittest.TestCase):
    def test_import_does_not_execute_main(self) -> None:
        module = importlib.import_module("scripts.build_vsigma_system_review")
        self.assertTrue(hasattr(module, "build_system_review"))
        self.assertTrue(hasattr(module, "parse_args"))

    def test_generates_review_with_minimal_empty_inputs(self) -> None:
        module = importlib.import_module("scripts.build_vsigma_system_review")
        target_date = "2026-05-18"
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / target_date
            ledger_dir = processed_dir / "ledger"
            today_dir.mkdir(parents=True)
            ledger_dir.mkdir(parents=True)

            pd.DataFrame(
                [
                    {
                        "target_date": target_date,
                        "fixture_id": "",
                        "league": "",
                        "home_team": "",
                        "away_team": "",
                        "market_primary": "",
                        "decision_state": "NO_BET",
                        "exclusion_reason": "",
                        "next_action": "NO_ACTION",
                    }
                ]
            ).to_csv(today_dir / "vsigma_cloud_decision_summary.csv", index=False)
            (today_dir / "vsigma_cloud_decision_summary.md").write_text(
                "\n".join(
                    [
                        "# vSIGMA Cloud Decision Summary - 2026-05-18",
                        "- Auto status: NO_BET",
                        "- Candidates reviewed: 0",
                        "- Executable picks: 0",
                        "- Waiting picks: 0",
                        "- Blocked picks: 0",
                        "- healthcheck_status: OK",
                    ]
                ),
                encoding="utf-8",
            )
            pd.DataFrame(columns=["target_date", "record_status"]).to_csv(
                ledger_dir / "vsigma_immutable_daily_pick_ledger.csv",
                index=False,
            )

            review, paths = module.build_system_review(target_date, "Atlantic/Canary", processed_dir)

            self.assertTrue(paths.governance_md.exists())
            self.assertTrue(paths.governance_csv.exists())
            self.assertTrue(paths.today_md.exists())
            self.assertFalse(review.empty)
            self.assertIn("## Executive Status", paths.today_md.read_text(encoding="utf-8"))

    def test_csv_has_expected_columns(self) -> None:
        module = importlib.import_module("scripts.build_vsigma_system_review")
        target_date = "2026-05-18"
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            review, paths = module.build_system_review(target_date, "Atlantic/Canary", processed_dir)
            written = pd.read_csv(paths.governance_csv)

            self.assertEqual(list(review.columns), EXPECTED_COLUMNS)
            self.assertEqual(list(written.columns), EXPECTED_COLUMNS)

    def test_missing_optional_files_do_not_fail(self) -> None:
        module = importlib.import_module("scripts.build_vsigma_system_review")
        target_date = "2026-05-18"
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / target_date
            today_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {
                        "target_date": target_date,
                        "fixture_id": "123",
                        "league": "Test League",
                        "home_team": "Home",
                        "away_team": "Away",
                        "market_primary": "OVER_1_5",
                        "decision_state": "PRELOCK_BLOCKED",
                        "exclusion_reason": "PRELOCK_NOT_AVAILABLE",
                        "next_action": "WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW",
                    }
                ]
            ).to_csv(today_dir / "vsigma_cloud_decision_summary.csv", index=False)

            review, paths = module.build_system_review(target_date, "Atlantic/Canary", processed_dir)

            self.assertTrue(paths.today_md.exists())
            self.assertIn("missing optional inputs:", paths.today_md.read_text(encoding="utf-8"))
            self.assertIn("P3", review["priority"].tolist())


if __name__ == "__main__":
    unittest.main()
