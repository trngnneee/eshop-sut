---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Forgot Password] Response chứa resetToken có thể bị cache'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`HT-FORGOT-EXT-007`

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
3. Kiểm tra response headers.

## Expected result

Response có chứa `resetToken` phải có header chống cache, ví dụ `Cache-Control: no-store` hoặc `Cache-Control: no-cache`.

## Actual result

Response không có header `Cache-Control` phù hợp. Newman report ghi nhận: `Cache-Control: expected '' to match /no-store|no-cache/i`.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/439#issue-5224661211
