param(
    [ValidateSet("pre","post")]
    [string]$Mode = "pre",

    [int]$DaysOffset = 0
)

$ErrorActionPreference = "Stop"
Set-Location "C:\vsigma"

$python = "C:\vsigma\.venv\Scripts\python.exe"
$timezone = "Atlantic/Canary"
$logDir = "C:\vsigma\automation_logs"

if (!(Test-Path $python)) {
    throw "No se encontró el Python del entorno virtual: $python"
}

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$date = & $python -c "from datetime import datetime, timedelta; from zoneinfo import ZoneInfo; print((datetime.now(ZoneInfo('$timezone')) + timedelta(days=$DaysOffset)).date())"
$date = $date.Trim()

$timestamp = & $python -c "from datetime import datetime; print(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))"
$timestamp = $timestamp.Trim()

if ($Mode -eq "pre") {
    $script = "scripts\run_today_match_pipeline.py"
    $label = "pre"
}
else {
    $script = "scripts\run_today_post_results_pipeline.py"
    $label = "post"
}

$logFile = Join-Path $logDir "$label`_$date`_$timestamp.log"

Write-Host "======================================"
Write-Host "vSIGMA AUTOMATION"
Write-Host "Modo: $Mode"
Write-Host "Fecha objetivo: $date"
Write-Host "Zona horaria: $timezone"
Write-Host "Log: $logFile"
Write-Host "======================================"

$env:PYTHONIOENCODING = "utf-8"

$cmdLine = "`"$python`" `"$script`" --date $date --timezone $timezone > `"$logFile`" 2>&1"

cmd.exe /c $cmdLine

Get-Content $logFile

if ($LASTEXITCODE -ne 0) {
    throw "El proceso terminó con código $LASTEXITCODE. Revisa el log: $logFile"
}