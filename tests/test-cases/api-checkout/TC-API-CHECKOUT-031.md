# TC-API-CHECKOUT-031

- Requirement: `FR-08/FR-10`
- Group/technique: Security / Security/IDOR
- Preconditions: Có orderId của user khác
- Method/data: `POST /api/checkout`; GET /api/orders/{id} không Authorization
- Expected: 401/403; không lộ order
- Result: FAIL — defect expected
- Related Bug: [#422](https://github.com/trngnneee/eshop-sut/issues/422) (`D-CHK-07`)

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
