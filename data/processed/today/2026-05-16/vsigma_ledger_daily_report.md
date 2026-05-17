# vSIGMA Immutable Ledger Daily Report - 2026-05-16

## Ledger Update Status
- Ledger CSV: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- JSONL event log: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.jsonl
- Official picks registered: 3
- Shadow picks registered: 9
- No-bet records: 1
- Pending records: 1
- Settled records: 11
- Daily winner: OFFICIAL_BASELINE

## Experiment Registry
| experiment_id | status | selection_role | allowed_to_select_officially | current_verdict |
| --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | official_selector | True | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | shadow_selector | False | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | audit_layer | False | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | shadow_selector | False | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | shadow_selector | False | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | audit_layer | False | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | shadow_selector | False | PRICE_DISCIPLINE_UNTESTED |

## Daily Summary By Experiment
| experiment_id | records | picks | no_bet_records | pending | settled | profit_units |
| --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 2 | 2 | 0 | 0 | 2 | -0.45 |
| CANDIDATE_V3_ODDS_DEPTH | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V4_O25_FIREWALL | 2 | 2 | 0 | 0 | 2 | -0.45 |
| CANDIDATE_V5_PLAYER_IMPACT | 2 | 2 | 0 | 0 | 2 | -0.45 |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 2 | 0 | 0 | 2 | -0.45 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1 | 0 | 1 | 0 | 0.0 |
| OFFICIAL_BASELINE | 3 | 3 | 0 | 0 | 3 | 0.07 |

## Official Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 2 | 1392194 | Granada CF | Burgos | OVER_1_5 | 0.8132 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.240; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| OFFICIAL_BASELINE | 3 | 1544949 | Juve Stabia | Monza | OVER_1_5 | 0.7672 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.202; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| OFFICIAL_BASELINE | 1 | 1388609 | SC Freiburg | RB Leipzig | OVER_2_5 | 0.797925 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.123; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |

## Shadow Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 1392194 | Granada CF | Burgos | OVER_1_5 | 0.796 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.222; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 2 | 1544949 | Juve Stabia | Monza | OVER_1_5 | 0.7637 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.199; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1 | 1392194 | Granada CF | Burgos | OVER_1_5 | 0.796 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.222; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 2 | 1544949 | Juve Stabia | Monza | OVER_1_5 | 0.7637 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.199; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1 | 1392194 | Granada CF | Burgos | OVER_1_5 | 0.796 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.222; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 2 | 1544949 | Juve Stabia | Monza | OVER_1_5 | 0.7637 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.199; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1 | 1392194 | Granada CF | Burgos | OVER_1_5 | 0.796 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.222; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 1544949 | Juve Stabia | Monza | OVER_1_5 | 0.7637 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.199; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1392194 | Granada CF | Burgos | OVER_1_5 | 0.796 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.222; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |

## No-Bet Modes
| experiment_id | record_status | reason_tags | source_file |
| --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH | NO_BET_RECORD | NO_BET; SOURCE_FILE_MISSING_OR_NOT_AVAILABLE | vsigma_today_candidate_v3_competition_top.csv |

## Pre-Lock Changes
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_status | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1392194 | Granada CF | Burgos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| OFFICIAL_BASELINE | 1544949 | Juve Stabia | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1392194 | Granada CF | Burgos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544949 | Juve Stabia | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V4_O25_FIREWALL | 1392194 | Granada CF | Burgos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V4_O25_FIREWALL | 1544949 | Juve Stabia | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V5_PLAYER_IMPACT | 1392194 | Granada CF | Burgos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V5_PLAYER_IMPACT | 1544949 | Juve Stabia | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V6_API_PREDICTIONS | 1392194 | Granada CF | Burgos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V6_API_PREDICTIONS | 1544949 | Juve Stabia | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1392194 | Granada CF | Burgos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| OFFICIAL_BASELINE | 1388609 | SC Freiburg | RB Leipzig | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |

## Result State
| experiment_id | fixture_id | market_primary | result_status | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1392194 | OVER_1_5 | RESULT_AVAILABLE | LOSS | -1.0 | SETTLED |
| OFFICIAL_BASELINE | 1544949 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.55 | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1392194 | OVER_1_5 | RESULT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544949 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.55 | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1392194 | OVER_1_5 | RESULT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1544949 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.55 | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1392194 | OVER_1_5 | RESULT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1544949 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.55 | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1392194 | OVER_1_5 | RESULT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1544949 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.55 | SETTLED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1392194 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| OFFICIAL_BASELINE | 1388609 | OVER_2_5 | RESULT_AVAILABLE | WIN | 0.52 | SETTLED |

## Freshness Warnings
| file_name | status | detail |
| --- | --- | --- |
| vsigma_today_candidate_v7_competition_top.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_prelock_competition_top.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_prelock_comparison.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| today_post_results_report.csv | WARNING_STALE_GLOBAL_FILE | snapshot context file not present yet |
