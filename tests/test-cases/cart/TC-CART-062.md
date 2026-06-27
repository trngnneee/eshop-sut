# TC-CART-062: POST /api/cart với id hợp lệ nhưng name sai

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Sản phẩm ID = 1 tồn tại trong hệ thống với tên thực tế.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| productId | `1` |
| name | `'Sản phẩm giả mạo'` |
| quantity | `1` |

## Test steps
1. Đăng nhập tài khoản và lấy token JWT.
2. Gửi request POST tới /api/cart với productId = 1 (Sản phẩm A) nhưng ghi đè trường name thành 'Sản phẩm giả mạo'.
3. Kiểm tra giỏ hàng bằng GET /api/cart xem tên sản phẩm hiển thị là tên thật (Sản phẩm A) hay tên giả.


## Expected result
- Server dùng dữ liệu thật từ DB hoặc reject request

## Status / Related bugs
Not Run / None
