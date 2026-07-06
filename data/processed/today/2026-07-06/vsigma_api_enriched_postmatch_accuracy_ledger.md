# vSIGMA API-Enriched Postmatch Accuracy Ledger - 2026-07-06

## Summary
- rows_reviewed: 2
- finished_rows: 2
- pending_rows: 0
- accuracy_bucket_counts: PARTIAL_SIGNAL_VALIDATED=2
- api_1x2_counts: HIT=1; MISS=1
- api_double_chance_counts: HIT=1; MISS=1
- api_dnb_counts: HIT=1; MISS=1
- over_1_5_counts: MISS=1; HIT=1
- over_2_5_counts: MISS=1; HIT=1
- under_3_5_counts: HIT=2
- btts_counts: MISS=1; HIT=1
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
- auto_apply: NO
- production_change: NO

## Evaluated Rows
- Degerfors IF vs Malmo FF | result=0-1 | prediction=Malmo FF | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=MISS | o2.5=MISS | u3.5=HIT | btts=MISS | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Jeonbuk Motors vs Gangwon FC | result=1-2 | prediction=Jeonbuk Motors | side=HOME | signal=81 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=MISS | dnb=MISS | o1.5=HIT | o2.5=HIT | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is postmatch calibration only.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
