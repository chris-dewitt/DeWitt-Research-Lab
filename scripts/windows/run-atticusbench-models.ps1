<#
.SYNOPSIS
    Measure local Ollama models on the AtticusBench public split, in one command.

.DESCRIPTION
    Checks the daemon, reports which tags it actually serves, pulls anything
    missing when asked, then runs the benchmark against each model and writes a
    run directory with a provenance manifest.

    The daemon that matters is the one answering GET /v1/models on the port this
    script uses. A tag listed by `ollama list` but absent from that endpoint is
    not served to the benchmark, which is a real and confusing failure mode on
    Windows, so the check is explicit.

.PARAMETER Model
    One or more Ollama tags to measure. Omit to measure every candidate in
    models/bakeoff/candidates.yaml that declares a serving block.

.PARAMETER Candidate
    One or more register candidate ids from models/bakeoff/candidates.yaml,
    measured with the serving settings the register declares (system_prefix and
    the rest). Prefer this over -Model: an ad-hoc tag gets the endpoint's
    defaults and nothing else, which for a reasoning model is the difference
    between a plan and a stall.

.PARAMETER Repeats
    Run the split this many times per model, to see how stable its plans are.

.PARAMETER Pull
    Pull any named tag the endpoint does not serve before running.

.PARAMETER Case
    Limit to one case id. Repeatable. Useful while setting up.

.PARAMETER BaseUrl
    OpenAI-compatible endpoint. Defaults to the local Ollama default.

.PARAMETER Timeout
    Total seconds one completion may take. Defaults to the Python default of
    600. A quantized model planning on a laptop CPU can need minutes per case,
    and a case that reaches the ceiling is recorded as a provider error rather
    than as the model declining to plan.

.EXAMPLE
    .\run-atticusbench-models.ps1
    Measures whatever the register serves.

.EXAMPLE
    .\run-atticusbench-models.ps1 -Candidate edge-qwen3-1.7b
    One register candidate, served exactly as the register declares it.

.EXAMPLE
    .\run-atticusbench-models.ps1 -Model qwen3:1.7b,llama3.2:3b -Pull -Repeats 2

.EXAMPLE
    .\run-atticusbench-models.ps1 -Stub
    No daemon, no model: exercises the path and proves the setup works.
#>

[CmdletBinding()]
param(
    # Every parameter is named. Without this a typo such as `- Stub` binds its
    # stray token positionally to the first parameter that accepts one, and the
    # error names a parameter the caller never mentioned.
    [Parameter(Mandatory = $false, Position = [int]::MaxValue)]
    [string[]] $Model,
    [Parameter(Mandatory = $false, Position = [int]::MaxValue)]
    [string[]] $Candidate,
    [Parameter(Mandatory = $false, Position = [int]::MaxValue)]
    [int] $Repeats = 1,
    [switch] $Pull,
    [Parameter(Mandatory = $false, Position = [int]::MaxValue)]
    [string[]] $Case,
    [Parameter(Mandatory = $false, Position = [int]::MaxValue)]
    [string] $BaseUrl = 'http://localhost:11434/v1',
    # Total seconds one completion may take. The Python default is 600; a
    # quantized model planning on a laptop CPU can need minutes per case, and a
    # case that reaches the ceiling is recorded as a provider error rather than
    # as the model declining to plan.
    [double] $Timeout = 0,
    [switch] $Stub
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

function Write-Step { param([string] $Text) Write-Host "==> $Text" -ForegroundColor Cyan }
function Write-Warn { param([string] $Text) Write-Host "    $Text" -ForegroundColor Yellow }

Write-Step "Repository: $RepoRoot"

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv is not on PATH. Install it from https://docs.astral.sh/uv/ and reopen the shell."
}

Push-Location $RepoRoot
try {
    if ($Stub) {
        Write-Step 'Stub run: no daemon, no model, plumbing only.'
        $stubArgs = @('run', 'python', 'scripts/run_atticusbench_models.py', '--stub')
        if ($Timeout -gt 0) { $stubArgs += @('--timeout', $Timeout) }
        foreach ($id in $Case) { $stubArgs += @('--case', $id) }
        & uv @stubArgs
        exit $LASTEXITCODE
    }

    $tagsUrl = ($BaseUrl.TrimEnd('/')) + '/models'
    Write-Step "Checking the daemon at $tagsUrl"
    $served = @()
    try {
        $response = Invoke-RestMethod -Uri $tagsUrl -TimeoutSec 10
        $served = @($response.data | ForEach-Object { $_.id })
        Write-Host "    serving $($served.Count) model(s): $($served -join ', ')"
    }
    catch {
        Write-Warn "No answer from $tagsUrl."
        Write-Warn 'Start it with `ollama serve` (or check that the Windows service is running),'
        Write-Warn 'then re-run. To verify the setup without a model, pass -Stub.'
        throw
    }

    if ($Model) {
        $missing = @($Model | Where-Object { $served -notcontains $_ })
        if ($missing.Count -gt 0) {
            if ($Pull) {
                foreach ($tag in $missing) {
                    Write-Step "Pulling $tag"
                    & ollama pull $tag
                    if ($LASTEXITCODE -ne 0) { throw "ollama pull $tag failed." }
                }
                # A pull must land on the daemon answering this endpoint, so
                # confirm rather than assume.
                $response = Invoke-RestMethod -Uri $tagsUrl -TimeoutSec 30
                $served = @($response.data | ForEach-Object { $_.id })
                $stillMissing = @($Model | Where-Object { $served -notcontains $_ })
                if ($stillMissing.Count -gt 0) {
                    Write-Warn "Pulled, but $tagsUrl still does not serve: $($stillMissing -join ', ')"
                    Write-Warn 'That usually means two daemons, or a pull that landed on a different one.'
                }
            }
            else {
                Write-Warn "Not served here: $($missing -join ', '). Re-run with -Pull, or pull them yourself."
            }
        }
    }

    $runArgs = @('run', 'python', 'scripts/run_atticusbench_models.py',
                 '--base-url', $BaseUrl, '--repeats', $Repeats)
    foreach ($tag in $Model) { $runArgs += @('--model', $tag) }
    foreach ($id in $Case) { $runArgs += @('--case', $id) }
    foreach ($id in $Candidate) { $runArgs += @('--candidate', $id) }
    if ($Timeout -gt 0) { $runArgs += @('--timeout', $Timeout) }

    Write-Step 'Running the benchmark'
    & uv @runArgs
    $code = $LASTEXITCODE

    Write-Step 'Where the results went'
    Write-Host '    runs/atticusbench/models/<system>/<run-id>/manifest.json   provenance + scores'
    Write-Host '    runs/atticusbench/models/<system>/<run-id>/records/        per-case detail'
    Write-Host ''
    Write-Host '    Model runs are not reproducible and are excluded from results.json'
    Write-Host '    and from every drift check. To share one, commit the run directory'
    Write-Host '    on a branch and push; the manifest carries the commit, the corpus'
    Write-Host '    digest, the model identity, and this host.'
    exit $code
}
finally {
    Pop-Location
}
