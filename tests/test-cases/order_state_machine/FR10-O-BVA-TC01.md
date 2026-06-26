# FR10-O-BVA-TC01: Kiểm thử Order ID ngay dưới biên tối thiểu

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / Boundary Value Analysis

## Preconditions
- Admin đã đăng nhập.
- Có ít nhất một đơn hàng hợp lệ trong hệ thống để đối chiếu trạng thái không bị ảnh hưởng.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Order ID | 0 |
| Current status | [Không tồn tại] |
| Requested status | confirmed |
| Endpoint | PUT /api/admin/orders/0/status |
| Body | {"status": "confirmed"} |

## Test steps
1. Đăng nhập bằng tài khoản `admin` hợp lệ.
2. Gửi request `PUT /api/admin/orders/0/status` với body `{"status":"confirmed"}`.
3. Kiểm tra response và danh sách đơn hàng sau request.

## Expected result
- Hệ thống trả về HTTP 400 hoặc 404 với thông báo lỗi phù hợp.
- Không có trạng thái đơn hàng nào bị thay đổi.

## Status / Related bugs
Not Run / None
