# FR10-S-TC11: Từ chối Admin hủy đơn hàng đang shipping

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-INVALID-04 |
| State variable | `status` |
| Actor | admin |
| Flow type | Invalid transition |
| Covered guard/rule | Invalid transition: shipping -> canceled |
| Covered requirement | Mọi chuyển đổi không hợp lệ phải trả về lỗi với thông báo phù hợp. Source: README.md:141-162. |

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `shipping`.
- Tài khoản `admin` đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current state | shipping |
| Action / Event | Update order status |
| Requested state | canceled |
| Endpoint / UI flow | PUT /api/admin/orders/:id/status |
| Body / Input | {"status": "canceled"} |
| Entity ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `shipping`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "canceled"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `shipping`.

## Status / Related bugs
Passed / None

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/admin/orders/11/status` with SQLite fixture order `11`.
- Initial status: `shipping`; expected final status: `shipping`; actual final status: `shipping`.
- HTTP status: `400`; response: `{'error': 'Invalid state transition from shipping to canceled'}`.
- Execution result: Passed.
