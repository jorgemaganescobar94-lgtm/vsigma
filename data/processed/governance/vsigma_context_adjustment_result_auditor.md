# vSIGMA Context Adjustment Result Auditor - 2026-05-23

## Executive Audit
- audit_verdict: CONTEXT_FILTER_IMPROVED_DAY
- base: 2W-1L, profit=0.16u
- adjusted counted: 1W-0L, profit=0.38u
- avoided_loss_units: 1.0
- missed_win_units: 0.78
- net_adjustment_delta_units: 0.22
- audit_label_counts: AVOIDED_LOSS=1; MISSED_WIN=1; KEPT_WIN=1
- auto_apply: NO
- production_change: NO

## Detail Rows
- #1 | AVOIDED_LOSS | Bologna vs Inter | market=AWAY_WIN | base=LOSS -1.0u | adjusted=BET_DOWNGRADED_TO_REVIEW | effect=1.0u
- #2 | MISSED_WIN | Lazio vs Pisa | market=HOME_WIN | base=WIN 0.78u | adjusted=BET_DOWNGRADED_TO_REVIEW | effect=-0.78u
- #3 | KEPT_WIN | Kalmar FF vs Degerfors IF | market=OVER_1_5 | base=WIN 0.38u | adjusted=SHADOW_RISK_ONLY | effect=0.38u

## Guardrails
- This audit does not rewrite historical results.
- Use repeated audits before changing thresholds or context rules.
