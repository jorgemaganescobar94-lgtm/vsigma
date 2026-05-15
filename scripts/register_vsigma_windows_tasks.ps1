param(
    [string]$Root = "C:\vsigma",
    [string]$PreTime = "09:00",
    [string]$PostTime = "23:55",
    [string]$PostBackupTime = "08:15",
    [string]$PrelockStart = "10:00",
    [int]$PrelockIntervalMinutes = 30,
    [int]$PrelockDurationHours = 14,
    [switch]$WhatIfOnly
)

$ErrorActionPreference = "Stop"

$wrapper = Join-Path $Root "run_vsigma_supervisor.ps1"
if (!(Test-Path $wrapper)) {
    throw "Supervisor wrapper not found: $wrapper"
}

function New-VsigmaAction {
    param([string]$Arguments)
    return New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$wrapper`" $Arguments" `
        -WorkingDirectory $Root
}

function Register-VsigmaTask {
    param(
        [string]$TaskName,
        [Microsoft.Management.Infrastructure.CimInstance]$Action,
        [Microsoft.Management.Infrastructure.CimInstance[]]$Trigger
    )
    if ($WhatIfOnly) {
        $triggerTimes = @($Trigger | ForEach-Object {
            if ($_.StartBoundary) {
                ([datetime]$_.StartBoundary).ToString("HH:mm")
            }
        })
        Write-Host "Would register: $TaskName"
        Write-Host "  Trigger count: $($Trigger.Count)"
        Write-Host "  Trigger times: $($triggerTimes -join ', ')"
        return
    }

    $settings = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -MultipleInstances IgnoreNew `
        -ExecutionTimeLimit (New-TimeSpan -Hours 4)
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $settings `
        -Description "vSIGMA daily competition automation" `
        -Force | Out-Null
}

function New-DailyTriggerSet {
    param(
        [string]$StartTime,
        [int]$IntervalMinutes,
        [int]$DurationHours
    )
    if ($IntervalMinutes -le 0) {
        throw "PrelockIntervalMinutes must be greater than zero."
    }
    if ($DurationHours -le 0) {
        throw "PrelockDurationHours must be greater than zero."
    }

    $start = [datetime]::Today.Add([TimeSpan]::Parse($StartTime))
    $end = $start.AddHours($DurationHours)
    $triggers = New-Object System.Collections.Generic.List[Microsoft.Management.Infrastructure.CimInstance]
    $current = $start

    while ($current -lt $end) {
        $triggers.Add((New-ScheduledTaskTrigger -Daily -At $current))
        $current = $current.AddMinutes($IntervalMinutes)
    }

    if ($triggers.Count -eq 0) {
        throw "No prelock triggers were generated."
    }
    return [Microsoft.Management.Infrastructure.CimInstance[]]$triggers.ToArray()
}

$preTrigger = New-ScheduledTaskTrigger -Daily -At $PreTime
$postTrigger = New-ScheduledTaskTrigger -Daily -At $PostTime
$postBackupTrigger = New-ScheduledTaskTrigger -Daily -At $PostBackupTime
$prelockTriggers = New-DailyTriggerSet `
    -StartTime $PrelockStart `
    -IntervalMinutes $PrelockIntervalMinutes `
    -DurationHours $PrelockDurationHours

Register-VsigmaTask `
    -TaskName "vSIGMA PRE Daily" `
    -Action (New-VsigmaAction "-Mode pre -DaysOffset 0") `
    -Trigger $preTrigger

Register-VsigmaTask `
    -TaskName "vSIGMA PRELOCK Check" `
    -Action (New-VsigmaAction "-Mode prelock-check -DaysOffset 0") `
    -Trigger $prelockTriggers

Register-VsigmaTask `
    -TaskName "vSIGMA POST Daily" `
    -Action (New-VsigmaAction "-Mode post -DaysOffset 0") `
    -Trigger $postTrigger

Register-VsigmaTask `
    -TaskName "vSIGMA POST Backup Yesterday" `
    -Action (New-VsigmaAction "-Mode post-backup -DaysOffset -1") `
    -Trigger $postBackupTrigger

if ($WhatIfOnly) {
    Write-Host "Dry run completed. No vSIGMA scheduled tasks were registered."
}
else {
    Write-Host "Registered vSIGMA scheduled tasks:"
}
Write-Host "- vSIGMA PRE Daily at $PreTime"
Write-Host "- vSIGMA PRELOCK Check every $PrelockIntervalMinutes minutes from $PrelockStart for $PrelockDurationHours hours"
Write-Host "- vSIGMA POST Daily at $PostTime"
Write-Host "- vSIGMA POST Backup Yesterday at $PostBackupTime"
