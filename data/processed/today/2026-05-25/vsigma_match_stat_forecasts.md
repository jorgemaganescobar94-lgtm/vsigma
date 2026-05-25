# vSIGMA Match Statistical Forecasts - 2026-05-25

## Summary
- rows_forecasted: 6
- source_file: matches_vsigma_scored_v3.csv
- source_guard: DATED_INPUT_ONLY
- confidence_counts: MEDIUM=4; LOW=2
- tempo_counts: MEDIUM_TEMPO=3; HIGH_TEMPO=3
- calibration_note: v44.1 tightened range width and confidence penalties; no auto-execution.
- auto_apply: NO
- production_change: NO

## Forecast Rows
- #1 | IF Elfsborg vs BK Hacken | score=2-2 / 1-2 / 2-3 | goals=2.35-3.90 | shots=20-31 | SoT=6-11 | corners=8-13 | cards=3-7 | tempo=MEDIUM_TEMPO | conf=MEDIUM(76.6) | warning=AVAILABILITY_RISK
- #2 | SC Paderborn 07 vs VfL Wolfsburg | score=2-2 / 1-2 / 2-3 | goals=2.65-4.35 | shots=22-34 | SoT=7-14 | corners=9-15 | cards=2-5 | tempo=HIGH_TEMPO | conf=MEDIUM(66.6) | warning=LINEUPS_INACTIVE; AVAILABILITY_RISK
- #3 | IFK Goteborg vs Mjallby AIF | score=1-2 / 0-2 / 1-3 | goals=2.40-3.98 | shots=25-38 | SoT=8-14 | corners=8-15 | cards=2-5 | tempo=HIGH_TEMPO | conf=MEDIUM(66.6) | warning=LINEUPS_INACTIVE; AVAILABILITY_RISK
- #4 | Sandefjord vs Fredrikstad | score=2-1 / 1-1 / 2-2 | goals=2.10-3.52 | shots=25-37 | SoT=6-12 | corners=10-16 | cards=2-5 | tempo=HIGH_TEMPO | conf=MEDIUM(66.6) | warning=LINEUPS_INACTIVE; AVAILABILITY_RISK
- #5 | Botafogo SP vs Athletic Club | score=1-1 / 0-1 / 1-2 | goals=1.58-3.12 | shots=17-29 | SoT=5-11 | corners=6-13 | cards=2-6 | tempo=MEDIUM_TEMPO | conf=LOW(55.6) | warning=PARTIAL_RECENT_STATS; SHOT_SAMPLE_WEAK; CORNER_SAMPLE_WEAK; CARD_SAMPLE_WEAK
- #6 | ST Mirren vs Partick | score=1-2 / 0-2 / 1-3 | goals=1.56-3.07 | shots=13-23 | SoT=4-10 | corners=7-15 | cards=1-5 | tempo=MEDIUM_TEMPO | conf=LOW(49.6) | warning=LINEUPS_INACTIVE; PARTIAL_RECENT_STATS; SHOT_SAMPLE_WEAK; CORNER_SAMPLE_WEAK; CARD_SAMPLE_WEAK

## Guardrails
- Forecasts are ranges, not exact-stat promises.
- This report refuses root-level or governance fallback sources.
- Use these forecasts as an input to market selection, not as automatic execution permission.
