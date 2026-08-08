# TC-CART-009: Thêm sản phẩm từ trang chủ

## Requirement ID
FR-07, FR-23, FR-24

## Module / Test type / Technique
Cart / Functional / Functional Testing

## Preconditions
- Người dùng đã đăng nhập vào hệ thống.
- Người dùng đang ở Trang chủ (`/`).

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm | `Sản phẩm A` |

## Test steps
1. Tại màn hình trang chủ, tìm đến sản phẩm A.
2. Nhấp vào nút 'Thêm vào giỏ hàng' của sản phẩm A.
3. Quan sát phản hồi trên màn hình (toast message) và số lượng hiển thị trên badge giỏ hàng ở navbar.

## Expected result
- Hệ thống hiển thị thông báo (toast message) thành công ngay lập tức.
- Số lượng sản phẩm trên badge giỏ hàng ở thanh điều hướng tăng lên chính xác.
- Sản phẩm A được thêm vào giỏ hàng thành công.

## Status / Related bugs
Not Run / None
