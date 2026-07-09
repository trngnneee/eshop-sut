# TC-CART-063: POST /api/cart với id hợp lệ nhưng price bị sửa thấp hơn

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Sản phẩm ID = 1 tồn tại trong hệ thống với giá gốc là 100.000đ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| productId | `1` |
| price | `1000` (Giá gốc là 100000) |
| quantity | `1` |

## Test steps
1. Đăng nhập tài khoản.
2. Gửi request POST tới /api/cart với productId = 1 (giá gốc 100.000đ) nhưng truyền trường price = 1000đ.
3. Kiểm tra giỏ hàng bằng GET /api/cart xem giá của sản phẩm trong giỏ có bị đổi thành 1.000đ hay không.


## Expected result
- Server không được lấy giá từ client; phải dùng giá gốc phía server

## Status / Related bugs
Fail / BUG-FR07-B-13
