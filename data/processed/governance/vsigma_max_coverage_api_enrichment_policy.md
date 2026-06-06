# vSIGMA Max-Coverage API Enrichment Policy - 2026-06-05

## Summary
- policy_status: MAX_COVERAGE_POLICY_READY
- api_plan_name: API-Football Ultra
- plan_requests_per_day: 75000
- rows_reviewed: 34
- rows_allowed: 34
- full_scoring_enrichment_rows: 15
- coverage_probe_rows: 14
- diagnostic_only_rows: 5
- blocked_rows: 0
- estimated_call_units: 160
- decision_counts: FULL_ENRICHMENT_ALLOWED_FOR_SCORING=15; COVERAGE_PROBE_ALLOWED_LOW_COVERAGE=14; DIAGNOSTIC_COVERAGE_ALLOWED_LOW_TRUST=5
- downstream_use_counts: SCORING_ALLOWED_WITH_NORMAL_GATES=15; COVERAGE_GATE_ONLY=14; DIAGNOSTIC_ONLY_NO_SCORING=5
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- auto_apply: NO
- production_change: NO

## Policy Rows
- Castellón vs Almeria | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- HK Kopavogur vs Afturelding | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Njardvik vs IR Reykjavik | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Ægir vs Leiknir R. | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Hvíti riddarinn vs Haukar | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Kormákur / Hvöt vs Magni | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- JS Kabylie vs CR Belouizdad | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- JS Saoura vs CS Constantine | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- MC Alger vs ASO Chlef | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Guarulhos vs Paulínia FU | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Binga vs US Bougouba | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Ituzaingó vs Real Pilar | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Wanderers vs Danubio | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Sabadell vs Real Madrid II | decision=DIAGNOSTIC_COVERAGE_ALLOWED_LOW_TRUST | downstream=DIAGNOSTIC_ONLY_NO_SCORING | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Plaza Colonia vs Sportivo Huracan | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Puerto Cabello II vs Zamora FC B | decision=DIAGNOSTIC_COVERAGE_ALLOWED_LOW_TRUST | downstream=DIAGNOSTIC_ONLY_NO_SCORING | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Preston Lions vs Melbourne City II | decision=DIAGNOSTIC_COVERAGE_ALLOWED_LOW_TRUST | downstream=DIAGNOSTIC_ONLY_NO_SCORING | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Tatran Všechovice vs Brumov | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Angola vs Mauritania | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Azerbaijan vs Malta | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Benin vs Niger | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Central African Republic vs Togo | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Hungary vs Finland | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Paraguay vs Nicaragua | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Allerheiligen vs FSC Hochegger Dächer | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Bruck an der Mur vs Union RB Weinland Gamlit | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Ilz vs Köflach | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Schladming vs Pachern | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Gurten vs Weiz | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Ried II vs SV Lafnitz | decision=DIAGNOSTIC_COVERAGE_ALLOWED_LOW_TRUST | downstream=DIAGNOSTIC_ONLY_NO_SCORING | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Voitsberg vs Wolfsberger AC II | decision=DIAGNOSTIC_COVERAGE_ALLOWED_LOW_TRUST | downstream=DIAGNOSTIC_ONLY_NO_SCORING | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Oberwart vs Krems / Rehberg | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- TWL Elektra vs SV Horn | decision=COVERAGE_PROBE_ALLOWED_LOW_COVERAGE | downstream=COVERAGE_GATE_ONLY | mode=COVERAGE_PROBE_ONLY | calls_executed=NO
- Estrella de Berisso vs Atletico Pilar | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO

## Guardrails
- This policy allows broad API coverage because the API plan is large.
- It does not execute external calls by itself.
- Low-trust fixtures may be queried for diagnostics, but cannot feed picks or scoring unless a separate reviewed model supports them.
- Enrichment never creates stake permission by itself.
