# FR10-O-BVA-TC02: Kiểm thử Order ID tại biên tối thiểu

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / Boundary Value Analysis

## Preconditions
- Admin đã đăng nhập.
- Có đơn hàng hợp lệ với `id = 1` đang ở trạng thái `pending`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Order ID | 1 |
| Current status | pending |
| Requested status | confirmed |
| Endpoint | PUT /api/admin/orders/1/status |
| Body | {"status": "confirmed"} |

## Test steps
1. Đăng nhập bằng tài khoản `admin` hợp lệ.
2. Chuẩn bị đơn hàng `id = 1` ở trạng thái `pending`.
3. Gửi request `PUT /api/admin/orders/1/status` với body `{"status":"confirmed"}`.
4. Tải lại thông tin đơn hàng `id = 1`.

## Expected result
- Hệ thống trả về HTTP 200.
- Trạng thái đơn hàng `id = 1` được cập nhật thành `confirmed`.

## Status / Related bugs
Not Run / None
