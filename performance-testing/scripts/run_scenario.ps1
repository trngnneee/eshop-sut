param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("Load", "Stress", "Spike", "Endurance", "load", "stress", "spike", "endurance")]
    [string]$Scenario,

    [string]$RunDate = (Get-Date -Format "yyyyMMdd"),

    [switch]$SkipReset
)

$ErrorActionPreference = "Stop"

# Capitalize scenario name
$scenName = (Get-Culture).TextInfo.ToTitleCase($Scenario.ToLower())
$scenLower = $scenName.ToLower()

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ptDir     = Split-Path -Parent $scriptDir
$rootDir   = Split-Path -Parent $ptDir

$testPlanName = "23127207_${scenName}_${RunDate}"
$jmxPath      = Join-Path $ptDir "test-plans\$testPlanName.jmx"
$outDir       = Join-Path $ptDir "results\$scenLower"
$jtlPath      = Join-Path $outDir "$testPlanName.jtl"
$jmeterLog    = Join-Path $outDir "$testPlanName.jmeter.log"
$htmlReport   = Join-Path $outDir "html-report"
$userProps    = Join-Path $scriptDir "jmeter-user.properties"
$dataDir      = Join-Path $ptDir "data"
$resourceCsv  = Join-Path $outDir "resource-$scenLower.csv"

# Locate JMeter binary
$jmeterBat = Join-Path $rootDir ".tools\jmeter\bin\jmeter.bat"
if (-not (Test-Path $jmeterBat)) {
    # Check if jmeter is in PATH or msi dir
    $cmd = Get-Command "jmeter.bat" -ErrorAction SilentlyContinue
    if ($cmd) {
        $jmeterBat = $cmd.Source
    } else {
        $candidate = Get-ChildItem -Path (Join-Path $rootDir ".tools") -Filter "jmeter.bat" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($candidate) {
            $jmeterBat = $candidate.FullName
        }
    }
}

if (-not (Test-Path $jmeterBat)) {
    Write-Error "[run_scenario] JMeter executable not found at $jmeterBat"
}

Write-Host "=========================================================="
Write-Host "   RUNNING PERFORMANCE SCENARIO: $scenName"
Write-Host "   Plan: $testPlanName.jmx"
Write-Host "   JMeter: $jmeterBat"
Write-Host "=========================================================="

# 1. Cleanly restart backend & redirect stderr for diagnostic trace
Write-Host "[1/7] Preparing results directory: $outDir"
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }

Write-Host "[1/7] Cleaning up existing node processes and port 3000..."
Get-Process -Name "node" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

$stderrFile = Join-Path $outDir "backend-stderr.log"
if (Test-Path $stderrFile) { Remove-Item -Force $stderrFile }

Write-Host "[1/7] Starting fresh backend server (logging stderr to $stderrFile)..."
$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = "node"
$startInfo.Arguments = "backend/server.js"
$startInfo.WorkingDirectory = $rootDir
$startInfo.RedirectStandardError = $true
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true

$backendProcess = New-Object System.Diagnostics.Process
$backendProcess.StartInfo = $startInfo
$backendProcess.Start() | Out-Null
$startedBackend = $backendProcess

# Background thread to capture stderr to file
$stderrTask = [System.Threading.Tasks.Task]::Run([Action]{
    $reader = $backendProcess.StandardError
    $writer = [System.IO.File]::CreateText($stderrFile)
    while (-not $reader.EndOfStream) {
        $line = $reader.ReadLine()
        $writer.WriteLine($line)
        $writer.Flush()
    }
    $writer.Close()
})

$retries = 15
$hc = $null
while ($retries -gt 0 -and $null -eq $hc) {
    Start-Sleep -Seconds 1
    try {
        $hc = Invoke-RestMethod -Uri "http://localhost:3000/api/products" -Method Get -TimeoutSec 3
    } catch {
        $retries--
    }
}

if ($null -eq $hc) {
    Write-Error "[1/7] Failed to start fresh backend server! Stderr: $(Get-Content $stderrFile -Raw -ErrorAction SilentlyContinue)"
}

Write-Host "[1/7] Seeding clean performance dataset (400 users, 500 products)..."
& node (Join-Path $scriptDir "seed_perf_data.js")
Start-Sleep -Seconds 1
$hc = Invoke-RestMethod -Uri "http://localhost:3000/api/products" -Method Get -TimeoutSec 5
Write-Host "[1/7] Backend started cleanly. Products in catalog: $($hc.Count)"

# 2. Reset lockout
$resetTimestamp = "SKIPPED"
if (-not $SkipReset) {
    Write-Host "[2/7] Resetting account lockouts..."
    $resetOutput = & node (Join-Path $scriptDir "reset_lockout.js")
    Write-Host $resetOutput
    $resetTimestamp = (Get-Date).ToString("o")
} else {
    Write-Host "[2/7] Skipping lockout reset as requested."
}

# 3. Prepare output directory
Write-Host "[3/7] Preparing results directory: $outDir"
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
}
# Clear previous HTML report folder if exists (JMeter requires empty or non-existent dir)
if (Test-Path $htmlReport) {
    Remove-Item -Recurse -Force $htmlReport
}
if (Test-Path $jtlPath) {
    Remove-Item -Force $jtlPath
}

# 4. Start resource monitor in background job
Write-Host "[4/7] Starting background resource monitor..."
$monitorJob = Start-Job -ScriptBlock {
    param($monScript, $scen, $outFile)
    & powershell.exe -ExecutionPolicy Bypass -File $monScript -Scenario $scen -IntervalSec 2 -OutFile $outFile
} -ArgumentList (Join-Path $scriptDir "monitor_backend.ps1"), $scenName, $resourceCsv

$testStart = Get-Date

try {
    # 5. Run JMeter non-GUI
    Write-Host "[5/7] Executing JMeter Non-GUI test plan..."
    $jmeterArgs = @(
        "-n",
        "-t", $jmxPath,
        "-l", $jtlPath,
        "-j", $jmeterLog,
        "-q", $userProps,
        "-Jcsvdir=$dataDir",
        "-e",
        "-o", $htmlReport
    )

    Write-Host "Running: & '$jmeterBat' $($jmeterArgs -join ' ')"
    & "$jmeterBat" @jmeterArgs
    
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "[5/7] JMeter exited with non-zero exit code: $LASTEXITCODE"
    } else {
        Write-Host "[5/7] JMeter test completed successfully."
    }
} finally {
    $testEnd = Get-Date
    # 6. Stop and remove monitor job & started backend
    Write-Host "[6/7] Stopping background resource monitor..."
    Stop-Job -Job $monitorJob -ErrorAction SilentlyContinue | Out-Null
    Remove-Job -Job $monitorJob -ErrorAction SilentlyContinue | Out-Null

    if ($startedBackend) {
        Write-Host "[6/7] Stopping auto-started backend process..."
        Stop-Process -Id $startedBackend.Id -Force -ErrorAction SilentlyContinue
    }
}

# 7. Analyze JTL and generate summaries
Write-Host "[7/7] Generating summary.json and summary.md with analyze_jtl.py..."
$sliceSec = 60
if ($scenName -eq "Stress" -or $scenName -eq "Endurance") {
    $sliceSec = 120
}

$analyzeScript = Join-Path $scriptDir "analyze_jtl.py"
& python $analyzeScript --jtl $jtlPath --out-dir $outDir --scenario $scenName --slice-sec $sliceSec --resource-csv $resourceCsv

Write-Host "=========================================================="
Write-Host "   EXECUTION FINISHED: $scenName"
Write-Host "   Start Time: $($testStart.ToString('yyyy-MM-dd HH:mm:ss'))"
Write-Host "   End Time:   $($testEnd.ToString('yyyy-MM-dd HH:mm:ss'))"
Write-Host "   Reset TS:   $resetTimestamp"
Write-Host "   JTL Output: $jtlPath"
Write-Host "   HTML Dashboard: $htmlReport\index.html"
Write-Host "   Resource Log: $resourceCsv"
Write-Host "=========================================================="
