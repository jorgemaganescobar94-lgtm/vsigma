param(
    [ValidateSet("pre", "status", "prelock", "post", "plan", "full")]
    [string]$Mode = "status",

    [string]$Date = "",

    [string]$Timezone = "Atlantic/Canary",

    [int]$WindowMinutes = 90
)

$ErrorActionPreference = "Stop"
Set-Location "C:\vsigma"

$python = "C:\vsigma\.venv\Scripts\python.exe"
if (!(Test-Path $python)) {
    throw "No se encontro el Python del entorno virtual: $python"
}

if ([string]::IsNullOrWhiteSpace($Date)) {
    $Date = & $python -c "from datetime import datetime; from zoneinfo import ZoneInfo; print(datetime.now(ZoneInfo('$Timezone')).date())"
    $Date = $Date.Trim()
}

$env:PYTHONIOENCODING = "utf-8"

& $python scripts\run_daily_competition_controller.py `
    --date $Date `
    --timezone $Timezone `
    --mode $Mode `
    --window-minutes $WindowMinutes
