# TC-API-ORDER-STATUS-040

- Requirement: `FR-10/FR-12/FR-18`
- Group/technique: Extension / State/security
- Preconditions: User A dùng token sửa order của user B
- Method/data: `Cross-user order mutation`
- Expected: 403; user không có quyền admin
- Result: FAIL — defect expected
- Related Bug: [#423](https://github.com/trngnneee/eshop-sut/issues/423) (`D-ADM-01`)

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
