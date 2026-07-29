# vSIGMA API Calibration Rule Candidates - 2026-07-29

## Summary
- rows_reviewed: 84
- candidate_rows: 26
- block_rows: 23
- observe_rows: 35
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_OBSERVE_ONLY_SEGMENT=26; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=23; RULE_CANDIDATE_PROTECTED_MARKET=14; RULE_CANDIDATE_TOTAL_MARKET=11; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_NEUTRAL_OBSERVE_MORE=2; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=1
- rule_decision_counts: OBSERVE_MORE_SEGMENT=26; FUTURE_RULE_REVIEW_ONLY=25; BLOCK_ML_PROMOTION=10; BLOCK_BTTS_YES_PROMOTION=7; COLLECT_MORE_SAMPLE=7; BLOCK_OVER_2_5_PROMOTION=6; OBSERVE_MORE_GLOBAL_MARKET=2; WATCH_ONLY_COLLECT_TO_50_SAMPLE=1
- future_rule_candidate_counts: NO_SEGMENT_SAMPLE_TOO_SMALL=26; YES_REVIEW_ONLY=25; NO_BLOCKED_MARKET=23; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=2; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=84
- pick_permission_counts: NO_PICK_PERMISSION=84
- stake_permission_counts: NO_STAKE_PERMISSION=84
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0002 | ALL=ALL | API_DNB | evaluated=321 | hit=55.5 | hit_or_void=76.3 | miss=23.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.3% and miss_rate=23.7% meet protected-market threshold.
- API_CAL_RULE_0003 | ALL=ALL | API_DOUBLE_CHANCE | evaluated=321 | hit=76.3 | hit_or_void=76.3 | miss=23.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.3% meets protected-market threshold.
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=322 | hit=75.5 | hit_or_void=75.5 | miss=24.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.5% meets total-market threshold.
- API_CAL_RULE_0009 | PREDICTED_SIDE=AWAY | API_DNB | evaluated=159 | hit=53.5 | hit_or_void=76.1 | miss=23.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.1% and miss_rate=23.9% meet protected-market threshold.
- API_CAL_RULE_0010 | PREDICTED_SIDE=AWAY | API_DOUBLE_CHANCE | evaluated=159 | hit=76.1 | hit_or_void=76.1 | miss=23.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.1% meets protected-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=159 | hit=80.5 | hit_or_void=80.5 | miss=19.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=80.5% meets total-market threshold.
- API_CAL_RULE_0016 | PREDICTED_SIDE=HOME | API_DNB | evaluated=162 | hit=57.4 | hit_or_void=76.5 | miss=23.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.5% and miss_rate=23.5% meet protected-market threshold.
- API_CAL_RULE_0017 | PREDICTED_SIDE=HOME | API_DOUBLE_CHANCE | evaluated=162 | hit=76.5 | hit_or_void=76.5 | miss=23.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.5% meets protected-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=162 | hit=71.0 | hit_or_void=71.0 | miss=29.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=71.0% meets total-market threshold.
- API_CAL_RULE_0030 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=153 | hit=59.5 | hit_or_void=79.7 | miss=20.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=79.7% and miss_rate=20.3% meet protected-market threshold.
- API_CAL_RULE_0031 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=153 | hit=79.7 | hit_or_void=79.7 | miss=20.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=79.7% meets protected-market threshold.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=154 | hit=74.0 | hit_or_void=74.0 | miss=26.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.0% meets total-market threshold.
- API_CAL_RULE_0040 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=168 | hit=76.8 | hit_or_void=76.8 | miss=23.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.8% meets total-market threshold.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_55_69 | OVER_1_5 | evaluated=78 | hit=70.5 | hit_or_void=70.5 | miss=29.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=70.5% meets total-market threshold.
- API_CAL_RULE_0051 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=103 | hit=57.3 | hit_or_void=75.7 | miss=24.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.7% and miss_rate=24.3% meet protected-market threshold.
- API_CAL_RULE_0052 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=103 | hit=75.7 | hit_or_void=75.7 | miss=24.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.7% meets protected-market threshold.
- API_CAL_RULE_0054 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=103 | hit=79.6 | hit_or_void=79.6 | miss=20.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=79.6% meets total-market threshold.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_80_89 | OVER_1_5 | evaluated=30 | hit=66.7 | hit_or_void=66.7 | miss=33.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=66.7% but sample=30 is below 50.
- API_CAL_RULE_0065 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=111 | hit=65.8 | hit_or_void=85.6 | miss=14.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=85.6% and miss_rate=14.4% meet protected-market threshold.
- API_CAL_RULE_0066 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=111 | hit=85.6 | hit_or_void=85.6 | miss=14.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=85.6% meets protected-market threshold.
- API_CAL_RULE_0068 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=111 | hit=77.5 | hit_or_void=77.5 | miss=22.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.5% meets total-market threshold.
- API_CAL_RULE_0070 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=111 | hit=71.2 | hit_or_void=71.2 | miss=28.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=71.2% meets total-market threshold.
- API_CAL_RULE_0072 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=153 | hit=59.5 | hit_or_void=79.7 | miss=20.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=79.7% and miss_rate=20.3% meet protected-market threshold.
- API_CAL_RULE_0073 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=153 | hit=79.7 | hit_or_void=79.7 | miss=20.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=79.7% meets protected-market threshold.
- API_CAL_RULE_0075 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=154 | hit=74.0 | hit_or_void=74.0 | miss=26.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.0% meets total-market threshold.
- API_CAL_RULE_0082 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=168 | hit=76.8 | hit_or_void=76.8 | miss=23.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.8% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=321 | hit=55.5 | miss=44.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=322 | hit=54.0 | miss=46.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=54.0% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=159 | hit=53.5 | miss=46.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=53.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=162 | hit=57.4 | miss=42.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=57.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=162 | hit=47.5 | miss=52.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=47.5% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=162 | hit=49.4 | miss=50.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=49.4% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=153 | hit=59.5 | miss=40.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=59.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=154 | hit=50.6 | miss=49.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.6% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=154 | hit=52.6 | miss=47.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=52.6% is weak/negative in current calibration.
- API_CAL_RULE_0036 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=168 | hit=51.8 | miss=48.2 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=51.8% is below the 60% minimum for any ML review.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=78 | hit=42.3 | miss=57.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=42.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0048 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=78 | hit=52.6 | miss=47.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=52.6% is weak/negative in current calibration.
- API_CAL_RULE_0050 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=103 | hit=57.3 | miss=42.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=57.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0053 | SCORE_BUCKET=SCORE_70_79 | BTTS_YES | evaluated=103 | hit=54.4 | miss=45.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=54.4% is weak/negative in current calibration.
- API_CAL_RULE_0057 | SCORE_BUCKET=SCORE_80_89 | API_1X2 | evaluated=29 | hit=44.8 | miss=55.2 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=44.8% is below the 60% minimum for any ML review.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_80_89 | BTTS_YES | evaluated=30 | hit=50.0 | miss=50.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_80_89 | OVER_2_5 | evaluated=30 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0067 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=111 | hit=51.4 | miss=48.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=51.4% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=111 | hit=53.2 | miss=46.8 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.2% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=153 | hit=59.5 | miss=40.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=59.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=154 | hit=50.6 | miss=49.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.6% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=154 | hit=52.6 | miss=47.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=52.6% is weak/negative in current calibration.
- API_CAL_RULE_0078 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=168 | hit=51.8 | miss=48.2 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=51.8% is below the 60% minimum for any ML review.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
