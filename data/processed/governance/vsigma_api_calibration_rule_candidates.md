# vSIGMA API Calibration Rule Candidates - 2026-06-10

## Summary
- rows_reviewed: 77
- candidate_rows: 8
- block_rows: 20
- observe_rows: 49
- insufficient_sample_rows: 28
- rule_bucket_counts: RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=28; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=20; RULE_OBSERVE_ONLY_SEGMENT=18; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=4; RULE_NEUTRAL_OBSERVE_MORE=3; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=3; RULE_CANDIDATE_TOTAL_MARKET=1
- rule_decision_counts: COLLECT_MORE_SAMPLE=28; OBSERVE_MORE_SEGMENT=18; BLOCK_ML_PROMOTION=7; BLOCK_OVER_2_5_PROMOTION=7; WATCH_ONLY_COLLECT_TO_50_SAMPLE=7; BLOCK_BTTS_YES_PROMOTION=6; OBSERVE_MORE_GLOBAL_MARKET=3; FUTURE_RULE_REVIEW_ONLY=1
- future_rule_candidate_counts: NO_SAMPLE_TOO_SMALL=28; NO_BLOCKED_MARKET=20; NO_SEGMENT_SAMPLE_TOO_SMALL=18; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=7; NO_OBSERVE_MORE=3; YES_REVIEW_ONLY=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=56 | hit=66.1 | hit_or_void=66.1 | miss=33.9 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=66.1% meets total-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=21 | hit=71.4 | hit_or_void=71.4 | miss=28.6 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=71.4% but sample=21 is below 50.
- API_CAL_RULE_0023 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=24 | hit=54.2 | hit_or_void=83.3 | miss=16.7 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=83.3% and miss_rate=16.7% but sample=24 is below 50.
- API_CAL_RULE_0024 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=24 | hit=83.3 | hit_or_void=83.3 | miss=16.7 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=83.3% but sample=24 is below 50.
- API_CAL_RULE_0026 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=24 | hit=79.2 | hit_or_void=79.2 | miss=20.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=79.2% but sample=24 is below 50.
- API_CAL_RULE_0065 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=24 | hit=54.2 | hit_or_void=83.3 | miss=16.7 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=83.3% and miss_rate=16.7% but sample=24 is below 50.
- API_CAL_RULE_0066 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=24 | hit=83.3 | hit_or_void=83.3 | miss=16.7 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=83.3% but sample=24 is below 50.
- API_CAL_RULE_0068 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=24 | hit=79.2 | hit_or_void=79.2 | miss=20.8 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=79.2% but sample=24 is below 50.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=56 | hit=44.6 | miss=55.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=44.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=56 | hit=44.6 | miss=55.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=44.6% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=56 | hit=46.4 | miss=53.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=46.4% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=21 | hit=42.9 | miss=57.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=42.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0013 | PREDICTED_SIDE=AWAY | OVER_2_5 | evaluated=21 | hit=52.4 | miss=47.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=52.4% is weak/negative in current calibration.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=35 | hit=45.7 | miss=54.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=45.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=35 | hit=37.1 | miss=62.9 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=37.1% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=35 | hit=42.9 | miss=57.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=42.9% is weak/negative in current calibration.
- API_CAL_RULE_0022 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=24 | hit=54.2 | miss=45.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=54.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0025 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=24 | hit=50.0 | miss=50.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0027 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=24 | hit=45.8 | miss=54.2 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.8% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=32 | hit=37.5 | miss=62.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=37.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | BTTS_YES | evaluated=32 | hit=40.6 | miss=59.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=40.6% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_2_5 | evaluated=32 | hit=46.9 | miss=53.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=46.9% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=24 | hit=54.2 | miss=45.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=54.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0067 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=24 | hit=50.0 | miss=50.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=24 | hit=45.8 | miss=54.2 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.8% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=32 | hit=37.5 | miss=62.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=37.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=32 | hit=40.6 | miss=59.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=40.6% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=32 | hit=46.9 | miss=53.1 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=46.9% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
