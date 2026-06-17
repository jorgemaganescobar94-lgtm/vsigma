# vSIGMA Learning Patterns - 2026-06-17

## Executive Pattern Summary
- generated_at: 2026-06-17T13:34:52+01:00
- patterns detected: 11
- pattern_type_counts: MARKET_RISK_CLUSTER=4, SAMPLE_KEY_CLUSTER=4, WAITING_PRELOCK_CLUSTER=1, UNRESOLVED_DOMINANCE=1, EXPIRED_PRELOCK_CLUSTER=1
- severity_counts: P2=7, P3=3, P1=1

## Top Patterns
- P1 | WAITING_PRELOCK_CLUSTER | WAITING_PRELOCK | n=4 | recommendation=Review execution timing and retry windows if waiting persists.
- P2 | UNRESOLVED_DOMINANCE | UNRESOLVED_RESULTS | n=14 | recommendation=Improve post-results labeling and wait for closed samples before proposing model changes.
- P2 | MARKET_RISK_CLUSTER | UNKNOWN_MARKET::UNKNOWN_RISK | n=9 | recommendation=Monitor market/risk concentration; do not adjust model until losses and sample size clear promotion gates.
- P2 | SAMPLE_KEY_CLUSTER | UNRESOLVED::UNKNOWN_MARKET::UNKNOWN_RISK::NO_SIGNAL | n=8 | recommendation=Keep collecting evidence; repeated sample key can feed improvement proposal only after sufficient closed results.
- P2 | MARKET_RISK_CLUSTER | OVER_1_5::UNKNOWN_RISK | n=7 | recommendation=Monitor market/risk concentration; do not adjust model until losses and sample size clear promotion gates.
- P2 | SAMPLE_KEY_CLUSTER | UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL | n=7 | recommendation=Keep collecting evidence; repeated sample key can feed improvement proposal only after sufficient closed results.
- P2 | MARKET_RISK_CLUSTER | OVER_1_5::FAILURE_MODE_LOW_CONVERSION | n=5 | recommendation=Monitor market/risk concentration; do not adjust model until losses and sample size clear promotion gates.
- P2 | SAMPLE_KEY_CLUSTER | WAITING_PRELOCK::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::WAIT_FOR_POST_RESULTS | n=3 | recommendation=Keep collecting evidence; repeated sample key can feed improvement proposal only after sufficient closed results.
- P3 | MARKET_RISK_CLUSTER | OVER_2_5::UNKNOWN_RISK | n=2 | recommendation=Monitor market/risk concentration; do not adjust model until losses and sample size clear promotion gates.
- P3 | SAMPLE_KEY_CLUSTER | UNRESOLVED::OVER_2_5::UNKNOWN_RISK::NO_SIGNAL | n=2 | recommendation=Keep collecting evidence; repeated sample key can feed improvement proposal only after sufficient closed results.
- P3 | EXPIRED_PRELOCK_CLUSTER | EXPIRED_PRELOCK | n=1 | recommendation=Review AUTO/PRELOCK timing; exclude expired rows from predictive accuracy metrics.

## Learning Use
- Pattern mining is evidence-only.
- Repeated P1/P2 patterns should feed a future improvement proposal engine.
- No model, threshold, calibration, ranking, or market-selection change is applied here.

## Guardrails
- predictive changes applied: NO
- threshold changes applied: NO
- calibration changes applied: NO
- ranking changes applied: NO
- market-selection changes applied: NO
