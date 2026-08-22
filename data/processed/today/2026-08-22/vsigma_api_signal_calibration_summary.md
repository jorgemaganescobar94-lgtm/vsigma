# vSIGMA API Signal Calibration Summary - 2026-08-22

## Summary
- source_rows: 705
- finished_rows: 351
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=87.0 | evaluated=131
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=87.0 | evaluated=131
- sample_warning_counts: SAMPLE_OK_100_PLUS=63; INSUFFICIENT_SAMPLE_UNDER_20=7; MEDIUM_SAMPLE_UNDER_100=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=30; CALIBRATION_STRONG_OBSERVED_EDGE=16; CALIBRATION_WEAK_OR_NEGATIVE=11; CALIBRATION_MEDIUM_OBSERVED_EDGE=10; CALIBRATION_STRONG_PROTECTED_MARKET=7; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=3
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=350 | HIT=183 | MISS=167 | VOID=0 | hit_rate=52.3 | hit_or_void=52.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=350 | HIT=183 | MISS=78 | VOID=89 | hit_rate=52.3 | hit_or_void=77.7 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=350 | HIT=272 | MISS=78 | VOID=0 | hit_rate=77.7 | hit_or_void=77.7 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=351 | HIT=198 | MISS=153 | VOID=0 | hit_rate=56.4 | hit_or_void=56.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=351 | HIT=269 | MISS=82 | VOID=0 | hit_rate=76.6 | hit_or_void=76.6 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=351 | HIT=182 | MISS=169 | VOID=0 | hit_rate=51.9 | hit_or_void=51.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=351 | HIT=235 | MISS=116 | VOID=0 | hit_rate=67.0 | hit_or_void=67.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=174 | HIT=91 | MISS=83 | VOID=0 | hit_rate=52.3 | hit_or_void=52.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=174 | HIT=91 | MISS=33 | VOID=50 | hit_rate=52.3 | hit_or_void=81.0 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=174 | HIT=141 | MISS=33 | VOID=0 | hit_rate=81.0 | hit_or_void=81.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=175 | HIT=97 | MISS=78 | VOID=0 | hit_rate=55.4 | hit_or_void=55.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=175 | HIT=133 | MISS=42 | VOID=0 | hit_rate=76.0 | hit_or_void=76.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=175 | HIT=81 | MISS=94 | VOID=0 | hit_rate=46.3 | hit_or_void=46.3 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=175 | HIT=126 | MISS=49 | VOID=0 | hit_rate=72.0 | hit_or_void=72.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
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
