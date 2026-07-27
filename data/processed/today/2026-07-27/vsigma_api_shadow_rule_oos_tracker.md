# vSIGMA API Shadow Rule Out-of-Sample Tracker - 2026-07-27

## Summary
- registry_rules: 59
- rows_reviewed: 53
- in_sample_rows: 0
- out_of_sample_rows: 53
- pending_rows: 0
- evaluated_rows: 53
- oos_evaluated_rows: 53
- oos_hit_rows: 42
- oos_miss_rows: 1
- oos_void_rows: 10
- oos_hit_rate_pct: 79.2
- oos_hit_or_void_rate_pct: 98.1
- oos_class_counts: OUT_OF_SAMPLE=53
- oos_outcome_counts: HIT=42; VOID=10; MISS=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=53
- pick_permission_counts: NO_PICK_PERMISSION=53
- stake_permission_counts: NO_STAKE_PERMISSION=53
- next_action: Collect future OUT_OF_SAMPLE rows. No rule activation before sufficient out-of-sample sample size.
- auto_apply: NO
- production_change: NO

## Market Out-of-Sample Summary
- API_DNB | oos_evaluated=15 | HIT=5 | MISS=0 | VOID=10 | hit_rate=33.3 | hit_or_void=100.0
- API_DOUBLE_CHANCE | oos_evaluated=15 | HIT=15 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- OVER_1_5 | oos_evaluated=20 | HIT=20 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- UNDER_3_5 | oos_evaluated=3 | HIT=2 | MISS=1 | VOID=0 | hit_rate=66.7 | hit_or_void=66.7

## OOS Rows
- API_OOS_00001 | OUT_OF_SAMPLE | first_seen=2026-06-19 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00002 | OUT_OF_SAMPLE | first_seen=2026-06-19 | KFUM Oslo vs Molde | score=2-4 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00003 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Remo vs Vitoria | score=2-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00004 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Aalesund vs Viking | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00005 | OUT_OF_SAMPLE | first_seen=2026-06-19 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00006 | OUT_OF_SAMPLE | first_seen=2026-06-19 | KFUM Oslo vs Molde | score=2-4 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00007 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Remo vs Vitoria | score=2-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00008 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Aalesund vs Viking | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00009 | OUT_OF_SAMPLE | first_seen=2026-06-10 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00010 | OUT_OF_SAMPLE | first_seen=2026-06-10 | KFUM Oslo vs Molde | score=2-4 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00011 | OUT_OF_SAMPLE | first_seen=2026-06-10 | Remo vs Vitoria | score=2-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00012 | OUT_OF_SAMPLE | first_seen=2026-06-10 | Aalesund vs Viking | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00013 | OUT_OF_SAMPLE | first_seen=2026-06-18 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00014 | OUT_OF_SAMPLE | first_seen=2026-06-18 | KFUM Oslo vs Molde | score=2-4 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00015 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Aalesund vs Viking | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00016 | OUT_OF_SAMPLE | first_seen=2026-06-18 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00017 | OUT_OF_SAMPLE | first_seen=2026-06-18 | KFUM Oslo vs Molde | score=2-4 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00018 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Aalesund vs Viking | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00019 | OUT_OF_SAMPLE | first_seen=2026-06-18 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00020 | OUT_OF_SAMPLE | first_seen=2026-06-18 | KFUM Oslo vs Molde | score=2-4 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00021 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Aalesund vs Viking | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00022 | OUT_OF_SAMPLE | first_seen=2026-06-21 | Remo vs Vitoria | score=2-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00023 | OUT_OF_SAMPLE | first_seen=2026-06-21 | Remo vs Vitoria | score=2-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00024 | OUT_OF_SAMPLE | first_seen=2026-06-16 | Remo vs Vitoria | score=2-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00025 | OUT_OF_SAMPLE | first_seen=2026-06-18 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00026 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Aalesund vs Viking | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00027 | OUT_OF_SAMPLE | first_seen=2026-06-18 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00028 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Aalesund vs Viking | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00029 | OUT_OF_SAMPLE | first_seen=2026-06-18 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00030 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Aalesund vs Viking | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00031 | OUT_OF_SAMPLE | first_seen=2026-06-17 | KFUM Oslo vs Molde | score=2-4 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00032 | OUT_OF_SAMPLE | first_seen=2026-06-17 | Remo vs Vitoria | score=2-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00033 | OUT_OF_SAMPLE | first_seen=2026-06-20 | KFUM Oslo vs Molde | score=2-4 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00034 | OUT_OF_SAMPLE | first_seen=2026-06-20 | KFUM Oslo vs Molde | score=2-4 | market=UNDER_3_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00035 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Remo vs Vitoria | score=2-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00036 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Remo vs Vitoria | score=2-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00037 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Remo vs Vitoria | score=2-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00038 | OUT_OF_SAMPLE | first_seen=2026-06-20 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00039 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Aalesund vs Viking | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00040 | OUT_OF_SAMPLE | first_seen=2026-06-20 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00041 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Aalesund vs Viking | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00042 | OUT_OF_SAMPLE | first_seen=2026-06-20 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00043 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Aalesund vs Viking | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00044 | OUT_OF_SAMPLE | first_seen=2026-06-20 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=UNDER_3_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00045 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Aalesund vs Viking | score=1-1 | market=UNDER_3_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00046 | OUT_OF_SAMPLE | first_seen=2026-06-18 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00047 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Aalesund vs Viking | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00048 | OUT_OF_SAMPLE | first_seen=2026-06-18 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00049 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Aalesund vs Viking | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00050 | OUT_OF_SAMPLE | first_seen=2026-06-18 | IF Brommapojkarna vs Hammarby FF | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00051 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Aalesund vs Viking | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00052 | OUT_OF_SAMPLE | first_seen=2026-06-17 | KFUM Oslo vs Molde | score=2-4 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00053 | OUT_OF_SAMPLE | first_seen=2026-06-17 | Remo vs Vitoria | score=2-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This tracker separates bootstrap/in-sample rows from future out-of-sample rows.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Future promotion requires separate implementation after sufficient OUT_OF_SAMPLE evidence.
