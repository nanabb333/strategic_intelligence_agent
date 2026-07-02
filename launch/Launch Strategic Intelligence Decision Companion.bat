@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."
cd /d "%ROOT_DIR%"

echo.
echo Strategic Intelligence Decision Companion
echo.
echo Preparing local launch...
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  python launch.py
  goto finished
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -3 launch.py
  goto finished
)

echo Python 3 is required to launch this product.
echo Install Python 3, then double-click this launcher again.

:finished
echo.
echo Decision Workspace stopped.
echo Press any key to close this window.
pause >nul
