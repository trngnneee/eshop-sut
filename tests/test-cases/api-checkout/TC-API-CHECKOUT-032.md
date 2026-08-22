# TC-API-CHECKOUT-032

- Requirement: `FR-08/FR-10`
- Group/technique: Security / Security
- Preconditions: User có JWT; giỏ có sản phẩm
- Method/data: `POST /api/checkout`; shipping_address='<script>alert(1)</script>'
- Expected: Payload bị từ chối hoặc được escape khi đọc lại
- Result: FAIL — defect expected
- Related Bug: `D-CHK-05`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
