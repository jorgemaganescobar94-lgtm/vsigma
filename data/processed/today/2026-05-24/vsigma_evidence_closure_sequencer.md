# vSIGMA Evidence Closure Sequencer - 2026-05-24

## Executive Sequence Summary
- generated_at: 2026-05-24T10:25:03+01:00
- executive_status: PRELOCK_FIRST
- sequence_items: 24
- phase_counts: POST_RESULTS=15; PRELOCK_CHECK=6; LEARNING_REBUILD=1; QUALITY_REVIEW=1; READINESS_REVIEW=1
- can_run_now_counts: NO=24
- auto_run: NO
- production_change: NO

## Safe Sequence
- #1 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1379344 | market=BTTS_YES | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-24"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #2 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1392205 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-24"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #3 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1392207 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-24"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #4 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1504827 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-24"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #5 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1537007 | market=HOME_WIN | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-24"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #6 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1545796 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-24"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #7 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #8 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1392205 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #9 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1392205 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #10 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1392207 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #11 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1492273 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #12 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1545796 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #13 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #14 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #15 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #16 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1392205 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #17 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1392205 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #18 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1392205 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #19 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1392205 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #20 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1392205 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #21 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1392205 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-24"` | reason=Post results can only run safely after matches are finished.
- #22 | phase=LEARNING_REBUILD | state=WAIT_FOR_POST_RESULTS | fixture=N/A | market=UNKNOWN | command=`python scripts/build_learning_ledger.py --date 2026-05-24 --timezone Atlantic/Canary` | reason=Learning rebuild should happen after post-result labeling.
- #23 | phase=QUALITY_REVIEW | state=WAIT_FOR_LEARNING_REBUILD | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_data_quality_governor.yml -f date="2026-05-24"` | reason=Quality review should be rerun after learning evidence is rebuilt.
- #24 | phase=READINESS_REVIEW | state=WAIT_FOR_QUALITY_REVIEW | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_pattern_promotion_readiness.yml -f date="2026-05-24"` | reason=Readiness should be reviewed only after data quality is refreshed.

## Guardrails
- This sequencer does not run commands.
- It only orders safe phases for operator or future controlled automation.
- Correct order: PRELOCK when timed, POST after fixtures, rebuild learning, rerun quality/readiness.