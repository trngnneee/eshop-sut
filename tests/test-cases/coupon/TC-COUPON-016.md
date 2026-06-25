# TC-COUPON-017: Áp dụng mã giảm giá thất bại do tổng đơn hàng (total_amount) là chuỗi không thể quy đổi thành số

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "SAVE10" |
| **total** | "invalid_number" |

## Test steps
1. Gửi yêu cầu POST áp dụng mã giảm giá với tham số `total_amount` là chuỗi không hợp lệ `"invalid_number"`.

## Expected result
- Hệ thống từ chối áp dụng.
- Trả về mã lỗi HTTP 400 (yêu cầu đầu vào không hợp lệ).

## Status / Related bugs
Fail / [BUG-COUPON-005](../../bug-reports/BUG-COUPON-005.md)
