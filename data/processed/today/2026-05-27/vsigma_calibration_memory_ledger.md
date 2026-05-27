# vSIGMA Calibration Memory Ledger - 2026-05-27

## Summary
- ledger_rows_total: 6
- metrics_tracked: 6
- memory_decision_counts: ACCUMULATE_MORE_SAMPLE=6
- auto_apply_allowed: NO
- source_guard: DATED_INPUT_ONLY
- production_change: NO

## Metric Memory
- total_cards | days=1 | rows=4 | hit_rate=0.750 | bias=UNDER_ESTIMATE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.
- total_corners | days=1 | rows=3 | hit_rate=0.333 | bias=OVER_ESTIMATE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.
- total_fouls | days=1 | rows=3 | hit_rate=1.000 | bias=BALANCED_OR_ON_RANGE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.
- total_goals | days=1 | rows=4 | hit_rate=0.000 | bias=OVER_ESTIMATE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.
- total_shots | days=1 | rows=3 | hit_rate=1.000 | bias=BALANCED_OR_ON_RANGE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.
- total_sot | days=1 | rows=3 | hit_rate=1.000 | bias=BALANCED_OR_ON_RANGE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.

## Governance Rules
- Never auto-apply calibration changes from one day or low sample.
- Patch candidates require >=10 evaluated rows, >=2 days, hit_rate < 0.55 and repeated same-direction bias.
- All changes remain review-only until manually accepted.
