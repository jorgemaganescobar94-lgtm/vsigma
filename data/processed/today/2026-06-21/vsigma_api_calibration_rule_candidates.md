# vSIGMA API Calibration Rule Candidates - 2026-06-21

## Summary
- rows_reviewed: 84
- candidate_rows: 23
- block_rows: 21
- observe_rows: 40
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_OBSERVE_ONLY_SEGMENT=29; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=21; RULE_CANDIDATE_TOTAL_MARKET=12; RULE_CANDIDATE_PROTECTED_MARKET=10; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_NEUTRAL_OBSERVE_MORE=4; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=1
- rule_decision_counts: OBSERVE_MORE_SEGMENT=29; FUTURE_RULE_REVIEW_ONLY=22; BLOCK_ML_PROMOTION=8; BLOCK_BTTS_YES_PROMOTION=7; COLLECT_MORE_SAMPLE=7; BLOCK_OVER_2_5_PROMOTION=6; OBSERVE_MORE_GLOBAL_MARKET=4; WATCH_ONLY_COLLECT_TO_50_SAMPLE=1
- future_rule_candidate_counts: NO_SEGMENT_SAMPLE_TOO_SMALL=29; YES_REVIEW_ONLY=22; NO_BLOCKED_MARKET=21; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=4; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=84
- pick_permission_counts: NO_PICK_PERMISSION=84
- stake_permission_counts: NO_STAKE_PERMISSION=84
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=250 | hit=74.4 | hit_or_void=74.4 | miss=25.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.4% meets total-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=116 | hit=77.6 | hit_or_void=77.6 | miss=22.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.6% meets total-market threshold.
- API_CAL_RULE_0016 | PREDICTED_SIDE=HOME | API_DNB | evaluated=133 | hit=55.6 | hit_or_void=75.9 | miss=24.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.9% and miss_rate=24.1% meet protected-market threshold.
- API_CAL_RULE_0017 | PREDICTED_SIDE=HOME | API_DOUBLE_CHANCE | evaluated=133 | hit=75.9 | hit_or_void=75.9 | miss=24.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.9% meets protected-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=133 | hit=72.2 | hit_or_void=72.2 | miss=27.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.2% meets total-market threshold.
- API_CAL_RULE_0030 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=105 | hit=60.0 | hit_or_void=79.0 | miss=21.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=79.0% and miss_rate=21.0% meet protected-market threshold.
- API_CAL_RULE_0031 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=105 | hit=79.0 | hit_or_void=79.0 | miss=21.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=79.0% meets protected-market threshold.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=106 | hit=72.6 | hit_or_void=72.6 | miss=27.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.6% meets total-market threshold.
- API_CAL_RULE_0040 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=144 | hit=75.7 | hit_or_void=75.7 | miss=24.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.7% meets total-market threshold.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_55_69 | OVER_1_5 | evaluated=66 | hit=68.2 | hit_or_void=68.2 | miss=31.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=68.2% meets total-market threshold.
- API_CAL_RULE_0049 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=66 | hit=72.7 | hit_or_void=72.7 | miss=27.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=72.7% meets total-market threshold.
- API_CAL_RULE_0051 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=88 | hit=54.5 | hit_or_void=75.0 | miss=25.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.0% and miss_rate=25.0% meet protected-market threshold.
- API_CAL_RULE_0052 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=88 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.0% meets protected-market threshold.
- API_CAL_RULE_0054 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=88 | hit=79.5 | hit_or_void=79.5 | miss=20.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=79.5% meets total-market threshold.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_80_89 | OVER_1_5 | evaluated=23 | hit=65.2 | hit_or_void=65.2 | miss=34.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=65.2% but sample=23 is below 50.
- API_CAL_RULE_0065 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=73 | hit=67.1 | hit_or_void=84.9 | miss=15.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=84.9% and miss_rate=15.1% meet protected-market threshold.
- API_CAL_RULE_0066 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=73 | hit=84.9 | hit_or_void=84.9 | miss=15.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=84.9% meets protected-market threshold.
- API_CAL_RULE_0068 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=73 | hit=76.7 | hit_or_void=76.7 | miss=23.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.7% meets total-market threshold.
- API_CAL_RULE_0070 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=73 | hit=71.2 | hit_or_void=71.2 | miss=28.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=71.2% meets total-market threshold.
- API_CAL_RULE_0072 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=105 | hit=60.0 | hit_or_void=79.0 | miss=21.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=79.0% and miss_rate=21.0% meet protected-market threshold.
- API_CAL_RULE_0073 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=105 | hit=79.0 | hit_or_void=79.0 | miss=21.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=79.0% meets protected-market threshold.
- API_CAL_RULE_0075 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=106 | hit=72.6 | hit_or_void=72.6 | miss=27.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.6% meets total-market threshold.
- API_CAL_RULE_0082 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=144 | hit=75.7 | hit_or_void=75.7 | miss=24.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.7% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=249 | hit=53.4 | miss=46.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=53.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=250 | hit=52.8 | miss=47.2 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=52.8% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=116 | hit=50.9 | miss=49.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=50.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=133 | hit=55.6 | miss=44.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=133 | hit=48.1 | miss=51.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.1% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=133 | hit=50.4 | miss=49.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.4% is weak/negative in current calibration.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=106 | hit=47.2 | miss=52.8 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=47.2% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=106 | hit=50.9 | miss=49.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.9% is weak/negative in current calibration.
- API_CAL_RULE_0036 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=144 | hit=48.6 | miss=51.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=48.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=66 | hit=39.4 | miss=60.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=39.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0046 | SCORE_BUCKET=SCORE_55_69 | BTTS_YES | evaluated=66 | hit=54.5 | miss=45.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=54.5% is weak/negative in current calibration.
- API_CAL_RULE_0048 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=66 | hit=47.0 | miss=53.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=47.0% is weak/negative in current calibration.
- API_CAL_RULE_0050 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=88 | hit=54.5 | miss=45.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=54.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0057 | SCORE_BUCKET=SCORE_80_89 | API_1X2 | evaluated=22 | hit=45.5 | miss=54.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=45.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_80_89 | BTTS_YES | evaluated=23 | hit=43.5 | miss=56.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=43.5% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_80_89 | OVER_2_5 | evaluated=23 | hit=43.5 | miss=56.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=43.5% is weak/negative in current calibration.
- API_CAL_RULE_0067 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=73 | hit=49.3 | miss=50.7 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=49.3% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=73 | hit=53.4 | miss=46.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.4% is weak/negative in current calibration.
- API_CAL_RULE_0074 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=106 | hit=47.2 | miss=52.8 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=47.2% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=106 | hit=50.9 | miss=49.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.9% is weak/negative in current calibration.
- API_CAL_RULE_0078 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=144 | hit=48.6 | miss=51.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=48.6% is below the 60% minimum for any ML review.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
