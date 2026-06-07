# vSIGMA Calibration Memory Ledger - 2026-06-07

## Summary
- ledger_rows_total: 24
- metrics_tracked: 6
- memory_decision_counts: CALIBRATION_STABLE=4; MIXED_CALIBRATION_REVIEW=1; PATCH_CANDIDATE_REVIEW=1
- auto_apply_allowed: NO
- source_guard: DATED_INPUT_ONLY
- production_change: NO

## Metric Memory
- total_cards | days=4 | rows=19 | hit_rate=0.789 | bias=UNDER_ESTIMATE | decision=CALIBRATION_STABLE | patch=NO | next=Keep current model calibration and continue monitoring.
- total_corners | days=4 | rows=23 | hit_rate=0.565 | bias=OVER_ESTIMATE | decision=MIXED_CALIBRATION_REVIEW | patch=NO | next=Signal is mixed. Wait for more sample or segment by league/profile.
- total_fouls | days=4 | rows=24 | hit_rate=0.667 | bias=OVER_ESTIMATE | decision=CALIBRATION_STABLE | patch=NO | next=Keep current model calibration and continue monitoring.
- total_goals | days=4 | rows=26 | hit_rate=0.347 | bias=OVER_ESTIMATE | decision=PATCH_CANDIDATE_REVIEW | patch=YES_REVIEW_ONLY | next=Review lowering total_goals projection/range for matching profiles; do not auto-apply.
- total_shots | days=4 | rows=24 | hit_rate=0.750 | bias=OVER_ESTIMATE | decision=CALIBRATION_STABLE | patch=NO | next=Keep current model calibration and continue monitoring.
- total_sot | days=4 | rows=23 | hit_rate=0.696 | bias=UNDER_ESTIMATE | decision=CALIBRATION_STABLE | patch=NO | next=Keep current model calibration and continue monitoring.

## Governance Rules
- Never auto-apply calibration changes from one day or low sample.
- Patch candidates require >=10 evaluated rows, >=2 days, hit_rate < 0.55 and repeated same-direction bias.
- All changes remain review-only until manually accepted.
