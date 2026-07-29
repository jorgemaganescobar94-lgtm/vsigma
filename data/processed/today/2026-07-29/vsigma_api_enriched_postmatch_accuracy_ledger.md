# vSIGMA API-Enriched Postmatch Accuracy Ledger - 2026-07-29

## Summary
- rows_reviewed: 4
- finished_rows: 4
- pending_rows: 0
- accuracy_bucket_counts: PARTIAL_SIGNAL_VALIDATED=2; STRONG_SIGNAL_VALIDATED=2
- api_1x2_counts: MISS=2; HIT=2
- api_double_chance_counts: HIT=4
- api_dnb_counts: VOID=2; HIT=2
- over_1_5_counts: HIT=4
- over_2_5_counts: MISS=3; HIT=1
- under_3_5_counts: HIT=3; MISS=1
- btts_counts: HIT=3; MISS=1
- pick_permission_counts: NO_PICK_PERMISSION=4
- stake_permission_counts: NO_STAKE_PERMISSION=4
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
- auto_apply: NO
- production_change: NO

## Evaluated Rows
- IF Brommapojkarna vs Hammarby FF | result=1-1 | prediction=Hammarby FF | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- KFUM Oslo vs Molde | result=2-4 | prediction=Molde | side=AWAY | signal=61 MEDIUM_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=HIT | o2.5=HIT | u3.5=MISS | btts=HIT | bucket=STRONG_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Remo vs Vitoria | result=2-0 | prediction=Remo | side=HOME | signal=70 MEDIUM_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=MISS | bucket=STRONG_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Aalesund vs Viking | result=1-1 | prediction=Viking | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is postmatch calibration only.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
