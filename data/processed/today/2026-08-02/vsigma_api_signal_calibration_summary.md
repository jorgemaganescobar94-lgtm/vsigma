# vSIGMA API Signal Calibration Summary - 2026-08-02

## Summary
- source_rows: 686
- finished_rows: 332
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=86.3 | evaluated=117
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=86.3 | evaluated=117
- sample_warning_counts: SAMPLE_OK_100_PLUS=63; INSUFFICIENT_SAMPLE_UNDER_20=7; MEDIUM_SAMPLE_UNDER_100=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=34; CALIBRATION_STRONG_OBSERVED_EDGE=15; CALIBRATION_MEDIUM_OBSERVED_EDGE=13; CALIBRATION_STRONG_PROTECTED_MARKET=7; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_WEAK_OR_NEGATIVE=4; CALIBRATION_MEDIUM_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
- auto_apply: NO
- production_change: NO

## Global Market Calibration
- API_1X2 | evaluated=331 | HIT=182 | MISS=149 | VOID=0 | hit_rate=55.0 | hit_or_void=55.0 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DNB | evaluated=331 | HIT=182 | MISS=76 | VOID=73 | hit_rate=55.0 | hit_or_void=77.0 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_DOUBLE_CHANCE | evaluated=331 | HIT=255 | MISS=76 | VOID=0 | hit_rate=77.0 | hit_or_void=77.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- BTTS_YES | evaluated=332 | HIT=182 | MISS=150 | VOID=0 | hit_rate=54.8 | hit_or_void=54.8 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_1_5 | evaluated=332 | HIT=253 | MISS=79 | VOID=0 | hit_rate=76.2 | hit_or_void=76.2 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- OVER_2_5 | evaluated=332 | HIT=182 | MISS=150 | VOID=0 | hit_rate=54.8 | hit_or_void=54.8 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- UNDER_3_5 | evaluated=332 | HIT=216 | MISS=116 | VOID=0 | hit_rate=65.1 | hit_or_void=65.1 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Signal Band Calibration
- HIGH_SIGNAL_REVIEW | API_1X2 | evaluated=159 | HIT=91 | MISS=68 | VOID=0 | hit_rate=57.2 | hit_or_void=57.2 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DNB | evaluated=159 | HIT=91 | MISS=31 | VOID=37 | hit_rate=57.2 | hit_or_void=80.5 | status=CALIBRATION_STRONG_PROTECTED_MARKET | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | API_DOUBLE_CHANCE | evaluated=159 | HIT=128 | MISS=31 | VOID=0 | hit_rate=80.5 | hit_or_void=80.5 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | BTTS_YES | evaluated=160 | HIT=84 | MISS=76 | VOID=0 | hit_rate=52.5 | hit_or_void=52.5 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_1_5 | evaluated=160 | HIT=120 | MISS=40 | VOID=0 | hit_rate=75.0 | hit_or_void=75.0 | status=CALIBRATION_STRONG_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | OVER_2_5 | evaluated=160 | HIT=81 | MISS=79 | VOID=0 | hit_rate=50.6 | hit_or_void=50.6 | status=CALIBRATION_NEUTRAL | sample=SAMPLE_OK_100_PLUS
- HIGH_SIGNAL_REVIEW | UNDER_3_5 | evaluated=160 | HIT=111 | MISS=49 | VOID=0 | hit_rate=69.4 | hit_or_void=69.4 | status=CALIBRATION_MEDIUM_OBSERVED_EDGE | sample=SAMPLE_OK_100_PLUS
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
