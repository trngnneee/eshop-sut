# TC-API-CHECKOUT-041

- Requirement: `FR-08/FR-10/SEC-02/SEC-04`
- Group/technique: Extension / Flow/security
- Preconditions: User A tạo order; request không token hoặc user B GET /api/orders/:id
- Method/data: `POST /api/checkout` + chained endpoint; IDOR khi đọc order
- Expected: 401/403; không lộ order A
- Result: FAIL — defect expected
- Related Bug: `D-CHK-07`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
