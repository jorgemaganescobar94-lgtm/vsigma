# vSIGMA Immutable Ledger Daily Report - 2026-05-20

## Ledger Update Status
- Ledger CSV: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- JSONL event log: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.jsonl
- Official picks registered: 3
- Shadow picks registered: 10
- No-bet records: 1
- Pending records: 8
- Settled records: 5
- Daily winner: TIE

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
| CANDIDATE_V2_SCHEDULE_ANOMALY | 2 | 2 | 0 | 1 | 1 | 0.6 |
| CANDIDATE_V3_ODDS_DEPTH | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V4_O25_FIREWALL | 2 | 2 | 0 | 1 | 1 | 0.6 |
| CANDIDATE_V5_PLAYER_IMPACT | 2 | 2 | 0 | 1 | 1 | 0.6 |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 2 | 0 | 1 | 1 | 0.6 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 2 | 2 | 0 | 2 | 0 | 0.0 |
| OFFICIAL_BASELINE | 3 | 3 | 0 | 2 | 1 | 0.6 |

## Official Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1 | 1535312 | Santa Fe | Platense | OVER_1_5 | 0.80046 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.243; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| OFFICIAL_BASELINE | 2 | 1494229 | Gais | Hammarby FF | OVER_2_5 | 0.800225 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.245; market_fit=SAFE_OK; LOW_CONVERSION | PENDING |
| OFFICIAL_BASELINE | 1 | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | 0.82976 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.157; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |

## Shadow Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 1535312 | Santa Fe | Platense | OVER_1_5 | 0.80346 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.246; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | 0.82476 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.152; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V4_O25_FIREWALL | 1 | 1535312 | Santa Fe | Platense | OVER_1_5 | 0.80346 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.246; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1 | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | 0.82476 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.152; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V5_PLAYER_IMPACT | 1 | 1535312 | Santa Fe | Platense | OVER_1_5 | 0.80346 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.246; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1 | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | 0.82476 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.152; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V6_API_PREDICTIONS | 1 | 1535312 | Santa Fe | Platense | OVER_1_5 | 0.80346 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.246; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1 | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | 0.82476 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.152; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1535312 | Santa Fe | Platense | OVER_1_5 | 0.80346 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.246; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | 0.82476 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.152; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |

## No-Bet Modes
| experiment_id | record_status | reason_tags | source_file |
| --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH | NO_BET_RECORD | NO_BET; SOURCE_FILE_MISSING_OR_NOT_AVAILABLE | vsigma_today_candidate_v3_competition_top.csv |

## Pre-Lock Changes
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_status | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1535312 | Santa Fe | Platense | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_CONFIRMED | lineups confirmed |
| OFFICIAL_BASELINE | 1494229 | Gais | Hammarby FF | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| OFFICIAL_BASELINE | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535312 | Santa Fe | Platense | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_CONFIRMED | lineups confirmed |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V4_O25_FIREWALL | 1535312 | Santa Fe | Platense | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_CONFIRMED | lineups confirmed |
| CANDIDATE_V4_O25_FIREWALL | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V5_PLAYER_IMPACT | 1535312 | Santa Fe | Platense | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_CONFIRMED | lineups confirmed |
| CANDIDATE_V5_PLAYER_IMPACT | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V6_API_PREDICTIONS | 1535312 | Santa Fe | Platense | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_CONFIRMED | lineups confirmed |
| CANDIDATE_V6_API_PREDICTIONS | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535312 | Santa Fe | Platense | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_CONFIRMED | lineups confirmed |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | WAITING_FOR_PRELOCK | fixture is outside requested pre-lock window |

## Result State
| experiment_id | fixture_id | market_primary | result_status | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1535312 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.6 | SETTLED |
| OFFICIAL_BASELINE | 1494229 | OVER_2_5 | PENDING | PENDING |  | PENDING |
| OFFICIAL_BASELINE | 1544596 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535312 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.6 | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544596 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V4_O25_FIREWALL | 1535312 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.6 | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1544596 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V5_PLAYER_IMPACT | 1535312 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.6 | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1544596 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V6_API_PREDICTIONS | 1535312 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.6 | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1544596 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535312 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1544596 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |

## Freshness Warnings
_No rows._
