# vSIGMA Self-Improvement Governor - 2026-06-10

## Executive Governor Summary
- generated_at: 2026-06-10T12:59:08+01:00
- executive_status: DATA_QUALITY_BLOCKS_MODEL_CHANGE
- decisions: 13
- decision_counts: DATA_QUALITY_FIRST=7; OPERATIONAL_REVIEW_REQUIRED=2; SHADOW_FACTORY_ALLOWED=2; SHADOW_TRACKING_ACTIVE=1; COLLECT_MORE_SAMPLES=1
- source_counts: IMPROVEMENT_PROPOSAL=11; SHADOW_CANDIDATE=1; PROMOTION_GATE=1
- auto_apply: NO
- production_change: NO

## Top Governor Decisions
- P2 | DATA_QUALITY_FIRST | IMPROVEMENT_PROPOSAL | sample=14 | shadow_allowed=NO | promotion_pr_allowed=NO | next=OPEN_DATA_QUALITY_REVIEW | reason=Evidence quality gap must be resolved before any model/shadow promotion path.
- P2 | DATA_QUALITY_FIRST | IMPROVEMENT_PROPOSAL | sample=8 | shadow_allowed=NO | promotion_pr_allowed=NO | next=OPEN_DATA_QUALITY_REVIEW | reason=Evidence quality gap must be resolved before any model/shadow promotion path.
- P2 | DATA_QUALITY_FIRST | IMPROVEMENT_PROPOSAL | sample=8 | shadow_allowed=NO | promotion_pr_allowed=NO | next=OPEN_DATA_QUALITY_REVIEW | reason=Evidence quality gap must be resolved before any model/shadow promotion path.
- P2 | DATA_QUALITY_FIRST | IMPROVEMENT_PROPOSAL | sample=7 | shadow_allowed=NO | promotion_pr_allowed=NO | next=OPEN_DATA_QUALITY_REVIEW | reason=Evidence quality gap must be resolved before any model/shadow promotion path.
- P2 | DATA_QUALITY_FIRST | IMPROVEMENT_PROPOSAL | sample=7 | shadow_allowed=NO | promotion_pr_allowed=NO | next=OPEN_DATA_QUALITY_REVIEW | reason=Evidence quality gap must be resolved before any model/shadow promotion path.
- P3 | DATA_QUALITY_FIRST | IMPROVEMENT_PROPOSAL | sample=2 | shadow_allowed=NO | promotion_pr_allowed=NO | next=OPEN_DATA_QUALITY_REVIEW | reason=Evidence quality gap must be resolved before any model/shadow promotion path.
- P3 | DATA_QUALITY_FIRST | IMPROVEMENT_PROPOSAL | sample=2 | shadow_allowed=NO | promotion_pr_allowed=NO | next=OPEN_DATA_QUALITY_REVIEW | reason=Evidence quality gap must be resolved before any model/shadow promotion path.
- P1 | OPERATIONAL_REVIEW_REQUIRED | IMPROVEMENT_PROPOSAL | sample=5 | shadow_allowed=NO | promotion_pr_allowed=NO | next=OPEN_OPERATIONAL_REVIEW | reason=Operational timing/freshness issue affects execution quality, not production model logic.
- P3 | OPERATIONAL_REVIEW_REQUIRED | IMPROVEMENT_PROPOSAL | sample=1 | shadow_allowed=NO | promotion_pr_allowed=NO | next=OPEN_OPERATIONAL_REVIEW | reason=Operational timing/freshness issue affects execution quality, not production model logic.
- P1 | SHADOW_FACTORY_ALLOWED | IMPROVEMENT_PROPOSAL | sample=6 | shadow_allowed=YES | promotion_pr_allowed=NO | next=CREATE_OR_CONTINUE_SHADOW_CANDIDATE | reason=Pattern has enough proposal evidence to create/continue a shadow-only candidate, not to modify production.
- P1 | SHADOW_FACTORY_ALLOWED | IMPROVEMENT_PROPOSAL | sample=4 | shadow_allowed=YES | promotion_pr_allowed=NO | next=CREATE_OR_CONTINUE_SHADOW_CANDIDATE | reason=Pattern has enough proposal evidence to create/continue a shadow-only candidate, not to modify production.
- P2 | SHADOW_TRACKING_ACTIVE | SHADOW_CANDIDATE | sample=1 | shadow_allowed=YES | promotion_pr_allowed=NO | next=TRACK_SHADOW_OUTCOME | reason=Shadow candidate may be monitored against baseline, but production remains unchanged.
- P2 | COLLECT_MORE_SAMPLES | PROMOTION_GATE | sample=1 | shadow_allowed=YES | promotion_pr_allowed=NO | next=CONTINUE_FORWARD_TEST | reason=Promotion evidence is too small for production consideration.

## Hard Guardrails
- Production model changes applied: NO
- Prediction formulas changed: NO
- Thresholds changed: NO
- Calibration changed: NO
- Ranking changed: NO
- Market-selection changed: NO
- Auto-apply allowed: NO
- Promotion requires a separate reviewed PR even when promotion_pr_allowed=YES_REVIEW_ONLY.

## Interpretation
- DATA_QUALITY_FIRST blocks model changes until evidence quality improves.
- SHADOW_FACTORY_ALLOWED means experiment only; official picks remain unchanged.
- HUMAN_PROMOTION_REVIEW_REQUIRED means open a separate PR/review path; no automatic activation.
