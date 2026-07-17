# Read-only central health entrypoint for Task Scheduler.  It executes no domain pipeline.
# Keep ASCII only for Windows PowerShell 5.1 compatibility.
$ErrorActionPreference = "Stop"
$base = Split-Path -Parent $PSScriptRoot
$tool = Join-Path $base "tools\ecosystem_health.py"
$log = Join-Path $base "ecosystem_health.log"
if (-not (Test-Path $tool)) { Write-Error "health tool ausente em $tool"; exit 2 }

$output = & py -3.14 $tool @args 2>&1
$exitCode = $LASTEXITCODE
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
@("===== ecosystem_health $stamp =====") + $output + "" | Out-File -FilePath $log -Append -Encoding utf8
$output | Write-Output
exit $exitCode
