# FR10-S-TC01: Admin xác nhận đơn hàng từ pending sang confirmed

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / Equivalence Partitioning / State Transition

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `pending`.
- Tài khoản `admin` đã đăng nhập và có quyền thực hiện thao tác.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current status | pending |
| Requested status | confirmed |
| Endpoint | PUT /api/admin/orders/:id/status |
| Body | {"status": "confirmed"} |
| Order ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `pending`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "confirmed"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 200.
- Trạng thái đơn hàng được cập nhật thành `confirmed`.

## Status / Related bugs
Passed / None
