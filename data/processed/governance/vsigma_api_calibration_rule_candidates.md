# vSIGMA API Calibration Rule Candidates - 2026-06-15

## Summary
- rows_reviewed: 77
- candidate_rows: 15
- block_rows: 24
- observe_rows: 38
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_OBSERVE_ONLY_SEGMENT=28; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=24; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=8; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=6; RULE_NEUTRAL_OBSERVE_MORE=3; RULE_CANDIDATE_TOTAL_MARKET=1
- rule_decision_counts: OBSERVE_MORE_SEGMENT=28; WATCH_ONLY_COLLECT_TO_50_SAMPLE=14; BLOCK_ML_PROMOTION=8; BLOCK_BTTS_YES_PROMOTION=8; BLOCK_OVER_2_5_PROMOTION=8; COLLECT_MORE_SAMPLE=7; OBSERVE_MORE_GLOBAL_MARKET=3; FUTURE_RULE_REVIEW_ONLY=1
- future_rule_candidate_counts: NO_SEGMENT_SAMPLE_TOO_SMALL=28; NO_BLOCKED_MARKET=24; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=14; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=3; YES_REVIEW_ONLY=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=76 | hit=69.7 | hit_or_void=69.7 | miss=30.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=69.7% meets total-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=30 | hit=80.0 | hit_or_void=80.0 | miss=20.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=80.0% but sample=30 is below 50.
- API_CAL_RULE_0023 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=29 | hit=55.2 | hit_or_void=82.8 | miss=17.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=82.8% and miss_rate=17.2% but sample=29 is below 50.
- API_CAL_RULE_0024 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=29 | hit=82.8 | hit_or_void=82.8 | miss=17.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=82.8% but sample=29 is below 50.
- API_CAL_RULE_0026 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=29 | hit=79.3 | hit_or_void=79.3 | miss=20.7 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=79.3% but sample=29 is below 50.
- API_CAL_RULE_0042 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=26 | hit=76.9 | hit_or_void=76.9 | miss=23.1 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=76.9% but sample=26 is below 50.
- API_CAL_RULE_0044 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=24 | hit=62.5 | hit_or_void=75.0 | miss=25.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.0% and miss_rate=25.0% but sample=24 is below 50.
- API_CAL_RULE_0045 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=24 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.0% but sample=24 is below 50.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=24 | hit=70.8 | hit_or_void=70.8 | miss=29.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=70.8% but sample=24 is below 50.
- API_CAL_RULE_0058 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=21 | hit=61.9 | hit_or_void=85.7 | miss=14.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=85.7% and miss_rate=14.3% but sample=21 is below 50.
- API_CAL_RULE_0059 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=21 | hit=85.7 | hit_or_void=85.7 | miss=14.3 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=85.7% but sample=21 is below 50.
- API_CAL_RULE_0061 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=21 | hit=76.2 | hit_or_void=76.2 | miss=23.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.2% but sample=21 is below 50.
- API_CAL_RULE_0065 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=29 | hit=55.2 | hit_or_void=82.8 | miss=17.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=82.8% and miss_rate=17.2% but sample=29 is below 50.
- API_CAL_RULE_0066 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=29 | hit=82.8 | hit_or_void=82.8 | miss=17.2 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=82.8% but sample=29 is below 50.
- API_CAL_RULE_0068 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=29 | hit=79.3 | hit_or_void=79.3 | miss=20.7 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=79.3% but sample=29 is below 50.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=76 | hit=47.4 | miss=52.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=47.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=76 | hit=47.4 | miss=52.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=47.4% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=76 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=30 | hit=46.7 | miss=53.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=46.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=46 | hit=47.8 | miss=52.2 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=47.8% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=46 | hit=39.1 | miss=60.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=39.1% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=46 | hit=45.7 | miss=54.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.7% is weak/negative in current calibration.
- API_CAL_RULE_0022 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=29 | hit=55.2 | miss=44.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0025 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=29 | hit=48.3 | miss=51.7 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.3% is weak/negative in current calibration.
- API_CAL_RULE_0027 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=29 | hit=48.3 | miss=51.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.3% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=47 | hit=42.6 | miss=57.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=42.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | BTTS_YES | evaluated=47 | hit=46.8 | miss=53.2 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=46.8% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_2_5 | evaluated=47 | hit=51.1 | miss=48.9 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=51.1% is weak/negative in current calibration.
- API_CAL_RULE_0036 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=26 | hit=26.9 | miss=73.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=26.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0039 | SCORE_BUCKET=SCORE_55_69 | BTTS_YES | evaluated=26 | hit=38.5 | miss=61.5 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=38.5% is weak/negative in current calibration.
- API_CAL_RULE_0041 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=26 | hit=42.3 | miss=57.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=42.3% is weak/negative in current calibration.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=21 | hit=38.1 | miss=61.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=38.1% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=21 | hit=42.9 | miss=57.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=42.9% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=29 | hit=55.2 | miss=44.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=55.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0067 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=29 | hit=48.3 | miss=51.7 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.3% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=29 | hit=48.3 | miss=51.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.3% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=47 | hit=42.6 | miss=57.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=42.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=47 | hit=46.8 | miss=53.2 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=46.8% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=47 | hit=51.1 | miss=48.9 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=51.1% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
