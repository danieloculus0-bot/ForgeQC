@echo off
setlocal
cd /d %~dp0

if not exist .venv (
  py -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python smoke_test.py
if errorlevel 1 (
  echo.
  echo ForgeQC smoke test failed. Fix the error above before launching.
  pause
  exit /b 1
)

python app.py
