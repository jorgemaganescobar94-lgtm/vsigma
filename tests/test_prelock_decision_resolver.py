from __future__ import annotations

import importlib
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


class PrelockDecisionResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = importlib.import_module("scripts.resolve_prelock_decision")
        self.target_date = "2026-05-18"
        self.tz = ZoneInfo("Atlantic/Canary")
        self.now = datetime(2026, 5, 18, 12, 0, tzinfo=self.tz)

    def write_candidate(self, today_dir: Path, fixture_id: str = "1", kickoff: str = "2026-05-18T13:00:00+01:00") -> None:
        pd.DataFrame(
            [
                {
                    "target_date": self.target_date,
                    "fixture_id": fixture_id,
                    "league": "Test League",
                    "home_team": "Home",
                    "away_team": "Away",
                    "market_primary": "OVER_1_5",
                    "fixture_datetime": kickoff,
                }
            ]
        ).to_csv(today_dir / "vsigma_today_competition_top.csv", index=False)

    def write_audit(
        self,
        today_dir: Path,
        *,
        fixture_id: str = "1",
        kickoff: str = "2026-05-18T13:00:00+01:00",
        retained: str = "NO",
        prelock_decision: str = "",
        exclusion_reason: str = "",
        lineup_state: str = "",
        odds_state: str = "",
        availability_state: str = "",
    ) -> None:
        pd.DataFrame(
            [
                {
                    "target_date": self.target_date,
                    "fixture_id": fixture_id,
                    "league": "Test League",
                    "home_team": "Home",
                    "away_team": "Away",
                    "market_primary": "OVER_1_5",
                    "fixture_datetime": kickoff,
                    "prelock_retained": retained,
                    "prelock_decision": prelock_decision,
                    "prelock_decision_reason": "no reliable pre-lock data available; missing data is neutral",
                    "prelock_lineup_state": lineup_state,
                    "prelock_odds_state": odds_state,
                    "prelock_availability_state": availability_state,
                    "exclusion_reason": exclusion_reason,
                }
            ]
        ).to_csv(today_dir / "vsigma_prelock_exclusion_audit.csv", index=False)

    def write_prelock(
        self,
        today_dir: Path,
        *,
        fixture_id: str = "1",
        kickoff: str = "2026-05-18T13:00:00+01:00",
        prelock_decision: str = "PRELOCK_CONFIRMED",
        lineup_state: str = "LINEUPS_CONFIRMED",
        odds_state: str = "ODDS_CONFIRMED",
        availability_state: str = "AVAILABILITY_CONFIRMED",
    ) -> None:
        pd.DataFrame(
            [
                {
                    "target_date": self.target_date,
                    "fixture_id": fixture_id,
                    "league": "Test League",
                    "home_team": "Home",
                    "away_team": "Away",
                    "market_primary": "OVER_1_5",
                    "fixture_datetime": kickoff,
                    "prelock_decision": prelock_decision,
                    "prelock_decision_reason": "prelock confirmed",
                    "prelock_lineup_state": lineup_state,
                    "prelock_odds_state": odds_state,
                    "prelock_availability_state": availability_state,
                }
            ]
        ).to_csv(today_dir / "vsigma_today_prelock_competition_top.csv", index=False)

    def run_resolver(self, processed_dir: Path) -> pd.DataFrame:
        resolver, paths = self.module.resolve_prelock_decisions(
            target_date=self.target_date,
            timezone_name="Atlantic/Canary",
            window_minutes=90,
            processed_dir=processed_dir,
            now=self.now,
        )
        self.assertTrue(paths.csv_path.exists())
        self.assertTrue(paths.md_path.exists())
        self.assertTrue(paths.latest_md_path.exists())
        return resolver

    def test_import_does_not_execute_main(self) -> None:
        self.assertTrue(hasattr(self.module, "resolve_prelock_decisions"))
        self.assertTrue(hasattr(self.module, "parse_args"))

    def test_no_candidates_maps_to_no_bet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            resolver = self.run_resolver(processed_dir)

        self.assertEqual(resolver["official_action"].tolist(), ["NO_BET"])
        self.assertEqual(resolver["final_block_reason"].tolist(), ["NO_CANDIDATES"])

    def test_outside_window_future_waits_for_next_slot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            self.write_candidate(today_dir, kickoff="2026-05-18T15:00:00+01:00")
            self.write_audit(today_dir, kickoff="2026-05-18T15:00:00+01:00", exclusion_reason="OUTSIDE_90_MIN_PRELOCK_WINDOW")

            resolver = self.run_resolver(processed_dir)

        self.assertEqual(resolver.loc[0, "official_action"], "WAIT")
        self.assertEqual(resolver.loc[0, "final_block_reason"], "OUTSIDE_PRELOCK_WINDOW")
        self.assertEqual(resolver.loc[0, "retry_allowed"], "YES")
        self.assertEqual(resolver.loc[0, "next_retry_time"], "2026-05-18T14:00+01:00")

    def test_kickoff_passed_maps_to_no_bet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            self.write_candidate(today_dir, kickoff="2026-05-18T11:30:00+01:00")
            self.write_audit(today_dir, kickoff="2026-05-18T11:30:00+01:00", exclusion_reason="PRELOCK_NOT_AVAILABLE")

            resolver = self.run_resolver(processed_dir)

        self.assertEqual(resolver.loc[0, "official_action"], "NO_BET")
        self.assertEqual(resolver.loc[0, "final_block_reason"], "KICKOFF_ALREADY_PASSED")
        self.assertEqual(resolver.loc[0, "execution_family_status"], "EXPIRED")

    def test_prelock_retained_confirmed_is_executable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            self.write_candidate(today_dir, kickoff="2026-05-18T13:00:00+01:00")
            self.write_prelock(today_dir, kickoff="2026-05-18T13:00:00+01:00")
            self.write_audit(today_dir, kickoff="2026-05-18T13:00:00+01:00", retained="YES", prelock_decision="PRELOCK_CONFIRMED")

            resolver = self.run_resolver(processed_dir)

        self.assertEqual(resolver.loc[0, "official_action"], "EXECUTABLE")
        self.assertEqual(resolver.loc[0, "executable_now"], "YES")
        self.assertEqual(resolver.loc[0, "final_block_reason"], "NONE")

    def test_prelock_not_available_odds_missing_is_no_bet_with_retry_slot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            self.write_candidate(today_dir, kickoff="2026-05-18T13:10:00+01:00")
            self.write_prelock(
                today_dir,
                kickoff="2026-05-18T13:10:00+01:00",
                prelock_decision="PRELOCK_NOT_AVAILABLE",
                odds_state="ODDS_NOT_AVAILABLE",
            )
            self.write_audit(
                today_dir,
                kickoff="2026-05-18T13:10:00+01:00",
                retained="YES",
                prelock_decision="PRELOCK_NOT_AVAILABLE",
                exclusion_reason="PRELOCK_NOT_AVAILABLE",
                odds_state="ODDS_NOT_AVAILABLE",
            )

            resolver = self.run_resolver(processed_dir)

        self.assertEqual(resolver.loc[0, "official_action"], "NO_BET")
        self.assertEqual(resolver.loc[0, "final_block_reason"], "ODDS_NOT_AVAILABLE")
        self.assertEqual(resolver.loc[0, "retry_allowed"], "YES")
        self.assertEqual(resolver.loc[0, "next_retry_time"], "2026-05-18T13:00+01:00")

    def test_multiple_gaps_are_concatenated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today" / self.target_date
            today_dir.mkdir(parents=True)
            self.write_candidate(today_dir, kickoff="2026-05-18T13:10:00+01:00")
            self.write_prelock(
                today_dir,
                kickoff="2026-05-18T13:10:00+01:00",
                prelock_decision="PRELOCK_NOT_AVAILABLE",
                lineup_state="LINEUPS_NOT_AVAILABLE",
                odds_state="ODDS_NOT_AVAILABLE",
                availability_state="AVAILABILITY_NOT_AVAILABLE",
            )
            self.write_audit(
                today_dir,
                kickoff="2026-05-18T13:10:00+01:00",
                retained="YES",
                prelock_decision="PRELOCK_NOT_AVAILABLE",
                exclusion_reason="PRELOCK_NOT_AVAILABLE",
                lineup_state="LINEUPS_NOT_AVAILABLE",
                odds_state="ODDS_NOT_AVAILABLE",
                availability_state="AVAILABILITY_NOT_AVAILABLE",
            )

            resolver = self.run_resolver(processed_dir)

        self.assertEqual(resolver.loc[0, "data_gap_flags"], "ODDS_MISSING;LINEUPS_MISSING;AVAILABILITY_MISSING")
        self.assertEqual(
            resolver.loc[0, "final_block_reason"],
            "ODDS_NOT_AVAILABLE;LINEUPS_NOT_AVAILABLE;AVAILABILITY_NOT_AVAILABLE",
        )


if __name__ == "__main__":
    unittest.main()
