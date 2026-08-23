---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin Coupons] SQLi/XSS payload trong coupon code không được validate an toàn'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-ADMIN-COUPONS-SEC-007`, `TC-ADMIN-COUPONS-SEC-008`

## Requirement liên quan

FR-17, SEC-04, SEC-05

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/admin/coupons`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Đăng nhập admin và lấy JWT hợp lệ.
3. Gửi `POST /api/admin/coupons` với `code` là payload SQL injection như `"' OR '1'='1"` hoặc payload XSS như `"<script>alert(1)</script>"`.
4. Chạy lại request hoặc kiểm tra report Newman để xem response.

## Expected result

API phải từ chối payload độc hại bằng HTTP `400 Bad Request` hoặc sanitize/validate theo rule coupon code; response không được lộ lỗi SQL/internal stack.

## Actual result

Report ghi expected `400` nhưng actual là HTTP `500`; response body chứa `{"error":"SQLITE_CONSTRAINT: UNIQUE constraint failed: coupons.code"}`. Điều này cho thấy payload độc hại đã đi tới tầng lưu DB và có thể đã được lưu ở lần chạy trước, đồng thời response lộ chi tiết SQLite.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/492#issue-5227502887
