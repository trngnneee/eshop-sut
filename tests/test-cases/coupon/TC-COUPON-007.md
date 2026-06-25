# TC-COUPON-007: Áp dụng mã giảm giá thất bại do mã không tồn tại trong hệ thống

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "NONEXIST" |
| **total** | 300000 |

## Test steps
1. Tại màn hình Checkout, nhập mã "NONEXIST" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Hệ thống từ chối áp dụng mã giảm giá.
- Hiển thị thông báo lỗi: "Mã giảm giá không tồn tại".
- Số tiền giảm giá hiển thị: `0 ₫`.
- Số tiền thanh toán cuối cùng giữ nguyên: `300,000 ₫`.

## Status / Related bugs
Not Run / None
