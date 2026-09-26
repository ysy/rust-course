# Windows PowerShell wrapper to sync upstream and rebuild ebooks
param (
    [switch]$Force,
    [string[]]$Targets = @("all"),
    [string]$OutputDir = "dist"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PyScript = Join-Path $ScriptDir "sync_and_build.py"

$ArgsList = @()
if ($Force) { $ArgsList += "--force" }
if ($Targets) { 
    $ArgsList += "--targets"
    $ArgsList += $Targets 
}
if ($OutputDir) {
    $ArgsList += "--output-dir"
    $ArgsList += $OutputDir
}

python $PyScript @ArgsList
