# ==============================================================================
# ThermoShield India — SIH26083 Local Launch Script (PowerShell)
# ==============================================================================

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host " ThermoShield India — SIH 2026 PS26083 Local Server Runner (PowerShell)" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
Set-Location $RootDir

python run_local.py
