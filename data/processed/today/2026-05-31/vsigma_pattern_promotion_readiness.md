# vSIGMA Pattern Promotion Readiness - 2026-05-31

## Executive Readiness Summary
- generated_at: 2026-05-31T11:00:22+01:00
- executive_status: DATA_QUALITY_BLOCKS_PROMOTION
- patterns_reviewed: 11
- readiness_counts: BLOCKED_BY_DATA_QUALITY=11
- auto_apply: NO
- production_change: NO

## Pattern Readiness Decisions
- #1 | BLOCKED_BY_DATA_QUALITY | key=UNRESOLVED_RESULTS | sample=14 | closed=0 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.
- #2 | BLOCKED_BY_DATA_QUALITY | key=OVER_1_5::UNKNOWN_RISK | sample=8 | closed=0 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.
- #3 | BLOCKED_BY_DATA_QUALITY | key=UNKNOWN_MARKET::UNKNOWN_RISK | sample=8 | closed=0 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.
- #4 | BLOCKED_BY_DATA_QUALITY | key=UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL | sample=8 | closed=0 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.
- #5 | BLOCKED_BY_DATA_QUALITY | key=UNRESOLVED::UNKNOWN_MARKET::UNKNOWN_RISK::NO_SIGNAL | sample=8 | closed=0 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.
- #6 | BLOCKED_BY_DATA_QUALITY | key=OVER_1_5::FAILURE_MODE_LOW_CONVERSION | sample=6 | closed=1 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.
- #7 | BLOCKED_BY_DATA_QUALITY | key=WAITING_PRELOCK | sample=5 | closed=0 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.
- #8 | BLOCKED_BY_DATA_QUALITY | key=WAITING_PRELOCK::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::WAIT_FOR_POST_RESULTS | sample=4 | closed=0 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.
- #9 | BLOCKED_BY_DATA_QUALITY | key=OVER_2_5::UNKNOWN_RISK | sample=2 | closed=0 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.
- #10 | BLOCKED_BY_DATA_QUALITY | key=UNRESOLVED::OVER_2_5::UNKNOWN_RISK::NO_SIGNAL | sample=2 | closed=0 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.
- #11 | BLOCKED_BY_DATA_QUALITY | key=EXPIRED_PRELOCK | sample=1 | closed=0 | next=RESOLVE_DATA_QUALITY_FIRST | reason=P1/P2 data-quality issues block model promotion and threshold/calibration changes.

## Guardrails
- No model changes are applied.
- No threshold/calibration/ranking/market-selection changes are applied.
- PROMOTION_REVIEW_CANDIDATE only means a separate PR/review path can be opened.
- BLOCKED_BY_DATA_QUALITY overrides predictive promotion.