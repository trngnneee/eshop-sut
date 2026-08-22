# TC-API-ORDER-STATUS-033

- Requirement: `FR-10/FR-12/FR-18`
- Group/technique: Security / Security/role
- Preconditions: User JWT; order tồn tại
- Method/data: `Bearer userToken; status='confirmed'`
- Expected: 403; không cập nhật
- Result: FAIL — defect expected
- Related Bug: [#423](https://github.com/trngnneee/eshop-sut/issues/423) (`D-ADM-01`)

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
