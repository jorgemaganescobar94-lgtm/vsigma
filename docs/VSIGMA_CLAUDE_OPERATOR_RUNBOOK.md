# vSIGMA Claude Operator Runbook

## Objective
This runbook tells Claude how to operate vSIGMA daily without breaking governance or creating fake picks.

## Daily morning checklist

### 1. Pull latest repo state
```powershell
cd C:\Users\jorge\vsigma
git pull origin main
git status
git log -8 --oneline
```

If there are local modified generated reports from prior manual tests, ask Jorge before restoring. Do not discard user work silently.

### 2. Check scheduled automation output
For the current date:

```powershell
Get-Content "data/processed/today/YYYY-MM-DD/vsigma_auto_api_board_batch_status.md" -Encoding UTF8
```

Interpretation:
- `pre_outcome: success` means PRE/API completed.
- `lineups_outcome: success` means board lineups refresh ran.
- `bridge_batch_outcome: success` means bridge/batch completed.
- Any `failure` needs diagnosis.

### 3. Check bridge report
```powershell
Get-Content "data/processed/governance/vsigma_api_board_candidate_bridge_YYYY-MM-DD.md" -Encoding UTF8
```

Interpretation:
- `candidates_written > 0` means batch candidate input was produced.
- `skipped_rows > 0` means inspect skipped reasons.
- Common skip reasons:
  - `UNSUPPORTED_MARKET`
  - `MISSING_ODDS`
  - `MISSING_1X2_PROBABILITIES`
  - `DUPLICATE_CANDIDATE`

### 4. Check batch report if present
```powershell
Get-Content "data/processed/governance/vsigma_batch_shadow_pipeline_<batch_label>.md" -Encoding UTF8
```

Interpretation:
- `TOP EXECUTABLES` means local checks passed, manual review only.
- `HOLDS` means wait/review.
- `NO EXECUTION` means rejected.
- `ERRORS` means debug scripts/data.

### 5. Never convert batch output into real bet execution
Even if report says `EXECUTE_SMALL_STAKE`, respond to Jorge:

`Sistema: executable shadow/manual review. No apuesta automática. Requiere revisión humana.`

## If API quota is exhausted
If API status returns request limit exhausted, stop all API-heavy operations.

Use:
```powershell
@'
from scripts.api_football_client import APIFootballClient, APIFootballError
c = APIFootballClient()
print('provider:', c.provider)
print('key_name:', c.key_name)
print('base_url:', c.base_url)
print('headers:', list(c.headers.keys()))
print('key_mask:', c.api_key[:4] + '...' + c.api_key[-4:])
try:
    print(c.status(force_refresh=True))
except APIFootballError as e:
    print('status:', e.status_code)
    print('msg:', e.message)
    print('api_errors:', e.api_errors)
    print('response:', e.response_text)
'@ | .\.venv\Scripts\python.exe -
```

Never print full key.

## If API key is invalid
If response says `Invalid API key`, tell Jorge to fix `.env` or GitHub Secrets. Never ask him to paste the full key into chat.

## If Python environment is broken
Use Python 3.11 only:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --no-cache-dir --force-reinstall -r requirements.txt
.\.venv\Scripts\python.exe -c "import sys, requests, numpy, pandas; print(sys.version); print('OK')"
```

## If bridge writes zero candidates
Do not force picks. Inspect skipped rows:

```powershell
Get-Content "data/processed/governance/vsigma_api_board_candidate_bridge_skipped_YYYY-MM-DD.csv" -Encoding UTF8
```

Possible actions:
- If unsupported market is common and important, create a new feature branch or documented commit to support that market.
- If missing odds, improve odds ingestion/board propagation.
- If missing probabilities, improve forecast-to-board propagation.

## Adding support for new markets
Only add one market family at a time. Required steps:
1. Define canonical market name.
2. Add bridge mapping.
3. Add price survival logic.
4. Add final lock handling.
5. Add tests or synthetic validation.
6. Document governance and failure modes.

Likely first candidate:
- `OVER_1_5_SUPPORTED` -> `OVER_1_5`

Do not add market aliases silently.

## Commit discipline
Before commit:
```powershell
.\.venv\Scripts\python.exe -m py_compile scripts/<changed_script>.py
git diff -- <files>
git status
```

Commit:
```powershell
git add explicit\file1 explicit\file2
git commit -m "Specific message [skip ci]"
git push origin main
```

## Reporting format to Jorge
Always classify any recommendation:

- `OFICIAL SISTEMA`
- `SHADOW SISTEMA`
- `API-BACKED`
- `MANUAL/SINTÉTICO`
- `NO DISPONIBLE`
- `NO BET`

Example:

`Veredicto: NO BET oficial. Motivo: API board generó 0 candidatos; bridge skipped 1 row por UNSUPPORTED_MARKET; no hay cuota/probabilidad compatible para batch.`

## Stop conditions
Stop and ask/report when:
- API quota exhausted
- API key invalid
- workflow failed with unknown error
- generated reports are stale
- candidate requires unsupported market support
- code change would alter thresholds/gates/production logic
- local repo has unexpected uncommitted user work

## Long-term Claude responsibilities
- Keep docs accurate.
- Keep workflows healthy.
- Reduce manual steps.
- Add market support incrementally.
- Preserve auditability.
- Maintain `auto_bet: NO`.
