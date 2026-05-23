# vSIGMA Immutable Ledger Daily Report - 2026-05-23

## Ledger Update Status
- Ledger CSV: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- JSONL event log: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.jsonl
- Official picks registered: 2
- Shadow picks registered: 10
- No-bet records: 1
- Pending records: 12
- Settled records: 0
- Daily winner: NO_SETTLED_RESULTS

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
| CANDIDATE_V2_SCHEDULE_ANOMALY | 2 | 2 | 0 | 2 | 0 | 0.0 |
| CANDIDATE_V3_ODDS_DEPTH | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V4_O25_FIREWALL | 2 | 2 | 0 | 2 | 0 | 0.0 |
| CANDIDATE_V5_PLAYER_IMPACT | 2 | 2 | 0 | 2 | 0 | 0.0 |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 2 | 0 | 2 | 0 | 0.0 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 2 | 2 | 0 | 2 | 0 | 0.0 |
| OFFICIAL_BASELINE | 2 | 2 | 0 | 2 | 0 | 0.0 |

## Official Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1 | 1504822 | Kashima | FC Tokyo | OVER_1_5 | 0.7902 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.156; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| OFFICIAL_BASELINE | 2 | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | 0.7829 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.149; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |

## Shadow Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 1504822 | Kashima | FC Tokyo | OVER_1_5 | 0.7912 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.157; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 2 | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | 0.7786 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.144; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V4_O25_FIREWALL | 1 | 1504822 | Kashima | FC Tokyo | OVER_1_5 | 0.7912 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.157; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V4_O25_FIREWALL | 2 | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | 0.7786 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.144; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1 | 1504822 | Kashima | FC Tokyo | OVER_1_5 | 0.7912 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.157; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 2 | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | 0.7786 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.144; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 1 | 1504822 | Kashima | FC Tokyo | OVER_1_5 | 0.7912 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.157; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | 0.7786 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.144; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1504822 | Kashima | FC Tokyo | OVER_1_5 | 0.7912 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.157; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 2 | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | 0.7786 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.144; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |

## No-Bet Modes
| experiment_id | record_status | reason_tags | source_file |
| --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH | NO_BET_RECORD | NO_BET; SOURCE_FILE_MISSING_OR_NOT_AVAILABLE | vsigma_today_candidate_v3_competition_top.csv |

## Pre-Lock Changes
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_status | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1504822 | Kashima | FC Tokyo | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| OFFICIAL_BASELINE | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1504822 | Kashima | FC Tokyo | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V4_O25_FIREWALL | 1504822 | Kashima | FC Tokyo | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V4_O25_FIREWALL | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V5_PLAYER_IMPACT | 1504822 | Kashima | FC Tokyo | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V5_PLAYER_IMPACT | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V6_API_PREDICTIONS | 1504822 | Kashima | FC Tokyo | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V6_API_PREDICTIONS | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1504822 | Kashima | FC Tokyo | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |

## Result State
| experiment_id | fixture_id | market_primary | result_status | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1504822 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| OFFICIAL_BASELINE | 1494182 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1504822 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1494182 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V4_O25_FIREWALL | 1504822 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V4_O25_FIREWALL | 1494182 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1504822 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1494182 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 1504822 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 1494182 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1504822 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1494182 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |

## Freshness Warnings
| file_name | status | detail |
| --- | --- | --- |
| vsigma_today_candidate_v7_competition_top.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_prelock_competition_top.csv | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-22'] does not match 2026-05-23 |
| vsigma_today_prelock_comparison.csv | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-22'] does not match 2026-05-23 |
| today_post_results_report.csv | WARNING_STALE_GLOBAL_FILE | snapshot context file not present yet |
