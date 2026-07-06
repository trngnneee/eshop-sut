# FR18-S-TC15: Từ chối status null

## Requirement ID
FR-18

## Module / Test type / Technique
Admin Order Management / Functional / Equivalence Partitioning

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `pending`.
- Admin đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current status | pending |
| Requested status | null |
| Endpoint | PUT /api/admin/orders/:id/status |
| Body | {"status": null} |
| Order ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `pending`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": null}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `pending`.

## Status / Related bugs
Passed / None
