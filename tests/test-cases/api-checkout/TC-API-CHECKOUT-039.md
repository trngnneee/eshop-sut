# TC-API-CHECKOUT-039

- Requirement: `FR-08/FR-10/SEC-02/SEC-04`
- Group/technique: Extension / Flow/security
- Preconditions: Checkout thành công rồi GET /api/cart
- Method/data: `POST /api/checkout` + chained endpoint; Hậu điều kiện xóa giỏ
- Expected: Response là []; không còn item cũ
- Result: FAIL — defect expected
- Related Bug: `D-CHK-03`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
