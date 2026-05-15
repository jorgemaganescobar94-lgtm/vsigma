from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import backtest_vsigma
from scripts import build_api_league_coverage_matrix
from scripts import build_competition_accuracy_mode
from scripts import build_daily_decision_journal
from scripts import build_execution_mode_comparison
from scripts import build_execution_pick_modes
from scripts import build_execution_shortlist_results_ledger
from scripts import build_historical_execution_shortlist_backtest
from scripts import build_match_script_forecasts
from scripts import build_today_execution_shortlist
from scripts import calibrate_vsigma_thresholds
from scripts import deep_analysis_candidates
from scripts import enrich_odds_structure_depth
from scripts import enrich_fixture_lineups
from scripts import enrich_injuries_availability
from scripts import enrich_api_predictions_benchmark
from scripts import enrich_player_impact
from scripts import enrich_recent_fixture_anomaly_flags
from scripts import enrich_recent_fixture_statistics
from scripts import enrich_recent_schedule_strength
from scripts import final_execution_exports
from scripts import pick_explanations
from scripts import run_historical_labeling_pipeline
from scripts import run_today_shadow_candidate_v2
from scripts import run_today_shadow_candidate_v2_post_results
from scripts import run_today_shadow_candidate_v4
from scripts import run_today_shadow_candidate_v4_post_results
from scripts import run_today_shadow_candidate_v5
from scripts import run_today_shadow_candidate_v5_post_results
from scripts import run_today_shadow_candidate_v6
from scripts import run_today_shadow_candidate_v6_post_results
from scripts import apply_price_discipline_guard
from scripts import run_today_shadow_candidate_v7
from scripts import run_today_shadow_candidate_v7_post_results
from scripts import capture_odds_snapshots
from scripts import rebuild_odds_snapshots_for_date
from scripts import build_clv_calibration_report
from scripts import build_candidate_v7_calibration_advisor
from scripts import run_today_post_results_pipeline
from scripts import run_today_match_pipeline
from scripts import run_today_prelock_pipeline
from scripts import run_extended_historical_evaluation
from scripts import build_vsigma_drift_monitor
from scripts import update_immutable_daily_ledger
from scripts import build_experiment_performance_report
from scripts import build_promotion_threshold_governance
from scripts import run_vsigma_backtest_calibration
from scripts import score_matches_v3
from scripts import select_core_candidates
from scripts import build_daily_competition_master_report
from scripts import daily_hardening
from scripts import update_competition_scoreboard
from scripts import validate_candidate_isolation
from scripts import validate_daily_output_freshness
from scripts import validate_final_execution_exports
from scripts import run_today_prelock_orchestrator
from scripts import run_daily_competition_controller
from scripts import run_daily_competition_supervisor
from scripts import run_vsigma_healthcheck


REAL_SCHEMA_ROWS = [
    {
        "shortlist_rank": 1,
        "shortlist_bucket": "TOP_CORE",
        "analysis_label": "TOP_CORE",
        "date": "2026-05-07",
        "country": "World",
        "league": "UEFA Europa Conference League",
        "fixture_id": 1540881,
        "home_team": "Crystal Palace",
        "away_team": "Shakhtar Donetsk",
        "selection_score": 78.75,
        "vsigma_pre_score": 72.85,
        "confidence_band": "MEDIUM_HIGH",
        "likely_scoreline": "1-2 / 1-3 / 2-2",
        "market_primary": "OVER_1_5",
        "market_alt": "OVER_2_5",
        "edge_floor_band": "STRONG",
        "execution_verdict": "TOP_CORE",
        "final_recommendation": "BET",
        "primary_model_prob": 0.8835,
        "primary_odds_used": 1.31,
        "primary_implied_prob": 0.763359,
        "primary_edge": 0.120141,
        "alt_model_prob": 0.7139,
        "alt_odds_used": 1.96,
        "alt_implied_prob": 0.510204,
        "alt_edge": 0.203696,
        "status": "FT",
        "primary_result": "WIN",
        "primary_profit_units": 0.31,
        "actionable_flag": 1,
        "actionable_result": "WIN",
        "actionable_profit_units": 0.31,
    },
    {
        "shortlist_rank": 2,
        "shortlist_bucket": "TOP_CORE",
        "analysis_label": "TOP_CORE",
        "date": "2026-05-07",
        "country": "World",
        "league": "UEFA Europa Conference League",
        "fixture_id": 1540882,
        "home_team": "Strasbourg",
        "away_team": "Rayo Vallecano",
        "selection_score": 78.45,
        "vsigma_pre_score": 72.75,
        "confidence_band": "MEDIUM_HIGH",
        "likely_scoreline": "1-2 / 1-3 / 2-2",
        "market_primary": "OVER_1_5",
        "market_alt": "OVER_2_5",
        "edge_floor_band": "PLAYABLE",
        "execution_verdict": "CORE_SHORTLIST",
        "final_recommendation": "LEAN_PLAY",
        "primary_model_prob": 0.8138,
        "primary_odds_used": 1.28,
        "primary_implied_prob": 0.781250,
        "primary_edge": 0.032550,
        "alt_model_prob": 0.5965,
        "alt_odds_used": 1.91,
        "alt_implied_prob": 0.523560,
        "alt_edge": 0.072940,
        "status": "FT",
        "primary_result": "LOSS",
        "primary_profit_units": -1.00,
        "actionable_flag": 1,
        "actionable_result": "LOSS",
        "actionable_profit_units": -1.00,
    },
    {
        "shortlist_rank": 3,
        "shortlist_bucket": "CORE_SHORTLIST",
        "analysis_label": "CORE",
        "date": "2026-05-07",
        "country": "World",
        "league": "UEFA Europa League",
        "fixture_id": 1540873,
        "home_team": "Aston Villa",
        "away_team": "Nottingham Forest",
        "selection_score": 77.73,
        "vsigma_pre_score": 72.03,
        "confidence_band": "MEDIUM_HIGH",
        "likely_scoreline": "2-2 / 2-1 / 1-2",
        "market_primary": "OVER_2_5",
        "market_alt": "OVER_1_5",
        "edge_floor_band": "STRONG",
        "execution_verdict": "CORE_SHORTLIST",
        "final_recommendation": "BET",
        "primary_model_prob": 0.7175,
        "primary_odds_used": 1.94,
        "primary_implied_prob": 0.515464,
        "primary_edge": 0.202036,
        "alt_model_prob": 0.8855,
        "alt_odds_used": 1.29,
        "alt_implied_prob": 0.775194,
        "alt_edge": 0.110306,
        "status": "FT",
        "primary_result": "WIN",
        "primary_profit_units": 0.94,
        "actionable_flag": 1,
        "actionable_result": "WIN",
        "actionable_profit_units": 0.94,
    },
    {
        "shortlist_rank": 4,
        "shortlist_bucket": "CORE_SHORTLIST",
        "analysis_label": "CORE",
        "date": "2026-05-07",
        "country": "World",
        "league": "UEFA Europa League",
        "fixture_id": 1540874,
        "home_team": "Bologna",
        "away_team": "Lille",
        "selection_score": 75.83,
        "vsigma_pre_score": 70.12,
        "confidence_band": "MEDIUM",
        "likely_scoreline": "2-1 / 1-1 / 2-2",
        "market_primary": "OVER_1_5",
        "market_alt": "OVER_2_5",
        "edge_floor_band": "STRONG",
        "execution_verdict": "CORE_SHORTLIST",
        "final_recommendation": "BET",
        "primary_model_prob": 0.7682,
        "primary_odds_used": 1.30,
        "primary_implied_prob": 0.769231,
        "primary_edge": 0.088269,
        "alt_model_prob": 0.6031,
        "alt_odds_used": 1.98,
        "alt_implied_prob": 0.505051,
        "alt_edge": 0.098049,
        "status": "FT",
        "primary_result": "WIN",
        "primary_profit_units": 0.30,
        "actionable_flag": 1,
        "actionable_result": "WIN",
        "actionable_profit_units": 0.30,
    },
    {
        "shortlist_rank": 5,
        "shortlist_bucket": "CORE_SHORTLIST",
        "analysis_label": "CORE",
        "date": "2026-05-07",
        "country": "Norway",
        "league": "Eliteserien",
        "fixture_id": 1535292,
        "home_team": "Home",
        "away_team": "Away",
        "selection_score": 67.78,
        "vsigma_pre_score": 63.58,
        "confidence_band": "MEDIUM",
        "likely_scoreline": "2-1 / 1-1 / 2-2",
        "market_primary": "OVER_1_5",
        "market_alt": "OVER_2_5",
        "edge_floor_band": "PLAYABLE",
        "execution_verdict": "WATCH",
        "final_recommendation": "LEAN_PLAY",
        "primary_model_prob": 0.6827,
        "primary_odds_used": 1.57,
        "primary_implied_prob": 0.636943,
        "primary_edge": 0.045757,
        "alt_model_prob": 0.4471,
        "alt_odds_used": 2.72,
        "alt_implied_prob": 0.367647,
        "alt_edge": 0.079453,
        "status": "FT",
        "primary_result": "WIN",
        "primary_profit_units": 0.57,
        "actionable_flag": 1,
        "actionable_result": "WIN",
        "actionable_profit_units": 0.57,
    },
    {
        "shortlist_rank": 6,
        "shortlist_bucket": "WATCHLIST",
        "analysis_label": "WATCH",
        "date": "2026-05-07",
        "country": "Norway",
        "league": "Eliteserien",
        "fixture_id": 1535199,
        "home_team": "Home 2",
        "away_team": "Away 2",
        "selection_score": 62.87,
        "vsigma_pre_score": 59.37,
        "confidence_band": "LOW",
        "likely_scoreline": "1-0 / 1-1 / 0-1",
        "market_primary": "OVER_1_5",
        "market_alt": "OVER_2_5",
        "edge_floor_band": "THIN",
        "execution_verdict": "WATCH",
        "final_recommendation": "WATCH",
        "primary_model_prob": 0.7071,
        "primary_odds_used": 1.40,
        "primary_implied_prob": 0.714286,
        "primary_edge": -0.007052,
        "alt_model_prob": 0.4012,
        "alt_odds_used": 2.20,
        "alt_implied_prob": 0.454545,
        "alt_edge": -0.053345,
        "status": "FT",
        "primary_result": "LOSS",
        "primary_profit_units": -1.00,
        "actionable_flag": 0,
        "actionable_result": "SKIPPED",
        "actionable_profit_units": None,
    },
    {
        "shortlist_rank": 7,
        "shortlist_bucket": "WATCHLIST",
        "analysis_label": "WATCH",
        "date": "2026-05-07",
        "country": "Sweden",
        "league": "Allsvenskan",
        "fixture_id": 1535190,
        "home_team": "Home 3",
        "away_team": "Away 3",
        "selection_score": 61.78,
        "vsigma_pre_score": 58.28,
        "confidence_band": "LOW",
        "likely_scoreline": "1-0 / 0-0 / 1-1",
        "market_primary": "UNDER_3_5",
        "market_alt": "OVER_1_5",
        "edge_floor_band": "THIN",
        "execution_verdict": "NO_BET",
        "final_recommendation": "NO_BET",
        "primary_model_prob": 0.7700,
        "primary_odds_used": 1.24,
        "primary_implied_prob": 0.806452,
        "primary_edge": 0.012414,
        "alt_model_prob": 0.7051,
        "alt_odds_used": 1.44,
        "alt_implied_prob": 0.694444,
        "alt_edge": 0.010656,
        "status": "FT",
        "primary_result": "LOSS",
        "primary_profit_units": -1.00,
        "actionable_flag": 0,
        "actionable_result": "SKIPPED",
        "actionable_profit_units": None,
    },
]


class VsigmBacktestCalibrationTests(unittest.TestCase):
    def write_real_schema_inputs(self, root: Path) -> tuple[Path, Path]:
        labeled_path = root / "vsigma_market_results_labeled.csv"
        deep_path = root / "vsigma_deep_analysis_candidates.csv"

        labeled = pd.DataFrame(REAL_SCHEMA_ROWS)
        deep = labeled.drop(
            columns=[
                "status",
                "primary_result",
                "primary_profit_units",
                "actionable_flag",
                "actionable_result",
                "actionable_profit_units",
            ]
        )

        labeled.to_csv(labeled_path, index=False)
        deep.to_csv(deep_path, index=False)
        return labeled_path, deep_path

    def test_fixture_statistics_normalizes_api_label_value_pairs(self) -> None:
        payload = {
            "response": [
                {
                    "team": {"id": 10},
                    "statistics": [
                        {"type": "Shots on Goal", "value": 5},
                        {"type": "Total Shots", "value": "14"},
                        {"type": "Corner Kicks", "value": 7},
                        {"type": "Ball Possession", "value": "53%"},
                        {"type": "Fouls", "value": None},
                        {"type": "Yellow Cards", "value": 2},
                        {"type": "Offsides", "value": "3"},
                        {"type": "Blocked Shots", "value": "4"},
                    ],
                }
            ]
        }

        parsed = enrich_recent_fixture_statistics.parse_fixture_statistics_payload(payload)

        self.assertEqual(parsed[10]["sot"], 5.0)
        self.assertEqual(parsed[10]["shots"], 14.0)
        self.assertEqual(parsed[10]["corners"], 7.0)
        self.assertEqual(parsed[10]["possession"], 53.0)
        self.assertTrue(pd.isna(parsed[10]["fouls"]))
        self.assertEqual(parsed[10]["yellow"], 2.0)
        self.assertEqual(parsed[10]["offsides"], 3.0)
        self.assertEqual(parsed[10]["blocked_shots"], 4.0)

    def test_fixture_statistics_quality_flags_are_coverage_aware(self) -> None:
        self.assertEqual(enrich_recent_fixture_statistics.quality_flag(5, 5), "FULL")
        self.assertEqual(enrich_recent_fixture_statistics.quality_flag(3, 4), "PARTIAL")
        self.assertEqual(enrich_recent_fixture_statistics.quality_flag(1, 0), "SPARSE")
        self.assertEqual(enrich_recent_fixture_statistics.quality_flag(0, 0), "NONE")

    def test_fixture_statistics_missing_data_remains_nan_not_zero(self) -> None:
        output = enrich_recent_fixture_statistics.build_empty_team_output(requested=5)

        self.assertEqual(output["recent_stats_matches_requested"], 5)
        self.assertEqual(output["recent_stats_matches_used"], 0)
        self.assertEqual(output["recent_stats_available_flag"], 0)
        self.assertTrue(pd.isna(output["recent_shots_for_pg"]))
        self.assertTrue(pd.isna(output["recent_sot_for_pg"]))
        self.assertTrue(pd.isna(output["recent_corners_for_pg"]))

    def test_fixture_statistics_window_uses_only_prior_completed_fixtures(self) -> None:
        fixtures = [
            {
                "fixture": {
                    "id": 1,
                    "date": "2026-05-01T18:00:00+00:00",
                    "timestamp": 1777658400,
                    "status": {"short": "FT"},
                }
            },
            {
                "fixture": {
                    "id": 2,
                    "date": "2026-05-02T18:00:00+00:00",
                    "timestamp": 1777744800,
                    "status": {"short": "NS"},
                }
            },
            {
                "fixture": {
                    "id": 3,
                    "date": "2026-05-03T18:00:00+00:00",
                    "timestamp": 1777831200,
                    "status": {"short": "FT"},
                }
            },
            {
                "fixture": {
                    "id": 4,
                    "date": "2026-05-04T18:00:00+00:00",
                    "timestamp": 1777917600,
                    "status": {"short": "FT"},
                }
            },
        ]

        selected = enrich_recent_fixture_statistics.pick_prior_completed_fixtures(
            fixtures,
            target_fixture_id=3,
            before_dt=pd.Timestamp("2026-05-04T00:00:00Z").to_pydatetime(),
            limit=5,
        )

        self.assertEqual([item["fixture"]["id"] for item in selected], [1])

    def test_recent_schedule_strength_generates_conservative_fields(self) -> None:
        class FakeClient:
            def standings(self, **_kwargs):
                return {
                    "response": [
                        {
                            "league": {
                                "id": 39,
                                "name": "Premier League",
                                "season": 2026,
                                "standings": [
                                    [
                                        {"team": {"id": 20}, "rank": 1, "points": 30, "all": {"played": 12}},
                                        {"team": {"id": 30}, "rank": 10, "points": 15, "all": {"played": 12}},
                                        {"team": {"id": 40}, "rank": 20, "points": 5, "all": {"played": 12}},
                                    ]
                                ],
                            }
                        }
                    ]
                }

        fixtures = [
            {"fixture": {"id": 1}, "league": {"id": 39, "season": 2026}, "teams": {"home": {"id": 10}, "away": {"id": 20}}},
            {"fixture": {"id": 2}, "league": {"id": 39, "season": 2026}, "teams": {"home": {"id": 30}, "away": {"id": 10}}},
            {"fixture": {"id": 3}, "league": {"id": 39, "season": 2026}, "teams": {"home": {"id": 10}, "away": {"id": 40}}},
        ]

        metrics = enrich_recent_schedule_strength.compute_team_schedule_strength(
            FakeClient(),
            {},
            fixtures,
            team_id=10,
            counters={},
        )

        self.assertEqual(metrics["recent_schedule_matches_used"], 3)
        self.assertEqual(metrics["recent_schedule_quality_flag"], "PARTIAL")
        self.assertGreaterEqual(metrics["recent_opponent_strength_avg"], 0.0)
        self.assertLessEqual(metrics["recent_opponent_strength_avg"], 1.0)
        self.assertGreaterEqual(metrics["recent_schedule_difficulty_score"], -1.0)
        self.assertLessEqual(metrics["recent_schedule_difficulty_score"], 1.0)

    def test_recent_anomaly_flags_from_events(self) -> None:
        payload = {
            "response": [
                {"time": {"elapsed": 12}, "team": {"id": 10}, "type": "Card", "detail": "Red Card"},
                {"time": {"elapsed": 20}, "team": {"id": 20}, "type": "Goal", "detail": "Penalty"},
            ]
        }

        parsed = enrich_recent_fixture_anomaly_flags.detect_fixture_anomalies(
            enrich_recent_fixture_anomaly_flags.parse_fixture_events_payload(payload),
            {"fixture": {"status": {"short": "FT"}}},
        )

        self.assertEqual(parsed["early_red_card"], 1)
        self.assertEqual(parsed["early_penalty"], 1)
        self.assertEqual(parsed["first_half_game_state_shock"], 1)
        self.assertEqual(parsed["fixture_anomaly_flag"], 1)

    def test_recent_anomaly_missing_coverage_is_uncertainty_not_weakness(self) -> None:
        class FakeClient:
            def _get_cached(self, _key):
                return None

            def fixture_events(self, _fixture):
                raise AssertionError("events should not be requested without supported coverage")

        fixtures = [
            {"fixture": {"id": 1, "status": {"short": "FT"}}, "league": {"id": 39, "season": 2026}},
            {"fixture": {"id": 2, "status": {"short": "FT"}}, "league": {"id": 39, "season": 2026}},
        ]

        metrics = enrich_recent_fixture_anomaly_flags.compute_team_recent_anomalies(
            FakeClient(),
            fixtures,
            coverage={},
            counters={},
        )

        self.assertEqual(metrics["recent_events_checked_last5"], 0)
        self.assertEqual(metrics["recent_anomaly_count_last5"], 0)
        self.assertEqual(metrics["recent_anomaly_penalty"], 0.0)
        self.assertEqual(metrics["recent_event_coverage_flag"], "UNKNOWN")

    def test_recent_lab_fields_survive_scoring_and_remain_conservative(self) -> None:
        df = pd.DataFrame(
            [
                {
                    "home_recent_schedule_quality_flag": "FULL",
                    "away_recent_schedule_quality_flag": "FULL",
                    "home_recent_event_coverage_flag": "SUPPORTED",
                    "away_recent_event_coverage_flag": "SUPPORTED",
                    "home_recent_schedule_difficulty_score": 1.0,
                    "away_recent_schedule_difficulty_score": -1.0,
                    "home_recent_anomaly_penalty": 0.0,
                    "away_recent_anomaly_penalty": 1.2,
                }
            ]
        )

        home_mult = score_matches_v3.recent_lab_trust_multiplier(df, "home").iloc[0]
        away_mult = score_matches_v3.recent_lab_trust_multiplier(df, "away").iloc[0]

        self.assertLessEqual(home_mult, 1.08)
        self.assertGreaterEqual(away_mult, 0.78)
        self.assertGreater(home_mult, away_mult)

    def test_odds_structure_fields_are_generated_from_payload(self) -> None:
        payload = {
            "response": [
                {
                    "bookmakers": [
                        {
                            "id": 1,
                            "bets": [
                                {
                                    "id": 5,
                                    "values": [
                                        {"value": "Over 1.5", "odd": "1.30"},
                                        {"value": "Over 2.5", "odd": "1.80"},
                                        {"value": "Under 3.5", "odd": "1.62"},
                                    ],
                                },
                                {"id": 8, "values": [{"value": "Yes", "odd": "1.75"}]},
                                {
                                    "id": 1,
                                    "values": [
                                        {"value": "Home", "odd": "2.10"},
                                        {"value": "Draw", "odd": "3.45"},
                                        {"value": "Away", "odd": "3.60"},
                                    ],
                                },
                            ],
                        },
                        {
                            "id": 2,
                            "bets": [
                                {
                                    "id": 5,
                                    "values": [
                                        {"value": "Over 1.5", "odd": "1.32"},
                                        {"value": "Over 2.5", "odd": "1.83"},
                                        {"value": "Under 3.5", "odd": "1.64"},
                                    ],
                                },
                                {"id": 8, "values": [{"value": "Yes", "odd": "1.78"}]},
                            ],
                        },
                    ]
                }
            ]
        }

        fields = enrich_odds_structure_depth.derive_depth_fields(
            enrich_odds_structure_depth.parse_odds_payload(payload)
        )

        self.assertGreater(fields["odds_imp_over15"], fields["odds_imp_over25"])
        self.assertEqual(fields["odds_bookmaker_support_count"], 2)
        self.assertGreaterEqual(fields["odds_market_support_count"], 7)
        self.assertIn(fields["odds_structure_coherence_flag"], {"RICH_COHERENT", "RICH_MIXED"})

    def test_odds_structure_missing_or_thin_support_is_uncertainty(self) -> None:
        fields = enrich_odds_structure_depth.derive_depth_fields(
            enrich_odds_structure_depth.ParsedOdds(
                values=enrich_odds_structure_depth.empty_market_values(),
                bookmaker_ids=set(),
            )
        )

        self.assertEqual(fields["odds_structure_coherence_flag"], "NO_ODDS_UNCERTAIN")
        self.assertEqual(fields["odds_market_translation_hint"], "ODDS_DEPTH_UNCERTAIN")
        self.assertEqual(fields["odds_confidence_adjustment_score"], 0.0)
        self.assertEqual(deep_analysis_candidates.odds_structure_market_adjustment(pd.Series(fields), "OVER_2_5"), 0.0)

    def test_odds_structure_coherent_ladder_can_strengthen_broad_goals(self) -> None:
        fields = enrich_odds_structure_depth.derive_depth_fields(
            enrich_odds_structure_depth.ParsedOdds(
                values={
                    "OVER_1_5": [1.25, 1.27, 1.26],
                    "OVER_2_5": [1.72, 1.75, 1.73],
                    "UNDER_3_5": [1.78, 1.80, 1.79],
                    "BTTS_YES": [1.70, 1.72, 1.71],
                    "HOME_WIN": [2.15, 2.18],
                    "DRAW": [3.55, 3.60],
                    "AWAY_WIN": [3.40, 3.45],
                    "HOME_DNB": [],
                    "AWAY_DNB": [],
                },
                bookmaker_ids={"a", "b", "c"},
            )
        )

        self.assertEqual(fields["odds_line_aggression_flag"], "OVER_2_5_SUPPORTED")
        self.assertGreater(deep_analysis_candidates.odds_structure_market_adjustment(pd.Series(fields), "OVER_2_5"), 0)

    def test_odds_structure_aggressive_line_detection_prefers_milder_totals(self) -> None:
        fields = enrich_odds_structure_depth.derive_depth_fields(
            enrich_odds_structure_depth.ParsedOdds(
                values={
                    "OVER_1_5": [1.30, 1.32, 1.31],
                    "OVER_2_5": [2.25, 2.30, 2.28],
                    "UNDER_3_5": [1.40, 1.42, 1.41],
                    "BTTS_YES": [2.05, 2.08],
                    "HOME_WIN": [2.20, 2.24],
                    "DRAW": [3.20, 3.25],
                    "AWAY_WIN": [3.30, 3.35],
                    "HOME_DNB": [],
                    "AWAY_DNB": [],
                },
                bookmaker_ids={"a", "b", "c"},
            )
        )
        row = pd.Series(fields)

        self.assertEqual(fields["odds_line_aggression_flag"], "PREFER_OVER_1_5")
        self.assertLess(deep_analysis_candidates.odds_structure_market_adjustment(row, "OVER_2_5"), 0)
        self.assertGreater(deep_analysis_candidates.odds_structure_market_adjustment(row, "OVER_1_5"), 0)

    def test_odds_structure_fragile_side_flag_is_not_hard_veto(self) -> None:
        fields = enrich_odds_structure_depth.derive_depth_fields(
            enrich_odds_structure_depth.ParsedOdds(
                values={
                    "OVER_1_5": [1.45, 1.47],
                    "OVER_2_5": [2.05, 2.08],
                    "UNDER_3_5": [1.45, 1.47],
                    "BTTS_YES": [1.95, 1.97],
                    "HOME_WIN": [2.45, 2.48],
                    "DRAW": [3.30, 3.35],
                    "AWAY_WIN": [2.95, 3.00],
                    "HOME_DNB": [1.70, 1.72],
                    "AWAY_DNB": [2.05, 2.08],
                },
                bookmaker_ids={"a", "b", "c"},
            )
        )
        adjustment = deep_analysis_candidates.odds_structure_market_adjustment(pd.Series(fields), "HOME_WIN")

        self.assertEqual(fields["odds_side_fragility_flag"], "DRAW_LIVE_FRAGILITY")
        self.assertLess(adjustment, 0)
        self.assertGreaterEqual(adjustment, -0.06)

    def test_odds_structure_outputs_and_reports_are_generated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "league": "League",
                        "home_team": "Home",
                        "away_team": "Away",
                        "odds_over_1_5_v3": 1.30,
                        "odds_over_2_5_v3": 2.25,
                        "odds_under_3_5_v3": 1.40,
                        "odds_bookmakers_count_v3": 1,
                    }
                ]
            )
            filtered = raw.assign(league_tier_rank=1)
            enriched, preview = enrich_odds_structure_depth.enrich_odds_structure_depth(raw, filtered, client=None)
            summary = enrich_odds_structure_depth.summarize_depth(enriched, {1})
            summary_path = root / "summary.csv"
            report_path = root / "report.txt"
            summary.to_csv(summary_path, index=False)
            enrich_odds_structure_depth.write_report(report_path, summary, preview)

            self.assertTrue(set(enrich_odds_structure_depth.ODDS_DEPTH_FIELDS).issubset(enriched.columns))
            self.assertTrue(summary_path.exists())
            self.assertTrue(report_path.exists())
            self.assertIn("ODDS STRUCTURE DEPTH", report_path.read_text(encoding="utf-8"))

    def test_odds_structure_experimental_use_remains_conservative(self) -> None:
        row = pd.Series(
            {
                "odds_structure_coherence_flag": "RICH_COHERENT",
                "odds_total_ladder_shape": "MILD_GOALS",
                "odds_market_translation_hint": "PREFER_MILDER_TOTAL",
                "odds_line_aggression_flag": "PREFER_OVER_1_5",
                "odds_side_fragility_flag": "DRAW_LIVE_FRAGILITY",
                "odds_btts_support_flag": "WEAK",
                "odds_over25_support_flag": "WEAK",
                "odds_over15_support_flag": "SUPPORTED",
                "odds_under35_support_flag": "SUPPORTED",
            }
        )

        adjustments = [
            deep_analysis_candidates.odds_structure_market_adjustment(row, market)
            for market in ["OVER_2_5", "OVER_1_5", "HOME_WIN", "BTTS_YES"]
        ]

        self.assertTrue(all(-0.06 <= value <= 0.035 for value in adjustments))
        self.assertLess(min(adjustments), 0)
        self.assertGreater(max(adjustments), 0)

    def test_injuries_normalization_builds_team_level_features(self) -> None:
        payload = {
            "response": [
                {
                    "fixture": {"id": 100},
                    "league": {"id": 39, "season": 2026},
                    "team": {"id": 10, "name": "Home"},
                    "player": {"id": 1, "name": "A", "type": "Injury", "reason": "Hamstring"},
                },
                {
                    "fixture": {"id": 100},
                    "league": {"id": 39, "season": 2026},
                    "team": {"id": 10, "name": "Home"},
                    "player": {"id": 2, "name": "B", "type": "Doubtful", "reason": "Knock"},
                },
                {
                    "fixture": {"id": 100},
                    "league": {"id": 39, "season": 2026},
                    "team": {"id": 20, "name": "Away"},
                    "player": {"id": 3, "name": "C", "type": "Suspended", "reason": "Red card"},
                },
            ]
        }

        features = enrich_injuries_availability.build_availability_features(payload, 10, 20)

        self.assertEqual(features["home_injuries_count"], 2)
        self.assertEqual(features["away_injuries_count"], 1)
        self.assertEqual(features["home_injuries_coverage_flag"], "FULL")
        self.assertEqual(features["away_injuries_coverage_flag"], "FULL")
        self.assertEqual(features["injuries_quality_flag"], "FULL")
        self.assertAlmostEqual(float(features["home_absence_risk_score"]), 1.6)
        self.assertEqual(features["home_absences"], 2)

    def test_injuries_zero_known_vs_unknown_missing(self) -> None:
        known_zero_payload = {
            "response": [
                {
                    "fixture": {"id": 100},
                    "team": {"id": 10, "name": "Home"},
                    "player": {"id": 1, "name": "A", "type": "Injury", "reason": "Muscle"},
                }
            ]
        }
        known = enrich_injuries_availability.build_availability_features(known_zero_payload, 10, 20)
        unknown = enrich_injuries_availability.build_availability_features({"response": []}, 10, 20)

        self.assertEqual(known["away_injuries_count"], 0)
        self.assertEqual(known["away_injuries_coverage_flag"], "FULL")
        self.assertEqual(known["away_absences"], 0)
        self.assertTrue(pd.isna(unknown["home_injuries_count"]))
        self.assertEqual(unknown["home_injuries_coverage_flag"], "NONE")
        self.assertEqual(unknown["home_absence_severity_flag"], "UNKNOWN")
        self.assertTrue(pd.isna(unknown["home_absences"]))

    def test_injuries_coverage_flags_full_partial_none_behavior(self) -> None:
        full = enrich_injuries_availability.build_availability_features(
            {"response": [{"team": {"id": 10}, "player": {"type": "Injury"}, "fixture": {"id": 1}}]},
            10,
            20,
        )
        sparse = enrich_injuries_availability.build_availability_features(
            {"response": [{"team": {"id": 99}, "player": {"type": "Injury"}, "fixture": {"id": 1}}]},
            10,
            20,
        )
        none = enrich_injuries_availability.build_availability_features({"response": []}, 10, 20)

        self.assertEqual(full["injuries_quality_flag"], "FULL")
        self.assertEqual(enrich_injuries_availability.injuries_quality_flag("FULL", "PARTIAL"), "PARTIAL")
        self.assertEqual(sparse["injuries_quality_flag"], "SPARSE")
        self.assertEqual(none["injuries_quality_flag"], "NONE")

    def lineup_payload(self) -> dict[str, object]:
        def players(positions: list[str]) -> list[dict[str, object]]:
            return [
                {"player": {"id": idx + 1, "name": f"P{idx}", "pos": position}}
                for idx, position in enumerate(positions)
            ]

        return {
            "response": [
                {
                    "team": {"id": 10, "name": "Home"},
                    "formation": "4-3-3",
                    "startXI": players(["G", "D", "D", "D", "D", "M", "M", "M", "F", "F", "F"]),
                    "substitutes": players(["G", "D", "M", "F"]),
                },
                {
                    "team": {"id": 20, "name": "Away"},
                    "formation": "4-4-2",
                    "startXI": players(["G", "D", "D", "D", "D", "M", "M", "M", "M", "F", "F"]),
                    "substitutes": players(["G", "D", "M", "F"]),
                },
            ]
        }

    def test_lineup_response_normalization_builds_team_level_features(self) -> None:
        features = enrich_fixture_lineups.build_lineup_features(self.lineup_payload(), 10, 20)

        self.assertEqual(features["lineup_quality_flag"], "FULL")
        self.assertEqual(features["home_lineup_available_flag"], 1)
        self.assertEqual(features["away_lineup_available_flag"], 1)
        self.assertEqual(features["home_lineup_known_starters_count"], 11)
        self.assertEqual(features["away_lineup_known_starters_count"], 11)
        self.assertGreater(float(features["lineup_confirmation_score"]), 0.0)
        self.assertEqual(features["lineup_activation_state"], "ADVISORY_ONLY")

    def test_lineup_unknown_is_not_bad_lineup_and_has_no_fake_zeros(self) -> None:
        features = enrich_fixture_lineups.build_lineup_features({"response": []}, 10, 20)

        self.assertEqual(features["lineup_quality_flag"], "NONE")
        self.assertEqual(features["home_lineup_available_flag"], 0)
        self.assertEqual(features["away_lineup_available_flag"], 0)
        self.assertTrue(pd.isna(features["home_lineup_known_starters_count"]))
        self.assertTrue(pd.isna(features["away_lineup_attacker_count"]))
        self.assertTrue(pd.isna(features["home_lineup_goalkeeper_known_flag"]))
        self.assertTrue(pd.isna(features["lineup_confirmation_score"]))
        self.assertEqual(features["lineup_activation_state"], "INACTIVE")
        self.assertLessEqual(float(features["lineup_uncertainty_penalty"]), 0.12)

    def test_lineup_full_within_activation_window_is_active(self) -> None:
        features = enrich_fixture_lineups.build_lineup_features(
            self.lineup_payload(),
            10,
            20,
            fixture_datetime_utc="2026-05-10T20:00:00+00:00",
            reference_datetime_utc="2026-05-10T18:45:00+00:00",
        )

        self.assertEqual(features["lineup_quality_flag"], "FULL")
        self.assertEqual(features["lineup_activation_state"], "ACTIVE")
        self.assertEqual(features["lineup_timing_eligible_flag"], 1)
        self.assertEqual(features["lineup_structural_confidence_flag"], 1)
        self.assertAlmostEqual(float(features["lineup_minutes_to_kickoff"]), 75.0)

    def test_lineup_full_outside_activation_window_is_advisory_only(self) -> None:
        features = enrich_fixture_lineups.build_lineup_features(
            self.lineup_payload(),
            10,
            20,
            fixture_datetime_utc="2026-05-10T20:00:00+00:00",
            reference_datetime_utc="2026-05-10T17:30:00+00:00",
        )

        self.assertEqual(features["lineup_quality_flag"], "FULL")
        self.assertEqual(features["lineup_activation_state"], "ADVISORY_ONLY")
        self.assertEqual(features["lineup_timing_eligible_flag"], 0)
        self.assertEqual(features["lineup_structural_confidence_flag"], 1)

    def test_lineup_none_is_inactive_even_inside_activation_window(self) -> None:
        features = enrich_fixture_lineups.build_lineup_features(
            {"response": []},
            10,
            20,
            fixture_datetime_utc="2026-05-10T20:00:00+00:00",
            reference_datetime_utc="2026-05-10T18:45:00+00:00",
        )

        self.assertEqual(features["lineup_quality_flag"], "NONE")
        self.assertEqual(features["lineup_activation_state"], "INACTIVE")
        self.assertEqual(features["lineup_timing_eligible_flag"], 1)
        self.assertEqual(features["lineup_structural_confidence_flag"], 0)

    def test_lineup_role_counts_and_goalkeeper_flags_from_available_xi(self) -> None:
        features = enrich_fixture_lineups.build_lineup_features(self.lineup_payload(), 10, 20)

        self.assertEqual(features["home_lineup_attacker_count"], 3)
        self.assertEqual(features["home_lineup_defender_count"], 4)
        self.assertEqual(features["home_lineup_midfielder_count"], 3)
        self.assertEqual(features["home_lineup_goalkeeper_known_flag"], 1)
        self.assertEqual(features["away_lineup_goalkeeper_known_flag"], 1)

    def test_lineup_goalkeeper_missing_is_known_structural_caution(self) -> None:
        payload = self.lineup_payload()
        payload["response"][0]["startXI"][0]["player"]["pos"] = "D"

        features = enrich_fixture_lineups.build_lineup_features(payload, 10, 20)

        self.assertEqual(features["home_lineup_goalkeeper_known_flag"], 0)
        self.assertEqual(
            deep_analysis_candidates.lineup_interpretation(pd.Series(features)),
            deep_analysis_candidates.GOALKEEPER_UNKNOWN_ADVISORY,
        )
        self.assertLess(float(features["home_lineup_defense_continuity_score"]), 0.1)

    def test_lineup_unknown_has_only_tiny_scoring_effect(self) -> None:
        no_lineup = {
            "lineup_quality_flag": "NONE",
            "lineup_activation_state": "INACTIVE",
            "home_lineup_available_flag": 0,
            "away_lineup_available_flag": 0,
            "lineup_confirmation_score": pd.NA,
            "lineup_uncertainty_penalty": 0.12,
        }
        full_lineup = {
            "lineup_quality_flag": "FULL",
            "lineup_activation_state": "ADVISORY_ONLY",
            "home_lineup_available_flag": 1,
            "away_lineup_available_flag": 1,
            "lineup_confirmation_score": 0.0,
            "lineup_uncertainty_penalty": 0.0,
        }

        scored = self.score_rows_in_tmp(
            [
                self.strong_scoring_row(9051, full_lineup),
                self.strong_scoring_row(9052, no_lineup),
            ]
        ).set_index("fixture_id")

        self.assertEqual(float(scored.loc[9052, "lineup_score_nudge"]), 0.0)
        self.assertLess(
            abs(float(scored.loc[9051, "vsigma_pre_score"]) - float(scored.loc[9052, "vsigma_pre_score"])),
            0.1,
        )

    def test_lineup_full_normal_xi_can_modestly_confirm_confidence(self) -> None:
        weak_known = {
            "lineup_quality_flag": "FULL",
            "lineup_activation_state": "ACTIVE",
            "home_lineup_available_flag": 1,
            "away_lineup_available_flag": 1,
            "lineup_confirmation_score": -0.35,
            "lineup_uncertainty_penalty": 0.0,
        }
        strong_known = {
            "lineup_quality_flag": "FULL",
            "lineup_activation_state": "ACTIVE",
            "home_lineup_available_flag": 1,
            "away_lineup_available_flag": 1,
            "lineup_confirmation_score": 0.35,
            "lineup_uncertainty_penalty": 0.0,
        }

        scored = self.score_rows_in_tmp(
            [
                self.strong_scoring_row(9061, weak_known),
                self.strong_scoring_row(9062, strong_known),
            ]
        ).set_index("fixture_id")

        self.assertLess(float(scored.loc[9061, "lineup_score_nudge"]), 0.0)
        self.assertGreater(float(scored.loc[9062, "lineup_score_nudge"]), 0.0)
        self.assertLess(
            float(scored.loc[9062, "vsigma_pre_score"]) - float(scored.loc[9061, "vsigma_pre_score"]),
            0.6,
        )

    def test_lineup_full_advisory_only_has_no_material_scoring_effect(self) -> None:
        advisory = {
            "lineup_quality_flag": "FULL",
            "lineup_activation_state": "ADVISORY_ONLY",
            "lineup_timing_eligible_flag": 0,
            "lineup_structural_confidence_flag": 1,
            "home_lineup_available_flag": 1,
            "away_lineup_available_flag": 1,
            "lineup_confirmation_score": 0.35,
            "lineup_uncertainty_penalty": 0.0,
        }
        active = {
            **advisory,
            "lineup_activation_state": "ACTIVE",
            "lineup_timing_eligible_flag": 1,
            "lineup_confirmation_score": 0.35,
        }

        scored = self.score_rows_in_tmp(
            [
                self.strong_scoring_row(9063, advisory),
                self.strong_scoring_row(9064, active),
            ]
        ).set_index("fixture_id")

        self.assertEqual(float(scored.loc[9063, "lineup_score_nudge"]), 0.0)
        self.assertGreater(float(scored.loc[9064, "lineup_score_nudge"]), 0.0)

    def test_fixture_datetime_survives_today_and_historical_normalization(self) -> None:
        payload = {
            "fixture": {
                "id": 1540001,
                "date": "2026-05-10T20:00:00+00:00",
                "timestamp": 1778443200,
            },
            "league": {"id": 39, "name": "Premier League", "country": "England"},
            "teams": {
                "home": {"id": 10, "name": "Home"},
                "away": {"id": 20, "name": "Away"},
            },
            "goals": {"home": None, "away": None},
            "score": {"fulltime": {"home": None, "away": None}},
            "fixture_status": {"short": "NS"},
        }

        today = run_today_match_pipeline.normalize_fixture_payload(payload)
        historical = run_historical_labeling_pipeline.normalize_fixture_payload(payload)

        self.assertEqual(today["fixture_datetime_utc"], "2026-05-10T20:00:00+00:00")
        self.assertEqual(today["fixture_timestamp"], 1778443200)
        self.assertEqual(historical["fixture_datetime_utc"], "2026-05-10T20:00:00+00:00")
        self.assertEqual(historical["fixture_timestamp"], 1778443200)

    def strong_scoring_row(self, fixture_id: int, injury_overrides: dict[str, object]) -> dict[str, object]:
        row = {
            "date": "2026-05-10",
            "country": "England",
            "league": "Premier League",
            "league_tier": "TIER_1",
            "league_tier_rank": 1,
            "fixture_id": fixture_id,
            "home_team": f"Home {fixture_id}",
            "away_team": f"Away {fixture_id}",
            "status": "NS",
            "home_xg_for": 1.6,
            "home_xg_against": 0.9,
            "away_xg_for": 1.4,
            "away_xg_against": 1.2,
            "home_sot_for": 5.0,
            "away_sot_for": 4.5,
            "home_big_for": 2.0,
            "away_big_for": 1.8,
            "home_form_pts": 2.1,
            "away_form_pts": 1.7,
            "home_goals_for_pg": 1.9,
            "away_goals_for_pg": 1.6,
            "home_goals_against_pg": 1.1,
            "away_goals_against_pg": 1.2,
            "home_scored_rate": 0.85,
            "away_scored_rate": 0.78,
            "home_clean_sheet_rate": 0.28,
            "away_clean_sheet_rate": 0.22,
            "home_btts_rate": 0.62,
            "away_btts_rate": 0.60,
            "home_over15_rate": 0.86,
            "away_over15_rate": 0.84,
            "home_over25_rate": 0.58,
            "away_over25_rate": 0.56,
            "home_rank": 4,
            "away_rank": 7,
            "home_points": 62,
            "away_points": 54,
            "home_goals_diff": 18,
            "away_goals_diff": 9,
            "home_urgency_score": 0.4,
            "away_urgency_score": 0.3,
            "league_team_count": 20,
            "home_recent_matches": 6,
            "away_recent_matches": 6,
            "home_recent_stats_matches_used": 5,
            "away_recent_stats_matches_used": 5,
            "home_recent_stats_coverage_ratio": 1.0,
            "away_recent_stats_coverage_ratio": 1.0,
            "home_recent_shots_for_pg": 15.0,
            "away_recent_shots_for_pg": 13.0,
            "home_recent_shots_against_pg": 10.0,
            "away_recent_shots_against_pg": 11.0,
            "home_recent_sot_for_pg": 6.0,
            "away_recent_sot_for_pg": 5.5,
            "home_recent_sot_against_pg": 3.5,
            "away_recent_sot_against_pg": 4.0,
            "home_recent_possession_pct": 56.0,
            "away_recent_possession_pct": 52.0,
            "home_recent_corners_for_pg": 6.0,
            "away_recent_corners_for_pg": 5.0,
            "home_recent_corners_against_pg": 4.0,
            "away_recent_corners_against_pg": 4.5,
            "home_recent_fouls_pg": 10.0,
            "away_recent_fouls_pg": 11.0,
            "home_recent_yellow_pg": 1.5,
            "away_recent_yellow_pg": 1.7,
            "home_recent_offsides_pg": 1.8,
            "away_recent_offsides_pg": 1.4,
            "home_recent_blocked_shots_pg": 4.0,
            "away_recent_blocked_shots_pg": 3.5,
            "recent_stats_quality_flag": "FULL",
            "data_enrichment_level": "OK",
            "home_motivation": 0.0,
            "away_motivation": 0.0,
        }
        row.update(injury_overrides)
        return row

    def score_rows_in_tmp(self, rows: list[dict[str, object]]) -> pd.DataFrame:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            processed = tmp_path / "processed"
            processed.mkdir()
            filtered_path = processed / "matches_league_filtered.csv"
            scored_path = processed / "matches_vsigma_scored_v3.csv"
            top_path = processed / "vsigma_top_candidates_v3.csv"
            report_path = processed / "vsigma_score_report_v3.csv"
            pd.DataFrame(rows).to_csv(filtered_path, index=False)

            with patch.object(score_matches_v3, "INPUT_PATH", filtered_path), patch.object(
                score_matches_v3, "OUTPUT_DIR", processed
            ), patch.object(score_matches_v3, "OUTPUT_SCORED", scored_path), patch.object(
                score_matches_v3, "OUTPUT_TOP", top_path
            ), patch.object(score_matches_v3, "OUTPUT_REPORT", report_path):
                score_matches_v3.main()

            return pd.read_csv(scored_path).sort_values("fixture_id").reset_index(drop=True)

    def test_injuries_none_unknown_scoring_has_no_material_execution_effect(self) -> None:
        full_zero = {
            "home_injuries_count": 0,
            "away_injuries_count": 0,
            "home_injuries_available_flag": 1,
            "away_injuries_available_flag": 1,
            "home_injuries_coverage_flag": "FULL",
            "away_injuries_coverage_flag": "FULL",
            "home_absence_risk_score": 0.0,
            "away_absence_risk_score": 0.0,
            "home_absence_severity_flag": "LOW",
            "away_absence_severity_flag": "LOW",
            "injuries_quality_flag": "FULL",
            "home_absences": 0,
            "away_absences": 0,
        }
        unknown = {
            "home_injuries_count": pd.NA,
            "away_injuries_count": pd.NA,
            "home_injuries_available_flag": 0,
            "away_injuries_available_flag": 0,
            "home_injuries_coverage_flag": "NONE",
            "away_injuries_coverage_flag": "NONE",
            "home_absence_risk_score": pd.NA,
            "away_absence_risk_score": pd.NA,
            "home_absence_severity_flag": "UNKNOWN",
            "away_absence_severity_flag": "UNKNOWN",
            "injuries_quality_flag": "NONE",
            "home_absences": pd.NA,
            "away_absences": pd.NA,
        }

        scored = self.score_rows_in_tmp(
            [
                self.strong_scoring_row(9001, full_zero),
                self.strong_scoring_row(9002, unknown),
            ]
        ).set_index("fixture_id")

        self.assertEqual(float(scored.loc[9002, "availability_uncertainty_penalty"]), 0.0)
        self.assertLess(
            abs(float(scored.loc[9001, "vsigma_pre_score"]) - float(scored.loc[9002, "vsigma_pre_score"])),
            0.2,
        )
        self.assertNotEqual(scored.loc[9002, "market_family_hint"], "UNDER_OR_TEAM_TOTAL_UNDER_CHECK")

    def test_full_high_absence_risk_is_advisory_tiny_score_nudge(self) -> None:
        full_zero = {
            "home_injuries_count": 0,
            "away_injuries_count": 0,
            "home_injuries_available_flag": 1,
            "away_injuries_available_flag": 1,
            "home_injuries_coverage_flag": "FULL",
            "away_injuries_coverage_flag": "FULL",
            "home_absence_risk_score": 0.0,
            "away_absence_risk_score": 0.0,
            "home_absence_severity_flag": "LOW",
            "away_absence_severity_flag": "LOW",
            "injuries_quality_flag": "FULL",
            "home_absences": 0,
            "away_absences": 0,
        }
        full_high = {
            **full_zero,
            "home_injuries_count": 3,
            "away_injuries_count": 2,
            "home_absence_risk_score": 3.2,
            "away_absence_risk_score": 1.4,
            "home_absence_severity_flag": "HIGH",
            "away_absence_severity_flag": "LOW",
            "home_absences": 3,
            "away_absences": 2,
        }

        scored = self.score_rows_in_tmp(
            [
                self.strong_scoring_row(9011, full_zero),
                self.strong_scoring_row(9012, full_high),
            ]
        ).set_index("fixture_id")

        self.assertGreater(float(scored.loc[9012, "availability_attack_penalty"]), 0.0)
        self.assertLessEqual(float(scored.loc[9012, "availability_attack_penalty"]), 0.1)
        self.assertLessEqual(float(scored.loc[9012, "absences_noise_penalty"]), 0.1)
        self.assertLess(
            float(scored.loc[9011, "vsigma_pre_score"]) - float(scored.loc[9012, "vsigma_pre_score"]),
            0.6,
        )

    def test_select_core_missing_injury_coverage_does_not_change_shortlist_score(self) -> None:
        base = {
            "date": "2026-05-10",
            "country": "England",
            "league": "Premier League",
            "league_tier": "TIER_1",
            "league_tier_rank": 1,
            "home_team": "Home",
            "away_team": "Away",
            "vsigma_priority": "A_ANALIZAR_PRIMERO",
            "market_family_hint": "OVER_OR_BTTS_CHECK",
            "data_warning": "OK_FULL_STATS",
            "data_enrichment_level": "OK",
            "home_recent_matches": 6,
            "away_recent_matches": 6,
            "vsigma_pre_score": 80.0,
            "availability_uncertainty_penalty": 0.0,
        }
        rows = [
            {
                **base,
                "fixture_id": 9101,
                "home_absence_risk_score": 0.0,
                "away_absence_risk_score": 0.0,
                "home_absence_severity_flag": "LOW",
                "away_absence_severity_flag": "LOW",
                "injuries_quality_flag": "FULL",
            },
            {
                **base,
                "fixture_id": 9102,
                "home_absence_risk_score": pd.NA,
                "away_absence_risk_score": pd.NA,
                "home_absence_severity_flag": "UNKNOWN",
                "away_absence_severity_flag": "UNKNOWN",
                "injuries_quality_flag": "NONE",
                "availability_uncertainty_penalty": 0.5,
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            processed = tmp_path / "processed"
            processed.mkdir()
            scored_path = processed / "matches_vsigma_scored_v3.csv"
            shortlist_path = processed / "vsigma_core_shortlist.csv"
            report_path = processed / "vsigma_core_shortlist_report.csv"
            pd.DataFrame(rows).to_csv(scored_path, index=False)

            with patch.object(select_core_candidates, "INPUT_PATH", scored_path), patch.object(
                select_core_candidates, "OUTPUT_DIR", processed
            ), patch.object(select_core_candidates, "OUTPUT_SHORTLIST", shortlist_path), patch.object(
                select_core_candidates, "OUTPUT_REPORT", report_path
            ):
                select_core_candidates.main()

            shortlist = pd.read_csv(shortlist_path).set_index("fixture_id")

        self.assertIn(9101, shortlist.index)
        self.assertIn(9102, shortlist.index)
        self.assertEqual(
            float(shortlist.loc[9101, "selection_score"]),
            float(shortlist.loc[9102, "selection_score"]),
        )

    def test_select_core_missing_lineup_coverage_does_not_change_shortlist_score(self) -> None:
        base = {
            "date": "2026-05-10",
            "country": "England",
            "league": "Premier League",
            "league_tier": "TIER_1",
            "league_tier_rank": 1,
            "home_team": "Home",
            "away_team": "Away",
            "vsigma_priority": "A_ANALIZAR_PRIMERO",
            "market_family_hint": "OVER_OR_BTTS_CHECK",
            "data_warning": "OK_FULL_STATS",
            "data_enrichment_level": "OK",
            "home_recent_matches": 6,
            "away_recent_matches": 6,
            "vsigma_pre_score": 80.0,
        }
        rows = [
            {
                **base,
                "fixture_id": 9111,
                "lineup_quality_flag": "FULL",
                "lineup_confirmation_score": 0.25,
                "lineup_uncertainty_penalty": 0.0,
            },
            {
                **base,
                "fixture_id": 9112,
                "lineup_quality_flag": "NONE",
                "lineup_confirmation_score": pd.NA,
                "lineup_uncertainty_penalty": 0.12,
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            processed = tmp_path / "processed"
            processed.mkdir()
            scored_path = processed / "matches_vsigma_scored_v3.csv"
            shortlist_path = processed / "vsigma_core_shortlist.csv"
            report_path = processed / "vsigma_core_shortlist_report.csv"
            pd.DataFrame(rows).to_csv(scored_path, index=False)

            with patch.object(select_core_candidates, "INPUT_PATH", scored_path), patch.object(
                select_core_candidates, "OUTPUT_DIR", processed
            ), patch.object(select_core_candidates, "OUTPUT_SHORTLIST", shortlist_path), patch.object(
                select_core_candidates, "OUTPUT_REPORT", report_path
            ):
                select_core_candidates.main()

            shortlist = pd.read_csv(shortlist_path).set_index("fixture_id")

        self.assertIn(9111, shortlist.index)
        self.assertIn(9112, shortlist.index)
        self.assertEqual(
            float(shortlist.loc[9111, "selection_score"]),
            float(shortlist.loc[9112, "selection_score"]),
        )

    def test_deep_analysis_weak_injury_coverage_note_does_not_downgrade_execution(self) -> None:
        row = self.market_fit_row(9201, "OVER_2_5", 1.60, 1.80)
        row.update(
            {
                "execution_verdict": "TOP_CORE",
                "injuries_quality_flag": "NONE",
                "home_injuries_coverage_flag": "NONE",
                "away_injuries_coverage_flag": "NONE",
                "home_absence_risk_score": pd.NA,
                "away_absence_risk_score": pd.NA,
                "home_absence_severity_flag": "UNKNOWN",
                "away_absence_severity_flag": "UNKNOWN",
                "availability_known_risk_score": 0.0,
            }
        )

        hardened = deep_analysis_candidates.apply_execution_market_fit_hardening(pd.DataFrame([row]))

        self.assertEqual(
            deep_analysis_candidates.availability_interpretation(hardened.loc[0]),
            deep_analysis_candidates.COVERAGE_TOO_WEAK_FOR_CONFIDENCE,
        )
        self.assertEqual(hardened.loc[0, "execution_market_fit_status"], "SAFE_OK")
        self.assertEqual(hardened.loc[0, "execution_verdict"], "TOP_CORE")
        self.assertEqual(hardened.loc[0, "final_recommendation"], "BET")

    def test_downstream_premium_core_survives_strong_evidence_with_weak_injury_coverage(self) -> None:
        row = self.market_fit_row(9301, "OVER_2_5", 1.60, 1.80)
        row.update(
            {
                "shortlist_rank": 1,
                "date": "2026-05-10",
                "league": "Premier League",
                "home_team": "Home",
                "away_team": "Away",
                "selection_score": 88.0,
                "confidence_band": "HIGH",
                "base_final_recommendation": "BET",
                "execution_verdict": "TOP_CORE",
                "production_governance_best_evidence_tier": "PREMIUM_EVIDENCE",
                "injuries_quality_flag": "NONE",
                "home_injuries_coverage_flag": "NONE",
                "away_injuries_coverage_flag": "NONE",
                "home_absence_risk_score": pd.NA,
                "away_absence_risk_score": pd.NA,
                "home_absence_severity_flag": "UNKNOWN",
                "away_absence_severity_flag": "UNKNOWN",
                "availability_known_risk_score": 0.0,
            }
        )
        hardened = deep_analysis_candidates.apply_execution_market_fit_hardening(pd.DataFrame([row]))

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_csv = tmp_path / "vsigma_deep_analysis_candidates.csv"
            hardened.to_csv(source_csv, index=False)
            _paths, exported, _summary = final_execution_exports.generate_final_execution_exports(
                source_csv=source_csv,
                output_dir=tmp_path,
            )
            _shortlist_paths, premium_core, shortlist, _bets_only, _shortlist_summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )

        self.assertEqual(exported.loc[0, "final_execution_bucket"], "APPROVED_PREMIUM")
        self.assertEqual(premium_core["fixture_id"].tolist(), [9301])
        self.assertEqual(shortlist["execution_shortlist_source"].tolist(), ["PREMIUM_CORE"])

    def test_full_high_absence_note_cannot_destroy_strong_premium_core_candidate(self) -> None:
        row = self.market_fit_row(9302, "OVER_1_5", 1.80, 1.45)
        row.update(
            {
                "shortlist_rank": 1,
                "date": "2026-05-10",
                "league": "Premier League",
                "home_team": "Home",
                "away_team": "Away",
                "selection_score": 88.0,
                "confidence_band": "HIGH",
                "base_final_recommendation": "BET",
                "execution_verdict": "TOP_CORE",
                "production_governance_best_evidence_tier": "PREMIUM_EVIDENCE",
                "injuries_quality_flag": "FULL",
                "home_injuries_coverage_flag": "FULL",
                "away_injuries_coverage_flag": "FULL",
                "home_absence_risk_score": 3.2,
                "away_absence_risk_score": 1.2,
                "home_absence_severity_flag": "HIGH",
                "away_absence_severity_flag": "LOW",
                "availability_known_risk_score": 4.4,
            }
        )
        hardened = deep_analysis_candidates.apply_execution_market_fit_hardening(pd.DataFrame([row]))

        self.assertEqual(
            deep_analysis_candidates.availability_interpretation(hardened.loc[0]),
            deep_analysis_candidates.ABSENCE_RISK_HIGH,
        )
        self.assertEqual(hardened.loc[0, "execution_market_fit_status"], "SAFE_OK")
        self.assertEqual(hardened.loc[0, "final_recommendation"], "BET")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_csv = tmp_path / "vsigma_deep_analysis_candidates.csv"
            hardened.to_csv(source_csv, index=False)
            _paths, exported, _summary = final_execution_exports.generate_final_execution_exports(
                source_csv=source_csv,
                output_dir=tmp_path,
            )
            _shortlist_paths, premium_core, shortlist, _bets_only, _shortlist_summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )

        self.assertEqual(exported.loc[0, "final_execution_bucket"], "APPROVED_PREMIUM")
        self.assertEqual(premium_core["fixture_id"].tolist(), [9302])
        self.assertEqual(shortlist["execution_shortlist_source"].tolist(), ["PREMIUM_CORE"])

    def test_lineup_uncertainty_alone_cannot_destroy_strong_premium_core_candidate(self) -> None:
        row = self.market_fit_row(9303, "OVER_1_5", 1.80, 1.45)
        row.update(
            {
                "shortlist_rank": 1,
                "date": "2026-05-10",
                "league": "Premier League",
                "home_team": "Home",
                "away_team": "Away",
                "selection_score": 88.0,
                "confidence_band": "HIGH",
                "base_final_recommendation": "BET",
                "execution_verdict": "TOP_CORE",
                "production_governance_best_evidence_tier": "PREMIUM_EVIDENCE",
                "lineup_quality_flag": "NONE",
                "lineup_activation_state": "INACTIVE",
                "home_lineup_available_flag": 0,
                "away_lineup_available_flag": 0,
                "lineup_confirmation_score": pd.NA,
                "lineup_uncertainty_penalty": 0.12,
            }
        )
        hardened = deep_analysis_candidates.apply_execution_market_fit_hardening(pd.DataFrame([row]))

        self.assertEqual(
            deep_analysis_candidates.lineup_interpretation(hardened.loc[0]),
            deep_analysis_candidates.LINEUP_INACTIVE_NO_TIMING_EDGE,
        )
        self.assertEqual(hardened.loc[0, "execution_market_fit_status"], "SAFE_OK")
        self.assertEqual(hardened.loc[0, "final_recommendation"], "BET")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_csv = tmp_path / "vsigma_deep_analysis_candidates.csv"
            hardened.to_csv(source_csv, index=False)
            _paths, exported, _summary = final_execution_exports.generate_final_execution_exports(
                source_csv=source_csv,
                output_dir=tmp_path,
            )
            _shortlist_paths, premium_core, shortlist, _bets_only, _shortlist_summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )

        self.assertEqual(exported.loc[0, "final_execution_bucket"], "APPROVED_PREMIUM")
        self.assertEqual(premium_core["fixture_id"].tolist(), [9303])
        self.assertEqual(shortlist["execution_shortlist_source"].tolist(), ["PREMIUM_CORE"])

    def test_availability_regression_advisory_mode_never_hard_downgrades(self) -> None:
        weak_coverage = pd.Series(
            {
                "market_primary": "BTTS_YES",
                "injuries_quality_flag": "NONE",
                "home_injuries_coverage_flag": "NONE",
                "away_injuries_coverage_flag": "NONE",
                "home_absence_risk_score": pd.NA,
                "away_absence_risk_score": pd.NA,
                "home_absence_severity_flag": "UNKNOWN",
                "away_absence_severity_flag": "UNKNOWN",
                "availability_known_risk_score": 0.0,
            }
        )
        full_high = pd.Series(
            {
                "market_primary": "BTTS_YES",
                "injuries_quality_flag": "FULL",
                "home_injuries_coverage_flag": "FULL",
                "away_injuries_coverage_flag": "FULL",
                "home_absence_risk_score": 3.2,
                "away_absence_risk_score": 1.2,
                "home_absence_severity_flag": "HIGH",
                "away_absence_severity_flag": "LOW",
                "availability_known_risk_score": 4.4,
            }
        )

        self.assertEqual(
            deep_analysis_candidates.availability_requires_execution_downgrade(weak_coverage, "BTTS_YES"),
            (False, ""),
        )
        self.assertEqual(
            deep_analysis_candidates.availability_requires_execution_downgrade(full_high, "BTTS_YES"),
            (False, ""),
        )

    def test_today_pipeline_runs_fixture_statistics_after_recent_form(self) -> None:
        steps = run_today_match_pipeline.PIPELINE_STEPS

        self.assertLess(
            steps.index("scripts/enrich_recent_form_v2.py"),
            steps.index("scripts/enrich_recent_fixture_statistics.py"),
        )
        self.assertLess(
            steps.index("scripts/enrich_recent_fixture_statistics.py"),
            steps.index("scripts/score_matches_v3.py"),
        )

    def test_today_pipeline_runs_injuries_after_fixture_statistics_before_scoring(self) -> None:
        steps = run_today_match_pipeline.PIPELINE_STEPS

        self.assertLess(
            steps.index("scripts/enrich_recent_fixture_statistics.py"),
            steps.index("scripts/enrich_injuries_availability.py"),
        )
        self.assertLess(
            steps.index("scripts/enrich_injuries_availability.py"),
            steps.index("scripts/score_matches_v3.py"),
        )

    def test_today_pipeline_runs_lineups_after_injuries_before_scoring(self) -> None:
        steps = run_today_match_pipeline.PIPELINE_STEPS

        self.assertLess(
            steps.index("scripts/enrich_injuries_availability.py"),
            steps.index("scripts/enrich_fixture_lineups.py"),
        )
        self.assertLess(
            steps.index("scripts/enrich_fixture_lineups.py"),
            steps.index("scripts/score_matches_v3.py"),
        )

    def test_today_snapshot_list_includes_fixture_statistics_report(self) -> None:
        names = {path.name for path in run_today_match_pipeline.TODAY_GENERATED_FILES}
        self.assertIn("recent_fixture_statistics_enrichment_report.csv", names)

    def test_today_snapshot_list_includes_injuries_report(self) -> None:
        names = {path.name for path in run_today_match_pipeline.TODAY_GENERATED_FILES}
        self.assertIn("injuries_availability_enrichment_report.csv", names)

    def test_today_snapshot_list_includes_lineups_report(self) -> None:
        names = {path.name for path in run_today_match_pipeline.TODAY_GENERATED_FILES}
        self.assertIn("fixture_lineups_enrichment_report.csv", names)

    def test_historical_pipeline_includes_injuries_step_and_snapshot_report(self) -> None:
        self.assertIn(
            "scripts/enrich_injuries_availability.py",
            run_historical_labeling_pipeline.PIPELINE_STEPS_BEFORE_DEEP,
        )
        self.assertIn(
            "injuries_availability_enrichment_report.csv",
            {path.name for path in run_historical_labeling_pipeline.SNAPSHOT_FILES},
        )

    def test_historical_pipeline_includes_lineups_step_and_snapshot_report(self) -> None:
        self.assertIn(
            "scripts/enrich_fixture_lineups.py",
            run_historical_labeling_pipeline.PIPELINE_STEPS_BEFORE_DEEP,
        )
        self.assertIn(
            "fixture_lineups_enrichment_report.csv",
            {path.name for path in run_historical_labeling_pipeline.SNAPSHOT_FILES},
        )

    def test_recent_fixture_statistics_survive_scoring_and_deep_analysis(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            processed = tmp_path / "processed"
            processed.mkdir()
            filtered_path = processed / "matches_league_filtered.csv"
            scored_path = processed / "matches_vsigma_scored_v3.csv"
            top_path = processed / "vsigma_top_candidates_v3.csv"
            score_report_path = processed / "vsigma_score_report_v3.csv"
            shortlist_path = processed / "vsigma_core_shortlist.csv"
            deep_path = processed / "vsigma_deep_analysis_candidates.csv"

            row = {
                "date": "2026-05-10",
                "country": "England",
                "league": "Premier League",
                "league_tier": "TIER_1",
                "league_tier_rank": 1,
                "fixture_id": 12345,
                "home_team": "Home",
                "away_team": "Away",
                "status": "NS",
                "home_form_pts": 2.0,
                "away_form_pts": 1.2,
                "home_goals_for_pg": 1.8,
                "away_goals_for_pg": 1.1,
                "home_goals_against_pg": 0.9,
                "away_goals_against_pg": 1.4,
                "home_scored_rate": 0.8,
                "away_scored_rate": 0.7,
                "home_clean_sheet_rate": 0.4,
                "away_clean_sheet_rate": 0.2,
                "home_btts_rate": 0.5,
                "away_btts_rate": 0.6,
                "home_over15_rate": 0.8,
                "away_over15_rate": 0.8,
                "home_over25_rate": 0.5,
                "away_over25_rate": 0.4,
                "home_recent_matches": 5,
                "away_recent_matches": 5,
                "home_rank": 4,
                "away_rank": 12,
                "home_points": 60,
                "away_points": 40,
                "home_goals_diff": 20,
                "away_goals_diff": -5,
                "home_urgency_score": 0.5,
                "away_urgency_score": 0.0,
                "league_team_count": 20,
                "home_recent_stats_matches_used": 5,
                "away_recent_stats_matches_used": 5,
                "home_recent_stats_coverage_ratio": 1.0,
                "away_recent_stats_coverage_ratio": 1.0,
                "home_recent_shots_for_pg": 15.0,
                "away_recent_shots_for_pg": 10.0,
                "home_recent_shots_against_pg": 8.0,
                "away_recent_shots_against_pg": 13.0,
                "home_recent_sot_for_pg": 6.0,
                "away_recent_sot_for_pg": 3.0,
                "home_recent_sot_against_pg": 2.0,
                "away_recent_sot_against_pg": 5.0,
                "home_recent_possession_pct": 58.0,
                "away_recent_possession_pct": 47.0,
                "home_recent_corners_for_pg": 6.0,
                "away_recent_corners_for_pg": 4.0,
                "home_recent_corners_against_pg": 3.0,
                "away_recent_corners_against_pg": 5.0,
                "home_recent_fouls_pg": 10.0,
                "away_recent_fouls_pg": 12.0,
                "home_recent_yellow_pg": 1.0,
                "away_recent_yellow_pg": 2.0,
                "home_recent_offsides_pg": 2.0,
                "away_recent_offsides_pg": 1.0,
                "home_recent_blocked_shots_pg": 4.0,
                "away_recent_blocked_shots_pg": 2.0,
                "recent_stats_quality_flag": "FULL",
                "home_injuries_count": 1,
                "away_injuries_count": 0,
                "home_injuries_available_flag": 1,
                "away_injuries_available_flag": 1,
                "home_injuries_coverage_flag": "FULL",
                "away_injuries_coverage_flag": "FULL",
                "home_absence_risk_score": 1.0,
                "away_absence_risk_score": 0.0,
                "home_absence_severity_flag": "LOW",
                "away_absence_severity_flag": "LOW",
                "injuries_quality_flag": "FULL",
                "home_lineup_available_flag": 1,
                "away_lineup_available_flag": 1,
                "home_lineup_quality_flag": "FULL",
                "away_lineup_quality_flag": "FULL",
                "lineup_quality_flag": "FULL",
                "lineup_activation_state": "ACTIVE",
                "lineup_activation_window_minutes": 90,
                "lineup_minutes_to_kickoff": 45,
                "lineup_timing_eligible_flag": 1,
                "lineup_structural_confidence_flag": 1,
                "home_lineup_known_starters_count": 11,
                "away_lineup_known_starters_count": 11,
                "home_lineup_bench_known_flag": 1,
                "away_lineup_bench_known_flag": 1,
                "home_lineup_attacker_count": 3,
                "away_lineup_attacker_count": 2,
                "home_lineup_defender_count": 4,
                "away_lineup_defender_count": 4,
                "home_lineup_midfielder_count": 3,
                "away_lineup_midfielder_count": 4,
                "home_lineup_goalkeeper_known_flag": 1,
                "away_lineup_goalkeeper_known_flag": 1,
                "home_lineup_attack_continuity_score": 0.40,
                "away_lineup_attack_continuity_score": 0.30,
                "home_lineup_defense_continuity_score": 0.40,
                "away_lineup_defense_continuity_score": 0.40,
                "lineup_confirmation_score": 0.38,
                "lineup_uncertainty_penalty": 0.0,
            }
            pd.DataFrame([row]).to_csv(filtered_path, index=False)

            with patch.object(score_matches_v3, "INPUT_PATH", filtered_path), patch.object(
                score_matches_v3, "OUTPUT_DIR", processed
            ), patch.object(score_matches_v3, "OUTPUT_SCORED", scored_path), patch.object(
                score_matches_v3, "OUTPUT_TOP", top_path
            ), patch.object(score_matches_v3, "OUTPUT_REPORT", score_report_path):
                score_matches_v3.main()

            scored = pd.read_csv(scored_path)
            self.assertIn("home_recent_sot_for_pg", scored.columns)
            self.assertIn("home_absence_risk_score", scored.columns)
            self.assertEqual(float(scored.loc[0, "home_recent_sot_for_pg"]), 6.0)
            self.assertEqual(float(scored.loc[0, "home_absence_risk_score"]), 1.0)
            self.assertEqual(scored.loc[0, "recent_stats_quality_flag"], "FULL")
            self.assertEqual(scored.loc[0, "injuries_quality_flag"], "FULL")
            self.assertEqual(scored.loc[0, "lineup_quality_flag"], "FULL")
            self.assertGreater(float(scored.loc[0, "recent_stats_process_score"]), 0.0)
            self.assertGreater(float(scored.loc[0, "lineup_score_nudge"]), 0.0)

            shortlist = scored.copy()
            shortlist["shortlist_rank"] = 1
            shortlist["shortlist_bucket"] = "TOP_CORE"
            shortlist["selection_score"] = 82.0
            shortlist.to_csv(shortlist_path, index=False)

            with patch.object(deep_analysis_candidates, "SHORTLIST_CSV", shortlist_path), patch.object(
                deep_analysis_candidates, "SCORED_CSV", scored_path
            ), patch.object(deep_analysis_candidates, "OUTPUT_CSV", deep_path), patch.object(
                deep_analysis_candidates,
                "PROMOTED_RULES_PRODUCTION_CSV",
                processed / "missing_promoted_rules.csv",
            ):
                deep_analysis_candidates.main()

            deep = pd.read_csv(deep_path)
            self.assertIn("home_recent_sot_for_pg", deep.columns)
            self.assertIn("home_absence_risk_score", deep.columns)
            self.assertEqual(float(deep.loc[0, "home_recent_sot_for_pg"]), 6.0)
            self.assertEqual(float(deep.loc[0, "home_absence_risk_score"]), 1.0)
            self.assertEqual(deep.loc[0, "recent_stats_quality_flag"], "FULL")
            self.assertEqual(deep.loc[0, "injuries_quality_flag"], "FULL")
            self.assertEqual(deep.loc[0, "lineup_quality_flag"], "FULL")
            self.assertEqual(deep.loc[0, "lineup_activation_state"], "ACTIVE")
            self.assertIn("availability=AVAILABILITY_SAFE", deep.loc[0, "reason_3"])
            self.assertIn("lineup=LINEUP_CONFIRMS_THESIS_ACTIVE", deep.loc[0, "reason_3"])
            self.assertGreater(float(deep.loc[0, "projected_home_goals"]), 0.35)

    def test_real_result_profit_and_odds_columns_are_resolved(self) -> None:
        df = backtest_vsigma.ensure_logical_columns(pd.DataFrame(REAL_SCHEMA_ROWS))

        self.assertEqual(df.loc[0, "market_result"], "WIN")
        self.assertEqual(df.loc[1, "market_result"], "LOSS")
        self.assertEqual(df.loc[5, "market_result"], "SKIPPED")
        self.assertEqual(float(df.loc[0, "units"]), 0.31)
        self.assertEqual(float(df.loc[1, "units"]), -1.0)
        self.assertEqual(float(df.loc[0, "odds"]), 1.31)
        self.assertEqual(float(df.loc[2, "odds"]), 1.94)
        self.assertEqual(float(df.loc[0, "model_edge_abs"]), 0.120141)
        self.assertEqual(backtest_vsigma.normalize_result("SKIPPED"), "NO_BET")

    def test_backtest_computes_graded_bets_from_real_labeled_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            labeled_path, deep_path = self.write_real_schema_inputs(tmp_path)
            output_dir = tmp_path / "out"

            argv = [
                "backtest_vsigma.py",
                "--labeled-csv",
                str(labeled_path),
                "--deep-csv",
                str(deep_path),
                "--output-dir",
                str(output_dir),
            ]
            with patch.object(sys, "argv", argv):
                backtest_vsigma.main()

            overall = pd.read_csv(output_dir / "vsigma_backtest_overall.csv")
            enriched = pd.read_csv(output_dir / "vsigma_backtest_enriched_source.csv")

            self.assertEqual(int(overall.loc[0, "rows_total"]), 7)
            self.assertEqual(int(overall.loc[0, "actionable_rows"]), 5)
            self.assertEqual(int(overall.loc[0, "graded_bets"]), 5)
            self.assertEqual(int(overall.loc[0, "wins"]), 4)
            self.assertEqual(int(overall.loc[0, "losses"]), 1)
            self.assertAlmostEqual(float(overall.loc[0, "profit_units"]), 1.12)
            self.assertAlmostEqual(float(overall.loc[0, "roi_pct"]), 22.4)

            graded = enriched[
                enriched["is_actionable"]
                & enriched["market_result_norm"].isin(["WIN", "LOSS", "PUSH", "VOID"])
            ]
            self.assertEqual(len(graded), 5)
            self.assertEqual(enriched["market_result_norm"].tolist()[-2:], ["NO_BET", "NO_BET"])
            self.assertAlmostEqual(float(enriched["profit_units_effective"].sum()), 1.12)

    def test_calibration_generates_output_files_from_backtest_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            labeled_path, deep_path = self.write_real_schema_inputs(tmp_path)
            backtest_output = tmp_path / "backtest"
            calibration_output = tmp_path / "calibration"

            with patch.object(
                sys,
                "argv",
                [
                    "backtest_vsigma.py",
                    "--labeled-csv",
                    str(labeled_path),
                    "--deep-csv",
                    str(deep_path),
                    "--output-dir",
                    str(backtest_output),
                ],
            ):
                backtest_vsigma.main()

            source_csv = backtest_output / "vsigma_backtest_enriched_source.csv"
            with patch.object(
                sys,
                "argv",
                [
                    "calibrate_vsigma_thresholds.py",
                    "--source-csv",
                    str(source_csv),
                    "--output-dir",
                    str(calibration_output),
                    "--min-graded",
                    "3",
                ],
            ):
                calibrate_vsigma_thresholds.main()

            candidates_path = calibration_output / "vsigma_threshold_calibration_candidates.csv"
            split_manifest_path = calibration_output / "vsigma_threshold_rolling_splits.csv"
            rolling_path = calibration_output / "vsigma_threshold_rolling_validation.csv"
            promoted_path = calibration_output / "vsigma_threshold_promoted_rules.csv"
            report_path = calibration_output / "vsigma_threshold_calibration_report.txt"

            self.assertTrue(candidates_path.exists())
            self.assertTrue(split_manifest_path.exists())
            self.assertTrue(rolling_path.exists())
            self.assertTrue(promoted_path.exists())
            self.assertTrue(report_path.exists())
            self.assertGreater(candidates_path.stat().st_size, 0)
            self.assertGreater(split_manifest_path.stat().st_size, 0)
            self.assertGreater(rolling_path.stat().st_size, 0)
            self.assertGreater(promoted_path.stat().st_size, 0)
            self.assertGreater(report_path.stat().st_size, 0)

            candidates = pd.read_csv(candidates_path)
            self.assertFalse(candidates.empty)
            self.assertIn("rule", candidates.columns)
            self.assertGreaterEqual(int(candidates["graded_bets"].max()), 3)
            report_text = report_path.read_text(encoding="utf-8")
            self.assertIn("VSIGMA THRESHOLD CALIBRATION", report_text)
            self.assertIn("ROLLING OUT-OF-SAMPLE VALIDATION", report_text)
            self.assertIn("Rolling split manifest", report_text)
            self.assertIn("PROMOTED RULES", report_text)

    def test_calibration_promotes_rules_from_rolling_chronological_validation(self) -> None:
        rows = [
            {
                "date_day": "2026-05-05",
                "fixture_id": 1,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 80,
                "market_primary": "OVER_1_5",
            },
            {
                "date_day": "2026-05-05",
                "fixture_id": 2,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 79,
                "market_primary": "OVER_1_5",
            },
            {
                "date_day": "2026-05-05",
                "fixture_id": 3,
                "market_result_norm": "LOSS",
                "is_actionable": True,
                "profit_units_effective": -1.0,
                "stake_units_effective": 1.0,
                "selection_score": 60,
                "market_primary": "UNDER_3_5",
            },
            {
                "date_day": "2026-05-06",
                "fixture_id": 4,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 81,
                "market_primary": "OVER_1_5",
            },
            {
                "date_day": "2026-05-06",
                "fixture_id": 5,
                "market_result_norm": "LOSS",
                "is_actionable": True,
                "profit_units_effective": -1.0,
                "stake_units_effective": 1.0,
                "selection_score": 55,
                "market_primary": "UNDER_3_5",
            },
            {
                "date_day": "2026-05-07",
                "fixture_id": 6,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 82,
                "market_primary": "OVER_1_5",
            },
            {
                "date_day": "2026-05-07",
                "fixture_id": 7,
                "market_result_norm": "LOSS",
                "is_actionable": True,
                "profit_units_effective": -1.0,
                "stake_units_effective": 1.0,
                "selection_score": 50,
                "market_primary": "UNDER_3_5",
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_csv = tmp_path / "source.csv"
            output_dir = tmp_path / "calibration"
            pd.DataFrame(rows).to_csv(source_csv, index=False)

            with patch.object(
                sys,
                "argv",
                [
                    "calibrate_vsigma_thresholds.py",
                    "--source-csv",
                    str(source_csv),
                    "--output-dir",
                    str(output_dir),
                    "--min-graded",
                    "1",
                    "--min-validation-graded",
                    "1",
                    "--min-validation-windows",
                    "2",
                    "--promote-top-n",
                    "0",
                ],
            ):
                calibrate_vsigma_thresholds.main()

            rolling = pd.read_csv(output_dir / "vsigma_threshold_rolling_validation.csv")
            split_manifest = pd.read_csv(output_dir / "vsigma_threshold_rolling_splits.csv")
            promoted = pd.read_csv(output_dir / "vsigma_threshold_promoted_rules.csv")

            self.assertEqual(split_manifest["split_id"].tolist(), [1, 2])
            self.assertEqual(
                split_manifest[["train_end_day", "validation_start_day"]].to_dict("records"),
                [
                    {"train_end_day": "2026-05-05", "validation_start_day": "2026-05-06"},
                    {"train_end_day": "2026-05-06", "validation_start_day": "2026-05-07"},
                ],
            )
            self.assertTrue(
                (
                    pd.to_datetime(split_manifest["train_end_day"])
                    < pd.to_datetime(split_manifest["validation_start_day"])
                ).all()
            )
            self.assertEqual(sorted(rolling["split_id"].unique().tolist()), [1, 2])
            self.assertEqual(
                rolling.groupby("split_id")["validation_start_day"].first().to_dict(),
                {1: "2026-05-06", 2: "2026-05-07"},
            )
            self.assertFalse(promoted.empty)

            score_rule = promoted[promoted["rule"] == "selection_score >= 79"]
            self.assertFalse(score_rule.empty)
            self.assertEqual(int(score_rule.iloc[0]["validation_windows"]), 2)
            self.assertEqual(str(score_rule.iloc[0]["source_split_ids"]), "1,2")
            self.assertAlmostEqual(float(score_rule.iloc[0]["validation_positive_window_rate_pct"]), 100.0)
            self.assertEqual(int(score_rule.iloc[0]["validation_graded_bets"]), 2)
            self.assertAlmostEqual(float(score_rule.iloc[0]["validation_profit_units"]), 1.0)

    def test_fixed_rolling_train_window_does_not_expand_history(self) -> None:
        rows = [
            {
                "date_day": "2026-05-01",
                "fixture_id": 1,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 90,
                "market_primary": "EARLY_EDGE",
            },
            {
                "date_day": "2026-05-02",
                "fixture_id": 2,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 91,
                "market_primary": "EARLY_EDGE",
            },
            {
                "date_day": "2026-05-03",
                "fixture_id": 3,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 60,
                "market_primary": "CURRENT_EDGE",
            },
            {
                "date_day": "2026-05-04",
                "fixture_id": 4,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 61,
                "market_primary": "CURRENT_EDGE",
            },
            {
                "date_day": "2026-05-05",
                "fixture_id": 5,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 92,
                "market_primary": "EARLY_EDGE",
            },
            {
                "date_day": "2026-05-05",
                "fixture_id": 6,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 62,
                "market_primary": "CURRENT_EDGE",
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_csv = tmp_path / "source.csv"
            output_dir = tmp_path / "calibration"
            pd.DataFrame(rows).to_csv(source_csv, index=False)

            with patch.object(
                sys,
                "argv",
                [
                    "calibrate_vsigma_thresholds.py",
                    "--source-csv",
                    str(source_csv),
                    "--output-dir",
                    str(output_dir),
                    "--min-graded",
                    "1",
                    "--min-train-days",
                    "2",
                    "--train-window-days",
                    "2",
                    "--validation-window-days",
                    "2",
                    "--min-validation-graded",
                    "1",
                    "--promote-top-n",
                    "0",
                ],
            ):
                calibrate_vsigma_thresholds.main()

            split_manifest = pd.read_csv(output_dir / "vsigma_threshold_rolling_splits.csv")
            rolling = pd.read_csv(output_dir / "vsigma_threshold_rolling_validation.csv")
            promoted = pd.read_csv(output_dir / "vsigma_threshold_promoted_rules.csv")
            report_text = (output_dir / "vsigma_threshold_calibration_report.txt").read_text(
                encoding="utf-8"
            )

            self.assertEqual(
                split_manifest[
                    [
                        "train_start_day",
                        "train_end_day",
                        "validation_start_day",
                        "validation_end_day",
                        "train_days",
                        "validation_days",
                    ]
                ].to_dict("records"),
                [
                    {
                        "train_start_day": "2026-05-01",
                        "train_end_day": "2026-05-02",
                        "validation_start_day": "2026-05-03",
                        "validation_end_day": "2026-05-04",
                        "train_days": 2,
                        "validation_days": 2,
                    },
                    {
                        "train_start_day": "2026-05-03",
                        "train_end_day": "2026-05-04",
                        "validation_start_day": "2026-05-05",
                        "validation_end_day": "2026-05-05",
                        "train_days": 2,
                        "validation_days": 1,
                    },
                ],
            )
            self.assertNotIn("market_primary == EARLY_EDGE", rolling["rule"].tolist())
            self.assertIn("market_primary == CURRENT_EDGE", rolling["rule"].tolist())
            self.assertFalse(promoted[promoted["rule"] == "market_primary == CURRENT_EDGE"].empty)
            self.assertIn("Train window days: 2", report_text)
            self.assertIn("Validation window days: 2", report_text)

    def test_rolling_validation_filters_unprofitable_train_rules(self) -> None:
        rows = [
            {
                "date_day": "2026-05-05",
                "fixture_id": 1,
                "market_result_norm": "LOSS",
                "is_actionable": True,
                "profit_units_effective": -1.0,
                "stake_units_effective": 1.0,
                "selection_score": 90,
                "market_primary": "RISKY_EDGE",
            },
            {
                "date_day": "2026-05-05",
                "fixture_id": 2,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 50,
                "market_primary": "STEADY_EDGE",
            },
            {
                "date_day": "2026-05-06",
                "fixture_id": 3,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 91,
                "market_primary": "RISKY_EDGE",
            },
            {
                "date_day": "2026-05-06",
                "fixture_id": 4,
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 51,
                "market_primary": "STEADY_EDGE",
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_csv = tmp_path / "source.csv"
            output_dir = tmp_path / "calibration"
            pd.DataFrame(rows).to_csv(source_csv, index=False)

            with patch.object(
                sys,
                "argv",
                [
                    "calibrate_vsigma_thresholds.py",
                    "--source-csv",
                    str(source_csv),
                    "--output-dir",
                    str(output_dir),
                    "--min-graded",
                    "1",
                    "--min-validation-graded",
                    "1",
                    "--promote-top-n",
                    "0",
                ],
            ):
                calibrate_vsigma_thresholds.main()

            rolling = pd.read_csv(output_dir / "vsigma_threshold_rolling_validation.csv")
            promoted = pd.read_csv(output_dir / "vsigma_threshold_promoted_rules.csv")
            report_text = (output_dir / "vsigma_threshold_calibration_report.txt").read_text(
                encoding="utf-8"
            )

            self.assertIn("Train candidate rows before filters", report_text)
            self.assertIn("Train candidate rows after train filters", report_text)
            self.assertNotIn("market_primary == RISKY_EDGE", rolling["rule"].tolist())
            self.assertNotIn("selection_score >= 90", rolling["rule"].tolist())
            self.assertIn("market_primary == STEADY_EDGE", rolling["rule"].tolist())
            self.assertFalse(promoted[promoted["rule"] == "market_primary == STEADY_EDGE"].empty)

    def test_runner_consumes_promoted_rules_and_writes_production_report(self) -> None:
        source_rows = [
            {
                "market_result_norm": "WIN",
                "is_actionable": True,
                "profit_units_effective": 0.5,
                "stake_units_effective": 1.0,
                "selection_score": 80,
                "market_primary": "OVER_1_5",
            },
            {
                "market_result_norm": "LOSS",
                "is_actionable": True,
                "profit_units_effective": -1.0,
                "stake_units_effective": 1.0,
                "selection_score": 70,
                "market_primary": "UNDER_3_5",
            },
            {
                "market_result_norm": "NO_BET",
                "is_actionable": False,
                "profit_units_effective": 0.0,
                "stake_units_effective": 0.0,
                "selection_score": 85,
                "market_primary": "OVER_1_5",
            },
        ]
        promoted_rows = [
            {
                "rule_type": "NUMERIC_THRESHOLD",
                "metric": "selection_score",
                "direction": ">=",
                "threshold": 79,
                "rule": "selection_score >= 79",
                "validation_windows": 2,
                "validation_positive_windows": 2,
                "validation_negative_windows": 0,
                "validation_positive_window_rate_pct": 100.0,
                "source_split_ids": "1,2",
                "first_validation_start_day": "2026-05-06",
                "last_validation_end_day": "2026-05-07",
                "validation_rows_total": 2,
                "validation_graded_bets": 2,
                "validation_wins": 2,
                "validation_losses": 0,
                "validation_pushes": 0,
                "validation_voids": 0,
                "validation_stake_units": 2.0,
                "validation_profit_units": 1.0,
                "validation_roi_pct": 50.0,
                "validation_hit_rate_decided_pct": 100.0,
                "promotion_reason": "test promotion",
            }
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output_dir = tmp_path / "out"
            output_dir.mkdir()
            source_path = output_dir / "vsigma_backtest_enriched_source.csv"
            promoted_path = output_dir / "vsigma_threshold_promoted_rules.csv"
            pd.DataFrame(source_rows).to_csv(source_path, index=False)
            pd.DataFrame(promoted_rows).to_csv(promoted_path, index=False)

            with patch.object(
                sys,
                "argv",
                [
                    "run_vsigma_backtest_calibration.py",
                    "--output-dir",
                    str(output_dir),
                ],
            ), patch.object(run_vsigma_backtest_calibration, "run_step") as run_step:
                run_vsigma_backtest_calibration.main()

            self.assertEqual(run_step.call_count, 2)
            production_csv = output_dir / "vsigma_promoted_rules_production_report.csv"
            production_txt = output_dir / "vsigma_promoted_rules_production_report.txt"
            self.assertTrue(production_csv.exists())
            self.assertTrue(production_txt.exists())

            report = pd.read_csv(production_csv)
            self.assertEqual(len(report), 1)
            self.assertEqual(report.loc[0, "production_status"], "PROMOTED_PRODUCTION_READY")
            self.assertEqual(int(report.loc[0, "current_rows_total"]), 2)
            self.assertEqual(int(report.loc[0, "current_actionable_rows"]), 1)
            self.assertEqual(int(report.loc[0, "current_graded_bets"]), 1)
            self.assertAlmostEqual(float(report.loc[0, "current_profit_units"]), 0.5)

            report_text = production_txt.read_text(encoding="utf-8")
            self.assertIn("VSIGMA PROMOTED RULES PRODUCTION REPORT", report_text)
            self.assertIn("PROMOTED_PRODUCTION_READY", report_text)

    def test_production_rule_tier_allows_premium_on_validated_window(self) -> None:
        tier, diagnostic = run_vsigma_backtest_calibration.classify_production_rule_tier(
            "PROMOTED_PRODUCTION_READY",
            {
                "validation_windows": 2,
                "validation_positive_window_rate_pct": 100.0,
                "validation_graded_bets": 16,
                "validation_roi_pct": 54.0,
                "current_graded_bets": 42,
                "current_roi_pct": 21.0,
                "current_match_rate_pct": 9.0,
                "current_actionable_coverage_pct": 60.0,
            },
        )

        self.assertEqual(tier, "PREMIUM_EVIDENCE")
        self.assertIn("strong repeated validation", diagnostic)

    def test_deep_analysis_governance_downgrades_actionable_without_promoted_match(self) -> None:
        candidates = pd.DataFrame(
            [
                {
                    "fixture_id": 1,
                    "execution_verdict": "TOP_CORE",
                    "final_recommendation": "BET",
                    "selection_score": 82,
                    "primary_odds_used": 1.80,
                    "primary_edge": 0.08,
                },
                {
                    "fixture_id": 2,
                    "execution_verdict": "CORE_SHORTLIST",
                    "final_recommendation": "LEAN_PLAY",
                    "selection_score": 72,
                    "primary_odds_used": 2.40,
                    "primary_edge": 0.03,
                },
                {
                    "fixture_id": 3,
                    "execution_verdict": "WATCH",
                    "final_recommendation": "WATCH",
                    "selection_score": 84,
                    "primary_odds_used": 1.70,
                    "primary_edge": 0.09,
                },
            ]
        )
        promoted_rules = pd.DataFrame(
            [
                {
                    "production_status": "PROMOTED_PRODUCTION_READY",
                    "production_rule_tier": "PREMIUM_EVIDENCE",
                    "rule_type": "NUMERIC_THRESHOLD",
                    "metric": "selection_score",
                    "direction": ">=",
                    "threshold": 80,
                    "rule": "selection_score >= 80",
                },
                {
                    "production_status": "PROMOTED_PRODUCTION_READY",
                    "production_rule_tier": "GENERIC_BROAD",
                    "rule_type": "NUMERIC_THRESHOLD",
                    "metric": "odds_num",
                    "direction": "<=",
                    "threshold": 1.90,
                    "rule": "odds_num <= 1.9",
                },
            ]
        )

        governed = deep_analysis_candidates.apply_promoted_rules_governance(
            candidates,
            promoted_rules,
        )

        self.assertEqual(governed.loc[0, "production_governance_status"], "APPROVED_BY_PREMIUM_PROMOTED_RULE")
        self.assertEqual(governed.loc[0, "final_recommendation"], "BET")
        self.assertEqual(int(governed.loc[0, "production_governance_rule_count"]), 2)
        self.assertEqual(int(governed.loc[0, "production_governance_premium_rule_count"]), 1)
        self.assertEqual(int(governed.loc[0, "production_governance_generic_rule_count"]), 1)
        self.assertEqual(governed.loc[0, "production_governance_best_evidence_tier"], "PREMIUM_EVIDENCE")
        self.assertEqual(governed.loc[0, "base_final_recommendation"], "BET")

        self.assertEqual(
            governed.loc[1, "production_governance_status"],
            "DOWNGRADED_NO_PROMOTED_RULE_MATCH",
        )
        self.assertEqual(governed.loc[1, "base_final_recommendation"], "LEAN_PLAY")
        self.assertEqual(governed.loc[1, "execution_verdict"], "WATCH")
        self.assertEqual(governed.loc[1, "final_recommendation"], "WATCH")

        self.assertEqual(
            governed.loc[2, "production_governance_status"],
            "ANNOTATED_NON_ACTIONABLE_RULE_MATCH",
        )
        self.assertEqual(governed.loc[2, "final_recommendation"], "WATCH")

    def test_deep_analysis_governance_downgrades_actionable_with_generic_rules_only(self) -> None:
        candidates = pd.DataFrame(
            [
                {
                    "fixture_id": 10,
                    "execution_verdict": "TOP_CORE",
                    "final_recommendation": "BET",
                    "selection_score": 74,
                    "primary_odds_used": 1.75,
                    "primary_edge": 0.08,
                },
            ]
        )
        promoted_rules = pd.DataFrame(
            [
                {
                    "production_status": "PROMOTED_PRODUCTION_READY",
                    "production_rule_tier": "GENERIC_BROAD",
                    "rule_type": "NUMERIC_THRESHOLD",
                    "metric": "odds_num",
                    "direction": "<=",
                    "threshold": 2.57,
                    "rule": "odds_num <= 2.57",
                },
            ]
        )

        governed = deep_analysis_candidates.apply_promoted_rules_governance(
            candidates,
            promoted_rules,
        )

        self.assertEqual(
            governed.loc[0, "production_governance_status"],
            "DOWNGRADED_GENERIC_PROMOTED_RULE_ONLY",
        )
        self.assertEqual(governed.loc[0, "execution_verdict"], "WATCH")
        self.assertEqual(governed.loc[0, "final_recommendation"], "WATCH")
        self.assertEqual(int(governed.loc[0, "production_governance_generic_rule_count"]), 1)

    def market_fit_row(
        self,
        fixture_id: int,
        market: str,
        projected_home: float,
        projected_away: float,
        model_prob: float = 0.80,
        edge: float = 0.17,
        odds: float = 1.80,
        market_alt: str = "OVER_1_5",
        production_status: str = "APPROVED_BY_PREMIUM_PROMOTED_RULE",
        base_verdict: str = "TOP_CORE",
        final_recommendation: str = "BET",
        likely_scoreline: str = "1-1 / 1-0 / 0-1",
    ) -> dict[str, object]:
        return {
            "fixture_id": fixture_id,
            "market_primary": market,
            "market_alt": market_alt,
            "base_execution_verdict": base_verdict,
            "final_recommendation": final_recommendation,
            "production_governance_status": production_status,
            "primary_model_prob": model_prob,
            "primary_edge": edge,
            "primary_odds_used": odds,
            "projected_home_goals": projected_home,
            "projected_away_goals": projected_away,
            "likely_scoreline": likely_scoreline,
        }

    def test_execution_market_fit_away_win_hard_filter(self) -> None:
        rows = pd.DataFrame(
            [
                self.market_fit_row(1, "AWAY_WIN", 0.90, 2.10, market_alt="AWAY_DNB"),
                self.market_fit_row(2, "AWAY_WIN", 1.10, 1.80, model_prob=0.78, market_alt="AWAY_DNB"),
            ]
        )

        hardened = deep_analysis_candidates.apply_execution_market_fit_hardening(rows)

        self.assertEqual(hardened.loc[0, "execution_market_fit_status"], "SAFE_OK")
        self.assertEqual(hardened.loc[0, "final_recommendation"], "BET")
        self.assertEqual(hardened.loc[1, "execution_market_fit_status"], "MARKET_FIT_DOWNGRADED")
        self.assertEqual(hardened.loc[1, "execution_fragility_reason"], "AWAY_WIN_DRAW_RISK")
        self.assertEqual(hardened.loc[1, "execution_preferred_safer_market"], "AWAY_DNB")
        self.assertEqual(hardened.loc[1, "final_recommendation"], "WATCH")

    def test_execution_market_fit_over_25_sync_gate(self) -> None:
        rows = pd.DataFrame(
            [
                self.market_fit_row(11, "OVER_2_5", 1.50, 1.85),
                self.market_fit_row(12, "OVER_2_5", 1.60, 0.70, market_alt="OVER_1_5"),
            ]
        )

        hardened = deep_analysis_candidates.apply_execution_market_fit_hardening(rows)

        self.assertEqual(hardened.loc[0, "execution_market_fit_status"], "SAFE_OK")
        self.assertEqual(hardened.loc[0, "final_recommendation"], "BET")
        self.assertEqual(hardened.loc[1, "execution_market_fit_status"], "MARKET_FIT_DOWNGRADED")
        self.assertEqual(hardened.loc[1, "execution_fragility_reason"], "OVER_2_5_DAMAGE_SYNC_FAIL")
        self.assertEqual(hardened.loc[1, "execution_preferred_safer_market"], "OVER_1_5")
        self.assertEqual(hardened.loc[1, "final_recommendation"], "WATCH")

    def test_execution_market_fit_under_35_avalanche_veto(self) -> None:
        rows = pd.DataFrame(
            [
                self.market_fit_row(21, "UNDER_3_5", 1.20, 1.30),
                self.market_fit_row(
                    22,
                    "UNDER_3_5",
                    2.55,
                    0.75,
                    likely_scoreline="3-0 / 3-1 / 2-0",
                ),
            ]
        )

        hardened = deep_analysis_candidates.apply_execution_market_fit_hardening(rows)

        self.assertEqual(hardened.loc[0, "execution_market_fit_status"], "SAFE_OK")
        self.assertEqual(hardened.loc[0, "final_recommendation"], "BET")
        self.assertEqual(hardened.loc[1, "execution_market_fit_status"], "MARKET_FIT_BLOCKED")
        self.assertEqual(hardened.loc[1, "execution_fragility_reason"], "UNDER_3_5_AVALANCHE_RISK")
        self.assertEqual(hardened.loc[1, "final_recommendation"], "WATCH")

    def test_final_execution_exports_split_governed_candidates(self) -> None:
        rows = [
            {
                "shortlist_rank": 1,
                "fixture_id": 1,
                "home_team": "Approved Home",
                "away_team": "Approved Away",
                "selection_score": 84,
                "primary_edge": 0.08,
                "base_final_recommendation": "BET",
                "execution_verdict": "TOP_CORE",
                "final_recommendation": "BET",
                "production_governance_best_evidence_tier": "PREMIUM_EVIDENCE",
                "production_governance_status": "APPROVED_BY_PREMIUM_PROMOTED_RULE",
            },
            {
                "shortlist_rank": 2,
                "fixture_id": 5,
                "home_team": "Standard Home",
                "away_team": "Standard Away",
                "selection_score": 80,
                "primary_edge": 0.04,
                "base_final_recommendation": "LEAN_PLAY",
                "execution_verdict": "WATCH",
                "final_recommendation": "LEAN_PLAY",
                "production_governance_best_evidence_tier": "STANDARD_EVIDENCE",
                "production_governance_status": "APPROVED_BY_PROMOTED_RULE",
            },
            {
                "shortlist_rank": 3,
                "fixture_id": 2,
                "home_team": "Downgraded Home",
                "away_team": "Downgraded Away",
                "selection_score": 74,
                "primary_edge": 0.03,
                "base_final_recommendation": "LEAN_PLAY",
                "execution_verdict": "WATCH",
                "final_recommendation": "WATCH",
                "production_governance_best_evidence_tier": "",
                "production_governance_status": "DOWNGRADED_NO_PROMOTED_RULE_MATCH",
            },
            {
                "shortlist_rank": 4,
                "fixture_id": 3,
                "home_team": "Blocked Home",
                "away_team": "Blocked Away",
                "selection_score": 80,
                "primary_edge": 0.06,
                "base_final_recommendation": "BET",
                "execution_verdict": "WATCH",
                "final_recommendation": "BET",
                "production_governance_best_evidence_tier": "",
                "production_governance_status": "NO_PROMOTED_RULES_AVAILABLE",
            },
            {
                "shortlist_rank": 5,
                "fixture_id": 4,
                "home_team": "Watch Home",
                "away_team": "Watch Away",
                "selection_score": 66,
                "primary_edge": 0.01,
                "base_final_recommendation": "WATCH",
                "execution_verdict": "WATCH",
                "final_recommendation": "WATCH",
                "production_governance_best_evidence_tier": "STANDARD_EVIDENCE",
                "production_governance_status": "ANNOTATED_NON_ACTIONABLE_RULE_MATCH",
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_csv = tmp_path / "vsigma_deep_analysis_candidates.csv"
            pd.DataFrame(rows).to_csv(source_csv, index=False)

            paths, exported, summary = final_execution_exports.generate_final_execution_exports(
                source_csv=source_csv,
                output_dir=tmp_path,
            )

            for key in [
                "APPROVED_PREMIUM",
                "APPROVED_STANDARD",
                "APPROVED",
                "DOWNGRADED",
                "BLOCKED",
                "WATCH",
                "SUMMARY",
            ]:
                self.assertTrue(paths[key].exists())

            self.assertEqual(
                exported[["fixture_id", "final_execution_bucket"]].to_dict("records"),
                [
                    {"fixture_id": 1, "final_execution_bucket": "APPROVED_PREMIUM"},
                    {"fixture_id": 5, "final_execution_bucket": "APPROVED_STANDARD"},
                    {"fixture_id": 2, "final_execution_bucket": "DOWNGRADED"},
                    {"fixture_id": 3, "final_execution_bucket": "BLOCKED"},
                    {"fixture_id": 4, "final_execution_bucket": "WATCH"},
                ],
            )

            approved = pd.read_csv(paths["APPROVED"])
            approved_premium = pd.read_csv(paths["APPROVED_PREMIUM"])
            approved_standard = pd.read_csv(paths["APPROVED_STANDARD"])
            downgraded = pd.read_csv(paths["DOWNGRADED"])
            blocked = pd.read_csv(paths["BLOCKED"])
            watch = pd.read_csv(paths["WATCH"])

            self.assertEqual(approved["fixture_id"].tolist(), [1, 5])
            self.assertEqual(approved_premium["fixture_id"].tolist(), [1])
            self.assertEqual(approved_standard["fixture_id"].tolist(), [5])
            self.assertEqual(downgraded["fixture_id"].tolist(), [2])
            self.assertEqual(blocked["fixture_id"].tolist(), [3])
            self.assertEqual(watch["fixture_id"].tolist(), [4])
            self.assertIn("final_execution_reason", approved.columns)

            by_bucket = summary[summary["summary_scope"] == "by_final_execution_bucket"]
            self.assertEqual(
                by_bucket.set_index("final_execution_bucket")["rows_total"].to_dict(),
                {
                    "APPROVED_PREMIUM": 1,
                    "APPROVED_STANDARD": 1,
                    "BLOCKED": 1,
                    "DOWNGRADED": 1,
                    "WATCH": 1,
                },
            )

    def test_market_fit_downgrades_do_not_flow_into_downstream_execution(self) -> None:
        rows = [
            {
                "shortlist_rank": 1,
                "fixture_id": 1001,
                "date": "2026-05-09",
                "league": "Integration League",
                "home_team": "Safe Home",
                "away_team": "Safe Away",
                "confidence_band": "HIGH",
                "market_primary": "OVER_1_5",
                "selection_score": 90.0,
                "primary_model_prob": 0.84,
                "primary_odds_used": 1.50,
                "primary_edge": 0.17,
                "base_execution_verdict": "TOP_CORE",
                "base_final_recommendation": "BET",
                "execution_verdict": "TOP_CORE",
                "final_recommendation": "BET",
                "production_governance_status": "APPROVED_BY_PREMIUM_PROMOTED_RULE",
                "production_governance_best_evidence_tier": "PREMIUM_EVIDENCE",
                "execution_market_fit_status": "SAFE_OK",
                "execution_fragility_reason": "",
            },
            {
                "shortlist_rank": 2,
                "fixture_id": 1002,
                "date": "2026-05-09",
                "league": "Integration League",
                "home_team": "Fragile Home",
                "away_team": "Fragile Away",
                "confidence_band": "HIGH",
                "market_primary": "OVER_2_5",
                "selection_score": 89.0,
                "primary_model_prob": 0.80,
                "primary_odds_used": 1.90,
                "primary_edge": 0.18,
                "base_execution_verdict": "TOP_CORE",
                "base_final_recommendation": "BET",
                "execution_verdict": "TOP_CORE",
                "final_recommendation": "BET",
                "production_governance_status": "APPROVED_BY_PREMIUM_PROMOTED_RULE",
                "production_governance_best_evidence_tier": "PREMIUM_EVIDENCE",
                "execution_market_fit_status": "MARKET_FIT_DOWNGRADED",
                "execution_fragility_reason": "OVER_2_5_DAMAGE_SYNC_FAIL",
                "execution_preferred_safer_market": "OVER_1_5",
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_csv = tmp_path / "vsigma_deep_analysis_candidates.csv"
            pd.DataFrame(rows).to_csv(source_csv, index=False)

            _paths, exported, _summary = final_execution_exports.generate_final_execution_exports(
                source_csv=source_csv,
                output_dir=tmp_path,
            )
            report, errors = validate_final_execution_exports.validate_exports(tmp_path)
            self.assertEqual(errors, [])
            self.assertTrue(report["status"].eq("PASS").all())
            self.assertEqual(
                exported.set_index("fixture_id")["final_execution_bucket"].to_dict(),
                {1001: "APPROVED_PREMIUM", 1002: "DOWNGRADED"},
            )

            _shortlist_paths, _premium_core, shortlist, _bets_only, _shortlist_summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )
            self.assertEqual(shortlist["fixture_id"].tolist(), [1001])

            _mode_paths, safe, balanced, aggressive, _mode_summary = (
                build_execution_pick_modes.build_execution_pick_modes(tmp_path)
            )
            self.assertEqual(safe["fixture_id"].tolist(), [1001])
            self.assertEqual(balanced["fixture_id"].tolist(), [1001])
            self.assertEqual(aggressive["fixture_id"].tolist(), [1001])

    def shortlist_row(
        self,
        fixture_id: int,
        bucket: str,
        recommendation: str,
        base_verdict: str,
        selection_score: float,
        edge: float,
        league: str,
        market: str,
        rank: int,
        model_prob: float = 0.75,
        odds: float = 1.8,
    ) -> dict[str, object]:
        return {
            "shortlist_rank": rank,
            "fixture_id": fixture_id,
            "date": "2026-05-09",
            "league": league,
            "home_team": f"Home {fixture_id}",
            "away_team": f"Away {fixture_id}",
            "market_primary": market,
            "selection_score": selection_score,
            "confidence_band": "HIGH",
            "primary_model_prob": model_prob,
            "primary_odds_used": odds,
            "primary_edge": edge,
            "base_execution_verdict": base_verdict,
            "final_recommendation": recommendation,
            "final_execution_bucket": bucket,
        }

    def write_shortlist_inputs(
        self,
        processed_dir: Path,
        premium_rows: list[dict[str, object]],
        standard_rows: list[dict[str, object]],
    ) -> None:
        base_columns = build_today_execution_shortlist.REQUIRED_COLUMNS + ["date", "home_team", "away_team"]
        extra_columns = []
        for row in premium_rows + standard_rows:
            extra_columns.extend([col for col in row if col not in base_columns])
        columns = list(dict.fromkeys(base_columns + extra_columns))
        pd.DataFrame(premium_rows, columns=columns).to_csv(
            processed_dir / build_today_execution_shortlist.PREMIUM_INPUT,
            index=False,
        )
        pd.DataFrame(standard_rows, columns=columns).to_csv(
            processed_dir / build_today_execution_shortlist.STANDARD_INPUT,
            index=False,
        )

    def test_execution_shortlist_ranking_and_caps(self) -> None:
        premium_rows = [
            self.shortlist_row(1, "APPROVED_PREMIUM", "BET", "TOP_CORE", 95, 0.20, "League A", "OVER_1_5", 1),
            self.shortlist_row(2, "APPROVED_PREMIUM", "BET", "TOP_CORE", 94, 0.19, "League A", "OVER_1_5", 2),
            self.shortlist_row(3, "APPROVED_PREMIUM", "BET", "TOP_CORE", 93, 0.18, "League A", "OVER_1_5", 3),
            self.shortlist_row(4, "APPROVED_PREMIUM", "BET", "TOP_CORE", 92, 0.17, "League B", "OVER_2_5", 4),
            self.shortlist_row(4, "APPROVED_PREMIUM", "BET", "TOP_CORE", 91, 0.16, "League C", "BTTS_YES", 5),
            self.shortlist_row(5, "APPROVED_PREMIUM", "BET", "TOP_CORE", 90, 0.15, "League B", "OVER_2_5", 6),
            self.shortlist_row(6, "APPROVED_PREMIUM", "BET", "TOP_CORE", 89, 0.14, "League C", "BTTS_YES", 7),
            self.shortlist_row(7, "APPROVED_PREMIUM", "BET", "TOP_CORE", 88, 0.13, "League D", "HOME_WIN", 8),
            self.shortlist_row(8, "APPROVED_PREMIUM", "BET", "TOP_CORE", 87, 0.12, "League D", "AWAY_WIN", 9),
            self.shortlist_row(9, "APPROVED_PREMIUM", "BET", "TOP_CORE", 86, 0.11, "League E", "DRAW", 10),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_shortlist_inputs(tmp_path, premium_rows, [])

            _paths, _core, shortlist, bets_only, summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )

            self.assertLessEqual(len(shortlist), 8)
            self.assertEqual(len(shortlist), 8)
            self.assertEqual(len(bets_only), 8)
            self.assertNotIn(3, shortlist["fixture_id"].tolist())
            self.assertEqual(shortlist["fixture_id"].tolist().count(4), 1)
            self.assertLessEqual(int(shortlist["league"].value_counts().max()), 2)
            self.assertLessEqual(int(shortlist["market_primary"].value_counts().max()), 2)
            self.assertEqual(shortlist["execution_rank"].tolist(), list(range(1, 9)))
            self.assertTrue(shortlist["execution_score"].is_monotonic_decreasing)
            self.assertEqual(
                int(summary.loc[summary["metric"].eq("final_shortlist_rows"), "rows_total"].iloc[0]),
                8,
            )

    def test_execution_shortlist_premium_core_extended_and_standard_fill(self) -> None:
        premium_rows = [
            self.shortlist_row(101, "APPROVED_PREMIUM", "BET", "TOP_CORE", 82, 0.08, "League A", "OVER_1_5", 1),
            self.shortlist_row(102, "APPROVED_PREMIUM", "LEAN_PLAY", "WATCH", 99, 0.12, "League B", "OVER_1_5", 2, model_prob=0.85),
            self.shortlist_row(103, "APPROVED_PREMIUM", "BET", "WATCH", 98, 0.10, "League C", "OVER_1_5", 3, model_prob=0.85),
            self.shortlist_row(104, "APPROVED_PREMIUM", "BET", "WATCH", 97, 0.20, "League D", "HOME_WIN", 4, model_prob=0.88),
            self.shortlist_row(105, "APPROVED_PREMIUM", "BET", "WATCH", 96, 0.03, "League E", "OVER_1_5", 5, model_prob=0.85),
            self.shortlist_row(106, "APPROVED_PREMIUM", "BET", "WATCH", 95, 0.12, "League F", "OVER_1_5", 6, model_prob=0.79),
            self.shortlist_row(107, "APPROVED_PREMIUM", "BET", "WATCH", 94, 0.12, "League G", "OVER_2_5", 7, model_prob=0.86),
            self.shortlist_row(108, "APPROVED_PREMIUM", "BET", "CORE_SHORTLIST", 100, -0.01, "League H", "MKT_H", 8),
            self.shortlist_row(109, "APPROVED_PREMIUM", "BET", "CORE_SHORTLIST", 100, 0.01, "League I", "MKT_I", 9, odds=pd.NA),
        ]
        standard_rows = [
            self.shortlist_row(201, "APPROVED_STANDARD", "BET", "TOP_CORE", 93, 0.04, "League H", "MKT_H", 10),
            self.shortlist_row(202, "APPROVED_STANDARD", "BET", "TOP_CORE", 92, 0.04, "League I", "MKT_I", 11),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_shortlist_inputs(tmp_path, premium_rows, standard_rows)

            _paths, premium_core, shortlist, bets_only, summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )

            self.assertEqual(premium_core["fixture_id"].tolist(), [101])
            self.assertEqual(len(shortlist), 5)
            self.assertIn(201, shortlist["fixture_id"].tolist())
            self.assertIn(202, shortlist["fixture_id"].tolist())
            self.assertNotIn(102, shortlist["fixture_id"].tolist())
            self.assertNotIn(104, shortlist["fixture_id"].tolist())
            self.assertNotIn(105, shortlist["fixture_id"].tolist())
            self.assertNotIn(106, shortlist["fixture_id"].tolist())
            self.assertNotIn(108, shortlist["fixture_id"].tolist())
            self.assertNotIn(109, shortlist["fixture_id"].tolist())
            self.assertEqual(
                shortlist.set_index("fixture_id").loc[101, "execution_shortlist_source"],
                "PREMIUM_CORE",
            )
            self.assertEqual(
                shortlist.set_index("fixture_id").loc[103, "execution_shortlist_source"],
                "PREMIUM_EXTENDED",
            )
            self.assertEqual(
                shortlist.set_index("fixture_id").loc[201, "execution_shortlist_source"],
                "STANDARD_FILL",
            )
            self.assertEqual(len(bets_only), 5)

            eligibility = summary[summary["summary_scope"].eq("eligibility")]
            self.assertEqual(
                eligibility.set_index("metric")["rows_total"].to_dict(),
                {
                    "premium_core_rows": 1,
                    "premium_extended_eligible_rows": 2,
                    "standard_eligible_rows": 2,
                },
            )

    def test_premium_core_survives_unchanged_under_extended_governance(self) -> None:
        premium_rows = [
            self.shortlist_row(
                301,
                "APPROVED_PREMIUM",
                "BET",
                "TOP_CORE",
                82,
                0.02,
                "League A",
                "HOME_WIN",
                1,
                model_prob=0.70,
            )
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_shortlist_inputs(tmp_path, premium_rows, [])

            _paths, premium_core, shortlist, _bets_only, _summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )

        self.assertEqual(premium_core["fixture_id"].tolist(), [301])
        self.assertEqual(shortlist["fixture_id"].tolist(), [301])
        self.assertEqual(
            shortlist.loc[0, "premium_extended_governance_status"],
            "PREMIUM_CORE_PROTECTED",
        )

    def test_weak_premium_extended_candidates_are_downgraded_out_of_execution(self) -> None:
        premium_rows = [
            self.shortlist_row(311, "APPROVED_PREMIUM", "LEAN_PLAY", "WATCH", 99, 0.12, "League A", "OVER_1_5", 1, model_prob=0.85),
            self.shortlist_row(312, "APPROVED_PREMIUM", "BET", "WATCH", 98, 0.07, "League B", "OVER_1_5", 2, model_prob=0.85),
            self.shortlist_row(313, "APPROVED_PREMIUM", "BET", "WATCH", 97, 0.12, "League C", "BTTS_YES", 3, model_prob=0.88),
            self.shortlist_row(314, "APPROVED_PREMIUM", "BET", "WATCH", 96, 0.12, "League D", "OVER_2_5", 4, model_prob=0.79),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_shortlist_inputs(tmp_path, premium_rows, [])

            _paths, premium_core, shortlist, bets_only, summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )

        self.assertTrue(premium_core.empty)
        self.assertTrue(shortlist.empty)
        self.assertTrue(bets_only.empty)
        self.assertEqual(
            int(summary.loc[summary["metric"].eq("premium_extended_eligible_rows"), "rows_total"].iloc[0]),
            0,
        )

    def test_stronger_premium_extended_rows_still_survive(self) -> None:
        premium_rows = [
            self.shortlist_row(321, "APPROVED_PREMIUM", "BET", "WATCH", 94, 0.10, "League A", "OVER_1_5", 1, model_prob=0.84),
            self.shortlist_row(322, "APPROVED_PREMIUM", "BET", "WATCH", 93, 0.18, "League B", "UNDER_3_5", 2, model_prob=0.88),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_shortlist_inputs(tmp_path, premium_rows, [])

            _paths, _premium_core, shortlist, bets_only, summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )

        self.assertEqual(shortlist["fixture_id"].tolist(), [322, 321])
        self.assertEqual(shortlist["execution_shortlist_source"].tolist(), ["PREMIUM_EXTENDED", "PREMIUM_EXTENDED"])
        self.assertEqual(set(shortlist["premium_extended_governance_status"]), {"EXTENDED_QUALITY_OK"})
        self.assertEqual(len(bets_only), 2)
        self.assertEqual(
            int(summary.loc[summary["metric"].eq("premium_extended_eligible_rows"), "rows_total"].iloc[0]),
            2,
        )

    def test_shortlist_and_pick_modes_do_not_overfill_from_weak_extended_rows(self) -> None:
        premium_rows = [
            self.shortlist_row(331, "APPROVED_PREMIUM", "BET", "TOP_CORE", 90, 0.10, "League A", "OVER_1_5", 1, model_prob=0.84),
            self.shortlist_row(332, "APPROVED_PREMIUM", "BET", "WATCH", 99, 0.07, "League B", "OVER_1_5", 2, model_prob=0.86),
            self.shortlist_row(333, "APPROVED_PREMIUM", "LEAN_PLAY", "WATCH", 98, 0.12, "League C", "OVER_2_5", 3, model_prob=0.86),
            self.shortlist_row(334, "APPROVED_PREMIUM", "BET", "WATCH", 97, 0.20, "League D", "AWAY_WIN", 4, model_prob=0.88),
        ]
        standard_rows = [
            self.shortlist_row(431, "APPROVED_STANDARD", "BET", "TOP_CORE", 88, 0.06, "League E", "HOME_DNB", 5, model_prob=0.80),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_shortlist_inputs(tmp_path, premium_rows, standard_rows)

            _paths, _premium_core, shortlist, _bets_only, _summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )
            _mode_paths, safe, balanced, aggressive, _mode_summary = (
                build_execution_pick_modes.build_execution_pick_modes(tmp_path)
            )

        self.assertEqual(shortlist["fixture_id"].tolist(), [331, 431])
        self.assertEqual(safe["fixture_id"].tolist(), [331, 431])
        self.assertEqual(balanced["fixture_id"].tolist(), [331, 431])
        self.assertEqual(aggressive["fixture_id"].tolist(), [331, 431])

    def test_premium_extended_mask_is_stricter_than_previous_positive_edge_rule(self) -> None:
        row = self.shortlist_row(
            341,
            "APPROVED_PREMIUM",
            "LEAN_PLAY",
            "WATCH",
            92,
            0.03,
            "League A",
            "OVER_1_5",
            1,
            model_prob=0.85,
        )
        normalized = build_today_execution_shortlist.add_execution_score(
            build_today_execution_shortlist.normalize_inputs(
                pd.DataFrame([row]),
                "APPROVED_PREMIUM",
                "test",
            )
        )
        legacy_mask = (
            normalized["_final_execution_bucket_norm"].eq("APPROVED_PREMIUM")
            & normalized["_final_recommendation_norm"].isin(build_today_execution_shortlist.ACTIONABLE_RECOMMENDATIONS)
            & normalized["primary_edge"].gt(0)
            & normalized["primary_odds_used"].notna()
        )
        governed = build_today_execution_shortlist.add_premium_extended_governance(normalized)

        self.assertTrue(bool(legacy_mask.iloc[0]))
        self.assertFalse(bool(build_today_execution_shortlist.premium_extended_mask(governed).iloc[0]))
        self.assertEqual(governed.loc[0, "premium_extended_governance_status"], "EXTENDED_DOWNGRADED_TO_WATCH")

    def test_generic_broad_extended_row_cannot_become_executable_because_it_almost_passes(self) -> None:
        generic = self.shortlist_row(
            351,
            "APPROVED_PREMIUM",
            "BET",
            "WATCH",
            98,
            0.20,
            "League A",
            "OVER_1_5",
            1,
            model_prob=0.90,
        )
        generic.update(
            {
                "production_governance_status": "APPROVED_BY_PREMIUM_PROMOTED_RULE",
                "production_governance_best_evidence_tier": "GENERIC_BROAD",
                "production_governance_premium_rule_count": 0,
                "production_governance_generic_rule_count": 10,
            }
        )
        strong = self.shortlist_row(
            352,
            "APPROVED_PREMIUM",
            "BET",
            "WATCH",
            97,
            0.12,
            "League B",
            "OVER_2_5",
            2,
            model_prob=0.86,
        )
        strong.update(
            {
                "production_governance_status": "APPROVED_BY_PREMIUM_PROMOTED_RULE",
                "production_governance_best_evidence_tier": "PREMIUM_EVIDENCE",
                "production_governance_premium_rule_count": 1,
                "production_governance_generic_rule_count": 10,
            }
        )

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_shortlist_inputs(tmp_path, [generic, strong], [])

            _paths, _premium_core, shortlist, _bets_only, _summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )

        self.assertEqual(shortlist["fixture_id"].tolist(), [352])

    def test_execution_shortlist_outputs_include_pick_explanations(self) -> None:
        premium_rows = [
            self.shortlist_row(401, "APPROVED_PREMIUM", "BET", "TOP_CORE", 95, 0.12, "League A", "OVER_1_5", 1, model_prob=0.84),
            self.shortlist_row(402, "APPROVED_PREMIUM", "BET", "WATCH", 94, 0.11, "League B", "OVER_2_5", 2, model_prob=0.86),
        ]
        premium_rows[0].update(
            {
                "recent_stats_quality_flag": "FULL",
                "recent_stats_process_score": 4.0,
                "home_recent_stats_matches_used": 5,
                "away_recent_stats_matches_used": 5,
                "home_recent_stats_coverage_ratio": 1.0,
                "away_recent_stats_coverage_ratio": 1.0,
                "execution_market_fit_status": "SAFE_OK",
                "production_governance_best_evidence_tier": "PREMIUM_EVIDENCE",
            }
        )

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_shortlist_inputs(tmp_path, premium_rows, [])

            paths, _premium_core, shortlist, _bets_only, _summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )
            written = pd.read_csv(paths["EXECUTION_SHORTLIST"])
            explanations = pd.read_csv(paths["PICK_EXPLANATIONS"])

        for col in pick_explanations.EXPLANATION_COLUMNS:
            self.assertIn(col, shortlist.columns)
            self.assertIn(col, written.columns)
            self.assertIn(col, explanations.columns)
        self.assertFalse(shortlist["pick_failure_mode"].isna().any())
        self.assertIn("CORE_GATE_PASSED", shortlist.loc[0, "pick_bucket_rationale"])
        self.assertIn("EXECUTION_SHORTLIST_SORT", shortlist.loc[0, "pick_rank_rationale"])
        self.assertIn("execution_score=", shortlist.loc[0, "pick_rank_rationale"])

    def test_pick_explanation_bucket_rationale_reflects_actual_source_bucket(self) -> None:
        premium_rows = [
            self.shortlist_row(411, "APPROVED_PREMIUM", "BET", "TOP_CORE", 90, 0.10, "League A", "OVER_1_5", 1, model_prob=0.84),
            self.shortlist_row(412, "APPROVED_PREMIUM", "BET", "WATCH", 99, 0.12, "League B", "OVER_2_5", 2, model_prob=0.86),
        ]
        standard_rows = [
            self.shortlist_row(413, "APPROVED_STANDARD", "BET", "TOP_CORE", 88, 0.06, "League C", "HOME_DNB", 3, model_prob=0.80),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_shortlist_inputs(tmp_path, premium_rows, standard_rows)

            _paths, _premium_core, shortlist, _bets_only, _summary = (
                build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)
            )

        rationale = shortlist.set_index("fixture_id")["pick_bucket_rationale"].to_dict()
        self.assertIn("PREMIUM_CORE", rationale[411])
        self.assertIn("PREMIUM_EXTENDED", rationale[412])
        self.assertIn("STANDARD_FILL", rationale[413])

    def test_pick_mode_outputs_include_explanations_and_mode_rank_logic(self) -> None:
        premium_rows = [
            self.shortlist_row(421, "APPROVED_PREMIUM", "BET", "TOP_CORE", 90, 0.10, "League A", "OVER_1_5", 1, model_prob=0.84),
            self.shortlist_row(422, "APPROVED_PREMIUM", "BET", "WATCH", 99, 0.12, "League B", "OVER_2_5", 2, model_prob=0.86),
        ]
        standard_rows = [
            self.shortlist_row(423, "APPROVED_STANDARD", "BET", "TOP_CORE", 88, 0.06, "League C", "HOME_DNB", 3, model_prob=0.80),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_shortlist_inputs(tmp_path, premium_rows, standard_rows)
            build_today_execution_shortlist.build_today_execution_shortlist(tmp_path)

            paths, safe, balanced, aggressive, _summary = build_execution_pick_modes.build_execution_pick_modes(tmp_path)
            written_safe = pd.read_csv(paths["SAFE_TOP5"])

        for output in [safe, balanced, aggressive, written_safe]:
            for col in pick_explanations.EXPLANATION_COLUMNS:
                self.assertIn(col, output.columns)
            self.assertFalse(output["pick_failure_mode"].isna().any())
        self.assertIn("SAFE_TOP5_SORT", safe.loc[0, "pick_rank_rationale"])
        self.assertIn("safe_score=", safe.loc[0, "pick_rank_rationale"])
        self.assertIn("BALANCED_TOP5_SORT", balanced.loc[0, "pick_rank_rationale"])
        self.assertIn("AGGRESSIVE_TOP5_SORT", aggressive.loc[0, "pick_rank_rationale"])

    def test_pick_explanation_tags_are_controlled_and_non_generic(self) -> None:
        row = pd.Series(
            {
                "execution_shortlist_source": "PREMIUM_CORE",
                "final_execution_bucket": "APPROVED_PREMIUM",
                "final_recommendation": "BET",
                "base_execution_verdict": "TOP_CORE",
                "market_primary": "BTTS_YES",
                "execution_market_fit_status": "SAFE_OK",
                "primary_edge": 0.15,
                "primary_model_prob": 0.82,
                "primary_odds_used": 1.90,
                "execution_score": 120.0,
                "selection_score": 95.0,
                "recent_stats_quality_flag": "FULL",
                "recent_stats_process_score": 4.0,
                "injuries_quality_flag": "NONE",
                "lineup_activation_state": "INACTIVE",
                "lineup_quality_flag": "NONE",
            }
        )

        explained = pick_explanations.explanation_for_row(row)
        tags = [tag for tag in explained["pick_supporting_edges"].split(";") if tag]

        self.assertTrue(tags)
        self.assertTrue(set(tags).issubset(pick_explanations.CONTROLLED_EXPLANATION_TAGS))
        self.assertNotIn("good pick", explained["pick_main_why"].lower())
        self.assertEqual(explained["pick_failure_mode"], "BTTS_BREAK")

    def test_today_pipeline_snapshot_list_includes_pick_explanation_outputs(self) -> None:
        names = {path.name for path in run_today_match_pipeline.TODAY_GENERATED_FILES}
        self.assertTrue(
            {
                "vsigma_today_pick_explanations.csv",
                "vsigma_today_pick_explanations_report.txt",
            }.issubset(names)
        )

    def league_coverage_payload(self) -> dict[str, object]:
        return {
            "response": [
                {
                    "league": {"id": 39, "name": "Premier League", "type": "League"},
                    "country": {"name": "England"},
                    "seasons": [
                        {
                            "year": 2026,
                            "current": True,
                            "start": "2026-08-01",
                            "end": "2027-05-31",
                            "coverage": {
                                "fixtures": {
                                    "events": True,
                                    "lineups": True,
                                    "statistics_fixtures": True,
                                    "statistics_players": True,
                                },
                                "standings": True,
                                "odds": True,
                                "players": True,
                                "injuries": True,
                                "predictions": True,
                                "top_scorers": True,
                                "top_assists": True,
                                "top_cards": True,
                            },
                        }
                    ],
                }
            ]
        }

    def test_league_coverage_response_normalizes_into_matrix(self) -> None:
        matrix = build_api_league_coverage_matrix.normalize_leagues_payload(
            self.league_coverage_payload(),
            requested_league_id=39,
            requested_season=2026,
        )

        self.assertEqual(len(matrix), 1)
        row = matrix.iloc[0]
        self.assertEqual(int(row["league_id"]), 39)
        self.assertEqual(row["league_coverage_class"], "COVERAGE_RICH")
        self.assertEqual(int(row["league_has_fixture_stats_coverage"]), 1)
        self.assertEqual(int(row["league_has_lineups_coverage"]), 1)
        self.assertEqual(int(row["league_has_injuries_coverage"]), 1)

    def test_league_coverage_class_assignment_logic(self) -> None:
        rich_flags = {
            "league_has_fixtures_coverage": True,
            "league_has_standings_coverage": True,
            "league_has_odds_coverage": True,
            "league_has_fixture_stats_coverage": True,
            "league_has_injuries_coverage": True,
            "league_has_lineups_coverage": True,
        }
        thin_flags = {key: False for key in rich_flags}
        thin_flags["league_has_fixtures_coverage"] = True

        self.assertEqual(build_api_league_coverage_matrix.coverage_class_from_flags(rich_flags)[0], "COVERAGE_RICH")
        self.assertEqual(build_api_league_coverage_matrix.coverage_class_from_flags(thin_flags)[0], "COVERAGE_THIN")

    def test_active_match_dataset_receives_league_coverage_fields(self) -> None:
        matrix = build_api_league_coverage_matrix.normalize_leagues_payload(
            self.league_coverage_payload(),
            requested_league_id=39,
            requested_season=2026,
        )
        matches = pd.DataFrame(
            [
                {
                    "league_id": 39,
                    "season": 2026,
                    "league": "Premier League",
                    "country": "England",
                    "fixture_id": 100,
                }
            ]
        )

        merged = build_api_league_coverage_matrix.merge_coverage_into_matches(matches, matrix)

        self.assertEqual(merged.loc[0, "league_coverage_class"], "COVERAGE_RICH")
        self.assertEqual(int(merged.loc[0, "league_has_fixture_stats_coverage"]), 1)
        self.assertGreater(float(merged.loc[0, "league_data_reliability_score"]), 0.9)

    def test_missing_coverage_is_uncertainty_not_fake_team_weakness(self) -> None:
        row = pd.DataFrame(
            [
                {
                    "league_coverage_source_status": "OFFICIAL_API_NO_SEASON_MATCH",
                    "league_coverage_class": "COVERAGE_MINIMAL",
                    "league_has_fixture_stats_coverage": 0,
                    "league_data_reliability_score": 0.40,
                }
            ]
        )

        self.assertEqual(float(score_matches_v3.stats_coverage_multiplier(row).iloc[0]), 0.0)
        self.assertLessEqual(float(score_matches_v3.coverage_uncertainty_penalty_series(row).iloc[0]), 1.25)

    def test_coverage_confidence_effect_is_modest_for_strong_picks(self) -> None:
        strong_thin = pd.Series(
            {
                "league_coverage_source_status": "OFFICIAL_API",
                "league_coverage_class": "COVERAGE_MINIMAL",
            }
        )

        penalty = deep_analysis_candidates.coverage_confidence_penalty(strong_thin)
        self.assertEqual(penalty, 3.0)
        self.assertEqual(deep_analysis_candidates.confidence_band(100.0 - penalty), "HIGH")

    def test_pick_explanations_carry_coverage_rationale_when_relevant(self) -> None:
        row = pd.Series(
            {
                "execution_shortlist_source": "PREMIUM_EXTENDED",
                "final_execution_bucket": "APPROVED_PREMIUM",
                "final_recommendation": "BET",
                "market_primary": "OVER_2_5",
                "execution_market_fit_status": "SAFE_OK",
                "primary_edge": 0.12,
                "primary_model_prob": 0.86,
                "primary_odds_used": 1.80,
                "execution_score": 110.0,
                "selection_score": 90.0,
                "league_coverage_source_status": "OFFICIAL_API",
                "league_coverage_class": "COVERAGE_THIN",
                "league_has_fixture_stats_coverage": 0,
                "league_has_injuries_coverage": 0,
                "league_has_lineups_coverage": 0,
                "league_has_odds_coverage": 1,
                "lineup_activation_state": "INACTIVE",
                "lineup_quality_flag": "NONE",
                "injuries_quality_flag": "NONE",
            }
        )

        explanation = pick_explanations.explanation_for_row(row)

        self.assertIn("COVERAGE_THIN_NO_EXTRA_TRUST", explanation["pick_supporting_edges"])
        self.assertIn("COVERAGE_LIMITS_STATS", explanation["pick_supporting_edges"])
        self.assertIn("COVERAGE_LIMITS_INJURIES", explanation["pick_supporting_edges"])

    def test_today_pipeline_snapshot_list_includes_coverage_outputs(self) -> None:
        names = {path.name for path in run_today_match_pipeline.TODAY_GENERATED_FILES}
        self.assertTrue(
            {
                "vsigma_api_league_coverage_matrix.csv",
                "vsigma_api_league_coverage_summary.csv",
                "vsigma_api_league_coverage_report.txt",
            }.issubset(names)
        )

    def test_today_pipeline_step_order_includes_execution_shortlist_after_validation(self) -> None:
        steps = run_today_match_pipeline.PIPELINE_STEPS
        validation_index = steps.index("scripts/validate_final_execution_exports.py")
        self.assertEqual(
            steps[validation_index + 1],
            "scripts/build_today_execution_shortlist.py",
        )

    def pick_mode_row(
        self,
        fixture_id: int,
        source: str,
        bucket: str,
        recommendation: str,
        verdict: str,
        market: str,
        league: str,
        execution_score: float,
        selection_score: float,
        edge: float,
        model_prob: float,
        odds: float,
        rank: int,
        confidence: str = "HIGH",
    ) -> dict[str, object]:
        return {
            "execution_rank": rank,
            "execution_score": execution_score,
            "execution_shortlist_source": source,
            "fixture_id": fixture_id,
            "league": league,
            "market_primary": market,
            "selection_score": selection_score,
            "primary_model_prob": model_prob,
            "primary_odds_used": odds,
            "primary_edge": edge,
            "base_execution_verdict": verdict,
            "final_recommendation": recommendation,
            "final_execution_bucket": bucket,
            "confidence_band": confidence,
            "home_team": f"Home {fixture_id}",
            "away_team": f"Away {fixture_id}",
        }

    def test_execution_pick_modes_stable_when_only_injury_uncertainty_changes(self) -> None:
        rows = pd.DataFrame(
            [
                self.pick_mode_row(1, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "CORE_SHORTLIST", "OVER_1_5", "League A", 100, 80, 0.08, 0.80, 1.45, 1),
                self.pick_mode_row(2, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "OVER_2_5", "League B", 98, 78, 0.09, 0.79, 1.80, 2),
                self.pick_mode_row(3, "STANDARD_FILL", "APPROVED_STANDARD", "BET", "TOP_CORE", "HOME_DNB", "League C", 96, 76, 0.07, 0.77, 1.60, 3),
            ]
        )
        weak = rows.copy()
        weak["injuries_quality_flag"] = "NONE"
        weak["home_injuries_coverage_flag"] = "NONE"
        weak["away_injuries_coverage_flag"] = "NONE"
        weak["home_absence_risk_score"] = pd.NA
        weak["away_absence_risk_score"] = pd.NA

        full = rows.copy()
        full["injuries_quality_flag"] = "FULL"
        full["home_injuries_coverage_flag"] = "FULL"
        full["away_injuries_coverage_flag"] = "FULL"
        full["home_absence_risk_score"] = 0.0
        full["away_absence_risk_score"] = 0.0

        weak_scored = build_execution_pick_modes.normalize_and_score(weak)
        full_scored = build_execution_pick_modes.normalize_and_score(full)

        self.assertEqual(
            build_execution_pick_modes.select_safe(weak_scored)["fixture_id"].tolist(),
            build_execution_pick_modes.select_safe(full_scored)["fixture_id"].tolist(),
        )
        self.assertEqual(
            build_execution_pick_modes.select_balanced(weak_scored)["fixture_id"].tolist(),
            build_execution_pick_modes.select_balanced(full_scored)["fixture_id"].tolist(),
        )
        self.assertEqual(
            build_execution_pick_modes.select_aggressive(weak_scored)["fixture_id"].tolist(),
            build_execution_pick_modes.select_aggressive(full_scored)["fixture_id"].tolist(),
        )

    def test_execution_pick_modes_stable_when_only_lineup_uncertainty_changes(self) -> None:
        rows = pd.DataFrame(
            [
                self.pick_mode_row(1, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "CORE_SHORTLIST", "OVER_1_5", "League A", 100, 80, 0.08, 0.80, 1.45, 1),
                self.pick_mode_row(2, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "OVER_2_5", "League B", 98, 78, 0.09, 0.79, 1.80, 2),
                self.pick_mode_row(3, "STANDARD_FILL", "APPROVED_STANDARD", "BET", "TOP_CORE", "HOME_DNB", "League C", 96, 76, 0.07, 0.77, 1.60, 3),
            ]
        )
        unknown = rows.copy()
        unknown["lineup_quality_flag"] = "NONE"
        unknown["lineup_activation_state"] = "INACTIVE"
        unknown["lineup_timing_eligible_flag"] = 0
        unknown["lineup_structural_confidence_flag"] = 0
        unknown["home_lineup_available_flag"] = 0
        unknown["away_lineup_available_flag"] = 0
        unknown["lineup_confirmation_score"] = pd.NA
        unknown["lineup_uncertainty_penalty"] = 0.12

        full = rows.copy()
        full["lineup_quality_flag"] = "FULL"
        full["lineup_activation_state"] = "ADVISORY_ONLY"
        full["lineup_timing_eligible_flag"] = 0
        full["lineup_structural_confidence_flag"] = 1
        full["home_lineup_available_flag"] = 1
        full["away_lineup_available_flag"] = 1
        full["lineup_confirmation_score"] = 0.25
        full["lineup_uncertainty_penalty"] = 0.0

        unknown_scored = build_execution_pick_modes.normalize_and_score(unknown)
        full_scored = build_execution_pick_modes.normalize_and_score(full)

        self.assertEqual(
            build_execution_pick_modes.select_safe(unknown_scored)["fixture_id"].tolist(),
            build_execution_pick_modes.select_safe(full_scored)["fixture_id"].tolist(),
        )
        self.assertEqual(
            build_execution_pick_modes.select_balanced(unknown_scored)["fixture_id"].tolist(),
            build_execution_pick_modes.select_balanced(full_scored)["fixture_id"].tolist(),
        )
        self.assertEqual(
            build_execution_pick_modes.select_aggressive(unknown_scored)["fixture_id"].tolist(),
            build_execution_pick_modes.select_aggressive(full_scored)["fixture_id"].tolist(),
        )

    def test_execution_pick_modes_safe_top5_ranking_and_caps(self) -> None:
        rows = pd.DataFrame(
            [
                self.pick_mode_row(1, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "CORE_SHORTLIST", "OVER_1_5", "League A", 100, 80, 0.08, 0.80, 1.45, 1),
                self.pick_mode_row(2, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "CORE_SHORTLIST", "UNDER_3_5", "League A", 99, 79, 0.08, 0.80, 1.55, 2),
                self.pick_mode_row(3, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "OVER_2_5", "League B", 98, 78, 0.09, 0.79, 1.80, 3),
                self.pick_mode_row(4, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "OVER_2_5", "League C", 97, 77, 0.09, 0.78, 1.80, 4),
                self.pick_mode_row(5, "STANDARD_FILL", "APPROVED_STANDARD", "BET", "TOP_CORE", "HOME_DNB", "League D", 96, 76, 0.07, 0.77, 1.60, 5),
                self.pick_mode_row(6, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "AWAY_WIN", "League E", 95, 75, 0.20, 0.76, 2.10, 6),
            ]
        )

        scored = build_execution_pick_modes.normalize_and_score(rows)
        safe = build_execution_pick_modes.select_safe(scored)

        self.assertLessEqual(len(safe), 5)
        self.assertNotIn(2, safe["fixture_id"].tolist())
        self.assertNotIn(4, safe["fixture_id"].tolist())
        self.assertLessEqual(int(safe["league"].value_counts().max()), 1)
        self.assertLessEqual(int(safe["market_primary"].value_counts().max()), 1)
        self.assertEqual(safe["mode_rank"].tolist(), list(range(1, len(safe) + 1)))
        self.assertEqual(safe.iloc[0]["fixture_id"], 1)

    def test_execution_pick_modes_safe_prioritizes_core_and_safe_market_over_raw_edge(self) -> None:
        rows = pd.DataFrame(
            [
                self.pick_mode_row(1, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "CORE_SHORTLIST", "OVER_1_5", "League A", 90, 80, 0.06, 0.82, 1.45, 1),
                self.pick_mode_row(2, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "AWAY_WIN", "League B", 110, 95, 0.30, 0.86, 2.20, 2),
            ]
        )

        safe = build_execution_pick_modes.select_safe(build_execution_pick_modes.normalize_and_score(rows))

        self.assertEqual(safe.iloc[0]["fixture_id"], 1)
        self.assertEqual(safe.iloc[0]["mode_entry_reason"], "PREMIUM_CORE_BET_HIGH_SAFETY")

    def test_execution_pick_modes_balanced_and_aggressive_order_differ(self) -> None:
        rows = pd.DataFrame(
            [
                self.pick_mode_row(1, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "OVER_1_5", "League A", 120, 95, 0.06, 0.88, 1.35, 1),
                self.pick_mode_row(2, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "AWAY_WIN", "League B", 105, 82, 0.24, 0.75, 2.30, 2),
                self.pick_mode_row(3, "STANDARD_FILL", "APPROVED_STANDARD", "BET", "TOP_CORE", "OVER_2_5", "League C", 94, 81, 0.12, 0.76, 2.05, 3),
            ]
        )
        scored = build_execution_pick_modes.normalize_and_score(rows)
        balanced = build_execution_pick_modes.select_balanced(scored)
        aggressive = build_execution_pick_modes.select_aggressive(scored)

        self.assertNotEqual(balanced["fixture_id"].tolist(), aggressive["fixture_id"].tolist())
        self.assertEqual(balanced.iloc[0]["fixture_id"], 1)
        self.assertEqual(aggressive.iloc[0]["fixture_id"], 2)

    def test_today_pipeline_step_order_includes_pick_modes_after_execution_shortlist(self) -> None:
        steps = run_today_match_pipeline.PIPELINE_STEPS
        shortlist_index = steps.index("scripts/build_today_execution_shortlist.py")
        self.assertEqual(
            steps[shortlist_index + 1],
            "scripts/build_execution_pick_modes.py",
        )

    def test_today_pipeline_snapshot_list_includes_pick_mode_outputs(self) -> None:
        names = {path.name for path in run_today_match_pipeline.TODAY_GENERATED_FILES}
        self.assertTrue(
            {
                "vsigma_today_safe_top5.csv",
                "vsigma_today_balanced_top5.csv",
                "vsigma_today_aggressive_top5.csv",
                "vsigma_today_pick_modes_summary.csv",
            }.issubset(names)
        )

    def competition_row(
        self,
        execution_rank: int,
        fixture_id: int,
        source: str,
        bucket: str,
        recommendation: str,
        base_verdict: str,
        market: str,
        selection_score: float,
        execution_score: float,
        model_prob: float,
        edge: float,
        league: str,
        market_fit: str = "SAFE_OK",
        stats_quality: str = "FULL",
        process_score: float = 3.6,
    ) -> dict[str, object]:
        return {
            "execution_rank": execution_rank,
            "shortlist_rank": execution_rank,
            "execution_shortlist_source": source,
            "fixture_id": fixture_id,
            "date": "2026-05-09",
            "league": league,
            "home_team": f"Home {fixture_id}",
            "away_team": f"Away {fixture_id}",
            "market_primary": market,
            "final_execution_bucket": bucket,
            "final_recommendation": recommendation,
            "base_execution_verdict": base_verdict,
            "selection_score": selection_score,
            "execution_score": execution_score,
            "primary_model_prob": model_prob,
            "primary_odds_used": 1.55,
            "primary_edge": edge,
            "execution_market_fit_status": market_fit,
            "confidence_band": "HIGH",
            "recent_stats_quality_flag": stats_quality,
            "recent_stats_process_score": process_score,
            "home_recent_stats_matches_used": 5,
            "away_recent_stats_matches_used": 5,
            "home_recent_stats_coverage_ratio": 0.8,
            "away_recent_stats_coverage_ratio": 0.8,
            "league_coverage_class": "COVERAGE_RICH",
            "lineup_activation_state": "INACTIVE",
            "lineup_quality_flag": "NONE",
        }

    def test_competition_accuracy_outputs_created_and_stricter_than_shortlist(self) -> None:
        rows = [
            self.competition_row(1, 701, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "TOP_CORE", "OVER_1_5", 92, 122, 0.86, 0.12, "League A"),
            self.competition_row(2, 702, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "OVER_1_5", 91, 113, 0.85, 0.13, "League B"),
            self.competition_row(3, 703, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "AWAY_WIN", 110, 130, 0.90, 0.28, "League C"),
            self.competition_row(4, 704, "STANDARD_FILL", "APPROVED_STANDARD", "BET", "TOP_CORE", "BTTS_YES", 100, 120, 0.88, 0.20, "League D"),
            self.competition_row(5, 705, "STANDARD_FILL", "APPROVED_STANDARD", "LEAN_PLAY", "TOP_CORE", "OVER_1_5", 105, 125, 0.90, 0.20, "League E"),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pd.DataFrame(rows).to_csv(
                tmp_path / build_competition_accuracy_mode.TODAY_SHORTLIST_INPUT,
                index=False,
            )

            paths, scored, shortlist, top = build_competition_accuracy_mode.build_today_competition_outputs(tmp_path)

            self.assertTrue(paths["COMPETITION_SHORTLIST"].exists())
            self.assertTrue(paths["COMPETITION_TOP"].exists())
            self.assertTrue(paths["COMPETITION_REPORT"].exists())
            self.assertLess(len(shortlist), len(scored))
            self.assertLessEqual(len(top), 3)
            self.assertIn(701, shortlist["fixture_id"].tolist())
            self.assertIn(702, shortlist["fixture_id"].tolist())
            self.assertNotIn(703, shortlist["fixture_id"].tolist())
            self.assertNotIn(704, shortlist["fixture_id"].tolist())
            self.assertNotIn(705, shortlist["fixture_id"].tolist())

            for col in build_competition_accuracy_mode.ACCURACY_COLUMNS:
                self.assertIn(col, scored.columns)
                self.assertIn(col, shortlist.columns)
            for col in build_competition_accuracy_mode.CALIBRATED_PROBABILITY_COLUMNS:
                self.assertIn(col, scored.columns)
                self.assertIn(col, shortlist.columns)

            self.assertTrue(shortlist["accuracy_confidence_score"].notna().all())
            self.assertTrue(shortlist["competition_raw_prob"].notna().all())
            self.assertTrue(shortlist["competition_calibrated_prob"].notna().all())
            self.assertTrue(shortlist["accuracy_mode_reason"].str.contains("ACCURACY_", regex=False).all())
            self.assertIn(
                "ACCURACY_SIDE_TOO_FRAGILE",
                scored.set_index("fixture_id").loc[703, "accuracy_mode_reason"],
            )
            self.assertIn(
                "ACCURACY_NO_BET_PREFERRED",
                scored.set_index("fixture_id").loc[705, "accuracy_mode_reason"],
            )

    def test_competition_accuracy_fields_reject_generic_weak_rows(self) -> None:
        rows = pd.DataFrame(
            [
                self.competition_row(
                    1,
                    801,
                    "STANDARD_FILL",
                    "APPROVED_STANDARD",
                    "BET",
                    "WATCH",
                    "DRAW",
                    70,
                    80,
                    0.74,
                    0.02,
                    "League A",
                    market_fit="",
                    stats_quality="NONE",
                    process_score=0.0,
                )
            ]
        )

        scored = build_competition_accuracy_mode.add_accuracy_mode_fields(rows)

        self.assertEqual(int(scored.loc[0, "accuracy_mode_eligible_flag"]), 0)
        self.assertEqual(scored.loc[0, "accuracy_mode_bucket"], "ACCURACY_REJECTED")
        self.assertIn("ACCURACY_", scored.loc[0, "accuracy_mode_reason"])

    def test_competition_calibrated_probability_shrinks_overconfident_group(self) -> None:
        historical = pd.DataFrame(
            [
                {
                    **self.competition_row(1, 811, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "TOP_CORE", "OVER_1_5", 92, 122, 0.91, 0.12, "League A"),
                    "result_status": "RESULT_AVAILABLE",
                    "actionable_result": "LOSS",
                    "profit_units": -1.0,
                },
                {
                    **self.competition_row(2, 812, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "TOP_CORE", "OVER_1_5", 91, 121, 0.89, 0.12, "League B"),
                    "result_status": "RESULT_AVAILABLE",
                    "actionable_result": "LOSS",
                    "profit_units": -1.0,
                },
                {
                    **self.competition_row(3, 813, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "TOP_CORE", "OVER_1_5", 90, 120, 0.90, 0.12, "League C"),
                    "result_status": "RESULT_AVAILABLE",
                    "actionable_result": "WIN",
                    "profit_units": 0.5,
                },
            ]
        )
        historical = build_competition_accuracy_mode.add_accuracy_mode_fields(historical)
        table = build_competition_accuracy_mode.build_probability_calibration_table(historical)

        today = build_competition_accuracy_mode.add_accuracy_mode_fields(
            pd.DataFrame(
                [
                    self.competition_row(
                        1,
                        814,
                        "PREMIUM_CORE",
                        "APPROVED_PREMIUM",
                        "BET",
                        "TOP_CORE",
                        "OVER_1_5",
                        92,
                        122,
                        0.90,
                        0.12,
                        "League D",
                    )
                ]
            )
        )
        calibrated = build_competition_accuracy_mode.add_competition_probability_calibration(today, table)

        self.assertLess(
            float(calibrated.loc[0, "competition_calibrated_prob"]),
            float(calibrated.loc[0, "competition_raw_prob"]),
        )
        self.assertGreaterEqual(float(calibrated.loc[0, "competition_calibrated_prob"]), 0.55)
        self.assertLessEqual(float(calibrated.loc[0, "competition_calibrated_prob"]), 0.95)
        self.assertEqual(
            calibrated.loc[0, "competition_prob_calibration_reason"],
            "CALIBRATED_MARKET_BUCKET_OVERCONFIDENCE",
        )
        self.assertEqual(int(calibrated.loc[0, "competition_prob_shrinkage_applied_flag"]), 1)

    def test_competition_calibration_uses_minimal_fallback_when_sample_is_thin(self) -> None:
        today = build_competition_accuracy_mode.add_accuracy_mode_fields(
            pd.DataFrame(
                [
                    self.competition_row(
                        1,
                        821,
                        "PREMIUM_CORE",
                        "APPROVED_PREMIUM",
                        "BET",
                        "TOP_CORE",
                        "OVER_1_5",
                        92,
                        122,
                        0.90,
                        0.12,
                        "League A",
                    )
                ]
            )
        )

        calibrated = build_competition_accuracy_mode.add_competition_probability_calibration(
            today,
            pd.DataFrame(),
        )

        self.assertAlmostEqual(float(calibrated.loc[0, "competition_calibrated_prob"]), 0.885)
        self.assertEqual(
            calibrated.loc[0, "competition_prob_calibration_reason"],
            "CALIBRATION_SAMPLE_THIN_MINIMAL_SHRINK",
        )

    def test_competition_probability_calibration_does_not_change_row_selection(self) -> None:
        rows = pd.DataFrame(
            [
                self.competition_row(1, 831, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "TOP_CORE", "OVER_1_5", 92, 122, 0.90, 0.12, "League A"),
                self.competition_row(2, 832, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "AWAY_WIN", 110, 130, 0.90, 0.28, "League B"),
                self.competition_row(3, 833, "PREMIUM_EXTENDED", "APPROVED_PREMIUM", "BET", "WATCH", "OVER_1_5", 91, 113, 0.86, 0.13, "League C"),
            ]
        )
        scored = build_competition_accuracy_mode.add_accuracy_mode_fields(rows)
        before = scored[scored["accuracy_mode_eligible_flag"].eq(1)]["fixture_id"].tolist()
        calibrated = build_competition_accuracy_mode.add_competition_probability_calibration(scored, pd.DataFrame())
        after = calibrated[calibrated["accuracy_mode_eligible_flag"].eq(1)]["fixture_id"].tolist()

        self.assertEqual(before, after)

    def test_competition_probability_calibration_table_and_report_are_generated(self) -> None:
        rows = pd.DataFrame(
            [
                {
                    **self.competition_row(1, 841, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "TOP_CORE", "OVER_1_5", 92, 122, 0.91, 0.12, "League A"),
                    "historical_batch_date": "2026-05-01",
                    "result_status": "RESULT_AVAILABLE",
                    "actionable_result": "LOSS",
                    "profit_units": -1.0,
                },
                {
                    **self.competition_row(2, 842, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "TOP_CORE", "OVER_1_5", 91, 121, 0.89, 0.12, "League B"),
                    "historical_batch_date": "2026-05-02",
                    "result_status": "RESULT_AVAILABLE",
                    "actionable_result": "LOSS",
                    "profit_units": -1.0,
                },
                {
                    **self.competition_row(3, 843, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "TOP_CORE", "OVER_1_5", 90, 120, 0.90, 0.12, "League C"),
                    "historical_batch_date": "2026-05-03",
                    "result_status": "RESULT_AVAILABLE",
                    "actionable_result": "WIN",
                    "profit_units": 0.5,
                },
            ]
        )

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / build_competition_accuracy_mode.HISTORICAL_SOURCE_INPUT
            build_competition_accuracy_mode.add_accuracy_mode_fields(rows).to_csv(source, index=False)

            paths, summary = build_competition_accuracy_mode.build_probability_evaluation(source, tmp_path)
            table = pd.read_csv(paths["calibration_table"])

            self.assertTrue(paths["calibration_table"].exists())
            self.assertTrue(paths["calibration_report"].exists())
            self.assertIn("brier_score_raw", summary.columns)
            self.assertIn("brier_score_calibrated", summary.columns)
            self.assertIn("MARKET_BUCKET", table["group_type"].tolist())
            self.assertTrue(table["usable_for_lookup"].astype(int).ge(0).all())

    def test_competition_probability_evaluation_outputs_are_generated(self) -> None:
        rows = pd.DataFrame(
            [
                {
                    **self.competition_row(1, 901, "PREMIUM_CORE", "APPROVED_PREMIUM", "BET", "TOP_CORE", "OVER_1_5", 92, 122, 0.86, 0.12, "League A"),
                    "historical_batch_date": "2026-05-01",
                    "result_status": "RESULT_AVAILABLE",
                    "actionable_result": "WIN",
                    "profit_units": 0.55,
                },
                {
                    **self.competition_row(2, 902, "STANDARD_FILL", "APPROVED_STANDARD", "BET", "TOP_CORE", "HOME_WIN", 90, 100, 0.76, 0.06, "League B"),
                    "historical_batch_date": "2026-05-01",
                    "result_status": "RESULT_AVAILABLE",
                    "actionable_result": "LOSS",
                    "profit_units": -1.0,
                },
            ]
        )

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / build_competition_accuracy_mode.HISTORICAL_SOURCE_INPUT
            build_competition_accuracy_mode.add_accuracy_mode_fields(rows).to_csv(source, index=False)

            paths, summary = build_competition_accuracy_mode.build_probability_evaluation(source, tmp_path)

            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["report"].exists())
            self.assertTrue(paths["calibration_table"].exists())
            self.assertTrue(paths["calibration_report"].exists())
            self.assertIn("COMPETITION_ACCURACY_MODE", summary["segment"].tolist())
            self.assertIn("calibration_bucket", summary["summary_scope"].tolist())
            self.assertIn("avg_probability_raw", summary.columns)
            self.assertIn("avg_probability_calibrated", summary.columns)
            competition = summary.set_index("segment").loc["COMPETITION_ACCURACY_MODE"]
            self.assertLessEqual(int(competition["rows_total"]), len(rows))

    def test_today_pipeline_step_order_and_snapshot_include_competition_mode(self) -> None:
        steps = run_today_match_pipeline.PIPELINE_STEPS
        pick_modes_index = steps.index("scripts/build_execution_pick_modes.py")
        self.assertEqual(
            steps[pick_modes_index + 1],
            "scripts/build_competition_accuracy_mode.py",
        )

        names = {path.name for path in run_today_match_pipeline.TODAY_GENERATED_FILES}
        self.assertTrue(
            {
                "vsigma_today_competition_shortlist.csv",
                "vsigma_today_competition_top.csv",
                "vsigma_today_competition_report.txt",
                "vsigma_probability_evaluation_summary.csv",
                "vsigma_probability_evaluation_report.txt",
                "vsigma_probability_calibration_table.csv",
                "vsigma_probability_calibration_report.txt",
            }.issubset(names)
        )

    def ledger_shortlist_row(
        self,
        execution_rank: int,
        fixture_id: int,
        market: str,
        recommendation: str = "BET",
        bucket: str = "APPROVED_PREMIUM",
        source: str = "PREMIUM_CORE",
    ) -> dict[str, object]:
        return {
            "execution_rank": execution_rank,
            "execution_shortlist_source": source,
            "fixture_id": fixture_id,
            "date": "2026-05-09",
            "league": "Ledger League",
            "home_team": f"Home {fixture_id}",
            "away_team": f"Away {fixture_id}",
            "market_primary": market,
            "final_execution_bucket": bucket,
            "final_recommendation": recommendation,
            "execution_score": 100.0 - execution_rank,
            "selection_score": 80.0 - execution_rank,
            "primary_model_prob": 0.75,
            "primary_odds_used": 1.8,
            "primary_edge": 0.08,
        }

    def write_ledger_inputs(
        self,
        processed_dir: Path,
        shortlist_rows: list[dict[str, object]],
        labeled_rows: list[dict[str, object]],
    ) -> None:
        pd.DataFrame(
            shortlist_rows,
            columns=build_execution_shortlist_results_ledger.REQUIRED_SHORTLIST_COLUMNS,
        ).to_csv(
            processed_dir / build_execution_shortlist_results_ledger.SHORTLIST_CSV,
            index=False,
        )
        pd.DataFrame(
            labeled_rows,
            columns=[
                "fixture_id",
                "market_primary",
                "actionable_result",
                "actionable_profit_units",
                "primary_result",
                "primary_profit_units",
            ],
        ).to_csv(
            processed_dir / build_execution_shortlist_results_ledger.LABELED_RESULTS_CSV,
            index=False,
        )

    def test_execution_shortlist_results_ledger_joins_labeled_results_correctly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_ledger_inputs(
                tmp_path,
                [
                    self.ledger_shortlist_row(1, 1, "OVER_1_5"),
                    self.ledger_shortlist_row(2, 2, "AWAY_WIN"),
                ],
                [
                    {
                        "fixture_id": 1,
                        "market_primary": "OVER_1_5",
                        "actionable_result": "WIN",
                        "actionable_profit_units": 0.8,
                        "primary_result": "WIN",
                        "primary_profit_units": 0.8,
                    },
                    {
                        "fixture_id": 2,
                        "market_primary": "AWAY_WIN",
                        "actionable_result": "LOSS",
                        "actionable_profit_units": -1.0,
                        "primary_result": "LOSS",
                        "primary_profit_units": -1.0,
                    },
                ],
            )

            paths, ledger, _summary = build_execution_shortlist_results_ledger.build_ledger(tmp_path)

            self.assertTrue(paths["LEDGER"].exists())
            self.assertEqual(len(ledger), 2)
            self.assertEqual(ledger["ledger_result_status"].tolist(), ["RESULT_AVAILABLE", "RESULT_AVAILABLE"])
            self.assertEqual(ledger["actionable_result"].tolist(), ["WIN", "LOSS"])
            self.assertEqual(ledger["execution_rank"].tolist(), [1, 2])

    def test_execution_shortlist_results_ledger_marks_pending_when_result_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_ledger_inputs(
                tmp_path,
                [
                    self.ledger_shortlist_row(1, 10, "OVER_1_5"),
                    self.ledger_shortlist_row(2, 20, "OVER_2_5"),
                ],
                [
                    {
                        "fixture_id": 10,
                        "market_primary": "OVER_1_5",
                        "actionable_result": pd.NA,
                        "actionable_profit_units": pd.NA,
                        "primary_result": pd.NA,
                        "primary_profit_units": pd.NA,
                    },
                ],
            )

            _paths, ledger, _summary = build_execution_shortlist_results_ledger.build_ledger(tmp_path)

            by_fixture = ledger.set_index("fixture_id")
            self.assertEqual(by_fixture.loc[10, "ledger_result_status"], "PENDING")
            self.assertEqual(by_fixture.loc[20, "ledger_result_status"], "UNMATCHED")

    def test_execution_shortlist_results_summary_metrics_and_groups(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_ledger_inputs(
                tmp_path,
                [
                    self.ledger_shortlist_row(1, 1, "OVER_1_5", "BET", "APPROVED_PREMIUM", "PREMIUM_CORE"),
                    self.ledger_shortlist_row(2, 2, "OVER_2_5", "BET", "APPROVED_PREMIUM", "PREMIUM_EXTENDED"),
                    self.ledger_shortlist_row(3, 3, "BTTS_YES", "LEAN_PLAY", "APPROVED_STANDARD", "STANDARD_FILL"),
                    self.ledger_shortlist_row(4, 4, "HOME_WIN", "BET", "APPROVED_STANDARD", "STANDARD_FILL"),
                    self.ledger_shortlist_row(5, 5, "AWAY_WIN", "BET", "APPROVED_PREMIUM", "PREMIUM_EXTENDED"),
                ],
                [
                    {
                        "fixture_id": 1,
                        "market_primary": "OVER_1_5",
                        "actionable_result": "WIN",
                        "actionable_profit_units": 0.8,
                        "primary_result": "WIN",
                        "primary_profit_units": 0.8,
                    },
                    {
                        "fixture_id": 2,
                        "market_primary": "OVER_2_5",
                        "actionable_result": "LOSS",
                        "actionable_profit_units": -1.0,
                        "primary_result": "LOSS",
                        "primary_profit_units": -1.0,
                    },
                    {
                        "fixture_id": 3,
                        "market_primary": "BTTS_YES",
                        "actionable_result": "PUSH",
                        "actionable_profit_units": 0.0,
                        "primary_result": "PUSH",
                        "primary_profit_units": 0.0,
                    },
                    {
                        "fixture_id": 4,
                        "market_primary": "HOME_WIN",
                        "actionable_result": "VOID",
                        "actionable_profit_units": pd.NA,
                        "primary_result": "VOID",
                        "primary_profit_units": 0.0,
                    },
                ],
            )

            _paths, _ledger, summary = build_execution_shortlist_results_ledger.build_ledger(tmp_path)
            overall = summary[summary["summary_scope"].eq("overall")].set_index("metric")["value_num"]

            self.assertEqual(int(overall["shortlist_rows"]), 5)
            self.assertEqual(int(overall["result_available_rows"]), 4)
            self.assertEqual(int(overall["unmatched_rows"]), 1)
            self.assertEqual(int(overall["bet_rows"]), 4)
            self.assertEqual(int(overall["lean_play_rows"]), 1)
            self.assertEqual(int(overall["premium_rows"]), 3)
            self.assertEqual(int(overall["standard_rows"]), 2)
            self.assertEqual(int(overall["wins"]), 1)
            self.assertEqual(int(overall["losses"]), 1)
            self.assertEqual(int(overall["pushes"]), 1)
            self.assertEqual(int(overall["voids"]), 1)
            self.assertAlmostEqual(float(overall["profit_units_total"]), -0.2)
            self.assertAlmostEqual(float(overall["roi_percent"]), -5.0)

            self.assertIn("by_final_execution_bucket", summary["summary_scope"].tolist())
            self.assertIn("by_final_recommendation", summary["summary_scope"].tolist())
            self.assertIn("by_execution_shortlist_source", summary["summary_scope"].tolist())
            premium_group = summary[
                summary["summary_scope"].eq("by_final_execution_bucket")
                & summary["metric"].eq("shortlist_rows")
                & summary["value_text"].eq("APPROVED_PREMIUM")
            ]
            self.assertEqual(int(premium_group.iloc[0]["value_num"]), 3)

    def test_execution_shortlist_results_ledger_duplicate_match_protection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_ledger_inputs(
                tmp_path,
                [self.ledger_shortlist_row(1, 1, "OVER_1_5")],
                [
                    {
                        "fixture_id": 1,
                        "market_primary": "OVER_1_5",
                        "actionable_result": "WIN",
                        "actionable_profit_units": 0.8,
                        "primary_result": "WIN",
                        "primary_profit_units": 0.8,
                    },
                    {
                        "fixture_id": 1,
                        "market_primary": "OVER_1_5",
                        "actionable_result": "LOSS",
                        "actionable_profit_units": -1.0,
                        "primary_result": "LOSS",
                        "primary_profit_units": -1.0,
                    },
                ],
            )

            with self.assertRaisesRegex(ValueError, "matches multiple labeled result rows"):
                build_execution_shortlist_results_ledger.build_ledger(tmp_path)

    def write_post_results_fixture_files(self, processed_dir: Path) -> tuple[Path, Path]:
        today_dir = processed_dir / "today"
        shortlist_path = processed_dir / "vsigma_today_execution_shortlist.csv"
        ledger_path = processed_dir / "vsigma_execution_shortlist_results_ledger.csv"

        shortlist = pd.DataFrame(
            [
                {
                    "execution_rank": 1,
                    "execution_shortlist_source": "PREMIUM_CORE",
                    "fixture_id": 9001,
                    "date": "2026-05-09",
                    "league": "Post League",
                    "home_team": "Post Home",
                    "away_team": "Post Away",
                    "market_primary": "OVER_1_5",
                    "final_execution_bucket": "APPROVED_PREMIUM",
                    "final_recommendation": "BET",
                    "execution_score": 101.5,
                    "selection_score": 88.0,
                    "primary_model_prob": 0.8,
                    "primary_odds_used": 1.8,
                    "primary_edge": 0.08,
                    "pick_main_why": "STRONG_ROLLING_STATS;CORE_GATE_PASSED",
                    "pick_primary_risk": "FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5",
                    "pick_bucket_rationale": "PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK",
                    "pick_rank_rationale": "EXECUTION_SHORTLIST_SORT: execution_rank=1; execution_score=101.500",
                    "pick_failure_mode": "LOW_CONVERSION",
                    "pick_confirmation_layers": "STATS+ODDS+FORM",
                }
            ]
        )
        ledger = shortlist.assign(
            actionable_result="WIN",
            actionable_profit_units=0.8,
            primary_result="WIN",
            primary_profit_units=0.8,
            ledger_result_status="RESULT_AVAILABLE",
        )[
            run_today_post_results_pipeline.REQUIRED_LEDGER_COLUMNS
        ]

        shortlist.to_csv(shortlist_path, index=False)
        ledger.to_csv(ledger_path, index=False)

        for filename in [
            "vsigma_today_premium_core.csv",
            "vsigma_today_execution_bets_only.csv",
            "vsigma_today_execution_summary.csv",
            "vsigma_execution_shortlist_results_summary.csv",
            "vsigma_market_results_labeled.csv",
            "vsigma_market_results_report.csv",
            "refresh_finished_results_by_date_report.csv",
        ]:
            pd.DataFrame([{"date": "2026-05-09", "rows_total": 1}]).to_csv(
                processed_dir / filename,
                index=False,
            )

        return shortlist_path, ledger_path

    def write_daily_journal_fixture_files(self, processed_dir: Path, match_date: str = "2026-05-09") -> None:
        snapshot_dir = processed_dir / "today" / match_date
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        shortlist = pd.DataFrame(
            [
                {
                    "execution_rank": 1,
                    "mode_rank": 1,
                    "fixture_id": 9101,
                    "date": match_date,
                    "league": "Journal League",
                    "home_team": "Journal Home",
                    "away_team": "Journal Away",
                    "market_primary": "OVER_1_5",
                    "final_execution_bucket": "APPROVED_PREMIUM",
                    "final_recommendation": "BET",
                    "execution_shortlist_source": "PREMIUM_CORE",
                    "execution_score": 120.25,
                    "pick_main_why": "STRONG_ROLLING_STATS;CORE_GATE_PASSED",
                    "pick_primary_risk": "FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5",
                    "pick_bucket_rationale": "PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK",
                    "pick_rank_rationale": "EXECUTION_SHORTLIST_SORT: execution_rank=1; execution_score=120.250",
                    "pick_failure_mode": "LOW_CONVERSION",
                    "pick_confirmation_layers": "STATS+ODDS+FORM",
                }
            ]
        )
        shortlist.to_csv(snapshot_dir / "vsigma_today_execution_shortlist.csv", index=False)
        shortlist.to_csv(snapshot_dir / "vsigma_today_safe_top5.csv", index=False)
        shortlist.to_csv(snapshot_dir / "vsigma_today_balanced_top5.csv", index=False)
        pd.DataFrame(
            [
                {
                    "date": match_date,
                    "timezone": "Atlantic/Canary",
                    "approved_premium_rows": 1,
                    "approved_standard_rows": 0,
                    "downgraded_rows": 2,
                    "blocked_rows": 1,
                    "watch_rows": 3,
                }
            ]
        ).to_csv(snapshot_dir / "today_pipeline_report.csv", index=False)
        ledger = shortlist[
            [
                "execution_rank",
                "execution_shortlist_source",
                "fixture_id",
                "date",
                "league",
                "home_team",
                "away_team",
                "market_primary",
                "final_execution_bucket",
                "final_recommendation",
                "execution_score",
            ]
        ].assign(
            selection_score=90.0,
            primary_model_prob=0.82,
            primary_odds_used=1.6,
            primary_edge=0.12,
            actionable_result="WIN",
            actionable_profit_units=0.6,
            primary_result="WIN",
            primary_profit_units=0.6,
            ledger_result_status="RESULT_AVAILABLE",
        )
        ledger.to_csv(snapshot_dir / "vsigma_execution_shortlist_results_ledger.csv", index=False)
        pd.DataFrame(
            [
                {
                    "date": match_date,
                    "timezone": "Atlantic/Canary",
                    "ledger_rows": 1,
                    "result_available_rows": 1,
                    "pending_rows": 0,
                    "unmatched_rows": 0,
                    "win_rows": 1,
                    "loss_rows": 0,
                    "push_rows": 0,
                    "void_rows": 0,
                    "profit_units_total": 0.6,
                    "roi_percent": 60.0,
                }
            ]
        ).to_csv(snapshot_dir / "today_post_results_report.csv", index=False)

    def test_daily_pre_summary_created_with_executable_pick_explanations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            self.write_daily_journal_fixture_files(processed_dir)

            output_path = build_daily_decision_journal.build_pre_summary(
                processed_dir,
                processed_dir / "today",
                "2026-05-09",
                "Atlantic/Canary",
            )

            text = output_path.read_text(encoding="utf-8")
            self.assertTrue(output_path.exists())
            self.assertIn("## Pipeline Counts", text)
            self.assertIn("## SAFE Picks", text)
            self.assertIn("## BALANCED Picks", text)
            self.assertIn("## Execution Shortlist", text)
            self.assertIn("Journal Home vs Journal Away", text)
            self.assertIn("STRONG_ROLLING_STATS;CORE_GATE_PASSED", text)
            self.assertIn("PREMIUM_CORE: CORE_GATE_PASSED", text)
            self.assertIn("EXECUTION_SHORTLIST_SORT", text)
            self.assertGreater(len(text.strip()), 200)

    def test_daily_post_summary_created_with_ledger_outcomes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            self.write_daily_journal_fixture_files(processed_dir)

            output_path = build_daily_decision_journal.build_post_summary(
                processed_dir,
                processed_dir / "today",
                "2026-05-09",
                "Atlantic/Canary",
            )

            text = output_path.read_text(encoding="utf-8")
            self.assertTrue(output_path.exists())
            self.assertIn("## Ledger Summary", text)
            self.assertIn("## Day Summary", text)
            self.assertIn("## Ledger Picks", text)
            self.assertIn("Result: WIN", text)
            self.assertIn("POST_VERDICT: WIN_CONFIRMED", text)
            self.assertIn("Original main why: STRONG_ROLLING_STATS;CORE_GATE_PASSED", text)
            self.assertIn("Total profit units: 0.600", text)
            self.assertGreater(len(text.strip()), 200)

    def forecast_pick_rows(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "accuracy_mode_rank": 1,
                    "fixture_id": 101,
                    "date": "2026-05-09",
                    "league": "Forecast League",
                    "home_team": "Forecast Home",
                    "away_team": "Forecast Away",
                    "market_primary": "OVER_2_5",
                    "projected_home_goals": 1.7,
                    "projected_away_goals": 1.5,
                    "competition_calibrated_prob": 0.82,
                    "accuracy_confidence_score": 132.0,
                    "recent_stats_quality_flag": "FULL",
                    "home_recent_shots_for_pg": 14.0,
                    "away_recent_shots_for_pg": 12.0,
                    "home_recent_shots_against_pg": 10.0,
                    "away_recent_shots_against_pg": 11.0,
                    "home_recent_sot_for_pg": 5.5,
                    "away_recent_sot_for_pg": 4.5,
                    "home_recent_sot_against_pg": 3.8,
                    "away_recent_sot_against_pg": 4.2,
                    "home_recent_corners_for_pg": 5.8,
                    "away_recent_corners_for_pg": 4.6,
                    "home_recent_corners_against_pg": 4.1,
                    "away_recent_corners_against_pg": 4.4,
                    "home_recent_possession_pct": 54.0,
                    "away_recent_possession_pct": 49.0,
                    "pick_failure_mode": "LOW_CONVERSION",
                    "pick_primary_risk": "FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5",
                    "league_coverage_source_status": "OFFICIAL_API",
                },
                {
                    "accuracy_mode_rank": 2,
                    "fixture_id": 102,
                    "date": "2026-05-09",
                    "league": "Forecast League 2",
                    "home_team": "Home Side",
                    "away_team": "Away Side",
                    "market_primary": "HOME_WIN",
                    "projected_home_goals": 1.9,
                    "projected_away_goals": 0.9,
                    "competition_calibrated_prob": 0.76,
                    "accuracy_confidence_score": 111.0,
                    "recent_stats_quality_flag": "PARTIAL",
                    "pick_failure_mode": "DRAW_LIVE",
                },
            ]
        )

    def test_match_script_forecast_output_files_and_required_fields_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            processed_dir.mkdir(parents=True)
            input_path = processed_dir / "vsigma_today_competition_top.csv"
            self.forecast_pick_rows().to_csv(input_path, index=False)

            paths, forecasts = build_match_script_forecasts.build_and_write_forecasts(processed_dir)

            self.assertTrue(paths["forecast_csv"].exists())
            self.assertTrue(paths["forecast_report"].exists())
            self.assertEqual(len(forecasts), 2)
            self.assertTrue(set(build_match_script_forecasts.FORECAST_COLUMNS).issubset(forecasts.columns))

    def test_match_script_forecasts_use_non_empty_ranges_and_modal_scores(self) -> None:
        forecasts = build_match_script_forecasts.build_match_script_forecasts(self.forecast_pick_rows())

        for col in [
            "predicted_home_xg_range",
            "predicted_away_xg_range",
            "predicted_home_shots_range",
            "predicted_away_sot_range",
            "predicted_total_corners_range",
            "predicted_possession_split",
            "predicted_pick_path",
            "predicted_pick_breaker",
        ]:
            self.assertTrue(forecasts[col].astype(str).str.len().ge(3).all(), col)
        self.assertTrue(forecasts["predicted_home_xg_range"].astype(str).str.contains("-").all())
        self.assertTrue(forecasts["predicted_score_main"].astype(str).str.contains("-").all())

    def test_match_script_forecast_layer_does_not_modify_official_selection_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            processed_dir.mkdir(parents=True)
            input_path = processed_dir / "vsigma_today_competition_top.csv"
            self.forecast_pick_rows().head(1).to_csv(input_path, index=False)
            before = input_path.read_text(encoding="utf-8")

            _paths, forecasts = build_match_script_forecasts.build_and_write_forecasts(processed_dir)

            self.assertEqual(input_path.read_text(encoding="utf-8"), before)
            self.assertEqual(len(forecasts), 1)

    def test_daily_pre_summary_includes_match_script_forecast_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            self.write_daily_journal_fixture_files(processed_dir)
            snapshot_dir = processed_dir / "today" / "2026-05-09"
            forecasts = build_match_script_forecasts.build_match_script_forecasts(
                self.forecast_pick_rows().head(1)
            )
            forecasts.to_csv(snapshot_dir / "vsigma_today_match_script_forecasts.csv", index=False)

            output_path = build_daily_decision_journal.build_pre_summary(
                processed_dir,
                processed_dir / "today",
                "2026-05-09",
                "Atlantic/Canary",
            )

            text = output_path.read_text(encoding="utf-8")
            self.assertIn("## Match Script Forecasts", text)
            self.assertIn("Forecast Home vs Forecast Away", text)
            self.assertIn("Pick breaker", text)

    def test_today_pipeline_runs_match_script_forecasts_after_competition_mode(self) -> None:
        steps = run_today_match_pipeline.PIPELINE_STEPS

        self.assertLess(
            steps.index("scripts/build_competition_accuracy_mode.py"),
            steps.index("scripts/build_match_script_forecasts.py"),
        )
        names = {path.name for path in run_today_match_pipeline.TODAY_GENERATED_FILES}
        self.assertIn("vsigma_today_match_script_forecasts.csv", names)
        self.assertIn("vsigma_today_match_script_forecasts_report.txt", names)

    def test_shadow_candidate_v2_daily_outputs_created_without_overwriting_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)

            baseline = pd.DataFrame(
                [
                    {
                        "fixture_id": 10,
                        "date": "2026-05-09",
                        "league": "League A",
                        "home_team": "Base Home",
                        "away_team": "Base Away",
                        "market_primary": "OVER_1_5",
                        "accuracy_mode_rank": 1,
                        "competition_calibrated_prob": 0.78,
                        "accuracy_confidence_score": 101.0,
                        "accuracy_mode_bucket": "ACCURACY_CORE",
                        "accuracy_mode_reason": "official baseline reason",
                        "accuracy_primary_risk": "baseline risk",
                    }
                ]
            )
            candidate = baseline.copy()
            candidate.loc[0, "competition_calibrated_prob"] = 0.81
            candidate.loc[0, "accuracy_mode_reason"] = "candidate lab reason"

            official_shortlist = processed_dir / "vsigma_today_competition_shortlist.csv"
            official_top = processed_dir / "vsigma_today_competition_top.csv"
            official_report = processed_dir / "vsigma_today_competition_report.txt"
            candidate.to_csv(official_shortlist, index=False)
            candidate.to_csv(official_top, index=False)
            official_report.write_text("candidate live report\n", encoding="utf-8")
            baseline_before = official_shortlist.read_text(encoding="utf-8")

            paths = run_today_shadow_candidate_v2.write_shadow_outputs(
                processed_dir,
                today_dir,
                "2026-05-09",
                "Atlantic/Canary",
                baseline,
                candidate,
            )

            snapshot_dir = today_dir / "2026-05-09"
            self.assertTrue(paths["candidate_shortlist"].exists())
            self.assertTrue(paths["candidate_top"].exists())
            self.assertTrue(paths["comparison_csv"].exists())
            self.assertTrue(paths["comparison_report"].exists())
            self.assertTrue((snapshot_dir / "vsigma_today_candidate_v2_competition_shortlist.csv").exists())
            self.assertTrue((snapshot_dir / build_daily_decision_journal.SHADOW_CANDIDATE_V2_PRE_SUMMARY_FILENAME).exists())
            self.assertEqual(official_shortlist.read_text(encoding="utf-8"), baseline_before)

    def test_shadow_candidate_v2_comparison_handles_more_or_fewer_picks(self) -> None:
        baseline = pd.DataFrame(
            [
                {"fixture_id": 1, "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5", "accuracy_mode_rank": 1},
                {"fixture_id": 2, "home_team": "C", "away_team": "D", "market_primary": "UNDER_3_5", "accuracy_mode_rank": 2},
            ]
        )
        candidate = pd.DataFrame(
            [
                {"fixture_id": 1, "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5", "accuracy_mode_rank": 1},
                {"fixture_id": 3, "home_team": "E", "away_team": "F", "market_primary": "OVER_2_5", "accuracy_mode_rank": 2},
            ]
        )

        comparison = run_today_shadow_candidate_v2.build_baseline_candidate_comparison(baseline, candidate)

        self.assertEqual(
            set(comparison["comparison_status"].tolist()),
            {"BOTH", "BASELINE_ONLY", "CANDIDATE_V2_ONLY"},
        )
        self.assertEqual(int(comparison["comparison_status"].eq("BOTH").sum()), 1)

    def test_shadow_candidate_v2_journal_sections_are_separate_from_official(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            snapshot_dir = processed_dir / "today" / "2026-05-09"
            snapshot_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "home_team": "Shadow Home",
                        "away_team": "Shadow Away",
                        "market_primary": "OVER_1_5",
                        "accuracy_mode_rank": 1,
                    }
                ]
            ).to_csv(snapshot_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
            pd.DataFrame(
                [{"baseline_competition_rows": 1, "candidate_v2_competition_rows": 1, "overlap_rows": 1}]
            ).to_csv(snapshot_dir / "today_shadow_candidate_v2_report.csv", index=False)
            pd.DataFrame([{"comparison_status": "BOTH", "fixture": "Shadow Home vs Shadow Away"}]).to_csv(
                snapshot_dir / "vsigma_today_baseline_vs_candidate_v2.csv",
                index=False,
            )

            path = build_daily_decision_journal.build_shadow_candidate_v2_pre_summary(
                processed_dir,
                processed_dir / "today",
                "2026-05-09",
                "Atlantic/Canary",
            )

            text = path.read_text(encoding="utf-8")
            self.assertEqual(path.name, build_daily_decision_journal.SHADOW_CANDIDATE_V2_PRE_SUMMARY_FILENAME)
            self.assertIn("SHADOW / experimental / non-official", text)
            self.assertIn("Candidate v2 Shadow Top", text)
            self.assertFalse((snapshot_dir / build_daily_decision_journal.PRE_SUMMARY_FILENAME).exists())

    def candidate_v4_fixture_row(
        self,
        fixture_id: int,
        market: str = "OVER_2_5",
        failure: str = "LOW_CONVERSION",
        projected_total: float = 3.55,
        calibrated_prob: float = 0.79,
        confidence_score: float = 118.0,
        market_alt: str = "OVER_1_5",
        alt_model_prob: float = 0.88,
        alt_odds_used: float = 1.35,
        alt_edge: float = 0.10,
    ) -> dict[str, object]:
        return {
            "execution_rank": fixture_id,
            "shortlist_rank": fixture_id,
            "date": "2026-05-09",
            "league": f"League {fixture_id}",
            "fixture_id": fixture_id,
            "home_team": f"Home {fixture_id}",
            "away_team": f"Away {fixture_id}",
            "market_primary": market,
            "market_alt": market_alt,
            "final_recommendation": "BET",
            "final_execution_bucket": "APPROVED_PREMIUM",
            "base_execution_verdict": "TOP_CORE",
            "execution_shortlist_source": "PREMIUM_CORE",
            "execution_market_fit_status": "SAFE_OK",
            "primary_model_prob": calibrated_prob,
            "primary_odds_used": 1.65,
            "primary_implied_prob": 0.606,
            "primary_edge": 0.18,
            "alt_model_prob": alt_model_prob,
            "alt_odds_used": alt_odds_used,
            "alt_implied_prob": 1 / alt_odds_used if alt_odds_used else pd.NA,
            "alt_edge": alt_edge,
            "selection_score": 90.0,
            "execution_score": 112.0,
            "accuracy_mode_eligible_flag": 1,
            "accuracy_confidence_score": confidence_score,
            "accuracy_mode_reason": "ACCURACY_CORE_PRIORITY;ACCURACY_OVER_CONFIRMED",
            "accuracy_primary_risk": f"FAILURE_MODE_{failure}" if failure else "FAILURE_MODE_UNKNOWN",
            "accuracy_mode_bucket": "ACCURACY_CORE",
            "accuracy_mode_rank": fixture_id,
            "competition_raw_prob": calibrated_prob,
            "competition_calibrated_prob": calibrated_prob,
            "pick_failure_mode": failure,
            "projected_home_goals": round(projected_total / 2, 2),
            "projected_away_goals": round(projected_total / 2, 2),
            "projected_total_goals": projected_total,
            "likely_scoreline": "2-1 / 1-1 / 2-2",
            "recent_stats_quality_flag": "FULL",
            "recent_stats_process_score": 4.0,
            "home_recent_stats_matches_used": 5,
            "away_recent_stats_matches_used": 5,
            "home_recent_stats_coverage_ratio": 0.8,
            "away_recent_stats_coverage_ratio": 0.8,
            "league_coverage_class": "COVERAGE_RICH",
            "home_recent_shots_for_pg": 13.0,
            "away_recent_shots_for_pg": 12.0,
            "home_recent_sot_for_pg": 5.0,
            "away_recent_sot_for_pg": 5.0,
            "home_recent_shots_against_pg": 11.0,
            "away_recent_shots_against_pg": 11.0,
            "home_recent_sot_against_pg": 4.0,
            "away_recent_sot_against_pg": 4.0,
        }

    def test_candidate_v4_over25_low_conversion_triggers_firewall_check(self) -> None:
        rows = pd.DataFrame([self.candidate_v4_fixture_row(1)])

        all_rows, _shortlist, _top = run_today_shadow_candidate_v4.apply_over25_low_conversion_firewall(
            rows,
            rows,
            pd.DataFrame(),
        )

        self.assertEqual(int(all_rows.loc[0, "over25_low_conversion_firewall_flag"]), 1)
        self.assertIn(
            all_rows.loc[0, "over25_low_conversion_firewall_decision"],
            {run_today_shadow_candidate_v4.DEGRADE, run_today_shadow_candidate_v4.SECONDARY, run_today_shadow_candidate_v4.REMOVE},
        )

    def test_candidate_v4_strong_confirmed_over25_can_remain_keep(self) -> None:
        rows = pd.DataFrame(
            [
                self.candidate_v4_fixture_row(
                    1,
                    projected_total=4.9,
                    calibrated_prob=0.89,
                    confidence_score=146.0,
                    market_alt="BTTS_YES",
                    alt_model_prob=0.78,
                    alt_odds_used=1.65,
                    alt_edge=0.08,
                )
            ]
        )
        rows["odds_total_ladder_shape"] = "WIDE_GOALS"
        rows["odds_over25_support_flag"] = "SUPPORTED"

        all_rows, shortlist, top = run_today_shadow_candidate_v4.apply_over25_low_conversion_firewall(
            rows,
            rows,
            pd.DataFrame(),
        )

        self.assertEqual(all_rows.loc[0, "over25_low_conversion_firewall_decision"], run_today_shadow_candidate_v4.KEEP)
        self.assertEqual(shortlist.loc[0, "market_primary"], "OVER_2_5")
        self.assertEqual(top.loc[0, "market_primary"], "OVER_2_5")

    def test_candidate_v4_weak_mild_over25_downgrades_when_clean_over15_available(self) -> None:
        rows = pd.DataFrame([self.candidate_v4_fixture_row(1, projected_total=3.45, calibrated_prob=0.78, confidence_score=116.0)])

        all_rows, shortlist, top = run_today_shadow_candidate_v4.apply_over25_low_conversion_firewall(
            rows,
            rows,
            pd.DataFrame(),
        )

        self.assertEqual(all_rows.loc[0, "over25_low_conversion_firewall_decision"], run_today_shadow_candidate_v4.DEGRADE)
        self.assertEqual(shortlist.loc[0, "market_primary"], "OVER_1_5")
        self.assertEqual(top.loc[0, "over25_low_conversion_original_market"], "OVER_2_5")
        self.assertEqual(top.loc[0, "over25_low_conversion_recommended_market"], "OVER_1_5")

    def test_candidate_v4_non_over25_markets_are_not_affected(self) -> None:
        rows = pd.DataFrame([self.candidate_v4_fixture_row(1, market="OVER_1_5")])

        all_rows, shortlist, top = run_today_shadow_candidate_v4.apply_over25_low_conversion_firewall(
            rows,
            rows,
            pd.DataFrame(),
        )

        self.assertEqual(int(all_rows.loc[0, "over25_low_conversion_firewall_flag"]), 0)
        self.assertEqual(all_rows.loc[0, "over25_low_conversion_firewall_decision"], run_today_shadow_candidate_v4.NOT_APPLIED)
        self.assertEqual(shortlist.loc[0, "market_primary"], "OVER_1_5")
        self.assertEqual(top.loc[0, "market_primary"], "OVER_1_5")

    def test_candidate_v4_low_conversion_absence_does_not_trigger_firewall(self) -> None:
        rows = pd.DataFrame([self.candidate_v4_fixture_row(1, failure="DRAW_LIVE")])

        all_rows, _shortlist, _top = run_today_shadow_candidate_v4.apply_over25_low_conversion_firewall(
            rows,
            rows,
            pd.DataFrame(),
        )

        self.assertEqual(int(all_rows.loc[0, "over25_low_conversion_firewall_flag"]), 0)
        self.assertEqual(all_rows.loc[0, "over25_low_conversion_firewall_decision"], run_today_shadow_candidate_v4.NOT_APPLIED)

    def test_candidate_v4_outputs_are_separate_from_baseline_and_candidate_v2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            baseline = pd.DataFrame([self.candidate_v4_fixture_row(10, market="OVER_1_5")])
            v2 = pd.DataFrame([self.candidate_v4_fixture_row(1)])
            baseline.to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)
            v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_shortlist.csv", index=False)
            v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
            baseline_before = (processed_dir / "vsigma_today_competition_top.csv").read_text(encoding="utf-8")
            v2_before = (processed_dir / "vsigma_today_candidate_v2_competition_top.csv").read_text(encoding="utf-8")

            paths = run_today_shadow_candidate_v4.build_candidate_v4_outputs(
                processed_dir,
                today_dir,
                "2026-05-09",
                "Atlantic/Canary",
            )

            self.assertTrue(paths["candidate_v4_shortlist"].exists())
            self.assertTrue(paths["candidate_v4_top"].exists())
            self.assertTrue(paths["comparison_csv"].exists())
            self.assertTrue((today_dir / "2026-05-09" / "daily_pre_shadow_candidate_v4.md").exists())
            self.assertEqual((processed_dir / "vsigma_today_competition_top.csv").read_text(encoding="utf-8"), baseline_before)
            self.assertEqual((processed_dir / "vsigma_today_candidate_v2_competition_top.csv").read_text(encoding="utf-8"), v2_before)

    def test_candidate_v4_handles_missing_candidate_v2_shortlist_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            pd.DataFrame(columns=["fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_competition_top.csv",
                index=False,
            )

            paths = run_today_shadow_candidate_v4.build_candidate_v4_outputs(
                processed_dir,
                today_dir,
                "2026-05-14",
                "Atlantic/Canary",
            )

            self.assertTrue(paths["candidate_v4_shortlist"].exists())
            self.assertTrue(paths["candidate_v4_top"].exists())
            report = paths["candidate_v4_report"].read_text(encoding="utf-8")
            self.assertIn("CANDIDATE_V4_NO_BET", report)
            self.assertIn("reason: candidate v2 shortlist empty", report)
            self.assertTrue((today_dir / "2026-05-14" / "vsigma_today_candidate_v4_competition_top.csv").exists())

    def test_candidate_v4_handles_empty_candidate_v2_shortlist_and_writes_headers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            empty_v2 = pd.DataFrame(columns=["fixture_id", "home_team", "away_team", "market_primary"])
            empty_v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_shortlist.csv", index=False)
            empty_v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
            pd.DataFrame(columns=["fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_competition_top.csv",
                index=False,
            )

            paths = run_today_shadow_candidate_v4.build_candidate_v4_outputs(
                processed_dir,
                today_dir,
                "2026-05-14",
                "Atlantic/Canary",
            )

            shortlist = pd.read_csv(paths["candidate_v4_shortlist"])
            top = pd.read_csv(paths["candidate_v4_top"])
            comparison = pd.read_csv(paths["comparison_csv"])
            self.assertEqual(len(shortlist), 0)
            self.assertEqual(len(top), 0)
            self.assertIn("fixture_id", shortlist.columns)
            self.assertIn("over25_low_conversion_firewall_decision", top.columns)
            self.assertIn("comparison_status", comparison.columns)
            self.assertTrue((today_dir / "2026-05-14" / "daily_pre_shadow_candidate_v4.md").exists())

    def test_candidate_v4_post_results_comparison_files_are_generated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            raw_path = Path(tmp) / "data" / "raw" / "matches.csv"
            processed_dir.mkdir(parents=True)
            raw_path.parent.mkdir(parents=True)
            baseline = pd.DataFrame([self.candidate_v4_fixture_row(1)])
            v2 = pd.DataFrame([self.candidate_v4_fixture_row(1)])
            v4 = pd.DataFrame([self.candidate_v4_fixture_row(1, market="OVER_1_5")])
            v4["over25_low_conversion_firewall_flag"] = 1
            v4["over25_low_conversion_firewall_decision"] = run_today_shadow_candidate_v4.DEGRADE
            v4["over25_low_conversion_original_market"] = "OVER_2_5"
            v4["over25_low_conversion_recommended_market"] = "OVER_1_5"
            v4["over25_low_conversion_action"] = "MARKET_DOWNGRADED_TO_OVER_1_5"
            baseline.to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)
            v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
            v4.to_csv(processed_dir / "vsigma_today_candidate_v4_competition_top.csv", index=False)
            pd.DataFrame([{"fixture_id": 1, "status": "FT", "goals_home": 1, "goals_away": 1}]).to_csv(raw_path, index=False)

            with patch.object(run_today_shadow_candidate_v4_post_results, "RAW_MATCHES_CSV", raw_path):
                paths = run_today_shadow_candidate_v4_post_results.build_candidate_v4_post_results(
                    processed_dir,
                    today_dir,
                    "2026-05-09",
                    "Atlantic/Canary",
                )

            self.assertTrue(paths["candidate_v4_results_ledger"].exists())
            self.assertTrue(paths["candidate_v4_results_summary"].exists())
            self.assertTrue(paths["result_comparison_csv"].exists())
            self.assertTrue(paths["result_comparison_report"].exists())
            ledger = pd.read_csv(paths["candidate_v4_results_ledger"])
            self.assertEqual(ledger.loc[0, "market_primary"], "OVER_1_5")
            self.assertEqual(ledger.loc[0, "actionable_result"], "WIN")

    def test_candidate_v4_post_results_handles_empty_v4_picks_gracefully(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            raw_path = Path(tmp) / "data" / "raw" / "matches.csv"
            processed_dir.mkdir(parents=True)
            raw_path.parent.mkdir(parents=True)
            pd.DataFrame([{"fixture_id": 1, "status": "FT", "goals_home": 1, "goals_away": 1}]).to_csv(raw_path, index=False)
            pd.DataFrame(columns=["fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_competition_top.csv",
                index=False,
            )
            pd.DataFrame(columns=["fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_candidate_v2_competition_top.csv",
                index=False,
            )
            pd.DataFrame(columns=["fixture_id", "market_primary", "over25_low_conversion_firewall_decision"]).to_csv(
                processed_dir / "vsigma_today_candidate_v4_competition_top.csv",
                index=False,
            )

            with patch.object(run_today_shadow_candidate_v4_post_results, "RAW_MATCHES_CSV", raw_path):
                paths = run_today_shadow_candidate_v4_post_results.build_candidate_v4_post_results(
                    processed_dir,
                    today_dir,
                    "2026-05-14",
                    "Atlantic/Canary",
                )

            ledger = pd.read_csv(paths["candidate_v4_results_ledger"])
            summary = pd.read_csv(paths["candidate_v4_results_summary"])
            report = paths["result_comparison_report"].read_text(encoding="utf-8")
            self.assertEqual(len(ledger), 0)
            self.assertIn("fixture_id", ledger.columns)
            self.assertEqual(int(summary.loc[0, "pick_count"]), 0)
            self.assertIn("CANDIDATE_V4_NO_BET", report)
            self.assertTrue((today_dir / "2026-05-14" / "daily_post_shadow_candidate_v4.md").exists())

    def player_impact_row(self, fixture_id: int = 1, market: str = "OVER_2_5") -> dict[str, object]:
        row = self.candidate_v4_fixture_row(fixture_id, market=market)
        row.update(
            {
                "home_lineup_available_flag": 1,
                "away_lineup_available_flag": 1,
                "home_lineup_quality_flag": "FULL",
                "away_lineup_quality_flag": "FULL",
                "lineup_quality_flag": "FULL",
                "lineup_activation_state": "ACTIVE",
                "home_lineup_known_starters_count": 11,
                "away_lineup_known_starters_count": 11,
                "home_lineup_attacker_count": 3,
                "away_lineup_attacker_count": 3,
                "home_lineup_midfielder_count": 4,
                "away_lineup_midfielder_count": 4,
                "home_lineup_defender_count": 4,
                "away_lineup_defender_count": 4,
                "home_lineup_goalkeeper_known_flag": 1,
                "away_lineup_goalkeeper_known_flag": 1,
                "home_lineup_attack_continuity_score": 0.20,
                "away_lineup_attack_continuity_score": 0.18,
                "home_lineup_defense_continuity_score": 0.18,
                "away_lineup_defense_continuity_score": 0.18,
                "injuries_quality_flag": "FULL",
                "home_injuries_coverage_flag": "FULL",
                "away_injuries_coverage_flag": "FULL",
                "home_absence_risk_score": 0.0,
                "away_absence_risk_score": 0.0,
                "home_absence_severity_flag": "LOW",
                "away_absence_severity_flag": "LOW",
            }
        )
        return row

    def test_player_impact_fields_generated_from_reliable_coverage(self) -> None:
        rows = pd.DataFrame([self.player_impact_row()])

        enriched = enrich_player_impact.add_player_impact_fields(rows)

        self.assertIn("home_attacking_core_available_score", enriched.columns)
        self.assertEqual(enriched.loc[0, "player_impact_quality_flag"], "FULL")
        self.assertGreater(float(enriched.loc[0, "home_attacking_core_available_score"]), 0.0)
        self.assertEqual(enriched.loc[0, "home_goalkeeper_confidence_flag"], "CONFIRMED")

    def test_player_impact_missing_coverage_is_neutral(self) -> None:
        rows = pd.DataFrame([self.candidate_v4_fixture_row(1)])

        enriched = enrich_player_impact.add_player_impact_fields(rows)
        all_rows, shortlist, top = run_today_shadow_candidate_v5.apply_player_impact_layer(rows)

        self.assertEqual(enriched.loc[0, "player_impact_quality_flag"], "NONE")
        self.assertEqual(float(enriched.loc[0, "home_attacking_core_available_score"]), 0.0)
        self.assertEqual(all_rows.loc[0, "player_impact_adjustment_action"], run_today_shadow_candidate_v5.NOT_APPLIED)
        self.assertEqual(shortlist.loc[0, "market_primary"], "OVER_2_5")
        self.assertEqual(top.loc[0, "market_primary"], "OVER_2_5")

    def test_candidate_v5_attacking_core_weakness_downgrades_goals_market(self) -> None:
        row = self.player_impact_row()
        row.update(
            {
                "home_lineup_attacker_count": 1,
                "home_lineup_midfielder_count": 2,
                "home_lineup_attack_continuity_score": -0.30,
                "home_absence_risk_score": 3.4,
                "home_absence_severity_flag": "HIGH",
            }
        )
        rows = pd.DataFrame([row])

        all_rows, shortlist, top = run_today_shadow_candidate_v5.apply_player_impact_layer(rows)

        self.assertEqual(all_rows.loc[0, "player_impact_adjustment_action"], run_today_shadow_candidate_v5.DOWNGRADE_GOALS)
        self.assertEqual(shortlist.loc[0, "market_primary"], "OVER_1_5")
        self.assertEqual(top.loc[0, "player_impact_original_market"], "OVER_2_5")

    def test_candidate_v5_defensive_weakness_can_support_goals_market(self) -> None:
        row = self.player_impact_row(market="OVER_1_5")
        row.update(
            {
                "away_lineup_defender_count": 2,
                "away_lineup_defense_continuity_score": -0.30,
            }
        )
        rows = pd.DataFrame([row])

        all_rows, shortlist, _top = run_today_shadow_candidate_v5.apply_player_impact_layer(rows)

        self.assertEqual(all_rows.loc[0, "player_impact_adjustment_action"], run_today_shadow_candidate_v5.STRENGTHEN)
        self.assertGreater(float(shortlist.loc[0, "accuracy_confidence_score"]), float(row["accuracy_confidence_score"]))

    def test_candidate_v5_outputs_are_separate_from_baseline_and_candidate_v2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            baseline = pd.DataFrame([self.player_impact_row(10, market="OVER_1_5")])
            v2 = pd.DataFrame([self.player_impact_row(1)])
            baseline.to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)
            v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_shortlist.csv", index=False)
            v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
            baseline_before = (processed_dir / "vsigma_today_competition_top.csv").read_text(encoding="utf-8")
            v2_before = (processed_dir / "vsigma_today_candidate_v2_competition_top.csv").read_text(encoding="utf-8")

            paths = run_today_shadow_candidate_v5.build_candidate_v5_outputs(
                processed_dir,
                today_dir,
                "2026-05-14",
                "Atlantic/Canary",
            )

            self.assertTrue(paths["candidate_v5_shortlist"].exists())
            self.assertTrue(paths["candidate_v5_top"].exists())
            self.assertTrue(paths["comparison_csv"].exists())
            self.assertEqual((processed_dir / "vsigma_today_competition_top.csv").read_text(encoding="utf-8"), baseline_before)
            self.assertEqual((processed_dir / "vsigma_today_candidate_v2_competition_top.csv").read_text(encoding="utf-8"), v2_before)
            self.assertTrue((today_dir / "2026-05-14" / "vsigma_today_candidate_v5_competition_top.csv").exists())

    def test_candidate_v5_post_results_handles_empty_v5_picks_gracefully(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            raw_path = Path(tmp) / "data" / "raw" / "matches.csv"
            processed_dir.mkdir(parents=True)
            raw_path.parent.mkdir(parents=True)
            pd.DataFrame([{"fixture_id": 1, "status": "FT", "goals_home": 1, "goals_away": 1}]).to_csv(raw_path, index=False)
            pd.DataFrame(columns=["fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_competition_top.csv",
                index=False,
            )
            pd.DataFrame(columns=["fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_candidate_v2_competition_top.csv",
                index=False,
            )
            pd.DataFrame(columns=["fixture_id", "market_primary", "player_impact_adjustment_action"]).to_csv(
                processed_dir / "vsigma_today_candidate_v5_competition_top.csv",
                index=False,
            )

            with patch.object(run_today_shadow_candidate_v5_post_results, "RAW_MATCHES_CSV", raw_path):
                paths = run_today_shadow_candidate_v5_post_results.build_candidate_v5_post_results(
                    processed_dir,
                    today_dir,
                    "2026-05-14",
                    "Atlantic/Canary",
                )

            ledger = pd.read_csv(paths["candidate_v5_results_ledger"])
            summary = pd.read_csv(paths["candidate_v5_results_summary"])
            report = paths["result_comparison_report"].read_text(encoding="utf-8")
            self.assertEqual(len(ledger), 0)
            self.assertIn("fixture_id", ledger.columns)
            self.assertEqual(int(summary.loc[0, "pick_count"]), 0)
            self.assertIn("CANDIDATE_V5_NO_BET", report)

    def prediction_payload(
        self,
        *,
        winner_id: int | None = None,
        advice: str = "Winner : Home",
        home: str = "62%",
        draw: str = "20%",
        away: str = "18%",
        under_over: str = "Over 2.5",
    ) -> dict[str, object]:
        winner = {"id": winner_id, "name": "Home 1"} if winner_id is not None else {}
        return {
            "response": [
                {
                    "predictions": {
                        "winner": winner,
                        "advice": advice,
                        "under_over": under_over,
                        "percent": {"home": home, "draw": draw, "away": away},
                        "goals": {"home": "-2.5", "away": "-1.5"},
                    }
                }
            ]
        }

    def candidate_v6_fixture_row(
        self,
        fixture_id: int = 1,
        market: str = "OVER_2_5",
        failure: str = "LOW_CONVERSION",
    ) -> dict[str, object]:
        row = self.candidate_v4_fixture_row(fixture_id, market=market, failure=failure)
        row.update({"home_team_id": 100 + fixture_id, "away_team_id": 200 + fixture_id})
        return row

    def test_api_predictions_fields_are_generated(self) -> None:
        rows = pd.DataFrame([self.candidate_v6_fixture_row(1, market="OVER_2_5")])

        enriched, counters = enrich_api_predictions_benchmark.add_api_prediction_benchmark_fields(
            rows,
            payload_by_fixture={1: self.prediction_payload(winner_id=101, advice="Over 2.5 goals", under_over="Over 2.5")},
        )

        self.assertEqual(int(enriched.loc[0, "api_prediction_available_flag"]), 1)
        self.assertEqual(enriched.loc[0, "api_prediction_quality_flag"], "FULL")
        self.assertEqual(enriched.loc[0, "api_prediction_alignment_flag"], "ALIGNED")
        self.assertGreater(float(enriched.loc[0, "api_prediction_confidence_adjustment"]), 0.0)
        self.assertEqual(int(counters["available_rows"]), 1)

    def test_api_predictions_missing_data_is_neutral_unknown(self) -> None:
        rows = pd.DataFrame([self.candidate_v6_fixture_row(1)])

        enriched, _counters = enrich_api_predictions_benchmark.add_api_prediction_benchmark_fields(
            rows,
            use_api=False,
            payload_by_fixture={},
        )
        all_rows, shortlist, top, _ = run_today_shadow_candidate_v6.apply_api_predictions_benchmark_layer(
            rows,
            use_api=False,
            payload_by_fixture={},
        )

        self.assertEqual(enriched.loc[0, "api_prediction_quality_flag"], "UNKNOWN")
        self.assertEqual(enriched.loc[0, "api_prediction_alignment_flag"], "UNKNOWN")
        self.assertEqual(all_rows.loc[0, "api_prediction_benchmark_action"], run_today_shadow_candidate_v6.NOT_APPLIED)
        self.assertEqual(shortlist.loc[0, "market_primary"], "OVER_2_5")
        self.assertEqual(top.loc[0, "market_primary"], "OVER_2_5")

    def test_candidate_v6_aligned_prediction_modestly_strengthens_confidence(self) -> None:
        rows = pd.DataFrame([self.candidate_v6_fixture_row(1, market="OVER_2_5", failure="")])

        all_rows, shortlist, _top, _ = run_today_shadow_candidate_v6.apply_api_predictions_benchmark_layer(
            rows,
            use_api=False,
            payload_by_fixture={1: self.prediction_payload(winner_id=101, advice="Over 2.5 goals", under_over="Over 2.5")},
        )

        self.assertEqual(all_rows.loc[0, "api_prediction_benchmark_action"], run_today_shadow_candidate_v6.ALIGNED_STRENGTHEN)
        self.assertGreater(float(shortlist.loc[0, "accuracy_confidence_score"]), float(rows.loc[0, "accuracy_confidence_score"]))

    def test_candidate_v6_disagreement_can_weaken_fragile_pick_to_secondary(self) -> None:
        rows = pd.DataFrame([self.candidate_v6_fixture_row(1, market="OVER_2_5", failure="LOW_CONVERSION")])

        all_rows, shortlist, top, _ = run_today_shadow_candidate_v6.apply_api_predictions_benchmark_layer(
            rows,
            use_api=False,
            payload_by_fixture={1: self.prediction_payload(advice="Under 2.5 goals", under_over="Under 2.5")},
        )

        self.assertEqual(all_rows.loc[0, "api_prediction_alignment_flag"], "DISAGREEMENT")
        self.assertEqual(all_rows.loc[0, "api_prediction_benchmark_action"], run_today_shadow_candidate_v6.DISAGREEMENT_SECONDARY)
        self.assertEqual(int(all_rows.loc[0, "api_prediction_benchmark_changed_inclusion_flag"]), 1)
        self.assertEqual(len(shortlist), 0)
        self.assertEqual(len(top), 0)

    def test_candidate_v6_api_predictions_do_not_create_picks_alone(self) -> None:
        rows = pd.DataFrame(columns=["fixture_id", "market_primary"])

        _all_rows, shortlist, top, _ = run_today_shadow_candidate_v6.apply_api_predictions_benchmark_layer(
            rows,
            use_api=False,
            payload_by_fixture={1: self.prediction_payload()},
        )

        self.assertEqual(len(shortlist), 0)
        self.assertEqual(len(top), 0)

    def test_candidate_v6_outputs_are_separate_from_baseline_and_candidate_v2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            baseline = pd.DataFrame([self.candidate_v6_fixture_row(10, market="OVER_1_5")])
            v2 = pd.DataFrame([self.candidate_v6_fixture_row(1, market="OVER_1_5", failure="")])
            baseline.to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)
            v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_shortlist.csv", index=False)
            v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
            baseline_before = (processed_dir / "vsigma_today_competition_top.csv").read_text(encoding="utf-8")
            v2_before = (processed_dir / "vsigma_today_candidate_v2_competition_top.csv").read_text(encoding="utf-8")

            paths = run_today_shadow_candidate_v6.build_candidate_v6_outputs(
                processed_dir,
                today_dir,
                "2026-05-14",
                "Atlantic/Canary",
                use_api=False,
                payload_by_fixture={1: self.prediction_payload(advice="Over 1.5 goals", under_over="Over 1.5")},
            )

            self.assertTrue(paths["candidate_v6_shortlist"].exists())
            self.assertTrue(paths["candidate_v6_top"].exists())
            self.assertTrue(paths["comparison_csv"].exists())
            self.assertTrue(paths["shadow_pre_journal"].exists())
            self.assertEqual((processed_dir / "vsigma_today_competition_top.csv").read_text(encoding="utf-8"), baseline_before)
            self.assertEqual((processed_dir / "vsigma_today_candidate_v2_competition_top.csv").read_text(encoding="utf-8"), v2_before)
            self.assertTrue((today_dir / "2026-05-14" / "vsigma_today_candidate_v6_competition_top.csv").exists())

    def test_candidate_v6_post_results_handles_empty_v6_picks_gracefully(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            raw_path = Path(tmp) / "data" / "raw" / "matches.csv"
            processed_dir.mkdir(parents=True)
            raw_path.parent.mkdir(parents=True)
            pd.DataFrame([{"fixture_id": 1, "status": "FT", "goals_home": 1, "goals_away": 1}]).to_csv(raw_path, index=False)
            pd.DataFrame(columns=["fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_competition_top.csv",
                index=False,
            )
            pd.DataFrame(columns=["fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_candidate_v2_competition_top.csv",
                index=False,
            )
            pd.DataFrame(columns=["fixture_id", "market_primary", "api_prediction_benchmark_action"]).to_csv(
                processed_dir / "vsigma_today_candidate_v6_competition_top.csv",
                index=False,
            )

            with patch.object(run_today_shadow_candidate_v6_post_results, "RAW_MATCHES_CSV", raw_path):
                paths = run_today_shadow_candidate_v6_post_results.build_candidate_v6_post_results(
                    processed_dir,
                    today_dir,
                    "2026-05-14",
                    "Atlantic/Canary",
                )

            ledger = pd.read_csv(paths["candidate_v6_results_ledger"])
            summary = pd.read_csv(paths["candidate_v6_results_summary"])
            report = paths["result_comparison_report"].read_text(encoding="utf-8")
            self.assertEqual(len(ledger), 0)
            self.assertIn("fixture_id", ledger.columns)
            self.assertEqual(int(summary.loc[0, "pick_count"]), 0)
            self.assertIn("CANDIDATE_V6_NO_BET", report)
            self.assertTrue(paths["shadow_post_journal"].exists())

    def test_today_pipeline_declares_shadow_candidate_v4_steps(self) -> None:
        self.assertEqual(
            run_today_match_pipeline.SHADOW_CANDIDATE_V4_STEP,
            "scripts/run_today_shadow_candidate_v4.py",
        )
        self.assertEqual(
            run_today_post_results_pipeline.SHADOW_CANDIDATE_V4_POST_STEP,
            "scripts/run_today_shadow_candidate_v4_post_results.py",
        )

    def test_today_pipeline_declares_shadow_candidate_v5_steps(self) -> None:
        self.assertEqual(
            run_today_match_pipeline.SHADOW_CANDIDATE_V5_STEP,
            "scripts/run_today_shadow_candidate_v5.py",
        )
        self.assertEqual(
            run_today_post_results_pipeline.SHADOW_CANDIDATE_V5_POST_STEP,
            "scripts/run_today_shadow_candidate_v5_post_results.py",
        )

    def test_today_pipeline_declares_shadow_candidate_v6_steps(self) -> None:
        self.assertEqual(
            run_today_match_pipeline.SHADOW_CANDIDATE_V6_STEP,
            "scripts/run_today_shadow_candidate_v6.py",
        )
        self.assertEqual(
            run_today_post_results_pipeline.SHADOW_CANDIDATE_V6_POST_STEP,
            "scripts/run_today_shadow_candidate_v6_post_results.py",
        )

    def test_today_pipeline_journal_files_are_declared_for_snapshot_context(self) -> None:
        self.assertIn(
            build_daily_decision_journal.PRE_SUMMARY_FILENAME,
            run_today_match_pipeline.TODAY_JOURNAL_FILES,
        )
        self.assertIn(
            build_daily_decision_journal.POST_SUMMARY_FILENAME,
            run_today_post_results_pipeline.POST_RESULTS_JOURNAL_FILES,
        )

    def test_today_pipeline_declares_shadow_candidate_v2_steps(self) -> None:
        self.assertEqual(
            run_today_match_pipeline.SHADOW_CANDIDATE_V2_STEP,
            "scripts/run_today_shadow_candidate_v2.py",
        )
        self.assertEqual(
            run_today_post_results_pipeline.SHADOW_CANDIDATE_V2_POST_STEP,
            "scripts/run_today_shadow_candidate_v2_post_results.py",
        )

    def test_today_post_results_pipeline_runs_steps_in_order_and_snapshots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            processed_dir.mkdir(parents=True)
            today_dir = processed_dir / "today"
            shortlist_path, ledger_path = self.write_post_results_fixture_files(processed_dir)
            step_calls: list[str] = []

            def fake_run_step(script_path: str) -> None:
                step_calls.append(script_path)

            snapshot_files = [
                processed_dir / path.name
                for path in run_today_post_results_pipeline.POST_RESULTS_SNAPSHOT_FILES
            ]
            for path in snapshot_files:
                if not path.exists():
                    pd.DataFrame([{"date": "2026-05-09"}]).to_csv(path, index=False)
            patchers = [
                patch.object(run_today_post_results_pipeline, "SHORTLIST_CSV", shortlist_path),
                patch.object(run_today_post_results_pipeline, "LEDGER_CSV", ledger_path),
                patch.object(run_today_post_results_pipeline, "PROCESSED_DIR", processed_dir),
                patch.object(run_today_post_results_pipeline, "TODAY_DIR", today_dir),
                patch.object(run_today_post_results_pipeline, "POST_RESULTS_SNAPSHOT_FILES", snapshot_files),
                patch.object(run_today_post_results_pipeline, "run_step", side_effect=fake_run_step),
                patch.object(run_today_post_results_pipeline, "run_shadow_candidate_v2_post_step"),
                patch.object(run_today_post_results_pipeline, "run_shadow_candidate_v4_post_step"),
                patch.object(run_today_post_results_pipeline, "run_shadow_candidate_v5_post_step"),
                patch.object(run_today_post_results_pipeline, "run_shadow_candidate_v6_post_step"),
                patch.object(run_today_post_results_pipeline, "run_daily_hardening_steps"),
            ]

            with ExitStack() as stack:
                for patcher in patchers:
                    stack.enter_context(patcher)
                snapshot_dir, report_path, ledger = (
                    run_today_post_results_pipeline.run_today_post_results_pipeline(
                        "2026-05-09",
                        "Atlantic/Canary",
                    )
                )

            self.assertEqual(step_calls, run_today_post_results_pipeline.POST_RESULTS_STEPS)
            self.assertEqual(snapshot_dir, today_dir / "2026-05-09")
            self.assertTrue(report_path.exists())
            self.assertEqual(len(ledger), 1)
            for src in snapshot_files:
                self.assertTrue((snapshot_dir / src.name).exists())
            self.assertTrue((snapshot_dir / build_daily_decision_journal.POST_SUMMARY_FILENAME).exists())

    def test_shadow_candidate_v2_post_results_outputs_and_journal_are_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "data" / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            raw = pd.DataFrame(
                [
                    {"fixture_id": 1, "status": "FT", "goals_home": 2, "goals_away": 0},
                    {"fixture_id": 2, "status": "FT", "goals_home": 1, "goals_away": 2},
                ]
            )
            baseline_top = pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "date": "2026-05-09",
                        "league": "League A",
                        "home_team": "A",
                        "away_team": "B",
                        "market_primary": "OVER_1_5",
                        "accuracy_mode_rank": 1,
                        "primary_odds_used": 1.5,
                    }
                ]
            )
            candidate_top = pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "date": "2026-05-09",
                        "league": "League A",
                        "home_team": "A",
                        "away_team": "B",
                        "market_primary": "OVER_1_5",
                        "accuracy_mode_rank": 1,
                        "primary_odds_used": 1.5,
                    },
                    {
                        "fixture_id": 2,
                        "date": "2026-05-09",
                        "league": "League B",
                        "home_team": "C",
                        "away_team": "D",
                        "market_primary": "AWAY_WIN",
                        "accuracy_mode_rank": 2,
                        "primary_odds_used": 2.1,
                    },
                ]
            )
            candidate_top.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)

            paths = run_today_shadow_candidate_v2_post_results.write_shadow_post_outputs(
                processed_dir,
                today_dir,
                "2026-05-09",
                "Atlantic/Canary",
                raw,
                baseline_top,
                candidate_top,
            )

            snapshot_dir = today_dir / "2026-05-09"
            self.assertTrue(paths["candidate_results_ledger"].exists())
            self.assertTrue(paths["candidate_results_summary"].exists())
            self.assertTrue(paths["result_comparison_csv"].exists())
            self.assertTrue(paths["result_comparison_report"].exists())
            self.assertTrue((snapshot_dir / build_daily_decision_journal.SHADOW_CANDIDATE_V2_POST_SUMMARY_FILENAME).exists())
            comparison = pd.read_csv(paths["result_comparison_csv"])
            self.assertIn("CANDIDATE_V2_ONLY", comparison["comparison_status"].tolist())
            summary = pd.read_csv(paths["candidate_results_summary"])
            self.assertEqual(int(summary.loc[0, "pick_count"]), 2)

    def test_today_post_results_snapshot_copy_list_includes_outputs(self) -> None:
        names = {path.name for path in run_today_post_results_pipeline.POST_RESULTS_SNAPSHOT_FILES}
        self.assertTrue(
            {
                "vsigma_today_premium_core.csv",
                "vsigma_today_execution_shortlist.csv",
                "vsigma_today_execution_bets_only.csv",
                "vsigma_today_execution_summary.csv",
                "vsigma_execution_shortlist_results_ledger.csv",
                "vsigma_execution_shortlist_results_summary.csv",
                "vsigma_market_results_labeled.csv",
                "vsigma_market_results_report.csv",
                "refresh_finished_results_by_date_report.csv",
            }.issubset(names)
        )

    def test_today_post_results_report_generation_from_temp_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            snapshot_dir = Path(tmp) / "today" / "2026-05-09"
            snapshot_dir.mkdir(parents=True)
            shortlist = pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "final_recommendation": "BET",
                    },
                    {
                        "fixture_id": 2,
                        "final_recommendation": "LEAN_PLAY",
                    },
                ]
            )
            ledger = pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "ledger_result_status": "RESULT_AVAILABLE",
                        "actionable_result": "WIN",
                        "actionable_profit_units": 0.8,
                        "primary_profit_units": 0.8,
                    },
                    {
                        "fixture_id": 2,
                        "ledger_result_status": "PENDING",
                        "actionable_result": "PENDING",
                        "actionable_profit_units": pd.NA,
                        "primary_profit_units": pd.NA,
                    },
                ]
            )

            report_path = run_today_post_results_pipeline.write_post_results_report(
                "2026-05-09",
                "Atlantic/Canary",
                shortlist,
                ledger,
                snapshot_dir,
            )

            report = pd.read_csv(report_path)
            self.assertEqual(int(report.loc[0, "shortlist_rows"]), 2)
            self.assertEqual(int(report.loc[0, "shortlist_bet_rows"]), 1)
            self.assertEqual(int(report.loc[0, "result_available_rows"]), 1)
            self.assertEqual(int(report.loc[0, "pending_rows"]), 1)
            self.assertEqual(float(report.loc[0, "profit_units_total"]), 0.8)
            self.assertEqual(float(report.loc[0, "roi_percent"]), 80.0)

    def test_today_post_results_ledger_fixture_ids_must_match_shortlist(self) -> None:
        shortlist = pd.DataFrame(
            [
                {"fixture_id": 1, "market_primary": "OVER_1_5", "execution_rank": 1},
            ]
        )
        ledger = pd.DataFrame(
            [
                {
                    "execution_rank": 1,
                    "fixture_id": 2,
                    "market_primary": "OVER_1_5",
                    "ledger_result_status": "PENDING",
                    "actionable_result": "PENDING",
                    "actionable_profit_units": pd.NA,
                    "primary_profit_units": pd.NA,
                },
            ]
        )

        with self.assertRaisesRegex(ValueError, "outside shortlist"):
            run_today_post_results_pipeline.validate_ledger_against_shortlist(ledger, shortlist)

    def test_today_post_results_ledger_rows_must_equal_shortlist_rows(self) -> None:
        shortlist = pd.DataFrame(
            [
                {"fixture_id": 1, "market_primary": "OVER_1_5", "execution_rank": 1},
                {"fixture_id": 2, "market_primary": "OVER_2_5", "execution_rank": 2},
            ]
        )
        ledger = pd.DataFrame(
            [
                {
                    "execution_rank": 1,
                    "fixture_id": 1,
                    "market_primary": "OVER_1_5",
                    "ledger_result_status": "PENDING",
                    "actionable_result": "PENDING",
                    "actionable_profit_units": pd.NA,
                    "primary_profit_units": pd.NA,
                },
            ]
        )

        with self.assertRaisesRegex(ValueError, "do not equal shortlist rows"):
            run_today_post_results_pipeline.validate_ledger_against_shortlist(ledger, shortlist)

    def test_historical_execution_shortlist_reconstruction_is_deterministic_with_caps(self) -> None:
        premium_rows = [
            self.shortlist_row(1, "APPROVED_PREMIUM", "BET", "TOP_CORE", 95, 0.20, "League A", "OVER_1_5", 1),
            self.shortlist_row(2, "APPROVED_PREMIUM", "BET", "TOP_CORE", 94, 0.19, "League A", "OVER_1_5", 2),
            self.shortlist_row(3, "APPROVED_PREMIUM", "BET", "TOP_CORE", 93, 0.18, "League A", "OVER_1_5", 3),
            self.shortlist_row(4, "APPROVED_PREMIUM", "BET", "TOP_CORE", 92, 0.17, "League B", "OVER_2_5", 4),
            self.shortlist_row(4, "APPROVED_PREMIUM", "BET", "TOP_CORE", 91, 0.16, "League C", "BTTS_YES", 5),
            self.shortlist_row(5, "APPROVED_PREMIUM", "BET", "TOP_CORE", 90, 0.15, "League B", "OVER_2_5", 6),
            self.shortlist_row(6, "APPROVED_PREMIUM", "BET", "TOP_CORE", 89, 0.14, "League C", "BTTS_YES", 7),
            self.shortlist_row(7, "APPROVED_PREMIUM", "BET", "TOP_CORE", 88, 0.13, "League D", "HOME_WIN", 8),
            self.shortlist_row(8, "APPROVED_PREMIUM", "BET", "TOP_CORE", 87, 0.12, "League D", "AWAY_WIN", 9),
            self.shortlist_row(9, "APPROVED_PREMIUM", "BET", "TOP_CORE", 86, 0.11, "League E", "DRAW", 10),
        ]

        shortlist = build_historical_execution_shortlist_backtest.reconstruct_execution_shortlist(
            pd.DataFrame(premium_rows),
            pd.DataFrame(columns=build_today_execution_shortlist.REQUIRED_COLUMNS),
        )

        self.assertEqual(len(shortlist), 8)
        self.assertNotIn(3, shortlist["fixture_id"].tolist())
        self.assertEqual(shortlist["fixture_id"].tolist().count(4), 1)
        self.assertLessEqual(int(shortlist["league"].value_counts().max()), 2)
        self.assertLessEqual(int(shortlist["market_primary"].value_counts().max()), 2)
        self.assertEqual(shortlist["execution_rank"].tolist(), list(range(1, 9)))
        self.assertTrue(shortlist["execution_score"].is_monotonic_decreasing)

    def test_historical_execution_shortlist_phase_ordering(self) -> None:
        premium_rows = [
            self.shortlist_row(101, "APPROVED_PREMIUM", "BET", "TOP_CORE", 80, 0.08, "League A", "OVER_1_5", 1),
            self.shortlist_row(102, "APPROVED_PREMIUM", "BET", "WATCH", 99, 0.10, "League B", "OVER_1_5", 2, model_prob=0.85),
            self.shortlist_row(103, "APPROVED_PREMIUM", "BET", "WATCH", 98, 0.03, "League C", "OVER_1_5", 3, model_prob=0.85),
            self.shortlist_row(104, "APPROVED_PREMIUM", "LEAN_PLAY", "WATCH", 97, 0.12, "League D", "OVER_2_5", 4, model_prob=0.86),
            self.shortlist_row(105, "APPROVED_PREMIUM", "BET", "WATCH", 96, 0.20, "League E", "BTTS_YES", 5, model_prob=0.88),
        ]
        standard_rows = [
            self.shortlist_row(201, "APPROVED_STANDARD", "BET", "TOP_CORE", 100, 0.05, "League I", "MKT_I", 9),
        ]

        shortlist = build_historical_execution_shortlist_backtest.reconstruct_execution_shortlist(
            pd.DataFrame(premium_rows),
            pd.DataFrame(standard_rows),
        )

        self.assertEqual(len(shortlist), 3)
        self.assertIn(201, shortlist["fixture_id"].tolist())
        self.assertEqual(
            shortlist.set_index("fixture_id").loc[101, "execution_shortlist_source"],
            "PREMIUM_CORE",
        )
        self.assertEqual(
            shortlist.set_index("fixture_id").loc[102, "execution_shortlist_source"],
            "PREMIUM_EXTENDED",
        )
        self.assertEqual(
            shortlist.set_index("fixture_id").loc[201, "execution_shortlist_source"],
            "STANDARD_FILL",
        )

    def test_historical_execution_shortlist_join_to_labeled_results(self) -> None:
        shortlist = pd.DataFrame(
            [
                {
                    "execution_rank": 1,
                    "execution_shortlist_source": "PREMIUM_CORE",
                    "fixture_id": 1,
                    "league": "League A",
                    "home_team": "Home 1",
                    "away_team": "Away 1",
                    "market_primary": "OVER_1_5",
                    "final_execution_bucket": "APPROVED_PREMIUM",
                    "final_recommendation": "BET",
                    "execution_score": 100,
                    "selection_score": 80,
                    "primary_model_prob": 0.8,
                    "primary_odds_used": 1.8,
                    "primary_edge": 0.08,
                },
                {
                    "execution_rank": 2,
                    "execution_shortlist_source": "PREMIUM_EXTENDED",
                    "fixture_id": 2,
                    "league": "League B",
                    "home_team": "Home 2",
                    "away_team": "Away 2",
                    "market_primary": "AWAY_WIN",
                    "final_execution_bucket": "APPROVED_PREMIUM",
                    "final_recommendation": "BET",
                    "execution_score": 99,
                    "selection_score": 79,
                    "primary_model_prob": 0.8,
                    "primary_odds_used": 2.0,
                    "primary_edge": 0.08,
                },
                {
                    "execution_rank": 3,
                    "execution_shortlist_source": "STANDARD_FILL",
                    "fixture_id": 3,
                    "league": "League C",
                    "home_team": "Home 3",
                    "away_team": "Away 3",
                    "market_primary": "BTTS_YES",
                    "final_execution_bucket": "APPROVED_STANDARD",
                    "final_recommendation": "LEAN_PLAY",
                    "execution_score": 98,
                    "selection_score": 78,
                    "primary_model_prob": 0.8,
                    "primary_odds_used": 1.9,
                    "primary_edge": 0.08,
                },
            ]
        )
        labeled = pd.DataFrame(
            [
                {
                    "fixture_id": 1,
                    "market_primary": "OVER_1_5",
                    "actionable_result": "SKIPPED",
                    "actionable_profit_units": pd.NA,
                    "primary_result": "WIN",
                    "primary_profit_units": 0.8,
                },
                {
                    "fixture_id": 2,
                    "market_primary": "OVER_2_5",
                    "actionable_result": "LOSS",
                    "actionable_profit_units": -1.0,
                    "primary_result": "LOSS",
                    "primary_profit_units": -1.0,
                },
            ]
        )

        joined = build_historical_execution_shortlist_backtest.join_shortlist_to_labeled(
            shortlist,
            labeled,
            "2026-05-01",
        )

        self.assertEqual(
            joined.set_index("fixture_id")["result_status"].to_dict(),
            {
                1: "RESULT_AVAILABLE",
                2: "UNMATCHED_MARKET",
                3: "UNMATCHED_FIXTURE",
            },
        )
        self.assertEqual(joined.set_index("fixture_id").loc[1, "actionable_result"], "WIN")
        self.assertAlmostEqual(float(joined.set_index("fixture_id").loc[1, "profit_units"]), 0.8)

    def test_historical_execution_shortlist_summary_math(self) -> None:
        rows = pd.DataFrame(
            [
                {"result_status": "RESULT_AVAILABLE", "actionable_result": "WIN", "profit_units": 0.8, "market_primary": "A"},
                {"result_status": "RESULT_AVAILABLE", "actionable_result": "LOSS", "profit_units": -1.0, "market_primary": "A"},
                {"result_status": "RESULT_AVAILABLE", "actionable_result": "PUSH", "profit_units": 0.0, "market_primary": "B"},
                {"result_status": "UNMATCHED_MARKET", "actionable_result": pd.NA, "profit_units": pd.NA, "market_primary": "B"},
            ]
        )

        summary = build_historical_execution_shortlist_backtest.build_summary(rows)
        self.assertEqual(int(summary.loc[0, "rows_total"]), 4)
        self.assertEqual(int(summary.loc[0, "graded_rows"]), 3)
        self.assertEqual(int(summary.loc[0, "wins"]), 1)
        self.assertEqual(int(summary.loc[0, "losses"]), 1)
        self.assertEqual(int(summary.loc[0, "pushes"]), 1)
        self.assertAlmostEqual(float(summary.loc[0, "profit_units_total"]), -0.2)
        self.assertAlmostEqual(float(summary.loc[0, "roi_percent"]), -6.666667)

    def test_historical_pipeline_runs_execution_shortlist_backtest_after_calibration(self) -> None:
        self.assertEqual(
            run_historical_labeling_pipeline.HISTORICAL_EXECUTION_SHORTLIST_BACKTEST_STEP,
            "scripts/build_historical_execution_shortlist_backtest.py",
        )

    def execution_mode_rows(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "historical_batch_date": "2026-05-01",
                    "execution_shortlist_source": "PREMIUM_CORE",
                    "actionable_result": "WIN",
                    "result_status": "RESULT_AVAILABLE",
                    "profit_units": 0.8,
                    "primary_odds_used": 1.8,
                    "primary_edge": 0.08,
                    "execution_score": 100,
                },
                {
                    "historical_batch_date": "2026-05-01",
                    "execution_shortlist_source": "STANDARD_FILL",
                    "actionable_result": "LOSS",
                    "result_status": "RESULT_AVAILABLE",
                    "profit_units": -1.0,
                    "primary_odds_used": 2.0,
                    "primary_edge": 0.05,
                    "execution_score": 90,
                },
                {
                    "historical_batch_date": "2026-05-02",
                    "execution_shortlist_source": "PREMIUM_EXTENDED",
                    "actionable_result": "WIN",
                    "result_status": "RESULT_AVAILABLE",
                    "profit_units": 0.5,
                    "primary_odds_used": 1.5,
                    "primary_edge": 0.04,
                    "execution_score": 85,
                },
                {
                    "historical_batch_date": "2026-05-02",
                    "execution_shortlist_source": "PREMIUM_EXTENDED",
                    "actionable_result": pd.NA,
                    "result_status": "UNMATCHED_MARKET",
                    "profit_units": pd.NA,
                    "primary_odds_used": 1.7,
                    "primary_edge": 0.03,
                    "execution_score": 80,
                },
            ]
        )

    def test_execution_mode_comparison_deterministic_mode_filtering(self) -> None:
        rows = self.execution_mode_rows()

        self.assertEqual(
            build_execution_mode_comparison.filter_mode(rows, "CORE_ONLY")[
                "execution_shortlist_source"
            ].tolist(),
            ["PREMIUM_CORE"],
        )
        self.assertEqual(
            build_execution_mode_comparison.filter_mode(rows, "CORE_PLUS_STANDARD")[
                "execution_shortlist_source"
            ].tolist(),
            ["PREMIUM_CORE", "STANDARD_FILL"],
        )
        self.assertEqual(len(build_execution_mode_comparison.filter_mode(rows, "FULL_SHORTLIST")), 4)

    def test_execution_mode_comparison_summary_math(self) -> None:
        rows = self.execution_mode_rows()
        overall = build_execution_mode_comparison.build_overall(rows)
        full = overall.set_index("mode").loc["FULL_SHORTLIST"]

        self.assertEqual(int(full["rows_total"]), 4)
        self.assertEqual(int(full["graded_rows"]), 3)
        self.assertEqual(int(full["wins"]), 2)
        self.assertEqual(int(full["losses"]), 1)
        self.assertAlmostEqual(float(full["profit_units_total"]), 0.3)
        self.assertAlmostEqual(float(full["roi_percent"]), 10.0)
        self.assertAlmostEqual(float(full["hit_rate"]), 66.666667)
        self.assertAlmostEqual(float(full["avg_odds"]), 1.766667)
        self.assertAlmostEqual(float(full["avg_edge"]), 0.05)
        self.assertAlmostEqual(float(full["avg_execution_score"]), 88.75)
        self.assertAlmostEqual(float(full["max_drawdown"]), 0.0)

    def test_execution_mode_comparison_source_inclusion_exclusion(self) -> None:
        rows = self.execution_mode_rows()
        mix = build_execution_mode_comparison.build_by_source_mix(rows)

        core_only_sources = mix[mix["mode"].eq("CORE_ONLY")]["execution_shortlist_source"].tolist()
        core_standard_sources = mix[
            mix["mode"].eq("CORE_PLUS_STANDARD")
        ]["execution_shortlist_source"].tolist()
        full_sources = mix[mix["mode"].eq("FULL_SHORTLIST")]["execution_shortlist_source"].tolist()

        self.assertEqual(core_only_sources, ["PREMIUM_CORE"])
        self.assertEqual(core_standard_sources, ["PREMIUM_CORE", "STANDARD_FILL"])
        self.assertEqual(
            full_sources,
            ["PREMIUM_CORE", "PREMIUM_EXTENDED", "STANDARD_FILL"],
        )

    def test_execution_mode_comparison_includes_competition_accuracy_mode(self) -> None:
        rows = self.execution_mode_rows()
        rows["accuracy_mode_eligible_flag"] = [1, 0, 1, 0]
        rows["accuracy_mode_bucket"] = [
            "ACCURACY_CORE",
            "ACCURACY_REJECTED",
            "ACCURACY_EXTENDED_STRONG",
            "ACCURACY_REJECTED",
        ]
        rows["market_primary"] = ["OVER_1_5", "HOME_WIN", "OVER_1_5", "BTTS_YES"]

        competition = build_execution_mode_comparison.filter_mode(rows, "COMPETITION_ACCURACY_MODE")
        overall = build_execution_mode_comparison.build_overall(rows)
        by_market = build_execution_mode_comparison.build_by_market(rows)
        by_bucket = build_execution_mode_comparison.build_by_bucket(rows)

        self.assertEqual(len(competition), 2)
        self.assertIn("COMPETITION_ACCURACY_MODE", overall["mode"].tolist())
        self.assertEqual(
            int(overall.set_index("mode").loc["COMPETITION_ACCURACY_MODE", "rows_total"]),
            2,
        )
        self.assertIn("OVER_1_5", by_market["market_primary"].tolist())
        self.assertIn("ACCURACY_CORE", by_bucket["accuracy_mode_bucket"].tolist())

    def test_historical_pipeline_runs_final_exports_immediately_after_deep_analysis(self) -> None:
        with patch.object(run_historical_labeling_pipeline, "run_step") as run_step:
            run_historical_labeling_pipeline.run_deep_analysis_and_final_exports()

        self.assertEqual(
            [call.args[0] for call in run_step.call_args_list],
            [
                "scripts/deep_analysis_candidates.py",
                "scripts/final_execution_exports.py",
                "scripts/validate_final_execution_exports.py",
            ],
        )

    def test_historical_pipeline_marks_final_export_validation_errors_as_fail_fast(self) -> None:
        validation_error = subprocess.CalledProcessError(
            1,
            [sys.executable, run_historical_labeling_pipeline.FINAL_EXECUTION_EXPORT_VALIDATION_STEP],
        )
        calibration_error = subprocess.CalledProcessError(
            1,
            [sys.executable, "scripts/run_vsigma_backtest_calibration.py"],
        )

        self.assertTrue(run_historical_labeling_pipeline.is_final_execution_validation_error(validation_error))
        self.assertFalse(run_historical_labeling_pipeline.is_final_execution_validation_error(calibration_error))

    def test_historical_pipeline_main_combines_temp_snapshots_and_refreshes_final_exports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_dir = tmp_path / "data" / "raw"
            processed_dir = tmp_path / "data" / "processed"
            historical_dir = processed_dir / "historical"
            raw_matches_csv = raw_dir / "matches.csv"
            raw_json_path = raw_dir / "api_matches.json"
            standard_deep_csv = processed_dir / "vsigma_deep_analysis_candidates.csv"
            standard_labeled_csv = processed_dir / "vsigma_market_results_labeled.csv"
            standard_backtest_source = processed_dir / "vsigma_backtest_enriched_source.csv"
            standard_calibration_candidates = (
                processed_dir / "vsigma_threshold_calibration_candidates.csv"
            )
            final_export_files = [
                processed_dir / "vsigma_final_approved_premium_candidates.csv",
                processed_dir / "vsigma_final_approved_standard_candidates.csv",
                processed_dir / "vsigma_final_approved_candidates.csv",
                processed_dir / "vsigma_final_downgraded_candidates.csv",
                processed_dir / "vsigma_final_blocked_candidates.csv",
                processed_dir / "vsigma_final_watch_candidates.csv",
                processed_dir / "vsigma_final_governance_summary.csv",
            ]
            snapshot_files = [
                raw_matches_csv,
                processed_dir / "vsigma_core_shortlist.csv",
                standard_deep_csv,
                *final_export_files,
                standard_labeled_csv,
                processed_dir / "vsigma_market_results_report.csv",
                processed_dir / "refresh_finished_results_by_date_report.csv",
            ]
            per_date_generated_files = [
                processed_dir / "matches_league_filtered.csv",
                processed_dir / "matches_league_rejected.csv",
                processed_dir / "league_filter_report.csv",
                processed_dir / "matches_vsigma_scored_v3.csv",
                processed_dir / "vsigma_score_report_v3.csv",
                processed_dir / "vsigma_top_candidates_v3.csv",
                processed_dir / "tie_state_adjust_report.csv",
                processed_dir / "vsigma_core_shortlist.csv",
                processed_dir / "vsigma_core_shortlist_report.csv",
                standard_deep_csv,
                *final_export_files,
                standard_labeled_csv,
                processed_dir / "vsigma_market_results_report.csv",
                processed_dir / "refresh_finished_results_by_date_report.csv",
            ]
            fixture_rows = {
                "2026-05-01": {
                    "date": "2026-05-01",
                    "fixture_id": 9001,
                    "home_team": "Temp Home 1",
                    "away_team": "Temp Away 1",
                    "status": "FT",
                },
                "2026-05-02": {
                    "date": "2026-05-02",
                    "fixture_id": 9002,
                    "home_team": "Temp Home 2",
                    "away_team": "Temp Away 2",
                    "status": "FT",
                },
            }
            run_step_calls: list[str] = []

            def fetch_without_api(_client, match_date: str, _timezone_name: str) -> pd.DataFrame:
                return pd.DataFrame([fixture_rows[match_date]])

            def read_current_raw() -> pd.DataFrame:
                return pd.read_csv(raw_matches_csv)

            def write_final_exports() -> None:
                deep = pd.read_csv(standard_deep_csv)
                approved_premium = deep.copy()
                approved_premium["final_execution_bucket"] = "APPROVED_PREMIUM"
                approved_premium.to_csv(final_export_files[0], index=False)

                approved_standard = deep.iloc[0:0].copy()
                approved_standard["final_execution_bucket"] = "APPROVED_STANDARD"
                approved_standard.to_csv(final_export_files[1], index=False)

                approved = deep.copy()
                approved["final_execution_bucket"] = "APPROVED_PREMIUM"
                approved.to_csv(final_export_files[2], index=False)

                empty = approved.iloc[0:0].copy()
                for path in final_export_files[3:6]:
                    empty.to_csv(path, index=False)

                pd.DataFrame(
                    [
                        {
                            "summary_scope": "overall",
                            "final_execution_bucket": pd.NA,
                            "production_governance_status": pd.NA,
                            "rows_total": len(deep),
                        },
                        {
                            "summary_scope": "by_final_execution_bucket",
                            "final_execution_bucket": "APPROVED_PREMIUM",
                            "production_governance_status": pd.NA,
                            "rows_total": len(approved),
                        },
                    ]
                ).to_csv(final_export_files[6], index=False)

            def fake_run_step(script_path: str) -> None:
                run_step_calls.append(script_path)
                processed_dir.mkdir(parents=True, exist_ok=True)

                if script_path == "scripts/select_core_candidates.py":
                    raw = read_current_raw()
                    shortlist = raw.assign(
                        shortlist_rank=range(1, len(raw) + 1),
                        shortlist_bucket="TOP_CORE",
                        selection_score=82.0,
                        market_primary="OVER_1_5",
                    )
                    shortlist.to_csv(processed_dir / "vsigma_core_shortlist.csv", index=False)
                    return

                if script_path == run_historical_labeling_pipeline.DEEP_ANALYSIS_STEP:
                    raw = read_current_raw()
                    deep = raw.assign(
                        shortlist_rank=range(1, len(raw) + 1),
                        shortlist_bucket="TOP_CORE",
                        analysis_label="TOP_CORE",
                        selection_score=82.0,
                        market_primary="OVER_1_5",
                        primary_odds_used=1.8,
                        primary_edge=0.08,
                        execution_verdict="TOP_CORE",
                        base_final_recommendation="BET",
                        final_recommendation="BET",
                        production_governance_status="APPROVED_BY_PROMOTED_RULE",
                    )
                    deep.to_csv(standard_deep_csv, index=False)
                    return

                if script_path == run_historical_labeling_pipeline.FINAL_EXECUTION_EXPORT_STEP:
                    write_final_exports()
                    return

                if script_path == run_historical_labeling_pipeline.FINAL_EXECUTION_EXPORT_VALIDATION_STEP:
                    report, errors = validate_final_execution_exports.validate_exports(processed_dir)
                    report.to_csv(
                        processed_dir / "vsigma_final_export_reconciliation_report.csv",
                        index=False,
                    )
                    if errors:
                        raise AssertionError(errors)
                    return

                if script_path == "scripts/refresh_finished_results_by_date.py":
                    pd.DataFrame([{"status": "OK"}]).to_csv(
                        processed_dir / "refresh_finished_results_by_date_report.csv",
                        index=False,
                    )
                    return

                if script_path == "scripts/label_market_results.py":
                    deep = pd.read_csv(standard_deep_csv)
                    labeled = deep.assign(
                        primary_result="WIN",
                        primary_profit_units=0.8,
                        actionable_flag=1,
                        actionable_result="WIN",
                        actionable_profit_units=0.8,
                    )
                    labeled.to_csv(standard_labeled_csv, index=False)
                    pd.DataFrame([{"graded_bets": len(labeled)}]).to_csv(
                        processed_dir / "vsigma_market_results_report.csv",
                        index=False,
                    )
                    return

                if script_path == "scripts/run_vsigma_backtest_calibration.py":
                    labeled = pd.read_csv(standard_labeled_csv)
                    labeled.assign(
                        market_result_norm=labeled["actionable_result"],
                        is_actionable=True,
                        profit_units_effective=labeled["actionable_profit_units"],
                        stake_units_effective=1.0,
                    ).to_csv(standard_backtest_source, index=False)
                    pd.DataFrame(
                        [
                            {
                                "rule": "selection_score >= 80",
                                "graded_bets": len(labeled),
                            }
                        ]
                    ).to_csv(standard_calibration_candidates, index=False)

            patchers = [
                patch.object(run_historical_labeling_pipeline, "RAW_MATCHES_CSV", raw_matches_csv),
                patch.object(run_historical_labeling_pipeline, "RAW_JSON_PATH", raw_json_path),
                patch.object(run_historical_labeling_pipeline, "PROCESSED_DIR", processed_dir),
                patch.object(run_historical_labeling_pipeline, "HISTORICAL_DIR", historical_dir),
                patch.object(run_historical_labeling_pipeline, "STANDARD_DEEP_CSV", standard_deep_csv),
                patch.object(run_historical_labeling_pipeline, "STANDARD_LABELED_CSV", standard_labeled_csv),
                patch.object(
                    run_historical_labeling_pipeline,
                    "STANDARD_BACKTEST_SOURCE",
                    standard_backtest_source,
                ),
                patch.object(
                    run_historical_labeling_pipeline,
                    "STANDARD_CALIBRATION_CANDIDATES",
                    standard_calibration_candidates,
                ),
                patch.object(
                    run_historical_labeling_pipeline,
                    "FINAL_EXECUTION_EXPORT_FILES",
                    final_export_files,
                ),
                patch.object(run_historical_labeling_pipeline, "SNAPSHOT_FILES", snapshot_files),
                patch.object(
                    run_historical_labeling_pipeline,
                    "PER_DATE_GENERATED_FILES",
                    per_date_generated_files,
                ),
                patch.object(run_historical_labeling_pipeline, "APIFootballClient", object),
                patch.object(
                    run_historical_labeling_pipeline,
                    "fetch_date_matches",
                    side_effect=fetch_without_api,
                ),
                patch.object(
                    run_historical_labeling_pipeline,
                    "run_step",
                    side_effect=fake_run_step,
                ),
                patch.object(
                    sys,
                    "argv",
                    [
                        "run_historical_labeling_pipeline.py",
                        "--dates",
                        "2026-05-01",
                        "2026-05-02",
                        "--min-added-graded",
                        "1",
                        "--min-total-graded",
                        "2",
                    ],
                ),
            ]

            with ExitStack() as stack:
                for patcher in patchers:
                    stack.enter_context(patcher)
                run_historical_labeling_pipeline.main()

            combined_deep = pd.read_csv(standard_deep_csv)
            combined_labeled = pd.read_csv(standard_labeled_csv)
            batch_report = pd.read_csv(processed_dir / "historical_labeling_batch_report.csv")
            final_summary = pd.read_csv(processed_dir / "vsigma_final_governance_summary.csv")

            self.assertEqual(combined_deep["fixture_id"].tolist(), [9001, 9002])
            self.assertEqual(combined_labeled["fixture_id"].tolist(), [9001, 9002])
            self.assertEqual(
                combined_deep["historical_batch_date"].tolist(),
                ["2026-05-01", "2026-05-02"],
            )
            self.assertEqual(
                batch_report[["date", "status", "graded_bets"]].to_dict("records"),
                [
                    {"date": "2026-05-01", "status": "OK", "graded_bets": 1},
                    {"date": "2026-05-02", "status": "OK", "graded_bets": 1},
                ],
            )
            self.assertEqual(int(batch_report.loc[0, "graded_before_batch"]), 0)
            self.assertEqual(int(batch_report.loc[0, "graded_after_batch"]), 2)
            self.assertTrue(standard_backtest_source.exists())
            self.assertTrue(standard_calibration_candidates.exists())
            self.assertEqual(int(final_summary.loc[0, "rows_total"]), 2)

            for match_date, fixture_id in [("2026-05-01", 9001), ("2026-05-02", 9002)]:
                snapshot_deep = pd.read_csv(
                    historical_dir / match_date / "vsigma_deep_analysis_candidates.csv"
                )
                snapshot_labeled = pd.read_csv(
                    historical_dir / match_date / "vsigma_market_results_labeled.csv"
                )
                snapshot_summary = pd.read_csv(
                    historical_dir / match_date / "vsigma_final_governance_summary.csv"
                )
                self.assertEqual(snapshot_deep["fixture_id"].tolist(), [fixture_id])
                self.assertEqual(snapshot_labeled["fixture_id"].tolist(), [fixture_id])
                self.assertEqual(int(snapshot_summary.loc[0, "rows_total"]), 1)

            final_export_call_indexes = [
                index
                for index, script_path in enumerate(run_step_calls)
                if script_path == run_historical_labeling_pipeline.FINAL_EXECUTION_EXPORT_STEP
            ]
            validation_call_indexes = [
                index
                for index, script_path in enumerate(run_step_calls)
                if script_path == run_historical_labeling_pipeline.FINAL_EXECUTION_EXPORT_VALIDATION_STEP
            ]
            calibration_index = run_step_calls.index("scripts/run_vsigma_backtest_calibration.py")
            historical_execution_index = run_step_calls.index(
                run_historical_labeling_pipeline.HISTORICAL_EXECUTION_SHORTLIST_BACKTEST_STEP
            )
            self.assertEqual(len(final_export_call_indexes), 3)
            self.assertEqual(len(validation_call_indexes), 3)
            self.assertLess(final_export_call_indexes[-1], calibration_index)
            self.assertLess(validation_call_indexes[-1], calibration_index)
            self.assertEqual(historical_execution_index, calibration_index + 1)
            self.assertEqual(
                validation_call_indexes,
                [index + 1 for index in final_export_call_indexes],
            )
            self.assertEqual(
                [
                    run_step_calls[index - 1]
                    for index in final_export_call_indexes[:2]
                ],
                [
                    run_historical_labeling_pipeline.DEEP_ANALYSIS_STEP,
                    run_historical_labeling_pipeline.DEEP_ANALYSIS_STEP,
                ],
            )

    def test_historical_sample_validation_allows_zero_required_added_graded(self) -> None:
        run_historical_labeling_pipeline.validate_expanded_sample(
            before_graded=249,
            after_graded=249,
            min_added_graded=0,
            min_total_graded=249,
        )

    def test_historical_sample_validation_keeps_default_added_graded_requirement(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "did not expand the graded sample"):
            run_historical_labeling_pipeline.validate_expanded_sample(
                before_graded=249,
                after_graded=249,
                min_added_graded=1,
                min_total_graded=249,
            )

    def test_daily_freshness_validator_catches_stale_date_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            pd.DataFrame(
                [{"date": "2026-05-13", "fixture_id": 1, "market_primary": "OVER_1_5"}]
            ).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)

            report = validate_daily_output_freshness.validate_freshness(
                processed_dir,
                "2026-05-14",
                processed_dir / "today" / "2026-05-14",
            )

            row = report[report["file_name"].eq("vsigma_today_competition_top.csv")].iloc[0]
            self.assertEqual(row["status"], "WARNING_STALE_GLOBAL_FILE")

    def test_daily_freshness_validator_accepts_empty_no_bet_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            for filename in [
                "vsigma_today_competition_shortlist.csv",
                "vsigma_today_competition_top.csv",
                "vsigma_today_candidate_v2_competition_top.csv",
            ]:
                pd.DataFrame(columns=["date", "fixture_id", "market_primary"]).to_csv(processed_dir / filename, index=False)

            report = validate_daily_output_freshness.validate_freshness(
                processed_dir,
                "2026-05-14",
                processed_dir / "today" / "2026-05-14",
            )
            statuses = set(report.loc[report["file_name"].str.contains("competition_top|competition_shortlist"), "status"])
            self.assertEqual(statuses, {"EMPTY_OK_NO_BET"})

    def test_competition_scoreboard_updates_date_without_duplicate_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            scoreboard_path = Path(tmp) / "notes" / "competition_scoreboard.md"
            pd.DataFrame(columns=["date", "fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_competition_top.csv",
                index=False,
            )

            update_competition_scoreboard.update_scoreboard(processed_dir, "2026-05-14", scoreboard_path)
            update_competition_scoreboard.update_scoreboard(processed_dir, "2026-05-14", scoreboard_path)

            text = scoreboard_path.read_text(encoding="utf-8")
            self.assertEqual(text.count("VSIGMA_SCOREBOARD_START 2026-05-14"), 1)
            self.assertIn("NO_BET_DAY", text)

    def test_daily_master_report_is_generated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            snapshot_dir = processed_dir / "today" / "2026-05-14"
            snapshot_dir.mkdir(parents=True)
            pd.DataFrame(columns=["date", "fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_competition_top.csv",
                index=False,
            )

            path = build_daily_competition_master_report.build_master_report(
                processed_dir,
                "2026-05-14",
                snapshot_dir,
            )

            text = path.read_text(encoding="utf-8")
            self.assertIn("Official Baseline Top Picks", text)
            self.assertIn("NO_BET", text)
            self.assertIn("PRE_LOCK_ACTIVE", text)

    def test_candidate_isolation_confirms_candidate_files_do_not_overwrite_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            snapshot_dir = processed_dir / "today" / "2026-05-14"
            snapshot_dir.mkdir(parents=True)
            for filename in [
                "vsigma_today_competition_shortlist.csv",
                "vsigma_today_competition_top.csv",
                "vsigma_today_candidate_v2_competition_top.csv",
                "vsigma_today_candidate_v4_competition_top.csv",
                "vsigma_today_candidate_v5_competition_top.csv",
                "vsigma_today_candidate_v6_competition_top.csv",
            ]:
                pd.DataFrame(columns=["date", "fixture_id", "market_primary"]).to_csv(processed_dir / filename, index=False)
                (snapshot_dir / filename).write_text((processed_dir / filename).read_text(encoding="utf-8"), encoding="utf-8")
            (processed_dir / "vsigma_today_competition_report.txt").write_text("baseline\n", encoding="utf-8")

            report = validate_candidate_isolation.validate_isolation(processed_dir, "2026-05-14", snapshot_dir)

            self.assertNotIn("ERROR_CANDIDATE_OVERWRITE_RISK", set(report["status"]))

    def test_candidate_empty_outputs_do_not_crash_master_report_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            snapshot_dir = processed_dir / "today" / "2026-05-14"
            snapshot_dir.mkdir(parents=True)
            for filename in [
                "vsigma_today_competition_top.csv",
                "vsigma_today_candidate_v2_competition_top.csv",
                "vsigma_today_candidate_v4_competition_top.csv",
                "vsigma_today_candidate_v5_competition_top.csv",
                "vsigma_today_candidate_v6_competition_top.csv",
            ]:
                pd.DataFrame(columns=["date", "fixture_id", "market_primary"]).to_csv(processed_dir / filename, index=False)

            path = build_daily_competition_master_report.build_master_report(processed_dir, "2026-05-14", snapshot_dir)

            self.assertTrue(path.exists())
            self.assertIn("Candidate v6: NO_BET", path.read_text(encoding="utf-8"))

    def test_post_results_scoreboard_update_handles_settled_and_pending_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            scoreboard_path = Path(tmp) / "notes" / "competition_scoreboard.md"
            pd.DataFrame(columns=["date", "fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_competition_top.csv",
                index=False,
            )
            pd.DataFrame([{"date": "2026-05-14", "fixture_id": 2, "market_primary": "OVER_1_5"}]).to_csv(
                processed_dir / "vsigma_today_candidate_v2_competition_top.csv",
                index=False,
            )
            pd.DataFrame(
                [{"pick_count": 1, "wins": 1, "losses": 0, "profit_units": 0.42, "roi_percent": 42.0}]
            ).to_csv(processed_dir / "vsigma_today_candidate_v2_results_summary.csv", index=False)
            pd.DataFrame([{"ledger_result_status": "PENDING"}]).to_csv(
                processed_dir / "vsigma_today_candidate_v2_results_ledger.csv",
                index=False,
            )

            update_competition_scoreboard.update_scoreboard(processed_dir, "2026-05-14", scoreboard_path)

            text = scoreboard_path.read_text(encoding="utf-8")
            self.assertIn("CANDIDATE_V2", text)
            self.assertIn("0.42", text)
            self.assertIn("pending", text)

    def test_daily_metadata_columns_exist_in_key_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            for filename in [
                "vsigma_today_competition_top.csv",
                "vsigma_today_candidate_v2_competition_top.csv",
                "vsigma_today_baseline_vs_candidate_v2.csv",
            ]:
                pd.DataFrame([{"date": "2026-05-14", "fixture_id": 1, "market_primary": "OVER_1_5"}]).to_csv(
                    processed_dir / filename,
                    index=False,
                )

            daily_hardening.stamp_daily_outputs(processed_dir, "2026-05-14", run_id="test-run")

            stamped = pd.read_csv(processed_dir / "vsigma_today_competition_top.csv")
            for column in daily_hardening.METADATA_COLUMNS:
                self.assertIn(column, stamped.columns)
            self.assertEqual(stamped.loc[0, "candidate_version"], "OFFICIAL_BASELINE")

    def test_prelock_outputs_are_generated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {
                        "date": "2026-05-14",
                        "fixture_id": 1,
                        "league": "League A",
                        "home_team": "A",
                        "away_team": "B",
                        "market_primary": "OVER_1_5",
                        "lineup_minutes_to_kickoff": 30,
                    }
                ]
            ).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)

            paths = run_today_prelock_pipeline.build_prelock_outputs(
                processed_dir,
                today_dir,
                "2026-05-14",
                "Atlantic/Canary",
                90,
                refresh=False,
            )

            self.assertTrue(paths["prelock_top"].exists())
            self.assertTrue(paths["prelock_comparison"].exists())
            self.assertTrue(paths["prelock_report"].exists())
            self.assertTrue((today_dir / "2026-05-14" / "vsigma_today_prelock_comparison.csv").exists())

    def test_prelock_missing_data_does_not_hard_veto(self) -> None:
        row = pd.Series({"market_primary": "OVER_1_5", "lineup_minutes_to_kickoff": 20})

        decision = run_today_prelock_pipeline.classify_prelock_decision(row, 90)

        self.assertEqual(decision["prelock_decision"], "PRELOCK_NOT_AVAILABLE")

    def test_prelock_morning_pick_can_be_confirmed(self) -> None:
        row = pd.Series(
            {
                "market_primary": "OVER_1_5",
                "lineup_minutes_to_kickoff": 20,
                "home_lineup_known_starters_count": 11,
                "away_lineup_known_starters_count": 11,
                "odds_market_support_count": 4,
            }
        )

        decision = run_today_prelock_pipeline.classify_prelock_decision(row, 90)

        self.assertEqual(decision["prelock_decision"], "PRELOCK_CONFIRMED")

    def test_prelock_explicit_contradiction_can_remove_pick(self) -> None:
        row = pd.Series(
            {
                "market_primary": "OVER_1_5",
                "lineup_minutes_to_kickoff": 20,
                "odds_market_translation_hint": "UNDER",
                "odds_over15_support_flag": "WEAK",
                "availability_attack_penalty": 2.5,
            }
        )

        decision = run_today_prelock_pipeline.classify_prelock_decision(row, 90)

        self.assertEqual(decision["prelock_decision"], "PRELOCK_REMOVED")

    def test_extended_historical_outputs_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline_dir = root / "historical" / "2026-05-01"
            v2_dir = root / "recent_lab" / "2026-05-01"
            output_dir = root / "out"
            baseline_dir.mkdir(parents=True)
            v2_dir.mkdir(parents=True)
            pd.DataFrame([{"fixture_id": 1}]).to_csv(baseline_dir / "matches.csv", index=False)
            pd.DataFrame([{"fixture_id": 1}]).to_csv(baseline_dir / "vsigma_execution_shortlist_historical.csv", index=False)
            pd.DataFrame([{"fixture_id": 1}]).to_csv(v2_dir / "vsigma_execution_shortlist_historical.csv", index=False)

            fake_ledger = pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "comparison_mode": "BASELINE_OFFICIAL",
                        "ledger_result_status": "RESULT_AVAILABLE",
                        "actionable_result": "WIN",
                        "actionable_profit_units": 0.5,
                        "market_primary": "OVER_1_5",
                        "league": "League A",
                        "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
                    }
                ]
            )

            with patch.object(run_extended_historical_evaluation, "BASELINE_HISTORICAL_DIR", root / "historical"), patch.object(
                run_extended_historical_evaluation,
                "RECENT_LAB_HISTORICAL_DIR",
                root / "recent_lab",
            ), patch.object(run_extended_historical_evaluation, "build_mode_ledgers", return_value=[fake_ledger]):
                paths = run_extended_historical_evaluation.evaluate_range(
                    "2026-05-01",
                    "2026-05-01",
                    output_dir=output_dir,
                )

            for path in paths.values():
                self.assertTrue(path.exists())
            summary = pd.read_csv(paths["summary"])
            self.assertEqual(int(summary.loc[0, "settled_rows"]), 1)

    def test_drift_monitor_detects_repeated_failure_pattern(self) -> None:
        rows = pd.DataFrame(
            [
                {
                    "comparison_mode": "BASELINE_OFFICIAL",
                    "market_primary": "OVER_1_5",
                    "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
                    "ledger_result_status": "RESULT_AVAILABLE",
                    "actionable_result": "LOSS",
                    "actionable_profit_units": -1.0,
                }
                for _ in range(6)
            ]
        )

        summary = build_vsigma_drift_monitor.build_drift_summary(rows, min_sample=5)
        status = summary.loc[summary["pattern"].eq("OVER_1_5 + FAILURE_MODE_LOW_CONVERSION"), "drift_status"].iloc[0]

        self.assertEqual(status, "ACTIVE_DRIFT")

    def test_drift_monitor_returns_sample_too_small_when_appropriate(self) -> None:
        rows = pd.DataFrame(
            [
                {
                    "comparison_mode": "BASELINE_OFFICIAL",
                    "market_primary": "OVER_1_5",
                    "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
                    "ledger_result_status": "RESULT_AVAILABLE",
                    "actionable_result": "LOSS",
                    "actionable_profit_units": -1.0,
                }
            ]
        )

        summary = build_vsigma_drift_monitor.build_drift_summary(rows, min_sample=5)
        status = summary.loc[summary["pattern"].eq("OVER_1_5 + FAILURE_MODE_LOW_CONVERSION"), "drift_status"].iloc[0]

        self.assertEqual(status, "SAMPLE_TOO_SMALL")

    def test_daily_master_report_includes_prelock_and_drift_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            snapshot_dir = processed_dir / "today" / "2026-05-14"
            snapshot_dir.mkdir(parents=True)
            pd.DataFrame(columns=["date", "fixture_id", "market_primary"]).to_csv(
                processed_dir / "vsigma_today_competition_top.csv",
                index=False,
            )
            pd.DataFrame([{"fixture_id": 1, "prelock_status": "IN_PRELOCK_WINDOW", "prelock_decision": "PRELOCK_CONFIRMED"}]).to_csv(
                processed_dir / "vsigma_today_prelock_comparison.csv",
                index=False,
            )
            pd.DataFrame([{"pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", "settled_rows": 5, "drift_status": "WATCH_PATTERN"}]).to_csv(
                processed_dir / "vsigma_drift_monitor_summary.csv",
                index=False,
            )
            odds_dir = processed_dir / "odds_snapshots"
            odds_dir.mkdir()
            pd.DataFrame(
                [
                    {
                        "target_date": "2026-05-14",
                        "fixture_id": 1,
                        "market_primary": "OVER_1_5",
                        "experiment_id": "OFFICIAL_BASELINE",
                        "pre_price": 1.4,
                        "prelock_price": 1.35,
                        "close_proxy_price": 1.35,
                        "clv_direction": "CLV_POSITIVE",
                    }
                ]
            ).to_csv(odds_dir / "vsigma_clv_summary.csv", index=False)
            pd.DataFrame(
                [
                    {
                        "market_family": "OVER_1_5",
                        "failure_mode": "LOW_CONVERSION",
                        "recommendation": "SAMPLE_TOO_SMALL",
                    }
                ]
            ).to_csv(odds_dir / "vsigma_candidate_v7_calibration_advice.csv", index=False)

            path = build_daily_competition_master_report.build_master_report(processed_dir, "2026-05-14", snapshot_dir)

            text = path.read_text(encoding="utf-8")
            self.assertIn("## Pre-Lock Status", text)
            self.assertIn("## Drift Monitor Status", text)
            self.assertIn("## Baseline vs Candidate Trend", text)
            self.assertIn("## Odds Snapshot / CLV Calibration", text)
            self.assertIn("SAMPLE_TOO_SMALL", text)

    def test_prelock_does_not_change_official_baseline_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            baseline_path = processed_dir / "vsigma_today_competition_top.csv"
            pd.DataFrame(
                [
                    {
                        "date": "2026-05-14",
                        "fixture_id": 1,
                        "home_team": "A",
                        "away_team": "B",
                        "market_primary": "OVER_1_5",
                        "lineup_minutes_to_kickoff": 20,
                    }
                ]
            ).to_csv(baseline_path, index=False)
            before = baseline_path.read_text(encoding="utf-8")

            run_today_prelock_pipeline.build_prelock_outputs(
                processed_dir,
                today_dir,
                "2026-05-14",
                "Atlantic/Canary",
                90,
                refresh=False,
            )

            self.assertEqual(baseline_path.read_text(encoding="utf-8"), before)

    def test_experiment_registry_loads_official_baseline(self) -> None:
        registry = update_immutable_daily_ledger.load_experiment_registry()

        self.assertIn("OFFICIAL_BASELINE", registry)
        self.assertIn("CANDIDATE_V7_PRICE_DISCIPLINE", registry)
        self.assertTrue(registry["OFFICIAL_BASELINE"]["allowed_to_select_officially"])
        self.assertFalse(registry["CANDIDATE_V7_PRICE_DISCIPLINE"]["allowed_to_select_officially"])
        self.assertEqual(registry["OFFICIAL_BASELINE"]["status"], "OFFICIAL")

    def test_price_discipline_config_loads(self) -> None:
        config = apply_price_discipline_guard.load_price_discipline_config()

        self.assertIn("rules", config)
        self.assertTrue(any(rule["market_family"] == "OVER_1_5" for rule in config["rules"]))

    def test_price_discipline_over15_low_conversion_thin_edge_is_secondary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "config.json"
            config_path.write_text(apply_price_discipline_guard.CONFIG_PATH.read_text(encoding="utf-8"), encoding="utf-8")
            drift_path = root / "drift.csv"
            pd.DataFrame([{"pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", "drift_status": "NO_DRIFT"}]).to_csv(drift_path, index=False)
            df = pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "market_primary": "OVER_1_5",
                        "primary_odds_used": 1.4,
                        "primary_edge": 0.04,
                        "competition_calibrated_prob": 0.8,
                        "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
                    }
                ]
            )

            out = apply_price_discipline_guard.apply_price_discipline_guard(df, config_path=config_path, drift_path=drift_path, prelock_path=root / "missing.csv")

            self.assertEqual(out.iloc[0]["price_discipline_decision"], "PRICE_THIN_SECONDARY_ONLY")
            self.assertEqual(int(out.iloc[0]["price_discipline_execution_allowed_flag"]), 0)

    def test_price_discipline_over15_low_conversion_strong_edge_survives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            drift_path = root / "drift.csv"
            pd.DataFrame([{"pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", "drift_status": "NO_DRIFT"}]).to_csv(drift_path, index=False)
            df = pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "market_primary": "OVER_1_5",
                        "primary_odds_used": 1.5,
                        "primary_edge": 0.18,
                        "competition_calibrated_prob": 0.82,
                        "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
                    }
                ]
            )

            out = apply_price_discipline_guard.apply_price_discipline_guard(df, drift_path=drift_path, prelock_path=root / "missing.csv")

            self.assertEqual(out.iloc[0]["price_discipline_decision"], "PRICE_OK")
            self.assertEqual(int(out.iloc[0]["price_discipline_execution_allowed_flag"]), 1)

    def test_price_discipline_watch_pattern_increases_required_edge(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            no_drift = root / "no.csv"
            watch = root / "watch.csv"
            pd.DataFrame([{"pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", "drift_status": "NO_DRIFT"}]).to_csv(no_drift, index=False)
            pd.DataFrame([{"pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", "drift_status": "WATCH_PATTERN"}]).to_csv(watch, index=False)
            df = pd.DataFrame([{"fixture_id": 1, "market_primary": "OVER_1_5", "primary_edge": 0.15, "competition_calibrated_prob": 0.8, "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION"}])

            base = apply_price_discipline_guard.apply_price_discipline_guard(df, drift_path=no_drift, prelock_path=root / "missing.csv")
            guarded = apply_price_discipline_guard.apply_price_discipline_guard(df, drift_path=watch, prelock_path=root / "missing.csv")

            self.assertGreater(float(guarded.iloc[0]["price_discipline_min_edge_required"]), float(base.iloc[0]["price_discipline_min_edge_required"]))

    def test_price_discipline_missing_drift_output_does_not_crash(self) -> None:
        df = pd.DataFrame([{"fixture_id": 1, "market_primary": "OVER_1_5", "primary_edge": 0.2, "competition_calibrated_prob": 0.85}])

        out = apply_price_discipline_guard.apply_price_discipline_guard(df, drift_path=Path("missing_drift.csv"), prelock_path=Path("missing_prelock.csv"))

        self.assertEqual(out.iloc[0]["price_discipline_drift_status"], "UNKNOWN")

    def test_price_discipline_clv_unavailable_is_neutral(self) -> None:
        df = pd.DataFrame([{"fixture_id": 1, "market_primary": "OVER_1_5", "primary_edge": 0.2, "competition_calibrated_prob": 0.85}])

        out = apply_price_discipline_guard.apply_price_discipline_guard(df, drift_path=Path("missing_drift.csv"), prelock_path=Path("missing_prelock.csv"))

        self.assertEqual(out.iloc[0]["clv_direction"], "CLV_UNAVAILABLE")
        self.assertEqual(int(out.iloc[0]["clv_available_flag"]), 0)

    def test_candidate_v7_outputs_are_separate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            baseline = pd.DataFrame([{"fixture_id": 1, "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5"}])
            v2 = pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "home_team": "A",
                        "away_team": "B",
                        "market_primary": "OVER_1_5",
                        "primary_edge": 0.2,
                        "primary_model_prob": 0.85,
                        "competition_calibrated_prob": 0.85,
                        "accuracy_mode_eligible_flag": 1,
                        "accuracy_confidence_score": 120,
                        "execution_shortlist_source": "PREMIUM_CORE",
                        "execution_rank": 1,
                    }
                ]
            )
            baseline_path = processed_dir / "vsigma_today_competition_top.csv"
            baseline.to_csv(baseline_path, index=False)
            v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_shortlist.csv", index=False)
            v2.to_csv(processed_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
            before = baseline_path.read_text(encoding="utf-8")

            paths = run_today_shadow_candidate_v7.build_candidate_v7_outputs(processed_dir, today_dir, "2026-05-14")

            self.assertTrue(paths["candidate_v7_top"].exists())
            self.assertEqual(baseline_path.read_text(encoding="utf-8"), before)

    def test_candidate_v7_post_results_handles_empty_picks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            pd.DataFrame(columns=["fixture_id", "market_primary"]).to_csv(processed_dir / "vsigma_today_candidate_v7_competition_top.csv", index=False)

            paths = run_today_shadow_candidate_v7_post_results.build_candidate_v7_post_results(processed_dir, today_dir, "2026-05-14")

            self.assertTrue(paths["candidate_v7_results_ledger"].exists())
            summary = pd.read_csv(paths["candidate_v7_results_summary"])
            self.assertEqual(int(summary.iloc[0]["pick_count"]), 0)

    def test_odds_snapshot_file_created_with_required_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            processed_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "league": "League A",
                        "home_team": "A",
                        "away_team": "B",
                        "market_primary": "OVER_1_5",
                        "market_alt": "OVER_2_5",
                        "primary_odds_used": 1.4,
                        "primary_implied_prob": 0.714286,
                        "odds_bookmaker_support_count": 5,
                    }
                ]
            ).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)

            paths = capture_odds_snapshots.capture_odds_snapshots(processed_dir, odds_dir, "2026-05-14", "PRE")

            snapshots = pd.read_csv(paths["snapshots_csv"])
            for column in capture_odds_snapshots.SNAPSHOT_COLUMNS:
                self.assertIn(column, snapshots.columns)
            self.assertEqual(len(snapshots), 1)

    def test_odds_snapshot_duplicate_handling_is_idempotent_by_snapshot_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            processed_dir.mkdir(parents=True)
            pd.DataFrame([{"fixture_id": 1, "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5", "primary_odds_used": 1.4}]).to_csv(
                processed_dir / "vsigma_today_competition_top.csv",
                index=False,
            )

            capture_odds_snapshots.capture_odds_snapshots(processed_dir, odds_dir, "2026-05-14", "PRE")
            capture_odds_snapshots.capture_odds_snapshots(processed_dir, odds_dir, "2026-05-14", "PRE")

            snapshots = pd.read_csv(odds_dir / "vsigma_odds_snapshots.csv")
            self.assertEqual(len(snapshots), 1)

    def test_odds_snapshot_excludes_source_rows_from_wrong_requested_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            processed_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {"date": "2026-05-14", "fixture_id": 1, "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5", "primary_odds_used": 1.4},
                    {"date": "2026-05-15", "fixture_id": 2, "home_team": "C", "away_team": "D", "market_primary": "OVER_1_5", "primary_odds_used": 1.5},
                ]
            ).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)

            paths = capture_odds_snapshots.capture_odds_snapshots(processed_dir, odds_dir, "2026-05-14", "PRE")

            snapshots = pd.read_csv(paths["snapshots_csv"])
            self.assertEqual(snapshots["fixture_id"].astype(str).tolist(), ["1"])
            self.assertEqual(snapshots["target_date"].astype(str).unique().tolist(), ["2026-05-14"])

    def test_odds_snapshot_does_not_change_official_baseline_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            processed_dir.mkdir(parents=True)
            baseline_path = processed_dir / "vsigma_today_competition_top.csv"
            pd.DataFrame(
                [{"date": "2026-05-14", "fixture_id": 1, "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5", "primary_odds_used": 1.4}]
            ).to_csv(baseline_path, index=False)
            before = baseline_path.read_text(encoding="utf-8")

            capture_odds_snapshots.capture_odds_snapshots(processed_dir, odds_dir, "2026-05-14", "PRE")

            self.assertEqual(baseline_path.read_text(encoding="utf-8"), before)

    def test_rebuild_odds_snapshots_archives_existing_target_date_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed_dir = root / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            today_dir = processed_dir / "today"
            odds_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {"snapshot_id": "target-pre", "target_date": "2026-05-14", "generated_at": "2026-05-14T08:00:00+00:00", "pipeline_stage": "PRE", "fixture_id": 1, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "source_candidate_version": "OFFICIAL_BASELINE", "selected_price": 1.4},
                    {"snapshot_id": "other-pre", "target_date": "2026-05-13", "generated_at": "2026-05-13T08:00:00+00:00", "pipeline_stage": "PRE", "fixture_id": 2, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "source_candidate_version": "OFFICIAL_BASELINE", "selected_price": 1.5},
                ]
            ).to_csv(odds_dir / "vsigma_odds_snapshots.csv", index=False)

            result = rebuild_odds_snapshots_for_date.rebuild_odds_snapshots_for_date(
                "2026-05-14",
                processed_dir=processed_dir,
                odds_dir=odds_dir,
                today_dir=today_dir,
                generated_at="2026-05-15T08:00:00+00:00",
            )

            archive = Path(result["archive_path"])
            self.assertTrue(archive.exists())
            archived = pd.read_csv(archive)
            self.assertEqual(archived["snapshot_id"].astype(str).tolist(), ["target-pre"])

    def test_rebuild_odds_snapshots_preserves_other_dates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed_dir = root / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            today_dir = processed_dir / "today"
            odds_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {"snapshot_id": "target-pre", "target_date": "2026-05-14", "pipeline_stage": "PRE", "fixture_id": 1, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "selected_price": 1.4},
                    {"snapshot_id": "other-pre", "target_date": "2026-05-13", "pipeline_stage": "PRE", "fixture_id": 2, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "selected_price": 1.5},
                ]
            ).to_csv(odds_dir / "vsigma_odds_snapshots.csv", index=False)

            rebuild_odds_snapshots_for_date.rebuild_odds_snapshots_for_date(
                "2026-05-14",
                processed_dir=processed_dir,
                odds_dir=odds_dir,
                today_dir=today_dir,
                generated_at="2026-05-15T08:00:00+00:00",
            )

            rebuilt = pd.read_csv(odds_dir / "vsigma_odds_snapshots.csv")
            self.assertIn("2026-05-13", set(rebuilt["target_date"].astype(str)))
            self.assertIn("other-pre", set(rebuilt["snapshot_id"].astype(str)))

    def test_rebuild_odds_snapshots_marks_backfilled_rows_audit_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed_dir = root / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            today_dir = processed_dir / "today"
            day_dir = today_dir / "2026-05-14"
            odds_dir.mkdir(parents=True)
            day_dir.mkdir(parents=True)
            pd.DataFrame(columns=["snapshot_id", "target_date"]).to_csv(odds_dir / "vsigma_odds_snapshots.csv", index=False)
            pd.DataFrame(
                [{"date": "2026-05-14", "fixture_id": 1, "league": "League A", "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5", "primary_odds_used": 1.4}]
            ).to_csv(day_dir / "vsigma_today_prelock_comparison.csv", index=False)

            result = rebuild_odds_snapshots_for_date.rebuild_odds_snapshots_for_date(
                "2026-05-14",
                processed_dir=processed_dir,
                odds_dir=odds_dir,
                today_dir=today_dir,
                generated_at="2026-05-15T08:00:00+00:00",
            )

            rebuilt = pd.read_csv(odds_dir / "vsigma_odds_snapshots.csv")
            self.assertGreater(int(result["audit_only_count"]), 0)
            self.assertEqual(set(rebuilt["snapshot_rebuild_mode"]), {"BACKFILLED_FROM_AVAILABLE_OUTPUTS"})
            self.assertEqual(set(rebuilt["clv_usable_for_threshold_calibration_flag"].astype(int)), {0})
            self.assertEqual(set(rebuilt["true_pre_snapshot_available_flag"].astype(int)), {0})

    def test_rebuild_odds_snapshots_dry_run_does_not_modify_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed_dir = root / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            today_dir = processed_dir / "today"
            odds_dir.mkdir(parents=True)
            snapshot_path = odds_dir / "vsigma_odds_snapshots.csv"
            pd.DataFrame(
                [{"snapshot_id": "target-pre", "target_date": "2026-05-14", "pipeline_stage": "PRE", "fixture_id": 1, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "selected_price": 1.4}]
            ).to_csv(snapshot_path, index=False)
            before = snapshot_path.read_text(encoding="utf-8")

            result = rebuild_odds_snapshots_for_date.rebuild_odds_snapshots_for_date(
                "2026-05-14",
                dry_run=True,
                processed_dir=processed_dir,
                odds_dir=odds_dir,
                today_dir=today_dir,
                generated_at="2026-05-15T08:00:00+00:00",
            )

            self.assertEqual(snapshot_path.read_text(encoding="utf-8"), before)
            self.assertFalse(Path(result["archive_path"]).exists())

    def test_rebuild_odds_snapshots_does_not_change_official_baseline_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed_dir = root / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            today_dir = processed_dir / "today"
            day_dir = today_dir / "2026-05-14"
            odds_dir.mkdir(parents=True)
            day_dir.mkdir(parents=True)
            pd.DataFrame(columns=["snapshot_id", "target_date"]).to_csv(odds_dir / "vsigma_odds_snapshots.csv", index=False)
            baseline_path = day_dir / "vsigma_today_competition_top.csv"
            pd.DataFrame(
                [{"date": "2026-05-14", "fixture_id": 1, "league": "League A", "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5", "primary_odds_used": 1.4}]
            ).to_csv(baseline_path, index=False)
            before = baseline_path.read_text(encoding="utf-8")

            rebuild_odds_snapshots_for_date.rebuild_odds_snapshots_for_date(
                "2026-05-14",
                processed_dir=processed_dir,
                odds_dir=odds_dir,
                today_dir=today_dir,
                generated_at="2026-05-15T08:00:00+00:00",
            )

            self.assertEqual(baseline_path.read_text(encoding="utf-8"), before)

    def test_clv_report_uses_requested_target_date_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            odds_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {"snapshot_id": "old", "target_date": "2026-05-09", "generated_at": "2026-05-14T08:00:00+00:00", "pipeline_stage": "POST", "fixture_id": 9, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "selected_price": 1.5},
                    {"snapshot_id": "pre", "target_date": "2026-05-14", "generated_at": "2026-05-14T08:00:00+00:00", "pipeline_stage": "PRE", "fixture_id": 14, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "selected_price": 1.4},
                    {"snapshot_id": "close", "target_date": "2026-05-14", "generated_at": "2026-05-14T10:00:00+00:00", "pipeline_stage": "CLOSE_PROXY", "fixture_id": 14, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "selected_price": 1.35},
                ]
            ).to_csv(odds_dir / "vsigma_odds_snapshots.csv", index=False)

            paths = build_clv_calibration_report.build_clv_calibration_report(processed_dir, odds_dir, "2026-05-14")

            summary = pd.read_csv(paths["summary"])
            self.assertEqual(summary["target_date"].astype(str).unique().tolist(), ["2026-05-14"])
            self.assertEqual(summary["fixture_id"].astype(str).tolist(), ["14"])
            self.assertIn("- Target date: 2026-05-14", paths["report"].read_text(encoding="utf-8"))

    def test_clv_report_does_not_mix_target_dates_and_reports_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            odds_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {"snapshot_id": "mismatch", "target_date": "2026-05-09", "generated_at": "2026-05-14T08:00:00+00:00", "pipeline_stage": "POST", "fixture_id": 9, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "selected_price": 1.5},
                    {"snapshot_id": "match", "target_date": "2026-05-14", "generated_at": "2026-05-14T08:00:00+00:00", "pipeline_stage": "PRE", "fixture_id": 14, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "selected_price": 1.4},
                ]
            ).to_csv(odds_dir / "vsigma_odds_snapshots.csv", index=False)

            paths = build_clv_calibration_report.build_clv_calibration_report(processed_dir, odds_dir, "2026-05-14")

            report_text = paths["report"].read_text(encoding="utf-8")
            self.assertIn("CLV_DATE_MISMATCH", report_text)
            self.assertIn("2026-05-09", report_text)
            self.assertNotIn("| 2026-05-09 |", report_text)

    def test_clv_report_handles_missing_prelock_gracefully(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            odds_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {
                        "snapshot_id": "a",
                        "target_date": "2026-05-14",
                        "generated_at": "2026-05-14T08:00:00+00:00",
                        "pipeline_stage": "PRE",
                        "fixture_id": 1,
                        "market_primary": "OVER_1_5",
                        "experiment_id": "OFFICIAL_BASELINE",
                        "source_candidate_version": "OFFICIAL_BASELINE",
                        "selected_price": 1.4,
                    }
                ]
            ).to_csv(odds_dir / "vsigma_odds_snapshots.csv", index=False)

            paths = build_clv_calibration_report.build_clv_calibration_report(processed_dir, odds_dir, "2026-05-14")

            summary = pd.read_csv(paths["summary"])
            self.assertEqual(summary.iloc[0]["clv_direction"], "CLV_UNAVAILABLE")

    def test_clv_report_missing_pre_snapshot_uses_insufficient_tracking_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            odds_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {
                        "snapshot_id": "close",
                        "target_date": "2026-05-14",
                        "generated_at": "2026-05-14T10:00:00+00:00",
                        "pipeline_stage": "CLOSE_PROXY",
                        "fixture_id": 1,
                        "market_primary": "OVER_1_5",
                        "experiment_id": "OFFICIAL_BASELINE",
                        "selected_price": 1.35,
                    }
                ]
            ).to_csv(odds_dir / "vsigma_odds_snapshots.csv", index=False)

            paths = build_clv_calibration_report.build_clv_calibration_report(processed_dir, odds_dir, "2026-05-14")

            summary = pd.read_csv(paths["summary"])
            self.assertEqual(summary.iloc[0]["clv_direction"], "CLV_UNAVAILABLE")
            self.assertEqual(summary.iloc[0]["clv_interpretation"], "CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING")
            self.assertIn("CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING", paths["report"].read_text(encoding="utf-8"))

    def test_clv_report_computes_positive_negative_flat_movement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            odds_dir.mkdir(parents=True)
            rows = []
            for fixture_id, close_price in [(1, 1.35), (2, 1.45), (3, 1.4005)]:
                rows.append({"snapshot_id": f"{fixture_id}p", "target_date": "2026-05-14", "generated_at": "2026-05-14T08:00:00+00:00", "pipeline_stage": "PRE", "fixture_id": fixture_id, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "source_candidate_version": "OFFICIAL_BASELINE", "selected_price": 1.4})
                rows.append({"snapshot_id": f"{fixture_id}c", "target_date": "2026-05-14", "generated_at": "2026-05-14T10:00:00+00:00", "pipeline_stage": "CLOSE_PROXY", "fixture_id": fixture_id, "market_primary": "OVER_1_5", "experiment_id": "OFFICIAL_BASELINE", "source_candidate_version": "OFFICIAL_BASELINE", "selected_price": close_price})
            pd.DataFrame(rows).to_csv(odds_dir / "vsigma_odds_snapshots.csv", index=False)

            paths = build_clv_calibration_report.build_clv_calibration_report(processed_dir, odds_dir, "2026-05-14")

            directions = set(pd.read_csv(paths["summary"])["clv_direction"])
            self.assertEqual(directions, {"CLV_POSITIVE", "CLV_NEGATIVE", "CLV_FLAT"})

    def test_candidate_v7_calibration_advisor_sample_too_small(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            processed_dir.mkdir(parents=True)
            odds_dir.mkdir(parents=True)
            pd.DataFrame(
                [
                    {
                        "target_date": "2026-05-14",
                        "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
                        "fixture_id": 1,
                        "league": "League A",
                        "market_primary": "OVER_1_5",
                        "risk_tags": "FAILURE_MODE_LOW_CONVERSION",
                        "result": "WIN",
                        "profit_units": 0.4,
                        "record_status": "SETTLED",
                    }
                ]
            ).to_csv(processed_dir / "ledger.csv", index=False)
            pd.DataFrame([{"pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", "drift_status": "WATCH_PATTERN"}]).to_csv(
                processed_dir / "vsigma_drift_monitor_summary.csv",
                index=False,
            )

            paths = build_candidate_v7_calibration_advisor.build_candidate_v7_calibration_advisor(processed_dir, odds_dir, processed_dir / "ledger.csv", "2026-05-14")

            advice = pd.read_csv(paths["advice"])
            self.assertEqual(advice.iloc[0]["recommendation"], "SAMPLE_TOO_SMALL")

    def test_candidate_v7_calibration_advisor_suggests_stricter_when_roi_and_clv_bad(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            processed_dir.mkdir(parents=True)
            odds_dir.mkdir(parents=True)
            ledger_rows = []
            clv_rows = []
            for fixture_id in range(1, 12):
                ledger_rows.append(
                    {
                        "target_date": "2026-05-14",
                        "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
                        "fixture_id": fixture_id,
                        "league": "League A",
                        "market_primary": "OVER_1_5",
                        "risk_tags": "FAILURE_MODE_LOW_CONVERSION",
                        "result": "LOSS",
                        "profit_units": -1.0,
                        "record_status": "SETTLED",
                    }
                )
                clv_rows.append(
                    {
                        "target_date": "2026-05-14",
                        "fixture_id": fixture_id,
                        "market_primary": "OVER_1_5",
                        "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
                        "clv_direction": "CLV_NEGATIVE",
                        "clv_delta": 0.05,
                    }
                )
            pd.DataFrame(ledger_rows).to_csv(processed_dir / "ledger.csv", index=False)
            pd.DataFrame(clv_rows).to_csv(odds_dir / "vsigma_clv_summary.csv", index=False)
            pd.DataFrame([{"pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", "drift_status": "WATCH_PATTERN"}]).to_csv(
                processed_dir / "vsigma_drift_monitor_summary.csv",
                index=False,
            )

            paths = build_candidate_v7_calibration_advisor.build_candidate_v7_calibration_advisor(processed_dir, odds_dir, processed_dir / "ledger.csv", "2026-05-14")

            advice = pd.read_csv(paths["advice"])
            self.assertIn("RAISE_MIN_EDGE", set(advice["recommendation"]))

    def test_candidate_v7_calibration_advisor_does_not_change_thresholds_when_pre_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            processed_dir.mkdir(parents=True)
            odds_dir.mkdir(parents=True)
            ledger_rows = []
            clv_rows = []
            for fixture_id in range(1, 12):
                ledger_rows.append(
                    {
                        "target_date": "2026-05-14",
                        "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
                        "fixture_id": fixture_id,
                        "league": "League A",
                        "market_primary": "OVER_1_5",
                        "risk_tags": "FAILURE_MODE_LOW_CONVERSION",
                        "result": "LOSS",
                        "profit_units": -1.0,
                        "record_status": "SETTLED",
                    }
                )
                clv_rows.append(
                    {
                        "target_date": "2026-05-14",
                        "fixture_id": fixture_id,
                        "market_primary": "OVER_1_5",
                        "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
                        "clv_direction": "CLV_UNAVAILABLE",
                        "clv_delta": "",
                        "clv_interpretation": "CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING",
                    }
                )
            pd.DataFrame(ledger_rows).to_csv(processed_dir / "ledger.csv", index=False)
            pd.DataFrame(clv_rows).to_csv(odds_dir / "vsigma_clv_summary.csv", index=False)
            pd.DataFrame([{"pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", "drift_status": "WATCH_PATTERN"}]).to_csv(
                processed_dir / "vsigma_drift_monitor_summary.csv",
                index=False,
            )

            paths = build_candidate_v7_calibration_advisor.build_candidate_v7_calibration_advisor(processed_dir, odds_dir, processed_dir / "ledger.csv", "2026-05-14")

            advice = pd.read_csv(paths["advice"])
            self.assertEqual(set(advice["recommendation"]), {"INSUFFICIENT_CLV_DATA"})
            self.assertNotIn("RAISE_MIN_EDGE", set(advice["recommendation"]))
            self.assertIn("CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING", paths["report"].read_text(encoding="utf-8"))

    def test_candidate_v7_calibration_advisor_ignores_audit_only_clv_for_threshold_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            odds_dir = processed_dir / "odds_snapshots"
            processed_dir.mkdir(parents=True)
            odds_dir.mkdir(parents=True)
            ledger_rows = []
            clv_rows = []
            for fixture_id in range(1, 12):
                ledger_rows.append(
                    {
                        "target_date": "2026-05-14",
                        "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
                        "fixture_id": fixture_id,
                        "league": "League A",
                        "market_primary": "OVER_1_5",
                        "risk_tags": "FAILURE_MODE_LOW_CONVERSION",
                        "result": "LOSS",
                        "profit_units": -1.0,
                        "record_status": "SETTLED",
                    }
                )
                clv_rows.append(
                    {
                        "target_date": "2026-05-14",
                        "fixture_id": fixture_id,
                        "market_primary": "OVER_1_5",
                        "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
                        "clv_direction": "CLV_NEGATIVE",
                        "clv_delta": 0.05,
                        "snapshot_rebuild_mode": "BACKFILLED_FROM_AVAILABLE_OUTPUTS",
                        "true_pre_snapshot_available_flag": 0,
                        "clv_usable_for_threshold_calibration_flag": 0,
                    }
                )
            pd.DataFrame(ledger_rows).to_csv(processed_dir / "ledger.csv", index=False)
            pd.DataFrame(clv_rows).to_csv(odds_dir / "vsigma_clv_summary.csv", index=False)
            pd.DataFrame([{"pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", "drift_status": "WATCH_PATTERN"}]).to_csv(
                processed_dir / "vsigma_drift_monitor_summary.csv",
                index=False,
            )

            paths = build_candidate_v7_calibration_advisor.build_candidate_v7_calibration_advisor(processed_dir, odds_dir, processed_dir / "ledger.csv", "2026-05-14")

            advice = pd.read_csv(paths["advice"])
            self.assertEqual(set(advice["recommendation"]), {"INSUFFICIENT_CLV_DATA"})
            self.assertNotIn("RAISE_MIN_EDGE", set(advice["recommendation"]))
            self.assertIn("CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING", paths["report"].read_text(encoding="utf-8"))

    def test_immutable_ledger_writes_official_and_shadow_picks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            ledger_dir = processed_dir / "ledger"
            today_dir = processed_dir / "today"
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_DIR", ledger_dir))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_CSV", ledger_dir / "ledger.csv"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_JSONL", ledger_dir / "ledger.jsonl"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "DAILY_REPORT", ledger_dir / "daily.md"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "TODAY_DIR", today_dir))
            row = {
                "date": "2026-05-14",
                "fixture_id": 1,
                "league": "League A",
                "home_team": "A",
                "away_team": "B",
                "market_primary": "OVER_1_5",
                "market_alt": "OVER_2_5",
                "accuracy_mode_rank": 1,
                "competition_calibrated_prob": 0.72,
                "competition_raw_prob": 0.8,
                "accuracy_confidence_score": 123,
                "primary_edge": 0.1,
                "accuracy_mode_reason": "ACCURACY_CORE",
                "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
            }
            pd.DataFrame([row]).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)
            shadow = dict(row, competition_calibrated_prob=0.71)
            pd.DataFrame([shadow]).to_csv(processed_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
            v7_shadow = dict(row, price_discipline_decision="PRICE_OK", price_discipline_actual_edge=0.1)
            pd.DataFrame([v7_shadow]).to_csv(processed_dir / "vsigma_today_candidate_v7_competition_top.csv", index=False)

            update_immutable_daily_ledger.update_immutable_ledger(processed_dir, "2026-05-14", "PRE")

            ledger = pd.read_csv(ledger_dir / "ledger.csv", dtype=str)
            self.assertTrue(ledger["experiment_id"].eq("OFFICIAL_BASELINE").any())
            self.assertTrue(ledger["experiment_id"].eq("CANDIDATE_V2_SCHEDULE_ANOMALY").any())
            self.assertTrue(ledger["experiment_id"].eq("CANDIDATE_V7_PRICE_DISCIPLINE").any())
            self.assertTrue(ledger["record_status"].eq("NO_BET_RECORD").any())

    def test_immutable_ledger_duplicate_pre_run_does_not_duplicate_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            ledger_dir = processed_dir / "ledger"
            today_dir = processed_dir / "today"
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_DIR", ledger_dir))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_CSV", ledger_dir / "ledger.csv"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_JSONL", ledger_dir / "ledger.jsonl"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "DAILY_REPORT", ledger_dir / "daily.md"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "TODAY_DIR", today_dir))
            pd.DataFrame(
                [{"date": "2026-05-14", "fixture_id": 1, "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5"}]
            ).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)

            update_immutable_daily_ledger.update_immutable_ledger(processed_dir, "2026-05-14", "PRE")
            first_count = len(pd.read_csv(ledger_dir / "ledger.csv", dtype=str))
            update_immutable_daily_ledger.update_immutable_ledger(processed_dir, "2026-05-14", "PRE")
            second_count = len(pd.read_csv(ledger_dir / "ledger.csv", dtype=str))

            self.assertEqual(first_count, second_count)

    def test_immutable_ledger_post_updates_existing_pick(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            ledger_dir = processed_dir / "ledger"
            today_dir = processed_dir / "today"
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_DIR", ledger_dir))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_CSV", ledger_dir / "ledger.csv"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_JSONL", ledger_dir / "ledger.jsonl"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "DAILY_REPORT", ledger_dir / "daily.md"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "TODAY_DIR", today_dir))
            pd.DataFrame(
                [{"date": "2026-05-14", "fixture_id": 1, "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5"}]
            ).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)
            update_immutable_daily_ledger.update_immutable_ledger(processed_dir, "2026-05-14", "PRE")
            pd.DataFrame(
                [
                    {
                        "fixture_id": 1,
                        "home_team": "A",
                        "away_team": "B",
                        "market_primary": "OVER_1_5",
                        "ledger_result_status": "RESULT_AVAILABLE",
                        "actionable_result": "WIN",
                        "actionable_profit_units": 0.4,
                    },
                    {
                        "fixture_id": 2,
                        "home_team": "C",
                        "away_team": "D",
                        "market_primary": "BTTS_YES",
                        "ledger_result_status": "RESULT_AVAILABLE",
                        "actionable_result": "WIN",
                        "actionable_profit_units": 0.8,
                    },
                ]
            ).to_csv(processed_dir / "vsigma_execution_shortlist_results_ledger.csv", index=False)

            update_immutable_daily_ledger.update_immutable_ledger(processed_dir, "2026-05-14", "POST")

            ledger = pd.read_csv(ledger_dir / "ledger.csv", dtype=str)
            official = ledger[ledger["experiment_id"].eq("OFFICIAL_BASELINE") & ledger["fixture_id"].astype(str).eq("1")]
            self.assertEqual(official.iloc[0]["record_status"], "SETTLED")
            self.assertEqual(official.iloc[0]["result"], "WIN")
            self.assertFalse(ledger["fixture_id"].astype(str).eq("2").any())

    def test_daily_ledger_report_and_required_traceability_fields_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            ledger_dir = processed_dir / "ledger"
            today_dir = processed_dir / "today"
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_DIR", ledger_dir))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_CSV", ledger_dir / "ledger.csv"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_JSONL", ledger_dir / "ledger.jsonl"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "DAILY_REPORT", ledger_dir / "daily.md"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "TODAY_DIR", today_dir))
            pd.DataFrame(
                [{"date": "2026-05-14", "fixture_id": 1, "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5"}]
            ).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)

            update_immutable_daily_ledger.update_immutable_ledger(processed_dir, "2026-05-14", "PRE")

            self.assertTrue((ledger_dir / "daily.md").exists())
            self.assertTrue((today_dir / "2026-05-14" / "daily.md").exists())
            ledger = pd.read_csv(ledger_dir / "ledger.csv", dtype=str)
            for column in ["ledger_id", "source_file_hash", "ledger_row_hash", "record_status", "experiment_id"]:
                self.assertIn(column, ledger.columns)

    def test_experiment_performance_report_is_generated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            processed_dir = Path(tmp) / "processed"
            ledger_dir = processed_dir / "ledger"
            ledger_dir.mkdir(parents=True)
            ledger_path = ledger_dir / "ledger.csv"
            stack.enter_context(patch.object(build_experiment_performance_report, "LEDGER_DIR", ledger_dir))
            stack.enter_context(patch.object(build_experiment_performance_report, "SUMMARY_CSV", ledger_dir / "summary.csv"))
            stack.enter_context(patch.object(build_experiment_performance_report, "REPORT_MD", ledger_dir / "report.md"))
            pd.DataFrame(
                [
                    {
                        "target_date": "2026-05-14",
                        "experiment_id": "OFFICIAL_BASELINE",
                        "fixture_id": 1,
                        "market_primary": "OVER_1_5",
                        "calibrated_probability": 0.7,
                        "result": "WIN",
                        "profit_units": 0.4,
                        "record_status": "SETTLED",
                    }
                ]
            ).to_csv(ledger_path, index=False)

            paths = build_experiment_performance_report.build_performance_report(processed_dir, ledger_path)

            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["report"].exists())
            summary = pd.read_csv(paths["summary"])
            official = summary[summary["experiment_id"].eq("OFFICIAL_BASELINE")].iloc[0]
            self.assertEqual(int(official["wins"]), 1)

    def test_ledger_update_does_not_change_official_baseline_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            ledger_dir = processed_dir / "ledger"
            today_dir = processed_dir / "today"
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_DIR", ledger_dir))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_CSV", ledger_dir / "ledger.csv"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_JSONL", ledger_dir / "ledger.jsonl"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "DAILY_REPORT", ledger_dir / "daily.md"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "TODAY_DIR", today_dir))
            baseline_path = processed_dir / "vsigma_today_competition_top.csv"
            pd.DataFrame(
                [{"date": "2026-05-14", "fixture_id": 1, "home_team": "A", "away_team": "B", "market_primary": "OVER_1_5"}]
            ).to_csv(baseline_path, index=False)
            before = baseline_path.read_text(encoding="utf-8")

            update_immutable_daily_ledger.update_immutable_ledger(processed_dir, "2026-05-14", "PRE")

            self.assertEqual(baseline_path.read_text(encoding="utf-8"), before)


class PromotionThresholdGovernanceTests(unittest.TestCase):
    def write_registry(self, root: Path) -> Path:
        config_dir = root / "config"
        config_dir.mkdir(parents=True)
        registry_path = config_dir / "vsigma_experiment_registry.json"
        registry_path.write_text(
            """
{
  "experiments": [
    {
      "experiment_id": "OFFICIAL_BASELINE",
      "display_name": "Official",
      "status": "OFFICIAL",
      "allowed_to_select_officially": true,
      "selection_role": "official_selector"
    },
    {
      "experiment_id": "CANDIDATE_V2_SCHEDULE_ANOMALY",
      "display_name": "Candidate v2",
      "status": "SHADOW",
      "allowed_to_select_officially": false,
      "selection_role": "shadow_selector"
    },
    {
      "experiment_id": "CANDIDATE_V6_API_PREDICTIONS",
      "display_name": "Candidate v6",
      "status": "AUDIT_ONLY",
      "allowed_to_select_officially": false,
      "selection_role": "audit_layer"
    }
  ]
}
""".strip(),
            encoding="utf-8",
        )
        return registry_path

    def write_governance_inputs(self, processed_dir: Path) -> None:
        ledger_dir = processed_dir / "ledger"
        odds_dir = processed_dir / "odds_snapshots"
        ledger_dir.mkdir(parents=True)
        odds_dir.mkdir(parents=True)
        rows = []
        for idx in range(1, 13):
            rows.append(
                {
                    "target_date": "2026-05-14",
                    "experiment_id": "OFFICIAL_BASELINE",
                    "fixture_id": idx,
                    "league": "League A",
                    "market_primary": "OVER_1_5",
                    "risk_tags": "FAILURE_MODE_LOW_CONVERSION",
                    "calibrated_probability": 0.7,
                    "edge": 0.08,
                    "result": "LOSS" if idx <= 7 else "WIN",
                    "profit_units": -1.0 if idx <= 7 else 0.5,
                    "record_status": "SETTLED",
                }
            )
        pd.DataFrame(rows).to_csv(ledger_dir / "vsigma_immutable_daily_pick_ledger.csv", index=False)
        pd.DataFrame(
            [
                {
                    "pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION",
                    "settled_rows": 12,
                    "wins": 5,
                    "losses": 7,
                    "profit_units": -4.5,
                    "roi_percent": -37.5,
                    "drift_status": "WATCH_PATTERN",
                }
            ]
        ).to_csv(processed_dir / "vsigma_drift_monitor_summary.csv", index=False)
        pd.DataFrame(
            [
                {
                    "target_date": "2026-05-14",
                    "fixture_id": idx,
                    "market_primary": "OVER_1_5",
                    "experiment_id": "OFFICIAL_BASELINE",
                    "clv_direction": "CLV_UNAVAILABLE",
                    "clv_delta": "",
                    "clv_usable_for_threshold_calibration_flag": 0,
                }
                for idx in range(1, 13)
            ]
        ).to_csv(odds_dir / "vsigma_clv_summary.csv", index=False)
        pd.DataFrame(
            [
                {
                    "market_family": "OVER_1_5",
                    "failure_mode": "LOW_CONVERSION",
                    "drift_status": "WATCH_PATTERN",
                    "clv_direction": "CLV_UNAVAILABLE",
                    "league": "ALL",
                    "n": 12,
                    "wins": 5,
                    "losses": 7,
                    "profit_units": -4.5,
                    "roi_percent": -37.5,
                    "avg_clv_delta": "",
                    "recommendation": "INSUFFICIENT_CLV_DATA",
                    "recommendation_reason": "CLV unavailable; no threshold change.",
                }
            ]
        ).to_csv(odds_dir / "vsigma_candidate_v7_calibration_advice.csv", index=False)

    def test_governance_script_creates_all_output_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed_dir = root / "processed"
            processed_dir.mkdir()
            registry_path = self.write_registry(root)
            self.write_governance_inputs(processed_dir)

            paths = build_promotion_threshold_governance.build_governance(
                processed_dir=processed_dir,
                registry_path=registry_path,
                target_date="2026-05-14",
                today_dir=processed_dir / "today",
            )

            for key in [
                "promotion_summary",
                "promotion_report",
                "threshold_summary",
                "threshold_report",
                "dashboard",
                "dashboard_snapshot",
            ]:
                self.assertTrue(paths[key].exists(), key)

    def test_promotion_recommendation_sample_too_small_when_settled_low(self) -> None:
        row = pd.Series({"experiment_id": "CANDIDATE_V2_SCHEDULE_ANOMALY", "current_status": "SHADOW", "settled_picks": 2, "picks_total": 2})
        rec, _, _ = build_promotion_threshold_governance.promotion_recommendation(row, pd.Series({"hit_rate": 55, "brier_score": 0.2}))
        self.assertEqual(rec, "SAMPLE_TOO_SMALL")

    def test_candidate_cannot_promote_with_high_roi_but_insufficient_sample(self) -> None:
        row = pd.Series(
            {
                "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
                "current_status": "SHADOW",
                "settled_picks": 3,
                "picks_total": 3,
                "roi_percent": 150.0,
                "profit_units": 4.5,
            }
        )
        rec, _, _ = build_promotion_threshold_governance.promotion_recommendation(row, pd.Series({"hit_rate": 50, "brier_score": 0.3}))
        self.assertEqual(rec, "SAMPLE_TOO_SMALL")

    def test_candidate_with_worse_hit_and_brier_gets_do_not_promote(self) -> None:
        official = pd.Series({"hit_rate": 60.0, "brier_score": 0.2, "roi_percent": 5.0, "profit_units": 2.0, "max_drawdown": -1.0})
        row = pd.Series(
            {
                "experiment_id": "CANDIDATE_V2_SCHEDULE_ANOMALY",
                "current_status": "SHADOW",
                "settled_picks": 40,
                "picks_total": 40,
                "hit_rate": 45.0,
                "brier_score": 0.35,
            }
        )
        rec, _, _ = build_promotion_threshold_governance.promotion_recommendation(row, official)
        self.assertEqual(rec, "DO_NOT_PROMOTE")

    def test_audit_only_candidate_gets_audit_only(self) -> None:
        row = pd.Series({"experiment_id": "CANDIDATE_V6_API_PREDICTIONS", "current_status": "AUDIT_ONLY", "selection_role": "audit_layer", "settled_picks": 50})
        rec, _, _ = build_promotion_threshold_governance.promotion_recommendation(row, pd.Series({"hit_rate": 55, "brier_score": 0.2}))
        self.assertEqual(rec, "AUDIT_ONLY")

    def test_threshold_governance_sample_too_small_for_low_n(self) -> None:
        rec, _ = build_promotion_threshold_governance.threshold_recommendation(pd.Series({"settled_rows": 9, "roi_percent": -50.0}))
        self.assertEqual(rec, "SAMPLE_TOO_SMALL")

    def test_threshold_governance_raises_min_edge_when_roi_negative(self) -> None:
        rec, _ = build_promotion_threshold_governance.threshold_recommendation(
            pd.Series({"settled_rows": 12, "roi_percent": -10.0, "hit_rate": 58.0, "clv_direction": "CLV_POSITIVE"})
        )
        self.assertEqual(rec, "RAISE_MIN_EDGE")

    def test_clv_unavailable_leads_to_insufficient_clv_data(self) -> None:
        rec, _ = build_promotion_threshold_governance.threshold_recommendation(
            pd.Series({"settled_rows": 12, "roi_percent": -10.0, "hit_rate": 58.0, "clv_direction": "CLV_UNAVAILABLE", "clv_rows": 12})
        )
        self.assertEqual(rec, "INSUFFICIENT_CLV_DATA")

    def test_daily_dashboard_includes_version_leader_and_threshold_alerts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed_dir = root / "processed"
            processed_dir.mkdir()
            registry_path = self.write_registry(root)
            self.write_governance_inputs(processed_dir)

            paths = build_promotion_threshold_governance.build_governance(
                processed_dir=processed_dir,
                registry_path=registry_path,
                target_date="2026-05-14",
                today_dir=processed_dir / "today",
            )

            dashboard = paths["dashboard"].read_text(encoding="utf-8")
            self.assertIn("## Version Leader", dashboard)
            self.assertIn("## Threshold Alerts", dashboard)

    def test_governance_does_not_change_official_baseline_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed_dir = root / "processed"
            processed_dir.mkdir()
            registry_path = self.write_registry(root)
            self.write_governance_inputs(processed_dir)
            baseline_path = processed_dir / "vsigma_today_competition_top.csv"
            baseline_path.write_text("fixture_id,market_primary\n1,OVER_1_5\n", encoding="utf-8")
            before = baseline_path.read_text(encoding="utf-8")

            build_promotion_threshold_governance.build_governance(
                processed_dir=processed_dir,
                registry_path=registry_path,
                target_date="2026-05-14",
                today_dir=processed_dir / "today",
            )

            self.assertEqual(baseline_path.read_text(encoding="utf-8"), before)


class DailyCompetitionControllerTests(unittest.TestCase):
    target_date = "2026-05-15"

    def base_pick(self, minutes: float = 240.0) -> dict[str, object]:
        return {
            "target_date": self.target_date,
            "date": self.target_date,
            "fixture_id": 1544651,
            "league": "Serie B",
            "home_team": "Bari",
            "away_team": "Sudtirol",
            "market_primary": "OVER_1_5",
            "accuracy_mode_rank": 1,
            "competition_calibrated_prob": 0.78,
            "lineup_minutes_to_kickoff": minutes,
            "candidate_v7_prelock_status": "V7_WAITING_FOR_PRELOCK",
            "candidate_v7_execution_status": "V7_WAITING_FOR_PRELOCK",
            "price_discipline_decision": "PRICE_NEEDS_PRELOCK_CONFIRMATION",
        }

    def write_pre_outputs(self, processed_dir: Path, minutes: float = 240.0) -> None:
        snapshot_dir = processed_dir / "today" / self.target_date
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        row = self.base_pick(minutes)
        pd.DataFrame([row]).to_csv(snapshot_dir / "vsigma_today_competition_top.csv", index=False)
        pd.DataFrame([row]).to_csv(snapshot_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
        pd.DataFrame(columns=list(row.keys())).to_csv(snapshot_dir / "vsigma_today_candidate_v7_competition_top.csv", index=False)
        pd.DataFrame([row]).to_csv(snapshot_dir / "vsigma_today_candidate_v7_competition_shortlist.csv", index=False)
        pd.DataFrame([{"date": self.target_date, "timezone": "Atlantic/Canary"}]).to_csv(snapshot_dir / "today_pipeline_report.csv", index=False)

    def write_ledger(self, processed_dir: Path, settled: bool = False) -> None:
        ledger_dir = processed_dir / "ledger"
        ledger_dir.mkdir(parents=True, exist_ok=True)
        status = "SETTLED" if settled else "PRE_REGISTERED"
        result_status = "RESULT_AVAILABLE" if settled else "PENDING"
        result = "WIN" if settled else "PENDING"
        pd.DataFrame(
            [
                {
                    "target_date": self.target_date,
                    "experiment_id": "OFFICIAL_BASELINE",
                    "fixture_id": 1544651,
                    "home_team": "Bari",
                    "away_team": "Sudtirol",
                    "market_primary": "OVER_1_5",
                    "pipeline_stage": "POST" if settled else "PRE",
                    "record_status": status,
                    "result_status": result_status,
                    "result": result,
                    "profit_units": 0.53 if settled else "",
                    "is_official_pick": 1,
                }
            ]
        ).to_csv(ledger_dir / "vsigma_immutable_daily_pick_ledger.csv", index=False)

    def build_controller(self, processed_dir: Path, minutes: float = 240.0) -> tuple[pd.DataFrame, dict[str, Path]]:
        self.write_pre_outputs(processed_dir, minutes=minutes)
        self.write_ledger(processed_dir, settled=False)
        plan, paths, _ = run_daily_competition_controller.build_plan_and_status(
            processed_dir=processed_dir,
            target_date=self.target_date,
            timezone_name="Atlantic/Canary",
            window_minutes=90,
            now_local_value=pd.Timestamp("2026-05-15T12:00:00+01:00").to_pydatetime(),
        )
        return plan, paths

    def test_controller_plan_output_is_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            plan, paths = self.build_controller(processed_dir)

            self.assertTrue(paths["plan_csv"].exists())
            self.assertTrue(paths["plan_md"].exists())
            self.assertIn("daily_run_plan_latest.md", str(paths["latest_plan_md"]))
            self.assertFalse(plan.empty)

    def test_controller_status_output_is_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            _plan, paths = self.build_controller(processed_dir)

            self.assertTrue(paths["status_md"].exists())
            self.assertIn("## Next Operator Command", paths["status_md"].read_text(encoding="utf-8"))

    def test_controller_no_bet_day_produces_outputs_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            snapshot_dir = processed_dir / "today" / self.target_date
            snapshot_dir.mkdir(parents=True)
            pd.DataFrame([{"date": self.target_date, "timezone": "Atlantic/Canary"}]).to_csv(snapshot_dir / "today_pipeline_report.csv", index=False)
            plan, paths, _ = run_daily_competition_controller.build_plan_and_status(
                processed_dir=processed_dir,
                target_date=self.target_date,
                timezone_name="Atlantic/Canary",
                window_minutes=90,
                now_local_value=pd.Timestamp("2026-05-15T12:00:00+01:00").to_pydatetime(),
            )

            self.assertEqual(plan.iloc[0]["recommended_next_action"], "NO_BET_DAY")
            self.assertTrue(paths["status_md"].exists())

    def test_controller_prelock_pending_action_when_pick_outside_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            plan, _paths = self.build_controller(processed_dir, minutes=240.0)

            self.assertIn("WAIT_FOR_PRELOCK", set(plan["recommended_next_action"]))

    def test_controller_run_prelock_now_when_inside_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            plan, _paths = self.build_controller(processed_dir, minutes=45.0)

            self.assertIn("RUN_PRELOCK_NOW", set(plan["recommended_next_action"]))

    def test_controller_post_pending_when_results_unsettled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            self.write_pre_outputs(processed_dir, minutes=-30.0)
            self.write_ledger(processed_dir, settled=False)
            prelock = dict(self.base_pick(minutes=-30.0), prelock_status="IN_PRELOCK_WINDOW", prelock_decision="PRELOCK_CONFIRMED")
            pd.DataFrame([prelock]).to_csv(processed_dir / "today" / self.target_date / "vsigma_today_prelock_comparison.csv", index=False)

            plan, _paths, _ = run_daily_competition_controller.build_plan_and_status(
                processed_dir=processed_dir,
                target_date=self.target_date,
                timezone_name="Atlantic/Canary",
                window_minutes=90,
                now_local_value=pd.Timestamp("2026-05-15T12:00:00+01:00").to_pydatetime(),
            )

            self.assertIn("RUN_POST_AFTER_FINISH", set(plan["recommended_next_action"]))

    def test_controller_settled_status_after_post_data_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            self.write_pre_outputs(processed_dir, minutes=-180.0)
            self.write_ledger(processed_dir, settled=True)
            snapshot_dir = processed_dir / "today" / self.target_date
            pd.DataFrame([{"date": self.target_date, "pending_rows": 0, "result_available_rows": 1}]).to_csv(
                snapshot_dir / "today_post_results_report.csv",
                index=False,
            )

            plan, paths, _ = run_daily_competition_controller.build_plan_and_status(
                processed_dir=processed_dir,
                target_date=self.target_date,
                timezone_name="Atlantic/Canary",
                window_minutes=90,
                now_local_value=pd.Timestamp("2026-05-15T12:00:00+01:00").to_pydatetime(),
            )

            self.assertIn("ALL_SETTLED", set(plan["recommended_next_action"]))
            self.assertIn("- POST: SETTLED", paths["status_md"].read_text(encoding="utf-8"))

    def test_controller_does_not_change_official_baseline_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            self.write_pre_outputs(processed_dir, minutes=45.0)
            baseline_path = processed_dir / "today" / self.target_date / "vsigma_today_competition_top.csv"
            before = baseline_path.read_text(encoding="utf-8")

            run_daily_competition_controller.build_plan_and_status(
                processed_dir=processed_dir,
                target_date=self.target_date,
                timezone_name="Atlantic/Canary",
                window_minutes=90,
                now_local_value=pd.Timestamp("2026-05-15T12:00:00+01:00").to_pydatetime(),
            )

            self.assertEqual(baseline_path.read_text(encoding="utf-8"), before)


class DailyCompetitionSupervisorTests(unittest.TestCase):
    target_date = "2026-05-15"

    def base_pick(self, minutes: float = 240.0) -> dict[str, object]:
        return {
            "target_date": self.target_date,
            "date": self.target_date,
            "fixture_id": 1544651,
            "league": "Serie B",
            "home_team": "Bari",
            "away_team": "Sudtirol",
            "market_primary": "OVER_1_5",
            "accuracy_mode_rank": 1,
            "competition_calibrated_prob": 0.78,
            "lineup_minutes_to_kickoff": minutes,
            "candidate_v7_prelock_status": "V7_WAITING_FOR_PRELOCK",
            "candidate_v7_execution_status": "V7_WAITING_FOR_PRELOCK",
            "price_discipline_decision": "PRICE_NEEDS_PRELOCK_CONFIRMATION",
        }

    def write_pre_outputs(self, processed_dir: Path, minutes: float = 240.0) -> Path:
        snapshot_dir = processed_dir / "today" / self.target_date
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        row = self.base_pick(minutes)
        baseline_path = snapshot_dir / "vsigma_today_competition_top.csv"
        pd.DataFrame([row]).to_csv(baseline_path, index=False)
        pd.DataFrame([row]).to_csv(snapshot_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
        pd.DataFrame(columns=list(row.keys())).to_csv(snapshot_dir / "vsigma_today_candidate_v7_competition_top.csv", index=False)
        pd.DataFrame([row]).to_csv(snapshot_dir / "vsigma_today_candidate_v7_competition_shortlist.csv", index=False)
        pd.DataFrame([{"date": self.target_date, "timezone": "Atlantic/Canary"}]).to_csv(snapshot_dir / "today_pipeline_report.csv", index=False)
        return baseline_path

    def write_ledger(self, processed_dir: Path) -> Path:
        ledger_dir = processed_dir / "ledger"
        ledger_dir.mkdir(parents=True, exist_ok=True)
        ledger_path = ledger_dir / "vsigma_immutable_daily_pick_ledger.csv"
        pd.DataFrame(
            [
                {
                    "target_date": self.target_date,
                    "experiment_id": "OFFICIAL_BASELINE",
                    "fixture_id": 1544651,
                    "home_team": "Bari",
                    "away_team": "Sudtirol",
                    "market_primary": "OVER_1_5",
                    "pipeline_stage": "PRE",
                    "record_status": "PRE_REGISTERED",
                    "result_status": "PENDING",
                    "result": "PENDING",
                    "is_official_pick": 1,
                }
            ]
        ).to_csv(ledger_path, index=False)
        return ledger_path

    def fake_command(self, label: str, command: list[str], target_date: str, mode: str) -> run_daily_competition_supervisor.CommandResult:
        log_path = Path(tempfile.gettempdir()) / f"vsigma_supervisor_{label}.log"
        log_path.write_text("fake", encoding="utf-8")
        return run_daily_competition_supervisor.CommandResult(label, command, 0, "ok", "", log_path)

    def test_supervisor_status_output_is_generated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(run_daily_competition_supervisor, "run_command", side_effect=self.fake_command):
            processed_dir = Path(tmp) / "processed"
            self.write_pre_outputs(processed_dir)
            self.write_ledger(processed_dir)

            paths = run_daily_competition_supervisor.run_supervisor(
                self.target_date,
                "Atlantic/Canary",
                "status",
                processed_dir=processed_dir,
            )

            self.assertTrue(paths["report_md"].exists())
            self.assertTrue(paths["status_csv"].exists())
            self.assertIn("Daily Supervisor Report", paths["report_md"].read_text(encoding="utf-8"))

    def test_supervisor_handles_no_bet_day(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(run_daily_competition_supervisor, "run_command", side_effect=self.fake_command):
            processed_dir = Path(tmp) / "processed"
            snapshot_dir = processed_dir / "today" / self.target_date
            snapshot_dir.mkdir(parents=True)
            pd.DataFrame([{"date": self.target_date, "timezone": "Atlantic/Canary"}]).to_csv(snapshot_dir / "today_pipeline_report.csv", index=False)

            paths = run_daily_competition_supervisor.run_supervisor(
                self.target_date,
                "Atlantic/Canary",
                "status",
                processed_dir=processed_dir,
            )

            status = pd.read_csv(paths["status_csv"])
            self.assertEqual(status.iloc[0]["next_recommended_action"], "NO_BET_DAY")

    def test_supervisor_prelock_check_no_due_when_outside_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(run_daily_competition_supervisor, "run_command", side_effect=self.fake_command) as run_mock:
            processed_dir = Path(tmp) / "processed"
            self.write_pre_outputs(processed_dir, minutes=240.0)
            self.write_ledger(processed_dir)

            paths = run_daily_competition_supervisor.run_supervisor(
                self.target_date,
                "Atlantic/Canary",
                "prelock-check",
                processed_dir=processed_dir,
            )

            status = pd.read_csv(paths["status_csv"])
            self.assertEqual(status.iloc[0]["detail"], "NO_PRELOCK_DUE")
            self.assertTrue(all(call.args[0] != "controller_prelock" for call in run_mock.call_args_list))

    def test_supervisor_does_not_duplicate_ledger_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(run_daily_competition_supervisor, "run_command", side_effect=self.fake_command):
            processed_dir = Path(tmp) / "processed"
            self.write_pre_outputs(processed_dir, minutes=240.0)
            ledger_path = self.write_ledger(processed_dir)
            before_rows = len(pd.read_csv(ledger_path))

            run_daily_competition_supervisor.run_supervisor(self.target_date, "Atlantic/Canary", "prelock-check", processed_dir=processed_dir)
            run_daily_competition_supervisor.run_supervisor(self.target_date, "Atlantic/Canary", "prelock-check", processed_dir=processed_dir)
            after_rows = len(pd.read_csv(ledger_path))

            self.assertEqual(before_rows, after_rows)

    def test_supervisor_post_backup_default_targets_yesterday(self) -> None:
        with patch.object(run_daily_competition_supervisor, "local_today", return_value=pd.Timestamp("2026-05-16").date()):
            self.assertEqual(run_daily_competition_supervisor.default_target_date("post-backup", "Atlantic/Canary"), "2026-05-15")

    def test_supervisor_wrapper_command_generation_is_valid(self) -> None:
        command = run_daily_competition_supervisor.controller_command("2026-05-15", "Atlantic/Canary", "prelock", 90)

        self.assertIn("scripts/run_daily_competition_controller.py", command)
        self.assertIn("--mode", command)
        self.assertIn("prelock", command)
        self.assertIn("--window-minutes", command)

    def test_task_registration_scripts_exist(self) -> None:
        self.assertTrue((ROOT / "scripts" / "register_vsigma_windows_tasks.ps1").exists())
        self.assertTrue((ROOT / "scripts" / "unregister_vsigma_windows_tasks.ps1").exists())

    def test_task_registration_avoids_direct_repetition_mutation(self) -> None:
        script = (ROOT / "scripts" / "register_vsigma_windows_tasks.ps1").read_text(encoding="utf-8")

        self.assertNotIn(".Repetition.Interval", script)
        self.assertNotIn(".Repetition.Duration", script)
        self.assertIn("New-DailyTriggerSet", script)
        self.assertIn("WhatIfOnly", script)

    def test_supervisor_does_not_change_official_baseline_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(run_daily_competition_supervisor, "run_command", side_effect=self.fake_command):
            processed_dir = Path(tmp) / "processed"
            baseline_path = self.write_pre_outputs(processed_dir, minutes=240.0)
            self.write_ledger(processed_dir)
            before = baseline_path.read_text(encoding="utf-8")

            run_daily_competition_supervisor.run_supervisor(
                self.target_date,
                "Atlantic/Canary",
                "prelock-check",
                processed_dir=processed_dir,
            )

            self.assertEqual(baseline_path.read_text(encoding="utf-8"), before)


class VsigmaHealthcheckTests(unittest.TestCase):
    target_date = "2026-05-15"

    def base_pick(self) -> dict[str, object]:
        return {
            "target_date": self.target_date,
            "date": self.target_date,
            "fixture_id": 1544651,
            "league": "Serie B",
            "home_team": "Bari",
            "away_team": "Sudtirol",
            "market_primary": "OVER_1_5",
            "accuracy_mode_rank": 1,
            "competition_calibrated_prob": 0.78,
            "candidate_v7_execution_status": "V7_WAITING_FOR_PRELOCK",
        }

    def write_pre_outputs(self, processed_dir: Path, include_optional_candidates: bool = True) -> Path:
        processed_dir.mkdir(parents=True, exist_ok=True)
        snapshot_dir = processed_dir / "today" / self.target_date
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        row = self.base_pick()
        baseline_path = snapshot_dir / "vsigma_today_competition_top.csv"
        pd.DataFrame([row]).to_csv(baseline_path, index=False)
        pd.DataFrame([row]).to_csv(snapshot_dir / "vsigma_today_candidate_v2_competition_top.csv", index=False)
        pd.DataFrame(columns=list(row.keys())).to_csv(snapshot_dir / "vsigma_today_candidate_v7_competition_top.csv", index=False)
        pd.DataFrame([row]).to_csv(snapshot_dir / "vsigma_today_candidate_v7_competition_shortlist.csv", index=False)
        if include_optional_candidates:
            for version in ["v4", "v5", "v6"]:
                pd.DataFrame(columns=list(row.keys())).to_csv(snapshot_dir / f"vsigma_today_candidate_{version}_competition_top.csv", index=False)
        pd.DataFrame([{"date": self.target_date, "timezone": "Atlantic/Canary"}]).to_csv(snapshot_dir / "today_pipeline_report.csv", index=False)
        (snapshot_dir / "daily_competition_master_report.md").write_text("# master\n", encoding="utf-8")
        return baseline_path

    def write_validation_reports(self, processed_dir: Path) -> None:
        pd.DataFrame([{"target_date": self.target_date, "file_name": "vsigma_today_competition_top.csv", "status": "PASS", "detail": "fresh"}]).to_csv(
            processed_dir / "vsigma_daily_freshness_report.csv",
            index=False,
        )
        pd.DataFrame([{"target_date": self.target_date, "check_name": "candidate_does_not_overwrite_baseline_path", "status": "PASS", "detail": "isolated"}]).to_csv(
            processed_dir / "vsigma_candidate_isolation_report.csv",
            index=False,
        )

    def write_ledger(self, processed_dir: Path, duplicate: bool = False) -> None:
        ledger_dir = processed_dir / "ledger"
        ledger_dir.mkdir(parents=True, exist_ok=True)
        rows = [
            {
                "ledger_id": "2026-05-15-OFFICIAL-1544651",
                "target_date": self.target_date,
                "experiment_id": "OFFICIAL_BASELINE",
                "fixture_id": 1544651,
                "pipeline_stage": "PRE",
                "record_status": "PRE_REGISTERED",
                "is_official_pick": 1,
            }
        ]
        if duplicate:
            rows.append(dict(rows[0], market_primary="OVER_1_5"))
        pd.DataFrame(rows).to_csv(ledger_dir / "vsigma_immutable_daily_pick_ledger.csv", index=False)

    def run_healthcheck(self, processed_dir: Path) -> dict[str, object]:
        return run_vsigma_healthcheck.run_healthcheck(
            self.target_date,
            "Atlantic/Canary",
            "quick",
            processed_dir=processed_dir,
            root=ROOT,
        )

    def test_healthcheck_report_is_generated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            self.write_pre_outputs(processed_dir)
            self.write_validation_reports(processed_dir)
            self.write_ledger(processed_dir)

            paths = self.run_healthcheck(processed_dir)

            self.assertTrue(paths["summary_csv"].exists())
            self.assertTrue(paths["report_md"].exists())
            self.assertTrue(paths["snapshot_report_md"].exists())
            self.assertIn(paths["global_status"], run_vsigma_healthcheck.STATUSES)

    def test_healthcheck_missing_optional_candidate_does_not_break(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            self.write_pre_outputs(processed_dir, include_optional_candidates=False)
            self.write_validation_reports(processed_dir)
            self.write_ledger(processed_dir)

            paths = self.run_healthcheck(processed_dir)
            summary = pd.read_csv(paths["summary_csv"])
            optional = summary[summary["check_name"].eq("candidate_output:CANDIDATE_V4")]

            self.assertFalse(optional.empty)
            self.assertNotEqual(optional.iloc[0]["status"], "BROKEN")
            self.assertNotEqual(paths["global_status"], "BROKEN")

    def test_healthcheck_stale_prelock_creates_warning_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            self.write_pre_outputs(processed_dir)
            self.write_validation_reports(processed_dir)
            self.write_ledger(processed_dir)
            snapshot_dir = processed_dir / "today" / self.target_date
            stale = dict(self.base_pick(), target_date="2026-05-14", date="2026-05-14", prelock_status="IN_PRELOCK_WINDOW")
            pd.DataFrame([stale]).to_csv(snapshot_dir / "vsigma_today_prelock_comparison.csv", index=False)

            paths = self.run_healthcheck(processed_dir)
            summary = pd.read_csv(paths["summary_csv"])
            prelock = summary[summary["check_name"].eq("prelock_freshness")].iloc[0]

            self.assertEqual(prelock["status"], "WARNING")
            self.assertIn("stale prelock", prelock["detail"])

    def test_healthcheck_duplicate_ledger_ids_create_broken_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            self.write_pre_outputs(processed_dir)
            self.write_validation_reports(processed_dir)
            self.write_ledger(processed_dir, duplicate=True)

            paths = self.run_healthcheck(processed_dir)
            summary = pd.read_csv(paths["summary_csv"])
            duplicates = summary[summary["check_name"].eq("ledger_duplicate_ids")].iloc[0]

            self.assertEqual(duplicates["status"], "BROKEN")
            self.assertEqual(paths["global_status"], "BROKEN")

    def test_healthcheck_recovery_commands_appear(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir(parents=True)

            paths = self.run_healthcheck(processed_dir)
            summary = pd.read_csv(paths["summary_csv"])
            recoveries = summary["recovery_command"].dropna().astype(str).tolist()

            self.assertTrue(any("run_daily_competition_controller.py" in command for command in recoveries))

    def test_master_report_includes_healthcheck_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            snapshot_dir = processed_dir / "today" / self.target_date
            self.write_pre_outputs(processed_dir)
            self.write_validation_reports(processed_dir)
            self.write_ledger(processed_dir)
            self.run_healthcheck(processed_dir)

            path = build_daily_competition_master_report.build_master_report(
                processed_dir=processed_dir,
                target_date=self.target_date,
                snapshot_dir=snapshot_dir,
            )

            self.assertIn("## Healthcheck", path.read_text(encoding="utf-8"))

    def test_healthcheck_does_not_change_official_baseline_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            baseline_path = self.write_pre_outputs(processed_dir)
            self.write_validation_reports(processed_dir)
            self.write_ledger(processed_dir)
            before = baseline_path.read_text(encoding="utf-8")

            self.run_healthcheck(processed_dir)

            self.assertEqual(baseline_path.read_text(encoding="utf-8"), before)


class PrelockOrchestratorTests(unittest.TestCase):
    def price_config(self, root: Path) -> Path:
        path = root / "price_config.json"
        path.write_text(
            """
{
  "default_rule": {
    "min_edge": 0.055,
    "min_calibrated_probability": 0.70,
    "allow_secondary_only": true,
    "drift_status_penalty": {
      "WATCH_PATTERN": 0.0
    }
  },
  "rules": [
    {
      "market_family": "OVER_1_5",
      "failure_mode": "LOW_CONVERSION",
      "min_edge": 0.055,
      "min_calibrated_probability": 0.70,
      "allow_secondary_only": true,
      "require_prelock_if_watch_pattern": true,
      "drift_status_penalty": {
        "WATCH_PATTERN": 0.0
      }
    }
  ]
}
""".strip(),
            encoding="utf-8",
        )
        return path

    def candidate_v2_row(self) -> dict[str, object]:
        return {
            "target_date": "2026-05-15",
            "date": "2026-05-15",
            "fixture_id": 1544651,
            "league": "Serie B",
            "home_team": "Bari",
            "away_team": "Sudtirol",
            "market_primary": "OVER_1_5",
            "market_alt": "OVER_2_5",
            "primary_model_prob": 0.855,
            "competition_calibrated_prob": 0.78,
            "primary_odds_used": 1.53,
            "primary_edge": 0.20,
            "accuracy_primary_risk": "FAILURE_MODE_LOW_CONVERSION",
            "final_recommendation": "BET",
            "accuracy_mode_eligible_flag": 1,
            "accuracy_mode_rank": 1,
        }

    def write_drift(self, root: Path) -> Path:
        path = root / "drift.csv"
        pd.DataFrame(
            [{"pattern": "OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", "drift_status": "WATCH_PATTERN"}]
        ).to_csv(path, index=False)
        return path

    def test_stale_prelock_rows_excluded_from_active_master_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            processed_dir = Path(tmp) / "processed"
            snapshot_dir = processed_dir / "today" / "2026-05-15"
            processed_dir.mkdir(parents=True)
            snapshot_dir.mkdir(parents=True)
            pd.DataFrame([self.candidate_v2_row()]).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)
            pd.DataFrame([self.candidate_v2_row()]).to_csv(processed_dir / "vsigma_today_candidate_v7_competition_shortlist.csv", index=False)
            stale = dict(self.candidate_v2_row(), target_date="2026-05-14", date="2026-05-14", home_team="Valencia", prelock_status="IN_PRELOCK_WINDOW", prelock_decision="PRELOCK_NO_CHANGE")
            pd.DataFrame([stale]).to_csv(processed_dir / "vsigma_today_prelock_comparison.csv", index=False)

            path = build_daily_competition_master_report.build_master_report(processed_dir, "2026-05-15", snapshot_dir)

            text = path.read_text(encoding="utf-8")
            active_section = text.split("### Active Pre-Lock Decisions", 1)[1].split("### Stale Pre-Lock Warning", 1)[0]
            warning_section = text.split("### Stale Pre-Lock Warning", 1)[1]
            self.assertNotIn("Valencia", active_section)
            self.assertIn("STALE_PRELOCK_EXCLUDED", warning_section)
            self.assertIn("2026-05-14", warning_section)

    def test_candidate_v7_waiting_state_before_valid_prelock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = pd.DataFrame([self.candidate_v2_row()])
            out = apply_price_discipline_guard.apply_price_discipline_guard(
                source,
                config_path=self.price_config(root),
                drift_path=self.write_drift(root),
                prelock_path=root / "missing_prelock.csv",
                target_date="2026-05-15",
            )
            self.assertEqual(out.iloc[0]["candidate_v7_execution_status"], "V7_WAITING_FOR_PRELOCK")

    def test_candidate_v7_confirmed_state_after_valid_prelock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prelock_path = root / "prelock.csv"
            pd.DataFrame(
                [dict(self.candidate_v2_row(), prelock_status="IN_PRELOCK_WINDOW", prelock_decision="PRELOCK_NO_CHANGE")]
            ).to_csv(prelock_path, index=False)
            out = apply_price_discipline_guard.apply_price_discipline_guard(
                pd.DataFrame([self.candidate_v2_row()]),
                config_path=self.price_config(root),
                drift_path=self.write_drift(root),
                prelock_path=prelock_path,
                target_date="2026-05-15",
            )
            self.assertEqual(out.iloc[0]["candidate_v7_execution_status"], "V7_PRELOCK_CONFIRMED")

    def test_candidate_v7_rejected_state_after_prelock_contradiction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prelock_path = root / "prelock.csv"
            pd.DataFrame(
                [dict(self.candidate_v2_row(), prelock_status="IN_PRELOCK_WINDOW", prelock_decision="PRELOCK_DOWNGRADED")]
            ).to_csv(prelock_path, index=False)
            out = apply_price_discipline_guard.apply_price_discipline_guard(
                pd.DataFrame([self.candidate_v2_row()]),
                config_path=self.price_config(root),
                drift_path=self.write_drift(root),
                prelock_path=prelock_path,
                target_date="2026-05-15",
            )
            self.assertEqual(out.iloc[0]["candidate_v7_execution_status"], "V7_PRELOCK_REJECTED")

    def test_orchestrator_handles_no_fixtures_in_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(run_today_prelock_orchestrator, "run_optional_step_with_args", return_value=True):
            processed_dir = Path(tmp) / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            row = dict(self.candidate_v2_row(), lineup_minutes_to_kickoff=240)
            pd.DataFrame([row]).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)
            paths = run_today_prelock_orchestrator.run_prelock_orchestrator(
                processed_dir=processed_dir,
                today_dir=today_dir,
                target_date="2026-05-15",
                now_utc=pd.Timestamp("2026-05-15T12:00:00Z").to_pydatetime(),
            )
            summary = pd.read_csv(paths["summary"])
            self.assertEqual(summary.iloc[0]["orchestrator_status"], "PRELOCK_NO_FIXTURES_IN_WINDOW")
            active_prelock = pd.read_csv(processed_dir / "vsigma_today_prelock_comparison.csv")
            self.assertEqual(len(active_prelock), 0)

    def test_ledger_prelock_update_does_not_duplicate_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            processed_dir = Path(tmp) / "processed"
            processed_dir.mkdir()
            ledger_dir = processed_dir / "ledger"
            today_dir = processed_dir / "today"
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_DIR", ledger_dir))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_CSV", ledger_dir / "ledger.csv"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "LEDGER_JSONL", ledger_dir / "ledger.jsonl"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "DAILY_REPORT", ledger_dir / "daily.md"))
            stack.enter_context(patch.object(update_immutable_daily_ledger, "TODAY_DIR", today_dir))
            pd.DataFrame([self.candidate_v2_row()]).to_csv(processed_dir / "vsigma_today_competition_top.csv", index=False)
            update_immutable_daily_ledger.update_immutable_ledger(processed_dir, "2026-05-15", "PRE")
            pd.DataFrame(
                [dict(self.candidate_v2_row(), prelock_status="IN_PRELOCK_WINDOW", prelock_decision="PRELOCK_NO_CHANGE")]
            ).to_csv(processed_dir / "vsigma_today_prelock_comparison.csv", index=False)

            update_immutable_daily_ledger.update_immutable_ledger(processed_dir, "2026-05-15", "PRELOCK")
            first_count = len(pd.read_csv(ledger_dir / "ledger.csv", dtype=str))
            update_immutable_daily_ledger.update_immutable_ledger(processed_dir, "2026-05-15", "PRELOCK")
            second_count = len(pd.read_csv(ledger_dir / "ledger.csv", dtype=str))

            self.assertEqual(first_count, second_count)

    def test_prelock_orchestrator_does_not_change_official_baseline_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(run_today_prelock_orchestrator, "run_optional_step_with_args", return_value=True):
            processed_dir = Path(tmp) / "processed"
            today_dir = processed_dir / "today"
            processed_dir.mkdir(parents=True)
            baseline_path = processed_dir / "vsigma_today_competition_top.csv"
            pd.DataFrame([dict(self.candidate_v2_row(), lineup_minutes_to_kickoff=240)]).to_csv(baseline_path, index=False)
            before = baseline_path.read_text(encoding="utf-8")

            run_today_prelock_orchestrator.run_prelock_orchestrator(
                processed_dir=processed_dir,
                today_dir=today_dir,
                target_date="2026-05-15",
                now_utc=pd.Timestamp("2026-05-15T12:00:00Z").to_pydatetime(),
            )

            self.assertEqual(baseline_path.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
