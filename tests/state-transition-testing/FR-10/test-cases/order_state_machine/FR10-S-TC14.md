# FR10-S-TC14: Từ chối User hủy lại đơn hàng đã canceled

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-INVALID-07 |
| State variable | `status` |
| Actor | user |
| Flow type | Final-state rejection |
| Covered guard/rule | Invalid final-state transition: canceled remains final for user |
| Covered requirement | `delivered` và `canceled` là final states, không được chuyển sang trạng thái khác. Source: README.md:141-162. |

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `canceled`.
- Tài khoản `user` đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Current state | canceled |
| Action / Event | Cancel order |
| Requested state | canceled |
| Endpoint / UI flow | PUT /api/orders/:id/cancel |
| Body / Input | [Không có body] |
| Entity ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `canceled`.
2. Đăng nhập bằng tài khoản `user` hợp lệ.
3. Gửi request `PUT /api/orders/:id/cancel`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `canceled`.

## Status / Related bugs
Passed / None

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/orders/14/cancel` with SQLite fixture order `14`.
- Initial status: `canceled`; expected final status: `canceled`; actual final status: `canceled`.
- HTTP status: `400`; response: `{'error': 'Cannot cancel this order.'}`.
- Execution result: Passed.
