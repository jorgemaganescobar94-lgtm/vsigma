# vSIGMA API Signal Calibration Summary - 2026-06-09

## Summary
- source_rows: 29
- finished_rows: 27
- pending_rows: 2
- summary_rows: 77
- top_market_by_hit_rate: ALL=ALL | API_DOUBLE_CHANCE | hit_rate_pct=77.8 | evaluated=27
- top_market_by_hit_or_void_rate: ALL=ALL | API_DNB | hit_or_void_rate_pct=77.8 | evaluated=27
- sample_warning_counts: INSUFFICIENT_SAMPLE_UNDER_20=70; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_OBSERVE_ONLY=70; CALIBRATION_WEAK_OR_NEGATIVE=2; CALIBRATION_MEDIUM_OBSERVED_EDGE=2; CALIBRATION_NEUTRAL=1; CALIBRATION_STRONG_PROTECTED_MARKET=1; CALIBRATION_STRONG_OBSERVED_EDGE=1
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=27 | HIT=15 | MISS=12 | VOID=0 | hit_rate=55.6 | hit_or_void=55.6 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=27 | HIT=15 | MISS=6 | VOID=6 | hit_rate=55.6 | hit_or_void=77.8 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=27 | HIT=21 | MISS=6 | VOID=0 | hit_rate=77.8 | hit_or_void=77.8 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=27 | HIT=13 | MISS=14 | VOID=0 | hit_rate=48.1 | hit_or_void=48.1 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=27 | HIT=18 | MISS=9 | VOID=0 | hit_rate=66.7 | hit_or_void=66.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=27 | HIT=11 | MISS=16 | VOID=0 | hit_rate=40.7 | hit_or_void=40.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=27 | HIT=20 | MISS=7 | VOID=0 | hit_rate=74.1 | hit_or_void=74.1 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=14 | HIT=9 | MISS=5 | VOID=0 | hit_rate=64.3 | hit_or_void=64.3 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=14 | HIT=9 | MISS=2 | VOID=3 | hit_rate=64.3 | hit_or_void=85.7 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=14 | HIT=12 | MISS=2 | VOID=0 | hit_rate=85.7 | hit_or_void=85.7 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=14 | HIT=8 | MISS=6 | VOID=0 | hit_rate=57.1 | hit_or_void=57.1 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=14 | HIT=10 | MISS=4 | VOID=0 | hit_rate=71.4 | hit_or_void=71.4 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=14 | HIT=6 | MISS=8 | VOID=0 | hit_rate=42.9 | hit_or_void=42.9 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=14 | HIT=10 | MISS=4 | VOID=0 | hit_rate=71.4 | hit_or_void=71.4 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=13 | HIT=6 | MISS=7 | VOID=0 | hit_rate=46.2 | hit_or_void=46.2 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=13 | HIT=6 | MISS=4 | VOID=3 | hit_rate=46.2 | hit_or_void=69.2 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=13 | HIT=9 | MISS=4 | VOID=0 | hit_rate=69.2 | hit_or_void=69.2 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=13 | HIT=5 | MISS=8 | VOID=0 | hit_rate=38.5 | hit_or_void=38.5 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=13 | HIT=8 | MISS=5 | VOID=0 | hit_rate=61.5 | hit_or_void=61.5 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=13 | HIT=5 | MISS=8 | VOID=0 | hit_rate=38.5 | hit_or_void=38.5 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=13 | HIT=10 | MISS=3 | VOID=0 | hit_rate=76.9 | hit_or_void=76.9 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
