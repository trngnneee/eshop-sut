# TC-COUPON-003: Áp dụng mã giảm giá SAVE10 thành công với giá trị đơn hàng trên ngưỡng tối thiểu biên dưới 1 đơn vị

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Boundary Value Analysis (3-Point)

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).
- Người dùng chưa sử dụng mã `SAVE10` lần nào.
- Mã `SAVE10` đang hoạt động (`is_active = 1`) và còn hạn dùng (`expired_at = 2099-12-31`).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "SAVE10" |
| **total** | 300001 |

## Test steps
1. Tại màn hình Checkout, nhập mã "SAVE10" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Mã giảm giá được áp dụng thành công.
- Số tiền giảm giá hiển thị: `30,000 ₫` (10% của 300,001 ₫, làm tròn).
- Số tiền thanh toán cuối cùng hiển thị: `270,001 ₫`.

## Status / Related bugs
Pass / None
