param(
    [switch]$WhatIfOnly
)

$ErrorActionPreference = "Stop"

$taskNames = @(
    "vSIGMA PRE Daily",
    "vSIGMA PRELOCK Check",
    "vSIGMA POST Daily",
    "vSIGMA POST Backup Yesterday"
)

foreach ($taskName in $taskNames) {
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($null -eq $task) {
        Write-Host "Not registered: $taskName"
        continue
    }

    if ($WhatIfOnly) {
        Write-Host "Would unregister: $taskName"
    }
    else {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-Host "Unregistered: $taskName"
    }
}
