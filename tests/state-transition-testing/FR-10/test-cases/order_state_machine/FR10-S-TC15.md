# FR10-S-TC15: Từ chối Admin chuyển delivered sang canceled

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-INVALID-08 |
| State variable | `status` |
| Actor | admin |
| Flow type | Final-state rejection |
| Covered guard/rule | Invalid final-state transition: delivered -> canceled by admin |
| Covered requirement | `delivered` và `canceled` là final states, không được chuyển sang trạng thái khác. Source: README.md:141-162. |

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `delivered`.
- Tài khoản `admin` đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current state | delivered |
| Action / Event | Update order status |
| Requested state | canceled |
| Endpoint / UI flow | PUT /api/admin/orders/:id/status |
| Body / Input | {"status": "canceled"} |
| Entity ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `delivered`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "canceled"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `delivered`.

## Status / Related bugs
Passed / None

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/admin/orders/15/status` with SQLite fixture order `15`.
- Initial status: `delivered`; expected final status: `delivered`; actual final status: `delivered`.
- HTTP status: `400`; response: `{'error': 'Invalid state transition from delivered to canceled'}`.
- Execution result: Passed.
