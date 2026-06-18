# vSIGMA API Signal Calibration Summary - 2026-06-18

## Summary
- source_rows: 273
- finished_rows: 141
- pending_rows: 132
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=85.4 | evaluated=41
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=85.4 | evaluated=41
- sample_warning_counts: MEDIUM_SAMPLE_UNDER_100=49; LOW_SAMPLE_UNDER_50=14; SAMPLE_OK_100_PLUS=7; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_NEUTRAL=21; CALIBRATION_WEAK_OR_NEGATIVE=16; CALIBRATION_MEDIUM_OBSERVED_EDGE=16; CALIBRATION_STRONG_OBSERVED_EDGE=8; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=5; CALIBRATION_STRONG_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=141 | HIT=68 | MISS=73 | VOID=0 | hit_rate=48.2 | hit_or_void=48.2 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=141 | HIT=68 | MISS=38 | VOID=35 | hit_rate=48.2 | hit_or_void=73.0 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=141 | HIT=103 | MISS=38 | VOID=0 | hit_rate=73.0 | hit_or_void=73.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=141 | HIT=69 | MISS=72 | VOID=0 | hit_rate=48.9 | hit_or_void=48.9 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=141 | HIT=104 | MISS=37 | VOID=0 | hit_rate=73.8 | hit_or_void=73.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=141 | HIT=74 | MISS=67 | VOID=0 | hit_rate=52.5 | hit_or_void=52.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=141 | HIT=94 | MISS=47 | VOID=0 | hit_rate=66.7 | hit_or_void=66.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=55 | HIT=31 | MISS=24 | VOID=0 | hit_rate=56.4 | hit_or_void=56.4 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=55 | HIT=31 | MISS=10 | VOID=14 | hit_rate=56.4 | hit_or_void=81.8 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=55 | HIT=45 | MISS=10 | VOID=0 | hit_rate=81.8 | hit_or_void=81.8 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=55 | HIT=23 | MISS=32 | VOID=0 | hit_rate=41.8 | hit_or_void=41.8 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=55 | HIT=41 | MISS=14 | VOID=0 | hit_rate=74.5 | hit_or_void=74.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=55 | HIT=25 | MISS=30 | VOID=0 | hit_rate=45.5 | hit_or_void=45.5 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=55 | HIT=41 | MISS=14 | VOID=0 | hit_rate=74.5 | hit_or_void=74.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=86 | HIT=37 | MISS=49 | VOID=0 | hit_rate=43.0 | hit_or_void=43.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=86 | HIT=37 | MISS=28 | VOID=21 | hit_rate=43.0 | hit_or_void=67.4 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=86 | HIT=58 | MISS=28 | VOID=0 | hit_rate=67.4 | hit_or_void=67.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=86 | HIT=46 | MISS=40 | VOID=0 | hit_rate=53.5 | hit_or_void=53.5 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=86 | HIT=63 | MISS=23 | VOID=0 | hit_rate=73.3 | hit_or_void=73.3 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=86 | HIT=49 | MISS=37 | VOID=0 | hit_rate=57.0 | hit_or_void=57.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=86 | HIT=53 | MISS=33 | VOID=0 | hit_rate=61.6 | hit_or_void=61.6 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
