# TC-COUPON-014: Áp dụng mã giảm giá thất bại do mã coupon là chuỗi rỗng

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "" |
| **total** | 350000 |

## Test steps
1. Tại màn hình Checkout, để trống ô nhập mã giảm giá (chuỗi rỗng).
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Hệ thống từ chối áp dụng.
- Trả về lỗi HTTP 400.
- Hiển thị thông báo lỗi: "Vui lòng nhập mã giảm giá".

## Status / Related bugs
Pass / None
