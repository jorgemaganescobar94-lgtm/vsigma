# vSIGMA API Shadow Rule Out-of-Sample Tracker - 2026-07-17

## Summary
- registry_rules: 59
- rows_reviewed: 45
- in_sample_rows: 0
- out_of_sample_rows: 45
- pending_rows: 0
- evaluated_rows: 45
- oos_evaluated_rows: 45
- oos_hit_rows: 30
- oos_miss_rows: 15
- oos_void_rows: 0
- oos_hit_rate_pct: 66.7
- oos_hit_or_void_rate_pct: 66.7
- oos_class_counts: OUT_OF_SAMPLE=45
- oos_outcome_counts: HIT=30; MISS=15
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=45
- pick_permission_counts: NO_PICK_PERMISSION=45
- stake_permission_counts: NO_STAKE_PERMISSION=45
- next_action: Collect future OUT_OF_SAMPLE rows. No rule activation before sufficient out-of-sample sample size.
- auto_apply: NO
- production_change: NO

## Market Out-of-Sample Summary
- API_DNB | oos_evaluated=15 | HIT=10 | MISS=5 | VOID=0 | hit_rate=66.7 | hit_or_void=66.7
- API_DOUBLE_CHANCE | oos_evaluated=15 | HIT=10 | MISS=5 | VOID=0 | hit_rate=66.7 | hit_or_void=66.7
- OVER_1_5 | oos_evaluated=15 | HIT=10 | MISS=5 | VOID=0 | hit_rate=66.7 | hit_or_void=66.7

## OOS Rows
- API_OOS_00001 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DNB | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00002 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00003 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00004 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DOUBLE_CHANCE | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00005 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00006 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00007 | OUT_OF_SAMPLE | first_seen=2026-06-10 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00008 | OUT_OF_SAMPLE | first_seen=2026-06-10 | Atert Bissen vs KI Klaksvik | score=1-2 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00009 | OUT_OF_SAMPLE | first_seen=2026-06-10 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=OVER_1_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00010 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DNB | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00011 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00012 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DOUBLE_CHANCE | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00013 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00014 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00015 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Atert Bissen vs KI Klaksvik | score=1-2 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00016 | OUT_OF_SAMPLE | first_seen=2026-06-21 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00017 | OUT_OF_SAMPLE | first_seen=2026-06-21 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00018 | OUT_OF_SAMPLE | first_seen=2026-06-16 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=OVER_1_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00019 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DNB | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00020 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00021 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00022 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DOUBLE_CHANCE | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00023 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00024 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00025 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00026 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Atert Bissen vs KI Klaksvik | score=1-2 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00027 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=OVER_1_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00028 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DNB | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00029 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00030 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00031 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DOUBLE_CHANCE | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00032 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00033 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00034 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00035 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Atert Bissen vs KI Klaksvik | score=1-2 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00036 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=OVER_1_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00037 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DNB | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00038 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00039 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00040 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DOUBLE_CHANCE | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00041 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00042 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00043 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00044 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Atert Bissen vs KI Klaksvik | score=1-2 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00045 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=OVER_1_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This tracker separates bootstrap/in-sample rows from future out-of-sample rows.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Future promotion requires separate implementation after sufficient OUT_OF_SAMPLE evidence.
