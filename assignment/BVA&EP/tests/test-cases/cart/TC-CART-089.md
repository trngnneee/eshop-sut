# TC-CART-089: Giỏ hàng không được xóa sạch sau khi thanh toán thành công (checkout success)

## Requirement ID
FR-08

## Module / Test type / Technique
Cart / Functional / Integration Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có ít nhất 1 sản phẩm.
- Người dùng đang ở giao diện thanh toán `/checkout`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| items | Danh sách sản phẩm trong giỏ hàng |

## Test steps
1. Nhấp nút "Thanh toán" để hoàn tất đơn hàng.
2. Chờ hệ thống báo "Thanh toán thành công!".
3. Điều hướng quay lại trang giỏ hàng `/cart` hoặc kiểm tra badge giỏ hàng trên thanh điều hướng Navbar.
4. Kiểm tra xem các sản phẩm đã thanh toán có còn tồn tại trong giỏ hàng hay không.

## Expected result
- Sau khi thanh toán thành công, giỏ hàng phải được làm sạch hoàn toàn (về trạng thái trống).
- Badge giỏ hàng trên Navbar hiển thị số 0.

## Status / Related bugs
Fail / BUG-FR07-B-19
