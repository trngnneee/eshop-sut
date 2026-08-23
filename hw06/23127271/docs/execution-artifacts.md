# Stage 4 — Execution artifacts

**Student:** 23127271 · **SUT:** EShop `http://localhost:3000` · **APIs:** FR-04, FR-07, FR-19

## Deliverables

| Artifact | Path | Count |
|----------|------|------:|
| Combined CSV | `sheets/all-test-cases.csv` | 280 |
| Excel workbook | `sheets/all-test-cases.xlsx` | 280 (+ Summary tab) |
| Postman collection | `postman/eshop-hw06.postman_collection.json` | 280 TC folders + Setup |
| Postman environment | `postman/eshop-hw06.postman_environment.json` | local vars |

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

## How to run

### Postman GUI
1. Import `postman/eshop-hw06.postman_collection.json` and `postman/eshop-hw06.postman_environment.json`
2. Select environment **eshop-hw06-local**
3. Run folder **00 — Setup (run first)**
4. Run FR/category folders or individual TC folders

### Newman (Stage 5)
```bash
# Setup only
newman run postman/eshop-hw06.postman_collection.json -e postman/eshop-hw06.postman_environment.json --folder "00 — Setup (run first)"

# Full collection (long — 280 cases; SUT must be running)
newman run postman/eshop-hw06.postman_collection.json -e postman/eshop-hw06.postman_environment.json -r cli,htmlextra --reporter-htmlextra-export reports/newman-report.html
```

**Note:** Concurrency / parallel probes are marked in request descriptions — run those manually or with multiple Newman workers. Observe-only oracles require human pass/fail against ExpectedResult in the Excel sheet.
