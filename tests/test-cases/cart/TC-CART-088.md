# TC-CART-088: Gửi request xóa/cập nhật item không thuộc giỏ hàng của user hiện tại

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Chuẩn bị sẵn 2 tài khoản và giỏ hàng chứa sản phẩm.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Target ID | ID dòng sản phẩm của User A |

## Test steps
1. Đăng nhập tài khoản A, ghi nhận ID giỏ hàng hoặc ID dòng sản phẩm.
2. Đăng nhập tài khoản B.
3. Gửi request DELETE hoặc PUT chỉnh sửa số lượng sản phẩm của tài khoản A bằng token của tài khoản B.


## Expected result
- Server trả 403/404, không ảnh hưởng giỏ hàng user khác

## Status / Related bugs
Not Run / None
