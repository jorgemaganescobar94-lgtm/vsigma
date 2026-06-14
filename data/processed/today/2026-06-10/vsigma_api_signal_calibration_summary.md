# vSIGMA API Signal Calibration Summary - 2026-06-10

## Summary
- source_rows: 63
- finished_rows: 56
- pending_rows: 7
- summary_rows: 77
- top_market_by_hit_rate: REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | hit_rate_pct=83.3 | evaluated=24
- top_market_by_hit_or_void_rate: REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | hit_or_void_rate_pct=83.3 | evaluated=24
- sample_warning_counts: LOW_SAMPLE_UNDER_50=42; INSUFFICIENT_SAMPLE_UNDER_20=28; MEDIUM_SAMPLE_UNDER_100=7
- calibration_status_counts: CALIBRATION_OBSERVE_ONLY=28; CALIBRATION_WEAK_OR_NEGATIVE=17; CALIBRATION_NEUTRAL=12; CALIBRATION_MEDIUM_OBSERVED_EDGE=11; CALIBRATION_STRONG_OBSERVED_EDGE=4; CALIBRATION_MEDIUM_PROTECTED_MARKET=3; CALIBRATION_STRONG_PROTECTED_MARKET=2
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=56 | HIT=25 | MISS=31 | VOID=0 | hit_rate=44.6 | hit_or_void=44.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=56 | HIT=25 | MISS=18 | VOID=13 | hit_rate=44.6 | hit_or_void=67.9 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=56 | HIT=38 | MISS=18 | VOID=0 | hit_rate=67.9 | hit_or_void=67.9 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=56 | HIT=25 | MISS=31 | VOID=0 | hit_rate=44.6 | hit_or_void=44.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=56 | HIT=37 | MISS=19 | VOID=0 | hit_rate=66.1 | hit_or_void=66.1 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=56 | HIT=26 | MISS=30 | VOID=0 | hit_rate=46.4 | hit_or_void=46.4 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=56 | HIT=37 | MISS=19 | VOID=0 | hit_rate=66.1 | hit_or_void=66.1 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=24 | HIT=13 | MISS=11 | VOID=0 | hit_rate=54.2 | hit_or_void=54.2 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=24 | HIT=13 | MISS=4 | VOID=7 | hit_rate=54.2 | hit_or_void=83.3 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=24 | HIT=20 | MISS=4 | VOID=0 | hit_rate=83.3 | hit_or_void=83.3 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=24 | HIT=12 | MISS=12 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=24 | HIT=19 | MISS=5 | VOID=0 | hit_rate=79.2 | hit_or_void=79.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=24 | HIT=11 | MISS=13 | VOID=0 | hit_rate=45.8 | hit_or_void=45.8 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=24 | HIT=16 | MISS=8 | VOID=0 | hit_rate=66.7 | hit_or_void=66.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=32 | HIT=12 | MISS=20 | VOID=0 | hit_rate=37.5 | hit_or_void=37.5 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=32 | HIT=12 | MISS=14 | VOID=6 | hit_rate=37.5 | hit_or_void=56.2 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=32 | HIT=18 | MISS=14 | VOID=0 | hit_rate=56.2 | hit_or_void=56.2 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=32 | HIT=13 | MISS=19 | VOID=0 | hit_rate=40.6 | hit_or_void=40.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=32 | HIT=18 | MISS=14 | VOID=0 | hit_rate=56.2 | hit_or_void=56.2 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=32 | HIT=15 | MISS=17 | VOID=0 | hit_rate=46.9 | hit_or_void=46.9 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=32 | HIT=21 | MISS=11 | VOID=0 | hit_rate=65.6 | hit_or_void=65.6 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
