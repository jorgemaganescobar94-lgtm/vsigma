from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class ImprovementProposalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_improvement_proposals")
        self.target_date = "2026-05-20"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_improvement_proposals"))
        self.assertTrue(hasattr(self.module, "build_proposals"))

    def test_waiting_prelock_generates_operational_proposal(self) -> None:
        pattern = {
            "pattern_id": "WAITING_PRELOCK_CLUSTER::WAITING_PRELOCK",
            "pattern_type": "WAITING_PRELOCK_CLUSTER",
            "pattern_key": "WAITING_PRELOCK",
            "severity": "P1",
            "sample_count": "4",
            "wins": "0",
            "losses": "0",
            "unresolved": "4",
            "markets": "OVER_1_5",
        }
        proposal = self.module.build_proposal(pattern, self.target_date, "2026-05-20T12:00:00+01:00")
        self.assertEqual(proposal["proposal_type"], "OPERATIONAL_PROPOSAL")
        self.assertEqual(proposal["proposal_status"], "PROPOSAL_ONLY")
        self.assertEqual(proposal["auto_apply"], "NO")
        self.assertEqual(proposal["priority"], "P1")
        self.assertIn("AUTO/PRELOCK", proposal["recommended_action"])

    def test_market_risk_cluster_generates_shadow_proposal(self) -> None:
        pattern = {
            "pattern_id": "MARKET_RISK_CLUSTER::OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
            "pattern_type": "MARKET_RISK_CLUSTER",
            "pattern_key": "OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
            "severity": "P2",
            "sample_count": "5",
            "wins": "1",
            "losses": "0",
            "unresolved": "4",
            "markets": "OVER_1_5",
        }
        proposal = self.module.build_proposal(pattern, self.target_date, "2026-05-20T12:00:00+01:00")
        self.assertEqual(proposal["proposal_type"], "MODEL_SHADOW_PROPOSAL")
        self.assertEqual(proposal["proposal_status"], "SHADOW_CANDIDATE_REQUIRED")
        self.assertEqual(proposal["next_engine"], "shadow_experiment_engine")
        self.assertEqual(proposal["auto_apply"], "NO")

    def test_unknown_or_unresolved_patterns_are_data_quality_not_shadow(self) -> None:
        patterns = [
            {
                "pattern_id": "MARKET_RISK_CLUSTER::UNKNOWN_MARKET::UNKNOWN_RISK",
                "pattern_type": "MARKET_RISK_CLUSTER",
                "pattern_key": "UNKNOWN_MARKET::UNKNOWN_RISK",
                "severity": "P1",
                "sample_count": "7",
                "wins": "0",
                "losses": "0",
                "unresolved": "7",
                "markets": "UNKNOWN",
            },
            {
                "pattern_id": "SAMPLE_KEY_CLUSTER::UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL",
                "pattern_type": "SAMPLE_KEY_CLUSTER",
                "pattern_key": "UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL",
                "severity": "P2",
                "sample_count": "7",
                "wins": "0",
                "losses": "0",
                "unresolved": "7",
                "markets": "OVER_1_5",
            },
        ]
        for pattern in patterns:
            proposal = self.module.build_proposal(pattern, self.target_date, "2026-05-20T12:00:00+01:00")
            self.assertEqual(proposal["proposal_type"], "DATA_QUALITY_PROPOSAL")
            self.assertEqual(proposal["proposal_status"], "PROPOSAL_ONLY")
            self.assertEqual(proposal["next_engine"], "data_quality_review")
            self.assertEqual(proposal["auto_apply"], "NO")
            self.assertIn("UNKNOWN/UNRESOLVED/NO_SIGNAL", proposal["recommended_action"])

    def test_unresolved_dominance_generates_data_quality_proposal(self) -> None:
        pattern = {
            "pattern_id": "UNRESOLVED_DOMINANCE::UNRESOLVED_RESULTS",
            "pattern_type": "UNRESOLVED_DOMINANCE",
            "pattern_key": "UNRESOLVED_RESULTS",
            "severity": "P2",
            "sample_count": "12",
            "wins": "0",
            "losses": "0",
            "unresolved": "12",
            "markets": "OVER_1_5",
        }
        proposal = self.module.build_proposal(pattern, self.target_date, "2026-05-20T12:00:00+01:00")
        self.assertEqual(proposal["proposal_type"], "DATA_QUALITY_PROPOSAL")
        self.assertEqual(proposal["proposal_status"], "PROPOSAL_ONLY")
        self.assertIn("UNKNOWN/UNRESOLVED/NO_SIGNAL", proposal["recommended_action"])

    def test_build_improvement_proposals_outputs_csv_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            governance_dir = processed_dir / "governance"
            today_dir = processed_dir / "today" / self.target_date
            governance_dir.mkdir(parents=True)
            today_dir.mkdir(parents=True)
            (today_dir / "vsigma_learning_patterns.csv").write_text(
                "target_date,pattern_id,pattern_type,pattern_key,severity,sample_count,wins,losses,voids,unresolved,markets\n"
                "2026-05-20,WAITING_PRELOCK_CLUSTER::WAITING_PRELOCK,WAITING_PRELOCK_CLUSTER,WAITING_PRELOCK,P1,4,0,0,0,4,OVER_1_5\n"
                "2026-05-20,MARKET_RISK_CLUSTER::OVER_1_5::FAILURE_MODE_LOW_CONVERSION,MARKET_RISK_CLUSTER,OVER_1_5::FAILURE_MODE_LOW_CONVERSION,P2,5,1,0,0,4,OVER_1_5\n"
                "2026-05-20,MARKET_RISK_CLUSTER::UNKNOWN_MARKET::UNKNOWN_RISK,MARKET_RISK_CLUSTER,UNKNOWN_MARKET::UNKNOWN_RISK,P1,7,0,0,0,7,UNKNOWN\n",
                encoding="utf-8",
            )
            proposals, paths = self.module.build_improvement_proposals(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.today_md.read_text(encoding="utf-8")

        self.assertEqual(len(proposals), 3)
        self.assertIn("OPERATIONAL_PROPOSAL", csv_text)
        self.assertIn("MODEL_SHADOW_PROPOSAL", csv_text)
        self.assertIn("DATA_QUALITY_PROPOSAL", csv_text)
        self.assertIn("auto_apply: NO", md_text)
        self.assertIn("predictive changes applied: NO", md_text)

    def test_empty_inputs_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            proposals, paths = self.module.build_improvement_proposals(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.governance_md.read_text(encoding="utf-8")

        self.assertEqual(proposals, [])
        self.assertIn("proposal_id", csv_text)
        self.assertIn("proposals generated: 0", md_text)


if __name__ == "__main__":
    unittest.main()
