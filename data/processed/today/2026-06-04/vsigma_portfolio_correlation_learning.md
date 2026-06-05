# vSIGMA Portfolio / Correlation Learning - 2026-06-04

## Summary
- cluster_rows: 11
- portfolio_correlation_status_counts: DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING=11
- correlation_risk_label_counts: NONE=11
- cluster_type_counts: CONFIDENCE_BUCKET=1; COUNTRY=1; DAILY_PORTFOLIO=1; DECISION_BUCKET=1; GOAL_TIMING_PROFILE=1; LEAGUE=1; LINEUP_SHOCK_STATUS=1; MARKET_FAMILY=1; NO_BET_QUALITY=1; QUALITY_CLASS=1; SCORELINE_BUCKET=1
- auto_apply: NO
- production_change: NO

## Cluster Rows
- CONFIDENCE_BUCKET:NO_CONFIDENCE | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- COUNTRY:UNKNOWN_COUNTRY | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- DAILY_PORTFOLIO:ALL | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- DECISION_BUCKET:DIAGNOSTIC_ONLY | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- GOAL_TIMING_PROFILE:DIAGNOSTIC_NO_GOAL_TIMING_LEARNING | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- LEAGUE:UNKNOWN_COUNTRY|UNKNOWN_LEAGUE | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- LINEUP_SHOCK_STATUS:DIAGNOSTIC_NO_LINEUP_LEARNING | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- MARKET_FAMILY:NO_MARKET | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- NO_BET_QUALITY:DIAGNOSTIC_NOT_REAL_FIXTURE_NO_BET | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- QUALITY_CLASS:DIAGNOSTIC_NO_LEARNING | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- SCORELINE_BUCKET:NO_SCORELINE | rows=1 real=0 | green=0 red=0 no_bet=1 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.

## Guardrails
- This portfolio correlation report is advisory only and never changes picks, stake, gates, or weights.
- Correlation labels are review candidates, not automatic truth.
- Diagnostic and single-row clusters must not train the model.
- No automatic portfolio cap, market-family change, or production change is created here.
