---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Apply Coupon] Payload SQLi/XSS trong code vẫn được áp dụng coupon'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-APPLY-COUPON-SEC-001`, `TC-APPLY-COUPON-SEC-010`

## Requirement liên quan

FR-09, SEC-04, SEC-05

## Severity / Priority

Critical / P0

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/apply-coupon`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi `POST /api/apply-coupon` với `code` là SQL injection payload hoặc XSS payload.
3. Kiểm tra HTTP status và response trong Newman report.

## Expected result

API phải từ chối payload độc hại như một coupon code không tồn tại, trả HTTP `404` hoặc lỗi validation phù hợp, và không trả `discount_amount`/`final_amount` như coupon hợp lệ.

## Actual result

Report ghi:

- SQL injection: `expected status list: expected [ 404 ] to include 200`
- SQL injection: `expected -4500000 to equal undefined`
- XSS payload: `expected status list: expected [ 404 ] to include 200`
- XSS payload: `expected -4500000 to equal undefined`

Backend trả HTTP `200` và response thành công cho payload độc hại. Đây là dấu hiệu nghiêm trọng: logic lookup/validate coupon code có thể đang match sai, fallback sang coupon mặc định, hoặc xử lý input không an toàn.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/465#issue-5227185096
