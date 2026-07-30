# Task 1 GUI Checklist Deliverables Validator
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BaseDir = Resolve-Path "$ScriptDir\.."

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "     Task 1 GUI Completion Validator      " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$passed = $true
$issues = @()

# 1. Check Mandatory Files
$files = @(
    "README.md",
    "scope-analysis.md",
    "GUI_Checklist_HW3.md",
    "GUI_Checklist_HW3.xlsx",
    "GUI_Coverage_Matrix.md",
    "GUI_Bug_Report_HW3.md",
    "GUI_Test_Summary_HW3.md",
    "AI_Item_Level_Critique.md",
    "AI_Critique_Task1.md",
    "AI_Audit_Report_Task1.md",
    "AI_Disclosure_Task1.md",
    "git-commit-log.txt",
    "ai-output\AI_INITIAL_GUI_Checklist.md"
)

foreach ($f in $files) {
    $fullPath = Join-Path $BaseDir $f
    if (-not (Test-Path $fullPath)) {
        $passed = $false
        $issues += "Missing file: $f"
    } else {
        Write-Host "[OK] Found $f" -ForegroundColor Green
    }
}

# 2. Check Evidence Files
$evidenceFiles = @(
    "evidence\web-login\BUG-GUI-01_web-login.png",
    "evidence\web-register\BUG-GUI-02_web-register.png",
    "evidence\admin-login\BUG-GUI-03_admin-login.png",
    "evidence\admin-category\BUG-GUI-04_admin-category.png",
    "evidence\mobile-login\BUG-GUI-05_mobile-login.png"
)

foreach ($ef in $evidenceFiles) {
    $fullPath = Join-Path $BaseDir $ef
    if (-not (Test-Path $fullPath)) {
        $passed = $false
        $issues += "Missing evidence screenshot: $ef"
    } else {
        Write-Host "[OK] Found evidence $ef" -ForegroundColor Green
    }
}

# 3. Check Checklist Items Count
$mdChecklist = Get-Content (Join-Path $BaseDir "GUI_Checklist_HW3.md") -Raw
$itemLines = ($mdChecklist -split "`n") | Where-Object { $_ -match "^\| GUI-" }
if ($itemLines.Count -lt 41) {
    $passed = $false
    $issues += "Checklist item count $($itemLines.Count) is less than required 41 items."
} else {
    Write-Host "[OK] Checklist item count: $($itemLines.Count) (>= 41)" -ForegroundColor Green
}

# 4. Check GitHub Issues Traceability
$bugsReport = Get-Content (Join-Path $BaseDir "GUI_Bug_Report_HW3.md") -Raw
if ($bugsReport -match "PENDING_EXTERNAL_ACTION") {
    Write-Host "[INFO] GitHub issues status is PENDING_EXTERNAL_ACTION (Pending manual student post)." -ForegroundColor Yellow
}

Write-Host "------------------------------------------" -ForegroundColor Cyan
if ($passed -and (-not ($bugsReport -match "PENDING_EXTERNAL_ACTION"))) {
    Write-Host "FINAL STATUS: COMPLETE" -ForegroundColor Green
} else {
    Write-Host "FINAL STATUS: INCOMPLETE" -ForegroundColor Yellow
    Write-Host "Reason / Action Required:" -ForegroundColor Yellow
    Write-Host "1. Manual student action needed: Post bugs to GitHub repository if URL assignment is needed." -ForegroundColor Yellow
    foreach ($iss in $issues) {
        Write-Host " - $iss" -ForegroundColor Red
    }
}
