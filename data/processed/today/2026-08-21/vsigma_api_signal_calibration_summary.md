# vSIGMA API Signal Calibration Summary - 2026-08-21

## Summary
- source_rows: 703
- finished_rows: 349
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=86.8 | evaluated=129
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=86.8 | evaluated=129
- sample_warning_counts: SAMPLE_OK_100_PLUS=63; INSUFFICIENT_SAMPLE_UNDER_20=7; MEDIUM_SAMPLE_UNDER_100=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=30; CALIBRATION_STRONG_OBSERVED_EDGE=16; CALIBRATION_WEAK_OR_NEGATIVE=11; CALIBRATION_MEDIUM_OBSERVED_EDGE=10; CALIBRATION_STRONG_PROTECTED_MARKET=7; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=3
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=348 | HIT=183 | MISS=165 | VOID=0 | hit_rate=52.6 | hit_or_void=52.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=348 | HIT=183 | MISS=78 | VOID=87 | hit_rate=52.6 | hit_or_void=77.6 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=348 | HIT=270 | MISS=78 | VOID=0 | hit_rate=77.6 | hit_or_void=77.6 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=349 | HIT=196 | MISS=153 | VOID=0 | hit_rate=56.2 | hit_or_void=56.2 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=349 | HIT=267 | MISS=82 | VOID=0 | hit_rate=76.5 | hit_or_void=76.5 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=349 | HIT=182 | MISS=167 | VOID=0 | hit_rate=52.1 | hit_or_void=52.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=349 | HIT=233 | MISS=116 | VOID=0 | hit_rate=66.8 | hit_or_void=66.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=172 | HIT=91 | MISS=81 | VOID=0 | hit_rate=52.9 | hit_or_void=52.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=172 | HIT=91 | MISS=33 | VOID=48 | hit_rate=52.9 | hit_or_void=80.8 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=172 | HIT=139 | MISS=33 | VOID=0 | hit_rate=80.8 | hit_or_void=80.8 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=173 | HIT=95 | MISS=78 | VOID=0 | hit_rate=54.9 | hit_or_void=54.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=173 | HIT=131 | MISS=42 | VOID=0 | hit_rate=75.7 | hit_or_void=75.7 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=173 | HIT=81 | MISS=92 | VOID=0 | hit_rate=46.8 | hit_or_void=46.8 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=173 | HIT=124 | MISS=49 | VOID=0 | hit_rate=71.7 | hit_or_void=71.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=176 | HIT=92 | MISS=84 | VOID=0 | hit_rate=52.3 | hit_or_void=52.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=176 | HIT=92 | MISS=45 | VOID=39 | hit_rate=52.3 | hit_or_void=74.4 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=176 | HIT=131 | MISS=45 | VOID=0 | hit_rate=74.4 | hit_or_void=74.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=176 | HIT=101 | MISS=75 | VOID=0 | hit_rate=57.4 | hit_or_void=57.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=176 | HIT=136 | MISS=40 | VOID=0 | hit_rate=77.3 | hit_or_void=77.3 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=176 | HIT=101 | MISS=75 | VOID=0 | hit_rate=57.4 | hit_or_void=57.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=176 | HIT=109 | MISS=67 | VOID=0 | hit_rate=61.9 | hit_or_void=61.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
