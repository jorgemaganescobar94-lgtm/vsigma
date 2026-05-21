# vSIGMA Governance Dashboard - 2026-05-21

## Version Leader
| official_version | current_best_official | main_challenger | best_roi_candidate | best_hit_rate_candidate | best_brier_candidate | most_stable_candidate | small_sample_candidates | audit_only_candidates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL_BASELINE | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V7_PRICE_DISCIPLINE | CANDIDATE_V7_PRICE_DISCIPLINE | CANDIDATE_V7_PRICE_DISCIPLINE | INSUFFICIENT_EVIDENCE | CANDIDATE_V2_SCHEDULE_ANOMALY, CANDIDATE_V4_O25_FIREWALL, CANDIDATE_V5_PLAYER_IMPACT, CANDIDATE_V7_PRICE_DISCIPLINE | CANDIDATE_V3_ODDS_DEPTH, CANDIDATE_V6_API_PREDICTIONS |

## Promotion Status
| experiment_id | settled_picks | roi_percent | brier_score | promotion_recommendation | required_next_evidence |
| --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 7 | -16.714286 | 0.309746 | KEEP_OFFICIAL_BASELINE | Continue accumulating official settled outcomes and compare challengers against it. |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 6 | -28.166667 | 0.349927 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V3_ODDS_DEPTH | 0 |  |  | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V4_O25_FIREWALL | 6 | -28.166667 | 0.349927 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V5_PLAYER_IMPACT | 6 | -28.166667 | 0.349927 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V6_API_PREDICTIONS | 6 | -28.166667 | 0.349649 | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 36.0 | 0.020079 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |

## Threshold Alerts
| market_family | failure_mode | experiment_id | settled_rows | roi_percent | clv_direction | threshold_recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 5 | -41.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V4_O25_FIREWALL | 5 | -41.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | 5 | -41.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | 5 | -41.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 5 | -41.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 4 | -75.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 3 | 0.0 | CLV_FLAT | SAMPLE_TOO_SMALL |
| UNDER_3_5 | ANY | CANDIDATE_V7_PRICE_DISCIPLINE | 3 | 36.0 | CLV_FLAT | SAMPLE_TOO_SMALL |
| UNDER_3_5 | ANY | CANDIDATE_V7_PRICE_DISCIPLINE | 3 | 36.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 2 | -100.0 | CLV_FLAT | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 0.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | CANDIDATE_V4_O25_FIREWALL | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | CANDIDATE_V5_PLAYER_IMPACT | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | CANDIDATE_V6_API_PREDICTIONS | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | OFFICIAL_BASELINE | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 1 | 52.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL |

## Drift Alerts
| alert_level | pattern | settled_rows | profit_units | roi_percent | drift_status | governance_action |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE_TOO_SMALL | OVER_2_5 + FAILURE_MODE_LOW_CONVERSION | 6 | 4.26 | 71.0 | NO_DRIFT | Review threshold summary before any config change. |
| WATCH | OVER_1_5 + FAILURE_MODE_LOW_CONVERSION | 26 | -3.39 | -13.038462 | WATCH_PATTERN | Review threshold summary before any config change. |
| SAMPLE_TOO_SMALL | BTTS_YES + FAILURE_MODE_BTTS_BREAK | 0 | 0.0 |  | SAMPLE_TOO_SMALL | Review threshold summary before any config change. |
| SAMPLE_TOO_SMALL | HOME/AWAY_WIN + FAILURE_MODE_DRAW_LIVE | 5 | 5.0 | 100.0 | NO_DRIFT | Review threshold summary before any config change. |
| SAMPLE_TOO_SMALL | candidate v2 vs baseline daily winner | 8 | 1.67 | 20.875 | NO_DRIFT | Review threshold summary before any config change. |
| SAMPLE_TOO_SMALL | candidate v4 firewall performance | 6 | 0.25 | 4.166667 | NO_DRIFT | Review threshold summary before any config change. |
| SAMPLE_TOO_SMALL | candidate v5 player-impact adjusted subset | 8 | 1.67 | 20.875 | NO_DRIFT | Review threshold summary before any config change. |
| SAMPLE_TOO_SMALL | candidate v6 API-prediction aligned subset | 1 | 1.0 | 100.0 | SAMPLE_TOO_SMALL | Review threshold summary before any config change. |
| SAMPLE_TOO_SMALL | candidate v6 API-prediction disagreement subset | 0 | 0.0 |  | SAMPLE_TOO_SMALL | Review threshold summary before any config change. |

## Daily Winners
| target_date | daily_winner | winner_reason |
| --- | --- | --- |
| 2026-05-14 | TIE | Top experiments tied on profit and hit rate. |
| 2026-05-15 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-16 | OFFICIAL_BASELINE | OFFICIAL_BASELINE led on profit=0.07, hit_rate=66.666667, settled=3. |
| 2026-05-17 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-18 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-19 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-20 | NO_BET_DAY | No model registered a pick. |
| 2026-05-21 | CANDIDATE_V7 | CANDIDATE_V7_PRICE_DISCIPLINE led on profit=0.36, hit_rate=100.0, settled=1. |

## CLV Data Sufficiency
CLV_DATA_SUFFICIENT_FOR_REVIEW: usable=10, available_direction_rows=10; advice remains reporting-only.

## Evidence Status
- All primary governance inputs available.

Official baseline remains unchanged: yes.
