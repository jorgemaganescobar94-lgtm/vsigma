# vSIGMA API Calibration Rule Candidates - 2026-06-15

## Summary
- rows_reviewed: 77
- candidate_rows: 9
- block_rows: 22
- observe_rows: 46
- insufficient_sample_rows: 21
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=22; RULE_OBSERVE_ONLY_SEGMENT=22; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=21; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=4; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=4; RULE_NEUTRAL_OBSERVE_MORE=3; RULE_CANDIDATE_TOTAL_MARKET=1
- rule_decision_counts: OBSERVE_MORE_SEGMENT=22; COLLECT_MORE_SAMPLE=21; BLOCK_ML_PROMOTION=8; WATCH_ONLY_COLLECT_TO_50_SAMPLE=8; BLOCK_BTTS_YES_PROMOTION=7; BLOCK_OVER_2_5_PROMOTION=7; OBSERVE_MORE_GLOBAL_MARKET=3; FUTURE_RULE_REVIEW_ONLY=1
- future_rule_candidate_counts: NO_BLOCKED_MARKET=22; NO_SEGMENT_SAMPLE_TOO_SMALL=22; NO_SAMPLE_TOO_SMALL=21; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=8; NO_OBSERVE_MORE=3; YES_REVIEW_ONLY=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=64 | hit=68.8 | hit_or_void=68.8 | miss=31.2 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=68.8% meets total-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=25 | hit=76.0 | hit_or_void=76.0 | miss=24.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.0% but sample=25 is below 50.
- API_CAL_RULE_0023 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=25 | hit=52.0 | hit_or_void=80.0 | miss=20.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=80.0% and miss_rate=20.0% but sample=25 is below 50.
- API_CAL_RULE_0024 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=25 | hit=80.0 | hit_or_void=80.0 | miss=20.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=80.0% but sample=25 is below 50.
- API_CAL_RULE_0026 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=25 | hit=80.0 | hit_or_void=80.0 | miss=20.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=80.0% but sample=25 is below 50.
- API_CAL_RULE_0042 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=22 | hit=77.3 | hit_or_void=77.3 | miss=22.7 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=77.3% but sample=22 is below 50.
- API_CAL_RULE_0065 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=25 | hit=52.0 | hit_or_void=80.0 | miss=20.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=80.0% and miss_rate=20.0% but sample=25 is below 50.
- API_CAL_RULE_0066 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=25 | hit=80.0 | hit_or_void=80.0 | miss=20.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=80.0% but sample=25 is below 50.
- API_CAL_RULE_0068 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=25 | hit=80.0 | hit_or_void=80.0 | miss=20.0 | decision=WATCH_ONLY_COLLECT_TO_50_SAMPLE | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=80.0% but sample=25 is below 50.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=64 | hit=46.9 | miss=53.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=46.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=64 | hit=46.9 | miss=53.1 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=46.9% is weak/negative in current calibration.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=64 | hit=50.0 | miss=50.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=25 | hit=44.0 | miss=56.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=44.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=39 | hit=48.7 | miss=51.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=48.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=39 | hit=41.0 | miss=59.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=41.0% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=39 | hit=46.2 | miss=53.8 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=46.2% is weak/negative in current calibration.
- API_CAL_RULE_0022 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=25 | hit=52.0 | miss=48.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0025 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=25 | hit=48.0 | miss=52.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.0% is weak/negative in current calibration.
- API_CAL_RULE_0027 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=25 | hit=48.0 | miss=52.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.0% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=39 | hit=43.6 | miss=56.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=43.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | BTTS_YES | evaluated=39 | hit=46.2 | miss=53.8 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=46.2% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_2_5 | evaluated=39 | hit=51.3 | miss=48.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=51.3% is weak/negative in current calibration.
- API_CAL_RULE_0036 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=22 | hit=27.3 | miss=72.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=27.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0039 | SCORE_BUCKET=SCORE_55_69 | BTTS_YES | evaluated=22 | hit=36.4 | miss=63.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=36.4% is weak/negative in current calibration.
- API_CAL_RULE_0041 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=22 | hit=36.4 | miss=63.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=36.4% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=25 | hit=52.0 | miss=48.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0067 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=25 | hit=48.0 | miss=52.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.0% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=25 | hit=48.0 | miss=52.0 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.0% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=39 | hit=43.6 | miss=56.4 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=43.6% is below the 60% minimum for any ML review.
- API_CAL_RULE_0074 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=39 | hit=46.2 | miss=53.8 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=46.2% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=39 | hit=51.3 | miss=48.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=51.3% is weak/negative in current calibration.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
