# vSIGMA Raw Candidate Trust Gate - 2026-06-01

## Summary
- rows_reviewed: 7
- trusted_rows: 1
- quarantine_rows: 0
- blocked_rows: 6
- trust_status_counts: REJECTED_SOURCE_BLOCK=6; TRUSTED_RAW_SOURCE=1
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; rejected rows remain diagnostic only.
- auto_apply: NO
- production_change: NO

## Rows
- Ponte Preta vs Botafogo SP | league=Serie B | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data\processed\matches_league_filtered.csv
- Leones del Norte vs Macara | league=Liga Pro | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data\processed\matches_league_rejected.csv
- ASKO vs Derby Academie | league=Première Division | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data\processed\matches_league_rejected.csv
- Binga vs US Bougouba | league=Première Division | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data\processed\matches_league_rejected.csv
- Carolina Ascent II W vs North Carolina Fusion W | league=USL W League | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data\processed\matches_league_rejected.csv
- Corinthians U17 vs Sao Paulo U17 | league=Brasileiro U17 | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data\processed\matches_league_rejected.csv
- Santa Clara U23 vs Gil Vicente U23 | league=Taça Revelação U23 | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data\processed\matches_league_rejected.csv

## Guardrails
- Trust gate is defensive and can only restrict downstream use.
- Rejected source rows cannot feed scoring without explicit future whitelist.
- Youth/women/reserve/academy rows remain quarantine-only unless explicitly whitelisted.
- No bets, stakes, secrets, API calls, or safety gates are changed.
