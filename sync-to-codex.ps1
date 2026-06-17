[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [string]$CodexSkillsPath,
    [switch]$NoPrune
)

$ErrorActionPreference = 'Stop'

$RepoRoot = $PSScriptRoot
$SourceSkillsPath = Join-Path $RepoRoot 'skills'
$SourceReadmePath = Join-Path $RepoRoot 'README.md'

if (-not (Test-Path -LiteralPath $SourceSkillsPath -PathType Container)) {
    throw "Source skills folder not found: $SourceSkillsPath"
}

if (-not $CodexSkillsPath) {
    if ($env:CODEX_HOME) {
        $CodexSkillsPath = Join-Path $env:CODEX_HOME 'skills'
    } else {
        $CodexSkillsPath = Join-Path $env:USERPROFILE '.codex\skills'
    }
}

function Get-FullPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.Path]::GetFullPath($Path)
}

$SourceSkillsFull = Get-FullPath $SourceSkillsPath
$CodexSkillsFull = Get-FullPath $CodexSkillsPath

if ($SourceSkillsFull.TrimEnd('\') -ieq $CodexSkillsFull.TrimEnd('\')) {
    throw "Source and target are the same path: $CodexSkillsFull"
}

if (-not (Test-Path -LiteralPath $CodexSkillsFull -PathType Container)) {
    if ($PSCmdlet.ShouldProcess($CodexSkillsFull, 'Create Codex skills directory')) {
        New-Item -ItemType Directory -Path $CodexSkillsFull | Out-Null
    }
}

$CodexSkillsResolved = Get-FullPath $CodexSkillsFull
$SourceSkillDirs = Get-ChildItem -LiteralPath $SourceSkillsFull -Directory | Sort-Object Name
$SourceSkillNames = @($SourceSkillDirs | ForEach-Object { $_.Name })

Write-Host "Source: $SourceSkillsFull"
Write-Host "Target: $CodexSkillsResolved"
Write-Host "Mode:   mirror repo skills to Codex skills"
if ($NoPrune) {
    Write-Host "Prune:  disabled"
} else {
    Write-Host "Prune:  enabled, preserving .system"
}

foreach ($Skill in $SourceSkillDirs) {
    $TargetSkillPath = Join-Path $CodexSkillsResolved $Skill.Name
    $Action = if (Test-Path -LiteralPath $TargetSkillPath) { 'Replace skill' } else { 'Install skill' }

    if ($PSCmdlet.ShouldProcess($TargetSkillPath, $Action)) {
        if (Test-Path -LiteralPath $TargetSkillPath) {
            $ResolvedTargetSkill = Get-FullPath $TargetSkillPath
            if (-not $ResolvedTargetSkill.StartsWith($CodexSkillsResolved, [System.StringComparison]::OrdinalIgnoreCase)) {
                throw "Refusing to remove path outside target root: $ResolvedTargetSkill"
            }
            Remove-Item -LiteralPath $ResolvedTargetSkill -Recurse -Force
        }

        Copy-Item -LiteralPath $Skill.FullName -Destination $TargetSkillPath -Recurse -Force
    }
}

if (Test-Path -LiteralPath $SourceReadmePath -PathType Leaf) {
    $TargetReadmePath = Join-Path $CodexSkillsResolved 'README.md'
    if ($PSCmdlet.ShouldProcess($TargetReadmePath, 'Copy repo README to Codex skills README')) {
        Copy-Item -LiteralPath $SourceReadmePath -Destination $TargetReadmePath -Force
    }
}

if (-not $NoPrune) {
    $TargetSkillDirs = Get-ChildItem -LiteralPath $CodexSkillsResolved -Directory | Sort-Object Name

    foreach ($TargetSkill in $TargetSkillDirs) {
        if ($TargetSkill.Name -eq '.system') {
            Write-Host "Preserve: $($TargetSkill.FullName)"
            continue
        }

        if ($SourceSkillNames -notcontains $TargetSkill.Name) {
            $ResolvedTargetSkill = Get-FullPath $TargetSkill.FullName
            if (-not $ResolvedTargetSkill.StartsWith($CodexSkillsResolved, [System.StringComparison]::OrdinalIgnoreCase)) {
                throw "Refusing to prune path outside target root: $ResolvedTargetSkill"
            }

            if ($PSCmdlet.ShouldProcess($ResolvedTargetSkill, 'Prune skill not present in repo')) {
                Remove-Item -LiteralPath $ResolvedTargetSkill -Recurse -Force
            }
        }
    }

    $AllowedRootFiles = @('README.md')
    Get-ChildItem -LiteralPath $CodexSkillsResolved -File | Where-Object {
        $AllowedRootFiles -notcontains $_.Name
    } | ForEach-Object {
        $ResolvedTargetFile = Get-FullPath $_.FullName
        if (-not $ResolvedTargetFile.StartsWith($CodexSkillsResolved, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to prune file outside target root: $ResolvedTargetFile"
        }

        if ($PSCmdlet.ShouldProcess($ResolvedTargetFile, 'Prune root file not managed by repo')) {
            Remove-Item -LiteralPath $ResolvedTargetFile -Force
        }
    }
}

Write-Host 'Sync complete.'
