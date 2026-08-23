---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Apply Coupon] Content-Type không phải JSON gây lỗi 500 thay vì validation error'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-APPLY-COUPON-DP-017`

## Requirement liên quan

FR-09

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/apply-coupon`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi `POST /api/apply-coupon` với `Content-Type` không phải `application/json`.
3. Kiểm tra HTTP status và body trong Newman report.

## Expected result

API phải trả HTTP `400 Bad Request` hoặc lỗi parse/validation dạng JSON ổn định. Backend không được crash hoặc trả lỗi server cho request sai định dạng.

## Actual result

Report ghi:

- `expected status list: expected [ 400 ] to include 500`
- `response JSON body: expected null to not equal null`

Backend trả HTTP `500 Internal Server Error` và body không phải JSON hợp lệ.

## Link Github Issue

N/A
