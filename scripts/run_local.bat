@echo off
REM ==============================================================================
REM ThermoShield India — SIH26083 Local Launch Script (Windows Batch)
REM ==============================================================================

echo [ThermoShield] Launching local evaluation server...
cd /d "%~dp0\.."

python run_local.py
pause
