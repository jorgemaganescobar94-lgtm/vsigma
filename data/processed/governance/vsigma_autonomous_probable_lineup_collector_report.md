# vSIGMA Autonomous Probable Lineup Collector - 2026-05-29

## Summary
- search_provider: SERPAPI;SERPAPI_ERROR
- rows_seen: 15
- urls_discovered: 21
- rows_extracted: 5
- status_counts: EXTRACTED=5; NO_XI_PATTERN=7; FETCH_FAILED=3
- source_counts: sportsmole=12; whoscored=3
- max_search_queries_per_fixture: 5
- auto_apply: NO
- production_change: NO

## Guardrails
- Uses only search API keys if configured; no search-page scraping.
- Searches approved probable-XI domains separately and deduplicates URLs.
- Search/API/fetch failures degrade to report rows instead of failing workflow.
- Fetches public source URLs only; does not bypass paywalls, logins, or blocks.
- Conservative extraction: blank if pattern confidence is insufficient.
- Output still passes through registry-weighted consensus.
