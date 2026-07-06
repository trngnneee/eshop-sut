# FR10-S-TC10: Từ chối Admin chuyển ngược shipping sang confirmed

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-INVALID-03 |
| State variable | `status` |
| Actor | admin |
| Flow type | Invalid transition |
| Covered guard/rule | Invalid transition: shipping -> confirmed |
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
| Requested state | confirmed |
| Endpoint / UI flow | PUT /api/admin/orders/:id/status |
| Body / Input | {"status": "confirmed"} |
| Entity ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `shipping`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "confirmed"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `shipping`.

## Status / Related bugs
Passed / None

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/admin/orders/10/status` with SQLite fixture order `10`.
- Initial status: `shipping`; expected final status: `shipping`; actual final status: `shipping`.
- HTTP status: `400`; response: `{'error': 'Invalid state transition from shipping to confirmed'}`.
- Execution result: Passed.
