@echo off
REM ==============================================================================
REM Taapamigo — SIH26083 Local Launch Script (Windows Batch)
REM ==============================================================================

echo [Taapamigo] Launching local evaluation server...
cd /d "%~dp0\.."

python run_local.py
pause
