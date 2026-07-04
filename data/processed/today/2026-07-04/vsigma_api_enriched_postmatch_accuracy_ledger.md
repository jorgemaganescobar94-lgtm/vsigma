# vSIGMA API-Enriched Postmatch Accuracy Ledger - 2026-07-04

## Summary
- rows_reviewed: 1
- finished_rows: 1
- pending_rows: 0
- accuracy_bucket_counts: PARTIAL_SIGNAL_VALIDATED=1
- api_1x2_counts: MISS=1
- api_double_chance_counts: HIT=1
- api_dnb_counts: VOID=1
- over_1_5_counts: HIT=1
- over_2_5_counts: HIT=1
- under_3_5_counts: MISS=1
- btts_counts: HIT=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
- auto_apply: NO
- production_change: NO

## Evaluated Rows
- Sirius vs Mjallby AIF | result=4-4 | prediction=Sirius | side=HOME | signal=58 MEDIUM_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=HIT | u3.5=MISS | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is postmatch calibration only.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
