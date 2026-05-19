from __future__ import annotations

import importlib
import unittest


class NotificationDispatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.dispatch_autonomous_monitoring_notification")

    def test_waiting_for_prelock_does_not_notify(self) -> None:
        text = """# Summary
- daily_classification: WAITING_FOR_PRELOCK
- action_level: REVIEW_REQUIRED
- operational_verdict: WAITING_FOR_PRELOCK
## Operator Action
- Wait for next scheduled run.
"""
        notification = self.module.build_notification("2026-05-19", "auto", text)
        self.assertFalse(notification.should_notify)
        self.assertEqual(notification.reason, "not_severe")

    def test_broken_missing_summary_notifies(self) -> None:
        notification = self.module.build_notification("2026-05-19", "auto", "")
        self.assertTrue(notification.should_notify)
        self.assertEqual(notification.classification, "BROKEN")
        self.assertEqual(notification.action_level, "ACTION_REQUIRED")

    def test_data_blocked_notifies_with_operator_action(self) -> None:
        text = """# Summary
- daily_classification: DATA_BLOCKED
- action_level: ACTION_REQUIRED
- operational_verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA
- predictive_failure: NO
## Operator Action
- Check provider/API coverage.
"""
        notification = self.module.build_notification("2026-05-19", "auto", text, "https://example/run")
        self.assertTrue(notification.should_notify)
        self.assertIn("DATA_BLOCKED", notification.title)
        self.assertIn("Check provider/API coverage", notification.body)
        self.assertIn("https://example/run", notification.body)


if __name__ == "__main__":
    unittest.main()
