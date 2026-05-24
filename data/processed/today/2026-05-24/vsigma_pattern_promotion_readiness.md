# vSIGMA Pattern Promotion Readiness - 2026-05-24

## Executive Readiness Summary
- generated_at: 2026-05-24T10:11:21+01:00
- executive_status: SHADOW_EXPERIMENT_REQUIRED
- patterns_reviewed: 13
- readiness_counts: DATA_QUALITY_REVIEW=7; MONITOR_MORE_EVIDENCE=2; MONITOR_ONLY=2; SHADOW_REQUIRED=1; BLOCKED_BY_SAMPLE_SIZE=1
- auto_apply: NO
- production_change: NO

## Pattern Readiness Decisions
- #1 | SHADOW_REQUIRED | key=WAITING_PRELOCK::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::WAIT_FOR_POST_RESULTS | sample=4 | closed=0 | next=CREATE_OR_CONTINUE_SHADOW_ONLY | reason=Pattern is repeated enough to create or continue shadow-only experiment.
- #2 | BLOCKED_BY_SAMPLE_SIZE | key=OVER_1_5::FAILURE_MODE_LOW_CONVERSION | sample=8 | closed=2 | next=CONTINUE_SHADOW_FORWARD_TEST | reason=Only 2 closed samples; minimum review sample is 30.
- #3 | DATA_QUALITY_REVIEW | key=UNRESOLVED_RESULTS | sample=16 | closed=0 | next=CLEAN_EVIDENCE | reason=Pattern is data-quality related and should not become predictive change.
- #4 | DATA_QUALITY_REVIEW | key=OVER_1_5::UNKNOWN_RISK | sample=8 | closed=0 | next=CLEAN_EVIDENCE | reason=Pattern is data-quality related and should not become predictive change.
- #5 | DATA_QUALITY_REVIEW | key=UNKNOWN_MARKET::UNKNOWN_RISK | sample=8 | closed=0 | next=CLEAN_EVIDENCE | reason=Pattern is data-quality related and should not become predictive change.
- #6 | DATA_QUALITY_REVIEW | key=UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL | sample=8 | closed=0 | next=CLEAN_EVIDENCE | reason=Pattern is data-quality related and should not become predictive change.
- #7 | DATA_QUALITY_REVIEW | key=UNRESOLVED::UNKNOWN_MARKET::UNKNOWN_RISK::NO_SIGNAL | sample=8 | closed=0 | next=CLEAN_EVIDENCE | reason=Pattern is data-quality related and should not become predictive change.
- #8 | DATA_QUALITY_REVIEW | key=OVER_2_5::UNKNOWN_RISK | sample=3 | closed=0 | next=CLEAN_EVIDENCE | reason=Pattern is data-quality related and should not become predictive change.
- #9 | DATA_QUALITY_REVIEW | key=UNRESOLVED::OVER_2_5::UNKNOWN_RISK::NO_SIGNAL | sample=3 | closed=0 | next=CLEAN_EVIDENCE | reason=Pattern is data-quality related and should not become predictive change.
- #10 | MONITOR_MORE_EVIDENCE | key=OVER_2_5::FAILURE_MODE_LOW_CONVERSION | sample=2 | closed=0 | next=COLLECT_MORE_SAMPLES | reason=Model-shadow proposal exists but evidence is not promotion-ready.
- #11 | MONITOR_MORE_EVIDENCE | key=WAITING_PRELOCK::OVER_2_5::FAILURE_MODE_LOW_CONVERSION::WAIT_FOR_POST_RESULTS | sample=2 | closed=0 | next=COLLECT_MORE_SAMPLES | reason=Model-shadow proposal exists but evidence is not promotion-ready.
- #12 | MONITOR_ONLY | key=WAITING_PRELOCK | sample=6 | closed=0 | next=KEEP_MONITORING | reason=Proposal does not clear shadow or promotion gates.
- #13 | MONITOR_ONLY | key=EXPIRED_PRELOCK | sample=1 | closed=0 | next=KEEP_MONITORING | reason=Proposal does not clear shadow or promotion gates.

## Guardrails
- No model changes are applied.
- No threshold/calibration/ranking/market-selection changes are applied.
- PROMOTION_REVIEW_CANDIDATE only means a separate PR/review path can be opened.
- BLOCKED_BY_DATA_QUALITY overrides predictive promotion.