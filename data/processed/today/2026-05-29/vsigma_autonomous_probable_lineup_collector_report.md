# vSIGMA Autonomous Probable Lineup Collector - 2026-05-29

## Summary
- search_provider: NO_SEARCH_KEY
- rows_seen: 20
- urls_discovered: 0
- rows_extracted: 0
- status_counts: NO_DATA=20
- source_counts: none
- auto_apply: NO
- production_change: NO

## Guardrails
- Uses only search API keys if configured; no search-page scraping.
- Fetches public source URLs only; does not bypass paywalls, logins, or blocks.
- Conservative extraction: blank if pattern confidence is insufficient.
- Output still passes through registry-weighted consensus.
