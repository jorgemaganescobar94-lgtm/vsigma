from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class ShadowExperimentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_shadow_experiments")
        self.target_date = "2026-05-20"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_shadow_experiments"))
        self.assertTrue(hasattr(self.module, "is_shadow_eligible"))

    def test_clean_model_shadow_proposal_is_eligible(self) -> None:
        proposal = {
            "proposal_type": "MODEL_SHADOW_PROPOSAL",
            "proposal_status": "SHADOW_CANDIDATE_REQUIRED",
            "auto_apply": "NO",
            "source_pattern_key": "OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
        }
        self.assertTrue(self.module.is_shadow_eligible(proposal))

    def test_unknown_or_unresolved_proposals_are_not_eligible(self) -> None:
        proposals = [
            {
                "proposal_type": "MODEL_SHADOW_PROPOSAL",
                "proposal_status": "SHADOW_CANDIDATE_REQUIRED",
                "auto_apply": "NO",
                "source_pattern_key": "UNKNOWN_MARKET::UNKNOWN_RISK",
            },
            {
                "proposal_type": "MODEL_SHADOW_PROPOSAL",
                "proposal_status": "SHADOW_CANDIDATE_REQUIRED",
                "auto_apply": "NO",
                "source_pattern_key": "UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL",
            },
            {
                "proposal_type": "DATA_QUALITY_PROPOSAL",
                "proposal_status": "PROPOSAL_ONLY",
                "auto_apply": "NO",
                "source_pattern_key": "UNKNOWN_MARKET::UNKNOWN_RISK",
            },
        ]
        for proposal in proposals:
            self.assertFalse(self.module.is_shadow_eligible(proposal))

    def test_operational_patterns_are_not_shadow_eligible(self) -> None:
        proposals = [
            {
                "proposal_type": "MODEL_SHADOW_PROPOSAL",
                "proposal_status": "SHADOW_CANDIDATE_REQUIRED",
                "auto_apply": "NO",
                "source_pattern_key": "WAITING_PRELOCK::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::WAIT_FOR_POST_RESULTS",
            },
            {
                "proposal_type": "MODEL_SHADOW_PROPOSAL",
                "proposal_status": "SHADOW_CANDIDATE_REQUIRED",
                "auto_apply": "NO",
                "source_pattern_key": "EXPIRED_PRELOCK::OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
            },
            {
                "proposal_type": "MODEL_SHADOW_PROPOSAL",
                "proposal_status": "SHADOW_CANDIDATE_REQUIRED",
                "auto_apply": "NO",
                "source_pattern_key": "DATA_BLOCKED::OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
            },
        ]
        for proposal in proposals:
            self.assertFalse(self.module.is_shadow_eligible(proposal))

    def test_build_experiment_for_low_conversion_over15(self) -> None:
        proposal = {
            "proposal_id": "MODEL_SHADOW_PROPOSAL::MARKET_RISK_CLUSTER::OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
            "proposal_type": "MODEL_SHADOW_PROPOSAL",
            "proposal_status": "SHADOW_CANDIDATE_REQUIRED",
            "auto_apply": "NO",
            "source_pattern_type": "MARKET_RISK_CLUSTER",
            "source_pattern_key": "OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
        }
        experiment = self.module.build_experiment(proposal, self.target_date, "2026-05-20T12:00:00+01:00")
        self.assertEqual(experiment["experiment_type"], "LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW")
        self.assertEqual(experiment["shadow_status"], "ACTIVE_SHADOW_ONLY")
        self.assertEqual(experiment["production_impact"], "NONE")
        self.assertEqual(experiment["auto_apply"], "NO")
        self.assertIn("CURRENT_PRODUCTION_LOGIC_UNCHANGED", experiment["baseline_policy"])

    def test_build_shadow_experiments_outputs_csv_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            (today_dir / "vsigma_improvement_proposals.csv").write_text(
                "target_date,proposal_id,source_pattern_type,source_pattern_key,proposal_type,proposal_status,auto_apply\n"
                "2026-05-20,MODEL_SHADOW_PROPOSAL::MARKET_RISK_CLUSTER::OVER_1_5::FAILURE_MODE_LOW_CONVERSION,MARKET_RISK_CLUSTER,OVER_1_5::FAILURE_MODE_LOW_CONVERSION,MODEL_SHADOW_PROPOSAL,SHADOW_CANDIDATE_REQUIRED,NO\n"
                "2026-05-20,DATA_QUALITY_PROPOSAL::MARKET_RISK_CLUSTER::UNKNOWN_MARKET::UNKNOWN_RISK,MARKET_RISK_CLUSTER,UNKNOWN_MARKET::UNKNOWN_RISK,DATA_QUALITY_PROPOSAL,PROPOSAL_ONLY,NO\n",
                encoding="utf-8",
            )
            experiments, paths = self.module.build_shadow_experiments(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.today_md.read_text(encoding="utf-8")

        self.assertEqual(len(experiments), 1)
        self.assertIn("LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW", csv_text)
        self.assertIn("production logic changed: NO", md_text)
        self.assertIn("official picks changed: NO", md_text)

    def test_empty_inputs_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            experiments, paths = self.module.build_shadow_experiments(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.governance_md.read_text(encoding="utf-8")

        self.assertEqual(experiments, [])
        self.assertIn("experiment_id", csv_text)
        self.assertIn("shadow_experiments: 0", md_text)


if __name__ == "__main__":
    unittest.main()
