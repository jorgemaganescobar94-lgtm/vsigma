from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class PromotionGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_promotion_gate")
        self.target_date = "2026-05-20"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_promotion_gate"))
        self.assertTrue(hasattr(self.module, "decision_for"))

    def test_not_ready_when_sample_too_small(self) -> None:
        row = {
            "closed_sample_count": "1",
            "wins": "1",
            "losses": "0",
            "promotion_readiness": "NOT_READY_SAMPLE_TOO_SMALL",
            "baseline_decision_quality": "BASELINE_POSITIVE_SIGNAL",
        }
        decision, reason, next_step = self.module.decision_for(row)
        self.assertEqual(decision, "NOT_READY_SAMPLE_TOO_SMALL")
        self.assertIn("minimum", reason)
        self.assertEqual(next_step, "COLLECT_MORE_CLOSED_SAMPLES")

    def test_rejected_when_losses_exceed_wins(self) -> None:
        row = {
            "closed_sample_count": "30",
            "wins": "10",
            "losses": "15",
            "promotion_readiness": "REVIEW_READY_REQUIRES_DEEP_AUDIT",
            "baseline_decision_quality": "BASELINE_MIXED_OR_UNKNOWN",
        }
        decision, _reason, next_step = self.module.decision_for(row)
        self.assertEqual(decision, "REJECTED_WEAK_SIGNAL")
        self.assertEqual(next_step, "KEEP_SHADOW_OR_REJECT")

    def test_candidate_review_only_when_sample_ready(self) -> None:
        row = {
            "closed_sample_count": "30",
            "wins": "25",
            "losses": "5",
            "promotion_readiness": "REVIEW_READY_BUT_NO_AUTO_PROMOTION",
            "baseline_decision_quality": "BASELINE_POSITIVE_SIGNAL",
        }
        decision, _reason, next_step = self.module.decision_for(row)
        self.assertEqual(decision, "PROMOTION_CANDIDATE_REVIEW_ONLY")
        self.assertEqual(next_step, "HUMAN_REVIEW_OR_SEPARATE_PROMOTION_PR")

    def test_build_promotion_gate_outputs_csv_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            (today_dir / "vsigma_shadow_performance.csv").write_text(
                "target_date,experiment_id,experiment_type,source_pattern_key,closed_sample_count,wins,losses,voids,baseline_decision_quality,shadow_performance_status,promotion_readiness\n"
                "2026-05-20,exp1,LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW,OVER_1_5::FAILURE_MODE_LOW_CONVERSION,1,1,0,0,BASELINE_POSITIVE_SIGNAL,TRACKING_ACTIVE_INSUFFICIENT_SAMPLE,NOT_READY_SAMPLE_TOO_SMALL\n",
                encoding="utf-8",
            )
            rows, paths = self.module.build_promotion_gate(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.today_md.read_text(encoding="utf-8")

        self.assertEqual(len(rows), 1)
        self.assertIn("NOT_READY_SAMPLE_TOO_SMALL", csv_text)
        self.assertIn("auto_promote: NO", md_text)
        self.assertIn("production_change: NO", md_text)

    def test_empty_inputs_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            rows, paths = self.module.build_promotion_gate(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.governance_md.read_text(encoding="utf-8")

        self.assertEqual(rows, [])
        self.assertIn("promotion_decision", csv_text)
        self.assertIn("experiments reviewed: 0", md_text)


if __name__ == "__main__":
    unittest.main()
