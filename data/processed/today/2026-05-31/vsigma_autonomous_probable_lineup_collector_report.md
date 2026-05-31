# vSIGMA Autonomous Probable Lineup Collector - 2026-05-31

## Summary
- search_provider: SERPAPI_SEARCH_FAILED
- rows_seen: 109
- urls_discovered: 128
- rows_extracted: 6
- status_counts: NO_XI_PATTERN=30; IRRELEVANT_FIXTURE_PAGE=44; EXTRACTED=6; FETCH_FAILED=13; NO_DATA=16
- source_counts: sportskeeda=10; sportsmole=42; sports_gambler=28; whoscored=13
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
