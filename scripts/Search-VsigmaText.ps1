param(
    [Parameter(Mandatory = $true)]
    [string]$Pattern,

    [string]$Path = ".",

    [string[]]$Include = @("*"),

    [switch]$CaseSensitive,

    [switch]$List,

    [int]$Context = 0
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $Path)) {
    throw "Search path not found: $Path"
}

$files = Get-ChildItem -LiteralPath $Path -Recurse -File -Include $Include -ErrorAction SilentlyContinue

$selectArgs = @{
    Pattern = $Pattern
}

if ($CaseSensitive) {
    $selectArgs.CaseSensitive = $true
}
if ($List) {
    $selectArgs.List = $true
}
if ($Context -gt 0) {
    $selectArgs.Context = $Context
}

$files | Select-String @selectArgs
