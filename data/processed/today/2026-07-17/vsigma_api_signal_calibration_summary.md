# vSIGMA API Signal Calibration Summary - 2026-07-17

## Summary
- source_rows: 655
- finished_rows: 301
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=85.4 | evaluated=96
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=85.4 | evaluated=96
- sample_warning_counts: SAMPLE_OK_100_PLUS=56; MEDIUM_SAMPLE_UNDER_100=14; INSUFFICIENT_SAMPLE_UNDER_20=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=32; CALIBRATION_MEDIUM_OBSERVED_EDGE=17; CALIBRATION_STRONG_OBSERVED_EDGE=12; CALIBRATION_STRONG_PROTECTED_MARKET=7; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_WEAK_OR_NEGATIVE=5; CALIBRATION_MEDIUM_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=300 | HIT=166 | MISS=134 | VOID=0 | hit_rate=55.3 | hit_or_void=55.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=300 | HIT=166 | MISS=74 | VOID=60 | hit_rate=55.3 | hit_or_void=75.3 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=300 | HIT=226 | MISS=74 | VOID=0 | hit_rate=75.3 | hit_or_void=75.3 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=301 | HIT=162 | MISS=139 | VOID=0 | hit_rate=53.8 | hit_or_void=53.8 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=301 | HIT=224 | MISS=77 | VOID=0 | hit_rate=74.4 | hit_or_void=74.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=301 | HIT=172 | MISS=129 | VOID=0 | hit_rate=57.1 | hit_or_void=57.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=301 | HIT=193 | MISS=108 | VOID=0 | hit_rate=64.1 | hit_or_void=64.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=138 | HIT=85 | MISS=53 | VOID=0 | hit_rate=61.6 | hit_or_void=61.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=138 | HIT=85 | MISS=29 | VOID=24 | hit_rate=61.6 | hit_or_void=79.0 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=138 | HIT=109 | MISS=29 | VOID=0 | hit_rate=79.0 | hit_or_void=79.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=139 | HIT=69 | MISS=70 | VOID=0 | hit_rate=49.6 | hit_or_void=49.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=139 | HIT=101 | MISS=38 | VOID=0 | hit_rate=72.7 | hit_or_void=72.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=139 | HIT=76 | MISS=63 | VOID=0 | hit_rate=54.7 | hit_or_void=54.7 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=139 | HIT=93 | MISS=46 | VOID=0 | hit_rate=66.9 | hit_or_void=66.9 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=162 | HIT=81 | MISS=81 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=162 | HIT=81 | MISS=45 | VOID=36 | hit_rate=50.0 | hit_or_void=72.2 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=162 | HIT=117 | MISS=45 | VOID=0 | hit_rate=72.2 | hit_or_void=72.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=162 | HIT=93 | MISS=69 | VOID=0 | hit_rate=57.4 | hit_or_void=57.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=162 | HIT=123 | MISS=39 | VOID=0 | hit_rate=75.9 | hit_or_void=75.9 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=162 | HIT=96 | MISS=66 | VOID=0 | hit_rate=59.3 | hit_or_void=59.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=162 | HIT=100 | MISS=62 | VOID=0 | hit_rate=61.7 | hit_or_void=61.7 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
