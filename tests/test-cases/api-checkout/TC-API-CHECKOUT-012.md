# TC-API-CHECKOUT-012

- Requirement: `FR-08/FR-10`
- Group/technique: Partition / Security
- Preconditions: User có JWT; giỏ có sản phẩm
- Method/data: `POST /api/checkout`; <img src=x onerror=alert(1)>
- Expected: Request bị từ chối hoặc dữ liệu được escape khi đọc lại
- Result: FAIL — defect expected
- Related Bug: `D-CHK-05`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
