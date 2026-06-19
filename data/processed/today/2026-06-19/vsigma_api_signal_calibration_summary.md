# vSIGMA API Signal Calibration Summary - 2026-06-19

## Summary
- source_rows: 331
- finished_rows: 151
- pending_rows: 180
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=86.0 | evaluated=43
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=86.0 | evaluated=43
- sample_warning_counts: MEDIUM_SAMPLE_UNDER_100=49; LOW_SAMPLE_UNDER_50=14; SAMPLE_OK_100_PLUS=7; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_NEUTRAL=20; CALIBRATION_MEDIUM_OBSERVED_EDGE=16; CALIBRATION_WEAK_OR_NEGATIVE=16; CALIBRATION_STRONG_OBSERVED_EDGE=9; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_STRONG_PROTECTED_MARKET=5; CALIBRATION_MEDIUM_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=151 | HIT=77 | MISS=74 | VOID=0 | hit_rate=51.0 | hit_or_void=51.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=151 | HIT=77 | MISS=38 | VOID=36 | hit_rate=51.0 | hit_or_void=74.8 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=151 | HIT=113 | MISS=38 | VOID=0 | hit_rate=74.8 | hit_or_void=74.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=151 | HIT=74 | MISS=77 | VOID=0 | hit_rate=49.0 | hit_or_void=49.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=151 | HIT=111 | MISS=40 | VOID=0 | hit_rate=73.5 | hit_or_void=73.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=151 | HIT=81 | MISS=70 | VOID=0 | hit_rate=53.6 | hit_or_void=53.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=151 | HIT=99 | MISS=52 | VOID=0 | hit_rate=65.6 | hit_or_void=65.6 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=58 | HIT=34 | MISS=24 | VOID=0 | hit_rate=58.6 | hit_or_void=58.6 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=58 | HIT=34 | MISS=10 | VOID=14 | hit_rate=58.6 | hit_or_void=82.8 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=58 | HIT=48 | MISS=10 | VOID=0 | hit_rate=82.8 | hit_or_void=82.8 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=58 | HIT=24 | MISS=34 | VOID=0 | hit_rate=41.4 | hit_or_void=41.4 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=58 | HIT=43 | MISS=15 | VOID=0 | hit_rate=74.1 | hit_or_void=74.1 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=58 | HIT=27 | MISS=31 | VOID=0 | hit_rate=46.6 | hit_or_void=46.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=58 | HIT=43 | MISS=15 | VOID=0 | hit_rate=74.1 | hit_or_void=74.1 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=93 | HIT=43 | MISS=50 | VOID=0 | hit_rate=46.2 | hit_or_void=46.2 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=93 | HIT=43 | MISS=28 | VOID=22 | hit_rate=46.2 | hit_or_void=69.9 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=93 | HIT=65 | MISS=28 | VOID=0 | hit_rate=69.9 | hit_or_void=69.9 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=93 | HIT=50 | MISS=43 | VOID=0 | hit_rate=53.8 | hit_or_void=53.8 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=93 | HIT=68 | MISS=25 | VOID=0 | hit_rate=73.1 | hit_or_void=73.1 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=93 | HIT=54 | MISS=39 | VOID=0 | hit_rate=58.1 | hit_or_void=58.1 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=93 | HIT=56 | MISS=37 | VOID=0 | hit_rate=60.2 | hit_or_void=60.2 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
