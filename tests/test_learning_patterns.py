from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class LearningPatternMinerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.build_learning_patterns")
        self.target_date = "2026-05-20"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "build_learning_patterns"))
        self.assertTrue(hasattr(self.module, "mine_patterns"))

    def test_detects_sample_key_cluster(self) -> None:
        rows = [
            {"target_date": self.target_date, "fixture_id": "1", "market_primary": "OVER_1_5", "official_action": "NO_BET", "result_status": "UNRESOLVED", "learning_family": "WAITING_PRELOCK", "learning_status": "COLLECT_MORE_SAMPLE", "sample_key": "WAITING_PRELOCK::OVER_1_5::LOW_CONVERSION::WAIT_FOR_POST_RESULTS", "accuracy_primary_risk": "LOW_CONVERSION", "improvement_signal": "WAIT_FOR_POST_RESULTS"},
            {"target_date": self.target_date, "fixture_id": "2", "market_primary": "OVER_1_5", "official_action": "NO_BET", "result_status": "UNRESOLVED", "learning_family": "WAITING_PRELOCK", "learning_status": "COLLECT_MORE_SAMPLE", "sample_key": "WAITING_PRELOCK::OVER_1_5::LOW_CONVERSION::WAIT_FOR_POST_RESULTS", "accuracy_primary_risk": "LOW_CONVERSION", "improvement_signal": "WAIT_FOR_POST_RESULTS"},
        ]
        patterns = self.module.mine_patterns(rows, self.target_date, "2026-05-20T12:00:00+01:00")
        pattern_types = {pattern["pattern_type"] for pattern in patterns}
        self.assertIn("SAMPLE_KEY_CLUSTER", pattern_types)
        self.assertIn("WAITING_PRELOCK_CLUSTER", pattern_types)

    def test_detects_unresolved_dominance(self) -> None:
        rows = [
            {"target_date": self.target_date, "fixture_id": str(index), "market_primary": "OVER_1_5", "official_action": "NO_BET", "result_status": "UNRESOLVED", "learning_family": "UNRESOLVED", "learning_status": "COLLECT_MORE_SAMPLE", "sample_key": f"UNRESOLVED::{index}", "accuracy_primary_risk": "UNKNOWN", "improvement_signal": "NO_SIGNAL"}
            for index in range(4)
        ]
        patterns = self.module.mine_patterns(rows, self.target_date, "2026-05-20T12:00:00+01:00")
        self.assertTrue(any(pattern["pattern_type"] == "UNRESOLVED_DOMINANCE" for pattern in patterns))

    def test_build_learning_patterns_outputs_csv_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            governance_dir = processed_dir / "governance"
            today_dir = processed_dir / "today" / self.target_date
            governance_dir.mkdir(parents=True)
            today_dir.mkdir(parents=True)
            (governance_dir / "vsigma_learning_ledger_all.csv").write_text(
                "target_date,fixture_id,market_primary,official_action,result_status,learning_family,learning_status,sample_key,accuracy_primary_risk,improvement_signal\n"
                "2026-05-20,1,OVER_1_5,NO_BET,UNRESOLVED,WAITING_PRELOCK,COLLECT_MORE_SAMPLE,WAITING_PRELOCK::OVER_1_5::LOW_CONVERSION::WAIT_FOR_POST_RESULTS,LOW_CONVERSION,WAIT_FOR_POST_RESULTS\n"
                "2026-05-20,2,OVER_1_5,NO_BET,UNRESOLVED,WAITING_PRELOCK,COLLECT_MORE_SAMPLE,WAITING_PRELOCK::OVER_1_5::LOW_CONVERSION::WAIT_FOR_POST_RESULTS,LOW_CONVERSION,WAIT_FOR_POST_RESULTS\n"
                "2026-05-20,3,OVER_2_5,EXECUTABLE,LOSS,ACTIONABLE_RESULT,REVIEW_PATTERN,ACTIONABLE_RESULT::OVER_2_5::LOW_CONVERSION::MONITOR_DECISION_QUALITY,LOW_CONVERSION,MONITOR_DECISION_QUALITY\n",
                encoding="utf-8",
            )
            patterns, paths = self.module.build_learning_patterns(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.today_md.read_text(encoding="utf-8")

        self.assertGreaterEqual(len(patterns), 1)
        self.assertIn("pattern_type", csv_text)
        self.assertIn("SAMPLE_KEY_CLUSTER", csv_text)
        self.assertIn("# vSIGMA Learning Patterns", md_text)
        self.assertIn("predictive changes applied: NO", md_text)

    def test_empty_inputs_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            patterns, paths = self.module.build_learning_patterns(
                self.target_date,
                processed_dir=processed_dir,
                now=datetime(2026, 5, 20, 12, 0, tzinfo=ZoneInfo("Atlantic/Canary")),
            )
            csv_text = paths.today_csv.read_text(encoding="utf-8")
            md_text = paths.governance_md.read_text(encoding="utf-8")

        self.assertEqual(patterns, [])
        self.assertIn("target_date", csv_text)
        self.assertIn("patterns detected: 0", md_text)


if __name__ == "__main__":
    unittest.main()
