$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot
$env:FORGEQC_DATA_DIR = Join-Path $PSScriptRoot 'data'

if (-not (Test-Path '.venv')) {
    py -m venv .venv
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\pip.exe install -r requirements.txt
& .\.venv\Scripts\python.exe smoke_test.py
& .\.venv\Scripts\python.exe app.py
