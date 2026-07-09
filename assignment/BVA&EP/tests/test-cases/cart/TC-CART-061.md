# TC-CART-061: POST /api/cart với id sản phẩm không tồn tại

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Người dùng đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| productId | `999999` (Không tồn tại) |
| quantity | `1` |

## Test steps
1. Đăng nhập tài khoản người dùng và lấy token JWT.
2. Gửi request POST tới /api/cart với body chứa productId không tồn tại trong hệ thống (ví dụ: 999999).
3. Kiểm tra phản hồi của server và giỏ hàng bằng GET /api/cart.


## Expected result
- Server trả 400/404, không thêm sản phẩm ma vào cart

## Status / Related bugs
Fail / BUG-FR07-B-14
