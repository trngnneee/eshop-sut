[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$taskRoot = Split-Path -Parent $PSScriptRoot
$repositoryRoot = Split-Path -Parent $taskRoot
$backendRoot = Join-Path $repositoryRoot "backend"
$frontendRoot = Join-Path $repositoryRoot "frontend-web"
$evidenceRoot = Join-Path $taskRoot "evidence\technical-preflight"
$nodeScript = Join-Path $PSScriptRoot "technical-preflight.js"

New-Item -ItemType Directory -Force -Path $evidenceRoot | Out-Null

$backendProcess = $null
$frontendProcess = $null

function Test-HttpReady {
    param([string]$Uri)
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri $Uri -TimeoutSec 2
        return $response.StatusCode -ge 200 -and $response.StatusCode -lt 500
    }
    catch {
        return $false
    }
}

function Stop-ProcessTree {
    param([int]$RootProcessId)

    $children = @(
        Get-CimInstance Win32_Process -Filter "ParentProcessId = $RootProcessId" -ErrorAction SilentlyContinue
    )
    foreach ($child in $children) {
        Stop-ProcessTree -RootProcessId $child.ProcessId
    }

    Stop-Process -Id $RootProcessId -Force -ErrorAction SilentlyContinue
}

try {
    if (-not (Test-HttpReady "http://127.0.0.1:3000/api/products")) {
        $backendProcess = Start-Process `
            -FilePath "npm.cmd" `
            -ArgumentList @("start") `
            -WorkingDirectory $backendRoot `
            -WindowStyle Hidden `
            -RedirectStandardOutput (Join-Path $evidenceRoot "backend.stdout.log") `
            -RedirectStandardError (Join-Path $evidenceRoot "backend.stderr.log") `
            -PassThru
    }

    if (-not (Test-HttpReady "http://127.0.0.1:5173")) {
        $frontendProcess = Start-Process `
            -FilePath "npm.cmd" `
            -ArgumentList @("run", "dev", "--", "--host", "127.0.0.1") `
            -WorkingDirectory $frontendRoot `
            -WindowStyle Hidden `
            -RedirectStandardOutput (Join-Path $evidenceRoot "frontend.stdout.log") `
            -RedirectStandardError (Join-Path $evidenceRoot "frontend.stderr.log") `
            -PassThru
    }

    $deadline = (Get-Date).AddSeconds(30)
    do {
        $backendReady = Test-HttpReady "http://127.0.0.1:3000/api/products"
        $frontendReady = Test-HttpReady "http://127.0.0.1:5173"
        if ($backendReady -and $frontendReady) {
            break
        }
        Start-Sleep -Milliseconds 500
    } while ((Get-Date) -lt $deadline)

    if (-not $backendReady -or -not $frontendReady) {
        throw "EShop servers did not become ready within 30 seconds."
    }

    & node $nodeScript
    if ($LASTEXITCODE -ne 0) {
        throw "Technical preflight failed. Inspect evidence/technical-preflight/result.json."
    }
}
finally {
    if ($null -ne $frontendProcess) {
        Stop-ProcessTree -RootProcessId $frontendProcess.Id
    }
    if ($null -ne $backendProcess) {
        Stop-ProcessTree -RootProcessId $backendProcess.Id
    }
}
