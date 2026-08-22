# TC-API-ORDER-STATUS-024

- Requirement: `FR-10/FR-12/FR-18`
- Group/technique: State / State-transition
- Preconditions: Admin JWT; order hiện ở trạng thái `canceled`
- Method/data: `PUT /api/admin/orders/:id; status='delivered'`
- Expected: 400; từ chối transition canceled → delivered
- Result: FAIL — defect expected
- Related Bug: [#424](https://github.com/trngnneee/eshop-sut/issues/424) (`D-ADM-02`)

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
