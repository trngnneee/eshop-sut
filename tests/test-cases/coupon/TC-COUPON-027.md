# TC-COUPON-027: Áp dụng mã giảm giá khi giỏ hàng trống

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Boundary Value Analysis

## Preconditions
- Mã SAVE10 hoạt động, người dùng đã đăng nhập.

## Test data
code: "SAVE10", total_amount: 0

## Test steps
1. Giỏ hàng trống (total_amount = 0).
2. Áp dụng mã SAVE10.

## Expected result
- Hệ thống từ chối áp dụng mã giảm giá, báo lỗi giỏ hàng trống hoặc chưa đạt giá trị tối thiểu. Trả về HTTP 400.

## Status / Related bugs
Fail / [BUG-COUPON-010](../../bug-reports/BUG-COUPON-010.md)
