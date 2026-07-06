# FR10-S-TC17: Từ chối Admin cập nhật pending sang chính pending

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-INVALID-10 |
| State variable | `status` |
| Actor | admin |
| Flow type | Invalid transition |
| Covered guard/rule | Invalid transition: no-op status update pending -> pending |
| Covered requirement | Mọi chuyển đổi không hợp lệ phải trả về lỗi với thông báo phù hợp. Source: README.md:141-162. |

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `pending`.
- Tài khoản `admin` đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current state | pending |
| Action / Event | Update order status |
| Requested state | pending |
| Endpoint / UI flow | PUT /api/admin/orders/:id/status |
| Body / Input | {"status": "pending"} |
| Entity ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `pending`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "pending"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `pending`.

## Status / Related bugs
Passed / None

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/admin/orders/17/status` with SQLite fixture order `17`.
- Initial status: `pending`; expected final status: `pending`; actual final status: `pending`.
- HTTP status: `400`; response: `{'error': 'Invalid state transition from pending to pending'}`.
- Execution result: Passed.
