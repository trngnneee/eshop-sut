# FR18-V-TC01: Admin xem toàn bộ đơn hàng của nhiều người dùng

## Requirement ID
FR-18

## Module / Test type / Technique
Admin Order Management / Functional / Equivalence Partitioning

## Preconditions
- Admin đã đăng nhập bằng JWT hợp lệ.
- Hệ thống có ít nhất 3 đơn hàng thuộc ít nhất 2 user khác nhau.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Endpoint | GET /api/admin/orders |
| Seed orders | [{"id": 101, "user_id": 1, "user_name": "Nguyen Van A", "status": "pending", "shipping_address": "12 Le Loi"}, {"id": 102, "user_id": 2, "user_name": "Tran Thi B", "status": "confirmed", "shipping_address": "34 Nguyen Hue"}, {"id": 103, "user_id": 1, "user_name": "Nguyen Van A", "status": "shipping", "shipping_address": "56 Pasteur"}] |

## Test steps
1. Đăng nhập bằng tài khoản `admin` hợp lệ.
2. Gửi request `GET /api/admin/orders` hoặc mở tab Quản lý Đơn hàng trong Admin UI.
3. Đối chiếu danh sách trả về với dữ liệu seed của nhiều user.

## Expected result
- Hệ thống trả về HTTP 200.
- Danh sách hiển thị toàn bộ đơn hàng của tất cả user, không chỉ đơn của admin hoặc một user hiện tại.
- Mỗi đơn hiển thị tối thiểu mã đơn, người đặt, tổng tiền, địa chỉ giao hàng và trạng thái hiện tại.

## Status / Related bugs
Passed / None
