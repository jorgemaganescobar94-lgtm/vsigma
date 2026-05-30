# vSIGMA Autonomous Probable Lineup Collector - 2026-05-29

## Summary
- search_provider: SERPAPI;SERPAPI_ERROR
- rows_seen: 18
- urls_discovered: 35
- rows_extracted: 5
- status_counts: EXTRACTED=5; NO_XI_PATTERN=9; FETCH_FAILED=4
- source_counts: sportsmole=12; gffn=2; whoscored=4
- max_search_queries_per_fixture: 8
- auto_apply: NO
- production_change: NO

## Guardrails
- Uses only search API keys if configured; no search-page scraping.
- Searches approved probable-XI domains separately and deduplicates URLs.
- Source expansion is weighted by registry; new sources are supporting only, never official.
- Search/API/fetch failures degrade to report rows instead of failing workflow.
- Fetches public source URLs only; does not bypass paywalls, logins, or blocks.
- Conservative extraction: blank if pattern confidence is insufficient.
- Output still passes through registry-weighted consensus.
