# vSIGMA API Calibration Rule Candidates - 2026-07-01

## Summary
- rows_reviewed: 84
- candidate_rows: 24
- block_rows: 20
- observe_rows: 40
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_OBSERVE_ONLY_SEGMENT=31; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=20; RULE_CANDIDATE_PROTECTED_MARKET=12; RULE_CANDIDATE_TOTAL_MARKET=12; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_NEUTRAL_OBSERVE_MORE=2
- rule_decision_counts: OBSERVE_MORE_SEGMENT=31; FUTURE_RULE_REVIEW_ONLY=24; BLOCK_ML_PROMOTION=8; COLLECT_MORE_SAMPLE=7; BLOCK_BTTS_YES_PROMOTION=6; BLOCK_OVER_2_5_PROMOTION=6; OBSERVE_MORE_GLOBAL_MARKET=2
- future_rule_candidate_counts: NO_SEGMENT_SAMPLE_TOO_SMALL=31; YES_REVIEW_ONLY=24; NO_BLOCKED_MARKET=20; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=2
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=84
- pick_permission_counts: NO_PICK_PERMISSION=84
- stake_permission_counts: NO_STAKE_PERMISSION=84
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0002 | ALL=ALL | API_DNB | evaluated=283 | hit=54.4 | hit_or_void=75.3 | miss=24.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.3% and miss_rate=24.7% meet protected-market threshold.
- API_CAL_RULE_0003 | ALL=ALL | API_DOUBLE_CHANCE | evaluated=283 | hit=75.3 | hit_or_void=75.3 | miss=24.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.3% meets protected-market threshold.
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=284 | hit=74.3 | hit_or_void=74.3 | miss=25.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=74.3% meets total-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=133 | hit=78.2 | hit_or_void=78.2 | miss=21.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=78.2% meets total-market threshold.
- API_CAL_RULE_0016 | PREDICTED_SIDE=HOME | API_DNB | evaluated=150 | hit=56.7 | hit_or_void=76.0 | miss=24.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.0% and miss_rate=24.0% meet protected-market threshold.
- API_CAL_RULE_0017 | PREDICTED_SIDE=HOME | API_DOUBLE_CHANCE | evaluated=150 | hit=76.0 | hit_or_void=76.0 | miss=24.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.0% meets protected-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=150 | hit=71.3 | hit_or_void=71.3 | miss=28.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=71.3% meets total-market threshold.
- API_CAL_RULE_0030 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=123 | hit=60.2 | hit_or_void=79.7 | miss=20.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=79.7% and miss_rate=20.3% meet protected-market threshold.
- API_CAL_RULE_0031 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=123 | hit=79.7 | hit_or_void=79.7 | miss=20.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=79.7% meets protected-market threshold.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=124 | hit=72.6 | hit_or_void=72.6 | miss=27.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.6% meets total-market threshold.
- API_CAL_RULE_0040 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=160 | hit=75.6 | hit_or_void=75.6 | miss=24.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.6% meets total-market threshold.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_55_69 | OVER_1_5 | evaluated=73 | hit=68.5 | hit_or_void=68.5 | miss=31.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=68.5% meets total-market threshold.
- API_CAL_RULE_0049 | SCORE_BUCKET=SCORE_55_69 | UNDER_3_5 | evaluated=73 | hit=72.6 | hit_or_void=72.6 | miss=27.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=72.6% meets total-market threshold.
- API_CAL_RULE_0051 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=100 | hit=56.0 | hit_or_void=75.0 | miss=25.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=75.0% and miss_rate=25.0% meet protected-market threshold.
- API_CAL_RULE_0052 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=100 | hit=75.0 | hit_or_void=75.0 | miss=25.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=75.0% meets protected-market threshold.
- API_CAL_RULE_0054 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=100 | hit=79.0 | hit_or_void=79.0 | miss=21.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=79.0% meets total-market threshold.
- API_CAL_RULE_0065 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=84 | hit=67.9 | hit_or_void=85.7 | miss=14.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=85.7% and miss_rate=14.3% meet protected-market threshold.
- API_CAL_RULE_0066 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=84 | hit=85.7 | hit_or_void=85.7 | miss=14.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=85.7% meets protected-market threshold.
- API_CAL_RULE_0068 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=84 | hit=77.4 | hit_or_void=77.4 | miss=22.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.4% meets total-market threshold.
- API_CAL_RULE_0070 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=84 | hit=70.2 | hit_or_void=70.2 | miss=29.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=70.2% meets total-market threshold.
- API_CAL_RULE_0072 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=123 | hit=60.2 | hit_or_void=79.7 | miss=20.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=79.7% and miss_rate=20.3% meet protected-market threshold.
- API_CAL_RULE_0073 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=123 | hit=79.7 | hit_or_void=79.7 | miss=20.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=79.7% meets protected-market threshold.
- API_CAL_RULE_0075 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=124 | hit=72.6 | hit_or_void=72.6 | miss=27.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.6% meets total-market threshold.
- API_CAL_RULE_0082 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=160 | hit=75.6 | hit_or_void=75.6 | miss=24.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=75.6% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=283 | hit=54.4 | miss=45.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=54.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0004 | ALL=ALL | BTTS_YES | evaluated=284 | hit=53.9 | miss=46.1 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=53.9% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=133 | hit=51.9 | miss=48.1 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=51.9% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=150 | hit=56.7 | miss=43.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=56.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=150 | hit=48.7 | miss=51.3 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.7% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=150 | hit=50.7 | miss=49.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=50.7% is weak/negative in current calibration.
- API_CAL_RULE_0032 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | BTTS_YES | evaluated=124 | hit=50.0 | miss=50.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=124 | hit=52.4 | miss=47.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=52.4% is weak/negative in current calibration.
- API_CAL_RULE_0036 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=160 | hit=50.0 | miss=50.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=50.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=73 | hit=39.7 | miss=60.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=39.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0048 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=73 | hit=49.3 | miss=50.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=49.3% is weak/negative in current calibration.
- API_CAL_RULE_0050 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=100 | hit=56.0 | miss=44.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=56.0% is below the 60% minimum for any ML review.
- API_CAL_RULE_0057 | SCORE_BUCKET=SCORE_80_89 | API_1X2 | evaluated=26 | hit=46.2 | miss=53.8 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=46.2% is below the 60% minimum for any ML review.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_80_89 | BTTS_YES | evaluated=27 | hit=44.4 | miss=55.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=44.4% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_80_89 | OVER_2_5 | evaluated=27 | hit=44.4 | miss=55.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=44.4% is weak/negative in current calibration.
- API_CAL_RULE_0067 | SCORE_BUCKET=SCORE_90_PLUS | BTTS_YES | evaluated=84 | hit=52.4 | miss=47.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=52.4% is weak/negative in current calibration.
- API_CAL_RULE_0069 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=84 | hit=54.8 | miss=45.2 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=54.8% is weak/negative in current calibration.
- API_CAL_RULE_0074 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=124 | hit=50.0 | miss=50.0 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.0% is weak/negative in current calibration.
- API_CAL_RULE_0076 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=124 | hit=52.4 | miss=47.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=52.4% is weak/negative in current calibration.
- API_CAL_RULE_0078 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=160 | hit=50.0 | miss=50.0 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=50.0% is below the 60% minimum for any ML review.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
