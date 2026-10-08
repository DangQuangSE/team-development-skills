param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$ScriptName
)

$ErrorActionPreference = "Stop"

if ([IO.Path]::IsPathRooted($ScriptName) -or
    $ScriptName.Contains("/") -or
    $ScriptName.Contains("\") -or
    $ScriptName.Contains("..")) {
    [Console]::Error.WriteLine("Hook script name must be a file name inside .codex/hooks.")
    exit 2
}

$hookDirectory = $PSScriptRoot
$workspaceRoot = Split-Path -Parent (Split-Path -Parent $hookDirectory)
$runner = Join-Path $hookDirectory "run_python.ps1"
$script = Join-Path $hookDirectory $ScriptName
if (-not (Test-Path -LiteralPath $runner -PathType Leaf) -or
    -not (Test-Path -LiteralPath $script -PathType Leaf)) {
    [Console]::Error.WriteLine("Codex hook script was not found beside the hook runner.")
    exit 127
}

Set-Location -LiteralPath $workspaceRoot
& $runner $script
exit $LASTEXITCODE
