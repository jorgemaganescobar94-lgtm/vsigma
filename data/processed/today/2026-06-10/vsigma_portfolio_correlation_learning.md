# vSIGMA Portfolio / Correlation Learning - 2026-06-10

## Summary
- cluster_rows: 18
- portfolio_correlation_status_counts: SINGLETON_NO_CORRELATION_SAMPLE=12; NO_BET_CONCENTRATION_REVIEW=6
- correlation_risk_label_counts: LOW=12; MEDIUM=6
- cluster_type_counts: DECISION_BUCKET=2; ERROR_FAMILY=2; MARKET_FAMILY=2; NO_BET_QUALITY=2; QUALITY_CLASS=2; SCORELINE_BUCKET=2; CONFIDENCE_BUCKET=1; COUNTRY=1; DAILY_PORTFOLIO=1; GOAL_TIMING_PROFILE=1; LEAGUE=1; LINEUP_SHOCK_STATUS=1
- auto_apply: NO
- production_change: NO

## Cluster Rows
- CONFIDENCE_BUCKET:NO_CONFIDENCE | rows=2 real=0 | green=0 red=0 no_bet=2 | status=NO_BET_CONCENTRATION_REVIEW | risk=MEDIUM | action=Multiple No Bet rows share this cluster; review whether the system is overblocking.
- COUNTRY:UNKNOWN_COUNTRY | rows=2 real=0 | green=0 red=0 no_bet=2 | status=NO_BET_CONCENTRATION_REVIEW | risk=MEDIUM | action=Multiple No Bet rows share this cluster; review whether the system is overblocking.
- DAILY_PORTFOLIO:ALL | rows=2 real=0 | green=0 red=0 no_bet=2 | status=NO_BET_CONCENTRATION_REVIEW | risk=MEDIUM | action=Multiple No Bet rows share this cluster; review whether the system is overblocking.
- DECISION_BUCKET:LIVE_ONLY | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- DECISION_BUCKET:NO_BET | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- ERROR_FAMILY:NO_BET_REVIEW | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- ERROR_FAMILY:PENDING | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- GOAL_TIMING_PROFILE:GOAL_TIMING_DATA_MISSING | rows=2 real=0 | green=0 red=0 no_bet=2 | status=NO_BET_CONCENTRATION_REVIEW | risk=MEDIUM | action=Multiple No Bet rows share this cluster; review whether the system is overblocking.
- LEAGUE:UNKNOWN_COUNTRY|UNKNOWN_LEAGUE | rows=2 real=0 | green=0 red=0 no_bet=2 | status=NO_BET_CONCENTRATION_REVIEW | risk=MEDIUM | action=Multiple No Bet rows share this cluster; review whether the system is overblocking.
- LINEUP_SHOCK_STATUS:LINEUP_DATA_MISSING | rows=2 real=0 | green=0 red=0 no_bet=2 | status=NO_BET_CONCENTRATION_REVIEW | risk=MEDIUM | action=Multiple No Bet rows share this cluster; review whether the system is overblocking.
- MARKET_FAMILY:TOTAL_GOALS | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- MARKET_FAMILY:UNKNOWN_FAMILY | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- NO_BET_QUALITY:NOT_A_NO_BET_ROW | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- NO_BET_QUALITY:NO_BET_TOO_CONSERVATIVE_CANDIDATE | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- QUALITY_CLASS:NO_BET_CAUSAL_REVIEW_REQUIRED | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- QUALITY_CLASS:PENDING_FINAL_ACTUALS | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- SCORELINE_BUCKET:DRAW_1_1 | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.
- SCORELINE_BUCKET:NO_SCORELINE | rows=1 real=0 | green=0 red=0 no_bet=1 | status=SINGLETON_NO_CORRELATION_SAMPLE | risk=LOW | action=Only one row in cluster; no portfolio correlation can be inferred.

## Guardrails
- This portfolio correlation report is advisory only and never changes picks, stake, gates, or weights.
- Correlation labels are review candidates, not automatic truth.
- Diagnostic and single-row clusters must not train the model.
- No automatic portfolio cap, market-family change, or production change is created here.
