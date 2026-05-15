cd C:\vsigma

$fecha = Read-Host "Introduce la fecha (YYYY-MM-DD)"
$tz = "Atlantic/Canary"

.\.venv\Scripts\python.exe scripts\run_today_post_results_pipeline.py --date $fecha --timezone $tz

Write-Host ""
Write-Host "===== RESUMEN LEDGER ====="
Import-Csv .\data\processed\vsigma_execution_shortlist_results_summary.csv |
Format-Table -AutoSize

Write-Host ""
Write-Host "===== DETALLE LEDGER ====="
Import-Csv .\data\processed\vsigma_execution_shortlist_results_ledger.csv |
Select-Object execution_rank,fixture_id,league,home_team,away_team,market_primary,final_recommendation,ledger_status,actionable_result,profit_units_effective |
Format-Table -AutoSize
