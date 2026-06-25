# TC-COUPON-019: Áp dụng mã giảm giá thất bại do tổng đơn hàng có giá trị âm (total_amount < 0)

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
| **total** | -50000 |

## Test steps
1. Gửi yêu cầu POST áp dụng mã giảm giá với tham số `total_amount` là số âm `-50000`.

## Expected result
- Hệ thống từ chối áp dụng.
- Trả về mã lỗi HTTP 400.

## Status / Related bugs
Fail / [BUG-COUPON-005](../../bug-reports/BUG-COUPON-005.md)
