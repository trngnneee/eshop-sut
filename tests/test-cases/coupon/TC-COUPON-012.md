# TC-COUPON-012: Áp dụng mã giảm giá thất bại tại biên thời gian hết hạn (date = expired_at)

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Boundary Value Analysis (2-Point)

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).
- Mã `EXP_BORDER` có hạn sử dụng `expired_at` bằng đúng thời điểm hiện tại của hệ thống.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "EXP_BORDER" |
| **total** | 200000 |

## Test steps
1. Tại màn hình Checkout, nhập mã "EXP_BORDER" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Hệ thống từ chối áp dụng mã giảm giá.
- Hiển thị thông báo lỗi: "Mã giảm giá đã hết hạn".
- Số tiền giảm giá hiển thị: `0 ₫`.

## Status / Related bugs
Pass / None
