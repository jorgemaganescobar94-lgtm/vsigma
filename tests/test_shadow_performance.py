from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class ShadowPerformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_shadow_performance")
        self.target_date = "2026-05-20"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_shadow_performance"))
        self.assertTrue(hasattr(self.module, "match_experiment_rows"))

    def test_matches_learning_rows_by_pattern_parts(self) -> None:
        experiment = {"source_pattern_key": "OVER_1_5::FAILURE_MODE_LOW_CONVERSION"}
        rows = [
            {
                "sample_key": "ACTIONABLE_RESULT::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::MONITOR_DECISION_QUALITY",
                "market_primary": "OVER_1_5",
                "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
                "improvement_signal": "MONITOR_DECISION_QUALITY",
                "learning_family": "ACTIONABLE_RESULT",
            },
            {
                "sample_key": "ACTIONABLE_RESULT::OVER_2_5::FAILURE_MODE_LOW_CONVERSION::MONITOR_DECISION_QUALITY",
                "market_primary": "OVER_2_5",
                "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
                "improvement_signal": "MONITOR_DECISION_QUALITY",
                "learning_family": "ACTIONABLE_RESULT",
            },
        ]
        matches = self.module.match_experiment_rows(experiment, rows)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["market_primary"], "OVER_1_5")

    def test_performance_row_requires_more_sample(self) -> None:
        experiment = {
            "experiment_id": "SHADOW::LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW::OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
            "experiment_type": "LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW",
            "source_pattern_key": "OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
            "shadow_status": "ACTIVE_SHADOW_ONLY",
            "baseline_policy": "CURRENT_PRODUCTION_LOGIC_UNCHANGED",
            "candidate_policy": "Shadow check",
        }
        learning_rows = [
            {
                "sample_key": "ACTIONABLE_RESULT::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::MONITOR_DECISION_QUALITY",
                "market_primary": "OVER_1_5",
                "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
                "improvement_signal": "MONITOR_DECISION_QUALITY",
                "learning_family": "ACTIONABLE_RESULT",
                "result_status": "WIN",
                "decision_quality_label": "ACTIONABLE_WIN",
            }
        ]
        row = self.module.build_performance_row(
            experiment, learning_rows, self.target_date, "2026-05-20T12:00:00+01:00"
        )
        self.assertEqual(row["matching_sample_count"], 1)
        self.assertEqual(row["closed_sample_count"], 1)
        self.assertEqual(row["wins"], 1)
        self.assertEqual(row["production_impact"], "NONE")
        self.assertEqual(row["auto_apply"], "NO")
        self.assertEqual(row["promotion_readiness"], "NOT_READY_SAMPLE_TOO_SMALL")

    def test_build_shadow_performance_outputs_csv_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            governance_dir = processed_dir / "governance"
            today_dir.mkdir(parents=True)
            governance_dir.mkdir(parents=True)

            (today_dir / "vsigma_shadow_experiments.csv").write_text(
                "target_date,experiment_id,experiment_type,source_pattern_key,shadow_status,baseline_policy,candidate_policy\n"
                "2026-05-20,SHADOW::LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW::OVER_1_5::FAILURE_MODE_LOW_CONVERSION,LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW,OVER_1_5::FAILURE_MODE_LOW_CONVERSION,ACTIVE_SHADOW_ONLY,CURRENT_PRODUCTION_LOGIC_UNCHANGED,Shadow policy\n",
                encoding="utf-8",
            )
            (today_dir / "vsigma_learning_ledger.csv").write_text(
                "target_date,fixture_id,market_primary,official_action,result_status,decision_quality_label,sample_key,accuracy_primary_risk,improvement_signal,learning_family\n"
                "2026-05-20,1,OVER_1_5,EXECUTABLE,WIN,ACTIONABLE_WIN,ACTIONABLE_RESULT::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::MONITOR_DECISION_QUALITY,FAILURE_MODE_LOW_CONVERSION,MONITOR_DECISION_QUALITY,ACTIONABLE_RESULT\n",
                encoding="utf-8",
            )

            rows, paths = self.module.build_shadow_performance(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.today_md.read_text(encoding="utf-8")

        self.assertEqual(len(rows), 1)
        self.assertIn("NOT_READY_SAMPLE_TOO_SMALL", csv_text)
        self.assertIn("production logic changed: NO", md_text)
        self.assertIn("promotion applied: NO", md_text)

    def test_empty_inputs_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            rows, paths = self.module.build_shadow_performance(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.governance_md.read_text(encoding="utf-8")

        self.assertEqual(rows, [])
        self.assertIn("experiment_id", csv_text)
        self.assertIn("experiments tracked: 0", md_text)


if __name__ == "__main__":
    unittest.main()
