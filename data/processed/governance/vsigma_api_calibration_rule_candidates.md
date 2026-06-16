# vSIGMA API Calibration Rule Candidates - 2026-06-16

## Summary
- rows_reviewed: 77
- candidate_rows: 17
- block_rows: 28
- observe_rows: 32
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=28; RULE_OBSERVE_ONLY_SEGMENT=22; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=9; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=6; RULE_NEUTRAL_OBSERVE_MORE=3; RULE_CANDIDATE_TOTAL_MARKET=2
- rule_decision_counts: OBSERVE_MORE_SEGMENT=22; WATCH_ONLY_COLLECT_TO_50_SAMPLE=15; BLOCK_OVER_2_5_PROMOTION=10; BLOCK_ML_PROMOTION=9; BLOCK_BTTS_YES_PROMOTION=9; COLLECT_MORE_SAMPLE=7; OBSERVE_MORE_GLOBAL_MARKET=3; FUTURE_RULE_REVIEW_ONLY=2
- future_rule_candidate_counts: NO_BLOCKED_MARKET=28; NO_SEGMENT_SAMPLE_TOO_SMALL=22; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=15; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=3; YES_REVIEW_ONLY=2
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=92 | hit=68.5 | hit_or_void=68.5 | miss=31.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=68.5% meets total-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=38 | hit=71.1 | hit_or_void=71.1 | miss=28.9 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=71.1% but sample=38 is below 50.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=54 | hit=66.7 | hit_or_void=66.7 | miss=33.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=66.7% meets total-market threshold.
- API_CAL_RULE_0023 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=38 | hit=55.3 | hit_or_void=81.6 | miss=18.4 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=81.6% and miss_rate=18.4% but sample=38 is below 50.
- API_CAL_RULE_0024 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=38 | hit=81.6 | hit_or_void=81.6 | miss=18.4 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=81.6% but sample=38 is below 50.
- API_CAL_RULE_0026 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=38 | hit=73.7 | hit_or_void=73.7 | miss=26.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=73.7% but sample=38 is below 50.
- API_CAL_RULE_0028 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | UNDER_3_5 | evaluated=38 | hit=71.1 | hit_or_void=71.1 | miss=28.9 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=71.1% but sample=38 is below 50.
- API_CAL_RULE_0042 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=29 | hit=72.4 | hit_or_void=72.4 | miss=27.6 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=72.4% but sample=29 is below 50.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=30 | hit=66.7 | hit_or_void=66.7 | miss=33.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=66.7% but sample=30 is below 50.
- API_CAL_RULE_0058 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=27 | hit=63.0 | hit_or_void=85.2 | miss=14.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=85.2% and miss_rate=14.8% but sample=27 is below 50.
- API_CAL_RULE_0059 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=27 | hit=85.2 | hit_or_void=85.2 | miss=14.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=85.2% but sample=27 is below 50.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=27 | hit=74.1 | hit_or_void=74.1 | miss=25.9 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.1% but sample=27 is below 50.
- API_CAL_RULE_0063 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=27 | hit=74.1 | hit_or_void=74.1 | miss=25.9 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=74.1% but sample=27 is below 50.
- API_CAL_RULE_0065 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=38 | hit=55.3 | hit_or_void=81.6 | miss=18.4 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=81.6% and miss_rate=18.4% but sample=38 is below 50.
- API_CAL_RULE_0066 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=38 | hit=81.6 | hit_or_void=81.6 | miss=18.4 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=81.6% but sample=38 is below 50.
- API_CAL_RULE_0068 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=38 | hit=73.7 | hit_or_void=73.7 | miss=26.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=73.7% but sample=38 is below 50.
- API_CAL_RULE_0070 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=38 | hit=71.1 | hit_or_void=71.1 | miss=28.9 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=71.1% but sample=38 is below 50.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=92 | hit=46.7 | miss=53.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=46.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=92 | hit=46.7 | miss=53.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=46.7% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=92 | hit=47.8 | miss=52.2 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=47.8% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=38 | hit=44.7 | miss=55.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=44.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0013 | PREDICTED_SIDE=AWAY | OVER_2_5 | evaluated=38 | hit=52.6 | miss=47.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=52.6% is weak/negative in current calibration.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=54 | hit=48.1 | miss=51.9 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=48.1% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=54 | hit=40.7 | miss=59.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=40.7% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=54 | hit=44.4 | miss=55.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=44.4% is weak/negative in current calibration.
- API_CAL_RULE_0022 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=38 | hit=55.3 | miss=44.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0025 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=38 | hit=44.7 | miss=55.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=44.7% is weak/negative in current calibration.
- API_CAL_RULE_0027 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=38 | hit=44.7 | miss=55.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=44.7% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=54 | hit=40.7 | miss=59.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=40.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | BTTS_YES | evaluated=54 | hit=48.1 | miss=51.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.1% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_2_5 | evaluated=54 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0036 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=29 | hit=27.6 | miss=72.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=27.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0039 | SCORE_BUCKET=SCORE_55_69 | BTTS_YES | evaluated=29 | hit=41.4 | miss=58.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=41.4% is weak/negative in current calibration.
- API_CAL_RULE_0041 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=29 | hit=44.8 | miss=55.2 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=44.8% is weak/negative in current calibration.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=30 | hit=53.3 | miss=46.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=53.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0046 | SCORE_BUCKET=SCORE_70_79 | BTTS_YES | evaluated=30 | hit=53.3 | miss=46.7 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.3% is weak/negative in current calibration.
- API_CAL_RULE_0048 | SCORE_BUCKET=SCORE_70_79 | OVER_2_5 | evaluated=30 | hit=53.3 | miss=46.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.3% is weak/negative in current calibration.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=27 | hit=37.0 | miss=63.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=37.0% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=27 | hit=40.7 | miss=59.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=40.7% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=38 | hit=55.3 | miss=44.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0067 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=38 | hit=44.7 | miss=55.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=44.7% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=38 | hit=44.7 | miss=55.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=44.7% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=54 | hit=40.7 | miss=59.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=40.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=54 | hit=48.1 | miss=51.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.1% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=54 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
