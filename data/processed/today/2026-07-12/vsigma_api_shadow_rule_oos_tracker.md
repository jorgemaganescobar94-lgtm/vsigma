# vSIGMA API Shadow Rule Out-of-Sample Tracker - 2026-07-12

## Summary
- registry_rules: 59
- rows_reviewed: 32
- in_sample_rows: 0
- out_of_sample_rows: 32
- pending_rows: 0
- evaluated_rows: 32
- oos_evaluated_rows: 32
- oos_hit_rows: 31
- oos_miss_rows: 1
- oos_void_rows: 0
- oos_hit_rate_pct: 96.9
- oos_hit_or_void_rate_pct: 96.9
- oos_class_counts: OUT_OF_SAMPLE=32
- oos_outcome_counts: HIT=31; MISS=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=32
- pick_permission_counts: NO_PICK_PERMISSION=32
- stake_permission_counts: NO_STAKE_PERMISSION=32
- next_action: Collect future OUT_OF_SAMPLE rows. No rule activation before sufficient out-of-sample sample size.
- auto_apply: NO
- production_change: NO

## Market Out-of-Sample Summary
- API_DNB | oos_evaluated=10 | HIT=10 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- API_DOUBLE_CHANCE | oos_evaluated=10 | HIT=10 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- OVER_1_5 | oos_evaluated=10 | HIT=10 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- UNDER_3_5 | oos_evaluated=2 | HIT=1 | MISS=1 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0

## OOS Rows
- API_OOS_00001 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00002 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00003 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00004 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00005 | OUT_OF_SAMPLE | first_seen=2026-06-10 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00006 | OUT_OF_SAMPLE | first_seen=2026-06-10 | Gwangju FC vs Pohang Steelers | score=0-3 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00007 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00008 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00009 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00010 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00011 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00012 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Gwangju FC vs Pohang Steelers | score=0-3 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00013 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00014 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00015 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00016 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00017 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00018 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Gwangju FC vs Pohang Steelers | score=0-3 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00019 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00020 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00021 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00022 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00023 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00024 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Gwangju FC vs Pohang Steelers | score=0-3 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00025 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=UNDER_3_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00026 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Gwangju FC vs Pohang Steelers | score=0-3 | market=UNDER_3_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00027 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00028 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00029 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00030 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00031 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00032 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Gwangju FC vs Pohang Steelers | score=0-3 | market=OVER_1_5 | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This tracker separates bootstrap/in-sample rows from future out-of-sample rows.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Future promotion requires separate implementation after sufficient OUT_OF_SAMPLE evidence.
