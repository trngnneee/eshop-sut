# FR10-S-TC06: User hủy đơn hàng ở trạng thái confirmed

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / Equivalence Partitioning / State Transition

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `confirmed`.
- Tài khoản `user` đã đăng nhập và có quyền thực hiện thao tác.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Current status | confirmed |
| Requested status | canceled |
| Endpoint | PUT /api/orders/:id/cancel |
| Body | [Không có body] |
| Order ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `confirmed`.
2. Đăng nhập bằng tài khoản `user` hợp lệ.
3. Gửi request `PUT /api/orders/:id/cancel`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 200.
- Trạng thái đơn hàng được cập nhật thành `canceled`.

## Status / Related bugs
Not Run / None
