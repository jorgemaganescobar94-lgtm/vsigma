from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class ShadowCandidateRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_shadow_candidates")
        self.target_date = "2026-05-21"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_shadow_candidates"))
        self.assertTrue(hasattr(self.module, "candidate_matches_experiment"))

    def test_candidate_matches_low_conversion_over15(self) -> None:
        candidate = {
            "market_primary": "OVER_1_5",
            "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
        }
        experiment = {
            "source_pattern_key": "OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
        }
        self.assertTrue(self.module.candidate_matches_experiment(candidate, experiment))

    def test_candidate_does_not_match_different_market(self) -> None:
        candidate = {
            "market_primary": "OVER_2_5",
            "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
        }
        experiment = {
            "source_pattern_key": "OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
        }
        self.assertFalse(self.module.candidate_matches_experiment(candidate, experiment))

    def test_build_shadow_candidates_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            governance_dir = processed_dir / "governance"
            today_dir.mkdir(parents=True)
            governance_dir.mkdir(parents=True)

            (today_dir / "vsigma_shadow_experiments.csv").write_text(
                "target_date,experiment_id,experiment_type,source_pattern_key,shadow_status,baseline_policy,candidate_policy\n"
                "2026-05-21,exp1,LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW,OVER_1_5::FAILURE_MODE_LOW_CONVERSION,ACTIVE_SHADOW_ONLY,CURRENT_PRODUCTION_LOGIC_UNCHANGED,Require stronger conversion evidence\n",
                encoding="utf-8",
            )
            (today_dir / "vsigma_today_prelock_competition_top.csv").write_text(
                "fixture_id,home_team,away_team,market_primary,final_recommendation,accuracy_primary_risk\n"
                "1,Flamengo,Estudiantes,OVER_1_5,BET,FAILURE_MODE_LOW_CONVERSION\n"
                "2,Gremio,Palestino,UNDER_3_5,BET,FAILURE_MODE_AVALANCHE_RISK\n",
                encoding="utf-8",
            )

            rows, paths = self.module.build_shadow_candidates(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 21, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )

            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.today_md.read_text(encoding="utf-8")

        self.assertEqual(len(rows), 1)
        self.assertIn("SHADOW_DOWNGRADE_REVIEW", csv_text)
        self.assertIn("official picks changed: NO", md_text)
        self.assertIn("production logic changed: NO", md_text)

    def test_empty_inputs_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            rows, paths = self.module.build_shadow_candidates(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 21, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.governance_md.read_text(encoding="utf-8")

        self.assertEqual(rows, [])
        self.assertIn("fixture_id", csv_text)
        self.assertIn("shadow_candidates: 0", md_text)


if __name__ == "__main__":
    unittest.main()
