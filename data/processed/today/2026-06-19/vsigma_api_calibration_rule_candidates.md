# vSIGMA API Calibration Rule Candidates - 2026-06-19

## Summary
- rows_reviewed: 77
- candidate_rows: 23
- block_rows: 25
- observe_rows: 29
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=25; RULE_OBSERVE_ONLY_SEGMENT=19; RULE_CANDIDATE_TOTAL_MARKET=10; RULE_CANDIDATE_PROTECTED_MARKET=8; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_NEUTRAL_OBSERVE_MORE=3; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=3; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=2
- rule_decision_counts: OBSERVE_MORE_SEGMENT=19; FUTURE_RULE_REVIEW_ONLY=18; BLOCK_BTTS_YES_PROMOTION=10; BLOCK_ML_PROMOTION=9; COLLECT_MORE_SAMPLE=7; BLOCK_OVER_2_5_PROMOTION=6; WATCH_ONLY_COLLECT_TO_50_SAMPLE=5; OBSERVE_MORE_GLOBAL_MARKET=3
- future_rule_candidate_counts: NO_BLOCKED_MARKET=25; NO_SEGMENT_SAMPLE_TOO_SMALL=19; YES_REVIEW_ONLY=18; NO_SAMPLE_TOO_SMALL=7; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=5; NO_OBSERVE_MORE=3
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=151 | hit=73.5 | hit_or_void=73.5 | miss=26.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=73.5% meets total-market threshold.
- API_CAL_RULE_0009 | PREDICTED_SIDE=AWAY | API_DNB | evaluated=70 | hit=52.9 | hit_or_void=77.1 | miss=22.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=77.1% and miss_rate=22.9% meet protected-market threshold.
- API_CAL_RULE_0010 | PREDICTED_SIDE=AWAY | API_DOUBLE_CHANCE | evaluated=70 | hit=77.1 | hit_or_void=77.1 | miss=22.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=77.1% meets protected-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=70 | hit=77.1 | hit_or_void=77.1 | miss=22.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.1% meets total-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=81 | hit=70.4 | hit_or_void=70.4 | miss=29.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=70.4% meets total-market threshold.
- API_CAL_RULE_0023 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=58 | hit=58.6 | hit_or_void=82.8 | miss=17.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=82.8% and miss_rate=17.2% meet protected-market threshold.
- API_CAL_RULE_0024 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=58 | hit=82.8 | hit_or_void=82.8 | miss=17.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=82.8% meets protected-market threshold.
- API_CAL_RULE_0026 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=58 | hit=74.1 | hit_or_void=74.1 | miss=25.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.1% meets total-market threshold.
- API_CAL_RULE_0028 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | UNDER_3_5 | evaluated=58 | hit=74.1 | hit_or_void=74.1 | miss=25.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=74.1% meets total-market threshold.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=93 | hit=73.1 | hit_or_void=73.1 | miss=26.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=73.1% meets total-market threshold.
- API_CAL_RULE_0042 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=39 | hit=71.8 | hit_or_void=71.8 | miss=28.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=71.8% but sample=39 is below 50.
- API_CAL_RULE_0044 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=61 | hit=57.4 | hit_or_void=75.4 | miss=24.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.4% and miss_rate=24.6% meet protected-market threshold.
- API_CAL_RULE_0045 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=61 | hit=75.4 | hit_or_void=75.4 | miss=24.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.4% meets protected-market threshold.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=61 | hit=77.0 | hit_or_void=77.0 | miss=23.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.0% meets total-market threshold.
- API_CAL_RULE_0058 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=43 | hit=62.8 | hit_or_void=86.0 | miss=14.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=86.0% and miss_rate=14.0% but sample=43 is below 50.
- API_CAL_RULE_0059 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=43 | hit=86.0 | hit_or_void=86.0 | miss=14.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=86.0% but sample=43 is below 50.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=43 | hit=76.7 | hit_or_void=76.7 | miss=23.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.7% but sample=43 is below 50.
- API_CAL_RULE_0063 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=43 | hit=76.7 | hit_or_void=76.7 | miss=23.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=76.7% but sample=43 is below 50.
- API_CAL_RULE_0065 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=58 | hit=58.6 | hit_or_void=82.8 | miss=17.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=82.8% and miss_rate=17.2% meet protected-market threshold.
- API_CAL_RULE_0066 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=58 | hit=82.8 | hit_or_void=82.8 | miss=17.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=82.8% meets protected-market threshold.
- API_CAL_RULE_0068 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=58 | hit=74.1 | hit_or_void=74.1 | miss=25.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.1% meets total-market threshold.
- API_CAL_RULE_0070 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=58 | hit=74.1 | hit_or_void=74.1 | miss=25.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=74.1% meets total-market threshold.
- API_CAL_RULE_0075 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=93 | hit=73.1 | hit_or_void=73.1 | miss=26.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=73.1% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=151 | hit=51.0 | miss=49.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=51.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=151 | hit=49.0 | miss=51.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=49.0% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=151 | hit=53.6 | miss=46.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.6% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=70 | hit=52.9 | miss=47.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0011 | PREDICTED_SIDE=AWAY | BTTS_YES | evaluated=70 | hit=54.3 | miss=45.7 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=54.3% is weak/negative in current calibration.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=81 | hit=49.4 | miss=50.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=49.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=81 | hit=44.4 | miss=55.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=44.4% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=81 | hit=48.1 | miss=51.9 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.1% is weak/negative in current calibration.
- API_CAL_RULE_0022 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=58 | hit=58.6 | miss=41.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=58.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0025 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=58 | hit=41.4 | miss=58.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=41.4% is weak/negative in current calibration.
- API_CAL_RULE_0027 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=58 | hit=46.6 | miss=53.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=46.6% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=93 | hit=46.2 | miss=53.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=46.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | BTTS_YES | evaluated=93 | hit=53.8 | miss=46.2 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.8% is weak/negative in current calibration.
- API_CAL_RULE_0036 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=39 | hit=28.2 | miss=71.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=28.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0039 | SCORE_BUCKET=SCORE_55_69 | BTTS_YES | evaluated=39 | hit=48.7 | miss=51.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.7% is weak/negative in current calibration.
- API_CAL_RULE_0041 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=39 | hit=41.0 | miss=59.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=41.0% is weak/negative in current calibration.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=61 | hit=57.4 | miss=42.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=57.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0046 | SCORE_BUCKET=SCORE_70_79 | BTTS_YES | evaluated=61 | hit=54.1 | miss=45.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=54.1% is weak/negative in current calibration.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=43 | hit=37.2 | miss=62.8 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=37.2% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=43 | hit=44.2 | miss=55.8 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=44.2% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=58 | hit=58.6 | miss=41.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=58.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0067 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=58 | hit=41.4 | miss=58.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=41.4% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=58 | hit=46.6 | miss=53.4 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=46.6% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=93 | hit=46.2 | miss=53.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=46.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=93 | hit=53.8 | miss=46.2 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.8% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
