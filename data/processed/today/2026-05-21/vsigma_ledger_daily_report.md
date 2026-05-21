# vSIGMA Immutable Ledger Daily Report - 2026-05-21

## Ledger Update Status
- Ledger CSV: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- JSONL event log: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.jsonl
- Official picks registered: 3
- Shadow picks registered: 13
- No-bet records: 1
- Pending records: 5
- Settled records: 11
- Daily winner: CANDIDATE_V7_PRICE_DISCIPLINE

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
| CANDIDATE_V2_SCHEDULE_ANOMALY | 3 | 3 | 0 | 1 | 2 | -0.64 |
| CANDIDATE_V3_ODDS_DEPTH | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V4_O25_FIREWALL | 3 | 3 | 0 | 1 | 2 | -0.64 |
| CANDIDATE_V5_PLAYER_IMPACT | 3 | 3 | 0 | 1 | 2 | -0.64 |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 2 | 0 | 0 | 2 | -0.64 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 2 | 2 | 0 | 1 | 1 | 0.36 |
| OFFICIAL_BASELINE | 3 | 3 | 0 | 1 | 2 | -0.64 |

## Official Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1 | 1545410 | Brondby | FC Copenhagen | OVER_2_5 | 0.801325 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.252; market_fit=SAFE_OK; LOW_CONVERSION | PENDING |
| OFFICIAL_BASELINE | 2 | 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | 0.8157 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.191; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| OFFICIAL_BASELINE | 3 | 1535208 | Gremio | Palestino | UNDER_3_5 | 0.8613 | FAILURE_MODE_AVALANCHE_RISK; FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.176; market_fit=SAFE_OK; AVALANCHE_RISK | SETTLED |

## Shadow Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 1545410 | Brondby | FC Copenhagen | OVER_2_5 | 0.797325 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.248; market_fit=SAFE_OK; LOW_CONVERSION | PENDING |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 2 | 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | 0.8181 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.194; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 3 | 1535208 | Gremio | Palestino | UNDER_3_5 | 0.8583 | FAILURE_MODE_AVALANCHE_RISK; FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.173; market_fit=SAFE_OK; AVALANCHE_RISK | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1 | 1545410 | Brondby | FC Copenhagen | OVER_1_5 | 0.84996 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.248; market_fit=SAFE_OK; LOW_CONVERSION | PENDING |
| CANDIDATE_V4_O25_FIREWALL | 2 | 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | 0.8181 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.194; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 3 | 1535208 | Gremio | Palestino | UNDER_3_5 | 0.8583 | FAILURE_MODE_AVALANCHE_RISK; FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.173; market_fit=SAFE_OK; AVALANCHE_RISK | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1 | 1545410 | Brondby | FC Copenhagen | OVER_2_5 | 0.797325 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.248; market_fit=SAFE_OK; LOW_CONVERSION | PENDING |
| CANDIDATE_V5_PLAYER_IMPACT | 2 | 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | 0.8181 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.194; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 3 | 1535208 | Gremio | Palestino | UNDER_3_5 | 0.8583 | FAILURE_MODE_AVALANCHE_RISK; FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.173; market_fit=SAFE_OK; AVALANCHE_RISK | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1 | 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | 0.8181 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.194; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 1535208 | Gremio | Palestino | UNDER_3_5 | 0.8643 | FAILURE_MODE_AVALANCHE_RISK; FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.173; market_fit=SAFE_OK; AVALANCHE_RISK | SETTLED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1545410 | Brondby | FC Copenhagen | OVER_2_5 | 0.797325 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.248; market_fit=SAFE_OK; LOW_CONVERSION | PENDING |
| CANDIDATE_V7_PRICE_DISCIPLINE | 2 | 1535208 | Gremio | Palestino | UNDER_3_5 | 0.8583 | FAILURE_MODE_AVALANCHE_RISK; FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.173; market_fit=SAFE_OK; AVALANCHE_RISK | SETTLED |

## No-Bet Modes
| experiment_id | record_status | reason_tags | source_file |
| --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH | NO_BET_RECORD | NO_BET; SOURCE_FILE_MISSING_OR_NOT_AVAILABLE | vsigma_today_candidate_v3_competition_top.csv |

## Pre-Lock Changes
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_status | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1545410 | Brondby | FC Copenhagen | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| OFFICIAL_BASELINE | 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| OFFICIAL_BASELINE | 1535208 | Gremio | Palestino | UNDER_3_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545410 | Brondby | FC Copenhagen | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535208 | Gremio | Palestino | UNDER_3_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V4_O25_FIREWALL | 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V4_O25_FIREWALL | 1535208 | Gremio | Palestino | UNDER_3_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V5_PLAYER_IMPACT | 1545410 | Brondby | FC Copenhagen | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V5_PLAYER_IMPACT | 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V5_PLAYER_IMPACT | 1535208 | Gremio | Palestino | UNDER_3_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V6_API_PREDICTIONS | 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V6_API_PREDICTIONS | 1535208 | Gremio | Palestino | UNDER_3_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1545410 | Brondby | FC Copenhagen | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535208 | Gremio | Palestino | UNDER_3_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |

## Result State
| experiment_id | fixture_id | market_primary | result_status | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1545410 | OVER_2_5 | PENDING | PENDING |  | PENDING |
| OFFICIAL_BASELINE | 1535302 | OVER_1_5 | RESULT_AVAILABLE | LOSS | -1.0 | SETTLED |
| OFFICIAL_BASELINE | 1535208 | UNDER_3_5 | RESULT_AVAILABLE | WIN | 0.36 | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545410 | OVER_2_5 | PENDING | PENDING |  | PENDING |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535302 | OVER_1_5 | RESULT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535208 | UNDER_3_5 | RESULT_AVAILABLE | WIN | 0.36 | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1545410 | OVER_1_5 | PENDING | PENDING |  | PENDING |
| CANDIDATE_V4_O25_FIREWALL | 1535302 | OVER_1_5 | RESULT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1535208 | UNDER_3_5 | RESULT_AVAILABLE | WIN | 0.36 | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1545410 | OVER_2_5 | PENDING | PENDING |  | PENDING |
| CANDIDATE_V5_PLAYER_IMPACT | 1535302 | OVER_1_5 | RESULT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1535208 | UNDER_3_5 | RESULT_AVAILABLE | WIN | 0.36 | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1535302 | OVER_1_5 | RESULT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1535208 | UNDER_3_5 | RESULT_AVAILABLE | WIN | 0.36 | SETTLED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1545410 | OVER_2_5 | PENDING | PENDING |  | PENDING |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535208 | UNDER_3_5 | RESULT_AVAILABLE | WIN | 0.36 | SETTLED |

## Freshness Warnings
| file_name | status | detail |
| --- | --- | --- |
| today_post_results_report.csv | WARNING_STALE_GLOBAL_FILE | snapshot context file not present yet |
