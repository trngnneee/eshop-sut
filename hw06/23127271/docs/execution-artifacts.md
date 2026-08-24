# Stage 4 — Execution artifacts

**Student:** 23127271 · **SUT:** EShop `http://localhost:3000` · **APIs:** FR-04, FR-07, FR-19

## Deliverables

| Artifact | Path | Count |
|----------|------|------:|
| Combined CSV | `sheets/all-test-cases.csv` | 280 |
| Excel workbook | `sheets/all-test-cases.xlsx` | 280 (+ Summary tab) |
| Postman collection | `postman/eshop-hw06.postman_collection.json` | 280 TC folders + Setup + **Data-driven** |
| Postman environment | `postman/eshop-hw06.postman_environment.json` | local vars |
| **Data file (Runner)** | `postman/runner-data-profile-phone.csv` | 5 phone partitions |

### Combined totals by category

| Category | Cases |
|----------|------:|
| DomainPartition | 114 |
| StateTransition | 57 |
| Security | 52 |
| SchemaValidation | 57 |
| **Total** | **280** |

## Postman features used

- **Collection variables** — `baseUrl`, `studentId`, `userToken`, `adminToken`, `userSelfId`, `adminSelfId`, `disposableUserId`
- **Environment file** — local overrides for base URL and tokens
- **Collection pre-request script** — injects `X-Student-Id` on every request
- **Setup folder** — login user/admin, capture ids, register disposable user
- **Nested folders** — FR → category → test case → step requests
- **Test scripts** — observe-only oracles (status recorded, no invented HTTP codes)
- **Dynamic variables** — `{{$timestamp}}` for unique register emails
- **Collection Runner data file** — `postman/runner-data-profile-phone.csv` drives folder **`99 — Data-driven Runner (CSV)`** (5 FR-04 phone partitions via `{{test_phone}}`)

See [`docs/data-driven-runner.md`](data-driven-runner.md) for GUI and Newman `-d` usage.

## How to run

### Postman GUI
1. Import `postman/eshop-hw06.postman_collection.json` and `postman/eshop-hw06.postman_environment.json`
2. Select environment **eshop-hw06-local**
3. Run folder **00 — Setup (run first)**
4. Run FR/category folders or individual TC folders
5. **Data-driven phone probe:** Run folder **`99 — Data-driven Runner (CSV)`** with data file `postman/runner-data-profile-phone.csv`

### Newman (Stage 5)
```bash
# Setup only
newman run postman/eshop-hw06.postman_collection.json -e postman/eshop-hw06.postman_environment.json --folder "00 — Setup (run first)"

# Data-driven FR-04 phone partitions (5 CSV rows)
newman run postman/eshop-hw06.postman_collection.json --folder "99 — Data-driven Runner (CSV)" -d postman/runner-data-profile-phone.csv -r cli

# Full collection (long — 280 cases; SUT must be running)
newman run postman/eshop-hw06.postman_collection.json -e postman/eshop-hw06.postman_environment.json -r cli,htmlextra --reporter-htmlextra-export reports/newman-report.html
```

**Note:** Concurrency / parallel probes are marked in request descriptions — run those manually or with multiple Newman workers. Observe-only oracles require human pass/fail against ExpectedResult in the Excel sheet.

## CI/CD (GitHub Actions)

| Item | Path |
|------|------|
| Workflow | `.github/workflows/hw06-api-tests.yml` (repo root) |
| CI demo folder | `CI — HW06 pipeline demo` (2 requests, strict assertions) |
| CI reports | `reports/newman-ci-report.html`, `reports/newman-ci.log` |
| Report doc | [`docs/cicd-report.md`](cicd-report.md) |
| Screenshots | `evidence/cicd/run-pass.png`, `run-fail.png` |

**CI Newman** (no `-e` env file):

```bash
newman run hw06/23127271/postman/eshop-hw06.postman_collection.json \
  --folder "CI — HW06 pipeline demo" \
  -r cli,htmlextra \
  --reporter-htmlextra-export hw06/23127271/reports/newman-ci-report.html
```

- **Pass run:** collection variable `ciFailDemo=false`
- **Fail demo:** `ciFailDemo=true` → exactly 1 failure (`INTENTIONAL CI FAIL DEMO`)

Full 280 TC suite remains a **local** artifact; CI runs the demo folder only for fast, clear pass/fail evidence.
