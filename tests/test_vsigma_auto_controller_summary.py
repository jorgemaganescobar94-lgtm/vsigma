from __future__ import annotations

import importlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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
        self.assertEqual(
            module.map_decision_state("", no_candidates=True),
            "NO_BET",
        )
        self.assertEqual(
            module.map_decision_state("", technical_warning=True),
            "TECHNICAL_WARNING",
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

    def test_summary_handles_missing_csvs(self) -> None:
        module = importlib.import_module("scripts.run_vsigma_auto_controller")
        target_date = "2026-05-16"
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"

            summary, paths = module.build_decision_summary(
                processed_dir=processed_dir,
                target_date=target_date,
                timezone_name="Atlantic/Canary",
                window_minutes=90,
            )

            self.assertTrue(paths["summary_csv"].exists())
            self.assertTrue(paths["summary_md"].exists())
            self.assertEqual(summary["decision_state"].tolist(), ["NO_BET"])
            self.assertIn("## Technical Warnings", paths["summary_md"].read_text(encoding="utf-8"))

    def test_past_target_date_skips_pre_recovery(self) -> None:
        module = importlib.import_module("scripts.run_vsigma_auto_controller")
        target_date = "2026-05-16"
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            calls: list[tuple[str, list[str], bool]] = []

            def fake_run_step(script_path: str, args: list[str], allow_failure: bool = False):
                calls.append((script_path, args, allow_failure))
                return module.StepResult(script_path, args, 0)

            with (
                patch.object(module, "today_in_timezone", return_value="2026-05-17"),
                patch.object(module, "detect_pre_refresh_needed", return_value=["stale rows"]),
                patch.object(module, "run_step", side_effect=fake_run_step),
            ):
                result = module.run_auto_controller(target_date, "Atlantic/Canary", 90, processed_dir)

            scripts_called = [call[0] for call in calls]
            self.assertNotIn("scripts/run_daily_competition_controller.py", scripts_called)
            self.assertEqual(result.technical_warnings.pre_refresh_skipped_reason, "PAST_TARGET_DATE")
            self.assertTrue(result.summary_paths["summary_md"].exists())
            self.assertEqual(result.summary["decision_state"].tolist(), ["PAST_DATE_NO_PRE_REFRESH"])

    def test_best_effort_pre_failure_still_generates_summary(self) -> None:
        module = importlib.import_module("scripts.run_vsigma_auto_controller")
        target_date = "2026-05-16"
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
                        "market_primary": "HOME_WIN",
                    }
                ]
            ).to_csv(today_dir / "vsigma_today_competition_top.csv", index=False)

            def fake_run_step(script_path: str, args: list[str], allow_failure: bool = False):
                if script_path == "scripts/run_daily_competition_controller.py":
                    return module.StepResult(script_path, args, 1, "simulated pre failure")
                return module.StepResult(script_path, args, 0)

            with (
                patch.object(module, "today_in_timezone", return_value=target_date),
                patch.object(module, "detect_pre_refresh_needed", return_value=["stale rows"]),
                patch.object(module, "run_step", side_effect=fake_run_step),
            ):
                result = module.run_auto_controller(target_date, "Atlantic/Canary", 90, processed_dir)

            self.assertTrue(result.summary_paths["summary_csv"].exists())
            self.assertTrue(result.summary_paths["summary_md"].exists())
            self.assertTrue(result.technical_warnings.pre_refresh_attempted)
            self.assertTrue(result.technical_warnings.pre_refresh_failed)
            self.assertEqual(result.summary["decision_state"].tolist(), ["TECHNICAL_WARNING"])


if __name__ == "__main__":
    unittest.main()
