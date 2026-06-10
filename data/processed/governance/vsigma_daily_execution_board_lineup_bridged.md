# vSIGMA Daily Execution Board - 2026-06-10 (Forced API Lineup Bridged Copy)

## Summary
- rows_on_board: 2
- bridge_status_counts: LINEUPS_CONFIRMED_BY_FORCED_API=2
- bridge_action_counts: CLEAR_LINEUPS_INACTIVE_WARNING_KEEP_EXECUTION_LOCK=2
- auto_apply: NO
- production_change: NO

## Board Rows
- #1 | LIVE_ONLY | Malaga vs Las Palmas | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | permission=NO_PREMATCH | conf=MEDIUM | warnings=API_EARLY_LOW_SUPPORT; LINEUPS_CONFIRMED_BY_FORCED_API | prelock=price remains above minimum; market not over-compressed; lineups confirmed; lineups confirmed by forced API fixture-id refresh | note=No prematch serious stake; require live tempo and chance confirmation.; api_gate=EARLY_WATCH_MORE_DATA_REQUIRED; coverage_score=80.0; missing=lineup_coverage=CONFIRMED_BY_FORCED_API_LINEUPS; injuries_coverage=NONE
- #2 | NO_BET | Cape Town City vs Magesi | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | permission=NO | conf=LOW | warnings=PARTIAL_RECENT_STATS; SHOT_SAMPLE_WEAK; CORNER_SAMPLE_WEAK; CARD_SAMPLE_WEAK; LINEUPS_CONFIRMED_BY_FORCED_API | prelock=none; lineups confirmed by forced API fixture-id refresh | note=No execution permission.; api_gate=LOW_COVERAGE_NO_BET; coverage_score=20.0; missing=recent_stats_coverage=NONE; lineup_coverage=CONFIRMED_BY_FORCED_API_LINEUPS; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- This is a bridged copy, not automatic execution permission.
- Forced API lineups can clear stale lineup warnings but cannot create picks or stake.
- Any future promotion must be handled by a separate prelock resolver with explicit governance.
