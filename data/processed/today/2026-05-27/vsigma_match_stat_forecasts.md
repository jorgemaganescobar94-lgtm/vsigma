# vSIGMA Match Statistical Forecasts - 2026-05-27

## Summary
- rows_forecasted: 10
- source_file: matches_vsigma_scored_v3.csv
- source_guard: DATED_INPUT_ONLY
- confidence_counts: MEDIUM=9; LOW=1
- tempo_counts: MEDIUM_TEMPO=7; HIGH_TEMPO=3
- calibration_note: v44.1 tightened range width and confidence penalties; no auto-execution.
- auto_apply: NO
- production_change: NO

## Forecast Rows
- #1 | Racing Club vs Independiente Petrolero | score=2-1 / 1-1 / 2-2 | goals=2.20-3.67 | shots=24-37 | SoT=7-14 | corners=8-14 | cards=2-6 | tempo=HIGH_TEMPO | conf=MEDIUM(71.6) | warning=LINEUPS_INACTIVE
- #2 | Crystal Palace vs Rayo Vallecano | score=1-1 / 0-1 / 1-2 | goals=2.05-3.45 | shots=22-33 | SoT=7-12 | corners=7-13 | cards=4-9 | tempo=MEDIUM_TEMPO | conf=MEDIUM(71.6) | warning=LINEUPS_INACTIVE
- #3 | Independiente del Valle vs Rosario Central | score=1-1 / 0-1 / 1-2 | goals=2.05-3.45 | shots=22-33 | SoT=6-11 | corners=8-14 | cards=3-7 | tempo=MEDIUM_TEMPO | conf=MEDIUM(71.6) | warning=LINEUPS_INACTIVE
- #4 | Vasco DA Gama vs Barracas Central | score=1-1 / 0-1 / 1-2 | goals=1.56-2.69 | shots=22-33 | SoT=7-13 | corners=8-14 | cards=3-7 | tempo=MEDIUM_TEMPO | conf=MEDIUM(71.6) | warning=LINEUPS_INACTIVE
- #5 | Libertad Asuncion vs UCV | score=2-2 / 1-2 / 2-3 | goals=2.35-4.15 | shots=22-35 | SoT=7-13 | corners=8-14 | cards=3-9 | tempo=HIGH_TEMPO | conf=MEDIUM(62.6) | warning=LINEUPS_INACTIVE; PARTIAL_RECENT_STATS
- #6 | Olimpia vs A. Italiano | score=2-1 / 1-1 / 2-2 | goals=2.16-3.84 | shots=20-33 | SoT=6-12 | corners=6-12 | cards=3-9 | tempo=MEDIUM_TEMPO | conf=MEDIUM(62.6) | warning=LINEUPS_INACTIVE; PARTIAL_RECENT_STATS
- #7 | Caracas FC vs Botafogo | score=1-2 / 0-2 / 1-3 | goals=2.16-3.84 | shots=24-38 | SoT=7-13 | corners=8-14 | cards=3-8 | tempo=HIGH_TEMPO | conf=MEDIUM(62.6) | warning=LINEUPS_INACTIVE; PARTIAL_RECENT_STATS
- #8 | Atletico-MG vs Puerto Cabello | score=1-1 / 0-1 / 1-2 | goals=2.02-3.61 | shots=21-33 | SoT=5-11 | corners=6-12 | cards=3-8 | tempo=MEDIUM_TEMPO | conf=MEDIUM(62.6) | warning=LINEUPS_INACTIVE; PARTIAL_RECENT_STATS
- #9 | Cienciano vs Juventud | score=1-1 / 0-1 / 1-2 | goals=1.78-3.22 | shots=20-32 | SoT=6-12 | corners=7-14 | cards=1-4 | tempo=MEDIUM_TEMPO | conf=MEDIUM(62.6) | warning=LINEUPS_INACTIVE; PARTIAL_RECENT_STATS
- #10 | Cuniburo vs Orense SC | score=1-1 / 0-1 / 1-2 | goals=1.58-3.12 | shots=17-29 | SoT=5-11 | corners=6-13 | cards=2-6 | tempo=MEDIUM_TEMPO | conf=LOW(51.1) | warning=PARTIAL_RECENT_STATS; SHOT_SAMPLE_WEAK; CORNER_SAMPLE_WEAK; CARD_SAMPLE_WEAK

## Guardrails
- Forecasts are ranges, not exact-stat promises.
- This report refuses root-level or governance fallback sources.
- Use these forecasts as an input to market selection, not as automatic execution permission.
