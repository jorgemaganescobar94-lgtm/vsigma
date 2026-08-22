# vSIGMA API Shadow Rule Outcome Ledger - 2026-08-22

## Summary
- rules_available: 84
- candidate_rules_applied: 28
- shadow_rows: 38
- finished_shadow_rows: 38
- pending_shadow_rows: 0
- shadow_outcome_counts: HIT=28; VOID=10
- rule_market_counts: API_DNB=10; API_DOUBLE_CHANCE=10; OVER_1_5=10; UNDER_3_5=8
- paper_trade_permission_counts: SHADOW_ONLY=38
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=38
- pick_permission_counts: NO_PICK_PERMISSION=38
- stake_permission_counts: NO_STAKE_PERMISSION=38
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Market Shadow Summary
- API_DNB | evaluated=10 | HIT=0 | MISS=0 | VOID=10 | hit_rate=0.0 | hit_or_void=100.0
- API_DOUBLE_CHANCE | evaluated=10 | HIT=10 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- OVER_1_5 | evaluated=10 | HIT=10 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0
- UNDER_3_5 | evaluated=8 | HIT=8 | MISS=0 | VOID=0 | hit_rate=100.0 | hit_or_void=100.0

## Shadow Rows
- API_SHADOW_00001 | API_CAL_RULE_0002 | Fenerbahçe vs Lyon | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00002 | API_CAL_RULE_0002 | Independ. Rivadavia vs Fluminense | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00003 | API_CAL_RULE_0003 | Fenerbahçe vs Lyon | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00004 | API_CAL_RULE_0003 | Independ. Rivadavia vs Fluminense | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00005 | API_CAL_RULE_0005 | Fenerbahçe vs Lyon | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00006 | API_CAL_RULE_0005 | Independ. Rivadavia vs Fluminense | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00007 | API_CAL_RULE_0016 | Fenerbahçe vs Lyon | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00008 | API_CAL_RULE_0016 | Independ. Rivadavia vs Fluminense | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00009 | API_CAL_RULE_0017 | Fenerbahçe vs Lyon | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00010 | API_CAL_RULE_0017 | Independ. Rivadavia vs Fluminense | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00011 | API_CAL_RULE_0019 | Fenerbahçe vs Lyon | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00012 | API_CAL_RULE_0019 | Independ. Rivadavia vs Fluminense | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00013 | API_CAL_RULE_0021 | Fenerbahçe vs Lyon | score=1-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00014 | API_CAL_RULE_0021 | Independ. Rivadavia vs Fluminense | score=1-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00015 | API_CAL_RULE_0030 | Fenerbahçe vs Lyon | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00016 | API_CAL_RULE_0030 | Independ. Rivadavia vs Fluminense | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00017 | API_CAL_RULE_0031 | Fenerbahçe vs Lyon | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00018 | API_CAL_RULE_0031 | Independ. Rivadavia vs Fluminense | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00019 | API_CAL_RULE_0033 | Fenerbahçe vs Lyon | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00020 | API_CAL_RULE_0033 | Independ. Rivadavia vs Fluminense | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00021 | API_CAL_RULE_0035 | Fenerbahçe vs Lyon | score=1-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00022 | API_CAL_RULE_0035 | Independ. Rivadavia vs Fluminense | score=1-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00023 | API_CAL_RULE_0065 | Fenerbahçe vs Lyon | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00024 | API_CAL_RULE_0065 | Independ. Rivadavia vs Fluminense | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00025 | API_CAL_RULE_0066 | Fenerbahçe vs Lyon | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00026 | API_CAL_RULE_0066 | Independ. Rivadavia vs Fluminense | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00027 | API_CAL_RULE_0068 | Fenerbahçe vs Lyon | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00028 | API_CAL_RULE_0068 | Independ. Rivadavia vs Fluminense | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00029 | API_CAL_RULE_0070 | Fenerbahçe vs Lyon | score=1-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00030 | API_CAL_RULE_0070 | Independ. Rivadavia vs Fluminense | score=1-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00031 | API_CAL_RULE_0072 | Fenerbahçe vs Lyon | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00032 | API_CAL_RULE_0072 | Independ. Rivadavia vs Fluminense | score=1-1 | market=API_DNB | outcome=VOID | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00033 | API_CAL_RULE_0073 | Fenerbahçe vs Lyon | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00034 | API_CAL_RULE_0073 | Independ. Rivadavia vs Fluminense | score=1-1 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00035 | API_CAL_RULE_0075 | Fenerbahçe vs Lyon | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00036 | API_CAL_RULE_0075 | Independ. Rivadavia vs Fluminense | score=1-1 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00037 | API_CAL_RULE_0077 | Fenerbahçe vs Lyon | score=1-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00038 | API_CAL_RULE_0077 | Independ. Rivadavia vs Fluminense | score=1-1 | market=UNDER_3_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is shadow/paper-trading only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future promotion must be implemented separately after sufficient out-of-sample evidence exists.
