# vSIGMA API Shadow Rule Out-of-Sample Tracker - 2026-07-20

## Summary
- registry_rules: 59
- rows_reviewed: 43
- in_sample_rows: 0
- out_of_sample_rows: 43
- pending_rows: 0
- evaluated_rows: 43
- oos_evaluated_rows: 43
- oos_hit_rows: 38
- oos_miss_rows: 0
- oos_void_rows: 5
- oos_hit_rate_pct: 88.4
- oos_hit_or_void_rate_pct: 100.0
- oos_class_counts: OUT_OF_SAMPLE=43
- oos_outcome_counts: HIT=38; VOID=5
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=43
- pick_permission_counts: NO_PICK_PERMISSION=43
- stake_permission_counts: NO_STAKE_PERMISSION=43
- next_action: Collect future OUT_OF_SAMPLE rows. No rule activation before sufficient out-of-sample sample size.
- auto_apply: NO
- production_change: NO

## Market Out-of-Sample Summary
- API_DNB | oos_evaluated=14 | HIT=9 | MISS=0 | VOID=5 | hit_rate=64.3 | hit_or_void=100.0
- API_DOUBLE_CHANCE | oos_evaluated=14 | HIT=14 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- OVER_1_5 | oos_evaluated=15 | HIT=15 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0

## OOS Rows
- API_OOS_00001 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Hammarby FF vs Degerfors IF | score=4-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00002 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Halmstad vs BK Hacken | score=0-2 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00003 | OUT_OF_SAMPLE | first_seen=2026-06-19 | FC Anyang vs Gwangju FC | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00004 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Hammarby FF vs Degerfors IF | score=4-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00005 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Halmstad vs BK Hacken | score=0-2 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00006 | OUT_OF_SAMPLE | first_seen=2026-06-19 | FC Anyang vs Gwangju FC | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00007 | OUT_OF_SAMPLE | first_seen=2026-06-10 | Hammarby FF vs Degerfors IF | score=4-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00008 | OUT_OF_SAMPLE | first_seen=2026-06-10 | Halmstad vs BK Hacken | score=0-2 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00009 | OUT_OF_SAMPLE | first_seen=2026-06-10 | FC Anyang vs Gwangju FC | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00010 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Halmstad vs BK Hacken | score=0-2 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00011 | OUT_OF_SAMPLE | first_seen=2026-06-21 | Hammarby FF vs Degerfors IF | score=4-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00012 | OUT_OF_SAMPLE | first_seen=2026-06-21 | FC Anyang vs Gwangju FC | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00013 | OUT_OF_SAMPLE | first_seen=2026-06-21 | Hammarby FF vs Degerfors IF | score=4-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00014 | OUT_OF_SAMPLE | first_seen=2026-06-21 | FC Anyang vs Gwangju FC | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00015 | OUT_OF_SAMPLE | first_seen=2026-06-16 | Hammarby FF vs Degerfors IF | score=4-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00016 | OUT_OF_SAMPLE | first_seen=2026-06-16 | FC Anyang vs Gwangju FC | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00017 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Hammarby FF vs Degerfors IF | score=4-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00018 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Halmstad vs BK Hacken | score=0-2 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00019 | OUT_OF_SAMPLE | first_seen=2026-06-18 | FC Anyang vs Gwangju FC | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00020 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Hammarby FF vs Degerfors IF | score=4-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00021 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Halmstad vs BK Hacken | score=0-2 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00022 | OUT_OF_SAMPLE | first_seen=2026-06-18 | FC Anyang vs Gwangju FC | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00023 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Hammarby FF vs Degerfors IF | score=4-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00024 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Halmstad vs BK Hacken | score=0-2 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00025 | OUT_OF_SAMPLE | first_seen=2026-06-18 | FC Anyang vs Gwangju FC | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00026 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Hammarby FF vs Degerfors IF | score=4-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00027 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Halmstad vs BK Hacken | score=0-2 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00028 | OUT_OF_SAMPLE | first_seen=2026-06-20 | FC Anyang vs Gwangju FC | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00029 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Hammarby FF vs Degerfors IF | score=4-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00030 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Halmstad vs BK Hacken | score=0-2 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00031 | OUT_OF_SAMPLE | first_seen=2026-06-20 | FC Anyang vs Gwangju FC | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00032 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Hammarby FF vs Degerfors IF | score=4-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00033 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Halmstad vs BK Hacken | score=0-2 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00034 | OUT_OF_SAMPLE | first_seen=2026-06-20 | FC Anyang vs Gwangju FC | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00035 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Hammarby FF vs Degerfors IF | score=4-0 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00036 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Halmstad vs BK Hacken | score=0-2 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00037 | OUT_OF_SAMPLE | first_seen=2026-06-18 | FC Anyang vs Gwangju FC | score=1-1 | market=API_DNB | outcome=VOID | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00038 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Hammarby FF vs Degerfors IF | score=4-0 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00039 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Halmstad vs BK Hacken | score=0-2 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00040 | OUT_OF_SAMPLE | first_seen=2026-06-18 | FC Anyang vs Gwangju FC | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00041 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Hammarby FF vs Degerfors IF | score=4-0 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00042 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Halmstad vs BK Hacken | score=0-2 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00043 | OUT_OF_SAMPLE | first_seen=2026-06-18 | FC Anyang vs Gwangju FC | score=1-1 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This tracker separates bootstrap/in-sample rows from future out-of-sample rows.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Future promotion requires separate implementation after sufficient OUT_OF_SAMPLE evidence.
