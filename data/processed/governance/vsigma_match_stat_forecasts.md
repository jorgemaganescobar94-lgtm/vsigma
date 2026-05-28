# vSIGMA Match Statistical Forecasts - 2026-05-28

## Summary
- rows_forecasted: 3
- source_file: matches_vsigma_scored_v3.csv
- source_guard: DATED_INPUT_ONLY
- confidence_counts: MEDIUM=2; LOW=1
- tempo_counts: MEDIUM_TEMPO=1; HIGH_TEMPO=1; LOW_TEMPO=1
- calibration_note: v44.1 tightened range width and confidence penalties; no auto-execution.
- auto_apply: NO
- production_change: NO

## Forecast Rows
- #1 | Cerro Porteno vs Sporting Cristal | score=1-1 / 0-1 / 1-2 | goals=1.66-2.84 | shots=21-32 | SoT=5-10 | corners=8-13 | cards=2-6 | tempo=MEDIUM_TEMPO | conf=MEDIUM(71.6) | warning=LINEUPS_INACTIVE
- #2 | Palmeiras vs Junior | score=1-1 / 0-1 / 1-2 | goals=1.49-2.76 | shots=22-35 | SoT=5-10 | corners=10-18 | cards=2-6 | tempo=HIGH_TEMPO | conf=MEDIUM(62.6) | warning=LINEUPS_INACTIVE; PARTIAL_RECENT_STATS
- #3 | Casa Pia vs Torreense | score=1-2 / 0-2 / 1-3 | goals=1.49-2.76 | shots=13-22 | SoT=4-9 | corners=7-13 | cards=4-9 | tempo=LOW_TEMPO | conf=LOW(59.6) | warning=PARTIAL_RECENT_STATS; SHOT_SAMPLE_WEAK; CORNER_SAMPLE_WEAK; CARD_SAMPLE_WEAK

## Guardrails
- Forecasts are ranges, not exact-stat promises.
- This report refuses root-level or governance fallback sources.
- Use these forecasts as an input to market selection, not as automatic execution permission.
