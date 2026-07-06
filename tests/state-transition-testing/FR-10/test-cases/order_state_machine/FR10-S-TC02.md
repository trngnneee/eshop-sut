# FR10-S-TC02: Admin giao hàng từ confirmed sang shipping

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-VALID-02 |
| State variable | `status` |
| Actor | admin |
| Flow type | Valid transition |
| Covered guard/rule | Valid FR-10 transition; actor is allowed for this action. |
| Covered requirement | Luồng hợp lệ: `pending -> confirmed -> shipping -> delivered`. Source: README.md:141-162. |

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `confirmed`.
- Tài khoản `admin` đã đăng nhập và có quyền thực hiện thao tác.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current state | confirmed |
| Action / Event | Update order status |
| Requested state | shipping |
| Endpoint / UI flow | PUT /api/admin/orders/:id/status |
| Body / Input | {"status": "shipping"} |
| Entity ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `confirmed`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "shipping"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 200.
- Trạng thái đơn hàng được cập nhật thành `shipping`.

## Status / Related bugs
Passed / None

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/admin/orders/2/status` with SQLite fixture order `2`.
- Initial status: `confirmed`; expected final status: `shipping`; actual final status: `shipping`.
- HTTP status: `200`; response: `{'message': 'Order status updated'}`.
- Execution result: Passed.
