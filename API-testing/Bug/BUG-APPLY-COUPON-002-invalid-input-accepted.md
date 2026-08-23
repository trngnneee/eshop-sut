---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Apply Coupon] Input không hợp lệ vẫn được xử lý như coupon hợp lệ'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-APPLY-COUPON-DP-006`, `TC-APPLY-COUPON-DP-007`, `TC-APPLY-COUPON-DP-011`, `TC-APPLY-COUPON-DP-013`, `TC-APPLY-COUPON-DP-014`, `TC-APPLY-COUPON-DP-015`, `TC-APPLY-COUPON-SV-007`, `HT-APPLY-EXT-004`, `HT-APPLY-EXT-005`

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
2. Gửi `POST /api/apply-coupon` với các input không hợp lệ như:
   - `code` chỉ chứa khoảng trắng.
   - `code` sai kiểu dữ liệu là number.
   - `total_amount` sai kiểu dữ liệu là string.
   - `user_id` không tồn tại, sai kiểu dữ liệu, thiếu field, `null` hoặc bằng `0`.
3. Kiểm tra HTTP status và response body trong Newman report.

## Expected result

API phải trả HTTP `400 Bad Request` cho lỗi validation input và không trả schema thành công có `discount_amount`/`final_amount`.

## Actual result

Nhiều input không hợp lệ vẫn trả HTTP `200` và response dạng áp dụng coupon thành công. Một số lỗi trong report:

- `expected status list: expected [ 400 ] to include 200`
- `expected -4500000 to equal undefined`
- `expected -7000000 to equal undefined`

Riêng case `code` là number trả `404` thay vì lỗi validation `400`, cho thấy backend đang lookup coupon trước hoặc thiếu validate kiểu dữ liệu.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/461#issue-5227154335
