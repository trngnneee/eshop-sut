# TC-API-CHECKOUT-040

- Requirement: `FR-08/FR-10/SEC-02/SEC-04`
- Group/technique: Extension / Flow/security
- Preconditions: Không thêm item; gọi checkout
- Method/data: `POST /api/checkout` + chained endpoint; Giỏ rỗng không thể thanh toán
- Expected: 400; không tạo order
- Result: FAIL — defect expected
- Related Bug: [#421](https://github.com/trngnneee/eshop-sut/issues/421) (`D-CHK-04`)

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
