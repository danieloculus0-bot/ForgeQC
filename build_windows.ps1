$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv-build")) {
    py -m venv .venv-build
}

$python = Join-Path $PSScriptRoot ".venv-build\Scripts\python.exe"
& $python -m pip install --upgrade pip
& $python -m pip install -r requirements-build.txt
& $python smoke_test.py
& $python -m PyInstaller --noconfirm --clean --onefile --console --name ForgeQC_Server desktop.py

Write-Host ""
Write-Host "Build complete:"
Write-Host (Join-Path $PSScriptRoot "dist\ForgeQC_Server.exe")
