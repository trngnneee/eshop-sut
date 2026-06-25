# TC-COUPON-015: Áp dụng mã giảm giá thất bại do mã coupon chứa ký tự đặc biệt

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "SAVE10!@#" |
| **total** | 350000 |

## Test steps
1. Tại màn hình Checkout, nhập mã "SAVE10!@#" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Hệ thống từ chối áp dụng.
- Trả về lỗi HTTP 404.
- Hiển thị thông báo lỗi: "Mã giảm giá không tồn tại hoặc đã bị vô hiệu hóa".

## Status / Related bugs
Pass / None
