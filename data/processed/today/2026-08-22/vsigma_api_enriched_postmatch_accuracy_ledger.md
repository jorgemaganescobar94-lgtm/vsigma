# vSIGMA API-Enriched Postmatch Accuracy Ledger - 2026-08-22

## Summary
- rows_reviewed: 2
- finished_rows: 2
- pending_rows: 0
- accuracy_bucket_counts: PARTIAL_SIGNAL_VALIDATED=2
- api_1x2_counts: MISS=2
- api_double_chance_counts: HIT=2
- api_dnb_counts: VOID=2
- over_1_5_counts: HIT=2
- over_2_5_counts: MISS=2
- under_3_5_counts: HIT=2
- btts_counts: HIT=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
- auto_apply: NO
- production_change: NO

## Evaluated Rows
- Fenerbahçe vs Lyon | result=1-1 | prediction=Fenerbahçe | side=HOME | signal=92 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Independ. Rivadavia vs Fluminense | result=1-1 | prediction=Independ. Rivadavia | side=HOME | signal=100 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is postmatch calibration only.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
