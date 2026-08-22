# TC-API-CHECKOUT-001

- Requirement: `FR-08/FR-10`
- Group/technique: Partition / EP
- Preconditions: User có JWT; giỏ có một sản phẩm
- Method/data: `POST /api/checkout`; total_amount=200000; shipping_address='123 Le Loi'
- Expected: 200; orderId là số nguyên; đơn có total theo giỏ; status=pending
- Result: FAIL — defect expected
- Related Bug: `D-CHK-01`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
