# vSIGMA Alert - 2026-06-18

System status: **UNKNOWN**
Alert required: **YES**
Notify required: **YES**
Alert hash: `bf3443b407dd3cd2b5551c340caba8b9aceb0c2ffdaaf224c889f9a1a42c16ed`

## Signals
- - memory_decision_counts: CALIBRATION_STABLE=4; MIXED_CALIBRATION_REVIEW=1; PATCH_CANDIDATE_REVIEW=1
- - total_goals | days=5 | rows=27 | hit_rate=0.371 | bias=OVER_ESTIMATE | decision=PATCH_CANDIDATE_REVIEW | patch=YES_REVIEW_ONLY | next=Review lowering total_goals projection/range for matching profiles; do not auto-apply.

## Health Snapshot
```
missing health report
```

## Live Trigger Snapshot
```
# vSIGMA Live Trigger Validator - 2026-06-18

## Summary
- rows_validated: 0
- window_counts: none
- live_trigger_counts: none
- auto_apply: NO
- production_change: NO

## Rows
- none. No live/prelock candidates found.

## Guardrails
- Diagnostic only; no execution.
- Manual review required for any action.

```

## Guardrails
- This issue is an alert only.
- Manual review is required before any action.
