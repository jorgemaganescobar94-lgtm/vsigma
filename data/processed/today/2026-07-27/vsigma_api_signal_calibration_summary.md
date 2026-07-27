# vSIGMA API Signal Calibration Summary - 2026-07-27

## Summary
- source_rows: 668
- finished_rows: 314
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=85.0 | evaluated=107
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=85.0 | evaluated=107
- sample_warning_counts: SAMPLE_OK_100_PLUS=63; INSUFFICIENT_SAMPLE_UNDER_20=7; MEDIUM_SAMPLE_UNDER_100=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=32; CALIBRATION_MEDIUM_OBSERVED_EDGE=16; CALIBRATION_STRONG_OBSERVED_EDGE=12; CALIBRATION_STRONG_PROTECTED_MARKET=7; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_WEAK_OR_NEGATIVE=6; CALIBRATION_MEDIUM_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=313 | HIT=174 | MISS=139 | VOID=0 | hit_rate=55.6 | hit_or_void=55.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=313 | HIT=174 | MISS=76 | VOID=63 | hit_rate=55.6 | hit_or_void=75.7 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=313 | HIT=237 | MISS=76 | VOID=0 | hit_rate=75.7 | hit_or_void=75.7 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=314 | HIT=168 | MISS=146 | VOID=0 | hit_rate=53.5 | hit_or_void=53.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=314 | HIT=235 | MISS=79 | VOID=0 | hit_rate=74.8 | hit_or_void=74.8 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=314 | HIT=178 | MISS=136 | VOID=0 | hit_rate=56.7 | hit_or_void=56.7 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=314 | HIT=202 | MISS=112 | VOID=0 | hit_rate=64.3 | hit_or_void=64.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=149 | HIT=91 | MISS=58 | VOID=0 | hit_rate=61.1 | hit_or_void=61.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=149 | HIT=91 | MISS=31 | VOID=27 | hit_rate=61.1 | hit_or_void=79.2 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=149 | HIT=118 | MISS=31 | VOID=0 | hit_rate=79.2 | hit_or_void=79.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=150 | HIT=74 | MISS=76 | VOID=0 | hit_rate=49.3 | hit_or_void=49.3 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=150 | HIT=110 | MISS=40 | VOID=0 | hit_rate=73.3 | hit_or_void=73.3 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=150 | HIT=81 | MISS=69 | VOID=0 | hit_rate=54.0 | hit_or_void=54.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=150 | HIT=101 | MISS=49 | VOID=0 | hit_rate=67.3 | hit_or_void=67.3 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=164 | HIT=83 | MISS=81 | VOID=0 | hit_rate=50.6 | hit_or_void=50.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=164 | HIT=83 | MISS=45 | VOID=36 | hit_rate=50.6 | hit_or_void=72.6 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=164 | HIT=119 | MISS=45 | VOID=0 | hit_rate=72.6 | hit_or_void=72.6 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=164 | HIT=94 | MISS=70 | VOID=0 | hit_rate=57.3 | hit_or_void=57.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=164 | HIT=125 | MISS=39 | VOID=0 | hit_rate=76.2 | hit_or_void=76.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=164 | HIT=97 | MISS=67 | VOID=0 | hit_rate=59.1 | hit_or_void=59.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=164 | HIT=101 | MISS=63 | VOID=0 | hit_rate=61.6 | hit_or_void=61.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
