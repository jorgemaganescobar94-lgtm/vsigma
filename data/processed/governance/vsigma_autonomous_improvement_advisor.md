# vSIGMA Autonomous Improvement Advisor - 2026-06-16

## Summary
- top_priority: HIGH
- rows: 7
- issue_required: YES
- auto_apply: NO
- production_change: NO

## Recommendations
- HIGH | calibration/total_corners | PATCH_CANDIDATE_REVIEW | evidence=days=4; total_rows=23; avg_hit=0.531; dominant_bias=OVER_ESTIMATE; statuses=MODEL_OVER_ESTIMATING;MODEL_OVER_ESTIMATING;MODEL_OVER_ESTIMATING;MODEL_UNDER_ESTIMATING | recommendation=Open manual review for metric-specific formula adjustment. No auto-apply. | safe_auto_pr=NO | auto_merge=NO
- HIGH | calibration/total_goals | PATCH_CANDIDATE_REVIEW | evidence=days=5; total_rows=27; avg_hit=0.430; dominant_bias=OVER_ESTIMATE; statuses=MODEL_OVER_ESTIMATING;MODEL_OVER_ESTIMATING;MODEL_OVER_ESTIMATING;MODEL_OVER_ESTIMATING;LOW_SAMPLE_HOLD | recommendation=Open manual review for metric-specific formula adjustment. No auto-apply. | safe_auto_pr=NO | auto_merge=NO
- LOW | issue_alert | MATERIAL_ALERT_CHANGE | evidence=notify_required=true | recommendation=Review vsigma-alert issue. | safe_auto_pr=NO | auto_merge=NO
- LOW | calibration/total_cards | ACCUMULATE_MORE_SAMPLE | evidence=days=4; total_rows=19; avg_hit=0.783; dominant_bias=UNDER_ESTIMATE; statuses=CALIBRATION_OK;CALIBRATION_OK;CALIBRATION_OK;CALIBRATION_OK | recommendation=Keep collecting evidence before formula changes. | safe_auto_pr=NO | auto_merge=NO
- LOW | calibration/total_fouls | ACCUMULATE_MORE_SAMPLE | evidence=days=4; total_rows=24; avg_hit=0.709; dominant_bias=OVER_ESTIMATE; statuses=CALIBRATION_OK;MODEL_UNDER_ESTIMATING;MODEL_OVER_ESTIMATING;MODEL_OVER_ESTIMATING | recommendation=Keep collecting evidence before formula changes. | safe_auto_pr=NO | auto_merge=NO
- LOW | calibration/total_shots | ACCUMULATE_MORE_SAMPLE | evidence=days=4; total_rows=24; avg_hit=0.778; dominant_bias=OVER_ESTIMATE; statuses=CALIBRATION_OK;MODEL_OVER_ESTIMATING;CALIBRATION_OK;CALIBRATION_OK | recommendation=Keep collecting evidence before formula changes. | safe_auto_pr=NO | auto_merge=NO
- LOW | calibration/total_sot | ACCUMULATE_MORE_SAMPLE | evidence=days=4; total_rows=23; avg_hit=0.708; dominant_bias=UNDER_ESTIMATE; statuses=CALIBRATION_OK;MODEL_UNDER_ESTIMATING;CALIBRATION_OK;MODEL_UNDER_ESTIMATING | recommendation=Keep collecting evidence before formula changes. | safe_auto_pr=NO | auto_merge=NO

## Guardrails
- Advisor proposes only; it does not change formulas, thresholds or stakes.
- safe_auto_pr=YES is only for reporting/ops cleanup, never prediction logic.
- auto_merge remains NO.
