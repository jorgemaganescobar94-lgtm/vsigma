# vSIGMA API Signal Calibration Summary - 2026-06-20

## Summary
- source_rows: 468
- finished_rows: 200
- pending_rows: 268
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=83.3 | evaluated=60
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=83.3 | evaluated=60
- sample_warning_counts: MEDIUM_SAMPLE_UNDER_100=42; SAMPLE_OK_100_PLUS=28; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_NEUTRAL=25; CALIBRATION_MEDIUM_OBSERVED_EDGE=17; CALIBRATION_WEAK_OR_NEGATIVE=10; CALIBRATION_STRONG_OBSERVED_EDGE=9; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_STRONG_PROTECTED_MARKET=5; CALIBRATION_MEDIUM_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=200 | HIT=104 | MISS=96 | VOID=0 | hit_rate=52.0 | hit_or_void=52.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=200 | HIT=104 | MISS=51 | VOID=45 | hit_rate=52.0 | hit_or_void=74.5 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=200 | HIT=149 | MISS=51 | VOID=0 | hit_rate=74.5 | hit_or_void=74.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=200 | HIT=105 | MISS=95 | VOID=0 | hit_rate=52.5 | hit_or_void=52.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=200 | HIT=149 | MISS=51 | VOID=0 | hit_rate=74.5 | hit_or_void=74.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=200 | HIT=109 | MISS=91 | VOID=0 | hit_rate=54.5 | hit_or_void=54.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=200 | HIT=133 | MISS=67 | VOID=0 | hit_rate=66.5 | hit_or_void=66.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=82 | HIT=48 | MISS=34 | VOID=0 | hit_rate=58.5 | hit_or_void=58.5 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=82 | HIT=48 | MISS=17 | VOID=17 | hit_rate=58.5 | hit_or_void=79.3 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=82 | HIT=65 | MISS=17 | VOID=0 | hit_rate=79.3 | hit_or_void=79.3 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=82 | HIT=39 | MISS=43 | VOID=0 | hit_rate=47.6 | hit_or_void=47.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=82 | HIT=61 | MISS=21 | VOID=0 | hit_rate=74.4 | hit_or_void=74.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=82 | HIT=41 | MISS=41 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=MEDIUM_SAMPLE_UNDER_100
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=82 | HIT=60 | MISS=22 | VOID=0 | hit_rate=73.2 | hit_or_void=73.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=MEDIUM_SAMPLE_UNDER_100
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=118 | HIT=56 | MISS=62 | VOID=0 | hit_rate=47.5 | hit_or_void=47.5 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=118 | HIT=56 | MISS=34 | VOID=28 | hit_rate=47.5 | hit_or_void=71.2 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=118 | HIT=84 | MISS=34 | VOID=0 | hit_rate=71.2 | hit_or_void=71.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=118 | HIT=66 | MISS=52 | VOID=0 | hit_rate=55.9 | hit_or_void=55.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=118 | HIT=88 | MISS=30 | VOID=0 | hit_rate=74.6 | hit_or_void=74.6 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=118 | HIT=68 | MISS=50 | VOID=0 | hit_rate=57.6 | hit_or_void=57.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=118 | HIT=73 | MISS=45 | VOID=0 | hit_rate=61.9 | hit_or_void=61.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
