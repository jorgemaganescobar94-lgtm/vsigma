# vSIGMA API Calibration Rule Candidates - 2026-06-10

## Summary
- rows_reviewed: 77
- candidate_rows: 10
- block_rows: 12
- observe_rows: 55
- insufficient_sample_rows: 49
- rule_bucket_counts: RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=49; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=12; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=8; RULE_OBSERVE_ONLY_SEGMENT=5; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=2; RULE_NEUTRAL_OBSERVE_MORE=1
- rule_decision_counts: COLLECT_MORE_SAMPLE=49; WATCH_ONLY_COLLECT_TO_50_SAMPLE=10; OBSERVE_MORE_SEGMENT=5; BLOCK_ML_PROMOTION=4; BLOCK_BTTS_YES_PROMOTION=4; BLOCK_OVER_2_5_PROMOTION=4; OBSERVE_MORE_GLOBAL_MARKET=1
- future_rule_candidate_counts: NO_SAMPLE_TOO_SMALL=49; NO_BLOCKED_MARKET=12; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=10; NO_SEGMENT_SAMPLE_TOO_SMALL=5; NO_OBSERVE_MORE=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0002 | ALL=ALL | API_DNB | evaluated=40 | hit=52.5 | hit_or_void=77.5 | miss=22.5 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=77.5% and miss_rate=22.5% but sample=40 is below 50.
- API_CAL_RULE_0003 | ALL=ALL | API_DOUBLE_CHANCE | evaluated=40 | hit=77.5 | hit_or_void=77.5 | miss=22.5 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=77.5% but sample=40 is below 50.
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=40 | hit=65.0 | hit_or_void=65.0 | miss=35.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=65.0% but sample=40 is below 50.
- API_CAL_RULE_0016 | PREDICTED_SIDE=HOME | API_DNB | evaluated=24 | hit=54.2 | hit_or_void=75.0 | miss=25.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.0% and miss_rate=25.0% but sample=24 is below 50.
- API_CAL_RULE_0017 | PREDICTED_SIDE=HOME | API_DOUBLE_CHANCE | evaluated=24 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.0% but sample=24 is below 50.
- API_CAL_RULE_0021 | PREDICTED_SIDE=HOME | UNDER_3_5 | evaluated=24 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=75.0% but sample=24 is below 50.
- API_CAL_RULE_0030 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_DNB | evaluated=21 | hit=47.6 | hit_or_void=76.2 | miss=23.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.2% and miss_rate=23.8% but sample=21 is below 50.
- API_CAL_RULE_0031 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=21 | hit=76.2 | hit_or_void=76.2 | miss=23.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.2% but sample=21 is below 50.
- API_CAL_RULE_0072 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=21 | hit=47.6 | hit_or_void=76.2 | miss=23.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.2% and miss_rate=23.8% but sample=21 is below 50.
- API_CAL_RULE_0073 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=21 | hit=76.2 | hit_or_void=76.2 | miss=23.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.2% but sample=21 is below 50.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=40 | hit=52.5 | miss=47.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=40 | hit=45.0 | miss=55.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=45.0% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=40 | hit=45.0 | miss=55.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.0% is weak/negative in current calibration.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=24 | hit=54.2 | miss=45.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=54.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=24 | hit=33.3 | miss=66.7 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=33.3% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=24 | hit=37.5 | miss=62.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=37.5% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=21 | hit=47.6 | miss=52.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=47.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | BTTS_YES | evaluated=21 | hit=42.9 | miss=57.1 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=42.9% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_2_5 | evaluated=21 | hit=42.9 | miss=57.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=42.9% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=21 | hit=47.6 | miss=52.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=47.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=21 | hit=42.9 | miss=57.1 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=42.9% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=21 | hit=42.9 | miss=57.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=42.9% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
