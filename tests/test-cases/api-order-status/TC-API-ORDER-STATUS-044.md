# TC-API-ORDER-STATUS-044

- Requirement: `FR-10/FR-12/FR-18`
- Group/technique: Extension / State/security
- Preconditions: Admin JWT; status=['delivered'] hoặc {value:'delivered'}
- Method/data: `Status sai kiểu dữ liệu`
- Expected: 400; phân biệt type invalid với transition invalid
- Result: FAIL — defect expected
- Related Bug: `D-ADM-06`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
