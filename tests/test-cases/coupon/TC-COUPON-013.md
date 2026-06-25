# TC-COUPON-013: Áp dụng mã giảm giá thất bại khi số lần sử dụng trong CSDL đã vượt hạn mức tối đa (used_count > max_uses_per_user)

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Boundary Value Analysis (2-Point)

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).
- Mã `SAVE10` có giới hạn 1 lần dùng (`max_uses_per_user = 1`).
- Do một sự cố đồng bộ hoặc bypass dữ liệu, trong cơ sở dữ liệu (`coupon_usage`) đã ghi nhận người dùng này đã sử dụng mã này 2 lần (used_count = 2 > 1).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | "SAVE10" |
| **total** | 350000 |

## Test steps
1. Tại màn hình Checkout, nhập mã "SAVE10" vào ô nhập mã giảm giá.
2. Nhấp chọn nút "Áp dụng".

## Expected result
- Hệ thống chặn đứng việc áp dụng và báo lỗi: "Bạn đã sử dụng mã này 1 lần (đã đạt giới hạn)" (hoặc thông báo vượt giới hạn tương đương).
- Số tiền giảm giá hiển thị: `0 ₫`.

## Status / Related bugs
Pass / None
