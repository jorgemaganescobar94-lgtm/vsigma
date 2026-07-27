# vSIGMA Raw Candidate Trust Gate - 2026-07-27

## Summary
- rows_reviewed: 4
- trusted_rows: 4
- quarantine_rows: 0
- blocked_rows: 0
- trust_status_counts: TRUSTED_RAW_SOURCE=4
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.
- auto_apply: NO
- production_change: NO

## Rows
- IF Brommapojkarna vs Hammarby FF | league=Allsvenskan | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- KFUM Oslo vs Molde | league=Eliteserien | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Remo vs Vitoria | league=Serie A | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Aalesund vs Viking | league=Eliteserien | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv

## Guardrails
- Trust gate is defensive and can only restrict downstream use.
- Rejected source rows cannot feed scoring without explicit future whitelist.
- Youth/women/reserve/academy rows remain quarantine-only unless explicitly whitelisted.
- No bets, stakes, secrets, API calls, or safety gates are changed.
