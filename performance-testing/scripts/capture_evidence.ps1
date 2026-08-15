<#
.SYNOPSIS
    Chup man hinh toan bo desktop vao dung duong dan bang chung cua HW05.

.DESCRIPTION
    Thay cho Win+PrtScn (luu file ten ngau nhien vao Pictures\Screenshots roi phai
    tu doi ten). Script dem nguoc vai giay de nguoi dung kip sap xep cua so, roi
    chup toan man hinh va ghi thang vao performance-testing\evidence\<...>.png

.EXAMPLE
    .\capture_evidence.ps1 -Name jmeter+taskmgr-load -Scenario load -Delay 5
    .\capture_evidence.ps1 -Name listener-stress -Scenario stress
    .\capture_evidence.ps1 -Name dxdiag -Scenario hardware -Delay 3
    .\capture_evidence.ps1 -Name github-issues-list -Scenario issues
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$Name,

    [Parameter(Mandatory = $true)]
    [ValidateSet("load", "stress", "spike", "endurance", "hardware", "issues")]
    [string]$Scenario,

    [int]$Delay = 5
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ptDir     = Split-Path -Parent $scriptDir
$outDir    = Join-Path $ptDir "evidence\$Scenario"

if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}

$outFile = Join-Path $outDir "$Name.png"

if (Test-Path $outFile) {
    Write-Host "[!] File da ton tai va se bi ghi de: $outFile" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  Se chup TOAN BO man hinh sau $Delay giay." -ForegroundColor Cyan
Write-Host "  Hay sap xep cua so ngay bay gio (JMeter ben trai, Task Manager ben phai)." -ForegroundColor Cyan
Write-Host ""

for ($i = $Delay; $i -gt 0; $i--) {
    Write-Host "  $i..." -NoNewline -ForegroundColor Yellow
    Start-Sleep -Seconds 1
}
Write-Host ""

# Chup toan bo vung ao phu het cac man hinh dang gan
$bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
$bmp    = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
$gfx    = [System.Drawing.Graphics]::FromImage($bmp)

try {
    $gfx.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $bmp.Save($outFile, [System.Drawing.Imaging.ImageFormat]::Png)
}
finally {
    $gfx.Dispose()
    $bmp.Dispose()
}

$sizeKb = [math]::Round((Get-Item $outFile).Length / 1KB, 1)
Write-Host ""
Write-Host "  [OK] Da luu: $outFile" -ForegroundColor Green
Write-Host "       Kich thuoc: $($bounds.Width)x$($bounds.Height) px, $sizeKb KB" -ForegroundColor Green
Write-Host ""
Write-Host "  Mo lai de kiem tra chu co doc duoc khong:" -ForegroundColor DarkGray
Write-Host "    Start-Process '$outFile'" -ForegroundColor DarkGray
Write-Host ""
