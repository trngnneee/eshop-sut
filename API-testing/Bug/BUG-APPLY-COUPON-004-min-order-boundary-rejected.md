---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Apply Coupon] Đơn hàng đúng bằng min_order_amount bị từ chối'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-APPLY-COUPON-ST-005`

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
2. Gửi `POST /api/apply-coupon` với coupon `SAVE10`, `user_id` hợp lệ và `total_amount` đúng bằng `min_order_amount`.
3. Kiểm tra HTTP status trong Newman report.

## Expected result

Khi `total_amount` đúng bằng ngưỡng tối thiểu, API phải cho áp dụng coupon và trả HTTP `200` kèm `discount_amount`/`final_amount` hợp lệ.

## Actual result

Report ghi:

- `expected status list: expected [ 200 ] to include 400`
- `At minimum order amount is accepted: expected undefined to be a number`

Backend đang từ chối đơn hàng tại đúng boundary `min_order_amount`, nhiều khả năng dùng điều kiện `>` thay vì `>=` hoặc so sánh sai ngưỡng.

## Link Github Issue

N/A
