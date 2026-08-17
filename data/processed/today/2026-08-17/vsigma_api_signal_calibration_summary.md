# vSIGMA API Signal Calibration Summary - 2026-08-17

## Summary
- source_rows: 697
- finished_rows: 343
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=86.2 | evaluated=123
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=86.2 | evaluated=123
- sample_warning_counts: SAMPLE_OK_100_PLUS=63; INSUFFICIENT_SAMPLE_UNDER_20=7; MEDIUM_SAMPLE_UNDER_100=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=30; CALIBRATION_STRONG_OBSERVED_EDGE=13; CALIBRATION_MEDIUM_OBSERVED_EDGE=13; CALIBRATION_WEAK_OR_NEGATIVE=11; CALIBRATION_STRONG_PROTECTED_MARKET=7; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=3
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=342 | HIT=183 | MISS=159 | VOID=0 | hit_rate=53.5 | hit_or_void=53.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=342 | HIT=183 | MISS=78 | VOID=81 | hit_rate=53.5 | hit_or_void=77.2 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=342 | HIT=264 | MISS=78 | VOID=0 | hit_rate=77.2 | hit_or_void=77.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=343 | HIT=190 | MISS=153 | VOID=0 | hit_rate=55.4 | hit_or_void=55.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=343 | HIT=261 | MISS=82 | VOID=0 | hit_rate=76.1 | hit_or_void=76.1 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=343 | HIT=182 | MISS=161 | VOID=0 | hit_rate=53.1 | hit_or_void=53.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=343 | HIT=227 | MISS=116 | VOID=0 | hit_rate=66.2 | hit_or_void=66.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=166 | HIT=91 | MISS=75 | VOID=0 | hit_rate=54.8 | hit_or_void=54.8 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=166 | HIT=91 | MISS=33 | VOID=42 | hit_rate=54.8 | hit_or_void=80.1 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=166 | HIT=133 | MISS=33 | VOID=0 | hit_rate=80.1 | hit_or_void=80.1 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=167 | HIT=89 | MISS=78 | VOID=0 | hit_rate=53.3 | hit_or_void=53.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=167 | HIT=125 | MISS=42 | VOID=0 | hit_rate=74.9 | hit_or_void=74.9 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=167 | HIT=81 | MISS=86 | VOID=0 | hit_rate=48.5 | hit_or_void=48.5 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=167 | HIT=118 | MISS=49 | VOID=0 | hit_rate=70.7 | hit_or_void=70.7 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
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
