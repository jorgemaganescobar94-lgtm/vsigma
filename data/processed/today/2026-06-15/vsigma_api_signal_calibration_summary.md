# vSIGMA API Signal Calibration Summary - 2026-06-15

## Summary
- source_rows: 99
- finished_rows: 64
- pending_rows: 35
- summary_rows: 77
- top_market_by_hit_rate: REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | hit_rate_pct=80.0 | evaluated=25
- top_market_by_hit_or_void_rate: REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | hit_or_void_rate_pct=80.0 | evaluated=25
- sample_warning_counts: LOW_SAMPLE_UNDER_50=49; INSUFFICIENT_SAMPLE_UNDER_20=21; MEDIUM_SAMPLE_UNDER_100=7
- calibration_status_counts: CALIBRATION_OBSERVE_ONLY=21; CALIBRATION_WEAK_OR_NEGATIVE=20; CALIBRATION_NEUTRAL=20; CALIBRATION_STRONG_OBSERVED_EDGE=6; CALIBRATION_MEDIUM_OBSERVED_EDGE=5; CALIBRATION_MEDIUM_PROTECTED_MARKET=3; CALIBRATION_STRONG_PROTECTED_MARKET=2
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=64 | HIT=30 | MISS=34 | VOID=0 | hit_rate=46.9 | hit_or_void=46.9 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=64 | HIT=30 | MISS=20 | VOID=14 | hit_rate=46.9 | hit_or_void=68.8 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=64 | HIT=44 | MISS=20 | VOID=0 | hit_rate=68.8 | hit_or_void=68.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=64 | HIT=30 | MISS=34 | VOID=0 | hit_rate=46.9 | hit_or_void=46.9 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=64 | HIT=44 | MISS=20 | VOID=0 | hit_rate=68.8 | hit_or_void=68.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=64 | HIT=32 | MISS=32 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=64 | HIT=41 | MISS=23 | VOID=0 | hit_rate=64.1 | hit_or_void=64.1 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=25 | HIT=13 | MISS=12 | VOID=0 | hit_rate=52.0 | hit_or_void=52.0 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=25 | HIT=13 | MISS=5 | VOID=7 | hit_rate=52.0 | hit_or_void=80.0 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=25 | HIT=20 | MISS=5 | VOID=0 | hit_rate=80.0 | hit_or_void=80.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=25 | HIT=12 | MISS=13 | VOID=0 | hit_rate=48.0 | hit_or_void=48.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=25 | HIT=20 | MISS=5 | VOID=0 | hit_rate=80.0 | hit_or_void=80.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=25 | HIT=12 | MISS=13 | VOID=0 | hit_rate=48.0 | hit_or_void=48.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=25 | HIT=16 | MISS=9 | VOID=0 | hit_rate=64.0 | hit_or_void=64.0 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=39 | HIT=17 | MISS=22 | VOID=0 | hit_rate=43.6 | hit_or_void=43.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=39 | HIT=17 | MISS=15 | VOID=7 | hit_rate=43.6 | hit_or_void=61.5 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=39 | HIT=24 | MISS=15 | VOID=0 | hit_rate=61.5 | hit_or_void=61.5 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=39 | HIT=18 | MISS=21 | VOID=0 | hit_rate=46.2 | hit_or_void=46.2 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=39 | HIT=24 | MISS=15 | VOID=0 | hit_rate=61.5 | hit_or_void=61.5 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=39 | HIT=20 | MISS=19 | VOID=0 | hit_rate=51.3 | hit_or_void=51.3 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=39 | HIT=25 | MISS=14 | VOID=0 | hit_rate=64.1 | hit_or_void=64.1 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
