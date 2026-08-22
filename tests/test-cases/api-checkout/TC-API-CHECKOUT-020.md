# TC-API-CHECKOUT-020

- Requirement: `FR-08/FR-10`
- Group/technique: State / State/post-condition
- Preconditions: User có JWT; giỏ có sản phẩm
- Method/data: `POST /api/checkout`; Checkout rồi GET /api/cart
- Expected: Giỏ rỗng sau checkout thành công
- Result: FAIL — defect expected
- Related Bug: [#420](https://github.com/trngnneee/eshop-sut/issues/420) (`D-CHK-03`)

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
