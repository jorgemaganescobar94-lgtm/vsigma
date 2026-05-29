# vSIGMA Evidence Closure Sequencer - 2026-05-29

## Executive Sequence Summary
- generated_at: 2026-05-29T13:29:24+01:00
- executive_status: PRELOCK_FIRST
- sequence_items: 9
- phase_counts: POST_RESULTS=4; PRELOCK_CHECK=2; LEARNING_REBUILD=1; QUALITY_REVIEW=1; READINESS_REVIEW=1
- can_run_now_counts: NO=9
- auto_run: NO
- production_change: NO

## Safe Sequence
- #1 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1535315 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-29"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #2 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1535327 | market=BTTS_YES | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-29"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #3 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-29"` | reason=Post results can only run safely after matches are finished.
- #4 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-29"` | reason=Post results can only run safely after matches are finished.
- #5 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-29"` | reason=Post results can only run safely after matches are finished.
- #6 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-29"` | reason=Post results can only run safely after matches are finished.
- #7 | phase=LEARNING_REBUILD | state=WAIT_FOR_POST_RESULTS | fixture=N/A | market=UNKNOWN | command=`python scripts/build_learning_ledger.py --date 2026-05-29 --timezone Atlantic/Canary` | reason=Learning rebuild should happen after post-result labeling.
- #8 | phase=QUALITY_REVIEW | state=WAIT_FOR_LEARNING_REBUILD | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_data_quality_governor.yml -f date="2026-05-29"` | reason=Quality review should be rerun after learning evidence is rebuilt.
- #9 | phase=READINESS_REVIEW | state=WAIT_FOR_QUALITY_REVIEW | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_pattern_promotion_readiness.yml -f date="2026-05-29"` | reason=Readiness should be reviewed only after data quality is refreshed.

## Guardrails
- This sequencer does not run commands.
- It only orders safe phases for operator or future controlled automation.
- Correct order: PRELOCK when timed, POST after fixtures, rebuild learning, rerun quality/readiness.