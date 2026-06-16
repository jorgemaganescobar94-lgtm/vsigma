# vSIGMA API Signal Calibration Summary - 2026-06-16

## Summary
- source_rows: 126
- finished_rows: 81
- pending_rows: 45
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=86.4 | evaluated=22
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=86.4 | evaluated=22
- sample_warning_counts: LOW_SAMPLE_UNDER_50=49; MEDIUM_SAMPLE_UNDER_100=21; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_NEUTRAL=26; CALIBRATION_WEAK_OR_NEGATIVE=18; CALIBRATION_STRONG_OBSERVED_EDGE=10; CALIBRATION_MEDIUM_OBSERVED_EDGE=9; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_STRONG_PROTECTED_MARKET=5; CALIBRATION_MEDIUM_PROTECTED_MARKET=2
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=81 | HIT=38 | MISS=43 | VOID=0 | hit_rate=46.9 | hit_or_void=46.9 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=81 | HIT=38 | MISS=24 | VOID=19 | hit_rate=46.9 | hit_or_void=70.4 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=81 | HIT=57 | MISS=24 | VOID=0 | hit_rate=70.4 | hit_or_void=70.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=81 | HIT=40 | MISS=41 | VOID=0 | hit_rate=49.4 | hit_or_void=49.4 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=81 | HIT=57 | MISS=24 | VOID=0 | hit_rate=70.4 | hit_or_void=70.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=81 | HIT=41 | MISS=40 | VOID=0 | hit_rate=50.6 | hit_or_void=50.6 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=81 | HIT=53 | MISS=28 | VOID=0 | hit_rate=65.4 | hit_or_void=65.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=31 | HIT=18 | MISS=13 | VOID=0 | hit_rate=58.1 | hit_or_void=58.1 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=31 | HIT=18 | MISS=5 | VOID=8 | hit_rate=58.1 | hit_or_void=83.9 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=31 | HIT=26 | MISS=5 | VOID=0 | hit_rate=83.9 | hit_or_void=83.9 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=31 | HIT=16 | MISS=15 | VOID=0 | hit_rate=51.6 | hit_or_void=51.6 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=31 | HIT=25 | MISS=6 | VOID=0 | hit_rate=80.6 | hit_or_void=80.6 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=31 | HIT=16 | MISS=15 | VOID=0 | hit_rate=51.6 | hit_or_void=51.6 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=31 | HIT=20 | MISS=11 | VOID=0 | hit_rate=64.5 | hit_or_void=64.5 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=50 | HIT=20 | MISS=30 | VOID=0 | hit_rate=40.0 | hit_or_void=40.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=50 | HIT=20 | MISS=19 | VOID=11 | hit_rate=40.0 | hit_or_void=62.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=50 | HIT=31 | MISS=19 | VOID=0 | hit_rate=62.0 | hit_or_void=62.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=50 | HIT=24 | MISS=26 | VOID=0 | hit_rate=48.0 | hit_or_void=48.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=50 | HIT=32 | MISS=18 | VOID=0 | hit_rate=64.0 | hit_or_void=64.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=50 | HIT=25 | MISS=25 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=50 | HIT=33 | MISS=17 | VOID=0 | hit_rate=66.0 | hit_or_void=66.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
