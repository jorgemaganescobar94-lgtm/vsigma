# vSIGMA API Signal Calibration Summary - 2026-07-18

## Summary
- source_rows: 658
- finished_rows: 304
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=84.8 | evaluated=99
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=84.8 | evaluated=99
- sample_warning_counts: SAMPLE_OK_100_PLUS=56; MEDIUM_SAMPLE_UNDER_100=14; INSUFFICIENT_SAMPLE_UNDER_20=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=31; CALIBRATION_MEDIUM_OBSERVED_EDGE=18; CALIBRATION_STRONG_OBSERVED_EDGE=11; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_STRONG_PROTECTED_MARKET=6; CALIBRATION_WEAK_OR_NEGATIVE=6; CALIBRATION_MEDIUM_PROTECTED_MARKET=5
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=303 | HIT=168 | MISS=135 | VOID=0 | hit_rate=55.4 | hit_or_void=55.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=303 | HIT=168 | MISS=75 | VOID=60 | hit_rate=55.4 | hit_or_void=75.2 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=303 | HIT=228 | MISS=75 | VOID=0 | hit_rate=75.2 | hit_or_void=75.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=304 | HIT=163 | MISS=141 | VOID=0 | hit_rate=53.6 | hit_or_void=53.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=304 | HIT=226 | MISS=78 | VOID=0 | hit_rate=74.3 | hit_or_void=74.3 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=304 | HIT=174 | MISS=130 | VOID=0 | hit_rate=57.2 | hit_or_void=57.2 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=304 | HIT=195 | MISS=109 | VOID=0 | hit_rate=64.1 | hit_or_void=64.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=141 | HIT=87 | MISS=54 | VOID=0 | hit_rate=61.7 | hit_or_void=61.7 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=141 | HIT=87 | MISS=30 | VOID=24 | hit_rate=61.7 | hit_or_void=78.7 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=141 | HIT=111 | MISS=30 | VOID=0 | hit_rate=78.7 | hit_or_void=78.7 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=142 | HIT=70 | MISS=72 | VOID=0 | hit_rate=49.3 | hit_or_void=49.3 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=142 | HIT=103 | MISS=39 | VOID=0 | hit_rate=72.5 | hit_or_void=72.5 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=142 | HIT=78 | MISS=64 | VOID=0 | hit_rate=54.9 | hit_or_void=54.9 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=142 | HIT=95 | MISS=47 | VOID=0 | hit_rate=66.9 | hit_or_void=66.9 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=162 | HIT=81 | MISS=81 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=162 | HIT=81 | MISS=45 | VOID=36 | hit_rate=50.0 | hit_or_void=72.2 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=162 | HIT=117 | MISS=45 | VOID=0 | hit_rate=72.2 | hit_or_void=72.2 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=162 | HIT=93 | MISS=69 | VOID=0 | hit_rate=57.4 | hit_or_void=57.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=162 | HIT=123 | MISS=39 | VOID=0 | hit_rate=75.9 | hit_or_void=75.9 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=162 | HIT=96 | MISS=66 | VOID=0 | hit_rate=59.3 | hit_or_void=59.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=162 | HIT=100 | MISS=62 | VOID=0 | hit_rate=61.7 | hit_or_void=61.7 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
