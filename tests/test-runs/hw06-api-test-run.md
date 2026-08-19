# HW06 API test run

| Suite | Iterations | Requests | Assertions | Failed | Result |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `00-off-suite` | 1 | 19 | 18 | 0 | PASS |
| `00-canary-suite` | 1 | 19 | 19 | 1 | FAIL (expected defect/oracle mismatch) |
| `00-full-suite` | 1 | 19 | 26 | 8 | FAIL (expected defect/oracle mismatch) |
| `01-ddt-login` | 16 | 16 | 16 | 0 | PASS |
| `02-ddt-checkout` | 18 | 18 | 18 | 0 | PASS |
| `03-ddt-order-status` | 25 | 25 | 25 | 7 | FAIL (expected defect/oracle mismatch) |

## Failure mapping

- Canary: `TC-API-LOGIN-018` → D-LOGIN-01.
- Full: D-LOGIN-08, D-LOGIN-03, D-CHK-07, D-CHK-03, D-CHK-02, D-ADM-01, D-ADM-02 (see `report/bug-report.md`).
- Status DDT: 7 matrix cells expose implementation/oracle divergence; each row has `tc_id` and expected status in `postman/data/order-status-matrix.data.json`.

All request logs use `X-Student-Id: 23127207`; reports are in `hw06/newman/reports/`.
