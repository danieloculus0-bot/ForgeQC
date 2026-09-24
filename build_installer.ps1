$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

& ".\build_windows.ps1"

$iscc = Get-Command "ISCC.exe" -ErrorAction SilentlyContinue
if (-not $iscc) {
    $candidate = Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe"
    if (Test-Path $candidate) {
        $iscc = Get-Item $candidate
    }
}

if (-not $iscc) {
    throw "Inno Setup 6 is required to build the ForgeQC installer."
}

& $iscc.Source ".\installer\ForgeQC.iss"

Write-Host ""
Write-Host "Installer build complete:"
Get-ChildItem ".\dist-installer\ForgeQC_Server_Setup_*.exe" | ForEach-Object { Write-Host $_.FullName }
