# vSIGMA API-Enriched Postmatch Accuracy Ledger - 2026-07-19

## Summary
- rows_reviewed: 3
- finished_rows: 3
- pending_rows: 0
- accuracy_bucket_counts: SIGNAL_FAILED=1; STRONG_SIGNAL_VALIDATED=1; PARTIAL_SIGNAL_VALIDATED=1
- api_1x2_counts: HIT=2; MISS=1
- api_double_chance_counts: HIT=2; MISS=1
- api_dnb_counts: HIT=2; MISS=1
- over_1_5_counts: HIT=2; MISS=1
- over_2_5_counts: HIT=2; MISS=1
- under_3_5_counts: HIT=2; MISS=1
- btts_counts: MISS=2; HIT=1
- pick_permission_counts: NO_PICK_PERMISSION=3
- stake_permission_counts: NO_STAKE_PERMISSION=3
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
- auto_apply: NO
- production_change: NO

## Evaluated Rows
- Malisheva vs Vllaznia Shkodër | result=5-0 | prediction=Vllaznia Shkodër | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=MISS | dnb=MISS | o1.5=HIT | o2.5=HIT | u3.5=MISS | btts=MISS | bucket=SIGNAL_FAILED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Atert Bissen vs KI Klaksvik | result=1-2 | prediction=KI Klaksvik | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=HIT | o2.5=HIT | u3.5=HIT | btts=HIT | bucket=STRONG_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Universitatea Craiova vs ML Vitebsk | result=1-0 | prediction=Universitatea Craiova | side=HOME | signal=100 HIGH_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=MISS | o2.5=MISS | u3.5=HIT | btts=MISS | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is postmatch calibration only.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
