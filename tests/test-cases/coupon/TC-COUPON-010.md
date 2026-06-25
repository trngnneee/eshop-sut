# TC-COUPON-010: Áp dụng mã giảm giá VIP100 thành công khi người dùng mới sử dụng 1 lần (dưới hạn mức tối đa 2 lần)

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Boundary Value Analysis (2-Point)

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).
- Người dùng mới sử dụng mã `VIP100` thành công 1 lần trước đó (số lần dùng = 1 < 2).
- Mã `VIP100` đang hoạt động (`is_active = 1`) và còn hạn dùng (`expired_at = 2099-12-31`).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "VIP100" |
| **total** | 350000 |

## Test steps
1. Tại màn hình Checkout, nhập mã "VIP100" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Mã giảm giá được áp dụng thành công.
- Số tiền giảm giá hiển thị: `100,000 ₫` (Giá trị cố định).
- Số tiền thanh toán cuối cùng hiển thị: `250,000 ₫`.

## Status / Related bugs
Not Run / None
