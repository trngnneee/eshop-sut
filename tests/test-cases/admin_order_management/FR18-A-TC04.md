# FR18-A-TC04: Từ chối request không có token cập nhật trạng thái đơn hàng

## Requirement ID
FR-18

## Module / Test type / Technique
Admin Order Management / Functional / Equivalence Partitioning / Authorization

## Preconditions
- Có đơn hàng `id = 101` đang ở trạng thái `pending`.
- Không gửi header Authorization.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | anonymous |
| Order ID | 101 |
| Current status | pending |
| Requested status | confirmed |
| Endpoint | PUT /api/admin/orders/101/status |
| Body | {"status": "confirmed"} |

## Test steps
1. Gửi request `PUT /api/admin/orders/101/status` với body `{"status":"confirmed"}` nhưng không kèm token.
2. Tải lại thông tin đơn hàng bằng tài khoản admin để đối chiếu.

## Expected result
- Hệ thống trả về HTTP 401 hoặc lỗi xác thực phù hợp.
- Trạng thái đơn hàng `id = 101` vẫn là `pending`.

## Status / Related bugs
Passed / None
