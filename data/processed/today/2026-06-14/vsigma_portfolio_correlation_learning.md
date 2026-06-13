# vSIGMA Portfolio / Correlation Learning - 2026-06-14

## Summary
- cluster_rows: 12
- portfolio_correlation_status_counts: DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING=12
- correlation_risk_label_counts: NONE=12
- cluster_type_counts: CONFIDENCE_BUCKET=1; COUNTRY=1; DAILY_PORTFOLIO=1; DECISION_BUCKET=1; ERROR_FAMILY=1; GOAL_TIMING_PROFILE=1; LEAGUE=1; LINEUP_SHOCK_STATUS=1; MARKET_FAMILY=1; NO_BET_QUALITY=1; QUALITY_CLASS=1; SCORELINE_BUCKET=1
- auto_apply: NO
- production_change: NO

## Cluster Rows
- CONFIDENCE_BUCKET:NO_CONFIDENCE | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- COUNTRY:DIAGNOSTIC | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- DAILY_PORTFOLIO:ALL | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- DECISION_BUCKET:DIAGNOSTIC_ONLY | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- ERROR_FAMILY:UNKNOWN_ERROR | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- GOAL_TIMING_PROFILE:NO_GOAL_TIMING_PROFILE | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- LEAGUE:DIAGNOSTIC|DIAGNOSTIC_NO_COMPETITION | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- LINEUP_SHOCK_STATUS:NO_LINEUP_STATUS | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- MARKET_FAMILY:UNKNOWN_FAMILY | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- NO_BET_QUALITY:NO_NO_BET_LABEL | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- QUALITY_CLASS:UNKNOWN_QUALITY | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.
- SCORELINE_BUCKET:NO_SCORELINE_BUCKET | rows=1 real=0 | green=0 red=0 no_bet=0 | status=DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING | risk=NONE | action=Diagnostic-only cluster; do not learn portfolio correlation.

## Guardrails
- This portfolio correlation report is advisory only and never changes picks, stake, gates, or weights.
- Correlation labels are review candidates, not automatic truth.
- Diagnostic and single-row clusters must not train the model.
- No automatic portfolio cap, market-family change, or production change is created here.
