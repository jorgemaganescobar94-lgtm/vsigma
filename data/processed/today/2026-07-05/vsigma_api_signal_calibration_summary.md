# vSIGMA API Signal Calibration Summary - 2026-07-05

## Summary
- source_rows: 641
- finished_rows: 287
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=85.9 | evaluated=85
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=85.9 | evaluated=85
- sample_warning_counts: SAMPLE_OK_100_PLUS=56; MEDIUM_SAMPLE_UNDER_100=14; INSUFFICIENT_SAMPLE_UNDER_20=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=31; CALIBRATION_MEDIUM_OBSERVED_EDGE=17; CALIBRATION_STRONG_OBSERVED_EDGE=11; CALIBRATION_WEAK_OR_NEGATIVE=7; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_STRONG_PROTECTED_MARKET=6; CALIBRATION_MEDIUM_PROTECTED_MARKET=5
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=286 | HIT=155 | MISS=131 | VOID=0 | hit_rate=54.2 | hit_or_void=54.2 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=286 | HIT=155 | MISS=71 | VOID=60 | hit_rate=54.2 | hit_or_void=75.2 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=286 | HIT=215 | MISS=71 | VOID=0 | hit_rate=75.2 | hit_or_void=75.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=287 | HIT=155 | MISS=132 | VOID=0 | hit_rate=54.0 | hit_or_void=54.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=287 | HIT=213 | MISS=74 | VOID=0 | hit_rate=74.2 | hit_or_void=74.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=287 | HIT=161 | MISS=126 | VOID=0 | hit_rate=56.1 | hit_or_void=56.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=287 | HIT=184 | MISS=103 | VOID=0 | hit_rate=64.1 | hit_or_void=64.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=125 | HIT=75 | MISS=50 | VOID=0 | hit_rate=60.0 | hit_or_void=60.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=125 | HIT=75 | MISS=26 | VOID=24 | hit_rate=60.0 | hit_or_void=79.2 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=125 | HIT=99 | MISS=26 | VOID=0 | hit_rate=79.2 | hit_or_void=79.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=126 | HIT=63 | MISS=63 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=126 | HIT=91 | MISS=35 | VOID=0 | hit_rate=72.2 | hit_or_void=72.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=126 | HIT=66 | MISS=60 | VOID=0 | hit_rate=52.4 | hit_or_void=52.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=126 | HIT=85 | MISS=41 | VOID=0 | hit_rate=67.5 | hit_or_void=67.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=161 | HIT=80 | MISS=81 | VOID=0 | hit_rate=49.7 | hit_or_void=49.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=161 | HIT=80 | MISS=45 | VOID=36 | hit_rate=49.7 | hit_or_void=72.0 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=161 | HIT=116 | MISS=45 | VOID=0 | hit_rate=72.0 | hit_or_void=72.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=161 | HIT=92 | MISS=69 | VOID=0 | hit_rate=57.1 | hit_or_void=57.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=161 | HIT=122 | MISS=39 | VOID=0 | hit_rate=75.8 | hit_or_void=75.8 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=161 | HIT=95 | MISS=66 | VOID=0 | hit_rate=59.0 | hit_or_void=59.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=161 | HIT=99 | MISS=62 | VOID=0 | hit_rate=61.5 | hit_or_void=61.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
