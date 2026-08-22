# TC-API-ORDER-STATUS-043

- Requirement: `FR-10/FR-12/FR-18`
- Group/technique: Extension / State/security
- Preconditions: User JWT; order shipping; PUT /api/orders/:id/cancel
- Method/data: `User không hủy order shipping qua endpoint user`
- Expected: 400; user không được hủy shipping
- Result: FAIL — defect expected
- Related Bug: `D-ADM-08`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
