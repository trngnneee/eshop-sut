# TC-API-CHECKOUT-004

- Requirement: `FR-08/FR-10`
- Group/technique: Partition / EP
- Preconditions: Có token giả
- Method/data: `POST /api/checkout`; Authorization='Bearer invalid.signature.token'
- Expected: 403; không tạo đơn
- Result: PASS/SMOKE
- Related Bug: `None`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
