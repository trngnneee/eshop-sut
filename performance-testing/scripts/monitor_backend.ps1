param (
    [Parameter(Mandatory=$true)]
    [string]$Scenario,

    [int]$IntervalSec = 2,

    [string]$OutFile = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrEmpty($OutFile)) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $rootDir = Split-Path -Parent $scriptDir
    $resultsDir = Join-Path $rootDir "results\$($Scenario.ToLower())"
    if (-not (Test-Path $resultsDir)) {
        New-Item -ItemType Directory -Force -Path $resultsDir | Out-Null
    }
    $OutFile = Join-Path $resultsDir "resource-$($Scenario.ToLower()).csv"
}

$numCores = [Environment]::ProcessorCount

Write-Host "[monitor] Starting backend resource monitor for Scenario: $Scenario (Interval: ${IntervalSec}s)"
Write-Host "[monitor] Output file: $OutFile"

# Header
"timestamp,elapsed_sec,pid,cpu_percent,working_set_mb,private_mb,handles,threads" | Out-File -Encoding utf8 -FilePath $OutFile

$startTime = Get-Date
$prevCpuTime = $null
$prevTime = $null

try {
    while ($true) {
        $now = Get-Date
        $elapsedSec = [math]::Round(($now - $startTime).TotalSeconds, 1)
        
        # Find node server process
        $nodeProc = Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object {
            try {
                $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)" -ErrorAction SilentlyContinue).CommandLine
                $cmd -like "*server.js*"
            } catch {
                $false
            }
        } | Select-Object -First 1

        if ($nodeProc) {
            $curCpuTime = $nodeProc.TotalProcessorTime.TotalSeconds
            $curTime = $now
            
            $cpuPercent = 0.0
            if ($prevCpuTime -ne $null -and $prevTime -ne $null) {
                $timeDelta = ($curTime - $prevTime).TotalSeconds
                $cpuDelta = $curCpuTime - $prevCpuTime
                if ($timeDelta -gt 0) {
                    $cpuPercent = [math]::Round(($cpuDelta / ($timeDelta * $numCores)) * 100, 2)
                    if ($cpuPercent -lt 0) { $cpuPercent = 0.0 }
                }
            }
            $prevCpuTime = $curCpuTime
            $prevTime = $curTime

            $wsMb = [math]::Round($nodeProc.WorkingSet64 / 1MB, 2)
            $pmMb = [math]::Round($nodeProc.PrivateMemorySize64 / 1MB, 2)
            $handles = $nodeProc.HandleCount
            $threads = $nodeProc.Threads.Count

            $tsIso = $now.ToString("yyyy-MM-ddTHH:mm:ss.fff")
            $line = "$tsIso,$elapsedSec,$($nodeProc.Id),$cpuPercent,$wsMb,$pmMb,$handles,$threads"
            $line | Out-File -Encoding utf8 -Append -FilePath $OutFile
        } else {
            # In case backend was temporarily unavailable
            $tsIso = $now.ToString("yyyy-MM-ddTHH:mm:ss.fff")
            "$tsIso,$elapsedSec,-1,0.0,0.0,0.0,0,0" | Out-File -Encoding utf8 -Append -FilePath $OutFile
        }

        Start-Sleep -Seconds $IntervalSec
    }
} finally {
    Write-Host "[monitor] Resource monitor stopped."
}
