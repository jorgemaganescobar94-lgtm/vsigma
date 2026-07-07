# vSIGMA API Shadow Rule Outcome Ledger - 2026-07-07

## Summary
- rules_available: 84
- candidate_rules_applied: 27
- shadow_rows: 13
- finished_shadow_rows: 13
- pending_shadow_rows: 0
- shadow_outcome_counts: HIT=13
- rule_market_counts: OVER_1_5=5; API_DNB=4; API_DOUBLE_CHANCE=4
- paper_trade_permission_counts: SHADOW_ONLY=13
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=13
- pick_permission_counts: NO_PICK_PERMISSION=13
- stake_permission_counts: NO_STAKE_PERMISSION=13
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Market Shadow Summary
- API_DNB | evaluated=4 | HIT=4 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- API_DOUBLE_CHANCE | evaluated=4 | HIT=4 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- OVER_1_5 | evaluated=5 | HIT=5 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0

## Shadow Rows
- API_SHADOW_00001 | API_CAL_RULE_0002 | BK Hacken vs Djurgardens IF | score=2-4 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00002 | API_CAL_RULE_0003 | BK Hacken vs Djurgardens IF | score=2-4 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00003 | API_CAL_RULE_0005 | BK Hacken vs Djurgardens IF | score=2-4 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00004 | API_CAL_RULE_0009 | BK Hacken vs Djurgardens IF | score=2-4 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00005 | API_CAL_RULE_0010 | BK Hacken vs Djurgardens IF | score=2-4 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00006 | API_CAL_RULE_0012 | BK Hacken vs Djurgardens IF | score=2-4 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00007 | API_CAL_RULE_0030 | BK Hacken vs Djurgardens IF | score=2-4 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00008 | API_CAL_RULE_0031 | BK Hacken vs Djurgardens IF | score=2-4 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00009 | API_CAL_RULE_0033 | BK Hacken vs Djurgardens IF | score=2-4 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00010 | API_CAL_RULE_0061 | BK Hacken vs Djurgardens IF | score=2-4 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00011 | API_CAL_RULE_0072 | BK Hacken vs Djurgardens IF | score=2-4 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00012 | API_CAL_RULE_0073 | BK Hacken vs Djurgardens IF | score=2-4 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00013 | API_CAL_RULE_0075 | BK Hacken vs Djurgardens IF | score=2-4 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is shadow/paper-trading only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future promotion must be implemented separately after sufficient out-of-sample evidence exists.
