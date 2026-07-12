# vSIGMA API Shadow Rule Outcome Ledger - 2026-07-12

## Summary
- rules_available: 84
- candidate_rules_applied: 27
- shadow_rows: 32
- finished_shadow_rows: 32
- pending_shadow_rows: 0
- shadow_outcome_counts: HIT=31; MISS=1
- rule_market_counts: API_DNB=10; API_DOUBLE_CHANCE=10; OVER_1_5=10; UNDER_3_5=2
- paper_trade_permission_counts: SHADOW_ONLY=32
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=32
- pick_permission_counts: NO_PICK_PERMISSION=32
- stake_permission_counts: NO_STAKE_PERMISSION=32
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Market Shadow Summary
- API_DNB | evaluated=10 | HIT=10 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- API_DOUBLE_CHANCE | evaluated=10 | HIT=10 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- OVER_1_5 | evaluated=10 | HIT=10 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- UNDER_3_5 | evaluated=2 | HIT=1 | MISS=1 | VOID=0 | hit_rate=50.0 | hit_or_void=50.0

## Shadow Rows
- API_SHADOW_00001 | API_CAL_RULE_0002 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00002 | API_CAL_RULE_0002 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00003 | API_CAL_RULE_0003 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00004 | API_CAL_RULE_0003 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00005 | API_CAL_RULE_0005 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00006 | API_CAL_RULE_0005 | Gwangju FC vs Pohang Steelers | score=0-3 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00007 | API_CAL_RULE_0009 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00008 | API_CAL_RULE_0009 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00009 | API_CAL_RULE_0010 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00010 | API_CAL_RULE_0010 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00011 | API_CAL_RULE_0012 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00012 | API_CAL_RULE_0012 | Gwangju FC vs Pohang Steelers | score=0-3 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00013 | API_CAL_RULE_0030 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00014 | API_CAL_RULE_0030 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00015 | API_CAL_RULE_0031 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00016 | API_CAL_RULE_0031 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00017 | API_CAL_RULE_0033 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00018 | API_CAL_RULE_0033 | Gwangju FC vs Pohang Steelers | score=0-3 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00019 | API_CAL_RULE_0065 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00020 | API_CAL_RULE_0065 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00021 | API_CAL_RULE_0066 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00022 | API_CAL_RULE_0066 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00023 | API_CAL_RULE_0068 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00024 | API_CAL_RULE_0068 | Gwangju FC vs Pohang Steelers | score=0-3 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00025 | API_CAL_RULE_0070 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=UNDER_3_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00026 | API_CAL_RULE_0070 | Gwangju FC vs Pohang Steelers | score=0-3 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00027 | API_CAL_RULE_0072 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00028 | API_CAL_RULE_0072 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00029 | API_CAL_RULE_0073 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00030 | API_CAL_RULE_0073 | Gwangju FC vs Pohang Steelers | score=0-3 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00031 | API_CAL_RULE_0075 | Ulsan Hyundai FC vs Jeonbuk Motors | score=1-3 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00032 | API_CAL_RULE_0075 | Gwangju FC vs Pohang Steelers | score=0-3 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is shadow/paper-trading only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future promotion must be implemented separately after sufficient out-of-sample evidence exists.
