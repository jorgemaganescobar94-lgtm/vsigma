param(
    [ValidateSet("pre", "prelock-check", "post", "post-backup", "status", "full-cycle")]
    [string]$Mode = "status",

    [int]$DaysOffset = 0,

    [string]$Date = "",

    [string]$Timezone = "Atlantic/Canary",

    [int]$WindowMinutes = 90
)

$ErrorActionPreference = "Stop"
Set-Location "C:\vsigma"

$python = "C:\vsigma\.venv\Scripts\python.exe"
$logDir = "C:\vsigma\automation_logs\supervisor"

if (!(Test-Path $python)) {
    throw "No se encontro el Python del entorno virtual: $python"
}

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

if ([string]::IsNullOrWhiteSpace($Date)) {
    $Date = & $python -c "from datetime import datetime, timedelta; from zoneinfo import ZoneInfo; print((datetime.now(ZoneInfo('$Timezone')) + timedelta(days=$DaysOffset)).date())"
    $Date = $Date.Trim()
}

$timestamp = & $python -c "from datetime import datetime; print(datetime.now().strftime('%Y%m%dT%H%M%S'))"
$timestamp = $timestamp.Trim()
$safeMode = $Mode.Replace("-", "_")
$logFile = Join-Path $logDir "$Date`_$safeMode`_$timestamp`_wrapper.log"

$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

Write-Host "======================================"
Write-Host "vSIGMA DAILY SUPERVISOR"
Write-Host "Mode: $Mode"
Write-Host "Date: $Date"
Write-Host "Timezone: $Timezone"
Write-Host "Log: $logFile"
Write-Host "======================================"

& $python scripts\run_daily_competition_supervisor.py `
    --date $Date `
    --timezone $Timezone `
    --mode $Mode `
    --window-minutes $WindowMinutes *>&1 |
    Tee-Object -FilePath $logFile

if ($LASTEXITCODE -ne 0) {
    throw "vSIGMA supervisor failed with exit code $LASTEXITCODE. See log: $logFile"
}
