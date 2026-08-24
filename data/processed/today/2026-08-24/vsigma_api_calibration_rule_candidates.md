# vSIGMA API Calibration Rule Candidates - 2026-08-24

## Summary
- rows_reviewed: 84
- candidate_rows: 28
- block_rows: 21
- observe_rows: 35
- insufficient_sample_rows: 7
- rule_bucket_counts: RULE_OBSERVE_ONLY_SEGMENT=26; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=21; RULE_CANDIDATE_PROTECTED_MARKET=14; RULE_CANDIDATE_TOTAL_MARKET=14; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_NEUTRAL_OBSERVE_MORE=2
- rule_decision_counts: FUTURE_RULE_REVIEW_ONLY=28; OBSERVE_MORE_SEGMENT=26; BLOCK_ML_PROMOTION=11; BLOCK_OVER_2_5_PROMOTION=7; COLLECT_MORE_SAMPLE=7; BLOCK_BTTS_YES_PROMOTION=3; OBSERVE_MORE_GLOBAL_MARKET=2
- future_rule_candidate_counts: YES_REVIEW_ONLY=28; NO_SEGMENT_SAMPLE_TOO_SMALL=26; NO_BLOCKED_MARKET=21; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=2
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=84
- pick_permission_counts: NO_PICK_PERMISSION=84
- stake_permission_counts: NO_STAKE_PERMISSION=84
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Candidate Rules
- API_CAL_RULE_0002 | ALL=ALL | API_DNB | evaluated=354 | hit=51.7 | hit_or_void=78.0 | miss=22.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=78.0% and miss_rate=22.0% meet protected-market threshold.
- API_CAL_RULE_0003 | ALL=ALL | API_DOUBLE_CHANCE | evaluated=354 | hit=78.0 | hit_or_void=78.0 | miss=22.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=78.0% meets protected-market threshold.
- API_CAL_RULE_0005 | ALL=ALL | OVER_1_5 | evaluated=355 | hit=76.9 | hit_or_void=76.9 | miss=23.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.9% meets total-market threshold.
- API_CAL_RULE_0009 | PREDICTED_SIDE=AWAY | API_DNB | evaluated=177 | hit=49.7 | hit_or_void=78.0 | miss=22.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=78.0% and miss_rate=22.0% meet protected-market threshold.
- API_CAL_RULE_0010 | PREDICTED_SIDE=AWAY | API_DOUBLE_CHANCE | evaluated=177 | hit=78.0 | hit_or_void=78.0 | miss=22.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=78.0% meets protected-market threshold.
- API_CAL_RULE_0012 | PREDICTED_SIDE=AWAY | OVER_1_5 | evaluated=177 | hit=81.4 | hit_or_void=81.4 | miss=18.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=81.4% meets total-market threshold.
- API_CAL_RULE_0016 | PREDICTED_SIDE=HOME | API_DNB | evaluated=177 | hit=53.7 | hit_or_void=78.0 | miss=22.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=78.0% and miss_rate=22.0% meet protected-market threshold.
- API_CAL_RULE_0017 | PREDICTED_SIDE=HOME | API_DOUBLE_CHANCE | evaluated=177 | hit=78.0 | hit_or_void=78.0 | miss=22.0 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=78.0% meets protected-market threshold.
- API_CAL_RULE_0019 | PREDICTED_SIDE=HOME | OVER_1_5 | evaluated=177 | hit=72.9 | hit_or_void=72.9 | miss=27.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=72.9% meets total-market threshold.
- API_CAL_RULE_0021 | PREDICTED_SIDE=HOME | UNDER_3_5 | evaluated=177 | hit=71.2 | hit_or_void=71.2 | miss=28.8 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=71.2% meets total-market threshold.
- API_CAL_RULE_0030 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | evaluated=178 | hit=51.1 | hit_or_void=81.5 | miss=18.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=81.5% and miss_rate=18.5% meet protected-market threshold.
- API_CAL_RULE_0031 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | evaluated=178 | hit=81.5 | hit_or_void=81.5 | miss=18.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=81.5% meets protected-market threshold.
- API_CAL_RULE_0033 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_1_5 | evaluated=179 | hit=76.5 | hit_or_void=76.5 | miss=23.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.5% meets total-market threshold.
- API_CAL_RULE_0035 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | UNDER_3_5 | evaluated=179 | hit=72.6 | hit_or_void=72.6 | miss=27.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=72.6% meets total-market threshold.
- API_CAL_RULE_0040 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | OVER_1_5 | evaluated=176 | hit=77.3 | hit_or_void=77.3 | miss=22.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.3% meets total-market threshold.
- API_CAL_RULE_0047 | SCORE_BUCKET=SCORE_55_69 | OVER_1_5 | evaluated=81 | hit=70.4 | hit_or_void=70.4 | miss=29.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=70.4% meets total-market threshold.
- API_CAL_RULE_0051 | SCORE_BUCKET=SCORE_70_79 | API_DNB | evaluated=108 | hit=56.5 | hit_or_void=76.9 | miss=23.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=76.9% and miss_rate=23.1% meet protected-market threshold.
- API_CAL_RULE_0052 | SCORE_BUCKET=SCORE_70_79 | API_DOUBLE_CHANCE | evaluated=108 | hit=76.9 | hit_or_void=76.9 | miss=23.1 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=76.9% meets protected-market threshold.
- API_CAL_RULE_0054 | SCORE_BUCKET=SCORE_70_79 | OVER_1_5 | evaluated=108 | hit=80.6 | hit_or_void=80.6 | miss=19.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=80.6% meets total-market threshold.
- API_CAL_RULE_0065 | SCORE_BUCKET=SCORE_90_PLUS | API_DNB | evaluated=135 | hit=54.1 | hit_or_void=87.4 | miss=12.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=87.4% and miss_rate=12.6% meet protected-market threshold.
- API_CAL_RULE_0066 | SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | evaluated=135 | hit=87.4 | hit_or_void=87.4 | miss=12.6 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=87.4% meets protected-market threshold.
- API_CAL_RULE_0068 | SCORE_BUCKET=SCORE_90_PLUS | OVER_1_5 | evaluated=135 | hit=80.7 | hit_or_void=80.7 | miss=19.3 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=80.7% meets total-market threshold.
- API_CAL_RULE_0070 | SCORE_BUCKET=SCORE_90_PLUS | UNDER_3_5 | evaluated=135 | hit=76.3 | hit_or_void=76.3 | miss=23.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=76.3% meets total-market threshold.
- API_CAL_RULE_0072 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DNB | evaluated=178 | hit=51.1 | hit_or_void=81.5 | miss=18.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API DNB hit_or_void=81.5% and miss_rate=18.5% meet protected-market threshold.
- API_CAL_RULE_0073 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=178 | hit=81.5 | hit_or_void=81.5 | miss=18.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=API double chance hit_rate=81.5% meets protected-market threshold.
- API_CAL_RULE_0075 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=179 | hit=76.5 | hit_or_void=76.5 | miss=23.5 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=76.5% meets total-market threshold.
- API_CAL_RULE_0077 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=179 | hit=72.6 | hit_or_void=72.6 | miss=27.4 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Under 3.5 hit_rate=72.6% meets total-market threshold.
- API_CAL_RULE_0082 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=176 | hit=77.3 | hit_or_void=77.3 | miss=22.7 | decision=FUTURE_RULE_REVIEW_ONLY | permission=NO_RULE_ACTIVATION_PERMISSION | reason=Over 1.5 hit_rate=77.3% meets total-market threshold.

## Block Rules
- API_CAL_RULE_0001 | ALL=ALL | API_1X2 | evaluated=354 | hit=51.7 | miss=48.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=51.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0006 | ALL=ALL | OVER_2_5 | evaluated=355 | hit=51.3 | miss=48.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=51.3% is weak/negative in current calibration.
- API_CAL_RULE_0008 | PREDICTED_SIDE=AWAY | API_1X2 | evaluated=177 | hit=49.7 | miss=50.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=49.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0015 | PREDICTED_SIDE=HOME | API_1X2 | evaluated=177 | hit=53.7 | miss=46.3 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=53.7% is below the 60% minimum for any ML review.
- API_CAL_RULE_0018 | PREDICTED_SIDE=HOME | BTTS_YES | evaluated=177 | hit=50.3 | miss=49.7 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=50.3% is weak/negative in current calibration.
- API_CAL_RULE_0020 | PREDICTED_SIDE=HOME | OVER_2_5 | evaluated=177 | hit=45.2 | miss=54.8 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.2% is weak/negative in current calibration.
- API_CAL_RULE_0029 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_1X2 | evaluated=178 | hit=51.1 | miss=48.9 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=51.1% is below the 60% minimum for any ML review.
- API_CAL_RULE_0034 | REVIEW_PRIORITY=P1_MANUAL_REVIEW | OVER_2_5 | evaluated=179 | hit=45.3 | miss=54.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.3% is weak/negative in current calibration.
- API_CAL_RULE_0036 | REVIEW_PRIORITY=P2_MANUAL_REVIEW | API_1X2 | evaluated=176 | hit=52.3 | miss=47.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0043 | SCORE_BUCKET=SCORE_55_69 | API_1X2 | evaluated=81 | hit=44.4 | miss=55.6 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=44.4% is below the 60% minimum for any ML review.
- API_CAL_RULE_0048 | SCORE_BUCKET=SCORE_55_69 | OVER_2_5 | evaluated=81 | hit=53.1 | miss=46.9 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=53.1% is weak/negative in current calibration.
- API_CAL_RULE_0050 | SCORE_BUCKET=SCORE_70_79 | API_1X2 | evaluated=108 | hit=56.5 | miss=43.5 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=56.5% is below the 60% minimum for any ML review.
- API_CAL_RULE_0053 | SCORE_BUCKET=SCORE_70_79 | BTTS_YES | evaluated=108 | hit=54.6 | miss=45.4 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=54.6% is weak/negative in current calibration.
- API_CAL_RULE_0057 | SCORE_BUCKET=SCORE_80_89 | API_1X2 | evaluated=30 | hit=43.3 | miss=56.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=43.3% is below the 60% minimum for any ML review.
- API_CAL_RULE_0060 | SCORE_BUCKET=SCORE_80_89 | BTTS_YES | evaluated=31 | hit=48.4 | miss=51.6 | decision=BLOCK_BTTS_YES_PROMOTION | reason=BTTS_YES hit_rate=48.4% is weak/negative in current calibration.
- API_CAL_RULE_0062 | SCORE_BUCKET=SCORE_80_89 | OVER_2_5 | evaluated=31 | hit=48.4 | miss=51.6 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=48.4% is weak/negative in current calibration.
- API_CAL_RULE_0064 | SCORE_BUCKET=SCORE_90_PLUS | API_1X2 | evaluated=135 | hit=54.1 | miss=45.9 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=54.1% is below the 60% minimum for any ML review.
- API_CAL_RULE_0069 | SCORE_BUCKET=SCORE_90_PLUS | OVER_2_5 | evaluated=135 | hit=43.7 | miss=56.3 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=43.7% is weak/negative in current calibration.
- API_CAL_RULE_0071 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=178 | hit=51.1 | miss=48.9 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=51.1% is below the 60% minimum for any ML review.
- API_CAL_RULE_0076 | SIGNAL_BAND=HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=179 | hit=45.3 | miss=54.7 | decision=BLOCK_OVER_2_5_PROMOTION | reason=OVER_2_5 hit_rate=45.3% is weak/negative in current calibration.
- API_CAL_RULE_0078 | SIGNAL_BAND=MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=176 | hit=52.3 | miss=47.7 | decision=BLOCK_ML_PROMOTION | reason=API 1X2 hit_rate=52.3% is below the 60% minimum for any ML review.

## Guardrails
- This board is rule-design only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future rule must be implemented separately after enough sample size exists and after explicit review.
