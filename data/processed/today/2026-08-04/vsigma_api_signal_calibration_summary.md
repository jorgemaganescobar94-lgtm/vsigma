# vSIGMA API Signal Calibration Summary - 2026-08-04

## Summary
- source_rows: 688
- finished_rows: 334
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=86.6 | evaluated=119
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=86.6 | evaluated=119
- sample_warning_counts: SAMPLE_OK_100_PLUS=63; INSUFFICIENT_SAMPLE_UNDER_20=7; MEDIUM_SAMPLE_UNDER_100=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=33; CALIBRATION_STRONG_OBSERVED_EDGE=15; CALIBRATION_MEDIUM_OBSERVED_EDGE=13; CALIBRATION_STRONG_PROTECTED_MARKET=7; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_WEAK_OR_NEGATIVE=5; CALIBRATION_MEDIUM_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=333 | HIT=182 | MISS=151 | VOID=0 | hit_rate=54.7 | hit_or_void=54.7 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=333 | HIT=182 | MISS=76 | VOID=75 | hit_rate=54.7 | hit_or_void=77.2 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=333 | HIT=257 | MISS=76 | VOID=0 | hit_rate=77.2 | hit_or_void=77.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=334 | HIT=184 | MISS=150 | VOID=0 | hit_rate=55.1 | hit_or_void=55.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=334 | HIT=255 | MISS=79 | VOID=0 | hit_rate=76.3 | hit_or_void=76.3 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=334 | HIT=182 | MISS=152 | VOID=0 | hit_rate=54.5 | hit_or_void=54.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=334 | HIT=218 | MISS=116 | VOID=0 | hit_rate=65.3 | hit_or_void=65.3 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=161 | HIT=91 | MISS=70 | VOID=0 | hit_rate=56.5 | hit_or_void=56.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=161 | HIT=91 | MISS=31 | VOID=39 | hit_rate=56.5 | hit_or_void=80.7 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=161 | HIT=130 | MISS=31 | VOID=0 | hit_rate=80.7 | hit_or_void=80.7 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=162 | HIT=86 | MISS=76 | VOID=0 | hit_rate=53.1 | hit_or_void=53.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=162 | HIT=122 | MISS=40 | VOID=0 | hit_rate=75.3 | hit_or_void=75.3 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=162 | HIT=81 | MISS=81 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=162 | HIT=113 | MISS=49 | VOID=0 | hit_rate=69.8 | hit_or_void=69.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=172 | HIT=91 | MISS=81 | VOID=0 | hit_rate=52.9 | hit_or_void=52.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=172 | HIT=91 | MISS=45 | VOID=36 | hit_rate=52.9 | hit_or_void=73.8 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=172 | HIT=127 | MISS=45 | VOID=0 | hit_rate=73.8 | hit_or_void=73.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=172 | HIT=98 | MISS=74 | VOID=0 | hit_rate=57.0 | hit_or_void=57.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=172 | HIT=133 | MISS=39 | VOID=0 | hit_rate=77.3 | hit_or_void=77.3 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=172 | HIT=101 | MISS=71 | VOID=0 | hit_rate=58.7 | hit_or_void=58.7 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=172 | HIT=105 | MISS=67 | VOID=0 | hit_rate=61.0 | hit_or_void=61.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
