$STUDENT_ID = "23127486"
$BASE_URL = "http://localhost:3000"
$COLLECTION = "postman\hw06_api1_collection.json"
$ENV_FILE = "postman\hw06_environment.json"
$REPORT_DIR = "newman_reports"

New-Item -ItemType Directory -Force -Path $REPORT_DIR | Out-Null

npx newman run $COLLECTION `
  --environment $ENV_FILE `
  --env-var "studentId=$STUDENT_ID" `
  --env-var "baseUrl=$BASE_URL" `
  --reporters cli,htmlextra `
  --reporter-htmlextra-export "$REPORT_DIR\newman_api1_report.html" `
  --reporter-htmlextra-title "HW06 API1 – Phan Quoc Thinh – $STUDENT_ID"
