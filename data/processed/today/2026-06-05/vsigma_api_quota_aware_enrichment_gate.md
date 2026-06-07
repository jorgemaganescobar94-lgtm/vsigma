# vSIGMA API Quota-Aware Enrichment Gate - 2026-06-05

## Summary
- quota_gate_status: AUTO_ENRICHMENT_ALLOWED_LIMITED
- api_plan_name: API-Football Ultra
- plan_requests_per_day: 75000
- rows_reviewed: 35
- p1_rows: 19
- p2_rows: 16
- p1_estimated_units: 95
- p2_estimated_units: 70
- p2_probe_units: 16
- total_estimated_units: 165
- auto_units_reserved: 111
- max_auto_units_per_day: 5000
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=19; COVERAGE_PROBE_ALLOWED_P2=16
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
- auto_apply: NO
- production_change: NO

## Allowlist / Policy Rows
- Las Palmas vs Malaga | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Castellón vs Almeria | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- HK Kopavogur vs Afturelding | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Njardvik vs IR Reykjavik | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Ægir vs Leiknir R. | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Hvíti riddarinn vs Haukar | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Kormákur / Hvöt vs Magni | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- JS Kabylie vs CR Belouizdad | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- JS Saoura vs CS Constantine | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- MC Alger vs ASO Chlef | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Guarulhos vs Paulínia FU | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Binga vs US Bougouba | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Ituzaingó vs Real Pilar | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Wanderers vs Danubio | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Sabadell vs Real Madrid II | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Plaza Colonia vs Sportivo Huracan | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Puerto Cabello II vs Zamora FC B | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Preston Lions vs Melbourne City II | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Tatran Všechovice vs Brumov | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Angola vs Mauritania | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Azerbaijan vs Malta | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Benin vs Niger | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Central African Republic vs Togo | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Hungary vs Finland | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Paraguay vs Nicaragua | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Allerheiligen vs FSC Hochegger Dächer | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Bruck an der Mur vs Union RB Weinland Gamlit | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Ilz vs Köflach | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Schladming vs Pachern | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Gurten vs Weiz | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Ried II vs SV Lafnitz | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Voitsberg vs Wolfsberger AC II | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Oberwart vs Krems / Rehberg | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- TWL Elektra vs SV Horn | priority=P2_LOW_COVERAGE_SCORING | risk=HIGH_LOW_COVERAGE | decision=COVERAGE_PROBE_ALLOWED_P2 | mode=COVERAGE_PROBE_ONLY | reserved=1 | api_allowed=YES_PROBE_ONLY | executed=NO
- Estrella de Berisso vs Atletico Pilar | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO

## Guardrails
- This gate is policy/allowlist only; it does not call APIs.
- API calls executed remains NO until a separate enrichment executor is explicitly run.
- P1 may be auto-allowlisted within quota; P2 is coverage-probe-only; volatile/manual rows stay blocked.
- Enrichment alone never creates pick or stake permission.
