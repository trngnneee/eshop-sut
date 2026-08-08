# TC-CART-072: Login user A thêm sản phẩm, logout, login lại user A

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Tài khoản A hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tài khoản | `userA@eshop.com` |

## Test steps
1. Đăng nhập tài khoản A, thêm sản phẩm vào giỏ hàng.
2. Đăng xuất tài khoản A và đóng trình duyệt.
3. Mở trình duyệt, đăng nhập lại tài khoản A và truy cập trang giỏ hàng.


## Expected result
- Cart của user A vẫn đúng hoặc được xử lý theo đặc tả hệ thống

## Status / Related bugs
Not Run / None
