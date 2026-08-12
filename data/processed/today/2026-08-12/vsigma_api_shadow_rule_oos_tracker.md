# vSIGMA API Shadow Rule Out-of-Sample Tracker - 2026-08-12

## Summary
- registry_rules: 59
- rows_reviewed: 9
- in_sample_rows: 0
- out_of_sample_rows: 9
- pending_rows: 0
- evaluated_rows: 9
- oos_evaluated_rows: 9
- oos_hit_rows: 4
- oos_miss_rows: 5
- oos_void_rows: 0
- oos_hit_rate_pct: 44.4
- oos_hit_or_void_rate_pct: 44.4
- oos_class_counts: OUT_OF_SAMPLE=9
- oos_outcome_counts: MISS=5; HIT=4
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=9
- pick_permission_counts: NO_PICK_PERMISSION=9
- stake_permission_counts: NO_STAKE_PERMISSION=9
- next_action: Collect future OUT_OF_SAMPLE rows. No rule activation before sufficient out-of-sample sample size.
- auto_apply: NO
- production_change: NO

## Market Out-of-Sample Summary
- API_DNB | oos_evaluated=2 | HIT=2 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- API_DOUBLE_CHANCE | oos_evaluated=2 | HIT=2 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- OVER_1_5 | oos_evaluated=5 | HIT=0 | MISS=5 | VOID=0 | hit_rate=0.0 | hit_or_void=0.0

## OOS Rows
- API_OOS_00001 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Kairat Almaty vs Levski Sofia | score=0-1 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00002 | OUT_OF_SAMPLE | first_seen=2026-06-19 | Kairat Almaty vs Levski Sofia | score=0-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00003 | OUT_OF_SAMPLE | first_seen=2026-06-10 | Kairat Almaty vs Levski Sofia | score=0-1 | market=OVER_1_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00004 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Kairat Almaty vs Levski Sofia | score=0-1 | market=API_DNB | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00005 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Kairat Almaty vs Levski Sofia | score=0-1 | market=API_DOUBLE_CHANCE | outcome=HIT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00006 | OUT_OF_SAMPLE | first_seen=2026-06-18 | Kairat Almaty vs Levski Sofia | score=0-1 | market=OVER_1_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00007 | OUT_OF_SAMPLE | first_seen=2026-06-17 | Kairat Almaty vs Levski Sofia | score=0-1 | market=OVER_1_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00008 | OUT_OF_SAMPLE | first_seen=2026-06-20 | Kairat Almaty vs Levski Sofia | score=0-1 | market=OVER_1_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_OOS_00009 | OUT_OF_SAMPLE | first_seen=2026-06-17 | Kairat Almaty vs Levski Sofia | score=0-1 | market=OVER_1_5 | outcome=MISS | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This tracker separates bootstrap/in-sample rows from future out-of-sample rows.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Future promotion requires separate implementation after sufficient OUT_OF_SAMPLE evidence.
