---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin Coupons] API tạo coupon chấp nhận nhiều field không hợp lệ'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-ADMIN-COUPONS-DP-005`, `TC-ADMIN-COUPONS-DP-008`, `TC-ADMIN-COUPONS-DP-009`, `TC-ADMIN-COUPONS-DP-010`, `TC-ADMIN-COUPONS-DP-011`, `TC-ADMIN-COUPONS-DP-012`, `TC-ADMIN-COUPONS-DP-013`, `TC-ADMIN-COUPONS-DP-014`, `TC-ADMIN-COUPONS-DP-015`, `TC-ADMIN-COUPONS-SEC-009`, `TC-ADMIN-COUPONS-SV-004`, `HT-ADMIN-EXT-002`, `HT-ADMIN-EXT-003`, `HT-ADMIN-EXT-006`

## Requirement liên quan

FR-17

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
3. Gửi `POST /api/admin/coupons` với các body không hợp lệ như thiếu `code`, thiếu `max_uses_per_user`, `type="percentage"`, `discount_value=0`, `discount_value=101`, `discount_value` là string, `min_order_amount=-1`, `expired_at="31-12-2026"`, `max_uses_per_user=0` hoặc `1.5`, coupon fixed có `discount_value > min_order_amount`, hoặc field thừa/nhạy cảm như `is_active`, `role`, `created_by`.
4. Kiểm tra status code và response body trong Newman report.

## Expected result

API phải trả HTTP `400 Bad Request` với JSON error rõ ràng và không tạo coupon mới.

## Actual result

Report `admin-coupons-report.html` ghi các request trên trả HTTP `200` và body dạng thành công, ví dụ `{"message":"Coupon created","id":38}` đến `{"message":"Coupon created","id":61}`. Điều này cho thấy endpoint thiếu validation cho required field, enum, numeric boundary, date format và monetary invariant.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/468#issue-5227443190
