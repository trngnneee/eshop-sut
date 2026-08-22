# API Testing Output

Generated test cases for selected EShop APIs.

| API slug | Method + endpoint | Related requirement | DomainPartition | StateTransition | Security | SchemaValidation | Total | Last run |
|---|---|---|---:|---:|---:|---:|---:|---|
| forgot-password | `POST /api/forgot-password` | FR-03 | 14 | 9 | 15 | 7 | 45 | Sun 08/23/2026 Asia/Saigon |
| apply-coupon | `POST /api/apply-coupon` | FR-09 | 17 | 8 | 10 | 7 | 42 | Sun 08/23/2026 01:13 Asia/Saigon |
| admin-coupons | `POST /api/admin/coupons`, `DELETE /api/admin/coupons/:id` | FR-17 | 15 | 8 | 11 | 8 | 42 | Sun 08/23/2026 02:15 Asia/Saigon |

## Files

- `specs/api_specification.md`: copied API specification used for generation.
- `forgot-password/01_domain_partitions.json`: Stage 1 output.
- `forgot-password/02_state_transitions.json`: Stage 2 output.
- `forgot-password/03_security.json`: Stage 3 output.
- `forgot-password/04_schema_validation.json`: Stage 4 output.
- `forgot-password/test_cases_master.csv`: consolidated CSV for Excel.
- `forgot-password/ai_audit_log.md`: AI audit log for the generation pipeline.
- `apply-coupon/01_domain_partitions.json`: Stage 1 output.
- `apply-coupon/02_state_transitions.json`: Stage 2 output.
- `apply-coupon/03_security.json`: Stage 3 output.
- `apply-coupon/04_schema_validation.json`: Stage 4 output.
- `apply-coupon/test_cases_master.csv`: consolidated CSV for Excel.
- `apply-coupon/ai_audit_log.md`: AI audit log for the generation pipeline.
- `admin-coupons/01_domain_partitions.json`: Stage 1 output.
- `admin-coupons/02_state_transitions.json`: Stage 2 output.
- `admin-coupons/03_security.json`: Stage 3 output.
- `admin-coupons/04_schema_validation.json`: Stage 4 output.
- `admin-coupons/test_cases_master.csv`: consolidated CSV for Excel.
- `admin-coupons/ai_audit_log.md`: AI audit log for the generation pipeline.
- `forgot_password.postman_collection.json`: dedicated FR-03 collection with one request per test case plus deeper per-test-case assertions and OTP/reset-password flows.
- `apply_coupon.postman_collection.json`: Postman collection for FR-09 only.
- `admin_coupons.postman_collection.json`: Postman collection for FR-17 only.
- `eshop_api.postman_collection.json`: combined data-driven Postman collection for all selected APIs.
- `build_forgot_password_collection.js`: helper script to regenerate the dedicated FR-03 collection from `data/forgot-password.test-data.json`.
- `data/test-data.json`: combined data-driven test case records used by Newman/Postman Collection Runner.
- `data/forgot-password.test-data.json`: split data file for FR-03 forgot-password records.
- `data/apply-coupon.test-data.json`: split data file for FR-09 apply-coupon records.
- `data/admin-coupons.test-data.json`: split data file for FR-17 admin-coupons records.
- `data/apply_coupon_data.csv`: legacy small iteration data file for the apply-coupon demo case.

## Postman / Newman

Primary data-driven flow:

```text
data/test-data.json
  -> eshop_api.postman_collection.json
  -> one iteration per test case record
  -> dynamic request method/path/body/headers
  -> pre-request login only when a row needs adminToken/userToken
  -> assertions from expectedStatus and response contract
  -> Newman HTML report
```

Split data files for easier review:

```text
data/forgot-password.test-data.json
data/apply-coupon.test-data.json
data/admin-coupons.test-data.json
```

Run the primary data-driven collection:

```powershell
newman run API-testing/eshop_api.postman_collection.json -e API-testing/eshop_api.postman_environment.json --iteration-data API-testing/data/test-data.json -r cli,html --reporter-html-export API-testing/newman-eshop-api-report.html
```

Run one API data file:

```powershell
newman run API-testing/eshop_api.postman_collection.json -e API-testing/eshop_api.postman_environment.json --iteration-data API-testing/data/forgot-password.test-data.json -r cli,html --reporter-html-export API-testing/newman-forgot-password-report.html
```

Run the dedicated forgot-password deep assertion collection:

```powershell
newman run API-testing/forgot_password.postman_collection.json -e API-testing/eshop_api.postman_environment.json -r cli,html --reporter-html-export API-testing/newman-forgot-password-deep-report.html
```

```powershell
newman run API-testing/eshop_api.postman_collection.json -e API-testing/eshop_api.postman_environment.json --iteration-data API-testing/data/apply-coupon.test-data.json -r cli,html --reporter-html-export API-testing/newman-apply-coupon-report.html
```

```powershell
newman run API-testing/eshop_api.postman_collection.json -e API-testing/eshop_api.postman_environment.json --iteration-data API-testing/data/admin-coupons.test-data.json -r cli,html --reporter-html-export API-testing/newman-admin-coupons-report.html
```

Small apply-coupon data-driven demo:

In Postman Collection Runner, select `FR-09 Apply Coupon > domain partitions > DP-DD - Áp dụng coupon bằng iteration data`, then choose `data/apply_coupon_data.csv` as the data file.

Newman can run with the same data file, but folder-level selection will run every request in the selected folder for each iteration. Prefer the Postman Runner for this single data-driven test case.

```powershell
newman run API-testing/apply_coupon.postman_collection.json -e API-testing/eshop_api.postman_environment.json --iteration-data API-testing/data/apply_coupon_data.csv -r cli,html --reporter-html-export API-testing/newman-apply-coupon-report.html
```
