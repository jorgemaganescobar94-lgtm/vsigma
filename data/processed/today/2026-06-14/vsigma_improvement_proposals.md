# vSIGMA Improvement Proposals - 2026-06-14

## Executive Proposal Summary
- generated_at: 2026-06-14T12:12:34+01:00
- proposals generated: 13
- proposal_type_counts: DATA_QUALITY_PROPOSAL=7; MODEL_SHADOW_PROPOSAL=4; OPERATIONAL_PROPOSAL=2
- proposal_status_counts: PROPOSAL_ONLY=8; MONITOR_ONLY=3; SHADOW_CANDIDATE_REQUIRED=2
- priority_counts: P2=5; P3=5; P1=3

## Top Proposals
- P1 | SHADOW_CANDIDATE_REQUIRED | MODEL_SHADOW_PROPOSAL | MARKET_RISK_CLUSTER | n=5 | auto_apply=NO | action=Create a shadow-only candidate for pattern OVER_1_5::FAILURE_MODE_LOW_CONVERSION; do not change production until backtest/forward-test promotion gates pass.
- P1 | SHADOW_CANDIDATE_REQUIRED | MODEL_SHADOW_PROPOSAL | SAMPLE_KEY_CLUSTER | n=3 | auto_apply=NO | action=Create a shadow-only candidate for pattern WAITING_PRELOCK::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::WAIT_FOR_POST_RESULTS; do not change production until backtest/forward-test promotion gates pass.
- P1 | PROPOSAL_ONLY | OPERATIONAL_PROPOSAL | WAITING_PRELOCK_CLUSTER | n=5 | auto_apply=NO | action=Review AUTO/PRELOCK schedule, retry windows, and whether candidates remain waiting too close to kickoff.
- P2 | PROPOSAL_ONLY | DATA_QUALITY_PROPOSAL | UNRESOLVED_DOMINANCE | n=14 | auto_apply=NO | action=Resolve UNKNOWN/UNRESOLVED/NO_SIGNAL evidence quality before creating any model shadow candidate.
- P2 | PROPOSAL_ONLY | DATA_QUALITY_PROPOSAL | MARKET_RISK_CLUSTER | n=8 | auto_apply=NO | action=Resolve UNKNOWN/UNRESOLVED/NO_SIGNAL evidence quality before creating any model shadow candidate.
- P2 | PROPOSAL_ONLY | DATA_QUALITY_PROPOSAL | MARKET_RISK_CLUSTER | n=8 | auto_apply=NO | action=Resolve UNKNOWN/UNRESOLVED/NO_SIGNAL evidence quality before creating any model shadow candidate.
- P2 | PROPOSAL_ONLY | DATA_QUALITY_PROPOSAL | SAMPLE_KEY_CLUSTER | n=8 | auto_apply=NO | action=Resolve UNKNOWN/UNRESOLVED/NO_SIGNAL evidence quality before creating any model shadow candidate.
- P2 | PROPOSAL_ONLY | DATA_QUALITY_PROPOSAL | SAMPLE_KEY_CLUSTER | n=8 | auto_apply=NO | action=Resolve UNKNOWN/UNRESOLVED/NO_SIGNAL evidence quality before creating any model shadow candidate.
- P3 | PROPOSAL_ONLY | DATA_QUALITY_PROPOSAL | MARKET_RISK_CLUSTER | n=2 | auto_apply=NO | action=Resolve UNKNOWN/UNRESOLVED/NO_SIGNAL evidence quality before creating any model shadow candidate.
- P3 | PROPOSAL_ONLY | DATA_QUALITY_PROPOSAL | SAMPLE_KEY_CLUSTER | n=2 | auto_apply=NO | action=Resolve UNKNOWN/UNRESOLVED/NO_SIGNAL evidence quality before creating any model shadow candidate.
- P3 | MONITOR_ONLY | MODEL_SHADOW_PROPOSAL | MARKET_RISK_CLUSTER | n=2 | auto_apply=NO | action=Create a shadow-only candidate for pattern OVER_2_5::FAILURE_MODE_LOW_CONVERSION; do not change production until backtest/forward-test promotion gates pass.
- P3 | MONITOR_ONLY | MODEL_SHADOW_PROPOSAL | SAMPLE_KEY_CLUSTER | n=2 | auto_apply=NO | action=Create a shadow-only candidate for pattern WAITING_PRELOCK::OVER_2_5::FAILURE_MODE_LOW_CONVERSION::WAIT_FOR_POST_RESULTS; do not change production until backtest/forward-test promotion gates pass.
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
