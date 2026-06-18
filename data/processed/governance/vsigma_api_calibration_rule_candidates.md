# vSIGMA API Calibration Rule Candidates - 2026-06-18

## Summary
- rows_reviewed: 77
- candidate_rows: 21
- block_rows: 25
- observe_rows: 31
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=25; RULE_OBSERVE_ONLY_SEGMENT=21; RULE_CANDIDATE_TOTAL_MARKET=10; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_CANDIDATE_PROTECTED_MARKET=6; RULE_NEUTRAL_OBSERVE_MORE=3; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=3; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=2
- rule_decision_counts: OBSERVE_MORE_SEGMENT=21; FUTURE_RULE_REVIEW_ONLY=16; BLOCK_BTTS_YES_PROMOTION=10; BLOCK_ML_PROMOTION=9; COLLECT_MORE_SAMPLE=7; BLOCK_OVER_2_5_PROMOTION=6; WATCH_ONLY_COLLECT_TO_50_SAMPLE=5; OBSERVE_MORE_GLOBAL_MARKET=3
- future_rule_candidate_counts: NO_BLOCKED_MARKET=25; NO_SEGMENT_SAMPLE_TOO_SMALL=21; YES_REVIEW_ONLY=16; NO_SAMPLE_TOO_SMALL=7; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=5; NO_OBSERVE_MORE=3
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=141 | hit=73.8 | hit_or_void=73.8 | miss=26.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=73.8% meets total-market threshold.
- API_CAL_RULE_0009 | PREDICTED_SIDE=AWAY | API_DNB | evaluated=67 | hit=50.7 | hit_or_void=76.1 | miss=23.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.1% and miss_rate=23.9% meet protected-market threshold.
- API_CAL_RULE_0010 | PREDICTED_SIDE=AWAY | API_DOUBLE_CHANCE | evaluated=67 | hit=76.1 | hit_or_void=76.1 | miss=23.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.1% meets protected-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=67 | hit=76.1 | hit_or_void=76.1 | miss=23.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.1% meets total-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=74 | hit=71.6 | hit_or_void=71.6 | miss=28.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=71.6% meets total-market threshold.
- API_CAL_RULE_0023 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=55 | hit=56.4 | hit_or_void=81.8 | miss=18.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=81.8% and miss_rate=18.2% meet protected-market threshold.
- API_CAL_RULE_0024 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=55 | hit=81.8 | hit_or_void=81.8 | miss=18.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=81.8% meets protected-market threshold.
- API_CAL_RULE_0026 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=55 | hit=74.5 | hit_or_void=74.5 | miss=25.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.5% meets total-market threshold.
- API_CAL_RULE_0028 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | UNDER_3_5 | evaluated=55 | hit=74.5 | hit_or_void=74.5 | miss=25.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=74.5% meets total-market threshold.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=86 | hit=73.3 | hit_or_void=73.3 | miss=26.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=73.3% meets total-market threshold.
- API_CAL_RULE_0042 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=36 | hit=72.2 | hit_or_void=72.2 | miss=27.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=72.2% but sample=36 is below 50.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=57 | hit=75.4 | hit_or_void=75.4 | miss=24.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.4% meets total-market threshold.
- API_CAL_RULE_0058 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=41 | hit=61.0 | hit_or_void=85.4 | miss=14.6 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=85.4% and miss_rate=14.6% but sample=41 is below 50.
- API_CAL_RULE_0059 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=41 | hit=85.4 | hit_or_void=85.4 | miss=14.6 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=85.4% but sample=41 is below 50.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=41 | hit=75.6 | hit_or_void=75.6 | miss=24.4 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.6% but sample=41 is below 50.
- API_CAL_RULE_0063 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=41 | hit=78.0 | hit_or_void=78.0 | miss=22.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=78.0% but sample=41 is below 50.
- API_CAL_RULE_0065 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=55 | hit=56.4 | hit_or_void=81.8 | miss=18.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=81.8% and miss_rate=18.2% meet protected-market threshold.
- API_CAL_RULE_0066 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=55 | hit=81.8 | hit_or_void=81.8 | miss=18.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=81.8% meets protected-market threshold.
- API_CAL_RULE_0068 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=55 | hit=74.5 | hit_or_void=74.5 | miss=25.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.5% meets total-market threshold.
- API_CAL_RULE_0070 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=55 | hit=74.5 | hit_or_void=74.5 | miss=25.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=74.5% meets total-market threshold.
- API_CAL_RULE_0075 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=86 | hit=73.3 | hit_or_void=73.3 | miss=26.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=73.3% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=141 | hit=48.2 | miss=51.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=48.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=141 | hit=48.9 | miss=51.1 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.9% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=141 | hit=52.5 | miss=47.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=52.5% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=67 | hit=50.7 | miss=49.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=50.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0011 | PREDICTED_SIDE=AWAY | BTTS_YES | evaluated=67 | hit=53.7 | miss=46.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.7% is weak/negative in current calibration.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=74 | hit=45.9 | miss=54.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=45.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=74 | hit=44.6 | miss=55.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=44.6% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=74 | hit=47.3 | miss=52.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=47.3% is weak/negative in current calibration.
- API_CAL_RULE_0022 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=55 | hit=56.4 | miss=43.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=56.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0025 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=55 | hit=41.8 | miss=58.2 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=41.8% is weak/negative in current calibration.
- API_CAL_RULE_0027 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=55 | hit=45.5 | miss=54.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.5% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=86 | hit=43.0 | miss=57.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=43.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | BTTS_YES | evaluated=86 | hit=53.5 | miss=46.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.5% is weak/negative in current calibration.
- API_CAL_RULE_0036 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=36 | hit=25.0 | miss=75.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=25.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0039 | SCORE_BUCKET=SCORE_55_69 | BTTS_YES | evaluated=36 | hit=50.0 | miss=50.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0041 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=36 | hit=41.7 | miss=58.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=41.7% is weak/negative in current calibration.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=57 | hit=54.4 | miss=45.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=54.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0046 | SCORE_BUCKET=SCORE_70_79 | BTTS_YES | evaluated=57 | hit=52.6 | miss=47.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=52.6% is weak/negative in current calibration.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=41 | hit=36.6 | miss=63.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=36.6% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=41 | hit=41.5 | miss=58.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=41.5% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=55 | hit=56.4 | miss=43.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=56.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0067 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=55 | hit=41.8 | miss=58.2 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=41.8% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=55 | hit=45.5 | miss=54.5 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.5% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=86 | hit=43.0 | miss=57.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=43.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=86 | hit=53.5 | miss=46.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.5% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
