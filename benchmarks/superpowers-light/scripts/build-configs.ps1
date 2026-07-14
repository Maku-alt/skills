param(
    [Parameter(Mandatory = $true)]
    [string]$SourceCodexHome,

    [Parameter(Mandatory = $true)]
    [string]$SourceSkills,

    [Parameter(Mandatory = $true)]
    [string]$OutputRoot
)

$ErrorActionPreference = 'Stop'

$selected = @(
    'brainstorming',
    'writing-plans',
    'systematic-debugging',
    'test-driven-development',
    'verification-before-completion',
    'dispatching-parallel-agents',
    'subagent-driven-development'
)

$sourceHomePath = [System.IO.Path]::GetFullPath($SourceCodexHome)
$sourceSkillsPath = [System.IO.Path]::GetFullPath($SourceSkills)
$outputPath = [System.IO.Path]::GetFullPath($OutputRoot)
$rootPath = [System.IO.Path]::GetPathRoot($outputPath)

if ($outputPath -eq $rootPath -or $outputPath -eq $sourceHomePath -or $outputPath -eq $sourceSkillsPath) {
    throw "Unsafe OutputRoot: $outputPath"
}

$authPath = Join-Path $sourceHomePath 'auth.json'
$systemSkillsPath = Join-Path $sourceSkillsPath '.system'
if (-not (Test-Path -LiteralPath $authPath -PathType Leaf)) {
    throw "Missing Codex authentication file: $authPath"
}
if (-not (Test-Path -LiteralPath $systemSkillsPath -PathType Container)) {
    throw "Missing .system skills directory: $systemSkillsPath"
}
foreach ($skill in $selected) {
    $skillPath = Join-Path $sourceSkillsPath $skill
    if (-not (Test-Path -LiteralPath $skillPath -PathType Container)) {
        throw "Missing selected skill: $skillPath"
    }
}

if (Test-Path -LiteralPath $outputPath) {
    Remove-Item -LiteralPath $outputPath -Recurse -Force
}
New-Item -ItemType Directory -Path $outputPath | Out-Null

foreach ($configuration in @('B0', 'S1')) {
    $configurationHome = Join-Path $outputPath $configuration
    $skills = Join-Path $configurationHome 'skills'
    New-Item -ItemType Directory -Path $skills -Force | Out-Null
    Copy-Item -LiteralPath $authPath -Destination (Join-Path $configurationHome 'auth.json')
    Copy-Item -LiteralPath $systemSkillsPath -Destination (Join-Path $skills '.system') -Recurse

    if ($configuration -eq 'S1') {
        foreach ($skill in $selected) {
            Copy-Item -LiteralPath (Join-Path $sourceSkillsPath $skill) -Destination (Join-Path $skills $skill) -Recurse
        }
    }
}

$inventory = [ordered]@{
    B0 = @()
    S1 = $selected
    system_skills_shared = $true
}
$inventory | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $outputPath 'inventory.json') -Encoding utf8
Write-Output (Join-Path $outputPath 'inventory.json')
