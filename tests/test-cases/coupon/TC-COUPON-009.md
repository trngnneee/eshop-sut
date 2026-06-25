# TC-COUPON-009: Áp dụng mã giảm giá VIP100 thất bại do người dùng đã dùng hết số lần tối đa (2 lần)

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Boundary Value Analysis (2-Point)

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).
- Người dùng đã sử dụng mã `VIP100` thành công 2 lần trước đó (số lần dùng = 2 >= 2).
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
- Hệ thống từ chối áp dụng mã giảm giá.
- Hiển thị thông báo lỗi: "Bạn đã hết lượt sử dụng mã giảm giá này".
- Số tiền giảm giá hiển thị: `0 ₫`.
- Số tiền thanh toán cuối cùng giữ nguyên: `350,000 ₫`.

## Status / Related bugs
Not Run / None
