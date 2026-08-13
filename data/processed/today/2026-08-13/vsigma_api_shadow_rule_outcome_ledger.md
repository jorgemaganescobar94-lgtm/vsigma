# vSIGMA API Shadow Rule Outcome Ledger - 2026-08-13

## Summary
- rules_available: 84
- candidate_rules_applied: 27
- shadow_rows: 14
- finished_shadow_rows: 14
- pending_shadow_rows: 0
- shadow_outcome_counts: MISS=12; HIT=2
- rule_market_counts: API_DNB=4; API_DOUBLE_CHANCE=4; OVER_1_5=4; UNDER_3_5=2
- paper_trade_permission_counts: SHADOW_ONLY=14
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=14
- pick_permission_counts: NO_PICK_PERMISSION=14
- stake_permission_counts: NO_STAKE_PERMISSION=14
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Market Shadow Summary
- API_DNB | evaluated=4 | HIT=0 | MISS=4 | VOID=0 | hit_rate=0.0 | hit_or_void=0.0
- API_DOUBLE_CHANCE | evaluated=4 | HIT=0 | MISS=4 | VOID=0 | hit_rate=0.0 | hit_or_void=0.0
- OVER_1_5 | evaluated=4 | HIT=0 | MISS=4 | VOID=0 | hit_rate=0.0 | hit_or_void=0.0
- UNDER_3_5 | evaluated=2 | HIT=2 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0

## Shadow Rows
- API_SHADOW_00001 | API_CAL_RULE_0002 | RB Bragantino vs Atletico-MG | score=0-1 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00002 | API_CAL_RULE_0003 | RB Bragantino vs Atletico-MG | score=0-1 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00003 | API_CAL_RULE_0005 | RB Bragantino vs Atletico-MG | score=0-1 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00004 | API_CAL_RULE_0016 | RB Bragantino vs Atletico-MG | score=0-1 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00005 | API_CAL_RULE_0017 | RB Bragantino vs Atletico-MG | score=0-1 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00006 | API_CAL_RULE_0019 | RB Bragantino vs Atletico-MG | score=0-1 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00007 | API_CAL_RULE_0030 | RB Bragantino vs Atletico-MG | score=0-1 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00008 | API_CAL_RULE_0031 | RB Bragantino vs Atletico-MG | score=0-1 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00009 | API_CAL_RULE_0033 | RB Bragantino vs Atletico-MG | score=0-1 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00010 | API_CAL_RULE_0035 | RB Bragantino vs Atletico-MG | score=0-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00011 | API_CAL_RULE_0072 | RB Bragantino vs Atletico-MG | score=0-1 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00012 | API_CAL_RULE_0073 | RB Bragantino vs Atletico-MG | score=0-1 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00013 | API_CAL_RULE_0075 | RB Bragantino vs Atletico-MG | score=0-1 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00014 | API_CAL_RULE_0077 | RB Bragantino vs Atletico-MG | score=0-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is shadow/paper-trading only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future promotion must be implemented separately after sufficient out-of-sample evidence exists.
