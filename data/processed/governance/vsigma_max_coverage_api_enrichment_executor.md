# vSIGMA Max-Coverage API Enrichment Executor - 2026-06-05

## Summary
- executor_status: EXECUTION_COMPLETE
- policy_rows_reviewed: 35
- rows_selected: 35
- rows_executed: 35
- rows_dry_run: 0
- rows_success_any: 5
- rows_failed_all: 30
- scoring_allowed_rows: 16
- coverage_probe_rows: 14
- diagnostic_only_rows: 5
- endpoint_success_counts: fixture_detail=4; predictions=3; statistics=2; events=2; lineups=2; odds=2
- endpoint_failure_counts: fixture_detail=31; statistics=28; events=28; odds=14; lineups=14; predictions=13
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: YES_LOGGED_EXECUTION
- auto_apply: NO
- production_change: NO

## Executor Rows
- Las Palmas vs Malaga | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_WITH_DATA | success=fixture_detail;statistics;events;lineups;predictions;odds | failed=none | scoring_after=YES_PENDING_NORMAL_GATES
- Castellón vs Almeria | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_WITH_DATA | success=fixture_detail;statistics;events;lineups | failed=predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- HK Kopavogur vs Afturelding | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- Njardvik vs IR Reykjavik | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- Ægir vs Leiknir R. | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- Hvíti riddarinn vs Haukar | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- Kormákur / Hvöt vs Magni | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- JS Kabylie vs CR Belouizdad | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- JS Saoura vs CS Constantine | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- MC Alger vs ASO Chlef | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- Guarulhos vs Paulínia FU | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_WITH_DATA | success=predictions | failed=fixture_detail;statistics;events;lineups;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- Binga vs US Bougouba | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_WITH_DATA | success=fixture_detail;predictions;odds | failed=statistics;events;lineups | scoring_after=YES_PENDING_NORMAL_GATES
- Ituzaingó vs Real Pilar | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_WITH_DATA | success=fixture_detail | failed=statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- Wanderers vs Danubio | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- Sabadell vs Real Madrid II | downstream=DIAGNOSTIC_ONLY_NO_SCORING | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail | scoring_after=NO_DIAGNOSTIC_ONLY
- Plaza Colonia vs Sportivo Huracan | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA
- Puerto Cabello II vs Zamora FC B | downstream=DIAGNOSTIC_ONLY_NO_SCORING | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail | scoring_after=NO_DIAGNOSTIC_ONLY
- Preston Lions vs Melbourne City II | downstream=DIAGNOSTIC_ONLY_NO_SCORING | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail | scoring_after=NO_DIAGNOSTIC_ONLY
- Tatran Všechovice vs Brumov | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Angola vs Mauritania | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Azerbaijan vs Malta | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Benin vs Niger | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Central African Republic vs Togo | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Hungary vs Finland | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Paraguay vs Nicaragua | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Allerheiligen vs FSC Hochegger Dächer | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Bruck an der Mur vs Union RB Weinland Gamlit | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Ilz vs Köflach | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Schladming vs Pachern | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Gurten vs Weiz | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Ried II vs SV Lafnitz | downstream=DIAGNOSTIC_ONLY_NO_SCORING | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail | scoring_after=NO_DIAGNOSTIC_ONLY
- Voitsberg vs Wolfsberger AC II | downstream=DIAGNOSTIC_ONLY_NO_SCORING | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail | scoring_after=NO_DIAGNOSTIC_ONLY
- Oberwart vs Krems / Rehberg | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- TWL Elektra vs SV Horn | downstream=COVERAGE_GATE_ONLY | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events | scoring_after=NO_COVERAGE_GATE_ONLY
- Estrella de Berisso vs Atletico Pilar | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_NO_DATA_OR_ERRORS | success=none | failed=fixture_detail;statistics;events;lineups;predictions;odds | scoring_after=NO_MISSING_REQUIRED_API_DATA

## Guardrails
- This executor may collect API data, but it does not create picks, stake permission, or bypass normal gates.
- SCORING_ALLOWED_WITH_NORMAL_GATES rows still require separate scoring and promotion gates before any market can be considered.
- COVERAGE_GATE_ONLY and DIAGNOSTIC_ONLY_NO_SCORING rows cannot feed picks.
- auto_apply=NO and production_change=NO are hardcoded.
