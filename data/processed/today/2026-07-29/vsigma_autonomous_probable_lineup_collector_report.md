# vSIGMA Autonomous Probable Lineup Collector - 2026-07-29

## Summary
- search_provider: SERPAPI;SERPAPI_SEARCH_FAILED;SERPAPI_ERROR
- rows_seen: 70
- urls_discovered: 52
- rows_extracted: 13
- status_counts: NO_XI_PATTERN=47; IRRELEVANT_FIXTURE_PAGE=2; EXTRACTED=13; FETCH_FAILED=8
- source_counts: sportsmole=33; sports_gambler=29; whoscored=8
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
