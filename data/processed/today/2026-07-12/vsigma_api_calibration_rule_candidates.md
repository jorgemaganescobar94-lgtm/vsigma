# vSIGMA API Calibration Rule Candidates - 2026-07-12

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
- API_CAL_RULE_0002 | ALL=ALL | API_DNB | evaluated=291 | hit=54.6 | hit_or_void=75.3 | miss=24.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.3% and miss_rate=24.7% meet protected-market threshold.
- API_CAL_RULE_0003 | ALL=ALL | API_DOUBLE_CHANCE | evaluated=291 | hit=75.3 | hit_or_void=75.3 | miss=24.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.3% meets protected-market threshold.
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=292 | hit=74.3 | hit_or_void=74.3 | miss=25.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.3% meets total-market threshold.
- API_CAL_RULE_0009 | PREDICTED_SIDE=AWAY | API_DNB | evaluated=138 | hit=53.6 | hit_or_void=75.4 | miss=24.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.4% and miss_rate=24.6% meet protected-market threshold.
- API_CAL_RULE_0010 | PREDICTED_SIDE=AWAY | API_DOUBLE_CHANCE | evaluated=138 | hit=75.4 | hit_or_void=75.4 | miss=24.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.4% meets protected-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=138 | hit=77.5 | hit_or_void=77.5 | miss=22.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.5% meets total-market threshold.
- API_CAL_RULE_0016 | PREDICTED_SIDE=HOME | API_DNB | evaluated=153 | hit=55.6 | hit_or_void=75.2 | miss=24.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.2% and miss_rate=24.8% meet protected-market threshold.
- API_CAL_RULE_0017 | PREDICTED_SIDE=HOME | API_DOUBLE_CHANCE | evaluated=153 | hit=75.2 | hit_or_void=75.2 | miss=24.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.2% meets protected-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=153 | hit=71.9 | hit_or_void=71.9 | miss=28.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=71.9% meets total-market threshold.
- API_CAL_RULE_0030 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=130 | hit=60.8 | hit_or_void=79.2 | miss=20.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=79.2% and miss_rate=20.8% meet protected-market threshold.
- API_CAL_RULE_0031 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=130 | hit=79.2 | hit_or_void=79.2 | miss=20.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=79.2% meets protected-market threshold.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=131 | hit=72.5 | hit_or_void=72.5 | miss=27.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.5% meets total-market threshold.
- API_CAL_RULE_0040 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=161 | hit=75.8 | hit_or_void=75.8 | miss=24.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.8% meets total-market threshold.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_55_69 | OVER_1_5 | evaluated=74 | hit=68.9 | hit_or_void=68.9 | miss=31.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=68.9% meets total-market threshold.
- API_CAL_RULE_0049 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=74 | hit=71.6 | hit_or_void=71.6 | miss=28.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=71.6% meets total-market threshold.
- API_CAL_RULE_0051 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=100 | hit=56.0 | hit_or_void=75.0 | miss=25.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.0% and miss_rate=25.0% meet protected-market threshold.
- API_CAL_RULE_0052 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=100 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.0% meets protected-market threshold.
- API_CAL_RULE_0054 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=100 | hit=79.0 | hit_or_void=79.0 | miss=21.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=79.0% meets total-market threshold.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_80_89 | OVER_1_5 | evaluated=30 | hit=66.7 | hit_or_void=66.7 | miss=33.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=66.7% but sample=30 is below 50.
- API_CAL_RULE_0065 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=88 | hit=69.3 | hit_or_void=86.4 | miss=13.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=86.4% and miss_rate=13.6% meet protected-market threshold.
- API_CAL_RULE_0066 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=88 | hit=86.4 | hit_or_void=86.4 | miss=13.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=86.4% meets protected-market threshold.
- API_CAL_RULE_0068 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=88 | hit=76.1 | hit_or_void=76.1 | miss=23.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.1% meets total-market threshold.
- API_CAL_RULE_0070 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=88 | hit=70.5 | hit_or_void=70.5 | miss=29.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=70.5% meets total-market threshold.
- API_CAL_RULE_0072 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=130 | hit=60.8 | hit_or_void=79.2 | miss=20.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=79.2% and miss_rate=20.8% meet protected-market threshold.
- API_CAL_RULE_0073 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=130 | hit=79.2 | hit_or_void=79.2 | miss=20.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=79.2% meets protected-market threshold.
- API_CAL_RULE_0075 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=131 | hit=72.5 | hit_or_void=72.5 | miss=27.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.5% meets total-market threshold.
- API_CAL_RULE_0082 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=161 | hit=75.8 | hit_or_void=75.8 | miss=24.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.8% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=291 | hit=54.6 | miss=45.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=54.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=292 | hit=54.1 | miss=45.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=54.1% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=138 | hit=53.6 | miss=46.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=53.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=153 | hit=55.6 | miss=44.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=153 | hit=49.7 | miss=50.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=49.7% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=153 | hit=51.6 | miss=48.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=51.6% is weak/negative in current calibration.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=131 | hit=50.4 | miss=49.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.4% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=131 | hit=53.4 | miss=46.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.4% is weak/negative in current calibration.
- API_CAL_RULE_0036 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=161 | hit=49.7 | miss=50.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=49.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=74 | hit=39.2 | miss=60.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=39.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0048 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=74 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0050 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=100 | hit=56.0 | miss=44.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=56.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0057 | SCORE_BUCKET=SCORE_80_89 | API_1X2 | evaluated=29 | hit=44.8 | miss=55.2 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=44.8% is below the 60% minimum for any ML review.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_80_89 | BTTS_YES | evaluated=30 | hit=50.0 | miss=50.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_80_89 | OVER_2_5 | evaluated=30 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0067 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=88 | hit=51.1 | miss=48.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=51.1% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=88 | hit=54.5 | miss=45.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=54.5% is weak/negative in current calibration.
- API_CAL_RULE_0074 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=131 | hit=50.4 | miss=49.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.4% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=131 | hit=53.4 | miss=46.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.4% is weak/negative in current calibration.
- API_CAL_RULE_0078 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=161 | hit=49.7 | miss=50.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=49.7% is below the 60% minimum for any ML review.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
