# vSIGMA API Calibration Rule Candidates - 2026-06-09

## Summary
- rows_reviewed: 77
- candidate_rows: 4
- block_rows: 3
- observe_rows: 70
- insufficient_sample_rows: 70
- rule_bucket_counts: RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=70; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=3; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=2; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=2
- rule_decision_counts: COLLECT_MORE_SAMPLE=70; WATCH_ONLY_COLLECT_TO_50_SAMPLE=4; BLOCK_ML_PROMOTION=1; BLOCK_BTTS_YES_PROMOTION=1; BLOCK_OVER_2_5_PROMOTION=1
- future_rule_candidate_counts: NO_SAMPLE_TOO_SMALL=70; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=4; NO_BLOCKED_MARKET=3
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0002 | ALL=ALL | API_DNB | evaluated=27 | hit=55.6 | hit_or_void=77.8 | miss=22.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=77.8% and miss_rate=22.2% but sample=27 is below 50.
- API_CAL_RULE_0003 | ALL=ALL | API_DOUBLE_CHANCE | evaluated=27 | hit=77.8 | hit_or_void=77.8 | miss=22.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=77.8% but sample=27 is below 50.
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=27 | hit=66.7 | hit_or_void=66.7 | miss=33.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=66.7% but sample=27 is below 50.
- API_CAL_RULE_0007 | ALL=ALL | UNDER_3_5 | evaluated=27 | hit=74.1 | hit_or_void=74.1 | miss=25.9 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=74.1% but sample=27 is below 50.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=27 | hit=55.6 | miss=44.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=27 | hit=48.1 | miss=51.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.1% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=27 | hit=40.7 | miss=59.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=40.7% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
