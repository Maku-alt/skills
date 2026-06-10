param(
    [Parameter(Mandatory = $true)]
    [string]$InputPptx,

    [string]$OutputDir = "."
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "extract-pptx.py"

python $pythonScript $InputPptx $OutputDir
