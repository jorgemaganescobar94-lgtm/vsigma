<#
  vSIGMA World Cup - LOCAL daily runner (stopgap while GitHub Actions is blocked).

  Replicates EXACTLY the cloud workflow `.github/workflows/vsigma_worldcup_cards.yml`
  in MORNING mode:
    load .env (API) + .env.telegram (Telegram) into the PROCESS env only ->
    build WIDE [HOY-1,HOY+3] -> log -> rebuild NARROW (morning) -> settle ->
    scorecard -> render -> send Telegram -> git pull --rebase + commit ONLY
    (log + scorecard [+ gaps]) [skip ci] + push (with retries).

  SECURITY:
    - This file contains NO secrets. It reads them from .env / .env.telegram.
    - It NEVER prints secret values (only "present/missing" + lengths are noted).
    - Per-run log goes to analysis/worldcup/worldcup_local_run.log (gitignored via *.log).
    - git add uses EXPLICIT paths only, never `git add .`.

  Safe to commit.
#>

$ErrorActionPreference = 'Stop'

# --- paths ---------------------------------------------------------------
$ScriptDir = $PSScriptRoot
$Repo      = (Resolve-Path (Join-Path $ScriptDir '..\..')).Path
$Py        = Join-Path $Repo '.venv\Scripts\python.exe'
$LogFile   = Join-Path $ScriptDir 'worldcup_local_run.log'
$LogCsv    = 'analysis/worldcup/worldcup_predictions_log.csv'
$Scorecard = 'analysis/worldcup/worldcup_scorecard.txt'
$GapsFile  = 'analysis/worldcup/worldcup_gaps.txt'
$Manifest  = Join-Path $ScriptDir 'worldcup_messages_manifest.txt'

Set-Location $Repo

# --- logging (never logs secret values) ----------------------------------
function Log([string]$msg) {
  $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
  $line = "[$ts] $msg"
  Add-Content -Path $LogFile -Value $line -Encoding utf8
  Write-Host $line
}

function Run-Step([string]$name, [scriptblock]$block) {
  Log "STEP START: $name"
  try {
    & $block
    if ($LASTEXITCODE -ne $null -and $LASTEXITCODE -ne 0) {
      Log "STEP FAIL : $name (exit=$LASTEXITCODE)"
      return $false
    }
    Log "STEP OK   : $name"
    return $true
  } catch {
    Log "STEP FAIL : $name (exception: $($_.Exception.GetType().Name))"
    return $false
  }
}

# Load KEY=VALUE pairs from a dotenv-style file into the PROCESS env.
# Silent: does not echo values.
function Load-EnvFile([string]$path) {
  if (-not (Test-Path $path)) { return $false }
  foreach ($raw in Get-Content -Path $path) {
    $line = $raw.Trim()
    if ($line -eq '' -or $line.StartsWith('#')) { continue }
    $idx = $line.IndexOf('=')
    if ($idx -lt 1) { continue }
    $k = $line.Substring(0, $idx).Trim()
    $v = $line.Substring($idx + 1).Trim()
    [Environment]::SetEnvironmentVariable($k, $v, 'Process')
  }
  return $true
}

Log "===== LOCAL RUN START (morning) ====="

# --- guards --------------------------------------------------------------
if (-not (Test-Path $Py)) { Log "FATAL: venv python not found at .venv\Scripts\python.exe"; exit 1 }

$envOk = Load-EnvFile (Join-Path $Repo '.env')
$tgOk  = Load-EnvFile (Join-Path $Repo '.env.telegram')
Log ".env loaded: $envOk | .env.telegram loaded: $tgOk"

$tok  = [Environment]::GetEnvironmentVariable('TELEGRAM_BOT_TOKEN', 'Process')
$chat = [Environment]::GetEnvironmentVariable('TELEGRAM_CHAT_ID', 'Process')
$tokOk  = -not [string]::IsNullOrWhiteSpace($tok)
$chatOk = -not [string]::IsNullOrWhiteSpace($chat)
Log "telegram secrets: TOKEN present=$tokOk (len=$($tok.Length)) | CHAT_ID present=$chatOk (len=$($chat.Length))"

# --- UTC window (mirrors the workflow's `date -u` math) ------------------
$nowUtc  = (Get-Date).ToUniversalTime()
$From    = $nowUtc.ToString('yyyy-MM-dd')
$To      = $nowUtc.AddDays(1).ToString('yyyy-MM-dd')   # morning days_ahead=1
$LogFrom = $nowUtc.AddDays(-1).ToString('yyyy-MM-dd')
$LogTo   = $nowUtc.AddDays(3).ToString('yyyy-MM-dd')
Log "window UTC: narrow [$From..$To]  wide [$LogFrom..$LogTo]"

# --- chain ---------------------------------------------------------------
$ok = $true

# 1) WIDE build (feeds the log only; not shown on Telegram)
$ok = $ok -and (Run-Step "build WIDE [$LogFrom..$LogTo]" {
  & $Py analysis/worldcup/build_worldcup_cards.py --from $LogFrom --to $LogTo | Out-Null
})

# 2) Log over wide window (pre-match only, dedup, writes gaps if any)
$ok = $ok -and (Run-Step "log predictions (wide)" {
  & $Py analysis/worldcup/worldcup_learning_loop.py log | Out-Null
})

# 3) Rebuild NARROW card (Telegram view; morning)
$ok = $ok -and (Run-Step "build NARROW [$From..$To]" {
  & $Py analysis/worldcup/build_worldcup_cards.py --from $From --to $To | Out-Null
})

# 4) Settle finished fixtures
$ok = $ok -and (Run-Step "settle" {
  & $Py analysis/worldcup/worldcup_learning_loop.py settle | Out-Null
})

# 5) Scorecard
$ok = $ok -and (Run-Step "scorecard" {
  & $Py analysis/worldcup/worldcup_learning_loop.py scorecard | Out-Null
})

# 6) Render paginated messages (morning adds 'ayer')
$ok = $ok -and (Run-Step "render messages" {
  & $Py analysis/worldcup/build_worldcup_full_card.py --from $From --to $To `
      --limit 10 --paginate --per-page 3 `
      --scorecard $Scorecard --log $LogCsv --show-yesterday | Out-Null
})

# 7) Send to Telegram (one call per message). Only if secrets present + manifest non-empty.
if ($tokOk -and $chatOk -and (Test-Path $Manifest)) {
  $sent = 0; $failed = 0
  foreach ($mline in Get-Content -Path $Manifest) {
    if ([string]::IsNullOrWhiteSpace($mline)) { continue }
    $parts = $mline.Split('|', 2)
    $f = $parts[0]; $t = if ($parts.Count -gt 1) { $parts[1] } else { 'Mundial 2026' }
    $out = & $Py scripts/dispatch_telegram_alert.py --title $t --date $From --body-file $f 2>&1 | Out-String
    if ($out -match 'HTTP 200|enviado') { $sent++; Log "telegram OK  : $t" }
    else {
      $failed++
      $code = if ($out -match '(\d{3})') { $Matches[1] } else { '???' }
      Log "telegram FAIL: $t (code=$code)"
    }
    Start-Sleep -Seconds 1
  }
  Log "telegram summary: sent=$sent failed=$failed"
} else {
  Log "telegram SKIP: secrets missing or no manifest (fail-soft)."
}

# 8) Persist ONLY log + scorecard (+ gaps if present); pull --rebase + push w/ retries
$ok = $ok -and (Run-Step "git commit + push (explicit paths)" {
  git add $LogCsv $Scorecard
  if (Test-Path $GapsFile) { git add $GapsFile }
  git diff --cached --quiet
  if ($LASTEXITCODE -eq 0) {
    Log "git: no changes to commit."
    $global:LASTEXITCODE = 0
  } else {
    git commit -m "vSIGMA World Cup learning loop $From (local stopgap) [skip ci]"
    $pushed = $false
    for ($i = 1; $i -le 3; $i++) {
      git pull --rebase origin main
      if ($LASTEXITCODE -eq 0) {
        git push origin main
        if ($LASTEXITCODE -eq 0) { $pushed = $true; break }
      }
      Log "git: push retry $i failed; re-syncing..."
      Start-Sleep -Seconds 5
    }
    if (-not $pushed) { Log "git: push FAILED after retries (Telegram already sent)."; $global:LASTEXITCODE = 1 }
    else { $global:LASTEXITCODE = 0 }
  }
})

if ($ok) { Log "===== LOCAL RUN END: OK =====" ; exit 0 }
else     { Log "===== LOCAL RUN END: WITH FAILURES =====" ; exit 1 }
