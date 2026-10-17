@echo off
cd /d "%~dp0"
python scripts\ouvrir-academy.py
if errorlevel 1 pause
