# TC-COUPON-006: Áp dụng mã giảm giá thất bại do mã đã hết hạn sử dụng

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).
- Người dùng chưa sử dụng mã `EXPIRED` lần nào.
- Mã `EXPIRED` đang ở trạng thái hoạt động (`is_active = 1`) nhưng đã hết hạn (`expired_at = 2020-01-01`).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "EXPIRED" |
| **total** | 150000 |

## Test steps
1. Tại màn hình Checkout, nhập mã "EXPIRED" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Hệ thống từ chối áp dụng mã giảm giá.
- Hiển thị thông báo lỗi: "Mã giảm giá đã hết hạn sử dụng".
- Số tiền giảm giá hiển thị: `0 ₫`.
- Số tiền thanh toán cuối cùng giữ nguyên: `150,000 ₫`.

## Status / Related bugs
Not Run / None
