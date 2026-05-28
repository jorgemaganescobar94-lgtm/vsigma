# vSIGMA Calibration Memory Ledger - 2026-05-28

## Summary
- ledger_rows_total: 18
- metrics_tracked: 6
- memory_decision_counts: CALIBRATION_STABLE=5; PATCH_CANDIDATE_REVIEW=1
- auto_apply_allowed: NO
- source_guard: DATED_INPUT_ONLY
- production_change: NO

## Metric Memory
- total_cards | days=3 | rows=13 | hit_rate=0.769 | bias=UNDER_ESTIMATE | decision=CALIBRATION_STABLE | patch=NO | next=Keep current model calibration and continue monitoring.
- total_corners | days=3 | rows=15 | hit_rate=0.600 | bias=OVER_ESTIMATE | decision=CALIBRATION_STABLE | patch=NO | next=Keep current model calibration and continue monitoring.
- total_fouls | days=3 | rows=15 | hit_rate=0.734 | bias=UNDER_ESTIMATE | decision=CALIBRATION_STABLE | patch=NO | next=Keep current model calibration and continue monitoring.
- total_goals | days=3 | rows=16 | hit_rate=0.188 | bias=OVER_ESTIMATE | decision=PATCH_CANDIDATE_REVIEW | patch=YES_REVIEW_ONLY | next=Review lowering total_goals projection/range for matching profiles; do not auto-apply.
- total_shots | days=3 | rows=15 | hit_rate=0.733 | bias=OVER_ESTIMATE | decision=CALIBRATION_STABLE | patch=NO | next=Keep current model calibration and continue monitoring.
- total_sot | days=3 | rows=15 | hit_rate=0.733 | bias=UNDER_ESTIMATE | decision=CALIBRATION_STABLE | patch=NO | next=Keep current model calibration and continue monitoring.

## Governance Rules
- Never auto-apply calibration changes from one day or low sample.
- Patch candidates require >=10 evaluated rows, >=2 days, hit_rate < 0.55 and repeated same-direction bias.
- All changes remain review-only until manually accepted.
