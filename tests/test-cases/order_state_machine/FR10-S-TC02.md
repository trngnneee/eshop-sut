# FR10-S-TC02: Admin giao hàng từ confirmed sang shipping

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / Equivalence Partitioning / State Transition

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `confirmed`.
- Tài khoản `admin` đã đăng nhập và có quyền thực hiện thao tác.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current status | confirmed |
| Requested status | shipping |
| Endpoint | PUT /api/admin/orders/:id/status |
| Body | {"status": "shipping"} |
| Order ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `confirmed`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "shipping"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 200.
- Trạng thái đơn hàng được cập nhật thành `shipping`.

## Status / Related bugs
Not Run / None
