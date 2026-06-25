# TC-COUPON-004: Áp dụng mã giảm giá cố định BIGBUY thành công với giá trị đơn hàng đạt ngưỡng tối thiểu biên dưới

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Boundary Value Analysis (3-Point)

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).
- Người dùng chưa sử dụng mã `BIGBUY` lần nào.
- Mã `BIGBUY` đang hoạt động (`is_active = 1`) và còn hạn dùng (`expired_at = 2099-12-31`).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "BIGBUY" |
| **total** | 500000 |

## Test steps
1. Tại màn hình Checkout, nhập mã "BIGBUY" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Mã giảm giá được áp dụng thành công.
- Số tiền giảm giá hiển thị: `50,000 ₫` (Giá trị cố định).
- Số tiền thanh toán cuối cùng hiển thị: `450,000 ₫`.

## Status / Related bugs
Not Run / None
