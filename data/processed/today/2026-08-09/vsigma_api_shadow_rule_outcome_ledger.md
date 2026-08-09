# vSIGMA API Shadow Rule Outcome Ledger - 2026-08-09

## Summary
- rules_available: 84
- candidate_rules_applied: 28
- shadow_rows: 11
- finished_shadow_rows: 11
- pending_shadow_rows: 0
- shadow_outcome_counts: HIT=8; VOID=3
- rule_market_counts: OVER_1_5=5; API_DNB=3; API_DOUBLE_CHANCE=3
- paper_trade_permission_counts: SHADOW_ONLY=11
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=11
- pick_permission_counts: NO_PICK_PERMISSION=11
- stake_permission_counts: NO_STAKE_PERMISSION=11
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Market Shadow Summary
- API_DNB | evaluated=3 | HIT=0 | MISS=0 | VOID=3 | hit_rate=0.0 | hit_or_void=100.0
- API_DOUBLE_CHANCE | evaluated=3 | HIT=3 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- OVER_1_5 | evaluated=5 | HIT=5 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0

## Shadow Rows
- API_SHADOW_00001 | API_CAL_RULE_0002 | Dundee Utd vs Rangers | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00002 | API_CAL_RULE_0003 | Dundee Utd vs Rangers | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00003 | API_CAL_RULE_0005 | Dundee Utd vs Rangers | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00004 | API_CAL_RULE_0009 | Dundee Utd vs Rangers | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00005 | API_CAL_RULE_0010 | Dundee Utd vs Rangers | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00006 | API_CAL_RULE_0012 | Dundee Utd vs Rangers | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00007 | API_CAL_RULE_0040 | Dundee Utd vs Rangers | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00008 | API_CAL_RULE_0051 | Dundee Utd vs Rangers | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00009 | API_CAL_RULE_0052 | Dundee Utd vs Rangers | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00010 | API_CAL_RULE_0054 | Dundee Utd vs Rangers | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00011 | API_CAL_RULE_0082 | Dundee Utd vs Rangers | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is shadow/paper-trading only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future promotion must be implemented separately after sufficient out-of-sample evidence exists.
