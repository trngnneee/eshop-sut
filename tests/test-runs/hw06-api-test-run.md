# HW06 API test run

| Suite | Iterations | Requests | Assertions | Failed | Result |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `00-off-suite` | 1 | 19 | 18 | 0 | PASS |
| `00-canary-suite` | 1 | 19 | 19 | 1 | FAIL (expected defect/oracle mismatch) |
| `00-full-suite` | 1 | 19 | 26 | 8 | FAIL (expected defect/oracle mismatch) |
| `01-ddt-login` | 39 | 89 | 39 | 23 | FAIL (expected defect/oracle mismatch) |
| `02-ddt-checkout` | 41 | 178 | 41 | 17 | FAIL (expected defect/oracle mismatch) |
| `03-ddt-order-status` | 43 | 127 | 43 | 7 | FAIL (expected defect/oracle mismatch) |

## Failure mapping

- Canary: `TC-API-LOGIN-018` → D-LOGIN-01; Newman JSON có đúng 1 failed assertion.
- Full probe: xem từng assertion TC ID trong `00-full-suite.json` và `report/bug-report.md`.
- DDT: expected giữ theo đặc tả; các failed assertion là chênh lệch oracle/SUT, không phải lỗi request hoặc test script.
- Đối soát 128 TC ID: `hw06/newman/reports/execution-coverage.md`.

All request logs use `X-Student-Id: 23127207`; reports are in `hw06/newman/reports/`.
