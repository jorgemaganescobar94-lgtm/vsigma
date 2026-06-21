# vSIGMA API Signal Calibration Summary - 2026-06-21

## Summary
- source_rows: 631
- finished_rows: 250
- pending_rows: 381
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=84.9 | evaluated=73
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=84.9 | evaluated=73
- sample_warning_counts: SAMPLE_OK_100_PLUS=49; MEDIUM_SAMPLE_UNDER_100=21; INSUFFICIENT_SAMPLE_UNDER_20=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=26; CALIBRATION_MEDIUM_OBSERVED_EDGE=19; CALIBRATION_WEAK_OR_NEGATIVE=12; CALIBRATION_STRONG_OBSERVED_EDGE=10; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=5; CALIBRATION_STRONG_PROTECTED_MARKET=5
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=249 | HIT=133 | MISS=116 | VOID=0 | hit_rate=53.4 | hit_or_void=53.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=249 | HIT=133 | MISS=63 | VOID=53 | hit_rate=53.4 | hit_or_void=74.7 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=249 | HIT=186 | MISS=63 | VOID=0 | hit_rate=74.7 | hit_or_void=74.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=250 | HIT=132 | MISS=118 | VOID=0 | hit_rate=52.8 | hit_or_void=52.8 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=250 | HIT=186 | MISS=64 | VOID=0 | hit_rate=74.4 | hit_or_void=74.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=250 | HIT=139 | MISS=111 | VOID=0 | hit_rate=55.6 | hit_or_void=55.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=250 | HIT=161 | MISS=89 | VOID=0 | hit_rate=64.4 | hit_or_void=64.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=105 | HIT=63 | MISS=42 | VOID=0 | hit_rate=60.0 | hit_or_void=60.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=105 | HIT=63 | MISS=22 | VOID=20 | hit_rate=60.0 | hit_or_void=79.0 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=105 | HIT=83 | MISS=22 | VOID=0 | hit_rate=79.0 | hit_or_void=79.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=106 | HIT=50 | MISS=56 | VOID=0 | hit_rate=47.2 | hit_or_void=47.2 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=106 | HIT=77 | MISS=29 | VOID=0 | hit_rate=72.6 | hit_or_void=72.6 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=106 | HIT=54 | MISS=52 | VOID=0 | hit_rate=50.9 | hit_or_void=50.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=106 | HIT=73 | MISS=33 | VOID=0 | hit_rate=68.9 | hit_or_void=68.9 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=144 | HIT=70 | MISS=74 | VOID=0 | hit_rate=48.6 | hit_or_void=48.6 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=144 | HIT=70 | MISS=41 | VOID=33 | hit_rate=48.6 | hit_or_void=71.5 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=144 | HIT=103 | MISS=41 | VOID=0 | hit_rate=71.5 | hit_or_void=71.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=144 | HIT=82 | MISS=62 | VOID=0 | hit_rate=56.9 | hit_or_void=56.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=144 | HIT=109 | MISS=35 | VOID=0 | hit_rate=75.7 | hit_or_void=75.7 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=144 | HIT=85 | MISS=59 | VOID=0 | hit_rate=59.0 | hit_or_void=59.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=144 | HIT=88 | MISS=56 | VOID=0 | hit_rate=61.1 | hit_or_void=61.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
