# vSIGMA API-Enriched Postmatch Accuracy Ledger - 2026-08-11

## Summary
- rows_reviewed: 1
- finished_rows: 1
- pending_rows: 0
- accuracy_bucket_counts: SIGNAL_FAILED=1
- api_1x2_counts: MISS=1
- api_double_chance_counts: MISS=1
- api_dnb_counts: MISS=1
- over_1_5_counts: MISS=1
- over_2_5_counts: MISS=1
- under_3_5_counts: HIT=1
- btts_counts: MISS=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
- auto_apply: NO
- production_change: NO

## Evaluated Rows
- Vasteras SK FK vs Djurgardens IF | result=1-0 | prediction=Djurgardens IF | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=MISS | dnb=MISS | o1.5=MISS | o2.5=MISS | u3.5=HIT | btts=MISS | bucket=SIGNAL_FAILED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is postmatch calibration only.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
