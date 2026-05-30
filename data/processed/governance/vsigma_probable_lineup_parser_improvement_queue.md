# vSIGMA Probable XI Parser Improvement Queue - 2026-05-29

## Queue
- HIGH | sportsmole | TEXT_BOUNDARY_FAILURE | evidence=1 | patch=Tighten regex boundaries and reject narrative fragments before player splitting. | promotion=Promote after narrative-fragment quarantine falls below 5% of extracted rows for 3 runs.
- HIGH | sportsmole | PARSER_EXTRACTION_FAILURE | evidence=4 | patch=Keep rows quarantined; improve page section targeting and do not downgrade source reliability from these rows. | promotion=Promote parser patch only after extracted XI reaches >=8/11 official overlap on at least 3 fixtures.

## Guardrails
- Queue is advisory only.
- No parser patch is promoted automatically from a single bad run.
- Source reliability is protected from parser failures.
