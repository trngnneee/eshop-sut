---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Forgot Password] Reset token/OTP chỉ có 4 chữ số thay vì 6 chữ số'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-FORGOT-PASSWORD-SEC-001`, `TC-FORGOT-PASSWORD-SV-002`

## Requirement liên quan

FR-03, SEC-07

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/forgot-password`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi `POST /api/forgot-password` với body `{ "email": "test@eshop.com" }`.
3. Kiểm tra field `resetToken` trong JSON response.

## Expected result

`resetToken` phải match regex `^[0-9]{6}$`, nghĩa là chuỗi gồm đúng 6 chữ số.

## Actual result

API trả token 4 chữ số, ví dụ `8070` hoặc `3032`. Điều này không đúng format OTP kỳ vọng và làm giảm entropy của OTP.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/436#issue-5224606695
