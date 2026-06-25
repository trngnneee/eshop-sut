# TC-COUPON-011: Áp dụng mã giảm giá thất bại do mã tồn tại nhưng bị tắt (is_active = 0)

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).
- Mã `INACTIVE` tồn tại trong hệ thống nhưng cột `is_active` được thiết lập bằng `0`.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "INACTIVE" |
| **total** | 200000 |

## Test steps
1. Tại màn hình Checkout, nhập mã "INACTIVE" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Hệ thống từ chối áp dụng mã giảm giá.
- Hiển thị thông báo lỗi: "Mã giảm giá không tồn tại hoặc đã bị vô hiệu hóa".
- Số tiền giảm giá hiển thị: `0 ₫`.

## Status / Related bugs
Pass / None
