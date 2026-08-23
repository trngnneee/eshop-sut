---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Forgot Password] Response cho email chưa đăng ký làm lộ trạng thái tồn tại tài khoản'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-FORGOT-PASSWORD-SEC-005`

## Requirement liên quan

FR-03

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/forgot-password`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi `POST /api/forgot-password` với email chưa đăng ký, ví dụ `{ "email": "secret-probe@example.com" }`.
3. Kiểm tra HTTP status và nội dung field `message` hoặc `error` trong response.

## Expected result

API có thể trả error response cho email chưa đăng ký, nhưng nội dung lỗi phải chung chung, không chứa `User not found` hoặc thông điệp xác nhận tài khoản không tồn tại.

## Actual result

API trả HTTP `404` với message `User not found`, trực tiếp tiết lộ email chưa được đăng ký. Hành vi này tạo rủi ro user enumeration.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/437#issue-5224646056