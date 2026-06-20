# vSIGMA API Calibration Rule Candidates - 2026-06-20

## Summary
- rows_reviewed: 77
- candidate_rows: 25
- block_rows: 23
- observe_rows: 29
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=23; RULE_OBSERVE_ONLY_SEGMENT=21; RULE_CANDIDATE_PROTECTED_MARKET=10; RULE_CANDIDATE_TOTAL_MARKET=10; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=3; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=2; RULE_NEUTRAL_OBSERVE_MORE=1
- rule_decision_counts: OBSERVE_MORE_SEGMENT=21; FUTURE_RULE_REVIEW_ONLY=20; BLOCK_ML_PROMOTION=9; BLOCK_BTTS_YES_PROMOTION=8; COLLECT_MORE_SAMPLE=7; BLOCK_OVER_2_5_PROMOTION=6; WATCH_ONLY_COLLECT_TO_50_SAMPLE=5; OBSERVE_MORE_GLOBAL_MARKET=1
- future_rule_candidate_counts: NO_BLOCKED_MARKET=23; NO_SEGMENT_SAMPLE_TOO_SMALL=21; YES_REVIEW_ONLY=20; NO_SAMPLE_TOO_SMALL=7; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=5; NO_OBSERVE_MORE=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0002 | ALL=ALL | API_DNB | evaluated=165 | hit=52.7 | hit_or_void=75.2 | miss=24.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.2% and miss_rate=24.8% meet protected-market threshold.
- API_CAL_RULE_0003 | ALL=ALL | API_DOUBLE_CHANCE | evaluated=165 | hit=75.2 | hit_or_void=75.2 | miss=24.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.2% meets protected-market threshold.
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=165 | hit=73.3 | hit_or_void=73.3 | miss=26.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=73.3% meets total-market threshold.
- API_CAL_RULE_0009 | PREDICTED_SIDE=AWAY | API_DNB | evaluated=76 | hit=53.9 | hit_or_void=77.6 | miss=22.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=77.6% and miss_rate=22.4% meet protected-market threshold.
- API_CAL_RULE_0010 | PREDICTED_SIDE=AWAY | API_DOUBLE_CHANCE | evaluated=76 | hit=77.6 | hit_or_void=77.6 | miss=22.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=77.6% meets protected-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=76 | hit=76.3 | hit_or_void=76.3 | miss=23.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.3% meets total-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=89 | hit=70.8 | hit_or_void=70.8 | miss=29.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=70.8% meets total-market threshold.
- API_CAL_RULE_0023 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=62 | hit=59.7 | hit_or_void=82.3 | miss=17.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=82.3% and miss_rate=17.7% meet protected-market threshold.
- API_CAL_RULE_0024 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=62 | hit=82.3 | hit_or_void=82.3 | miss=17.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=82.3% meets protected-market threshold.
- API_CAL_RULE_0026 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=62 | hit=74.2 | hit_or_void=74.2 | miss=25.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.2% meets total-market threshold.
- API_CAL_RULE_0028 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | UNDER_3_5 | evaluated=62 | hit=74.2 | hit_or_void=74.2 | miss=25.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=74.2% meets total-market threshold.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=103 | hit=72.8 | hit_or_void=72.8 | miss=27.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.8% meets total-market threshold.
- API_CAL_RULE_0042 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=43 | hit=72.1 | hit_or_void=72.1 | miss=27.9 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=72.1% but sample=43 is below 50.
- API_CAL_RULE_0044 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=67 | hit=58.2 | hit_or_void=76.1 | miss=23.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.1% and miss_rate=23.9% meet protected-market threshold.
- API_CAL_RULE_0045 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=67 | hit=76.1 | hit_or_void=76.1 | miss=23.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.1% meets protected-market threshold.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=67 | hit=76.1 | hit_or_void=76.1 | miss=23.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.1% meets total-market threshold.
- API_CAL_RULE_0058 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=46 | hit=65.2 | hit_or_void=87.0 | miss=13.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=87.0% and miss_rate=13.0% but sample=46 is below 50.
- API_CAL_RULE_0059 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=46 | hit=87.0 | hit_or_void=87.0 | miss=13.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=87.0% but sample=46 is below 50.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=46 | hit=76.1 | hit_or_void=76.1 | miss=23.9 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.1% but sample=46 is below 50.
- API_CAL_RULE_0063 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=46 | hit=78.3 | hit_or_void=78.3 | miss=21.7 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=78.3% but sample=46 is below 50.
- API_CAL_RULE_0065 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=62 | hit=59.7 | hit_or_void=82.3 | miss=17.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=82.3% and miss_rate=17.7% meet protected-market threshold.
- API_CAL_RULE_0066 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=62 | hit=82.3 | hit_or_void=82.3 | miss=17.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=82.3% meets protected-market threshold.
- API_CAL_RULE_0068 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=62 | hit=74.2 | hit_or_void=74.2 | miss=25.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.2% meets total-market threshold.
- API_CAL_RULE_0070 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=62 | hit=74.2 | hit_or_void=74.2 | miss=25.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=74.2% meets total-market threshold.
- API_CAL_RULE_0075 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=103 | hit=72.8 | hit_or_void=72.8 | miss=27.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.8% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=165 | hit=52.7 | miss=47.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=165 | hit=49.7 | miss=50.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=49.7% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=165 | hit=53.9 | miss=46.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.9% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=76 | hit=53.9 | miss=46.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=53.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=89 | hit=51.7 | miss=48.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=51.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=89 | hit=44.9 | miss=55.1 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=44.9% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=89 | hit=49.4 | miss=50.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=49.4% is weak/negative in current calibration.
- API_CAL_RULE_0022 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=62 | hit=59.7 | miss=40.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=59.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0025 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=62 | hit=43.5 | miss=56.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=43.5% is weak/negative in current calibration.
- API_CAL_RULE_0027 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=62 | hit=48.4 | miss=51.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.4% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=103 | hit=48.5 | miss=51.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=48.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | BTTS_YES | evaluated=103 | hit=53.4 | miss=46.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.4% is weak/negative in current calibration.
- API_CAL_RULE_0036 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=43 | hit=32.6 | miss=67.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=32.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0039 | SCORE_BUCKET=SCORE_55_69 | BTTS_YES | evaluated=43 | hit=46.5 | miss=53.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=46.5% is weak/negative in current calibration.
- API_CAL_RULE_0041 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=43 | hit=41.9 | miss=58.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=41.9% is weak/negative in current calibration.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=67 | hit=58.2 | miss=41.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=58.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=46 | hit=39.1 | miss=60.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=39.1% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=46 | hit=45.7 | miss=54.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.7% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=62 | hit=59.7 | miss=40.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=59.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0067 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=62 | hit=43.5 | miss=56.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=43.5% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=62 | hit=48.4 | miss=51.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.4% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=103 | hit=48.5 | miss=51.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=48.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=103 | hit=53.4 | miss=46.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.4% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
