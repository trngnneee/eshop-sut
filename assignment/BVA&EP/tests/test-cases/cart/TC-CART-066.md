# TC-CART-066: POST /api/cart với quantity dạng chuỗi "2"

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Người dùng đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| productId | `1` |
| quantity | `'2'` (String) |

## Test steps
1. Đăng nhập tài khoản.
2. Gửi request POST tới /api/cart với quantity dạng string: '2' thay vì số nguyên 2.
3. Kiểm tra xem server có tự động ép kiểu thành số nguyên hoặc reject với lỗi 400 Bad Request.


## Expected result
- Server phải reject hoặc normalize nhất quán; không lưu sai kiểu dữ liệu

## Status / Related bugs
Fail / BUG-FR07-B-15
