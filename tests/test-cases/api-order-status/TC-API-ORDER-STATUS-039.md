# TC-API-ORDER-STATUS-039

- Requirement: `FR-10/FR-12/FR-18`
- Group/technique: Extension / State/security
- Preconditions: User thường có JWT; order tồn tại; PUT status=confirmed
- Method/data: `Role escalation bằng user token`
- Expected: 403; không cập nhật order
- Result: FAIL — defect expected
- Related Bug: `D-ADM-01`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
