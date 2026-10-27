@echo off
setlocal
cd /d "%~dp0"
echo.
echo ORCHESTRA NSI - Installation de Pyodide 0.27.7 pour usage hors connexion
where py >nul 2>nul
if %errorlevel%==0 (py -3 installer_pyodide.py) else (python installer_pyodide.py)
echo.
pause
