# vSIGMA Evidence Closure Sequencer - 2026-05-22

## Executive Sequence Summary
- generated_at: 2026-05-22T15:52:38+01:00
- executive_status: PRELOCK_FIRST
- sequence_items: 20
- phase_counts: POST_RESULTS=13; PRELOCK_CHECK=3; LEARNING_REBUILD=2; QUALITY_REVIEW=1; READINESS_REVIEW=1
- can_run_now_counts: NO=20
- auto_run: NO
- production_change: NO

## Safe Sequence
- #1 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1494177 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-22"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #2 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1544652 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-22"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #3 | phase=PRELOCK_CHECK | state=WAIT_FOR_WINDOW_OR_OPERATOR | fixture=1545405 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=prelock -f date="2026-05-22"` | reason=Prelock/lineup timing must be checked before any serious execution.
- #4 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #5 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #6 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1494177 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #7 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1544652 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #8 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #9 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #10 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #11 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1494177 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #12 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1494177 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #13 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1494177 | market=OVER_2_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #14 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1544652 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #15 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1544652 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #16 | phase=POST_RESULTS | state=WAIT_FOR_FIXTURES_FINISHED | fixture=1544652 | market=OVER_1_5 | command=`gh workflow run vsigma_production.yml -f mode=post -f date="2026-05-22"` | reason=Post results can only run safely after matches are finished.
- #17 | phase=LEARNING_REBUILD | state=WAIT_FOR_POST_RESULTS | fixture=N/A | market=UNKNOWN | command=`python scripts/build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild should happen after post-result labeling.
- #18 | phase=LEARNING_REBUILD | state=WAIT_FOR_POST_RESULTS | fixture=1544652 | market=OVER_1_5 | command=`python scripts/build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild should happen after post-result labeling.
- #19 | phase=QUALITY_REVIEW | state=WAIT_FOR_LEARNING_REBUILD | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_data_quality_governor.yml -f date="2026-05-22"` | reason=Quality review should be rerun after learning evidence is rebuilt.
- #20 | phase=READINESS_REVIEW | state=WAIT_FOR_QUALITY_REVIEW | fixture=N/A | market=UNKNOWN | command=`gh workflow run vsigma_pattern_promotion_readiness.yml -f date="2026-05-22"` | reason=Readiness should be reviewed only after data quality is refreshed.

## Guardrails
- This sequencer does not run commands.
- It only orders safe phases for operator or future controlled automation.
- Correct order: PRELOCK when timed, POST after fixtures, rebuild learning, rerun quality/readiness.