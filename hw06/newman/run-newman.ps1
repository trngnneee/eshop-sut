param(
    [ValidateSet('off','canary','full')]
    [string]$Mode = 'full',
    [string]$BaseUrl = 'http://127.0.0.1:3001',
    [string]$ReportName = '00-full-suite',
    [switch]$DataDriven
)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Resolve-Path (Join-Path $here '..')
$collection = Join-Path $root 'postman\EShop-HW06-23127207.postman_collection.json'
$environment = Join-Path $root 'postman\EShop-HW06-local.postman_environment.json'
$dataDir = Join-Path $root 'postman\data'
$out = Join-Path $here 'reports'
New-Item -ItemType Directory -Force -Path $out | Out-Null

$newman = Join-Path $root 'node_modules\newman\bin\newman.js'
if (-not (Test-Path -LiteralPath $newman)) { throw "Newman not installed at $newman. Run npm install in hw06." }
$script:runExitCodes = @()

function Invoke-NewmanRun([string]$Name, [string[]]$ExtraArgs, [string]$EnvironmentPath = $environment) {
    $html = Join-Path $out ($Name + '.html')
    $json = Join-Path $out ($Name + '.json')
    Write-Host "Running $Name against $BaseUrl (spec_strict=$Mode)"
    & node $newman run $collection -e $EnvironmentPath --env-var "base_url=$BaseUrl" --env-var "spec_strict=$Mode" -r cli,htmlextra,json --reporter-htmlextra-export $html --reporter-json-export $json @ExtraArgs
    $script:runExitCodes += [int]$LASTEXITCODE
    if ($LASTEXITCODE -ne 0) { Write-Warning "$Name exited with $LASTEXITCODE; report was preserved." }
}

if ($DataDriven) {
    # A folder-only Newman run does not execute collection setup.  Export a
    # prepared environment first so DDT requests receive real auth/session
    # state instead of producing misleading 401/empty-order failures.
    $prepEnv = Join-Path $out ('.ddt-prep-' + $PID + '.json')
    try {
        Invoke-NewmanRun '00-ddt-setup' @('--folder','00 - Setup','--export-environment',$prepEnv)
        Invoke-NewmanRun '01-ddt-login' @('--folder','1.1 Domain partitions [DDT]','-d',(Join-Path $dataDir 'login-partitions.data.json')) $prepEnv
        Invoke-NewmanRun '02-ddt-checkout' @('--folder','2.1 Domain partitions [DDT]','-d',(Join-Path $dataDir 'checkout-partitions.data.json')) $prepEnv

        # Recreate a clean cart/order for the transition matrix.  The setup
        # folder alone cannot provide orderId; API-2 must run first.
        $statusPrepEnv = Join-Path $out ('.ddt-status-prep-' + $PID + '.json')
        Invoke-NewmanRun '00-ddt-status-prep' @('--folder','00 - Setup','--folder','API-2 - POST /api/checkout','--export-environment',$statusPrepEnv)
        Invoke-NewmanRun '03-ddt-order-status' @('--folder','3.1 Transition matrix [DDT]','-d',(Join-Path $dataDir 'order-status-matrix.data.json')) $statusPrepEnv
    } finally {
        foreach ($tempPath in @($prepEnv, (Join-Path $out ('.ddt-status-prep-' + $PID + '.json')))) {
            if (Test-Path -LiteralPath $tempPath) { Remove-Item -LiteralPath $tempPath -Force }
        }
    }
} else {
    Invoke-NewmanRun $ReportName @()
}

if (($script:runExitCodes | Where-Object { $_ -ne 0 }).Count -gt 0) { exit 1 }
exit 0
