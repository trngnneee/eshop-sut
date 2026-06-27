# TC-COUPON-024: Áp dụng mã giảm giá cố định có giá trị giảm lớn hơn tổng giá trị đơn hàng

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Boundary Value Analysis

## Preconditions
- Đơn hàng đạt giá trị tối thiểu nhưng nhỏ hơn giá trị giảm của mã. Người dùng đã đăng nhập.

## Test data
code: "FIXED50" (giảm 50,000 VND, min_order = 30,000 VND), total_amount: 30000

## Test steps
1. Đặt đơn hàng trị giá 30,000 VND.
2. Áp dụng mã "FIXED50".

## Expected result
- Áp dụng thành công, discount_amount = 30,000 VND, final_amount = 0 VND (không được hiển thị số tiền âm). Trả về HTTP 200.

## Status / Related bugs
Fail / [BUG-COUPON-007](../../bug-reports/BUG-COUPON-007.md)
