---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Forgot Password] Input email/body không hợp lệ trả 404 hoặc 500 thay vì 400'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-FORGOT-PASSWORD-DP-004`, `TC-FORGOT-PASSWORD-DP-005`, `TC-FORGOT-PASSWORD-DP-006`, `TC-FORGOT-PASSWORD-DP-007`, `TC-FORGOT-PASSWORD-DP-008`, `TC-FORGOT-PASSWORD-DP-009`, `TC-FORGOT-PASSWORD-DP-011`, `TC-FORGOT-PASSWORD-DP-012`, `TC-FORGOT-PASSWORD-DP-014`, `TC-FORGOT-PASSWORD-SEC-003`, `TC-FORGOT-PASSWORD-SEC-004`, `TC-FORGOT-PASSWORD-SEC-006`, `TC-FORGOT-PASSWORD-SV-004`, `TC-FORGOT-PASSWORD-SV-005`

## Requirement liên quan

FR-03, SEC-04, SEC-05

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/forgot-password`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi `POST /api/forgot-password` với các giá trị body không hợp lệ như thiếu `email`, email rỗng, chỉ có khoảng trắng, `null`, sai định dạng, sai kiểu dữ liệu, SQL injection payload, XSS payload hoặc body không phải JSON.
3. Kiểm tra HTTP status trong Newman report `API-testing/forgot-password--report.html`.

## Expected result

API phải từ chối input không hợp lệ bằng HTTP `400 Bad Request` và trả JSON validation error ổn định. API không nên tiếp tục xử lý như email hợp lệ, không nên đi tới bước lookup user, và không được trả lỗi server `500` cho lỗi format request.

## Actual result

Phần lớn input không hợp lệ trả HTTP `404 User not found` thay vì `400`. Trường hợp body không phải JSON trả HTTP `500 Internal Server Error`.

Ví dụ từ report:

- Expected `400`, actual `404` với missing/empty/null/malformed email.
- Expected `400`, actual `500` với `Content-Type: text/plain`.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/433#issue-5224587789
