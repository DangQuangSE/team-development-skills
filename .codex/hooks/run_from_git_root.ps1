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

$root = ((& git rev-parse --show-toplevel 2>$null) | Select-Object -First 1)
if ($null -eq $root) {
    [Console]::Error.WriteLine("Could not determine the git repository root for Codex hook.")
    exit 128
}
$root = $root.ToString().Trim()
if ([string]::IsNullOrWhiteSpace($root)) {
    [Console]::Error.WriteLine("Could not determine the git repository root for Codex hook.")
    exit 128
}

$runner = Join-Path $root ".codex/hooks/run_python.ps1"
$script = Join-Path $root (Join-Path ".codex/hooks" $ScriptName)
if (-not (Test-Path -LiteralPath $runner -PathType Leaf) -or
    -not (Test-Path -LiteralPath $script -PathType Leaf)) {
    [Console]::Error.WriteLine("Codex hook script was not found under the repository root.")
    exit 127
}

Set-Location -LiteralPath $root
& $runner $script
exit $LASTEXITCODE
