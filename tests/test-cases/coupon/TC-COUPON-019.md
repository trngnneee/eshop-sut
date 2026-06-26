# TC-COUPON-019: Áp dụng mã giảm giá thất bại do mã coupon chứa thẻ HTML/JS (phòng tránh tấn công XSS)

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Người dùng đã đăng nhập thành công (có JWT Token hợp lệ).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **coupon_code** | `<script>alert('XSS')</script>` |
| **total** | 50000 |

## Test steps
1. Nhập mã `<script>alert('XSS')</script>`.
2. Nhấn "Áp dụng".

## Expected result
- Từ chối áp dụng. Báo lỗi không hợp lệ (không thực thi mã script).

## Status / Related bugs
Pass / None
