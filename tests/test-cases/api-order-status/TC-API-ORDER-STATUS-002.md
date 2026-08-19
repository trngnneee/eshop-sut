# TC-API-ORDER-STATUS-002

- Requirement: `FR-10/FR-12/FR-18`
- Group/technique: State / State-transition
- Preconditions: Admin JWT; order hiện ở trạng thái `pending`
- Method/data: `PUT /api/admin/orders/:id; status='confirmed'`
- Expected: 200; transition pending → confirmed được chấp nhận
- Result: PASS/SMOKE
- Related Bug: `None`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
