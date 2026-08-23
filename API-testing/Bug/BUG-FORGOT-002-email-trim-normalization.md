---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Forgot Password] Email có khoảng trắng đầu/cuối không được chuẩn hóa'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-FORGOT-PASSWORD-DP-010`

## Requirement liên quan

FR-03

## Severity / Priority

Minor / P2

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/forgot-password`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi `POST /api/forgot-password` với body `{ "email": "  test@eshop.com  " }`.
3. Kiểm tra HTTP status và response body.

## Expected result

API nên trim khoảng trắng đầu/cuối và xử lý email đã đăng ký `test@eshop.com`, sau đó trả HTTP `200` cùng response chứa reset token.

## Actual result

API trả HTTP `404 User not found`, cho thấy email chưa được chuẩn hóa trước khi lookup user.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/434#issue-5224595468