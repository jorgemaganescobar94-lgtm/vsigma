# vSIGMA API Signal Calibration Summary - 2026-06-17

## Summary
- source_rows: 196
- finished_rows: 98
- pending_rows: 98
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=82.1 | evaluated=28
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=82.1 | evaluated=28
- sample_warning_counts: LOW_SAMPLE_UNDER_50=42; MEDIUM_SAMPLE_UNDER_100=28; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_NEUTRAL=21; CALIBRATION_WEAK_OR_NEGATIVE=20; CALIBRATION_MEDIUM_OBSERVED_EDGE=18; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=4; CALIBRATION_STRONG_OBSERVED_EDGE=4; CALIBRATION_STRONG_PROTECTED_MARKET=3
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=98 | HIT=45 | MISS=53 | VOID=0 | hit_rate=45.9 | hit_or_void=45.9 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=98 | HIT=45 | MISS=29 | VOID=24 | hit_rate=45.9 | hit_or_void=70.4 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=98 | HIT=69 | MISS=29 | VOID=0 | hit_rate=70.4 | hit_or_void=70.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=98 | HIT=48 | MISS=50 | VOID=0 | hit_rate=49.0 | hit_or_void=49.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=98 | HIT=68 | MISS=30 | VOID=0 | hit_rate=69.4 | hit_or_void=69.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=98 | HIT=49 | MISS=49 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=98 | HIT=64 | MISS=34 | VOID=0 | hit_rate=65.3 | hit_or_void=65.3 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=39 | HIT=21 | MISS=18 | VOID=0 | hit_rate=53.8 | hit_or_void=53.8 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=39 | HIT=21 | MISS=8 | VOID=10 | hit_rate=53.8 | hit_or_void=79.5 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=39 | HIT=31 | MISS=8 | VOID=0 | hit_rate=79.5 | hit_or_void=79.5 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=39 | HIT=17 | MISS=22 | VOID=0 | hit_rate=43.6 | hit_or_void=43.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=39 | HIT=28 | MISS=11 | VOID=0 | hit_rate=71.8 | hit_or_void=71.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=39 | HIT=17 | MISS=22 | VOID=0 | hit_rate=43.6 | hit_or_void=43.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=39 | HIT=28 | MISS=11 | VOID=0 | hit_rate=71.8 | hit_or_void=71.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=59 | HIT=24 | MISS=35 | VOID=0 | hit_rate=40.7 | hit_or_void=40.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=59 | HIT=24 | MISS=21 | VOID=14 | hit_rate=40.7 | hit_or_void=64.4 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=59 | HIT=38 | MISS=21 | VOID=0 | hit_rate=64.4 | hit_or_void=64.4 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=59 | HIT=31 | MISS=28 | VOID=0 | hit_rate=52.5 | hit_or_void=52.5 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=59 | HIT=40 | MISS=19 | VOID=0 | hit_rate=67.8 | hit_or_void=67.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=59 | HIT=32 | MISS=27 | VOID=0 | hit_rate=54.2 | hit_or_void=54.2 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=59 | HIT=36 | MISS=23 | VOID=0 | hit_rate=61.0 | hit_or_void=61.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
