@echo off
setlocal
cd /d "%~dp0"
echo.
echo ====================================================
echo   ORCHESTRA NSI - PARCOURS PREMIERE ET TERMINALE
echo ====================================================
echo.
echo Ouvrir dans Edge : http://127.0.0.1:8000/
echo Premiere : http://127.0.0.1:8000/premiere/
echo Terminale : http://127.0.0.1:8000/terminale/
echo Pyodide local si installe avec INSTALLER_PYODIDE.cmd ; sinon Internet requis.
echo Arreter : Ctrl+C
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -m http.server 8000 --bind 127.0.0.1
) else (
  python -m http.server 8000 --bind 127.0.0.1
)
pause
