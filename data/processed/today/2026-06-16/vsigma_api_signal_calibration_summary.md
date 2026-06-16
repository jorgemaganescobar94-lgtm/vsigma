# vSIGMA API Signal Calibration Summary - 2026-06-16

## Summary
- source_rows: 129
- finished_rows: 92
- pending_rows: 37
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=85.2 | evaluated=27
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=85.2 | evaluated=27
- sample_warning_counts: LOW_SAMPLE_UNDER_50=42; MEDIUM_SAMPLE_UNDER_100=28; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_WEAK_OR_NEGATIVE=23; CALIBRATION_MEDIUM_OBSERVED_EDGE=20; CALIBRATION_NEUTRAL=17; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=4; CALIBRATION_STRONG_PROTECTED_MARKET=3; CALIBRATION_STRONG_OBSERVED_EDGE=3
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=92 | HIT=43 | MISS=49 | VOID=0 | hit_rate=46.7 | hit_or_void=46.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=92 | HIT=43 | MISS=27 | VOID=22 | hit_rate=46.7 | hit_or_void=70.7 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=92 | HIT=65 | MISS=27 | VOID=0 | hit_rate=70.7 | hit_or_void=70.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=92 | HIT=43 | MISS=49 | VOID=0 | hit_rate=46.7 | hit_or_void=46.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=92 | HIT=63 | MISS=29 | VOID=0 | hit_rate=68.5 | hit_or_void=68.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=92 | HIT=44 | MISS=48 | VOID=0 | hit_rate=47.8 | hit_or_void=47.8 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=92 | HIT=63 | MISS=29 | VOID=0 | hit_rate=68.5 | hit_or_void=68.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=38 | HIT=21 | MISS=17 | VOID=0 | hit_rate=55.3 | hit_or_void=55.3 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=38 | HIT=21 | MISS=7 | VOID=10 | hit_rate=55.3 | hit_or_void=81.6 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=38 | HIT=31 | MISS=7 | VOID=0 | hit_rate=81.6 | hit_or_void=81.6 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=38 | HIT=17 | MISS=21 | VOID=0 | hit_rate=44.7 | hit_or_void=44.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=38 | HIT=28 | MISS=10 | VOID=0 | hit_rate=73.7 | hit_or_void=73.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=38 | HIT=17 | MISS=21 | VOID=0 | hit_rate=44.7 | hit_or_void=44.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=38 | HIT=27 | MISS=11 | VOID=0 | hit_rate=71.1 | hit_or_void=71.1 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=54 | HIT=22 | MISS=32 | VOID=0 | hit_rate=40.7 | hit_or_void=40.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=54 | HIT=22 | MISS=20 | VOID=12 | hit_rate=40.7 | hit_or_void=63.0 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=54 | HIT=34 | MISS=20 | VOID=0 | hit_rate=63.0 | hit_or_void=63.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=54 | HIT=26 | MISS=28 | VOID=0 | hit_rate=48.1 | hit_or_void=48.1 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=54 | HIT=35 | MISS=19 | VOID=0 | hit_rate=64.8 | hit_or_void=64.8 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=54 | HIT=27 | MISS=27 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=54 | HIT=36 | MISS=18 | VOID=0 | hit_rate=66.7 | hit_or_void=66.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
