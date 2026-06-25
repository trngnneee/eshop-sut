# TC-COUPON-008: Áp dụng mã giảm giá thất bại do người dùng chưa đăng nhập

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning

## Preconditions
- Người dùng chưa đăng nhập hệ thống (không có JWT Token).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "SAVE10" |
| **total** | 350000 |

## Test steps
1. Tại màn hình Checkout của Khách (Guest Checkout), nhập mã "SAVE10" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Hệ thống từ chối áp dụng mã giảm giá.
- Hiển thị thông báo yêu cầu đăng nhập: "Vui lòng đăng nhập để sử dụng mã giảm giá".
- Số tiền giảm giá hiển thị: `0 ₫`.
- Số tiền thanh toán cuối cùng giữ nguyên: `350,000 ₫`.

## Status / Related bugs
Not Run / None
