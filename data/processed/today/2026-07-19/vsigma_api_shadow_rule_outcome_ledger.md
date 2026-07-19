# vSIGMA API Shadow Rule Outcome Ledger - 2026-07-19

## Summary
- rules_available: 84
- candidate_rules_applied: 24
- shadow_rows: 41
- finished_shadow_rows: 41
- pending_shadow_rows: 0
- shadow_outcome_counts: HIT=28; MISS=13
- rule_market_counts: OVER_1_5=15; API_DNB=13; API_DOUBLE_CHANCE=13
- paper_trade_permission_counts: SHADOW_ONLY=41
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=41
- pick_permission_counts: NO_PICK_PERMISSION=41
- stake_permission_counts: NO_STAKE_PERMISSION=41
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
- auto_apply: NO
- production_change: NO

## Market Shadow Summary
- API_DNB | evaluated=13 | HIT=9 | MISS=4 | VOID=0 | hit_rate=69.2 | hit_or_void=69.2
- API_DOUBLE_CHANCE | evaluated=13 | HIT=9 | MISS=4 | VOID=0 | hit_rate=69.2 | hit_or_void=69.2
- OVER_1_5 | evaluated=15 | HIT=10 | MISS=5 | VOID=0 | hit_rate=66.7 | hit_or_void=66.7

## Shadow Rows
- API_SHADOW_00001 | API_CAL_RULE_0002 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00002 | API_CAL_RULE_0002 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00003 | API_CAL_RULE_0002 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00004 | API_CAL_RULE_0003 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00005 | API_CAL_RULE_0003 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00006 | API_CAL_RULE_0003 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00007 | API_CAL_RULE_0005 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00008 | API_CAL_RULE_0005 | Atert Bissen vs KI Klaksvik | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00009 | API_CAL_RULE_0005 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00010 | API_CAL_RULE_0012 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00011 | API_CAL_RULE_0012 | Atert Bissen vs KI Klaksvik | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00012 | API_CAL_RULE_0016 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00013 | API_CAL_RULE_0017 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00014 | API_CAL_RULE_0019 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00015 | API_CAL_RULE_0030 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00016 | API_CAL_RULE_0030 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00017 | API_CAL_RULE_0030 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00018 | API_CAL_RULE_0031 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00019 | API_CAL_RULE_0031 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00020 | API_CAL_RULE_0031 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00021 | API_CAL_RULE_0033 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00022 | API_CAL_RULE_0033 | Atert Bissen vs KI Klaksvik | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00023 | API_CAL_RULE_0033 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00024 | API_CAL_RULE_0065 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00025 | API_CAL_RULE_0065 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00026 | API_CAL_RULE_0065 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00027 | API_CAL_RULE_0066 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00028 | API_CAL_RULE_0066 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00029 | API_CAL_RULE_0066 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00030 | API_CAL_RULE_0068 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00031 | API_CAL_RULE_0068 | Atert Bissen vs KI Klaksvik | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00032 | API_CAL_RULE_0068 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00033 | API_CAL_RULE_0072 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DNB | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00034 | API_CAL_RULE_0072 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00035 | API_CAL_RULE_0072 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DNB | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00036 | API_CAL_RULE_0073 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=API_DOUBLE_CHANCE | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00037 | API_CAL_RULE_0073 | Atert Bissen vs KI Klaksvik | score=1-2 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00038 | API_CAL_RULE_0073 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=API_DOUBLE_CHANCE | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00039 | API_CAL_RULE_0075 | Malisheva vs Vllaznia Shkodër | score=5-0 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00040 | API_CAL_RULE_0075 | Atert Bissen vs KI Klaksvik | score=1-2 | market=OVER_1_5 | outcome=HIT | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- API_SHADOW_00041 | API_CAL_RULE_0075 | Universitatea Craiova vs ML Vitebsk | score=1-0 | market=OVER_1_5 | outcome=MISS | status=SHADOW_EVALUATED | paper=SHADOW_ONLY | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is shadow/paper-trading only.
- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.
- Any future promotion must be implemented separately after sufficient out-of-sample evidence exists.
