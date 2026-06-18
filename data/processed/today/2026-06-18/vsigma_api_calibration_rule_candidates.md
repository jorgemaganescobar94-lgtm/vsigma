# vSIGMA API Calibration Rule Candidates - 2026-06-18

## Summary
- rows_reviewed: 77
- candidate_rows: 22
- block_rows: 25
- observe_rows: 30
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=25; RULE_OBSERVE_ONLY_SEGMENT=20; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_CANDIDATE_TOTAL_MARKET=6; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=6; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=6; RULE_CANDIDATE_PROTECTED_MARKET=4; RULE_NEUTRAL_OBSERVE_MORE=3
- rule_decision_counts: OBSERVE_MORE_SEGMENT=20; WATCH_ONLY_COLLECT_TO_50_SAMPLE=12; BLOCK_BTTS_YES_PROMOTION=10; FUTURE_RULE_REVIEW_ONLY=10; BLOCK_ML_PROMOTION=9; COLLECT_MORE_SAMPLE=7; BLOCK_OVER_2_5_PROMOTION=6; OBSERVE_MORE_GLOBAL_MARKET=3
- future_rule_candidate_counts: NO_BLOCKED_MARKET=25; NO_SEGMENT_SAMPLE_TOO_SMALL=20; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=12; YES_REVIEW_ONLY=10; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=3
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=127 | hit=72.4 | hit_or_void=72.4 | miss=27.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.4% meets total-market threshold.
- API_CAL_RULE_0009 | PREDICTED_SIDE=AWAY | API_DNB | evaluated=59 | hit=52.5 | hit_or_void=76.3 | miss=23.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.3% and miss_rate=23.7% meet protected-market threshold.
- API_CAL_RULE_0010 | PREDICTED_SIDE=AWAY | API_DOUBLE_CHANCE | evaluated=59 | hit=76.3 | hit_or_void=76.3 | miss=23.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.3% meets protected-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=59 | hit=72.9 | hit_or_void=72.9 | miss=27.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.9% meets total-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=68 | hit=72.1 | hit_or_void=72.1 | miss=27.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.1% meets total-market threshold.
- API_CAL_RULE_0023 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=48 | hit=58.3 | hit_or_void=81.2 | miss=18.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=81.2% and miss_rate=18.8% but sample=48 is below 50.
- API_CAL_RULE_0024 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=48 | hit=81.2 | hit_or_void=81.2 | miss=18.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=81.2% but sample=48 is below 50.
- API_CAL_RULE_0026 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=48 | hit=72.9 | hit_or_void=72.9 | miss=27.1 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.9% but sample=48 is below 50.
- API_CAL_RULE_0028 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | UNDER_3_5 | evaluated=48 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=75.0% but sample=48 is below 50.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=79 | hit=72.2 | hit_or_void=72.2 | miss=27.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.2% meets total-market threshold.
- API_CAL_RULE_0044 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=52 | hit=57.7 | hit_or_void=76.9 | miss=23.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.9% and miss_rate=23.1% meet protected-market threshold.
- API_CAL_RULE_0045 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=52 | hit=76.9 | hit_or_void=76.9 | miss=23.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.9% meets protected-market threshold.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=52 | hit=73.1 | hit_or_void=73.1 | miss=26.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=73.1% meets total-market threshold.
- API_CAL_RULE_0058 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=35 | hit=62.9 | hit_or_void=82.9 | miss=17.1 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=82.9% and miss_rate=17.1% but sample=35 is below 50.
- API_CAL_RULE_0059 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=35 | hit=82.9 | hit_or_void=82.9 | miss=17.1 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=82.9% but sample=35 is below 50.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=35 | hit=74.3 | hit_or_void=74.3 | miss=25.7 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.3% but sample=35 is below 50.
- API_CAL_RULE_0063 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=35 | hit=77.1 | hit_or_void=77.1 | miss=22.9 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=77.1% but sample=35 is below 50.
- API_CAL_RULE_0065 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=48 | hit=58.3 | hit_or_void=81.2 | miss=18.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=81.2% and miss_rate=18.8% but sample=48 is below 50.
- API_CAL_RULE_0066 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=48 | hit=81.2 | hit_or_void=81.2 | miss=18.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=81.2% but sample=48 is below 50.
- API_CAL_RULE_0068 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=48 | hit=72.9 | hit_or_void=72.9 | miss=27.1 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.9% but sample=48 is below 50.
- API_CAL_RULE_0070 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=48 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=75.0% but sample=48 is below 50.
- API_CAL_RULE_0075 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=79 | hit=72.2 | hit_or_void=72.2 | miss=27.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.2% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=127 | hit=50.4 | miss=49.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=50.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=127 | hit=47.2 | miss=52.8 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=47.2% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=127 | hit=53.5 | miss=46.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.5% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=59 | hit=52.5 | miss=47.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0011 | PREDICTED_SIDE=AWAY | BTTS_YES | evaluated=59 | hit=52.5 | miss=47.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=52.5% is weak/negative in current calibration.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=68 | hit=48.5 | miss=51.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=48.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=68 | hit=42.6 | miss=57.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=42.6% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=68 | hit=48.5 | miss=51.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.5% is weak/negative in current calibration.
- API_CAL_RULE_0022 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=48 | hit=58.3 | miss=41.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=58.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0025 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=48 | hit=41.7 | miss=58.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=41.7% is weak/negative in current calibration.
- API_CAL_RULE_0027 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=48 | hit=45.8 | miss=54.2 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.8% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=79 | hit=45.6 | miss=54.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=45.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | BTTS_YES | evaluated=79 | hit=50.6 | miss=49.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.6% is weak/negative in current calibration.
- API_CAL_RULE_0036 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=33 | hit=27.3 | miss=72.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=27.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0039 | SCORE_BUCKET=SCORE_55_69 | BTTS_YES | evaluated=33 | hit=48.5 | miss=51.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.5% is weak/negative in current calibration.
- API_CAL_RULE_0041 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=33 | hit=45.5 | miss=54.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.5% is weak/negative in current calibration.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=52 | hit=57.7 | miss=42.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=57.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0046 | SCORE_BUCKET=SCORE_70_79 | BTTS_YES | evaluated=52 | hit=50.0 | miss=50.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=35 | hit=34.3 | miss=65.7 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=34.3% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=35 | hit=42.9 | miss=57.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=42.9% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=48 | hit=58.3 | miss=41.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=58.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0067 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=48 | hit=41.7 | miss=58.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=41.7% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=48 | hit=45.8 | miss=54.2 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.8% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=79 | hit=45.6 | miss=54.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=45.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=79 | hit=50.6 | miss=49.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.6% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
