# TC-API-CHECKOUT-042

- Requirement: `FR-08/FR-10/SEC-02/SEC-04`
- Group/technique: Extension / Flow/security
- Preconditions: Địa chỉ là <img src=x onerror=alert(1)>; đọc lại order
- Method/data: `POST /api/checkout` + chained endpoint; XSS trong shipping_address
- Expected: Payload bị reject hoặc escape, không lưu raw
- Result: FAIL — defect expected
- Related Bug: `D-CHK-05`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
