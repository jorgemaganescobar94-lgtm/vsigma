# vSIGMA Scoring Gap Explainer - 2026-06-02

## Summary
- rows_reviewed: 59
- missing_scored_rows: 44
- no_data_blocked_rows: 1
- not_trusted_rows: 14
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=44; NOT_TRUSTED_SKIPPED=14; SCORED_ROW_NO_DATA_BLOCKED=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.
- auto_apply: NO
- production_change: NO

## Gap Diagnosis
- 44 trusted raw candidates have no matching row in `matches_vsigma_scored_v3.csv`; they are waiting for scoring/enrichment.
- 1 trusted raw candidate has a matching scored row, but it is `NO_DATA_BLOCKED`.
- 14 raw candidates are not trusted and remain diagnostic-only.
- 0 candidates are promoted to scoring-safe downstream use.

## Key Examples
- La Unión vs Deportivo Cuenca | gap=SCORED_ROW_NO_DATA_BLOCKED | stage=SCORING_ENRICHMENT_BLOCKED | scored=NO_DATA_BLOCKED | fix=Repair enrichment inputs for stats/odds/standings/coverage; do not promote until non-blocked.
- Ario Eslamshahr vs Shahrdari Noshahr | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Fard Alborz vs Mes Kerman | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- China PR U20 vs Congo DR U20 | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.

## Guardrails
- Scoring gap explainer is diagnostic only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Missing scored rows must be repaired upstream before translator/board discussion.
