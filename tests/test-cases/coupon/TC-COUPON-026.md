# TC-COUPON-026: Áp dụng mã giảm giá cho tài khoản Admin

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning

## Preconditions
- Mã SAVE10 hoạt động. Đăng nhập bằng tài khoản Admin.

## Test data
code: "SAVE10", total_amount: 300000, JWT token của Admin

## Test steps
1. Đăng nhập tài khoản Admin.
2. Gửi request áp dụng mã giảm giá SAVE10.

## Expected result
- Hệ thống từ chối áp dụng (do Admin không được mua hàng/sử dụng coupon). Trả về HTTP 403 Forbidden hoặc HTTP 400.

## Status / Related bugs
Fail / [BUG-COUPON-009](../../bug-reports/BUG-COUPON-009.md)
