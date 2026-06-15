# vSIGMA API Signal Calibration Summary - 2026-06-15

## Summary
- source_rows: 99
- finished_rows: 76
- pending_rows: 23
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=85.7 | evaluated=21
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=85.7 | evaluated=21
- sample_warning_counts: LOW_SAMPLE_UNDER_50=63; MEDIUM_SAMPLE_UNDER_100=7; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_WEAK_OR_NEGATIVE=22; CALIBRATION_NEUTRAL=20; CALIBRATION_MEDIUM_OBSERVED_EDGE=12; CALIBRATION_STRONG_OBSERVED_EDGE=9; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_STRONG_PROTECTED_MARKET=4; CALIBRATION_MEDIUM_PROTECTED_MARKET=3
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=76 | HIT=36 | MISS=40 | VOID=0 | hit_rate=47.4 | hit_or_void=47.4 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=76 | HIT=36 | MISS=23 | VOID=17 | hit_rate=47.4 | hit_or_void=69.7 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=76 | HIT=53 | MISS=23 | VOID=0 | hit_rate=69.7 | hit_or_void=69.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=76 | HIT=36 | MISS=40 | VOID=0 | hit_rate=47.4 | hit_or_void=47.4 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=76 | HIT=53 | MISS=23 | VOID=0 | hit_rate=69.7 | hit_or_void=69.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=76 | HIT=38 | MISS=38 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=76 | HIT=50 | MISS=26 | VOID=0 | hit_rate=65.8 | hit_or_void=65.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=29 | HIT=16 | MISS=13 | VOID=0 | hit_rate=55.2 | hit_or_void=55.2 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=29 | HIT=16 | MISS=5 | VOID=8 | hit_rate=55.2 | hit_or_void=82.8 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=29 | HIT=24 | MISS=5 | VOID=0 | hit_rate=82.8 | hit_or_void=82.8 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=29 | HIT=14 | MISS=15 | VOID=0 | hit_rate=48.3 | hit_or_void=48.3 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=29 | HIT=23 | MISS=6 | VOID=0 | hit_rate=79.3 | hit_or_void=79.3 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=29 | HIT=14 | MISS=15 | VOID=0 | hit_rate=48.3 | hit_or_void=48.3 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=29 | HIT=19 | MISS=10 | VOID=0 | hit_rate=65.5 | hit_or_void=65.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=47 | HIT=20 | MISS=27 | VOID=0 | hit_rate=42.6 | hit_or_void=42.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=47 | HIT=20 | MISS=18 | VOID=9 | hit_rate=42.6 | hit_or_void=61.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=47 | HIT=29 | MISS=18 | VOID=0 | hit_rate=61.7 | hit_or_void=61.7 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=47 | HIT=22 | MISS=25 | VOID=0 | hit_rate=46.8 | hit_or_void=46.8 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=47 | HIT=30 | MISS=17 | VOID=0 | hit_rate=63.8 | hit_or_void=63.8 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=47 | HIT=24 | MISS=23 | VOID=0 | hit_rate=51.1 | hit_or_void=51.1 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=47 | HIT=31 | MISS=16 | VOID=0 | hit_rate=66.0 | hit_or_void=66.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
