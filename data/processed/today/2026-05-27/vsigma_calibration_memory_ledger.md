# vSIGMA Calibration Memory Ledger - 2026-05-27

## Summary
- ledger_rows_total: 12
- metrics_tracked: 6
- memory_decision_counts: ACCUMULATE_MORE_SAMPLE=5; PATCH_CANDIDATE_REVIEW=1
- auto_apply_allowed: NO
- source_guard: DATED_INPUT_ONLY
- production_change: NO

## Metric Memory
- total_cards | days=2 | rows=8 | hit_rate=0.750 | bias=UNDER_ESTIMATE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.
- total_corners | days=2 | rows=9 | hit_rate=0.556 | bias=OVER_ESTIMATE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.
- total_fouls | days=2 | rows=9 | hit_rate=0.778 | bias=UNDER_ESTIMATE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.
- total_goals | days=2 | rows=10 | hit_rate=0.100 | bias=OVER_ESTIMATE | decision=PATCH_CANDIDATE_REVIEW | patch=YES_REVIEW_ONLY | next=Review lowering total_goals projection/range for matching profiles; do not auto-apply.
- total_shots | days=2 | rows=9 | hit_rate=0.667 | bias=OVER_ESTIMATE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.
- total_sot | days=2 | rows=9 | hit_rate=0.555 | bias=UNDER_ESTIMATE | decision=ACCUMULATE_MORE_SAMPLE | patch=NO | next=Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days.

## Governance Rules
- Never auto-apply calibration changes from one day or low sample.
- Patch candidates require >=10 evaluated rows, >=2 days, hit_rate < 0.55 and repeated same-direction bias.
- All changes remain review-only until manually accepted.
