# FR10-S-TC01: Admin xác nhận đơn hàng từ pending sang confirmed

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-VALID-01 |
| State variable | `status` |
| Actor | admin |
| Flow type | Valid transition |
| Covered guard/rule | Valid FR-10 transition; actor is allowed for this action. |
| Covered requirement | Luồng hợp lệ: `pending -> confirmed -> shipping -> delivered`. Source: README.md:141-162. |

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `pending`.
- Tài khoản `admin` đã đăng nhập và có quyền thực hiện thao tác.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current state | pending |
| Action / Event | Update order status |
| Requested state | confirmed |
| Endpoint / UI flow | PUT /api/admin/orders/:id/status |
| Body / Input | {"status": "confirmed"} |
| Entity ID | {existing_order_id} |

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

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/admin/orders/1/status` with SQLite fixture order `1`.
- Initial status: `pending`; expected final status: `confirmed`; actual final status: `confirmed`.
- HTTP status: `200`; response: `{'message': 'Order status updated'}`.
- Execution result: Passed.
