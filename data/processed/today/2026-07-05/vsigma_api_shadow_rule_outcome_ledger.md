# vSIGMA API Shadow Rule Outcome Ledger - 2026-07-05

## Summary
- rules_available: 84
- candidate_rules_applied: 24
- shadow_rows: 26
- finished_shadow_rows: 26
- pending_shadow_rows: 0
- shadow_outcome_counts: HIT=13; MISS=13
- rule_market_counts: OVER_1_5=9; API_DNB=8; API_DOUBLE_CHANCE=8; UNDER_3_5=1
- paper_trade_permission_counts: SHADOW_ONLY=26
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=26
- pick_permission_counts: NO_PICK_PERMISSION=26
- stake_permission_counts: NO_STAKE_PERMISSION=26
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Market Shadow Summary
- API_DNB | evaluated=8 | HIT=4 | MISS=4 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0
- API_DOUBLE_CHANCE | evaluated=8 | HIT=4 | MISS=4 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0
- OVER_1_5 | evaluated=9 | HIT=4 | MISS=5 | VOID=0 | hit_rate=44.4 | hit_or_void=44.4
- UNDER_3_5 | evaluated=1 | HIT=1 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0

## Shadow Rows
- API_SHADOW_00001 | API_CAL_RULE_0002 | Degerfors IF vs Malmo FF | score=0-1 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00002 | API_CAL_RULE_0002 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00003 | API_CAL_RULE_0003 | Degerfors IF vs Malmo FF | score=0-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00004 | API_CAL_RULE_0003 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00005 | API_CAL_RULE_0005 | Degerfors IF vs Malmo FF | score=0-1 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00006 | API_CAL_RULE_0005 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00007 | API_CAL_RULE_0012 | Degerfors IF vs Malmo FF | score=0-1 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00008 | API_CAL_RULE_0016 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00009 | API_CAL_RULE_0017 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00010 | API_CAL_RULE_0019 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00011 | API_CAL_RULE_0030 | Degerfors IF vs Malmo FF | score=0-1 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00012 | API_CAL_RULE_0030 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00013 | API_CAL_RULE_0031 | Degerfors IF vs Malmo FF | score=0-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00014 | API_CAL_RULE_0031 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00015 | API_CAL_RULE_0033 | Degerfors IF vs Malmo FF | score=0-1 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00016 | API_CAL_RULE_0033 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00017 | API_CAL_RULE_0065 | Degerfors IF vs Malmo FF | score=0-1 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00018 | API_CAL_RULE_0066 | Degerfors IF vs Malmo FF | score=0-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00019 | API_CAL_RULE_0068 | Degerfors IF vs Malmo FF | score=0-1 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00020 | API_CAL_RULE_0070 | Degerfors IF vs Malmo FF | score=0-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00021 | API_CAL_RULE_0072 | Degerfors IF vs Malmo FF | score=0-1 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00022 | API_CAL_RULE_0072 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00023 | API_CAL_RULE_0073 | Degerfors IF vs Malmo FF | score=0-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00024 | API_CAL_RULE_0073 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00025 | API_CAL_RULE_0075 | Degerfors IF vs Malmo FF | score=0-1 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00026 | API_CAL_RULE_0075 | Jeonbuk Motors vs Gangwon FC | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is shadow/paper-trading only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future promotion must be implemented separately after sufficient out-of-sample evidence exists.
