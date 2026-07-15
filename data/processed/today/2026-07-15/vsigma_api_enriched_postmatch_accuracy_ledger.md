# vSIGMA API-Enriched Postmatch Accuracy Ledger - 2026-07-15

## Summary
- rows_reviewed: 1
- finished_rows: 1
- pending_rows: 0
- accuracy_bucket_counts: STRONG_SIGNAL_VALIDATED=1
- api_1x2_counts: HIT=1
- api_double_chance_counts: HIT=1
- api_dnb_counts: HIT=1
- over_1_5_counts: HIT=1
- over_2_5_counts: HIT=1
- under_3_5_counts: HIT=1
- btts_counts: HIT=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
- auto_apply: NO
- production_change: NO

## Evaluated Rows
- The New Saints vs Sabah FA | result=1-2 | prediction=Sabah FA | side=AWAY | signal=55 MEDIUM_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=HIT | o2.5=HIT | u3.5=HIT | btts=HIT | bucket=STRONG_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is postmatch calibration only.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
