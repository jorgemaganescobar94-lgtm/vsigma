from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class LearningAutopilotAlertTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.dispatch_learning_autopilot_alerts")
        self.target_date = "2026-05-20"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_learning_autopilot_alerts"))
        self.assertTrue(hasattr(self.module, "promotion_alerts"))

    def test_not_ready_promotion_does_not_alert(self) -> None:
        rows = [
            {
                "promotion_decision": "NOT_READY_SAMPLE_TOO_SMALL",
                "experiment_type": "LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW",
                "experiment_id": "exp1",
                "closed_sample_count": "1",
                "wins": "1",
                "losses": "0",
            }
        ]
        alerts = self.module.promotion_alerts(self.target_date, "2026-05-20T12:00:00+01:00", rows, "")
        self.assertEqual(alerts, [])

    def test_review_candidate_promotion_alerts(self) -> None:
        rows = [
            {
                "promotion_decision": "PROMOTION_CANDIDATE_REVIEW_ONLY",
                "experiment_type": "LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW",
                "experiment_id": "exp1",
                "closed_sample_count": "30",
                "wins": "25",
                "losses": "5",
            }
        ]
        alerts = self.module.promotion_alerts(self.target_date, "2026-05-20T12:00:00+01:00", rows, "https://example.test/run")
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["alert_type"], "PROMOTION_REVIEW_REQUIRED")
        self.assertEqual(alerts[0]["severity"], "P1")
        self.assertEqual(alerts[0]["auto_apply"], "NO")
        self.assertEqual(alerts[0]["production_change"], "NO")

    def test_operational_and_data_quality_proposals_alert(self) -> None:
        rows = [
            {
                "proposal_type": "OPERATIONAL_PROPOSAL",
                "proposal_status": "PROPOSAL_ONLY",
                "priority": "P1",
                "source_pattern_key": "WAITING_PRELOCK",
                "recommended_action": "Review AUTO/PRELOCK schedule",
            },
            {
                "proposal_type": "DATA_QUALITY_PROPOSAL",
                "proposal_status": "PROPOSAL_ONLY",
                "priority": "P2",
                "source_pattern_key": "UNRESOLVED_RESULTS",
                "recommended_action": "Improve post-results labeling",
            },
            {
                "proposal_type": "MODEL_SHADOW_PROPOSAL",
                "proposal_status": "SHADOW_CANDIDATE_REQUIRED",
                "priority": "P1",
                "source_pattern_key": "OVER_1_5::FAILURE_MODE_LOW_CONVERSION",
                "recommended_action": "Create shadow-only candidate",
            },
        ]
        alerts = self.module.proposal_alerts(self.target_date, "2026-05-20T12:00:00+01:00", rows, "")
        self.assertEqual(len(alerts), 2)
        self.assertEqual({alert["alert_type"] for alert in alerts}, {"OPERATIONAL_REVIEW_REQUIRED", "DATA_QUALITY_REVIEW_REQUIRED"})

    def test_consolidates_data_quality_alerts_by_category(self) -> None:
        rows = [
            {
                "proposal_type": "DATA_QUALITY_PROPOSAL",
                "proposal_status": "PROPOSAL_ONLY",
                "priority": "P2",
                "source_pattern_key": "UNKNOWN_MARKET::UNKNOWN_RISK",
                "recommended_action": "Improve data quality",
            },
            {
                "proposal_type": "DATA_QUALITY_PROPOSAL",
                "proposal_status": "PROPOSAL_ONLY",
                "priority": "P2",
                "source_pattern_key": "UNRESOLVED_RESULTS",
                "recommended_action": "Improve post-results labeling",
            },
        ]
        raw = self.module.proposal_alerts(
            self.target_date,
            "2026-05-20T12:00:00+01:00",
            rows,
            "",
        )
        consolidated = self.module.consolidate_alerts(
            raw,
            self.target_date,
            "2026-05-20T12:00:00+01:00",
        )
        self.assertEqual(len(consolidated), 1)
        self.assertEqual(consolidated[0]["alert_type"], "DATA_QUALITY_REVIEW_REQUIRED")
        self.assertIn("UNKNOWN_MARKET::UNKNOWN_RISK", consolidated[0]["source_key"])
        self.assertIn("UNRESOLVED_RESULTS", consolidated[0]["source_key"])

    def test_build_learning_autopilot_alerts_outputs_csv_and_markdown_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            (today_dir / "vsigma_improvement_proposals.csv").write_text(
                "target_date,proposal_id,source_pattern_key,proposal_type,proposal_status,priority,recommended_action\n"
                "2026-05-20,p1,WAITING_PRELOCK,OPERATIONAL_PROPOSAL,PROPOSAL_ONLY,P1,Review timing\n",
                encoding="utf-8",
            )
            (today_dir / "vsigma_promotion_gate.csv").write_text(
                "target_date,experiment_id,experiment_type,promotion_decision,closed_sample_count,wins,losses\n"
                "2026-05-20,exp1,LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW,NOT_READY_SAMPLE_TOO_SMALL,1,1,0\n",
                encoding="utf-8",
            )
            alerts, paths = self.module.build_learning_autopilot_alerts(
                self.target_date,
                processed_dir=processed_dir,
                repo="owner/repo",
                run_url="https://example.test/run",
                dry_run=True,
                dispatch=True,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.today_md.read_text(encoding="utf-8")

        self.assertEqual(len(alerts), 1)
        self.assertIn("OPERATIONAL_REVIEW_REQUIRED", csv_text)
        self.assertIn("DRY_RUN", csv_text)
        self.assertIn("alerts generated: 1", md_text)
        self.assertIn("auto_apply: NO", md_text)

    def test_empty_inputs_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            alerts, paths = self.module.build_learning_autopilot_alerts(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.governance_md.read_text(encoding="utf-8")

        self.assertEqual(alerts, [])
        self.assertIn("alert_id", csv_text)
        self.assertIn("alerts generated: 0", md_text)


if __name__ == "__main__":
    unittest.main()
