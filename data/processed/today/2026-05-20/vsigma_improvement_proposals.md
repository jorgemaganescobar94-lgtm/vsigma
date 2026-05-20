# vSIGMA Improvement Proposals - 2026-05-20

## Executive Proposal Summary
- generated_at: 2026-05-20T18:50:50+01:00
- proposals generated: 11
- proposal_type_counts: MODEL_SHADOW_PROPOSAL=8; OPERATIONAL_PROPOSAL=2; DATA_QUALITY_PROPOSAL=1
- proposal_status_counts: SHADOW_CANDIDATE_REQUIRED=6; MONITOR_ONLY=3; PROPOSAL_ONLY=2
- priority_counts: P1=7; P3=3; P2=1

## Top Proposals
- P1 | SHADOW_CANDIDATE_REQUIRED | MODEL_SHADOW_PROPOSAL | MARKET_RISK_CLUSTER | n=7 | auto_apply=NO | action=Create a shadow-only candidate for pattern OVER_1_5::UNKNOWN_RISK; do not change production until backtest/forward-test promotion gates pass.
- P1 | SHADOW_CANDIDATE_REQUIRED | MODEL_SHADOW_PROPOSAL | MARKET_RISK_CLUSTER | n=7 | auto_apply=NO | action=Create a shadow-only candidate for pattern UNKNOWN_MARKET::UNKNOWN_RISK; do not change production until backtest/forward-test promotion gates pass.
- P1 | SHADOW_CANDIDATE_REQUIRED | MODEL_SHADOW_PROPOSAL | SAMPLE_KEY_CLUSTER | n=7 | auto_apply=NO | action=Create a shadow-only candidate for pattern UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL; do not change production until backtest/forward-test promotion gates pass.
- P1 | SHADOW_CANDIDATE_REQUIRED | MODEL_SHADOW_PROPOSAL | SAMPLE_KEY_CLUSTER | n=7 | auto_apply=NO | action=Create a shadow-only candidate for pattern UNRESOLVED::UNKNOWN_MARKET::UNKNOWN_RISK::NO_SIGNAL; do not change production until backtest/forward-test promotion gates pass.
- P1 | SHADOW_CANDIDATE_REQUIRED | MODEL_SHADOW_PROPOSAL | MARKET_RISK_CLUSTER | n=5 | auto_apply=NO | action=Create a shadow-only candidate for pattern OVER_1_5::FAILURE_MODE_LOW_CONVERSION; do not change production until backtest/forward-test promotion gates pass.
- P1 | SHADOW_CANDIDATE_REQUIRED | MODEL_SHADOW_PROPOSAL | SAMPLE_KEY_CLUSTER | n=3 | auto_apply=NO | action=Create a shadow-only candidate for pattern WAITING_PRELOCK::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::WAIT_FOR_POST_RESULTS; do not change production until backtest/forward-test promotion gates pass.
- P1 | PROPOSAL_ONLY | OPERATIONAL_PROPOSAL | WAITING_PRELOCK_CLUSTER | n=4 | auto_apply=NO | action=Review AUTO/PRELOCK schedule, retry windows, and whether candidates remain waiting too close to kickoff.
- P2 | PROPOSAL_ONLY | DATA_QUALITY_PROPOSAL | UNRESOLVED_DOMINANCE | n=12 | auto_apply=NO | action=Improve post-results labeling coverage before approving model changes.
- P3 | MONITOR_ONLY | MODEL_SHADOW_PROPOSAL | MARKET_RISK_CLUSTER | n=2 | auto_apply=NO | action=Create a shadow-only candidate for pattern OVER_2_5::UNKNOWN_RISK; do not change production until backtest/forward-test promotion gates pass.
- P3 | MONITOR_ONLY | MODEL_SHADOW_PROPOSAL | SAMPLE_KEY_CLUSTER | n=2 | auto_apply=NO | action=Create a shadow-only candidate for pattern UNRESOLVED::OVER_2_5::UNKNOWN_RISK::NO_SIGNAL; do not change production until backtest/forward-test promotion gates pass.
- P3 | MONITOR_ONLY | OPERATIONAL_PROPOSAL | EXPIRED_PRELOCK_CLUSTER | n=1 | auto_apply=NO | action=Review execution timing and exclude expired rows from predictive hit-rate metrics.

## Guardrails
- auto_apply: NO for every proposal
- predictive changes applied: NO
- threshold changes applied: NO
- calibration changes applied: NO
- ranking changes applied: NO
- market-selection changes applied: NO

## Next Engine
- OPERATIONAL_PROPOSAL rows feed operator/workflow review.
- DATA_QUALITY_PROPOSAL rows feed data coverage and post-result labeling improvement.
- MODEL_SHADOW_PROPOSAL rows feed the future shadow experiment engine only.
