# vSIGMA Promotion Input Bridge - 2026-06-30

## Summary
- source_rows_reviewed: 0
- bridge_rows_written: 0
- promotion_ready_review_only_rows: 0
- blocked_rows: 0
- status_counts: none
- signal_band_counts: none
- promotion_permission_counts: none
- pick_permission_counts: none
- stake_permission_counts: none
- auto_apply: NO
- production_change: NO

## Bridge Rows

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
