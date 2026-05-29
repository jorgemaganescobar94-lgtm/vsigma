# vSIGMA Autonomous Probable Lineup Collector - 2026-05-29

## Summary
- search_provider: SERPAPI
- rows_seen: 3
- urls_discovered: 1
- rows_extracted: 1
- status_counts: EXTRACTED=1; NO_XI_PATTERN=1; NO_DATA=1
- source_counts: sportsmole=2
- auto_apply: NO
- production_change: NO

## Guardrails
- Uses only search API keys if configured; no search-page scraping.
- Search/API/fetch failures degrade to report rows instead of failing workflow.
- Fetches public source URLs only; does not bypass paywalls, logins, or blocks.
- Conservative extraction: blank if pattern confidence is insufficient.
- Output still passes through registry-weighted consensus.
