$STUDENT_ID = "23127486"
$BASE_URL = "http://localhost:3000"
$ENV_FILE = "postman\hw06_environment.json"
$REPORT_DIR = "newman_reports"

New-Item -ItemType Directory -Force -Path $REPORT_DIR | Out-Null

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  RUNNING DATA-DRIVEN TEST SUITES FOR HW06" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. API 1 Data-Driven
Write-Host "`n>>> [1/3] Running Data-Driven API 1 (POST /api/register)..." -ForegroundColor Yellow
npx newman run "postman\hw06_api1_datadriven_collection.json" `
  --environment $ENV_FILE `
  --iteration-data "postman\data_driven\api1_data.json" `
  --env-var "studentId=$STUDENT_ID" `
  --env-var "baseUrl=$BASE_URL" `
  --reporters cli,htmlextra `
  --reporter-htmlextra-export "$REPORT_DIR\datadriven_api1_report.html" `
  --reporter-htmlextra-title "HW06 Data-Driven API1 – Phan Quoc Thinh – $STUDENT_ID"

# 2. API 2 Data-Driven
Write-Host "`n>>> [2/3] Running Data-Driven API 2 (GET /api/orders/my-orders)..." -ForegroundColor Yellow
npx newman run "postman\hw06_api2_datadriven_collection.json" `
  --environment $ENV_FILE `
  --iteration-data "postman\data_driven\api2_data.json" `
  --env-var "studentId=$STUDENT_ID" `
  --env-var "baseUrl=$BASE_URL" `
  --reporters cli,htmlextra `
  --reporter-htmlextra-export "$REPORT_DIR\datadriven_api2_report.html" `
  --reporter-htmlextra-title "HW06 Data-Driven API2 – Phan Quoc Thinh – $STUDENT_ID"

# 3. API 3 Data-Driven
Write-Host "`n>>> [3/3] Running Data-Driven API 3 (POST /api/admin/import-products)..." -ForegroundColor Yellow
npx newman run "postman\hw06_api3_datadriven_collection.json" `
  --environment $ENV_FILE `
  --iteration-data "postman\data_driven\api3_data.json" `
  --env-var "studentId=$STUDENT_ID" `
  --env-var "baseUrl=$BASE_URL" `
  --reporters cli,htmlextra `
  --reporter-htmlextra-export "$REPORT_DIR\datadriven_api3_report.html" `
  --reporter-htmlextra-title "HW06 Data-Driven API3 – Phan Quoc Thinh – $STUDENT_ID"

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "  ALL DATA-DRIVEN TEST RUNS COMPLETED!" -ForegroundColor Green
Write-Host "  Reports generated in: $REPORT_DIR\datadriven_api*.html" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
