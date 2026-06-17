# vSIGMA API Signal Calibration Summary - 2026-06-17

## Summary
- source_rows: 202
- finished_rows: 109
- pending_rows: 93
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=81.2 | evaluated=32
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=81.2 | evaluated=32
- sample_warning_counts: LOW_SAMPLE_UNDER_50=42; MEDIUM_SAMPLE_UNDER_100=21; SAMPLE_OK_100_PLUS=7; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_MEDIUM_OBSERVED_EDGE=20; CALIBRATION_WEAK_OR_NEGATIVE=18; CALIBRATION_NEUTRAL=18; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=5; CALIBRATION_STRONG_OBSERVED_EDGE=5; CALIBRATION_STRONG_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=109 | HIT=51 | MISS=58 | VOID=0 | hit_rate=46.8 | hit_or_void=46.8 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=109 | HIT=51 | MISS=31 | VOID=27 | hit_rate=46.8 | hit_or_void=71.6 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=109 | HIT=78 | MISS=31 | VOID=0 | hit_rate=71.6 | hit_or_void=71.6 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=109 | HIT=52 | MISS=57 | VOID=0 | hit_rate=47.7 | hit_or_void=47.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=109 | HIT=76 | MISS=33 | VOID=0 | hit_rate=69.7 | hit_or_void=69.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=109 | HIT=55 | MISS=54 | VOID=0 | hit_rate=50.5 | hit_or_void=50.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=109 | HIT=73 | MISS=36 | VOID=0 | hit_rate=67.0 | hit_or_void=67.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=45 | HIT=25 | MISS=20 | VOID=0 | hit_rate=55.6 | hit_or_void=55.6 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=45 | HIT=25 | MISS=9 | VOID=11 | hit_rate=55.6 | hit_or_void=80.0 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=45 | HIT=36 | MISS=9 | VOID=0 | hit_rate=80.0 | hit_or_void=80.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=45 | HIT=19 | MISS=26 | VOID=0 | hit_rate=42.2 | hit_or_void=42.2 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=45 | HIT=32 | MISS=13 | VOID=0 | hit_rate=71.1 | hit_or_void=71.1 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=45 | HIT=20 | MISS=25 | VOID=0 | hit_rate=44.4 | hit_or_void=44.4 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=45 | HIT=33 | MISS=12 | VOID=0 | hit_rate=73.3 | hit_or_void=73.3 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=64 | HIT=26 | MISS=38 | VOID=0 | hit_rate=40.6 | hit_or_void=40.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=64 | HIT=26 | MISS=22 | VOID=16 | hit_rate=40.6 | hit_or_void=65.6 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=64 | HIT=42 | MISS=22 | VOID=0 | hit_rate=65.6 | hit_or_void=65.6 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=64 | HIT=33 | MISS=31 | VOID=0 | hit_rate=51.6 | hit_or_void=51.6 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=64 | HIT=44 | MISS=20 | VOID=0 | hit_rate=68.8 | hit_or_void=68.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=64 | HIT=35 | MISS=29 | VOID=0 | hit_rate=54.7 | hit_or_void=54.7 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=64 | HIT=40 | MISS=24 | VOID=0 | hit_rate=62.5 | hit_or_void=62.5 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
