# vSIGMA API Calibration Rule Candidates - 2026-07-08

## Summary
- rows_reviewed: 84
- candidate_rows: 27
- block_rows: 20
- observe_rows: 37
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_OBSERVE_ONLY_SEGMENT=28; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=20; RULE_CANDIDATE_PROTECTED_MARKET=14; RULE_CANDIDATE_TOTAL_MARKET=12; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_NEUTRAL_OBSERVE_MORE=2; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=1
- rule_decision_counts: OBSERVE_MORE_SEGMENT=28; FUTURE_RULE_REVIEW_ONLY=26; BLOCK_ML_PROMOTION=8; COLLECT_MORE_SAMPLE=7; BLOCK_BTTS_YES_PROMOTION=6; BLOCK_OVER_2_5_PROMOTION=6; OBSERVE_MORE_GLOBAL_MARKET=2; WATCH_ONLY_COLLECT_TO_50_SAMPLE=1
- future_rule_candidate_counts: NO_SEGMENT_SAMPLE_TOO_SMALL=28; YES_REVIEW_ONLY=26; NO_BLOCKED_MARKET=20; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=2; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=84
- pick_permission_counts: NO_PICK_PERMISSION=84
- stake_permission_counts: NO_STAKE_PERMISSION=84
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0002 | ALL=ALL | API_DNB | evaluated=289 | hit=54.3 | hit_or_void=75.1 | miss=24.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.1% and miss_rate=24.9% meet protected-market threshold.
- API_CAL_RULE_0003 | ALL=ALL | API_DOUBLE_CHANCE | evaluated=289 | hit=75.1 | hit_or_void=75.1 | miss=24.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.1% meets protected-market threshold.
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=290 | hit=74.1 | hit_or_void=74.1 | miss=25.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.1% meets total-market threshold.
- API_CAL_RULE_0009 | PREDICTED_SIDE=AWAY | API_DNB | evaluated=136 | hit=52.9 | hit_or_void=75.0 | miss=25.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.0% and miss_rate=25.0% meet protected-market threshold.
- API_CAL_RULE_0010 | PREDICTED_SIDE=AWAY | API_DOUBLE_CHANCE | evaluated=136 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.0% meets protected-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=136 | hit=77.2 | hit_or_void=77.2 | miss=22.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.2% meets total-market threshold.
- API_CAL_RULE_0016 | PREDICTED_SIDE=HOME | API_DNB | evaluated=153 | hit=55.6 | hit_or_void=75.2 | miss=24.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.2% and miss_rate=24.8% meet protected-market threshold.
- API_CAL_RULE_0017 | PREDICTED_SIDE=HOME | API_DOUBLE_CHANCE | evaluated=153 | hit=75.2 | hit_or_void=75.2 | miss=24.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.2% meets protected-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=153 | hit=71.9 | hit_or_void=71.9 | miss=28.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=71.9% meets total-market threshold.
- API_CAL_RULE_0030 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=128 | hit=60.2 | hit_or_void=78.9 | miss=21.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=78.9% and miss_rate=21.1% meet protected-market threshold.
- API_CAL_RULE_0031 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=128 | hit=78.9 | hit_or_void=78.9 | miss=21.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=78.9% meets protected-market threshold.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=129 | hit=72.1 | hit_or_void=72.1 | miss=27.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.1% meets total-market threshold.
- API_CAL_RULE_0040 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=161 | hit=75.8 | hit_or_void=75.8 | miss=24.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.8% meets total-market threshold.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_55_69 | OVER_1_5 | evaluated=74 | hit=68.9 | hit_or_void=68.9 | miss=31.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=68.9% meets total-market threshold.
- API_CAL_RULE_0049 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=74 | hit=71.6 | hit_or_void=71.6 | miss=28.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=71.6% meets total-market threshold.
- API_CAL_RULE_0051 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=100 | hit=56.0 | hit_or_void=75.0 | miss=25.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.0% and miss_rate=25.0% meet protected-market threshold.
- API_CAL_RULE_0052 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=100 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.0% meets protected-market threshold.
- API_CAL_RULE_0054 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=100 | hit=79.0 | hit_or_void=79.0 | miss=21.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=79.0% meets total-market threshold.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_80_89 | OVER_1_5 | evaluated=30 | hit=66.7 | hit_or_void=66.7 | miss=33.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=66.7% but sample=30 is below 50.
- API_CAL_RULE_0065 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=86 | hit=68.6 | hit_or_void=86.0 | miss=14.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=86.0% and miss_rate=14.0% meet protected-market threshold.
- API_CAL_RULE_0066 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=86 | hit=86.0 | hit_or_void=86.0 | miss=14.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=86.0% meets protected-market threshold.
- API_CAL_RULE_0068 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=86 | hit=75.6 | hit_or_void=75.6 | miss=24.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.6% meets total-market threshold.
- API_CAL_RULE_0070 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=86 | hit=70.9 | hit_or_void=70.9 | miss=29.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=70.9% meets total-market threshold.
- API_CAL_RULE_0072 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=128 | hit=60.2 | hit_or_void=78.9 | miss=21.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=78.9% and miss_rate=21.1% meet protected-market threshold.
- API_CAL_RULE_0073 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=128 | hit=78.9 | hit_or_void=78.9 | miss=21.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=78.9% meets protected-market threshold.
- API_CAL_RULE_0075 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=129 | hit=72.1 | hit_or_void=72.1 | miss=27.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.1% meets total-market threshold.
- API_CAL_RULE_0082 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=161 | hit=75.8 | hit_or_void=75.8 | miss=24.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.8% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=289 | hit=54.3 | miss=45.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=54.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=290 | hit=54.1 | miss=45.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=54.1% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=136 | hit=52.9 | miss=47.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=153 | hit=55.6 | miss=44.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=153 | hit=49.7 | miss=50.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=49.7% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=153 | hit=51.6 | miss=48.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=51.6% is weak/negative in current calibration.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=129 | hit=50.4 | miss=49.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.4% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=129 | hit=52.7 | miss=47.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=52.7% is weak/negative in current calibration.
- API_CAL_RULE_0036 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=161 | hit=49.7 | miss=50.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=49.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=74 | hit=39.2 | miss=60.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=39.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0048 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=74 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0050 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=100 | hit=56.0 | miss=44.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=56.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0057 | SCORE_BUCKET=SCORE_80_89 | API_1X2 | evaluated=29 | hit=44.8 | miss=55.2 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=44.8% is below the 60% minimum for any ML review.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_80_89 | BTTS_YES | evaluated=30 | hit=50.0 | miss=50.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_80_89 | OVER_2_5 | evaluated=30 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0067 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=86 | hit=51.2 | miss=48.8 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=51.2% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=86 | hit=53.5 | miss=46.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.5% is weak/negative in current calibration.
- API_CAL_RULE_0074 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=129 | hit=50.4 | miss=49.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.4% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=129 | hit=52.7 | miss=47.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=52.7% is weak/negative in current calibration.
- API_CAL_RULE_0078 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=161 | hit=49.7 | miss=50.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=49.7% is below the 60% minimum for any ML review.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
