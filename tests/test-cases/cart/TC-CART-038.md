# TC-CART-038: Toast hiển thị sau khi thêm vào giỏ hàng

## Requirement ID
FR-24

## Module / Test type / Technique
Cart / UI Feedback / UI Feedback

## Preconditions
- Người dùng đã đăng nhập.
- Người dùng đang ở Trang chủ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm | `Sản phẩm A` |

## Test steps
1. Tìm sản phẩm A và click vào nút 'Thêm vào giỏ hàng'.

## Expected result
- Hệ thống ngay lập tức hiển thị một popup/toast thông báo thành công (ví dụ: 'Đã thêm sản phẩm vào giỏ hàng!') ở góc màn hình.
- Toast tự động biến mất sau vài giây mà không cần người dùng tắt thủ công.

## Status / Related bugs
Not Run / None
