# vSIGMA Immutable Ledger Daily Report - 2026-06-16

## Ledger Update Status
- Ledger CSV: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- JSONL event log: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.jsonl
- Official picks registered: 0
- Shadow picks registered: 0
- No-bet records: 7
- Pending records: 0
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
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V3_ODDS_DEPTH | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V4_O25_FIREWALL | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V5_PLAYER_IMPACT | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V6_API_PREDICTIONS | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 0 | 1 | 0 | 0 | 0.0 |
| OFFICIAL_BASELINE | 1 | 0 | 1 | 0 | 0 | 0.0 |

## Official Picks
_No rows._

## Shadow Picks
_No rows._

## No-Bet Modes
| experiment_id | record_status | reason_tags | source_file |
| --- | --- | --- | --- |
| OFFICIAL_BASELINE | NO_BET_RECORD | NO_BET; no competition top rows | vsigma_today_competition_top.csv |
| CANDIDATE_V2_SCHEDULE_ANOMALY | NO_BET_RECORD | NO_BET; no competition top rows | vsigma_today_candidate_v2_competition_top.csv |
| CANDIDATE_V3_ODDS_DEPTH | NO_BET_RECORD | NO_BET; SOURCE_FILE_MISSING_OR_NOT_AVAILABLE | vsigma_today_candidate_v3_competition_top.csv |
| CANDIDATE_V4_O25_FIREWALL | NO_BET_RECORD | NO_BET; no competition top rows | vsigma_today_candidate_v4_competition_top.csv |
| CANDIDATE_V5_PLAYER_IMPACT | NO_BET_RECORD | NO_BET; no competition top rows | vsigma_today_candidate_v5_competition_top.csv |
| CANDIDATE_V6_API_PREDICTIONS | NO_BET_RECORD | NO_BET; no competition top rows | vsigma_today_candidate_v6_competition_top.csv |
| CANDIDATE_V7_PRICE_DISCIPLINE | NO_BET_RECORD | NO_BET; no competition top rows | vsigma_today_candidate_v7_competition_top.csv |

## Pre-Lock Changes
_No rows._

## Result State
_No rows._

## Freshness Warnings
| file_name | status | detail |
| --- | --- | --- |
| vsigma_today_competition_shortlist.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_competition_top.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v2_competition_shortlist.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v2_competition_top.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v4_competition_shortlist.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v4_competition_top.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v5_competition_shortlist.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v5_competition_top.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v6_competition_shortlist.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v6_competition_top.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v7_competition_shortlist.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v7_competition_top.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_baseline_vs_candidate_v2.csv | EMPTY_UNEXPECTED | empty output was not expected for this report |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4.csv | EMPTY_UNEXPECTED | empty output was not expected for this report |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5.csv | EMPTY_UNEXPECTED | empty output was not expected for this report |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6.csv | EMPTY_UNEXPECTED | empty output was not expected for this report |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7.csv | EMPTY_UNEXPECTED | empty output was not expected for this report |
| vsigma_today_match_script_forecasts.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v2_match_script_forecasts.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_candidate_v4_match_script_forecasts.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
