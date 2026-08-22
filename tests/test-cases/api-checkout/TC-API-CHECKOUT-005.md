# TC-API-CHECKOUT-005

- Requirement: `FR-08/FR-10`
- Group/technique: Partition / BVA
- Preconditions: User có JWT; giỏ có sản phẩm
- Method/data: `POST /api/checkout`; total_amount=0; shipping_address='A'
- Expected: 400; không tạo đơn
- Result: FAIL — defect expected
- Related Bug: [#419](https://github.com/trngnneee/eshop-sut/issues/419) (`D-CHK-02`)

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
