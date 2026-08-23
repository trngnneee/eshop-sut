---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Reset Password] API reset-password chấp nhận mật khẩu yếu'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`HT-FORGOT-EXT-004`

## Requirement liên quan

FR-03, SEC-07

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/reset-password`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Gọi `POST /api/forgot-password` để lấy OTP cho `test@eshop.com`.
2. Dùng `resetToken` nhận được để gọi `POST /api/reset-password`.
3. Gửi `newPassword` là giá trị yếu, ví dụ `"123"`.

## Expected result

API phải từ chối mật khẩu yếu bằng HTTP `400 Bad Request` và không cập nhật mật khẩu của user.

## Actual result

API chấp nhận mật khẩu yếu và trả HTTP `200`. Newman report ghi nhận: `weak password should be rejected: expected 400 but got 200`.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/438#issue-5224652192
