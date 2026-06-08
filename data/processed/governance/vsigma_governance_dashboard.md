# vSIGMA Governance Dashboard - 2026-06-07

## Version Leader
| official_version | current_best_official | main_challenger | best_roi_candidate | best_hit_rate_candidate | best_brier_candidate | most_stable_candidate | small_sample_candidates | audit_only_candidates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL_BASELINE | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V4_O25_FIREWALL | CANDIDATE_V4_O25_FIREWALL | CANDIDATE_V4_O25_FIREWALL | INSUFFICIENT_EVIDENCE | CANDIDATE_V2_SCHEDULE_ANOMALY, CANDIDATE_V4_O25_FIREWALL, CANDIDATE_V5_PLAYER_IMPACT, CANDIDATE_V7_PRICE_DISCIPLINE | CANDIDATE_V3_ODDS_DEPTH, CANDIDATE_V6_API_PREDICTIONS |

## Promotion Status
| experiment_id | settled_picks | roi_percent | brier_score | promotion_recommendation | required_next_evidence |
| --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 8 | -8.25 | 0.282192 | KEEP_OFFICIAL_BASELINE | Continue accumulating official settled outcomes and compare challengers against it. |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 7 | -16.857143 | 0.308389 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V3_ODDS_DEPTH | 0 |  |  | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V4_O25_FIREWALL | 7 | 1.0 | 0.218245 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V5_PLAYER_IMPACT | 7 | 1.0 | 0.221381 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V6_API_PREDICTIONS | 6 | -3.0 | 0.251104 | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | -100.0 | 0.652097 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |

## Threshold Alerts
| market_family | failure_mode | experiment_id | settled_rows | roi_percent | clv_direction | threshold_recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V4_O25_FIREWALL | 7 | 1.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | 7 | 1.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 6 | -3.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | 6 | -3.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 6 | -3.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 5 | 0.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 2 | -24.0 |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | -100.0 |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 1 | -100.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 0.0 | CLV_FLAT | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V2_SCHEDULE_ANOMALY | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V4_O25_FIREWALL | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V5_PLAYER_IMPACT | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V6_API_PREDICTIONS | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V2_SCHEDULE_ANOMALY | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V5_PLAYER_IMPACT | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | OFFICIAL_BASELINE | 0 |  |  | SAMPLE_TOO_SMALL |

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
| 2026-05-19 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-20 | NO_BET_DAY | No model registered a pick. |
| 2026-05-21 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-22 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-23 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-24 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-25 | TIE | Top experiments tied on profit and hit rate. |
| 2026-05-26 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-27 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-28 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-29 | TIE | Top experiments tied on profit and hit rate. |
| 2026-05-30 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-05-31 | NO_BET_DAY | No model registered a pick. |
| 2026-06-06 | NO_SETTLED_RESULTS | Picks exist but no settled results are available. |
| 2026-06-07 | NO_BET_DAY | No model registered a pick. |

## CLV Data Sufficiency
INSUFFICIENT_CLV_DATA: usable=1, available_direction_rows=1; do not change thresholds from CLV yet.

## Evidence Status
- All primary governance inputs available.

Official baseline remains unchanged: yes.
