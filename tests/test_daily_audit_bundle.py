from __future__ import annotations

import importlib
import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd


class DailyAuditBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.materialize_daily_audit_bundle")
        self.target_date = "2026-05-18"

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "materialize_daily_audit_bundle"))
        self.assertTrue(hasattr(self.module, "parse_args"))

    def test_materializes_daily_ledger_slice_and_optional_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            ledger_dir = processed_dir / "ledger"
            governance_dir = processed_dir / "governance"
            today_dir = processed_dir / "today" / self.target_date
            ledger_dir.mkdir(parents=True)
            governance_dir.mkdir(parents=True)
            today_dir.mkdir(parents=True)

            pd.DataFrame(
                [
                    {"target_date": self.target_date, "fixture_id": "1392197", "market_primary": "OVER_1_5"},
                    {"target_date": "2026-05-17", "fixture_id": "old", "market_primary": "HOME_WIN"},
                ]
            ).to_csv(ledger_dir / "vsigma_decision_outcome_ledger.csv", index=False)
            with (ledger_dir / "vsigma_decision_outcome_ledger.jsonl").open("w", encoding="utf-8") as handle:
                handle.write(json.dumps({"target_date": self.target_date, "fixture_id": "1392197"}) + "\n")
                handle.write(json.dumps({"target_date": "2026-05-17", "fixture_id": "old"}) + "\n")
            (ledger_dir / "vsigma_ledger_daily_report.md").write_text("# daily ledger\n", encoding="utf-8")
            (governance_dir / "vsigma_system_review.md").write_text("# system review\n", encoding="utf-8")
            (governance_dir / "vsigma_system_review.csv").write_text("target_date\n2026-05-18\n", encoding="utf-8")
            (governance_dir / "vsigma_prelock_decision_resolver_latest.md").write_text("# resolver\n", encoding="utf-8")
            (today_dir / "vsigma_cloud_decision_summary.csv").write_text("target_date\n2026-05-18\n", encoding="utf-8")

            files = self.module.materialize_daily_audit_bundle(self.target_date, processed_dir)

            daily_ledger = pd.read_csv(today_dir / "vsigma_decision_outcome_ledger.csv")
            daily_jsonl = (today_dir / "vsigma_decision_outcome_ledger.jsonl").read_text(encoding="utf-8")
            statuses = {item.name: item.status for item in files}

            self.assertEqual(statuses["vsigma_decision_outcome_ledger.csv"], "MATERIALIZED")
            self.assertEqual(len(daily_ledger), 1)
            self.assertEqual(str(daily_ledger.loc[0, "fixture_id"]), "1392197")
            self.assertIn("1392197", daily_jsonl)
            self.assertNotIn("old", daily_jsonl)
            self.assertTrue((today_dir / "vsigma_ledger_daily_report.md").exists())
            self.assertTrue((today_dir / "vsigma_system_review.md").exists())
            self.assertTrue((today_dir / "vsigma_system_review.csv").exists())
            self.assertTrue((today_dir / "vsigma_prelock_decision_resolver.md").exists())
            self.assertTrue((today_dir / "vsigma_cloud_decision_summary.csv").exists())


if __name__ == "__main__":
    unittest.main()
