cd C:\vsigma

$fecha = Read-Host "Introduce la fecha (YYYY-MM-DD)"
$tz = "Atlantic/Canary"

.\.venv\Scripts\python.exe scripts\run_today_match_pipeline.py --date $fecha --timezone $tz

Write-Host ""
Write-Host "===== SAFE TOP5 ====="
Import-Csv .\data\processed\vsigma_today_safe_top5.csv |
Select-Object execution_mode_rank,fixture_id,league,home_team,away_team,market_primary,final_recommendation,pick_mode_reason |
Format-Table -AutoSize

Write-Host ""
Write-Host "===== BALANCED TOP5 ====="
Import-Csv .\data\processed\vsigma_today_balanced_top5.csv |
Select-Object execution_mode_rank,fixture_id,league,home_team,away_team,market_primary,final_recommendation,pick_mode_reason |
Format-Table -AutoSize

Write-Host ""
Write-Host "===== AGGRESSIVE TOP5 ====="
Import-Csv .\data\processed\vsigma_today_aggressive_top5.csv |
Select-Object execution_mode_rank,fixture_id,league,home_team,away_team,market_primary,final_recommendation,pick_mode_reason |
Format-Table -AutoSize

Write-Host ""
Write-Host "===== EXECUTION SHORTLIST ====="
Import-Csv .\data\processed\vsigma_today_execution_shortlist.csv |
Select-Object execution_rank,fixture_id,league,home_team,away_team,market_primary,final_execution_bucket,final_recommendation,execution_score |
Format-Table -AutoSize
