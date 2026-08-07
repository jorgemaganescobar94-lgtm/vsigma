# vSIGMA API Calibration Rule Candidates - 2026-08-07

## Summary
- rows_reviewed: 84
- candidate_rows: 28
- block_rows: 23
- observe_rows: 33
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_OBSERVE_ONLY_SEGMENT=24; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=23; RULE_CANDIDATE_PROTECTED_MARKET=14; RULE_CANDIDATE_TOTAL_MARKET=13; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_NEUTRAL_OBSERVE_MORE=2; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=1
- rule_decision_counts: FUTURE_RULE_REVIEW_ONLY=27; OBSERVE_MORE_SEGMENT=24; BLOCK_ML_PROMOTION=11; BLOCK_OVER_2_5_PROMOTION=7; COLLECT_MORE_SAMPLE=7; BLOCK_BTTS_YES_PROMOTION=5; OBSERVE_MORE_GLOBAL_MARKET=2; WATCH_ONLY_COLLECT_TO_50_SAMPLE=1
- future_rule_candidate_counts: YES_REVIEW_ONLY=27; NO_SEGMENT_SAMPLE_TOO_SMALL=24; NO_BLOCKED_MARKET=23; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=2; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=84
- pick_permission_counts: NO_PICK_PERMISSION=84
- stake_permission_counts: NO_STAKE_PERMISSION=84
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0002 | ALL=ALL | API_DNB | evaluated=336 | hit=54.2 | hit_or_void=77.4 | miss=22.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=77.4% and miss_rate=22.6% meet protected-market threshold.
- API_CAL_RULE_0003 | ALL=ALL | API_DOUBLE_CHANCE | evaluated=336 | hit=77.4 | hit_or_void=77.4 | miss=22.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=77.4% meets protected-market threshold.
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=337 | hit=76.6 | hit_or_void=76.6 | miss=23.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.6% meets total-market threshold.
- API_CAL_RULE_0009 | PREDICTED_SIDE=AWAY | API_DNB | evaluated=172 | hit=50.6 | hit_or_void=77.9 | miss=22.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=77.9% and miss_rate=22.1% meet protected-market threshold.
- API_CAL_RULE_0010 | PREDICTED_SIDE=AWAY | API_DOUBLE_CHANCE | evaluated=172 | hit=77.9 | hit_or_void=77.9 | miss=22.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=77.9% meets protected-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=172 | hit=82.0 | hit_or_void=82.0 | miss=18.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=82.0% meets total-market threshold.
- API_CAL_RULE_0016 | PREDICTED_SIDE=HOME | API_DNB | evaluated=164 | hit=57.9 | hit_or_void=76.8 | miss=23.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.8% and miss_rate=23.2% meet protected-market threshold.
- API_CAL_RULE_0017 | PREDICTED_SIDE=HOME | API_DOUBLE_CHANCE | evaluated=164 | hit=76.8 | hit_or_void=76.8 | miss=23.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.8% meets protected-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=164 | hit=71.3 | hit_or_void=71.3 | miss=28.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=71.3% meets total-market threshold.
- API_CAL_RULE_0030 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=164 | hit=55.5 | hit_or_void=81.1 | miss=18.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=81.1% and miss_rate=18.9% meet protected-market threshold.
- API_CAL_RULE_0031 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=164 | hit=81.1 | hit_or_void=81.1 | miss=18.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=81.1% meets protected-market threshold.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=165 | hit=75.8 | hit_or_void=75.8 | miss=24.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.8% meets total-market threshold.
- API_CAL_RULE_0035 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | UNDER_3_5 | evaluated=165 | hit=70.3 | hit_or_void=70.3 | miss=29.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=70.3% meets total-market threshold.
- API_CAL_RULE_0040 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=172 | hit=77.3 | hit_or_void=77.3 | miss=22.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.3% meets total-market threshold.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_55_69 | OVER_1_5 | evaluated=80 | hit=71.2 | hit_or_void=71.2 | miss=28.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=71.2% meets total-market threshold.
- API_CAL_RULE_0051 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=105 | hit=58.1 | hit_or_void=76.2 | miss=23.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.2% and miss_rate=23.8% meet protected-market threshold.
- API_CAL_RULE_0052 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=105 | hit=76.2 | hit_or_void=76.2 | miss=23.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.2% meets protected-market threshold.
- API_CAL_RULE_0054 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=105 | hit=80.0 | hit_or_void=80.0 | miss=20.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=80.0% meets total-market threshold.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_80_89 | OVER_1_5 | evaluated=30 | hit=66.7 | hit_or_void=66.7 | miss=33.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=66.7% but sample=30 is below 50.
- API_CAL_RULE_0065 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=122 | hit=59.8 | hit_or_void=86.9 | miss=13.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=86.9% and miss_rate=13.1% meet protected-market threshold.
- API_CAL_RULE_0066 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=122 | hit=86.9 | hit_or_void=86.9 | miss=13.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=86.9% meets protected-market threshold.
- API_CAL_RULE_0068 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=122 | hit=79.5 | hit_or_void=79.5 | miss=20.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=79.5% meets total-market threshold.
- API_CAL_RULE_0070 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=122 | hit=73.8 | hit_or_void=73.8 | miss=26.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=73.8% meets total-market threshold.
- API_CAL_RULE_0072 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=164 | hit=55.5 | hit_or_void=81.1 | miss=18.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=81.1% and miss_rate=18.9% meet protected-market threshold.
- API_CAL_RULE_0073 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=164 | hit=81.1 | hit_or_void=81.1 | miss=18.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=81.1% meets protected-market threshold.
- API_CAL_RULE_0075 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=165 | hit=75.8 | hit_or_void=75.8 | miss=24.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.8% meets total-market threshold.
- API_CAL_RULE_0077 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=165 | hit=70.3 | hit_or_void=70.3 | miss=29.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=70.3% meets total-market threshold.
- API_CAL_RULE_0082 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=172 | hit=77.3 | hit_or_void=77.3 | miss=22.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.3% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=336 | hit=54.2 | miss=45.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=54.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=337 | hit=54.0 | miss=46.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=54.0% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=172 | hit=50.6 | miss=49.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=50.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=164 | hit=57.9 | miss=42.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=57.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=164 | hit=47.0 | miss=53.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=47.0% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=164 | hit=48.8 | miss=51.2 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.8% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=164 | hit=55.5 | miss=44.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=165 | hit=53.9 | miss=46.1 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.9% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=165 | hit=49.1 | miss=50.9 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=49.1% is weak/negative in current calibration.
- API_CAL_RULE_0036 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=172 | hit=52.9 | miss=47.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=80 | hit=43.8 | miss=56.2 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=43.8% is below the 60% minimum for any ML review.
- API_CAL_RULE_0048 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=80 | hit=53.8 | miss=46.2 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.8% is weak/negative in current calibration.
- API_CAL_RULE_0050 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=105 | hit=58.1 | miss=41.9 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=58.1% is below the 60% minimum for any ML review.
- API_CAL_RULE_0053 | SCORE_BUCKET=SCORE_70_79 | BTTS_YES | evaluated=105 | hit=53.3 | miss=46.7 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.3% is weak/negative in current calibration.
- API_CAL_RULE_0057 | SCORE_BUCKET=SCORE_80_89 | API_1X2 | evaluated=29 | hit=44.8 | miss=55.2 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=44.8% is below the 60% minimum for any ML review.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_80_89 | BTTS_YES | evaluated=30 | hit=50.0 | miss=50.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_80_89 | OVER_2_5 | evaluated=30 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SCORE_BUCKET=SCORE_90_PLUS | API_1X2 | evaluated=122 | hit=59.8 | miss=40.2 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=59.8% is below the 60% minimum for any ML review.
- API_CAL_RULE_0069 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=122 | hit=48.4 | miss=51.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.4% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=164 | hit=55.5 | miss=44.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=165 | hit=53.9 | miss=46.1 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.9% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=165 | hit=49.1 | miss=50.9 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=49.1% is weak/negative in current calibration.
- API_CAL_RULE_0078 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=172 | hit=52.9 | miss=47.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.9% is below the 60% minimum for any ML review.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
