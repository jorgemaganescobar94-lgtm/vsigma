# vSIGMA API Shadow Rule Outcome Ledger - 2026-07-15

## Summary
- rules_available: 84
- candidate_rules_applied: 27
- shadow_rows: 10
- finished_shadow_rows: 10
- pending_shadow_rows: 0
- shadow_outcome_counts: HIT=10
- rule_market_counts: OVER_1_5=5; API_DNB=2; API_DOUBLE_CHANCE=2; UNDER_3_5=1
- paper_trade_permission_counts: SHADOW_ONLY=10
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=10
- pick_permission_counts: NO_PICK_PERMISSION=10
- stake_permission_counts: NO_STAKE_PERMISSION=10
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Market Shadow Summary
- API_DNB | evaluated=2 | HIT=2 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- API_DOUBLE_CHANCE | evaluated=2 | HIT=2 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- OVER_1_5 | evaluated=5 | HIT=5 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- UNDER_3_5 | evaluated=1 | HIT=1 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0

## Shadow Rows
- API_SHADOW_00001 | API_CAL_RULE_0002 | The New Saints vs Sabah FA | score=1-2 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00002 | API_CAL_RULE_0003 | The New Saints vs Sabah FA | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00003 | API_CAL_RULE_0005 | The New Saints vs Sabah FA | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00004 | API_CAL_RULE_0009 | The New Saints vs Sabah FA | score=1-2 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00005 | API_CAL_RULE_0010 | The New Saints vs Sabah FA | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00006 | API_CAL_RULE_0012 | The New Saints vs Sabah FA | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00007 | API_CAL_RULE_0040 | The New Saints vs Sabah FA | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00008 | API_CAL_RULE_0047 | The New Saints vs Sabah FA | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00009 | API_CAL_RULE_0049 | The New Saints vs Sabah FA | score=1-2 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00010 | API_CAL_RULE_0082 | The New Saints vs Sabah FA | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is shadow/paper-trading only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future promotion must be implemented separately after sufficient out-of-sample evidence exists.
