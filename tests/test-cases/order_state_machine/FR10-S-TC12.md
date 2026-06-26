# FR10-S-TC12: Từ chối User tự hủy đơn hàng đang shipping

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / Equivalence Partitioning / State Transition

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `shipping`.
- Tài khoản `user` đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Current status | shipping |
| Requested status | canceled |
| Endpoint | PUT /api/orders/:id/cancel |
| Body | [Không có body] |
| Order ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `shipping`.
2. Đăng nhập bằng tài khoản `user` hợp lệ.
3. Gửi request `PUT /api/orders/:id/cancel`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `shipping`.

## Status / Related bugs
Not Run / None
