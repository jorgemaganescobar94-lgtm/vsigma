# vSIGMA API Shadow Rule Out-of-Sample Tracker - 2026-06-26

## Summary
- registry_rules: 59
- rows_reviewed: 0
- in_sample_rows: 0
- out_of_sample_rows: 0
- pending_rows: 0
- evaluated_rows: 0
- oos_evaluated_rows: 0
- oos_hit_rows: 0
- oos_miss_rows: 0
- oos_void_rows: 0
- oos_hit_rate_pct: 
- oos_hit_or_void_rate_pct: 
- oos_class_counts: none
- oos_outcome_counts: none
- activation_permission_counts: none
- pick_permission_counts: none
- stake_permission_counts: none
- next_action: Collect future OUT_OF_SAMPLE rows. No rule activation before sufficient out-of-sample sample size.
- auto_apply: NO
- production_change: NO

## Market Out-of-Sample Summary
- none.

## OOS Rows

## Guardrails
- This tracker separates bootstrap/in-sample rows from future out-of-sample rows.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Future promotion requires separate implementation after sufficient OUT_OF_SAMPLE evidence.
