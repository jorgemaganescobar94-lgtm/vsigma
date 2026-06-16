# vSIGMA API Calibration Rule Candidates - 2026-06-16

## Summary
- rows_reviewed: 77
- candidate_rows: 17
- block_rows: 24
- observe_rows: 36
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_OBSERVE_ONLY_SEGMENT=26; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=24; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=10; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=6; RULE_NEUTRAL_OBSERVE_MORE=3; RULE_CANDIDATE_TOTAL_MARKET=1
- rule_decision_counts: OBSERVE_MORE_SEGMENT=26; WATCH_ONLY_COLLECT_TO_50_SAMPLE=16; BLOCK_ML_PROMOTION=8; BLOCK_BTTS_YES_PROMOTION=8; BLOCK_OVER_2_5_PROMOTION=8; COLLECT_MORE_SAMPLE=7; OBSERVE_MORE_GLOBAL_MARKET=3; FUTURE_RULE_REVIEW_ONLY=1
- future_rule_candidate_counts: NO_SEGMENT_SAMPLE_TOO_SMALL=26; NO_BLOCKED_MARKET=24; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=16; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=3; YES_REVIEW_ONLY=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=81 | hit=70.4 | hit_or_void=70.4 | miss=29.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=70.4% meets total-market threshold.
- API_CAL_RULE_0009 | PREDICTED_SIDE=AWAY | API_DNB | evaluated=33 | hit=48.5 | hit_or_void=75.8 | miss=24.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.8% and miss_rate=24.2% but sample=33 is below 50.
- API_CAL_RULE_0010 | PREDICTED_SIDE=AWAY | API_DOUBLE_CHANCE | evaluated=33 | hit=75.8 | hit_or_void=75.8 | miss=24.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.8% but sample=33 is below 50.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=33 | hit=78.8 | hit_or_void=78.8 | miss=21.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=78.8% but sample=33 is below 50.
- API_CAL_RULE_0023 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=31 | hit=58.1 | hit_or_void=83.9 | miss=16.1 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=83.9% and miss_rate=16.1% but sample=31 is below 50.
- API_CAL_RULE_0024 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=31 | hit=83.9 | hit_or_void=83.9 | miss=16.1 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=83.9% but sample=31 is below 50.
- API_CAL_RULE_0026 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=31 | hit=80.6 | hit_or_void=80.6 | miss=19.4 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=80.6% but sample=31 is below 50.
- API_CAL_RULE_0042 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=28 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=75.0% but sample=28 is below 50.
- API_CAL_RULE_0044 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=25 | hit=60.0 | hit_or_void=76.0 | miss=24.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.0% and miss_rate=24.0% but sample=25 is below 50.
- API_CAL_RULE_0045 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=25 | hit=76.0 | hit_or_void=76.0 | miss=24.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.0% but sample=25 is below 50.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=25 | hit=72.0 | hit_or_void=72.0 | miss=28.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.0% but sample=25 is below 50.
- API_CAL_RULE_0058 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=22 | hit=63.6 | hit_or_void=86.4 | miss=13.6 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=86.4% and miss_rate=13.6% but sample=22 is below 50.
- API_CAL_RULE_0059 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=22 | hit=86.4 | hit_or_void=86.4 | miss=13.6 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=86.4% but sample=22 is below 50.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=22 | hit=77.3 | hit_or_void=77.3 | miss=22.7 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.3% but sample=22 is below 50.
- API_CAL_RULE_0065 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=31 | hit=58.1 | hit_or_void=83.9 | miss=16.1 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=83.9% and miss_rate=16.1% but sample=31 is below 50.
- API_CAL_RULE_0066 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=31 | hit=83.9 | hit_or_void=83.9 | miss=16.1 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=83.9% but sample=31 is below 50.
- API_CAL_RULE_0068 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=31 | hit=80.6 | hit_or_void=80.6 | miss=19.4 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=80.6% but sample=31 is below 50.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=81 | hit=46.9 | miss=53.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=46.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=81 | hit=49.4 | miss=50.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=49.4% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=81 | hit=50.6 | miss=49.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.6% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=33 | hit=48.5 | miss=51.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=48.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=48 | hit=45.8 | miss=54.2 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=45.8% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=48 | hit=41.7 | miss=58.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=41.7% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=48 | hit=45.8 | miss=54.2 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.8% is weak/negative in current calibration.
- API_CAL_RULE_0022 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=31 | hit=58.1 | miss=41.9 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=58.1% is below the 60% minimum for any ML review.
- API_CAL_RULE_0025 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=31 | hit=51.6 | miss=48.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=51.6% is weak/negative in current calibration.
- API_CAL_RULE_0027 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=31 | hit=51.6 | miss=48.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=51.6% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=50 | hit=40.0 | miss=60.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=40.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | BTTS_YES | evaluated=50 | hit=48.0 | miss=52.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.0% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_2_5 | evaluated=50 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0036 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=28 | hit=25.0 | miss=75.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=25.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0039 | SCORE_BUCKET=SCORE_55_69 | BTTS_YES | evaluated=28 | hit=39.3 | miss=60.7 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=39.3% is weak/negative in current calibration.
- API_CAL_RULE_0041 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=28 | hit=42.9 | miss=57.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=42.9% is weak/negative in current calibration.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=22 | hit=40.9 | miss=59.1 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=40.9% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=22 | hit=45.5 | miss=54.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.5% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=31 | hit=58.1 | miss=41.9 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=58.1% is below the 60% minimum for any ML review.
- API_CAL_RULE_0067 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=31 | hit=51.6 | miss=48.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=51.6% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=31 | hit=51.6 | miss=48.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=51.6% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=50 | hit=40.0 | miss=60.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=40.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=50 | hit=48.0 | miss=52.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.0% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=50 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
