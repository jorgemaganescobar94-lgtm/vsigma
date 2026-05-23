# vSIGMA Real Objective Context Gate - 2026-05-23

## Summary
- rows_reviewed: 3
- context_gate_decision_counts: CONTEXT_DOWNGRADE=2; TABLE_PROXY_TEMPO=1
- objective_override_status_counts: REAL_OVERRIDE=2; PROXY_ONLY=1
- auto_apply: NO
- production_change: NO

## Rows
- #1 | CONTEXT_DOWNGRADE | Bologna vs Inter | market=AWAY_WIN | override=REAL_OVERRIDE | edge=NEUTRAL | action=Downgrade side market; do not treat ranking proxy as motivation
- #2 | CONTEXT_DOWNGRADE | Lazio vs Pisa | market=HOME_WIN | override=REAL_OVERRIDE | edge=NEUTRAL | action=Downgrade side market; do not treat ranking proxy as motivation
- #3 | TABLE_PROXY_TEMPO | Kalmar FF vs Degerfors IF | market=OVER_1_5 | override=PROXY_ONLY | edge=TEMPO | action=No real objective override available

## Guardrails
- Real context overrides ranking urgency proxy.
- This report does not change production picks automatically.
