# vSIGMA Autonomous Probable Lineup Collector - 2026-07-04

## Summary
- search_provider: SERPAPI_SEARCH_FAILED
- rows_seen: 116
- urls_discovered: 82
- rows_extracted: 1
- status_counts: EXTRACTED=1; NO_XI_PATTERN=63; IRRELEVANT_FIXTURE_PAGE=39; FETCH_FAILED=8; NO_DATA=5
- source_counts: sportsmole=35; sports_gambler=68; whoscored=8
- max_search_queries_per_fixture: 8
- auto_apply: NO
- production_change: NO

## Guardrails
- Uses only search API keys if configured; no search-page scraping.
- Searches approved probable-XI domains separately and deduplicates URLs.
- Fixture-date relevance filter blocks historical or related articles before extraction.
- SportsMole uses section-aware parsing and does not fall back to narrative regex.
- Source expansion is weighted by registry; new sources are supporting only, never official.
- Search/API/fetch failures degrade to report rows instead of failing workflow.
- Fetches public source URLs only; does not bypass paywalls, logins, or blocks.
- Conservative extraction: blank if pattern confidence is insufficient.
- Output still passes through quarantine and registry-weighted consensus.
