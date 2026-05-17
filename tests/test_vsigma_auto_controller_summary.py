from __future__ import annotations

import importlib
import tempfile
import unittest
from pathlib import Path

import pandas as pd


class VsigmaAutoControllerSummaryTests(unittest.TestCase):
    def test_script_exists(self) -> None:
        self.assertTrue(Path("scripts/run_vsigma_auto_controller.py").exists())

    def test_import_does_not_execute_main(self) -> None:
        module = importlib.import_module("scripts.run_vsigma_auto_controller")
        self.assertTrue(hasattr(module, "map_decision_state"))
        self.assertTrue(hasattr(module, "build_decision_summary"))

    def test_decision_state_mapping(self) -> None:
        module = importlib.import_module("scripts.run_vsigma_auto_controller")
        self.assertEqual(
            module.map_decision_state("OUTSIDE_90_MIN_PRELOCK_WINDOW"),
            "WAITING_FOR_PRELOCK_WINDOW",
        )
        self.assertEqual(
            module.map_decision_state("IN_WINDOW_BUT_NOT_RETAINED"),
            "IN_WINDOW_BUT_BLOCKED",
        )
        self.assertEqual(
            module.map_decision_state("MISSING_KICKOFF_DATETIME"),
            "DATA_PROBLEM",
        )

    def test_summary_handles_empty_csvs_with_headers(self) -> None:
        module = importlib.import_module("scripts.run_vsigma_auto_controller")
        target_date = "2026-05-16"
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / target_date
            today_dir.mkdir(parents=True)

            pd.DataFrame(
                columns=[
                    "target_date",
                    "fixture_id",
                    "league",
                    "home_team",
                    "away_team",
                    "market_primary",
                    "competition_calibrated_prob",
                    "accuracy_confidence_score",
                    "accuracy_primary_risk",
                ]
            ).to_csv(today_dir / "vsigma_today_competition_top.csv", index=False)
            pd.DataFrame(columns=["target_date", "fixture_id", "market_primary", "prelock_decision"]).to_csv(
                today_dir / "vsigma_today_prelock_competition_top.csv",
                index=False,
            )
            pd.DataFrame(
                columns=[
                    "target_date",
                    "fixture_id",
                    "market_primary",
                    "exclusion_reason",
                    "next_action",
                ]
            ).to_csv(today_dir / "vsigma_prelock_exclusion_audit.csv", index=False)
            (today_dir / "vsigma_today_prelock_report.txt").write_text("Morning official picks reviewed: 0\n", encoding="utf-8")

            summary, paths = module.build_decision_summary(
                processed_dir=processed_dir,
                target_date=target_date,
                timezone_name="Atlantic/Canary",
                window_minutes=90,
            )

            self.assertTrue(paths["summary_csv"].exists())
            self.assertTrue(paths["summary_md"].exists())
            self.assertEqual(summary["decision_state"].tolist(), ["NO_BET"])


if __name__ == "__main__":
    unittest.main()
