# vSIGMA API Signal Calibration Summary - 2026-06-20

## Summary
- source_rows: 331
- finished_rows: 165
- pending_rows: 166
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=87.0 | evaluated=46
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=87.0 | evaluated=46
- sample_warning_counts: MEDIUM_SAMPLE_UNDER_100=35; SAMPLE_OK_100_PLUS=21; LOW_SAMPLE_UNDER_50=14; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_NEUTRAL=20; CALIBRATION_MEDIUM_OBSERVED_EDGE=16; CALIBRATION_WEAK_OR_NEGATIVE=15; CALIBRATION_STRONG_OBSERVED_EDGE=10; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_STRONG_PROTECTED_MARKET=6; CALIBRATION_MEDIUM_PROTECTED_MARKET=3
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=165 | HIT=87 | MISS=78 | VOID=0 | hit_rate=52.7 | hit_or_void=52.7 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=165 | HIT=87 | MISS=41 | VOID=37 | hit_rate=52.7 | hit_or_void=75.2 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=165 | HIT=124 | MISS=41 | VOID=0 | hit_rate=75.2 | hit_or_void=75.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=165 | HIT=82 | MISS=83 | VOID=0 | hit_rate=49.7 | hit_or_void=49.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=165 | HIT=121 | MISS=44 | VOID=0 | hit_rate=73.3 | hit_or_void=73.3 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=165 | HIT=89 | MISS=76 | VOID=0 | hit_rate=53.9 | hit_or_void=53.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=165 | HIT=108 | MISS=57 | VOID=0 | hit_rate=65.5 | hit_or_void=65.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=62 | HIT=37 | MISS=25 | VOID=0 | hit_rate=59.7 | hit_or_void=59.7 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=62 | HIT=37 | MISS=11 | VOID=14 | hit_rate=59.7 | hit_or_void=82.3 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=62 | HIT=51 | MISS=11 | VOID=0 | hit_rate=82.3 | hit_or_void=82.3 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=62 | HIT=27 | MISS=35 | VOID=0 | hit_rate=43.5 | hit_or_void=43.5 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=62 | HIT=46 | MISS=16 | VOID=0 | hit_rate=74.2 | hit_or_void=74.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=62 | HIT=30 | MISS=32 | VOID=0 | hit_rate=48.4 | hit_or_void=48.4 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=62 | HIT=46 | MISS=16 | VOID=0 | hit_rate=74.2 | hit_or_void=74.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=103 | HIT=50 | MISS=53 | VOID=0 | hit_rate=48.5 | hit_or_void=48.5 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=103 | HIT=50 | MISS=30 | VOID=23 | hit_rate=48.5 | hit_or_void=70.9 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=103 | HIT=73 | MISS=30 | VOID=0 | hit_rate=70.9 | hit_or_void=70.9 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=103 | HIT=55 | MISS=48 | VOID=0 | hit_rate=53.4 | hit_or_void=53.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=103 | HIT=75 | MISS=28 | VOID=0 | hit_rate=72.8 | hit_or_void=72.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=103 | HIT=59 | MISS=44 | VOID=0 | hit_rate=57.3 | hit_or_void=57.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=103 | HIT=62 | MISS=41 | VOID=0 | hit_rate=60.2 | hit_or_void=60.2 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
