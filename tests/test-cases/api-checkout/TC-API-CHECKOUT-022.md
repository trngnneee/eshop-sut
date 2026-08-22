# TC-API-CHECKOUT-022

- Requirement: `FR-08/FR-10`
- Group/technique: State / State-transition
- Preconditions: User có JWT; không thêm sản phẩm
- Method/data: `POST /api/checkout`; Body total_amount=1
- Expected: 400; không tạo đơn
- Result: FAIL — defect expected
- Related Bug: `D-CHK-04`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
