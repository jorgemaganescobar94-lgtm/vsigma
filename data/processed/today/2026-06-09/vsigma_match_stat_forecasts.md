# vSIGMA Match Statistical Forecasts - 2026-06-09

## Summary
- rows_forecasted: 3
- source_file: matches_vsigma_scored_v3.csv
- source_guard: DATED_INPUT_ONLY
- confidence_counts: LOW=2; MEDIUM=1
- tempo_counts: MEDIUM_TEMPO=2; HIGH_TEMPO=1
- calibration_note: v44.1 tightened range width and confidence penalties; no auto-execution.
- auto_apply: NO
- production_change: NO

## Forecast Rows
- #1 | Almeria vs Castellón | score=2-2 / 1-2 / 2-3 | goals=3.09-5.04 | shots=24-36 | SoT=9-16 | corners=8-14 | cards=3-7 | tempo=HIGH_TEMPO | conf=MEDIUM(71.6) | warning=LINEUPS_INACTIVE
- #2 | Nautico Recife vs Fortaleza EC | score=1-1 / 0-1 / 1-2 | goals=1.58-3.12 | shots=17-29 | SoT=5-11 | corners=6-13 | cards=2-6 | tempo=MEDIUM_TEMPO | conf=LOW(55.6) | warning=PARTIAL_RECENT_STATS; SHOT_SAMPLE_WEAK; CORNER_SAMPLE_WEAK; CARD_SAMPLE_WEAK
- #3 | Ponte Preta vs Cuiaba | score=1-1 / 0-1 / 1-2 | goals=1.58-3.12 | shots=17-29 | SoT=5-11 | corners=6-13 | cards=2-6 | tempo=MEDIUM_TEMPO | conf=LOW(55.6) | warning=PARTIAL_RECENT_STATS; SHOT_SAMPLE_WEAK; CORNER_SAMPLE_WEAK; CARD_SAMPLE_WEAK

## Guardrails
- Forecasts are ranges, not exact-stat promises.
- This report refuses root-level or governance fallback sources.
- Use these forecasts as an input to market selection, not as automatic execution permission.
