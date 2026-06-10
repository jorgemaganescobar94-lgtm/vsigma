# vSIGMA API Signal Calibration Summary - 2026-06-10

## Summary
- source_rows: 61
- finished_rows: 40
- pending_rows: 21
- summary_rows: 77
- top_market_by_hit_rate: ALL=ALL | API_DOUBLE_CHANCE | hit_rate_pct=77.5 | evaluated=40
- top_market_by_hit_or_void_rate: ALL=ALL | API_DNB | hit_or_void_rate_pct=77.5 | evaluated=40
- sample_warning_counts: INSUFFICIENT_SAMPLE_UNDER_20=49; LOW_SAMPLE_UNDER_50=28
- calibration_status_counts: CALIBRATION_OBSERVE_ONLY=49; CALIBRATION_WEAK_OR_NEGATIVE=10; CALIBRATION_NEUTRAL=5; CALIBRATION_STRONG_OBSERVED_EDGE=5; CALIBRATION_STRONG_PROTECTED_MARKET=4; CALIBRATION_MEDIUM_OBSERVED_EDGE=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=40 | HIT=21 | MISS=19 | VOID=0 | hit_rate=52.5 | hit_or_void=52.5 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=40 | HIT=21 | MISS=9 | VOID=10 | hit_rate=52.5 | hit_or_void=77.5 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=40 | HIT=31 | MISS=9 | VOID=0 | hit_rate=77.5 | hit_or_void=77.5 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=40 | HIT=18 | MISS=22 | VOID=0 | hit_rate=45.0 | hit_or_void=45.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=40 | HIT=26 | MISS=14 | VOID=0 | hit_rate=65.0 | hit_or_void=65.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=40 | HIT=18 | MISS=22 | VOID=0 | hit_rate=45.0 | hit_or_void=45.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=40 | HIT=27 | MISS=13 | VOID=0 | hit_rate=67.5 | hit_or_void=67.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=19 | HIT=11 | MISS=8 | VOID=0 | hit_rate=57.9 | hit_or_void=57.9 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=19 | HIT=11 | MISS=4 | VOID=4 | hit_rate=57.9 | hit_or_void=78.9 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=19 | HIT=15 | MISS=4 | VOID=0 | hit_rate=78.9 | hit_or_void=78.9 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=19 | HIT=9 | MISS=10 | VOID=0 | hit_rate=47.4 | hit_or_void=47.4 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=19 | HIT=14 | MISS=5 | VOID=0 | hit_rate=73.7 | hit_or_void=73.7 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=19 | HIT=9 | MISS=10 | VOID=0 | hit_rate=47.4 | hit_or_void=47.4 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=19 | HIT=13 | MISS=6 | VOID=0 | hit_rate=68.4 | hit_or_void=68.4 | status=CALIBRATION_OBSERVE_ONLY | sample=INSUFFICIENT_SAMPLE_UNDER_20
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=21 | HIT=10 | MISS=11 | VOID=0 | hit_rate=47.6 | hit_or_void=47.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=21 | HIT=10 | MISS=5 | VOID=6 | hit_rate=47.6 | hit_or_void=76.2 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=21 | HIT=16 | MISS=5 | VOID=0 | hit_rate=76.2 | hit_or_void=76.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=21 | HIT=9 | MISS=12 | VOID=0 | hit_rate=42.9 | hit_or_void=42.9 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=21 | HIT=12 | MISS=9 | VOID=0 | hit_rate=57.1 | hit_or_void=57.1 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=21 | HIT=9 | MISS=12 | VOID=0 | hit_rate=42.9 | hit_or_void=42.9 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=21 | HIT=14 | MISS=7 | VOID=0 | hit_rate=66.7 | hit_or_void=66.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
