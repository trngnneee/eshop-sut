# TC-CART-071: Thêm sản phẩm rồi logout, login bằng user khác

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Chuẩn bị sẵn 2 tài khoản người dùng khác nhau.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tài khoản A | `userA@eshop.com` |
| Tài khoản B | `userB@eshop.com` |

## Test steps
1. Đăng nhập tài khoản A, thêm sản phẩm vào giỏ hàng.
2. Đăng xuất tài khoản A.
3. Đăng nhập tài khoản B và truy cập trang giỏ hàng /cart.


## Expected result
- User mới không thấy cart của user cũ

## Status / Related bugs
Pass / None
