# TC-API-CHECKOUT-038

- Requirement: `FR-08/FR-10/SEC-02/SEC-04`
- Group/technique: Extension / Flow/security
- Preconditions: Có JWT và giỏ có sản phẩm; gửi total_amount=-500000
- Method/data: `POST /api/checkout` + chained endpoint; Biên total_amount âm
- Expected: 400; không tạo đơn
- Result: FAIL — defect expected
- Related Bug: [#419](https://github.com/trngnneee/eshop-sut/issues/419) (`D-CHK-02`)

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
