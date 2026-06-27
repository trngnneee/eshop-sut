# FR18-A-TC03: Từ chối user thường cập nhật trạng thái đơn hàng qua endpoint Admin

## Requirement ID
FR-18

## Module / Test type / Technique
Admin Order Management / Functional / Equivalence Partitioning / Authorization

## Preconditions
- User thường đã đăng nhập bằng JWT hợp lệ với `role = user`.
- Có đơn hàng `id = 101` đang ở trạng thái `pending`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Order ID | 101 |
| Current status | pending |
| Requested status | confirmed |
| Endpoint | PUT /api/admin/orders/101/status |
| Body | {"status": "confirmed"} |

## Test steps
1. Đăng nhập bằng tài khoản user thường.
2. Gửi request `PUT /api/admin/orders/101/status` với body `{"status":"confirmed"}`.
3. Tải lại thông tin đơn hàng `id = 101` bằng tài khoản admin để đối chiếu.

## Expected result
- Hệ thống trả về HTTP 403 hoặc lỗi quyền truy cập phù hợp.
- Trạng thái đơn hàng `id = 101` vẫn là `pending`.

## Status / Related bugs
Failed / BUG-FR18-A-01 - API Admin không kiểm tra role admin
