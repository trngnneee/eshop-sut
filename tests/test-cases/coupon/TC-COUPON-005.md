# TC-COUPON-005: Áp dụng mã giảm giá cố định BIGBUY thất bại do giá trị đơn hàng dưới ngưỡng tối thiểu biên dưới 1 đơn vị

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
| **total** | 499999 |

## Test steps
1. Tại màn hình Checkout, nhập mã "BIGBUY" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Hệ thống từ chối áp dụng mã giảm giá.
- Hiển thị thông báo lỗi: "Đơn hàng chưa đạt giá trị tối thiểu để áp dụng mã giảm giá này".
- Số tiền giảm giá hiển thị: `0 ₫`.
- Số tiền thanh toán cuối cùng giữ nguyên: `499,999 ₫`.

## Status / Related bugs
Not Run / None
