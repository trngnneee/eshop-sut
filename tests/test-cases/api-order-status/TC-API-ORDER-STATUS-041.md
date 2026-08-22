# TC-API-ORDER-STATUS-041

- Requirement: `FR-10/FR-12/FR-18`
- Group/technique: Extension / State/security
- Preconditions: Admin thử canceled→delivered rồi kiểm tra dữ liệu delivered/dashboard
- Method/data: `Canceled không hồi sinh và dashboard không tăng doanh thu`
- Expected: 400; không tăng delivered revenue
- Result: FAIL — defect expected
- Related Bug: `D-ADM-02`

> This file is a representative/failed-case traceability artifact generated from the final Markdown test table. Full inventory remains in `hw06/api-*/test-cases.md`.
