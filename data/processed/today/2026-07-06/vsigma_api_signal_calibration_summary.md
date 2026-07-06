# vSIGMA API Signal Calibration Summary - 2026-07-06

## Summary
- source_rows: 643
- finished_rows: 289
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=86.0 | evaluated=86
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=86.0 | evaluated=86
- sample_warning_counts: SAMPLE_OK_100_PLUS=56; MEDIUM_SAMPLE_UNDER_100=14; INSUFFICIENT_SAMPLE_UNDER_20=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=30; CALIBRATION_MEDIUM_OBSERVED_EDGE=18; CALIBRATION_STRONG_OBSERVED_EDGE=11; CALIBRATION_WEAK_OR_NEGATIVE=8; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_STRONG_PROTECTED_MARKET=6; CALIBRATION_MEDIUM_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=288 | HIT=156 | MISS=132 | VOID=0 | hit_rate=54.2 | hit_or_void=54.2 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=288 | HIT=156 | MISS=72 | VOID=60 | hit_rate=54.2 | hit_or_void=75.0 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=288 | HIT=216 | MISS=72 | VOID=0 | hit_rate=75.0 | hit_or_void=75.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=289 | HIT=156 | MISS=133 | VOID=0 | hit_rate=54.0 | hit_or_void=54.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=289 | HIT=214 | MISS=75 | VOID=0 | hit_rate=74.0 | hit_or_void=74.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=289 | HIT=162 | MISS=127 | VOID=0 | hit_rate=56.1 | hit_or_void=56.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=289 | HIT=186 | MISS=103 | VOID=0 | hit_rate=64.4 | hit_or_void=64.4 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=127 | HIT=76 | MISS=51 | VOID=0 | hit_rate=59.8 | hit_or_void=59.8 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=127 | HIT=76 | MISS=27 | VOID=24 | hit_rate=59.8 | hit_or_void=78.7 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=127 | HIT=100 | MISS=27 | VOID=0 | hit_rate=78.7 | hit_or_void=78.7 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=128 | HIT=64 | MISS=64 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=128 | HIT=92 | MISS=36 | VOID=0 | hit_rate=71.9 | hit_or_void=71.9 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=128 | HIT=67 | MISS=61 | VOID=0 | hit_rate=52.3 | hit_or_void=52.3 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=128 | HIT=87 | MISS=41 | VOID=0 | hit_rate=68.0 | hit_or_void=68.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_1X2 | evaluated=161 | HIT=80 | MISS=81 | VOID=0 | hit_rate=49.7 | hit_or_void=49.7 | status=CALIBRATION_WEAK_OR_NEGATIVE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DNB | evaluated=161 | HIT=80 | MISS=45 | VOID=36 | hit_rate=49.7 | hit_or_void=72.0 | status=CALIBRATION_MEDIUM_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=161 | HIT=116 | MISS=45 | VOID=0 | hit_rate=72.0 | hit_or_void=72.0 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | BTTS_YES | evaluated=161 | HIT=92 | MISS=69 | VOID=0 | hit_rate=57.1 | hit_or_void=57.1 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_1_5 | evaluated=161 | HIT=122 | MISS=39 | VOID=0 | hit_rate=75.8 | hit_or_void=75.8 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | OVER_2_5 | evaluated=161 | HIT=95 | MISS=66 | VOID=0 | hit_rate=59.0 | hit_or_void=59.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- MEDIUM_SIGNAL_REVIEW | UNDER_3_5 | evaluated=161 | HIT=99 | MISS=62 | VOID=0 | hit_rate=61.5 | hit_or_void=61.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS

## Guardrails
- This summary is calibration-only.
- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
