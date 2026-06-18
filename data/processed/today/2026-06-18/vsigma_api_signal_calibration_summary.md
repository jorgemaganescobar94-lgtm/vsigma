# vSIGMA API Signal Calibration Summary - 2026-06-18

## Summary
- source_rows: 271
- finished_rows: 127
- pending_rows: 144
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=82.9 | evaluated=35
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=82.9 | evaluated=35
- sample_warning_counts: MEDIUM_SAMPLE_UNDER_100=35; LOW_SAMPLE_UNDER_50=28; SAMPLE_OK_100_PLUS=7; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_NEUTRAL=22; CALIBRATION_WEAK_OR_NEGATIVE=16; CALIBRATION_MEDIUM_OBSERVED_EDGE=15; CALIBRATION_STRONG_OBSERVED_EDGE=8; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_STRONG_PROTECTED_MARKET=5; CALIBRATION_MEDIUM_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=127 | HIT=64 | MISS=63 | VOID=0 | hit_rate=50.4 | hit_or_void=50.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=127 | HIT=64 | MISS=34 | VOID=29 | hit_rate=50.4 | hit_or_void=73.2 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=127 | HIT=93 | MISS=34 | VOID=0 | hit_rate=73.2 | hit_or_void=73.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=127 | HIT=60 | MISS=67 | VOID=0 | hit_rate=47.2 | hit_or_void=47.2 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=127 | HIT=92 | MISS=35 | VOID=0 | hit_rate=72.4 | hit_or_void=72.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=127 | HIT=68 | MISS=59 | VOID=0 | hit_rate=53.5 | hit_or_void=53.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=127 | HIT=82 | MISS=45 | VOID=0 | hit_rate=64.6 | hit_or_void=64.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=48 | HIT=28 | MISS=20 | VOID=0 | hit_rate=58.3 | hit_or_void=58.3 | status=CALIBRATION_NEUTRAL | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=48 | HIT=28 | MISS=9 | VOID=11 | hit_rate=58.3 | hit_or_void=81.2 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=48 | HIT=39 | MISS=9 | VOID=0 | hit_rate=81.2 | hit_or_void=81.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=48 | HIT=20 | MISS=28 | VOID=0 | hit_rate=41.7 | hit_or_void=41.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=48 | HIT=35 | MISS=13 | VOID=0 | hit_rate=72.9 | hit_or_void=72.9 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=48 | HIT=22 | MISS=26 | VOID=0 | hit_rate=45.8 | hit_or_void=45.8 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=LOW_SAMPLE_UNDER_50
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=48 | HIT=36 | MISS=12 | VOID=0 | hit_rate=75.0 | hit_or_void=75.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=LOW_SAMPLE_UNDER_50
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=79 | HIT=36 | MISS=43 | VOID=0 | hit_rate=45.6 | hit_or_void=45.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=79 | HIT=36 | MISS=25 | VOID=18 | hit_rate=45.6 | hit_or_void=68.4 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=79 | HIT=54 | MISS=25 | VOID=0 | hit_rate=68.4 | hit_or_void=68.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=79 | HIT=40 | MISS=39 | VOID=0 | hit_rate=50.6 | hit_or_void=50.6 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=79 | HIT=57 | MISS=22 | VOID=0 | hit_rate=72.2 | hit_or_void=72.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=79 | HIT=46 | MISS=33 | VOID=0 | hit_rate=58.2 | hit_or_void=58.2 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=79 | HIT=46 | MISS=33 | VOID=0 | hit_rate=58.2 | hit_or_void=58.2 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
