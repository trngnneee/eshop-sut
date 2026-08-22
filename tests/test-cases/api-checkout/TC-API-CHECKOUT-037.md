# TC-API-CHECKOUT-037

- Requirement: `FR-08/FR-10/SEC-02/SEC-04`
- Group/technique: Extension / Flow/security
- Preconditions: Có giỏ chứa sản phẩm 30 triệu; gửi total_amount=1
- Method/data: `POST /api/checkout` + chained endpoint; Dùng tổng giả trong body
- Expected: Đơn phải có tổng tính từ giỏ, không phải 1
- Result: FAIL — defect expected
- Related Bug: [#418](https://github.com/trngnneee/eshop-sut/issues/418) (`D-CHK-01`)

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
