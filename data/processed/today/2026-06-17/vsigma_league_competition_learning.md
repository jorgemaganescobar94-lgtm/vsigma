# vSIGMA League / Competition Learning - 2026-06-17

## Summary
- competition_rows: 2
- sample_gate_counts: INSUFFICIENT_SAMPLE=2
- data_coverage_status_counts: DIAGNOSTIC_ONLY=1; NO_REAL_SAMPLE=1
- volatility_status_counts: UNKNOWN_VOLATILITY=2
- competition_learning_status_counts: DIAGNOSTIC_ONLY_NO_REAL_SAMPLE=1; HOLD_NO_REAL_SAMPLE=1
- recommended_downstream_use_counts: DIAGNOSTIC_ONLY_NO_SCORING=1; COVERAGE_GATE_ONLY=1
- auto_apply: NO
- production_change: NO

## Competition Rows
- DIAGNOSTIC|DIAGNOSTIC_NO_COMPETITION | real=0/1 | green=0 red=0 void=0 | no_bet=1 | top_family=NO_MARKET | gate=INSUFFICIENT_SAMPLE | volatility=UNKNOWN_VOLATILITY | status=DIAGNOSTIC_ONLY_NO_REAL_SAMPLE | downstream=DIAGNOSTIC_ONLY_NO_SCORING
- UNKNOWN_COUNTRY|UNKNOWN_LEAGUE | real=0/8 | green=0 red=0 void=0 | no_bet=7 | top_family=UNKNOWN_FAMILY | gate=INSUFFICIENT_SAMPLE | volatility=UNKNOWN_VOLATILITY | status=HOLD_NO_REAL_SAMPLE | downstream=COVERAGE_GATE_ONLY

## Guardrails
- This competition learning report is advisory only and never changes league scoring permissions.
- Diagnostic and pending rows do not count as real hit-rate samples.
- SCORING_ALLOWED recommendations are candidates only and require causal/manual review.
- No picks, stakes, production changes, or automatic downstream changes are created here.
