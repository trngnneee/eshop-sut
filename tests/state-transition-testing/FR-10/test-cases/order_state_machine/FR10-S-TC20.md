# FR10-S-TC20: Từ chối status null

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-INVALID-13 |
| State variable | `status` |
| Actor | admin |
| Flow type | Invalid transition |
| Covered guard/rule | Invalid status value: null |
| Covered requirement | Admin cập nhật trạng thái qua `PUT /api/admin/orders/:id/status` với 5 trạng thái hợp lệ. Source: api_specification.md:173-182. |

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `pending`.
- Admin đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current state | pending |
| Action / Event | Update order status |
| Requested state | null |
| Endpoint / UI flow | PUT /api/admin/orders/:id/status |
| Body / Input | {"status": null} |
| Entity ID | {existing_order_id} |

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

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/admin/orders/20/status` with SQLite fixture order `20`.
- Initial status: `pending`; expected final status: `pending`; actual final status: `pending`.
- HTTP status: `400`; response: `{'error': 'Invalid state transition from pending to null'}`.
- Execution result: Passed.
